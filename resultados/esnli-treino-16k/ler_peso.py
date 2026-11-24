"""Reads the decoder-loss weight sweep against its criterion (docs/2026-11-18-gaps-da-argumentacao.md, "Gap 9"):
each weight against the calendar arm of the same machine, on the seeds both have, paired by seed, 95% t interval.

    uv run --frozen python resultados/esnli-treino-16k/ler_peso.py

Reads resultados/esnli-treino-16k-fora-pesos-aux-<weight>/<machine>/ and the calendar and decoder (weight 0.1) copies
of the same machine under resultados/esnli-treino-16k*-fora-pesos/<machine>/.
"""
import pandas as pd
from scipy import stats

from radibert.paths import RESULTADOS

MEASURES = ["accuracy", "mnli_accuracy", "fora_roc_auc", "dev_ece", "dev_confidence_auroc", "dev_worst_f1"]


def read(folder) -> pd.DataFrame | None:
    """One row per arm and seed of a folder, joining the three files it may have."""
    if not (folder / "resultados.csv").exists():
        return None
    runs = pd.read_csv(folder / "resultados.csv")
    for name in ("mnli-hans", "painel"):
        if (folder / f"{name}.csv").exists():
            extra = pd.read_csv(folder / f"{name}.csv")
            new = [c for c in extra.columns if c not in runs.columns or c in ("arm", "seed")]
            runs = runs.merge(extra[new], on=["arm", "seed"], how="left")
    return runs


def arm(machine: str, part: str, name: str) -> pd.DataFrame | None:
    """An arm of a machine: one of the two files below holds it (the scoring files sit in the first folder)."""
    runs = read(RESULTADOS / f"esnli-treino-16k{part}-fora-pesos" / machine)
    scores = read_scores(machine)
    if runs is None:
        return None
    runs = runs[runs["arm"] == name]
    if scores is not None:
        new = [c for c in scores.columns if c not in runs.columns or c in ("arm", "seed")]
        runs = runs.merge(scores[new], on=["arm", "seed"], how="left")
    return runs.set_index("seed")


def read_scores(machine: str) -> pd.DataFrame | None:
    folder = RESULTADOS / "esnli-treino-16k-fora-pesos" / machine
    frames = [pd.read_csv(folder / f"{name}.csv") for name in ("mnli-hans", "painel") if (folder / f"{name}.csv").exists()]
    if not frames:
        return None
    scores = frames[0]
    for extra in frames[1:]:
        new = [c for c in extra.columns if c not in scores.columns or c in ("arm", "seed")]
        scores = scores.merge(extra[new], on=["arm", "seed"], how="outer")
    return scores


def paired(x: pd.Series, y: pd.Series) -> str:
    d = (x - y).dropna()
    if len(d) < 2:
        return "sem sementes pareadas"
    half = stats.t.ppf(0.975, len(d) - 1) * d.std(ddof=1) / len(d) ** 0.5
    return f"{d.mean():+.4f} ({d.mean() - half:+.4f} a {d.mean() + half:+.4f}), positivo em {(d > 0).sum()} de {len(d)}"


def main():
    for folder in sorted(RESULTADOS.glob("esnli-treino-16k-fora-pesos-aux-*")):
        weight = folder.name.rsplit("-aux-", 1)[1]
        for machine_dir in sorted(p for p in folder.iterdir() if p.is_dir() and p.name in ("pc", "amigo")):
            machine = machine_dir.name
            swept = read(machine_dir)
            if swept is None:
                continue
            swept = swept.set_index("seed")
            calendar = arm(machine, "-calendario", "bert_calendar")
            paper = arm(machine, "", "bert_decoder")
            print(f"\npeso {weight}, {machine}, sementes {sorted(swept.index)}")
            for m in [m for m in MEASURES if m in swept.columns]:
                line = f"  {m}: média {swept[m].mean():.4f}"
                if calendar is not None and m in calendar.columns:
                    line += (f" | calendário {calendar.loc[calendar.index.isin(swept.index), m].mean():.4f}"
                             f" | menos calendário {paired(swept[m], calendar[m])}")
                if paper is not None and len(paper) and m in paper.columns:
                    line += f" | menos peso 0,1: {paired(swept[m], paper[m])}"
                print(line)


if __name__ == "__main__":
    main()
