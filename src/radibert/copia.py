"""How much of a rationale is already written in the pair?

copia = |content words of the explanation that appear in the reference| / |content words of the explanation|

Reference = premise + hypothesis ("entrada") or the hypothesis alone ("hipotese").
Control: the same measure against the input of another, randomly drawn pair ("controle").
Content words: lowercase letters only, sklearn English stop words, one-letter tokens and contraction
fragments removed, no lemmatization.
META words (premise, hypothesis, true...) are removed from explanations too, so the LLMs' boilerplate
does not count as "new information".

Usage: python -m radibert.copia
"""
import re
from collections import Counter

import pandas as pd
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

from radibert.paths import COPIA, ESNLI_DEV, PILOTO_PROFESSORES

CSV_DEV = ESNLI_DEV
CSV_PILOT = PILOTO_PROFESSORES / "resultados.csv"
OUT = COPIA / "copia-numeros.md"
SEED = 0

META = {
    "premise", "hypothesis", "sentence", "statement", "true", "false", "guarantee", "guarantees",
    "guaranteed", "imply", "implies", "implied", "follow", "follows", "scene", "described", "describes",
    "describe", "say", "says", "state", "states", "stated", "label",
}
# Fragments left by contractions ("doesn't" -> "doesn" + "t") and auxiliaries sklearn keeps.
CONTRACTIONS = {"doesn", "isn", "don", "didn", "aren", "wasn", "weren", "couldn", "shouldn", "wouldn", "does", "did"}
DROP = ENGLISH_STOP_WORDS | META | CONTRACTIONS


def words(text) -> set[str]:
    return {w for w in re.findall(r"[a-z]+", str(text).lower()) if len(w) > 1 and w not in DROP}


def copy_fraction(explanation, reference):
    exp = words(explanation)
    if not exp:
        return None
    return len(exp & words(reference)) / len(exp)


def new_words(explanation, reference) -> int:
    return len(words(explanation) - words(reference))


def measure(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Copy measures of one explanation column; df must have Sentence1, Sentence2, gold_label."""
    entrada = (df["Sentence1"] + " " + df["Sentence2"]).to_numpy()
    hipotese = df["Sentence2"].to_numpy()
    other = df.sample(frac=1, random_state=SEED)
    entrada_outro = (other["Sentence1"] + " " + other["Sentence2"]).to_numpy()
    exps = df[col].to_numpy()
    return pd.DataFrame({
        "gold_label": df["gold_label"].to_numpy(),
        "entrada": [copy_fraction(e, r) for e, r in zip(exps, entrada)],
        "hipotese": [copy_fraction(e, r) for e, r in zip(exps, hipotese)],
        "controle": [copy_fraction(e, r) for e, r in zip(exps, entrada_outro)],
        "novas": [new_words(e, r) for e, r in zip(exps, entrada)],
        "total100": [copy_fraction(e, r) == 1 for e, r in zip(exps, entrada)],
    })


def summary(m: pd.DataFrame) -> dict:
    valid = m.dropna(subset=["entrada"])
    return {
        "n": len(valid),
        "sem_conteudo": int(m["entrada"].isna().sum()),
        "copia_entrada": valid["entrada"].mean(),
        "copia_hipotese": valid["hipotese"].mean(),
        "controle": valid["controle"].mean(),
        "100%_copiada": valid["total100"].mean(),
        "palavras_novas_mediana": valid["novas"].median(),
    }


def fmt(rows: dict[str, dict]) -> str:
    cols = ["n", "sem_conteudo", "copia_entrada", "copia_hipotese", "controle", "100%_copiada",
            "palavras_novas_mediana"]
    lines = ["| fonte | " + " | ".join(cols) + " |", "|---" * (len(cols) + 1) + "|"]
    for name, s in rows.items():
        cells = [f"{s[c]:.1%}" if isinstance(s[c], float) and c not in ("palavras_novas_mediana",) else f"{s[c]:g}"
                 for c in cols]
        lines.append(f"| {name} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def by_label(measures: dict[str, pd.DataFrame], field: str) -> str:
    table = pd.DataFrame({name: m.dropna(subset=["entrada"]).groupby("gold_label")[field].mean()
                          for name, m in measures.items()})
    return table.map(lambda v: f"{v:.1%}").to_markdown()


def top_new(df: pd.DataFrame, col: str, k: int = 12) -> str:
    counts = Counter()
    for exp, s1, s2 in zip(df[col], df["Sentence1"], df["Sentence2"]):
        counts.update(words(exp) - words(f"{s1} {s2}"))
    return ", ".join(f"{w} ({n})" for w, n in counts.most_common(k))


def main():
    dev = pd.read_csv(CSV_DEV)
    long = dev.melt(id_vars=["pairID", "gold_label", "Sentence1", "Sentence2"],
                    value_vars=["Explanation_1", "Explanation_2", "Explanation_3"], value_name="exp")
    pilot = pd.read_csv(CSV_PILOT)

    all_human = {"humano (9.842 pares × 3)": measure(long, "exp")}
    same_pairs = {name: measure(pilot, col) for name, col in
                  [("humano", "Explanation_1"), ("haiku", "haiku"), ("sonnet", "sonnet")]}

    report = [
        "# Cópia: números (gerado por `copia.py`)", "",
        "## A. Todas as explicações humanas da validação", "", fmt({k: summary(v) for k, v in all_human.items()}), "",
        "## B. Os mesmos 1.000 pares do piloto: humano × Haiku × Sonnet", "",
        fmt({k: summary(v) for k, v in same_pairs.items()}), "",
        "### Cópia da entrada por rótulo", "", by_label(same_pairs, "entrada"), "",
        "### Cópia só da hipótese por rótulo", "", by_label(same_pairs, "hipotese"), "",
        "### Palavras novas mais frequentes (não estão no par)", "",
        *[f"- **{name}:** {top_new(pilot, col)}" for name, col in
          [("humano", "Explanation_1"), ("haiku", "haiku"), ("sonnet", "sonnet")]], "",
    ]
    OUT.write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))


if __name__ == "__main__":
    main()
