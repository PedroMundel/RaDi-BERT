"""Distillation from a larger BERT into the student (plan, sections 11 to 11.5; Pedro's idea, 16/11).

The teacher is a frozen classifier (encoder + head). At every step the batch goes through it with no gradient, and
the student's auxiliary loss is the sum of what it is asked to imitate:
  answers     the teacher's label probabilities (Hinton et al. 2015)
  attention   the attention distributions: KL row by row, after averaging the heads on each side (the teacher has
              12, the student 8)
  hidden      the embedding output and the layers' hidden states: squared error after a learned projection to the
              teacher's size (TinyBERT, Jiao et al. 2020, eq. 8 and 9)
  values      the relation between the value vectors of every pair of tokens: KL, heads averaged as the attention
              (MiniLM, Wang et al. 2020, eq. 7 to 9; the head average is ours, the paper has 12 heads on both sides)
Which teacher layer teaches which student layer is a map: the last to the last (MiniLM) or evenly spaced layers
(TinyBERT).
"""
import math
from dataclasses import dataclass
from types import SimpleNamespace

import torch
import torch.nn.functional as F

from radibert import rte_dados as dados
from radibert.rte_modelo import Classifier, RationaleBert, logits_of, run_encoder

EPS = 1e-9


def last_map(n_student: int, n_teacher: int) -> dict[int, int]:
    """Student layer -> teacher layer (0-based): only the last of each."""
    return {n_student - 1: n_teacher - 1}


def uniform_map(n_student: int, n_teacher: int) -> dict[int, int]:
    """Student layer m (1-based) learns from teacher layer m * (n_teacher / n_student): 3, 6, 9, 12 for 4 and 12."""
    if n_teacher % n_student:
        raise ValueError(f"{n_teacher} teacher layers do not split evenly over {n_student} student layers")
    step = n_teacher // n_student
    return {m: (m + 1) * step - 1 for m in range(n_student)}


