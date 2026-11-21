"""Figure 30 (19/11): the decoder against the calendar arm inside the domain, outside it, on the panel measures and
across the decoder-loss weights. Every number is read from the copied result files (the same ler_fora.py and
ler_peso.py read); nothing is typed in.

    uv run --frozen --with matplotlib python resultados/figuras/figura_fora_painel.py
"""
from pathlib import Path

import matplotlib
import pandas as pd
from scipy import stats

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RESULTADOS = Path(__file__).resolve().parents[1]
OUT = Path(__file__).with_name("30-fora-de-dominio-painel-e-peso.png")


def folder(part: str, machine: str) -> pd.DataFrame:
    """One row per arm and seed of a folder, with the scoring columns of the machine joined in."""
    runs = pd.read_csv(RESULTADOS / f"esnli-treino-16k{part}" / machine / "resultados.csv")
    for where in (RESULTADOS / f"esnli-treino-16k{part}" / machine, RESULTADOS / "esnli-treino-16k-fora-pesos" / machine):
        for name in ("mnli-hans", "painel"):
            if (where / f"{name}.csv").exists():
                extra = pd.read_csv(where / f"{name}.csv")
                new = [c for c in extra.columns if c not in runs.columns or c in ("arm", "seed")]
                runs = runs.merge(extra[new], on=["arm", "seed"], how="left")
    return runs


def paired(x: pd.Series, y: pd.Series, scale: float = 100.0) -> tuple[float, float, int]:
    d = ((x - y) * scale).dropna()
    return d.mean(), stats.t.ppf(0.975, len(d) - 1) * d.std(ddof=1) / len(d) ** 0.5, len(d)


def column(runs: pd.DataFrame, arm: str, name: str) -> pd.Series:
    return runs[runs["arm"] == arm].set_index("seed")[name]


def main():
    pc = pd.concat([folder("-fora-pesos", "pc"), folder("-calendario-fora-pesos", "pc")], ignore_index=True)
    # (label, column, sign): sign -1 turns "smaller is better" into "right is better"
    measures = [("Acurácia no dev do e-SNLI (dentro)", "accuracy", 1), ("Acurácia no MNLI (fora)", "mnli_accuracy", 1),
                ("Acurácia no RTE (fora)", "fora_accuracy", 1), ("Calibração: ECE no dev, sinal invertido", "dev_ece", -1),
                ("Predição seletiva: ROC-AUC da confiança", "dev_confidence_auroc", 1),
                ("Pior classe: menor F1 no dev", "dev_worst_f1", 1)]
    fig, (left, right) = plt.subplots(1, 2, figsize=(13, 4.6), gridspec_kw={"width_ratios": [1.5, 1]})
    for row, (_, name, sign) in enumerate(reversed(measures)):
        mean, half, n = paired(column(pc, "bert_decoder", name), column(pc, "bert_calendar", name), 100.0 * sign)
        left.errorbar(mean, row, xerr=half, fmt="o", color="#b3541e", capsize=4)
        left.text(mean, row + 0.22, f"{mean:+.1f} (n={n})", ha="center", fontsize=8)
    left.set_yticks(range(len(measures)), [m[0] for m in reversed(measures)])
    left.axvline(0, color="gray", linestyle="--", linewidth=1)
    left.set_xlabel("Decoder menos calendário, em pontos (à direita da linha o decoder é melhor)")
    left.set_title("Com decoder contra sem decoder, mesmo calendário, 5 sementes")

    weights = [("0", folder("-fora-pesos-aux-0", "pc"), pc), ("0,05", folder("-fora-pesos-aux-0.05", "pc"), pc),
               ("0,1", pc, pc), ("0,5", folder("-fora-pesos-aux-0.5", "amigo"), folder("-calendario-fora-pesos", "amigo"))]
    for position, (_, swept, base) in enumerate(weights):
        x = column(swept, "bert_decoder", "accuracy")
        y = column(base, "bert_calendar", "accuracy")
        y = y[y.index.isin(x.index)]
        mean, half, n = paired(x, y)
        right.errorbar(position, mean, yerr=half, fmt="o", color="#b3541e", capsize=4)
        right.text(position + 0.08, mean, f"{mean:+.1f}\n(n={n})", fontsize=8, va="center")
    right.set_xticks(range(len(weights)), [w[0] for w in weights])
    right.set_xlim(-0.5, len(weights) - 0.2)
    right.axhline(0, color="gray", linestyle="--", linewidth=1)
    right.set_xlabel("Peso da perda do decoder durante a classificação")
    right.set_ylabel("Acurácia no dev menos o calendário (pontos)")
    right.set_title("Variando o peso do decoder")
    fig.tight_layout()
    fig.savefig(OUT, dpi=150)
    print("saved", OUT)


if __name__ == "__main__":
    main()
