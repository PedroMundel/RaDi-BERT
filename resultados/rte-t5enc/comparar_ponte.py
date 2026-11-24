"""Bridge test: L_aux per token, by group, of the decoder reading BERT (bert_decoder) and of the decoder reading its
own encoder (t5enc_decoder), on the same 64 train probe pairs and the same t5-base tokenization of the targets.

Usage: uv run --frozen python resultados/rte-t5enc/comparar_ponte.py   (reads pc/ in rte-treino and rte-t5enc)
Prints a markdown table; the decoders are T5 base from different checkpoints (t5-base and t5-v1_1-base).
"""
from pathlib import Path

import pandas as pd

RESULTADOS = Path(__file__).resolve().parents[1]
SOURCES = {"bert_decoder": RESULTADOS / "rte-treino" / "pc" / "gradientes.csv",
           "t5enc_decoder": RESULTADOS / "rte-t5enc" / "pc" / "gradientes.csv"}
COLUMNS = ["l_aux", "l_S", "l_F", "l_C", "l_N", "cos_c_a"]
STEPS = [1, 25, 100, 175, 200, 300, 400, 500, 600]


def main():
    rows = []
    for arm, path in SOURCES.items():
        g = pd.read_csv(path, dtype={"warmup": str})
        g = g[(g.arm == arm) & (g.warmup == "prop") & g.step.isin(STEPS)]
        mean = g.groupby("step")[COLUMNS].mean()
        mean.insert(0, "seeds", g.groupby("step").seed.nunique())
        rows.append(mean.add_prefix(f"{arm}:"))
    table = pd.concat(rows, axis=1)
    print("| passo | " + " | ".join(table.columns) + " |")
    print("|---|" + "---|" * len(table.columns))
    for step, r in table.iterrows():
        print(f"| {step} | " + " | ".join(f"{v:.3f}" if isinstance(v, float) else str(v) for v in r) + " |")


if __name__ == "__main__":
    main()
