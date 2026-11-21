"""2-D coordinates of the rationales' new words, to DRAW the groups of medir_grupos_palavras.py.

The groups themselves are the saved ones (grupos-palavras-novas-palavras.csv, HDBSCAN over a 10-dimension UMAP):
nothing is clustered again here. The word vectors are recomputed the same way (BERT base, last layer, mean of the
word's pieces, mean over its occurrences) and a second UMAP takes them to 2 dimensions, only for the picture, so
distances on the map are not the ones the grouping saw.

    uv run --frozen --with umap-learn python resultados/rte-pequenos/mapa_grupos_palavras.py
Writes grupos-palavras-novas-mapa.csv (word, group, pairs, x, y).
"""
from pathlib import Path

import numpy as np
import pandas as pd
import umap
from medir_grupos_palavras import SEED, UMAP_NEIGHBORS, new_word_spans, word_vectors

from radibert import esnli_dados as esnli

HERE = Path(__file__).parent


def main():
    saved = pd.read_csv(HERE / "grupos-palavras-novas-palavras.csv")
    pairs = esnli.training_pairs()
    vectors = word_vectors(list(pairs["rationale"]), new_word_spans(pairs), set(saved["word"]))
    missing = [word for word in saved["word"] if word not in vectors]
    if missing:
        raise SystemExit(f"{len(missing)} saved words got no vector (first: {missing[:5]})")
    matrix = np.stack([vectors[word] for word in saved["word"]])
    flat = umap.UMAP(n_components=2, n_neighbors=UMAP_NEIGHBORS, metric="cosine",
                     random_state=SEED).fit_transform(matrix)
    saved.assign(x=flat[:, 0], y=flat[:, 1]).to_csv(HERE / "grupos-palavras-novas-mapa.csv", index=False)
    print(f"{len(saved)} palavras, {saved['group'].nunique() - 1} grupos e {(saved['group'] == -1).sum()} sem grupo")


if __name__ == "__main__":
    main()
