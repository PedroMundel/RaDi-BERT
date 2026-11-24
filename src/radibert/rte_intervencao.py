"""Attention intervention at inference (plan, section 10.1; Pedro's ablation, 16/11).

A trained model predicts with some attention links cut in chosen layers: the [CLS] row (or every row) cannot look at
a set of input positions. The weights do not change. The cut is made the way BERT already ignores padding: a very
negative number added to the attention scores of the forbidden positions, before the softmax, so the attention
redistributes over what is left.
"""
import itertools
from contextlib import contextmanager

import torch

from radibert import rte_gradientes as grads
from radibert.rte_dados import MAX_INPUT_TOKENS

OPERATIONS = ("block", "only")


def layer_sets(n_layers: int) -> list[tuple[int, ...]]:
    """Each layer alone, each pair of layers, and all of them (0-based)."""
    layers = range(n_layers)
    sets = [(k,) for k in layers] + list(itertools.combinations(layers, 2))
    return sets if n_layers <= 2 else sets + [tuple(layers)]


def forbidden_positions(marks: torch.Tensor, attention_mask: torch.Tensor, operation: str) -> torch.Tensor:
    """(pairs, positions) 0/1 of what the attention may not look at. `block`: the marked positions. `only`: every
    real position that is not marked, except [CLS] itself (position 0), so only the marked ones and [CLS] remain."""
    if operation == "block":
        return marks.bool()
    if operation != "only":
        raise ValueError(f"unknown operation {operation!r}")
    forbidden = attention_mask.bool() & ~marks.bool()
    forbidden[:, 0] = False
    return forbidden


@contextmanager
def restricted_attention(bert: torch.nn.Module, layers: tuple[int, ...], forbidden: torch.Tensor, cls_only: bool):
    """While open, in each of `layers` the [CLS] row (`cls_only`) or every row of the attention cannot look at the
    positions where `forbidden` (pairs, positions) is set. For one batch: `forbidden` has the batch's shape."""
    def cut(module, args, kwargs):
        mask = kwargs["attention_mask"]  # (pairs, 1, from, to), 0 or the most negative number where it is padding
        block = forbidden[:, None, None, :].expand_as(mask)
        if cls_only:
            rows = torch.zeros(mask.shape[2], dtype=torch.bool, device=mask.device)
            rows[0] = True
            block = block & rows[None, None, :, None]
        kwargs["attention_mask"] = mask.masked_fill(block, torch.finfo(mask.dtype).min)
        return args, kwargs

    handles = [bert.encoder.layer[k].attention.self.register_forward_pre_hook(cut, with_kwargs=True) for k in layers]
    try:
        yield
    finally:
        for handle in handles:
            handle.remove()


def content_positions(premise: str, hypothesis: str, bert_tok) -> list[int]:
    """Input positions inside a content word of the pair: the words a mark can fall on (rte_gradientes.word_groups
    puts single letters, function words and source words in group F, and a real mark is never in F)."""
    enc = bert_tok(premise, hypothesis, return_offsets_mapping=True, truncation="only_first",
                   max_length=MAX_INPUT_TOKENS)
    texts = (premise, hypothesis)
    spans = [[(m.start(), m.end(), m.group().lower()) for m in grads.WORD.finditer(text)] for text in texts]
    return [pos for pos, ((a, b), seq) in enumerate(zip(enc["offset_mapping"], enc.sequence_ids()))
            if seq is not None and any(start < b and a < end and is_content(word) for start, end, word in spans[seq])]


def is_content(word: str) -> bool:
    return not ((len(word) == 1 and not word.isdigit()) or word in grads.DROP or word in grads.SOURCE_WORDS)


def content_draw(n_marks: int, candidates: list[int], generator: torch.Generator) -> list[int]:
    """`n_marks` of the content positions, drawn without replacement. May coincide with real marks: it is a draw
    among the words a mark could fall on, not among the unmarked ones."""
    chosen = torch.randperm(len(candidates), generator=generator)[:n_marks]
    return sorted(candidates[i] for i in chosen.tolist())
