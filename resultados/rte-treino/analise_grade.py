"""Analysis of a training grid: metrics per arm, paired differences by seed, gradient measures by group and by word.

Usage: uv run --frozen python resultados/rte-treino/analise_grade.py [csv_dir] [--saida md] [--titulo T]
       [--avaliacao TEXT] [--agrawal]
csv_dir defaults to resultados/rte-treino/pc (the CSVs copied from the PC); the report defaults to analise-grade.md
next to this file. The comparison is paired: within a warmup, the same seed gives the same batch order and head
initialization in every arm, so arm - baseline is taken seed by seed (t interval with n - 1 degrees of freedom). The
baseline of an arm is the same arm without its decoder (bert_decoder - bert, t5enc_decoder - t5enc).
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
METRICS = ["roc_auc", "accuracy", "f1_macro", "precision_at_0_7", "recall_at_0_7",
           "f1_entailment", "f1_not_entailment", "f1_neutral", "f1_contradiction"]
GROUPS = ["S", "F", "C", "N"]
STEPS = [1, 25, 175]  # plus every multiple of 100; 175 is the last measure of the RTE's phase B (ends at 187)
AGRAWAL_RTE = {"BERT (MS MARCO)": 0.4754, "+ Reasoning": 0.5873}  # Table 2 of the paper, ROC-AUC
MIN_WORD_COUNT = 5
DECODER = "_decoder"


def fmt(x: float, digits: int = 4) -> str:
    return "—" if pd.isna(x) else f"{x:.{digits}f}"


def interval(values: np.ndarray) -> tuple[float, float, float]:
    """Mean and 95% t interval; the interval is NaN with fewer than 2 values."""
    mean = float(np.mean(values))
    if len(values) < 2:
        return mean, float("nan"), float("nan")
    half = stats.t.ppf(0.975, len(values) - 1) * np.std(values, ddof=1) / np.sqrt(len(values))
    return mean, mean - half, mean + half


def metrics_table(res: pd.DataFrame, metrics: list[str]) -> list[str]:
    lines = ["| Braço | Aquecimento | n | " + " | ".join(metrics) + " | min/treino |", "|---|---|---|"
             + "---|" * (len(metrics) + 1)]
    for (arm, warmup), g in res.groupby(["arm", "warmup"]):
        cells = [f"{g[m].mean():.4f} ± {g[m].std(ddof=1):.4f}" if len(g) > 1 else f"{g[m].mean():.4f}"
                 for m in metrics]
        lines.append(f"| {arm} | {warmup} | {len(g)} | " + " | ".join(cells) + f" | {g['seconds'].mean() / 60:.1f} |")
    return lines


def paired_table(res: pd.DataFrame) -> list[str]:
    lines = ["| Braço − base | Aquecimento | sementes pareadas | Δ ROC-AUC (IC 95%) | vence em | Δ acurácia (IC 95%) |",
             "|---|---|---|---|---|---|"]
    for (arm, warmup), g in res[res.arm.str.endswith(DECODER)].groupby(["arm", "warmup"]):
        base_arm = arm.removesuffix(DECODER)
        base = res[res.arm == base_arm].set_index(["warmup", "seed"])
        joined = g.set_index(["warmup", "seed"]).join(base, rsuffix="_base", how="inner")
        if joined.empty:
            continue
        cells = []
        for m in ("roc_auc", "accuracy"):
            mean, lo, hi = interval((joined[m] - joined[f"{m}_base"]).to_numpy())
            cells.append(f"{mean:+.4f} ({fmt(lo, 4)}, {fmt(hi, 4)})")
        wins = int((joined["roc_auc"] > joined["roc_auc_base"]).sum())
        lines.append(f"| {arm} − {base_arm} | {warmup} | {len(joined)} | {cells[0]} | {wins}/{len(joined)} "
                     f"| {cells[1]} |")
    return lines


def measured_steps(steps: pd.Series) -> list[int]:
    return sorted(int(s) for s in steps.unique() if s in STEPS or s % 100 == 0)


def gradient_tables(grad: pd.DataFrame) -> list[str]:
    lines = []
    for (arm, warmup), g in grad.groupby(["arm", "warmup"]):
        mean = g[g.step.isin(measured_steps(g.step))].groupby("step").mean(numeric_only=True)
        lines += [f"#### {arm}, aquecimento {warmup} ({g.seed.nunique()} sementes)", "",
                  "| passo | L_aux/token | ‖g_c‖ | ‖g_a‖ | cos(g_c, g_a) | "
                  + " | ".join(f"{k}: tokens → parcela (cos)" for k in GROUPS) + " |",
                  "|---|---|---|---|---|" + "---|" * len(GROUPS)]
        for step, r in mean.iterrows():
            cells = [f"{r[f'frac_tokens_{k}']:.2f} → {r[f'share_{k}']:.2f} ({r[f'cos_c_{k}']:+.2f})" for k in GROUPS]
            lines.append(f"| {int(step)} | {r['l_aux']:.2f} | {r['norm_c']:.3f} | {r['norm_a']:.3f} "
                         f"| {r['cos_c_a']:+.3f} | " + " | ".join(cells) + " |")
        lines.append("")
    return lines


def word_tables(words: pd.DataFrame) -> list[str]:
    lines = []
    for (arm, warmup, step), g in words.groupby(["arm", "warmup", "step"]):
        total = g["align_t"].sum()
        by_group = g.groupby("group").agg(n=("word", "size"), align=("align_t", "sum"), norm=("norm_t", "mean"))
        lines += [f"#### {arm}, aquecimento {warmup}, passo {step}", "",
                  "| Grupo | ocorrências | parcela do alinhamento total | ‖g‖ médio por palavra |", "|---|---|---|---|"]
        for group in GROUPS:
            if group in by_group.index:
                r = by_group.loc[group]
                lines.append(f"| {group} | {int(r['n'])} | {r['align'] / total:+.2f} | {r['norm']:.4f} |")
        frequent = g.groupby(["word", "group"]).agg(n=("align_t", "size"), align=("align_t", "mean"))
        frequent = frequent[frequent.n >= MIN_WORD_COUNT].sort_values("align", ascending=False)
        top = ", ".join(f"{w} ({grp}, {a:+.4f})" for (w, grp), a in frequent["align"].head(10).items())
        bottom = ", ".join(f"{w} ({grp}, {a:+.4f})" for (w, grp), a in frequent["align"].tail(5).items())
        lines += ["", f"Mais alinhadas com a L_cls (≥ {MIN_WORD_COUNT} ocorrências, média): {top}", "",
                  f"Menos alinhadas: {bottom}", ""]
    return lines


def read(src: Path, name: str) -> pd.DataFrame:
    path = src / name
    return pd.read_csv(path, dtype={"warmup": str}) if path.exists() and path.stat().st_size else pd.DataFrame()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_dir", nargs="?", type=Path, default=HERE / "pc")
    parser.add_argument("--saida", type=Path, default=HERE / "analise-grade.md")
    parser.add_argument("--titulo", default="Análise da grade do RTE")
    parser.add_argument("--avaliacao", default="Avaliação no dev do RTE (277 pares), que faz o papel de teste.")
    parser.add_argument("--agrawal", action="store_true", help="add the paper's RTE reference (BERT arms on RTE)")
    args = parser.parse_args()
    src = args.csv_dir.resolve()
    res, grad, words = read(src, "resultados.csv"), read(src, "gradientes.csv"), read(src, "palavras.csv")
    metrics = [m for m in METRICS if m in res]
    reference = ["Referência do Agrawal (Tabela 2, ROC-AUC no RTE): "
                 + ", ".join(f"{k} {v:.4f}" for k, v in AGRAWAL_RTE.items())
                 + f" (Δ {AGRAWAL_RTE['+ Reasoning'] - AGRAWAL_RTE['BERT (MS MARCO)']:+.4f}).", ""] if args.agrawal else []
    out = [f"# {args.titulo}", "",
           f"Gerado por `analise_grade.py` sobre `{src.relative_to(ROOT)}`: {len(res)} treinos. "
           f"{args.avaliacao} Média ± desvio padrão entre sementes.", "",
           "## Métricas por braço", "", *metrics_table(res, metrics), "",
           "## Diferença pareada por semente contra o mesmo encoder sem decoder", "", *paired_table(res), "",
           *reference,
           "## Medidas de gradiente por grupo (média entre sementes)", "",
           "L_aux/token = perda da justificativa na sonda (64 pares do treino, fixos). Em cada célula de grupo: "
           "fração dos tokens do alvo no grupo → parcela do gradiente da L_aux que vem dele (cosseno com a L_cls). "
           "Parcela maior que a fração quer dizer que o grupo empurra o encoder mais do que o seu tamanho. As "
           "parcelas somam 1.", "", *(gradient_tables(grad) if not grad.empty else ["(sem medidas)", ""]),
           "## Influência por palavra (semente 1)", "",
           "align_t = quanto do empurrão da palavra no encoder aponta na direção da L_cls (positivo ajuda a "
           "classificar). A parcela do alinhamento total soma 1 sobre todas as palavras da sonda.", "",
           *(word_tables(words) if not words.empty else ["(sem medidas)", ""])]
    args.saida.write_text("\n".join(out), encoding="utf-8")
    print(f"{len(res)} treinos -> {args.saida}")


if __name__ == "__main__":
    main()
