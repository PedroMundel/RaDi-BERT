"""Where the auxiliary loss pushes BERT: by group of rationale tokens and by word (docs/2026-11-09-codigo-treino-rte.md).

Every gradient here is taken on the BERT weights only, with torch.autograd.grad: nothing is added to `.grad`, no weight
changes, and the model runs in eval mode (no dropout, so no random draw), which keeps training identical (I14).

Groups, tested in this order (Pedro, 09/11: three groups, then F apart):
  S  label word: inside an expression of 1-3 words seen in >= 30 train rationales, >= 90% of them with one label
  F  function word: stop word, statement word ("states", "text"), single letter, or a token that is no word at all
     (punctuation, the closing </s>)
  N  new word: content word absent from premise and hypothesis (copia.new_words' rule, digits kept)
  C  copied word: content word that is in the pair
"""
import contextlib
import re
from collections import Counter
from dataclasses import dataclass
from enum import IntEnum

import pandas as pd
import torch
import torch.nn.functional as F

from radibert.copia import DROP
from radibert.rte_dados import IGNORED, MAX_TARGET_TOKENS, Tokenizers, collate, encode
from radibert.rte_modelo import cls_loss


class Group(IntEnum):
    S = 0  # label word
    F = 1  # function word or non-word token
    C = 2  # copied from the pair
    N = 3  # new


MIN_COUNT, MIN_SHARE = 30, 0.9
SOURCE_WORDS = {"text", "passage"}  # name the source, as "premise" and "sentence" do in copia.META
WORD = re.compile(r"[a-z0-9]+", re.I)  # matched on the original text, so offsets stay those of the tokenizer
PROBE_SEED = 0
GROUP_PROBE_SIZE, WORD_PROBE_SIZE = 64, 128
TOP_WORDS_PER_GROUP = 50
CHUNK_PAIRS = 16  # probe pairs per forward pass in the measures


def words_of(text: str) -> list[str]:
    return [w.lower() for w in WORD.findall(text)]


RTE_LABELS = {1: "entailment", 0: "not_entailment"}  # y -> name, in the table's column order


def expression_table(pairs: pd.DataFrame, labels: dict[int, str] = RTE_LABELS) -> pd.DataFrame:
    """Expressions of 1-3 words found in >= MIN_COUNT rationales, >= MIN_SHARE of them with one label (train only)."""
    seen = {y: Counter() for y in labels}
    for y, rationale in zip(pairs["y"], pairs["rationale"]):
        tokens = words_of(rationale)
        seen[y].update({" ".join(tokens[i:i + n]) for n in (1, 2, 3) for i in range(len(tokens) - n + 1)})
    rows = []
    for expr in set().union(*seen.values()):
        counts = {y: seen[y][expr] for y in labels}
        total = sum(counts.values())
        if total >= MIN_COUNT and max(counts.values()) / total >= MIN_SHARE:
            rows.append({"expression": expr} | {f"n_{labels[y]}": n for y, n in counts.items()})
    columns = [f"n_{name}" for name in labels.values()]
    return pd.DataFrame(rows, columns=["expression", *columns]).sort_values(columns, ascending=False,
                                                                             ignore_index=True)


def expression_pattern(table: pd.DataFrame) -> re.Pattern:
    """One regex for all expressions, longest first; words may be joined by any non-word run ("doesn't")."""
    parts = sorted((r"\W+".join(map(re.escape, e.split())) for e in table["expression"]), key=len, reverse=True)
    return re.compile(r"\b(?:" + "|".join(parts) + r")\b", re.I)


def word_groups(rationale: str, premise: str, hypothesis: str, label_expr: re.Pattern) -> list[tuple[int, int, str, int]]:
    """(start, end, word, group) for each word of the rationale."""
    label_spans = [m.span() for m in label_expr.finditer(rationale)]
    pair = set(words_of(f"{premise} {hypothesis}"))
    out = []
    for m in WORD.finditer(rationale):
        word, (start, end) = m.group().lower(), m.span()
        if any(a < end and start < b for a, b in label_spans):
            group = Group.S
        elif (len(word) == 1 and not word.isdigit()) or word in DROP or word in SOURCE_WORDS:
            group = Group.F
        else:
            group = Group.C if word in pair else Group.N
        out.append((start, end, word, group))
    return out


@dataclass(frozen=True)
class Unit:
    """One word of a rationale (or one non-word token) and the T5 target positions it spans."""
    word: str
    group: int
    positions: tuple[int, ...]


