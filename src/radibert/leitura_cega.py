"""Blind reading sheet: 30 Qwen rationales from the batch + 20 GPT-3 explanations already judged by Wiegreffe et al.
(2022) annotators, shuffled together so the reader does not know the source.

The 20 judged items calibrate the reader: their human acceptability votes (0-3 of 3 annotators) are the reference for
question 4. Source, ids and votes go to a separate answer key, never to the sheet.
Data: dados/wiegreffe2022/snli_test.csv, from github.com/allenai/few_shot_explanations (Apache-2.0), downloaded 29/10.
Caveat: their annotators judged each explanation next to the other 4 candidates of the same pair; here it is shown alone.

Usage: python -m radibert.leitura_cega
"""

import pandas as pd

from radibert.paths import LOTE_35B, WIEGREFFE

BATCH = LOTE_35B / "racionalizacoes-F-35B.csv"
JUDGED = WIEGREFFE / "snli_test.csv"
SHEET = LOTE_35B / "leitura-50-cega.md"
KEY = LOTE_35B / "leitura-50-gabarito.csv"
SEED = 42
LABELS = {"entailment": "implicação", "neutral": "neutro", "contradiction": "contradição"}
W_LABELS = {"TRUE": "entailment", "NEITHER": "neutral", "FALSE": "contradiction"}


def qwen_items(per_label=10) -> pd.DataFrame:
    batch = pd.read_csv(BATCH)  # already in seed-42 order, so the first of each label are a random draw
    take = batch.groupby("gold_label", sort=False).head(per_label)
    return pd.DataFrame({"fonte": "qwen", "id": take["pairID"], "gold_label": take["gold_label"],
                         "premissa": take["Sentence1"], "hipotese": take["Sentence2"],
                         "justificativa": take["qwen"], "votos": pd.NA})


def judged_explanations() -> pd.DataFrame:
    """One row per (pair, explanation) with how many of the annotators marked it acceptable."""
    raw = pd.read_csv(JUDGED, keep_default_na=False)
    rows = []
    for _, r in raw.iterrows():  # one row per annotator; explanation order is shuffled per row
        chosen = {int(i) for i in str(r["Answer.acceptable"]).split("|") if i}
        for k in range(1, 6):
            rows.append({"id": r["Input.id"], "fonte_amostra": str(r[f"Input.source_sample_{k}"]),
                         "premissa": r["Input.premise"], "hipotese": r["Input.hypothesis"],
                         "gold_label": W_LABELS[str(r["Input.gold_label"]).upper()],
                         "justificativa": r[f"Input.explanation_{k}"], "aceita": int(k in chosen)})
    df = pd.DataFrame(rows)
    keys = ["id", "fonte_amostra", "premissa", "hipotese", "gold_label", "justificativa"]
    out = df.groupby(keys, as_index=False).agg(votos=("aceita", "sum"), anotadores=("aceita", "size"))
    return out[out["anotadores"] == 3]  # a few pairs were annotated twice; keep the clean 3-annotator ones


def judged_items(n=20) -> pd.DataFrame:
    """Spread over votes 0-3 (5 each) and labels, one explanation per pair."""
    pool = judged_explanations().sample(frac=1, random_state=SEED).drop_duplicates("id")
    per_vote = [pool[pool["votos"] == v].groupby("gold_label").head(2).head(n // 4) for v in range(4)]
    picked = pd.concat(per_vote).assign(fonte="wiegreffe")
    return picked[["fonte", "id", "gold_label", "premissa", "hipotese", "justificativa", "votos"]]


if __name__ == "__main__":
    items = pd.concat([qwen_items(), judged_items()], ignore_index=True)
    items = items.sample(frac=1, random_state=SEED).reset_index(drop=True)
    items.insert(0, "n", range(1, len(items) + 1))
    items.to_csv(KEY, index=False)
    lines = [
        "# Leitura cega de 50 justificativas (29/10)",
        "",
        "30 do lote 35B (10 por rótulo, os primeiros na ordem da semente 42) e 20 de Wiegreffe et al. (2022), já",
        "julgadas por 3 avaliadores deles, misturadas com a semente 42. A fonte de cada uma está só no gabarito",
        "(`leitura-50-gabarito.csv`): não abrir antes de terminar.",
        "",
        "**Rubrica** (Wiegreffe et al. 2022, App. B.3; julgue considerando o rótulo dado como certo):",
        "",
        "1. **Nova** (s/n): traz fato, informação ou raciocínio que não está no par nem no rótulo?",
        "2. **Sustenta** (s/n): o que ela diz é relevante para justificar o rótulo?",
        "3. **Quantidade** (p/s/d): pouca, suficiente ou demais?",
        "4. **Aceitável** (s/n): no geral, você aceitaria?",
        "",
        "Resposta: uma linha por item, `7: n s p n motivo`.",
        "",
    ]
    for r in items.itertuples():
        lines += [f"## {r.n}. {LABELS[r.gold_label]}", "", f"- **Premissa:** {r.premissa}",
                  f"- **Hipótese:** {r.hipotese}", f"- **Justificativa:** {r.justificativa}", "",
                  "Nova · Sustenta · Quantidade · Aceitável: ", ""]
    SHEET.write_text("\n".join(lines), encoding="utf-8")
    w = items[items.fonte == "wiegreffe"]
    print(items.groupby(["fonte", "gold_label"]).size().to_dict())
    print("votos wiegreffe:", w.votos.value_counts().sort_index().to_dict())
