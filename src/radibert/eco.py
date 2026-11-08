"""Echo mark for the batch: an entailment pair whose hypothesis has no content word missing from the premise.

In those pairs there is nothing to explain beyond repeating the hypothesis, so the rationale tends to be an echo
(docs/2026-10-21-pesquisa-eco-justificativa.md). The rule is lexical and uses the content words of
src/radibert/copia.py (no lemmatization, so "boy" and "boys" differ and echo is undercounted).

Writes marcas.csv (pairID, novas_hipotese, eco) next to the batch; the batch file itself is not touched.
Usage: python -m radibert.eco       # marks the batch
       python -m radibert.eco dev      # same rule on the e-SNLI dev, to check against the 21/10 count
"""
import sys

import pandas as pd

from radibert.copia import new_words
from radibert.paths import ESNLI_DEV, LOTE_35B

BATCH = LOTE_35B / "racionalizacoes-F-35B.csv"
DEV = ESNLI_DEV
OUT = LOTE_35B / "marcas.csv"


def mark(df: pd.DataFrame) -> pd.DataFrame:
    novas = [new_words(h, p) for p, h in zip(df["Sentence1"], df["Sentence2"])]
    out = pd.DataFrame({"pairID": df["pairID"], "gold_label": df["gold_label"], "novas_hipotese": novas})
    out["eco"] = (out["gold_label"] == "entailment") & (out["novas_hipotese"] == 0)
    return out


def summary(m: pd.DataFrame, name: str):
    share = pd.crosstab(m["gold_label"], m["novas_hipotese"].clip(upper=3), normalize="index").round(3)
    print(f"{name}: {len(m)} pares, eco = {m['eco'].sum()} ({m['eco'].mean():.1%} do total, "
          f"{m.loc[m.gold_label == 'entailment', 'eco'].mean():.1%} das implicações)")
    print(share.rename(columns={3: "3+"}).to_string())


if __name__ == "__main__":
    if sys.argv[1:] == ["dev"]:
        summary(mark(pd.read_csv(DEV)), "dev")
    else:
        marks = mark(pd.read_csv(BATCH))
        marks.drop(columns="gold_label").to_csv(OUT, index=False)
        summary(marks, "lote")
        print(f"-> {OUT}")
