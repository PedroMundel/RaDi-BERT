"""Do the rationale's word groups depend on the pair, or only on the label? (plan
docs/2026-11-10-plano-teste-fora-da-distribuicao.md, section 11.8, stage 1, written before this ran.)

No BERT: for each of the 29 HDBSCAN groups of new words (section 11.7), two logistic regressions predict whether
the group shows up in the pair's rationale, one seeing only the gold label, the other the gold label and the pair's
own words (presence). ROC-AUC, 5-fold cross-validated, on the 4,000 e-SNLI train pairs.

Usage:  uv run --frozen --with umap-learn python resultados/rte-pequenos/medir_grupos_dependem_do_par.py
        (umap-learn only because medir_grupos_palavras.py, imported for the word spans, imports it)
"""
from pathlib import Path

import numpy as np
import pandas as pd
from medir_grupos_palavras import NO_GROUP, new_word_spans
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict

from radibert import esnli_dados as esnli
from radibert import rte_gradientes as grads

HERE = Path(__file__).parent
FOLDS, SEED, MIN_PAIRS = 5, 0, 2


def group_targets(pairs: pd.DataFrame) -> pd.DataFrame:
    """One 0/1 column per group: does any new word of the pair's rationale belong to it?"""
    group_of = pd.read_csv(HERE / "grupos-palavras-novas-palavras.csv").set_index("word")["group"].to_dict()
    groups = sorted({group for group in group_of.values() if group != NO_GROUP})
    rows = [{group_of[word] for _, _, word in spans if group_of.get(word, NO_GROUP) != NO_GROUP}
            for spans in new_word_spans(pairs)]
    return pd.DataFrame([[int(group in present) for group in groups] for present in rows], columns=groups)


def main():
    pairs = esnli.training_pairs()
    y = pairs["y"].to_numpy()
    targets = group_targets(pairs)
    label = csr_matrix(np.eye(len(esnli.LABELS))[y])
    pair_words = CountVectorizer(analyzer=lambda words: words, binary=True, min_df=MIN_PAIRS).fit_transform(
        [grads.words_of(f"{a} {b}") for a, b in zip(pairs["sentence1"], pairs["sentence2"])])
    features = {"label": label, "label_and_pair": hstack([label, pair_words]).tocsr(), "pair": pair_words}
    tops = pd.read_csv(HERE / "grupos-palavras-novas.csv").set_index("group")["top_words"]
    rows = []
    for group in targets.columns:
        present = targets[group].to_numpy()
        folds = StratifiedKFold(FOLDS, shuffle=True, random_state=SEED)
        row = {"group": group, "pairs_with_it": int(present.sum())}
        for name, x in features.items():
            scores = cross_val_predict(LogisticRegression(max_iter=2000), x, present, cv=folds,
                                       method="predict_proba")[:, 1]
            row[f"auc_{name}"] = float(roc_auc_score(present, scores))
        row["gain"] = row["auc_label_and_pair"] - row["auc_label"]
        rows.append(row | {"top_words": " ".join(tops[group].split()[:6])})
    table = pd.DataFrame(rows).sort_values("gain", ascending=False)
    table.to_csv(HERE / "grupos-dependem-do-par.csv", index=False)
    means = table[["auc_label", "auc_label_and_pair", "auc_pair", "gain"]].mean()
    print(f"grupos {len(table)} | media: so rotulo {means['auc_label']:.3f} | rotulo e par "
          f"{means['auc_label_and_pair']:.3f} | so par {means['auc_pair']:.3f} | ganho {means['gain']:+.3f} | "
          f"grupos com ganho de 0,02 ou mais: {int((table['gain'] >= 0.02).sum())}")
    with pd.option_context("display.width", 220, "display.max_colwidth", 60, "display.float_format", "{:.3f}".format):
        print(table.to_string(index=False))


if __name__ == "__main__":
    main()
