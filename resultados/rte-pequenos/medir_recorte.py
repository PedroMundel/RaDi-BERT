"""Accuracy of each student inside and outside the cut of section 11.8, and each comparison of the criterion
(plan docs/2026-11-10-plano-teste-fora-da-distribuicao.md, "Critério dos braços com a cabeça de grupos", written
before any head arm existed).

The cut: the choice pairs whose Qwen rationale has a new word of one of the seven groups Pedro chose (17/11), by
the word -> group table built on the train pairs. Reads the per-pair hits medir_grupos_cls.py wrote.

Usage:  uv run --frozen --with umap-learn python resultados/rte-pequenos/medir_recorte.py [--sementes 1-5]
        (umap-learn only because medir_grupos_palavras.py, imported down the chain, imports it)
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from medir_grupos_cls import CUT_GROUPS, HEAD_ARMS
from medir_grupos_dependem_do_par import group_targets
from scipy import stats

from radibert import esnli_dados as esnli

HERE = Path(__file__).parent
PARTS = ("cut", "outside", "all")


def comparisons(arms: set[str]) -> list[tuple[str, str]]:
    """(arm, what it is compared with): the answers against nothing, and each head arm against its reference and
    against its swapped control."""
    pairs = [("answers", "none")]
    for name, arm in HEAD_ARMS.items():
        if arm.swapped:
            continue
        control = name.replace("head_all", "head_all_swapped").replace("head_cut", "head_cut_swapped")
        pairs += [(name, "answers" if arm.answers else "none"), (name, control)]
    return [(arm, base) for arm, base in pairs if {arm, base} <= arms]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sementes", default=None, help="first-last seed to read (default: every seed there)")
    args = parser.parse_args()
    choice = esnli.choice_split()[0]
    in_cut = group_targets(choice)[CUT_GROUPS].any(axis=1).to_numpy()
    hits = pd.read_csv(HERE / f"grupos-cls-acertos-esnli-{len(choice)}.csv", dtype={"hits": str})
    hits = hits[hits["split"] == "choice"]
    if args.sementes:
        first, last = (int(part) for part in args.sementes.split("-"))
        hits = hits[hits["seed"].between(first, last)]
    rows = []
    for row in hits.itertuples():
        right = np.array([char == "1" for char in row.hits])
        if len(right) != len(choice):
            raise SystemExit(f"{row.arm} seed {row.seed}: {len(right)} acertos para {len(choice)} pares")
        rows.append({"arm": row.arm, "seed": row.seed, "cut": 100 * right[in_cut].mean(),
                     "outside": 100 * right[~in_cut].mean(), "all": 100 * right.mean()})
    table = pd.DataFrame(rows)
    table.to_csv(HERE / "recorte-acuracias.csv", index=False)
    print(f"recorte: {int(in_cut.sum())} de {len(choice)} pares do conjunto de escolha; grupos {CUT_GROUPS}")
    by_seed = table.set_index(["arm", "seed"])
    gains = []
    for arm, base in comparisons(set(table["arm"])):
        gain = (by_seed.loc[arm] - by_seed.loc[base]).dropna()
        n = len(gain)
        half = stats.t.ppf(0.975, n - 1) / n ** 0.5
        row = {"arm": arm, "minus": base, "seeds": n}
        for part in PARTS:
            row |= {part: gain[part].mean(), f"{part}_half": half * gain[part].std(),
                    f"{part}_above": int((gain[part] > 0).sum())}
        gains.append(row)
    with pd.option_context("display.float_format", "{:.2f}".format, "display.width", 220):
        print("\nmedia e desvio padrao entre sementes, em pontos percentuais:")
        print(table.groupby("arm")[list(PARTS)].agg(["mean", "std"]).to_string())
        print("\ndiferenca semente a semente (media; _half = metade do intervalo de 95%; _above = sementes acima):")
        print(pd.DataFrame(gains).to_string(index=False))


if __name__ == "__main__":
    main()
