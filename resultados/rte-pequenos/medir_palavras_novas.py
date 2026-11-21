"""How much do the rationale's new words say about the label? (plan
docs/2026-11-10-plano-teste-fora-da-distribuicao.md, section 11.6, written before this ran; Pedro's hypothesis, 17/11.)

No BERT here: a logistic regression on word presence (a word seen in 2 pairs or more is one 0/1 column), 5-fold
cross-validated accuracy on the 4,000 e-SNLI train pairs, one model per set of words:
  N           the rationale's new words (not in the pair, not a function word, not a label expression)
  S, C, F     its label expressions, the words it copies from the pair, its function words
  rationale   every word of the rationale
  pair        the words of the premise and the hypothesis: what the encoder already reads
  pair+N      the pair's words and the new words, each in its own columns: what N adds to the input

Usage:  uv run --frozen python resultados/rte-pequenos/medir_palavras_novas.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.sparse import hstack
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict

from radibert import esnli_dados as esnli
from radibert import rte_gradientes as grads

HERE = Path(__file__).parent
FOLDS, FOLD_SEED, MIN_PAIRS = 5, 0, 2


def presence(texts: list[list[str]]):
    """One 0/1 column per word present in MIN_PAIRS pairs or more."""
    return CountVectorizer(analyzer=lambda words: words, binary=True, min_df=MIN_PAIRS).fit_transform(texts)


def main():
    pairs = esnli.training_pairs()
    label_expr = grads.expression_pattern(grads.expression_table(pairs, esnli.LABELS))
    words = {name: [] for name in ("N", "S", "C", "F", "rationale", "pair")}
    for premise, hypothesis, rationale in zip(pairs["sentence1"], pairs["sentence2"], pairs["rationale"]):
        grouped = grads.word_groups(rationale, premise, hypothesis, label_expr)
        for group in grads.Group:
            words[group.name].append([word for _, _, word, g in grouped if g == group])
        words["rationale"].append([word for _, _, word, _ in grouped])
        words["pair"].append(grads.words_of(f"{premise} {hypothesis}"))
    y = pairs["y"].to_numpy()
    features = {name: presence(texts) for name, texts in words.items()}
    features["pair+N"] = hstack([features["pair"], features["N"]]).tocsr()
    folds = StratifiedKFold(FOLDS, shuffle=True, random_state=FOLD_SEED)
    rows = [{"words": "majority class", "columns": 0, "words_per_pair": 0.0, "pairs_with_none": 0,
             "accuracy": float(np.bincount(y).max() / len(y))}]
    for name, x in features.items():
        predicted = cross_val_predict(LogisticRegression(max_iter=2000), x, y, cv=folds)
        counts = [len(texts) for texts in words[name]] if name in words else []
        rows.append({"words": name, "columns": x.shape[1],
                     "words_per_pair": float(np.mean(counts)) if counts else float("nan"),
                     "pairs_with_none": int(sum(count == 0 for count in counts)) if counts else -1,
                     "accuracy": float((predicted == y).mean())})
        by_label = {esnli.LABELS[label]: round(float((predicted[y == label] == label).mean()), 3)
                    for label in sorted(esnli.LABELS)}
        print(f"{name:10s} colunas {x.shape[1]:5d} acuracia {rows[-1]['accuracy']:.3f} por rotulo {by_label}", flush=True)
    out = HERE / "palavras-novas-esnli-4000.csv"
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f"completo {out}")


if __name__ == "__main__":
    main()