def attention_kl(student: torch.Tensor, teacher: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
    """KL(teacher || student) of one layer's attention, (pairs, heads, from, to) each: heads averaged on each side,
    one KL per row, mean over each pair's real rows, then over the pairs. In fp32, as the mark loss."""
    s, t = student.float().mean(1), teacher.float().mean(1)
    per_row = (t * (torch.log(t.clamp_min(EPS)) - torch.log(s.clamp_min(EPS)))).sum(-1)
    rows = attention_mask.float()
    return ((per_row * rows).sum(1) / rows.sum(1)).mean()


def hidden_mse(student: torch.Tensor, teacher: torch.Tensor, projection: torch.nn.Module,
               attention_mask: torch.Tensor) -> torch.Tensor:
    """Squared error between the teacher's vectors and the student's after the projection, (pairs, tokens, size)
    each: mean over the dimensions and each pair's real tokens, then over the pairs. In fp32, as the other losses."""
    with torch.autocast(student.device.type, enabled=False):
        per_token = ((projection(student.float()) - teacher.float()) ** 2).mean(-1)
        real = attention_mask.float()
        return ((per_token * real).sum(1) / real.sum(1)).mean()


def by_head(vectors: torch.Tensor, n_heads: int) -> torch.Tensor:
    """(pairs, tokens, size) -> (pairs, heads, tokens, size / heads), in fp32."""
    return vectors.view(*vectors.shape[:2], n_heads, -1).transpose(1, 2).float()


def scaled_dot_softmax(left: torch.Tensor, right: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
    """softmax(left right^T / sqrt(d_k)) per head, padding tokens left out of every row: (pairs, heads, tokens,
    tokens). Autocast off: under bf16 the product would go back to 8 mantissa bits."""
    with torch.autocast(left.device.type, enabled=False):
        scores = left @ right.transpose(-1, -2) / math.sqrt(left.shape[-1])
        return scores.masked_fill(attention_mask[:, None, None, :] == 0, float("-inf")).softmax(-1)


def value_relation(layer: torch.nn.Module, layer_input: torch.Tensor, attention_mask: torch.Tensor) -> torch.Tensor:
    """softmax(V V^T / sqrt(d_k)) of one BERT layer, one per head. The values are the layer's own `value`
    projection of its input."""
    attention = layer.attention.self
    values = by_head(attention.value(layer_input), attention.num_attention_heads)
    return scaled_dot_softmax(values, values, attention_mask)


def attention_before_dropout(layer: torch.nn.Module, layer_input: torch.Tensor,
                             attention_mask: torch.Tensor) -> torch.Tensor:
    """One BERT layer's attention distributions recomputed from its input: softmax(Q K^T / sqrt(d_k)) per head.
    What the model returns in training mode has already been through dropout (10% of the entries zeroed, rows that
    no longer add up to 1: audit and brute-test of 17/11); this is the same thing before it."""
    attention = layer.attention.self
    queries = by_head(attention.query(layer_input), attention.num_attention_heads)
    keys = by_head(attention.key(layer_input), attention.num_attention_heads)
    return scaled_dot_softmax(queries, keys, attention_mask)


def output_kl(student_logits: torch.Tensor, teacher_logits: torch.Tensor, temperature: float = 1.0) -> torch.Tensor:
    """KL(teacher || student) of the label probabilities, mean over the pairs (more than two labels). Both sides'
    logits are divided by the temperature, which spreads the probabilities, and the loss is multiplied by its
    square so the gradient keeps its size (Hinton et al. 2015)."""
    t = temperature
    return F.kl_div(F.log_softmax(student_logits.float() / t, -1), F.softmax(teacher_logits.float() / t, -1),
                    reduction="batchmean") * t * t


def target_kl(student_logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
    """KL(target || student) for target probabilities given directly, mean over the pairs."""
    targets = targets.float()
    log_ratio = torch.log(targets.clamp_min(EPS)) - F.log_softmax(student_logits.float(), -1)
    return (targets * log_ratio).sum(-1).mean()


def smoothed_targets(labels: list[int], n_labels: int, smoothing: float) -> torch.Tensor:
    """1 - smoothing on the right label, the rest shared evenly by the others: a soft target with no teacher."""
    targets = torch.full((len(labels), n_labels), smoothing / (n_labels - 1))
    targets[torch.arange(len(labels)), torch.tensor(labels)] = 1 - smoothing
    return targets


def swapped_within_label(probs: torch.Tensor, labels: list[int], seed: int) -> torch.Tensor:
    """Each pair gets the teacher's probabilities of another pair with the same gold label (a fixed shuffle inside
    each label): the same soft targets overall, but no longer about that pair."""
    out = probs.clone()
    generator = torch.Generator().manual_seed(seed)
    by_label = torch.tensor(labels)
    for label in by_label.unique():
        rows = (by_label == label).nonzero().squeeze(1)
        out[rows] = probs[rows[torch.randperm(len(rows), generator=generator)]]
    return out


@dataclass
class TargetTable:
    """Fixed soft targets, one row of label probabilities per train pair, looked up by the pair's idx. Stands where
    a Distillation stands (RationaleBert.distill) for the arms that have no live teacher."""
    targets: dict[int, torch.Tensor]

    def terms(self, student: RationaleBert, student_out, student_logits: torch.Tensor, batch: dict) -> dict:
        rows = torch.stack([self.targets[i] for i in batch["idx"].tolist()]).to(student_logits.device)
        return {"answers": target_kl(student_logits, rows)}


def label_rate_logits(rows: torch.Tensor, labels: list[int], n_labels: int) -> torch.Tensor:
    """For each gold label and group, the logit of how often the group shows up among that label's pairs (half a
    pair added to each side, so a group a label never has stays finite). The group head's label bias starts here:
    at the classifier's learning rate it could never get there from zero (training audit, 17/11), and with it in
    place the head's linear layer is left with what the label does not explain."""
    by_label = torch.tensor(labels)
    logits = torch.zeros(n_labels, rows.shape[1])
    for label in range(n_labels):
        of_label = rows[by_label == label].float()
        rate = (of_label.sum(0) + 0.5) / (len(of_label) + 1)
        logits[label] = torch.log(rate) - torch.log1p(-rate)
    return logits


@dataclass
class GroupTargets:
    """The auxiliary target of plan section 11.8: for each train pair (looked up by idx), a 0/1 row saying which
    groups of new words show up in its rationale. The student's group head (RationaleBert.with_group_head) predicts
    the row from the [CLS] vector. With `teacher`, that Distillation's losses come along in the same sum."""
    targets: dict[int, torch.Tensor]
    teacher: "Distillation | None" = None

    def group_losses(self, student: RationaleBert, student_out, batch: dict) -> torch.Tensor:
        """Binary cross-entropy of each group, mean over the pairs: one value per group."""
        logits = student.group_logits(student_out.last_hidden_state, batch["y"])
        rows = torch.stack([self.targets[i] for i in batch["idx"].tolist()]).to(logits.device)
        return F.binary_cross_entropy_with_logits(logits, rows.float(), reduction="none").mean(0)

    def terms(self, student: RationaleBert, student_out, student_logits: torch.Tensor, batch: dict) -> dict:
        terms = self.teacher.terms(student, student_out, student_logits, batch) if self.teacher is not None else {}
        return terms | {"groups": self.group_losses(student, student_out, batch).mean()}


def pair_part(teacher_out, student_mask: torch.Tensor) -> SimpleNamespace:
    """The teacher's output cut to the student's positions, for a teacher that read more than the student. Hidden
    states: the first `width` positions. Attention: the square among the student's real positions, each row divided
    by what is left of it, so it adds up to 1 again (the rest went to tokens the student does not have)."""
    width = student_mask.shape[1]
    hidden = teacher_out.hidden_states and tuple(h[:, :width] for h in teacher_out.hidden_states)
    attentions = None
    if teacher_out.attentions:
        kept = [a[:, :, :width, :width].float() * student_mask[:, None, None, :] for a in teacher_out.attentions]
        attentions = tuple(a / a.sum(-1, keepdim=True).clamp_min(EPS) for a in kept)
    return SimpleNamespace(hidden_states=hidden, attentions=attentions)


@dataclass
class Distillation:
    """What RationaleBert.forward calls when it has a teacher. Not a module: the teacher stays out of the student's
    parameters, optimizer and evaluation copy. Each map is student layer -> teacher layer (0-based) and turns one
    loss on; `hidden_map` also turns on the embedding loss and needs RationaleBert.with_projections."""
    teacher: Classifier
    layer_map: dict[int, int] | None = None  # attention
    answers: bool = False
    temperature: float = 1.0  # of the answers
    hidden_map: dict[int, int] | None = None
    value_map: dict[int, int] | None = None
    before_dropout: bool = False  # the student's attention is read before its dropout (attention_before_dropout)
    # idx -> the item the TEACHER reads for that pair: the student's own tokens first, in the same positions, then
    # more (the rationale: docs/2026-11-18-professor-que-le-a-justificativa.md). The student imitates only the
    # positions it has (pair_part). Not with `answers` or `value_map`: those would need the teacher's whole input.
    teacher_inputs: dict[int, dict] | None = None

    def __post_init__(self):
        if self.teacher_inputs is not None and (self.answers or self.value_map is not None):
            raise ValueError("teacher_inputs works with the attention and hidden-state losses only")

    def student_attention(self, student: RationaleBert, student_out, layer: int, mask: torch.Tensor) -> torch.Tensor:
        if not self.before_dropout:
            return student_out.attentions[layer]
        return attention_before_dropout(student.bert.encoder.layer[layer], student_out.hidden_states[layer], mask)

    @torch.no_grad()
    def teacher_pass(self, batch: dict) -> tuple:
        self.teacher.eval()
        read = batch if self.teacher_inputs is None else self.teacher_batch(batch)
        out = run_encoder(self.teacher.bert, read, output_attentions=self.layer_map is not None,
                          output_hidden_states=self.hidden_map is not None or self.value_map is not None)
        logits = logits_of(self.teacher.bert, self.teacher.head, out.last_hidden_state, read["attention_mask"])
        return (out if self.teacher_inputs is None else pair_part(out, batch["attention_mask"])), logits

    def teacher_batch(self, batch: dict) -> dict:
        """What the teacher reads for the student's batch, pair by pair in the same order."""
        device = batch["input_ids"].device
        read = dados.collate([self.teacher_inputs[i] for i in batch["idx"].tolist()])
        width = batch["input_ids"].shape[1]
        if not torch.equal(read["input_ids"][:, :width].to(device) * batch["attention_mask"], batch["input_ids"]):
            raise ValueError("the teacher's input does not start with the student's own tokens")
        return {name: value.to(device) for name, value in read.items()}

    @torch.no_grad()
    def teacher_relation(self, layer: int, teacher_out, mask: torch.Tensor) -> torch.Tensor:
        return value_relation(self.teacher.bert.encoder.layer[layer], teacher_out.hidden_states[layer], mask)

    def terms(self, student: RationaleBert, student_out, student_logits: torch.Tensor, batch: dict) -> dict:
        """Each loss that is on, by name. hidden_states[k] is the input of layer k and the output of layer k - 1."""
        if not (self.answers or self.layer_map or self.hidden_map or self.value_map):
            raise ValueError("this Distillation has no loss on: set answers or one of the layer maps")
        if self.hidden_map is not None and student.projections is None:
            raise ValueError("hidden_map needs the student's projections: call RationaleBert.with_projections first")
        teacher_out, teacher_logits = self.teacher_pass(batch)
        mask = batch["attention_mask"]
        terms = {}
        if self.answers:
            terms["answers"] = output_kl(student_logits, teacher_logits, self.temperature)
        if self.layer_map is not None:
            terms["attention"] = sum(attention_kl(self.student_attention(student, student_out, s, mask),
                                                  teacher_out.attentions[t], mask)
                                     for s, t in self.layer_map.items())
        if self.hidden_map is not None:
            terms["embeddings"] = hidden_mse(student_out.hidden_states[0], teacher_out.hidden_states[0],
                                             student.projections["embeddings"], mask)
            terms["hidden"] = sum(hidden_mse(student_out.hidden_states[s + 1], teacher_out.hidden_states[t + 1],
                                             student.projections["hidden"], mask)
                                  for s, t in self.hidden_map.items())
        if self.value_map is not None:
            layers = student.bert.encoder.layer
            terms["values"] = sum(attention_kl(value_relation(layers[s], student_out.hidden_states[s], mask),
                                               self.teacher_relation(t, teacher_out, mask), mask)
                                  for s, t in self.value_map.items())
        return terms
