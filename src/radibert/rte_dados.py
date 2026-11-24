"""RTE pairs and FA rationales turned into training items for the Agrawal replication.

Design and decisions: docs/2026-11-09-codigo-treino-rte.md. Cleanup C runs here, never on the CSV. The 20 prompt
examples have no FA row, so the inner merge drops them from BOTH arms. GLUE codes entailment as 0; the positive class
(y = 1) is entailment, the class the rationale defends, as "relevant" is in the paper.
"""
from dataclasses import dataclass

import numpy as np
import pandas as pd
import torch
from transformers import AutoTokenizer

from radibert.paths import RTE, RTE_35B
from radibert.rte_racionalizacoes import clean_opening

FA_CSV = RTE_35B / "racionalizacoes-FA.csv"
BERT = "google-bert/bert-base-uncased"
# Agrawal's baseline is a BERT base "further trained on MS-MARCO" (§5); the paper names no checkpoint. This one has
# BERT's vocab.txt (same MD5, 10/11), so the pairs are tokenized with BERT's tokenizer.
MSMARCO = "nboost/pt-bert-base-uncased-msmarco"
CAPREOLUS = "Capreolus/bert-base-msmarco"  # second MS-MARCO checkpoint (18/11): same vocab.txt MD5 as BERT base
# Weaker encoders (10/11, Pedro's idea): Google's BERT miniatures, same vocabulary and token ids as bert-base-uncased
SMALL = "google/bert_uncased_L-4_H-512_A-8"
TINY = "google/bert_uncased_L-2_H-128_A-2"
T5 = "google-t5/t5-base"
T5_ENCODER = "google/t5-v1_1-base"  # T5-encoder arms: C4 only; t5-base saw RTE and MNLI in pre-training (HF card)
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


def all_pairs() -> pd.DataFrame:
    """Every RTE pair on disk, train (the ones with a rationale) then dev, without the rationale: the test outside
    the distribution of a model trained on e-SNLI, which never sees any of them."""
    return pd.concat([training_pairs().drop(columns="rationale"), dev_pairs()], ignore_index=True)


def shuffle_within_label(pairs: pd.DataFrame, seed: int) -> pd.DataFrame:
    """The shuffled control: every pair gets the rationale of another pair of its own label (a cycle over a random
    order of the label's pairs, so nobody keeps its own). Keeps what a rationale says about the label, drops what it
    says about the pair. Everything but `rationale` is untouched."""
    rng = np.random.default_rng(seed)
    shuffled = pairs.copy()
    for _, rows in pairs.groupby("y"):
        if len(rows) < 2:
            raise ValueError("a label with a single pair has no other rationale to take")
        order = rng.permutation(rows.index.to_numpy())
        shuffled.loc[order, "rationale"] = pairs.loc[np.roll(order, 1), "rationale"].to_numpy()
    return shuffled


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
    # the T5 tokenizer (T5-encoder arms) joins the pair with </s> and has no segment ids: zeros, never read by T5
    types = enc["token_type_ids"] if "token_type_ids" in enc else [[0] * len(ids) for ids in enc["input_ids"]]
    items = [{"idx": int(idx), "y": int(y), "input_ids": ids, "token_type_ids": tt}
             for idx, y, ids, tt in zip(pairs["idx"], pairs["y"], enc["input_ids"], types)]
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
    if "marks" in items[0]:  # rte_marcas: 1 on the input positions the [CLS] attention is pulled to
        batch["marks"] = pad([it["marks"] for it in items], 0)
    return batch
