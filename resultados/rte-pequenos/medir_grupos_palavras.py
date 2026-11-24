"""Groups the rationales' new words with HDBSCAN: argument mold or content? (plan
docs/2026-11-10-plano-teste-fora-da-distribuicao.md, section 11.7, written before this ran; Pedro's idea, 17/11.)

Each new word (group N, in 2 pairs or more) gets one vector: pre-trained BERT base reading the whole rationale, last
layer, mean of the word's pieces, then mean over all its occurrences. UMAP takes the vectors to 10 dimensions and
HDBSCAN groups them. For each group: how its pairs split over the labels and how well the logistic regression of
section 11.6 guesses the label from that group's words alone.

Usage:  uv run --frozen --with umap-learn python resultados/rte-pequenos/medir_grupos_palavras.py
"""
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import umap
from sklearn.cluster import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from transformers import AutoModel, AutoTokenizer

from radibert import esnli_dados as esnli
from radibert import rte_dados as dados
from radibert import rte_gradientes as grads

HERE = Path(__file__).parent
MIN_PAIRS, UMAP_DIMENSIONS, UMAP_NEIGHBORS, MIN_GROUP, SEED, FOLDS, BATCH = 2, 10, 15, 15, 0, 5, 64
NO_GROUP = -1  # HDBSCAN's label for a word it leaves out


def new_word_spans(pairs: pd.DataFrame) -> list[list[tuple[int, int, str]]]:
    """Per pair, (start, end, word) of every new word of its rationale."""
    label_expr = grads.expression_pattern(grads.expression_table(pairs, esnli.LABELS))
    return [[(start, end, word) for start, end, word, group in grads.word_groups(rationale, premise, hypothesis,
                                                                               label_expr) if group == grads.Group.N]
            for premise, hypothesis, rationale in zip(pairs["sentence1"], pairs["sentence2"], pairs["rationale"])]


@torch.no_grad()
def word_vectors(rationales: list[str], spans: list[list[tuple[int, int, str]]], kept: set[str]) -> dict:
    """word -> mean, over its occurrences, of the mean of its pieces' last-layer vectors."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tok = AutoTokenizer.from_pretrained(dados.BERT)
    bert = AutoModel.from_pretrained(dados.BERT, add_pooling_layer=False).to(device).eval()
    sums, counts = defaultdict(lambda: 0.0), defaultdict(int)
    for first in range(0, len(rationales), BATCH):
        texts = rationales[first:first + BATCH]
        enc = tok(texts, return_offsets_mapping=True, padding=True, truncation=True, return_tensors="pt")
        offsets = enc.pop("offset_mapping")
        hidden = bert(**enc.to(device)).last_hidden_state.float().cpu()
        for row, pair_spans in enumerate(spans[first:first + BATCH]):
            for start, end, word in pair_spans:
                if word not in kept:
                    continue
                pieces = [i for i, (a, b) in enumerate(offsets[row].tolist()) if a < end and start < b and b > a]
                if pieces:
                    sums[word] = sums[word] + hidden[row, pieces].mean(0)
                    counts[word] += 1
    return {word: (sums[word] / counts[word]).numpy() for word in counts}


def main():
    pairs = esnli.training_pairs()
    y = pairs["y"].to_numpy()
    spans = new_word_spans(pairs)
    per_pair = [[word for _, _, word in pair_spans] for pair_spans in spans]
    vectorizer = CountVectorizer(analyzer=lambda words: words, binary=True, min_df=MIN_PAIRS)
    presence = vectorizer.fit_transform(per_pair)
    words = list(vectorizer.get_feature_names_out())
    vectors = word_vectors(list(pairs["rationale"]), spans, set(words))
    missing = [word for word in words if word not in vectors]
    if missing:
        raise RuntimeError(f"{len(missing)} words got no vector (first: {missing[:5]}): the spans and the tokenizer disagree")
    matrix = np.stack([vectors[word] for word in words])
    reduced = umap.UMAP(n_components=UMAP_DIMENSIONS, n_neighbors=UMAP_NEIGHBORS, metric="cosine",
                        random_state=SEED).fit_transform(matrix)
    groups = HDBSCAN(min_cluster_size=MIN_GROUP).fit_predict(reduced)
    pairs_per_word = np.asarray(presence.sum(0)).ravel()
    pd.DataFrame({"word": words, "group": groups, "pairs": pairs_per_word}).to_csv(
        HERE / "grupos-palavras-novas-palavras.csv", index=False)

    folds = StratifiedKFold(FOLDS, shuffle=True, random_state=SEED)
    rows = []
    for group in sorted(set(groups)):
        columns = np.flatnonzero(groups == group)
        x = presence[:, columns]
        has = np.asarray(x.sum(1)).ravel() > 0
        accuracy = float((cross_val_predict(LogisticRegression(max_iter=2000), x, y, cv=folds) == y).mean())
        split = {f"share_{name}": float((y[has] == label).mean()) for label, name in esnli.LABELS.items()}
        top = columns[np.argsort(-pairs_per_word[columns])[:12]]
        rows.append({"group": int(group), "words": len(columns), "pairs_with_it": int(has.sum())} | split
                    | {"accuracy_alone": accuracy, "top_words": " ".join(words[i] for i in top)})
    table = pd.DataFrame(rows).sort_values("pairs_with_it", ascending=False)
    table.to_csv(HERE / "grupos-palavras-novas.csv", index=False)
    grouped = groups != NO_GROUP
    print(f"palavras {len(words)} | grupos {len(set(groups)) - (NO_GROUP in groups)} | sem grupo {int((~grouped).sum())} "
          f"({(~grouped).mean():.0%})")
    for name, columns in (("so palavras com grupo", grouped), ("so palavras sem grupo", ~grouped)):
        accuracy = (cross_val_predict(LogisticRegression(max_iter=2000), presence[:, np.flatnonzero(columns)], y,
                                      cv=folds) == y).mean()
        print(f"{name}: acuracia {accuracy:.3f}")
    with pd.option_context("display.width", 250, "display.max_colwidth", 110, "display.float_format", "{:.2f}".format):
        print(table.to_string(index=False))


if __name__ == "__main__":
    main()
