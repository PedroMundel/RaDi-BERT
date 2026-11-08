"""Surface measures of the Qwen variants on the same 45 pairs, one script for every column.

Usage: python -m radibert.medir_variantes E E3 F # any variants with a resultados-<v>.csv here
       python -m radibert.medir_variantes F-9B-90 vazao-paralelo/resultados-F-9B-90-kvu-w8.csv   # or a csv path
"""
import re
import sys

import pandas as pd

from radibert.copia import copy_fraction
from radibert.paths import PILOTO_QWEN

PILOT = PILOTO_QWEN
LABEL = re.compile(r"\b(entail\w*|neutral|contradict\w*)\b", re.I)
META = re.compile(r"\b(premise|hypothesis|statement|the question)\b", re.I)
RELATION = re.compile(r"\b(contradict\w*|confirm\w*|support\w*|entail\w*|satisf\w*|consistent with|guarantee\w*|"
                      r"impl(y|ies|ied)|mutually exclusive|incompatible|directly|explicitly|"
                      r"which means|therefore|thus)\b", re.I)
TEXT_ABOUT_TEXT = re.compile(r"describ|\bstated?\b|\bstates\b|mention", re.I)
SAME_MOMENT = re.compile(r"simultaneous|same (?:time|moment|place|scene)", re.I)

cols = {}
human = None
for v in sys.argv[1:]:  # a variant name, or a .csv path relative to resultados/piloto-qwen (e.g. a vazao-paralelo run)
    df = pd.read_csv(PILOT / (v if v.endswith(".csv") else f"resultados-{v}.csv"), index_col="idx")
    cols[f"Qwen {v}"] = df["qwen"]
    human = df
cols = {"Humano": human["Explanation_1"], **cols}

rows = {}
for name, s in cols.items():
    n = s.str.split().str.len()
    rows[name] = {
        "Palavras (mediana / máx.)": f"{n.median():.0f} / {n.max()}",
        "Palavras por rótulo (impl. / neutro / contr.)": " / ".join(
            f"{n[human.gold_label == lab].median():.0f}" for lab in ("entailment", "neutral", "contradiction")),
        "Uma frase só": int((s.str.count(r"[.!?](\s|$)") <= 1).sum()),
        "Acima de 30 palavras": int((n > 30).sum()),
        "Nomeia o rótulo": int(s.str.contains(LABEL).sum()),
        "Palavra de relação (lista)": int(s.str.contains(RELATION).sum()),
        "Fala de premise/hypothesis": int(s.str.contains(META).sum()),
        "Texto sobre o texto (describes, stated, mentions)": int(s.str.contains(TEXT_ABOUT_TEXT).sum()),
        "Simultaneamente / mesmo lugar ou momento": int(s.str.contains(SAME_MOMENT).sum()),
        "Cópia do par (mediana)": f"{pd.Series([copy_fraction(e, p + ' ' + h) for e, p, h in zip(s, human.Sentence1, human.Sentence2)]).median():.2f}",
    }
table = pd.DataFrame(rows)
print(table.to_markdown())
for name in list(cols)[1:]:
    hits = cols[name][cols[name].str.contains(RELATION)]
    print(f"\n{name} relation hits:", {i: RELATION.findall(t)[0][0] for i, t in hits.items()})
