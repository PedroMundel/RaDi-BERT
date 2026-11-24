"""Reads the out-of-domain test and the panel against their criteria (docs/2026-11-18-gaps-da-argumentacao.md,
"Gap 7" and "Gap 8"): means per arm and paired differences by seed with the 95% t interval.

    uv run --frozen python resultados/esnli-treino-16k/ler_fora.py [pc|amigo ...]

Reads the copies under resultados/esnli-treino-16k*-fora-pesos/<machine>/ (resultados.csv, mnli-hans.csv, painel.csv),
every machine given, and prints nothing it does not compute from those files.
"""
import sys

import pandas as pd
from scipy import stats

from radibert.paths import RESULTADOS

PARTS = ("", "-calendario", "-embaralhado")
REFERENCE = {"bert": 0.834, "bert_calendar": 0.837, "bert_decoder": 0.828, "bert_decoder_shuffled": 0.807}  # 18/11
COMPARISONS = [("bert_decoder", "bert_calendar"), ("bert_decoder", "bert_decoder_shuffled"),
               ("bert_calendar", "bert")]
MEASURES = ["accuracy", "mnli_accuracy", "mnli_roc_auc", "mnli_matched_accuracy", "mnli_mismatched_accuracy",
            "fora_roc_auc", "fora_accuracy", "hans_non_entailment_accuracy", "hans_accuracy",
            "dev_ece", "mnli_ece", "dev_confidence_auroc", "mnli_confidence_auroc", "dev_coverage_at_95",
            "dev_worst_f1", "mnli_worst_f1", "dev_recall_entailment", "dev_recall_neutral", "dev_recall_contradiction"]


def read(machine: str) -> pd.DataFrame:
    """One row per arm and seed of a machine, with every column its three files have."""
    tables = {}
    for name in ("resultados", "mnli-hans", "painel"):
        frames = [pd.read_csv(path) for part in PARTS
                  if (path := RESULTADOS / f"esnli-treino-16k{part}-fora-pesos" / machine / f"{name}.csv").exists()]
        if frames:
            tables[name] = pd.concat(frames, ignore_index=True)
    runs = tables["resultados"]
    for name in ("mnli-hans", "painel"):
        if name in tables:
            new = [c for c in tables[name].columns if c not in runs.columns or c in ("arm", "seed")]
            runs = runs.merge(tables[name][new], on=["arm", "seed"], how="left")
    return runs.assign(machine=machine)


def paired(runs: pd.DataFrame, a: str, b: str, column: str) -> str:
    x = runs[runs["arm"] == a].set_index("seed")[column]
    y = runs[runs["arm"] == b].set_index("seed")[column]
    d = (x - y).dropna()
    if len(d) < 2:
        return f"{column}: sem sementes pareadas"
    half = stats.t.ppf(0.975, len(d) - 1) * d.std(ddof=1) / len(d) ** 0.5
    return (f"{column}: {d.mean():+.4f} ({d.mean() - half:+.4f} a {d.mean() + half:+.4f}), metade {half:.4f}, "
            f"positivo em {(d > 0).sum()} de {len(d)}")


def main():
    machines = sys.argv[1:] or ["pc"]
    runs = pd.concat([read(m) for m in machines], ignore_index=True)
    have = [m for m in MEASURES if m in runs.columns]
    pd.set_option("display.width", 250)
    print(runs.groupby(["machine", "arm"])[have].mean().round(4).T.to_string())
    print("\nsementes:", runs.groupby(["machine", "arm"])["seed"].apply(sorted).to_dict())
    print("\nconferência 1 (acurácia no dev menos a de 18/11, em pontos; limite 0,6):")
    for (machine, arm), acc in runs.groupby(["machine", "arm"])["accuracy"].mean().items():
        print(f"  {machine} {arm}: {100 * (acc - REFERENCE[arm]):+.2f}")
    if "dev_accuracy_reloaded" in runs:
        print("conferência 2 (maior diferença recarregado menos gravado):",
              f"{(runs['dev_accuracy_reloaded'] - runs['accuracy']).abs().max():.5f}")
    # an arm trained on two machines (the calendar anchor) enters the comparisons from the first machine given
    first = runs.drop_duplicates(subset=["arm", "seed"], keep="first")
    for a, b in COMPARISONS:
        print(f"\n{a} menos {b}")
        for column in have:
            print("  " + paired(first, a, b, column))
    if len(machines) > 1:
        print("\nâncora de máquina: bert_calendar, amigo menos pc")
        both = runs[runs["arm"] == "bert_calendar"].assign(arm=lambda f: f["arm"] + "@" + f["machine"])
        for column in have:
            print("  " + paired(both, "bert_calendar@amigo", "bert_calendar@pc", column))


if __name__ == "__main__":
    main()
