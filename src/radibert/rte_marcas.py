"""Key-word marks for the [CLS] attention experiment (Pedro's idea, 10/11).

The decoder of the Agrawal replication points at the pair's key words in its own cross-attention, and that pointing
never reaches the [CLS] vector the head reads (docs/2026-11-10-hipoteses-do-nulo.md). Here the pointing is given to the
encoder directly: the input positions whose word the rationale copies from the pair (group C of rte_gradientes) are
"marked", and a loss pulls the last layer's [CLS] attention onto them. No decoder.

The control marks the same number of positions per pair at random (Herrewijnen et al. 2026: random tokens gave gains
similar to human rationales in attention regularization).
"""
import pandas as pd
import torch

from radibert import rte_gradientes as grads
from radibert.rte_dados import MAX_INPUT_TOKENS, Tokenizers

RANDOM_SEED = 0  # the random marks are data, fixed across training seeds


def real_marks(premise: str, hypothesis: str, rationale: str, label_expr, bert_tok) -> list[int]:
    """Input positions (BERT tokens of the pair) inside a word that the rationale copies from the pair."""
    copied = {word for _, _, word, group in grads.word_groups(rationale, premise, hypothesis, label_expr)
              if group == grads.Group.C}
    enc = bert_tok(premise, hypothesis, return_offsets_mapping=True, truncation="only_first",
                   max_length=MAX_INPUT_TOKENS)
    texts = (premise, hypothesis)
    spans = [[(m.start(), m.end(), m.group().lower()) for m in grads.WORD.finditer(text)] for text in texts]
    marks = []
    for pos, ((a, b), seq) in enumerate(zip(enc["offset_mapping"], enc.sequence_ids())):
        if seq is None:  # [CLS], [SEP]
            continue
        if any(start < b and a < end and word in copied for start, end, word in spans[seq]):
            marks.append(pos)
    return marks


def random_marks(n_marks: int, sequence_ids: list, generator: torch.Generator) -> list[int]:
    """`n_marks` positions drawn without replacement among the pair's own tokens (never [CLS] or [SEP])."""
    candidates = [pos for pos, seq in enumerate(sequence_ids) if seq is not None]
    chosen = torch.randperm(len(candidates), generator=generator)[:n_marks]
    return sorted(candidates[i] for i in chosen.tolist())


def mark_table(pairs: pd.DataFrame, tok: Tokenizers, label_expr) -> pd.DataFrame:
    """One row per train pair: idx, number of input tokens, real and random marked positions (same count)."""
    generator = torch.Generator().manual_seed(RANDOM_SEED)
    rows = []
    for idx, p, h, r in zip(pairs["idx"], pairs["sentence1"], pairs["sentence2"], pairs["rationale"]):
        real = real_marks(p, h, r, label_expr, tok.bert)
        seq_ids = tok.bert(p, h, truncation="only_first", max_length=MAX_INPUT_TOKENS).sequence_ids()
        rows.append({"idx": int(idx), "n_tokens": len(seq_ids), "real": real,
                     "random": random_marks(len(real), seq_ids, generator)})
    return pd.DataFrame(rows)


def with_marks(items: list[dict], table: pd.DataFrame, kind: str) -> list[dict]:
    """Copies of the items with `marks`: one 0/1 per input position. `kind` is a column of the table."""
    positions = dict(zip(table["idx"], table[kind]))
    out = []
    for item in items:
        marks = [0] * len(item["input_ids"])
        for pos in positions[item["idx"]]:
            marks[pos] = 1
        out.append(item | {"marks": marks})
    return out


def marked_pairs(batch: dict) -> int:
    return int((batch["marks"].sum(1) > 0).sum())