def token_units(rationale: str, premise: str, hypothesis: str, t5_tok, label_expr: re.Pattern) -> list[Unit]:
    """Every T5 target position belongs to exactly one unit, so units split L_aux with nothing left over (I15)."""
    enc = t5_tok(rationale, return_offsets_mapping=True, truncation=True, max_length=MAX_TARGET_TOKENS)
    words = word_groups(rationale, premise, hypothesis, label_expr)
    owner = {}
    for pos, (a, b) in enumerate(enc["offset_mapping"]):
        hit = next((i for i, (start, end, _, _) in enumerate(words) if a < end and start < b), None)
        owner.setdefault(("w", hit) if hit is not None else ("t", pos), []).append(pos)
    tokens = t5_tok.convert_ids_to_tokens(enc["input_ids"])
    units = []
    for (kind, ref), positions in owner.items():
        word, group = words[ref][2:] if kind == "w" else (tokens[ref], Group.F)
        units.append(Unit(word, group, tuple(positions)))
    return units


def group_word_table(pairs: pd.DataFrame, label_expr: re.Pattern) -> pd.DataFrame:
    """The most common words of each group over the train rationales, to read what each group really holds."""
    counts = {g: Counter() for g in Group}
    for p, h, r in zip(pairs["sentence1"], pairs["sentence2"], pairs["rationale"]):
        for _, _, word, group in word_groups(r, p, h, label_expr):
            counts[group][word] += 1
    return pd.DataFrame([{"group": g.name, "word": w, "count": c}
                         for g in Group for w, c in counts[g].most_common(TOP_WORDS_PER_GROUP)])


@dataclass
class Probe:
    """A fixed batch of train pairs, the group of each target position (-1 on padding) and its word units."""
    batch: dict
    groups: torch.Tensor
    units: list[list[Unit]]

    def to(self, device) -> "Probe":
        return Probe({k: v.to(device) for k, v in self.batch.items()}, self.groups.to(device), self.units)


def build_probe(pairs: pd.DataFrame, tok: Tokenizers, label_expr: re.Pattern, size: int) -> Probe:
    """size / (number of labels) pairs per label, drawn with PROBE_SEED, the same in every run."""
    per_label = size // pairs["y"].nunique()
    chosen = pd.concat([g.sample(per_label, random_state=PROBE_SEED) for _, g in pairs.groupby("y")])
    chosen = chosen.sort_values("idx")
    batch = collate(encode(chosen, tok))
    units = [token_units(r, p, h, tok.t5, label_expr)
             for p, h, r in zip(chosen["sentence1"], chosen["sentence2"], chosen["rationale"])]
    groups = torch.full_like(batch["labels"], -1)
    for i, pair_units in enumerate(units):
        for unit in pair_units:
            groups[i, list(unit.positions)] = unit.group
    if not torch.equal(groups == -1, batch["labels"] == IGNORED):
        raise ValueError("probe: target positions without a group, or a group on padding; offsets and ids disagree")
    return Probe(batch, groups, units)


@contextlib.contextmanager
def evaluating(model):
    was_training = model.training
    model.eval()
    try:
        yield
    finally:
        model.train(was_training)


def measured_params(model) -> list:
    """The encoder weights the measures look at. In the T5-encoder arm with decoder the `shared` embedding is left
    out: the decoder also embeds its own target tokens with it, so its gradient would mix the decoder's learning
    with the push on the encoder (audit 10/11)."""
    params = list(model.bert.parameters())
    if getattr(model, "shares_t5_encoder", False):
        params = [p for p in params if p is not model.t5.shared.weight]
    return params


def bert_grad(loss: torch.Tensor, model, retain_graph: bool = True) -> tuple[torch.Tensor, ...]:
    return torch.autograd.grad(loss, measured_params(model), retain_graph=retain_graph)


def dot(a, b) -> float:
    return float(sum((x.float() * y.float()).sum() for x, y in zip(a, b)))


