"""RTE pairs and FA rationales turned into training items for the Agrawal replication.

Design and decisions: docs/2026-11-09-codigo-treino-rte.md. Cleanup C runs here, never on the CSV. The 20 prompt
examples have no FA row, so the inner merge drops them from BOTH arms. GLUE codes entailment as 0; the positive class
(y = 1) is entailment, the class the rationale defends, as "relevant" is in the paper.
"""
from dataclasses import dataclass

import pandas as pd
import torch
from transformers import AutoTokenizer

from radibert.paths import RTE, RTE_35B
from radibert.rte_racionalizacoes import clean_opening

FA_CSV = RTE_35B / "racionalizacoes-FA.csv"
BERT = "google-bert/bert-base-uncased"
T5 = "google-t5/t5-base"
MAX_INPUT_TOKENS = 512  # BERT's limit; the longest RTE pair is ~320 (analise-lote-FA.md), so nothing is cut (I9)
MAX_TARGET_TOKENS = 64  # the longest rationale has 34 words
IGNORED = -100  # label value the T5 cross-entropy skips
ENTAILMENT = 0  # GLUE RTE ClassLabel


@dataclass(frozen=True)
class Tokenizers:
    bert: object
    t5: object


def load_tokenizers(bert_name: str = BERT) -> Tokenizers:
    return Tokenizers(AutoTokenizer.from_pretrained(bert_name), AutoTokenizer.from_pretrained(T5))


def read_rte(split: str) -> pd.DataFrame:
    pairs = pd.read_parquet(RTE / f"rte_{split}.parquet")
    pairs["y"] = (pairs["label"] == ENTAILMENT).astype(int)
    return pairs


def training_pairs() -> pd.DataFrame:
    """The 2,470 train pairs with an FA rationale, cleaned by C: the same set for both arms (E4)."""
    fa = pd.read_csv(FA_CSV, usecols=["idx", "qwen"])
    pairs = read_rte("train").merge(fa, on="idx", how="inner")
    pairs["rationale"] = pairs["qwen"].map(clean_opening)
    return pairs.drop(columns="qwen").sort_values("idx").reset_index(drop=True)


def dev_pairs() -> pd.DataFrame:
    return read_rte("validation").sort_values("idx").reset_index(drop=True)


def overlong_counts(pairs: pd.DataFrame, tok: Tokenizers) -> dict:
    """How many inputs and targets the truncation would cut (I9: both must be 0)."""
    inputs = tok.bert(list(pairs["sentence1"]), list(pairs["sentence2"]))["input_ids"]
    counts = {"inputs_cut": sum(len(ids) > MAX_INPUT_TOKENS for ids in inputs)}
    if "rationale" in pairs:
        targets = tok.t5(list(pairs["rationale"]))["input_ids"]
        counts["targets_cut"] = sum(len(ids) > MAX_TARGET_TOKENS for ids in targets)
    return counts


def encode(pairs: pd.DataFrame, tok: Tokenizers) -> list[dict]:
    """One dict of token ids per pair; `labels` (the T5 target) only when the pairs carry a rationale."""
    enc = tok.bert(list(pairs["sentence1"]), list(pairs["sentence2"]), truncation="only_first",
                   max_length=MAX_INPUT_TOKENS)
    items = [{"idx": int(idx), "y": int(y), "input_ids": ids, "token_type_ids": types}
             for idx, y, ids, types in zip(pairs["idx"], pairs["y"], enc["input_ids"], enc["token_type_ids"])]
    if "rationale" in pairs:
        targets = tok.t5(list(pairs["rationale"]), truncation=True, max_length=MAX_TARGET_TOKENS)["input_ids"]
        for item, target in zip(items, targets):
            item["labels"] = target
    return items


def pad(rows: list[list[int]], value: int) -> torch.Tensor:
    width = max(map(len, rows))
    return torch.tensor([row + [value] * (width - len(row)) for row in rows])


def collate(items: list[dict]) -> dict:
    """Pads each batch to its own longest pair (BERT pad id is 0) and the targets with IGNORED."""
    batch = {"idx": torch.tensor([it["idx"] for it in items]),
             "y": torch.tensor([it["y"] for it in items], dtype=torch.float),
             "input_ids": pad([it["input_ids"] for it in items], 0),
             "token_type_ids": pad([it["token_type_ids"] for it in items], 0),
             "attention_mask": pad([[1] * len(it["input_ids"]) for it in items], 0)}
    if "labels" in items[0]:
        batch["labels"] = pad([it["labels"] for it in items], IGNORED)
    return batch
