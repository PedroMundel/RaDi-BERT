"""The seven-groups arm against nothing and against its swapped control, by how hard a pair is and by label
(plan docs/2026-11-10-plano-teste-fora-da-distribuicao.md, section 11.9, written before reading the dev by subset).

How hard a pair is = how many of the 15 "answers" students get it right on that split (an arm that is neither side
of the comparisons). Reads the per-pair hits medir_grupos_cls.py wrote; trains nothing.

Usage:  uv run --frozen python resultados/rte-pequenos/medir_dificeis.py --split dev
        (--split choice gives the exploratory table of 18/11 back: the check that this script counts the same way)
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from radibert import esnli_dados as esnli

HERE = Path(__file__).parent
HITS = HERE / f"grupos-cls-acertos-esnli-{esnli.N_TRAIN}.csv"
ARM, BASES, DIFFICULTY_ARM = "head_cut", ("none", "head_cut_swapped"), "answers"
BANDS = {"faceis (13 a 15)": (13, 15), "medios (3 a 12)": (3, 12), "dificeis (0 a 2)": (0, 2)}


def hits_of(split: str) -> dict[str, pd.DataFrame]:
    """arm -> one row per seed, one column per pair, True where the student is right."""
    table = pd.read_csv(HITS, dtype={"hits": str})
    table = table[table["split"] == split]
    return {arm: pd.DataFrame({row.seed: [char == "1" for char in row.hits] for row in rows.itertuples()}).T.sort_index()
            for arm, rows in table.groupby("arm")}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--split", choices=("dev", "choice"), required=True)
    args = parser.parse_args()
    pairs = esnli.dev_pairs() if args.split == "dev" else esnli.choice_split()[0]
    hits = hits_of(args.split)
    seeds = hits[DIFFICULTY_ARM].index
    for arm in (ARM, *BASES):
        if list(hits[arm].index) != list(seeds) or hits[arm].shape[1] != len(pairs):
            raise SystemExit(f"{arm}: sementes {list(hits[arm].index)}, {hits[arm].shape[1]} acertos para {len(pairs)} pares")
    if pairs["y"].isna().any():
        raise SystemExit("par sem rotulo")
    right_count = hits[DIFFICULTY_ARM].sum(axis=0).to_numpy()
    subsets = {name: (right_count >= low) & (right_count <= high) for name, (low, high) in BANDS.items()}
    subsets |= {f"rotulo {name}": (pairs["y"] == y).to_numpy() for y, name in esnli.LABELS.items()}
    subsets["geral"] = np.ones(len(pairs), dtype=bool)
    half = stats.t.ppf(0.975, len(seeds) - 1) / len(seeds) ** 0.5
    rows = []
    for name, mask in subsets.items():
        accuracy = {arm: 100 * hits[arm].loc[:, mask].mean(axis=1) for arm in (ARM, *BASES)}
        row = {"subconjunto": name, "pares": int(mask.sum()), "acerto_none": accuracy["none"].mean()}
        for base in BASES:
            gain = accuracy[ARM] - accuracy[base]
            row |= {f"menos_{base}": gain.mean(), f"menos_{base}_half": half * gain.std(),
                    f"menos_{base}_above": int((gain > 0).sum())}
        rows.append(row)
    print(f"{args.split}: {len(pairs)} pares, {len(seeds)} sementes ({seeds.min()} a {seeds.max()}); "
          f"{ARM} menos cada base, em pontos percentuais; _half = metade do intervalo de 95%; _above = sementes acima")
    with pd.option_context("display.float_format", "{:.2f}".format, "display.width", 220):
        print(pd.DataFrame(rows).to_string(index=False))


if __name__ == "__main__":
    main()