def token_nll(logits: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
    """Per-position cross-entropy of the T5 target; 0 on IGNORED positions."""
    return F.cross_entropy(logits.transpose(1, 2).float(), labels, ignore_index=IGNORED, reduction="none")


def split_aux_loss(logits: torch.Tensor, labels: torch.Tensor, groups: torch.Tensor, n_tokens: int) -> list:
    """L_aux split by group over the target tokens of the whole probe (`n_tokens`), so the parts of every chunk add up
    to L_aux exactly (I12)."""
    nll = token_nll(logits, labels)
    return [(nll * (groups == g)).sum() / n_tokens for g in Group]


def rows_of(batch: dict, start: int, stop: int) -> dict:
    """Rows start..stop-1 of a batch, trimmed to their own longest input and target. Contiguous copies: a trimmed
    slice is not, and T5 calls labels.view(-1) (the PC run of 09/11 died on it)."""
    rows = slice(start, stop)
    n_in = int(batch["attention_mask"][rows].sum(1).max())
    n_out = int((batch["labels"][rows] != IGNORED).sum(1).max())
    out = {k: batch[k][rows, :n_in] for k in ("input_ids", "token_type_ids", "attention_mask", "marks") if k in batch}
    out |= {"labels": batch["labels"][rows, :n_out], "y": batch["y"][rows], "idx": batch["idx"][rows]}
    return {k: v.contiguous() for k, v in out.items()}


def summed_grads(model, probe: Probe, terms, amp, chunk: int) -> tuple[list, list[float]]:
    """For each loss term that `terms(model, rows, groups)` returns on a chunk of the probe, its BERT gradient summed
    over all chunks, in fp32 on the CPU, and the term's value summed. Only one chunk's graph and one gradient are on
    the GPU at a time (audit 09/11: the whole probe's graph plus 6 BERT gradients would not fit the 5060)."""
    acc, values = None, None
    for start in range(0, len(probe.batch["y"]), chunk):
        rows = rows_of(probe.batch, start, start + chunk)
        with amp():
            losses = terms(model, rows, probe.groups[start:start + chunk, :rows["labels"].shape[1]])
        if acc is None:
            acc = [[torch.zeros(p.shape) for p in measured_params(model)] for _ in losses]
            values = [0.0] * len(losses)
        for k, loss in enumerate(losses):
            for total, g in zip(acc[k], bert_grad(loss, model, retain_graph=k < len(losses) - 1)):
                total += g.float().cpu()
            values[k] += loss.item()
    return acc, values


def cls_term(n_pairs: int):
    """L_cls of a chunk, scaled so the chunks add up to the mean over the whole probe."""
    def terms(model, rows, groups):
        _, logit = model.encode(rows)
        return [cls_loss(logit, rows["y"], reduction="sum") / n_pairs]
    return terms


def cls_and_group_terms(n_pairs: int, n_tokens: int):
    def terms(model, rows, groups):
        h, logit = model.encode(rows)
        l_cls = cls_loss(logit, rows["y"], reduction="sum") / n_pairs
        return [l_cls] + split_aux_loss(model.decode(h, rows).logits, rows["labels"], groups, n_tokens)
    return terms


def probe_sizes(probe: Probe) -> tuple[int, int]:
    return len(probe.batch["y"]), int((probe.batch["labels"] != IGNORED).sum())


def measure_groups(model, probe: Probe, step: int, amp=contextlib.nullcontext, chunk: int = CHUNK_PAIRS) -> dict:
    """g_c and one L_aux gradient per group, reduced to fractions, shares, cosines and per-token losses.
    `amp` builds the autocast context of the forward pass; the gradients are taken outside it, as in training."""
    with evaluating(model):
        (g_c, *g_parts), (l_cls, *parts) = summed_grads(model, probe, cls_and_group_terms(*probe_sizes(probe)), amp,
                                                        chunk)
    g_a = [sum(layer) for layer in zip(*g_parts)]
    aa, cc = dot(g_a, g_a), dot(g_c, g_c)
    valid = probe.groups[probe.groups >= 0]
    row = {"step": step, "l_cls": l_cls, "l_aux": sum(parts), "norm_c": cc ** 0.5, "norm_a": aa ** 0.5,
           "cos_c_a": dot(g_c, g_a) / (cc * aa) ** 0.5}
    for g, part, g_x in zip(Group, parts, g_parts):
        frac = float((valid == g).float().mean())
        xx = dot(g_x, g_x)
        row |= {f"frac_tokens_{g.name}": frac, f"share_{g.name}": dot(g_x, g_a) / aa,
                f"cos_c_{g.name}": dot(g_c, g_x) / (cc * xx) ** 0.5 if xx else 0.0,
                f"l_{g.name}": part / frac if frac else 0.0}
    return row


def measure_words(model, probe: Probe, step: int, amp=contextlib.nullcontext, chunk: int = CHUNK_PAIRS) -> list[dict]:
    """One row per word occurrence: loss in the decoder, size of its push on BERT, and how much of it helps L_cls.
    g_c is summed in chunks; then one pair's graph at a time, one backward per word, reduced to numbers at once."""
    n_pairs, n_tokens = probe_sizes(probe)
    device = next(model.bert.parameters()).device
    rows = []
    with evaluating(model):
        ([g_c], _) = summed_grads(model, probe, cls_term(n_pairs), amp, chunk)
        g_c = [g.to(device) for g in g_c]
        norm_c = dot(g_c, g_c) ** 0.5
        for i, units in enumerate(probe.units):
            pair = rows_of(probe.batch, i, i + 1)
            with amp():
                h, _ = model.encode(pair)
                nll = token_nll(model.decode(h, pair).logits, pair["labels"])[0] / n_tokens
            for j, unit in enumerate(units):
                part = nll[list(unit.positions)].sum()
                g_t = bert_grad(part, model, retain_graph=j < len(units) - 1)
                ct, tt = dot(g_c, g_t), dot(g_t, g_t)
                rows.append({"step": step, "idx": int(pair["idx"]), "word": unit.word, "group": unit.group.name,
                             "n_tokens": len(unit.positions), "l_t": part.item() * n_tokens / len(unit.positions),
                             "norm_t": tt ** 0.5, "align_t": ct / norm_c,
                             "cos_t": ct / (norm_c * tt ** 0.5) if tt else 0.0})
    return rows
