"""BERT + classification head, with the T5 decoder as auxiliary head (Agrawal, Ahemad & Sembium 2025, §4.3).

The T5 decoder reads the BERT vectors as if they were its own encoder's output: T5ForConditionalGeneration only runs
its encoder when `encoder_outputs` is empty (modeling_t5.py v5.20.2, l. 1009), and the attention mask passed with it
becomes the cross-attention mask (l. 1037). The T5 encoder stays loaded but frozen and out of the optimizer.

T5-encoder arms (10/11, AUTONOMIA.md): the classifier's encoder is the T5 encoder itself; with a decoder it is the
SAME model's encoder (`t5.encoder`), trained, so the decoder reads its own encoder (the bridge test). T5 has no [CLS]:
the head reads the mean of the real tokens' vectors (Sentence-T5's pooling).
"""
import copy

import torch
import torch.nn.functional as F
from torch import nn
from transformers import AutoModel, T5EncoderModel, T5ForConditionalGeneration

HEAD_DROPOUT = 0.1  # E7: BERT's own default; the paper does not say


def is_t5(encoder: nn.Module) -> bool:
    return encoder.config.model_type == "t5"


def run_encoder(bert: nn.Module, batch: dict, output_attentions: bool = False, output_hidden_states: bool = False):
    extra = {} if is_t5(bert) else {"token_type_ids": batch["token_type_ids"]}
    return bert(input_ids=batch["input_ids"], attention_mask=batch["attention_mask"],
                output_attentions=output_attentions, output_hidden_states=output_hidden_states, **extra)


def classify(bert: nn.Module, head: nn.Module, batch: dict) -> tuple[torch.Tensor, torch.Tensor]:
    """Encoder vectors of every token, and the logits from the [CLS] vector (BERT) or the mean of the real tokens
    (T5): one logit per pair for two labels, one per label otherwise. Training and evaluation both call this, so the
    classifier evaluated is the one trained."""
    h = run_encoder(bert, batch).last_hidden_state
    return h, logits_of(bert, head, h, batch["attention_mask"])


def logits_of(bert: nn.Module, head: nn.Module, h: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    """The head runs in fp32 even under bf16 autocast: with 8 mantissa bits, 277 dev probabilities would tie and
    coarsen ROC-AUC (audit 09/11)."""
    with torch.autocast(h.device.type, enabled=False):
        if is_t5(bert):
            m = mask.unsqueeze(-1).float()
            pooled = (h.float() * m).sum(1) / m.sum(1)
        else:
            pooled = h[:, 0].float()
        logits = head(pooled)
        return logits.squeeze(-1) if logits.shape[-1] == 1 else logits


def mark_loss(attention: torch.Tensor, marks: torch.Tensor) -> torch.Tensor | None:
    """-log of the [CLS] attention mass on the marked positions, mean over the pairs that have a mark; None when no
    pair has one. `attention` is one layer's (pairs, heads, from, to); the mass is the mean over heads of row [CLS].
    Computed in fp32: under bf16 the probabilities have 8 mantissa bits."""
    has_mark = marks.sum(1) > 0
    if not has_mark.any():
        return None
    mass = (attention[:, :, 0, :].float().mean(1) * marks).sum(1)
    return -torch.log(mass[has_mark].clamp_min(1e-6)).mean()


def token_mark_loss(logits: torch.Tensor, marks: torch.Tensor, mask: torch.Tensor) -> torch.Tensor | None:
    """Token head: binary cross-entropy of one logit per input position against the marks, mean over each pair's
    real tokens, then over the pairs that have a mark; None when no pair has one. In fp32, as mark_loss."""
    has_mark = marks.sum(1) > 0
    if not has_mark.any():
        return None
    per_token = F.binary_cross_entropy_with_logits(logits.float(), marks.float(), reduction="none") * mask
    return (per_token.sum(1) / mask.sum(1))[has_mark].mean()


def cls_loss(logits: torch.Tensor, y: torch.Tensor, reduction: str = "mean") -> torch.Tensor:
    """L_cls: binary cross-entropy on the single logit (RTE), cross-entropy over the labels otherwise (e-SNLI)."""
    if logits.dim() == 1:
        return F.binary_cross_entropy_with_logits(logits, y.float(), reduction=reduction)
    return F.cross_entropy(logits, y.long(), reduction=reduction)


class RationaleBert(nn.Module):
    def __init__(self, bert: nn.Module, t5: T5ForConditionalGeneration | None, n_labels: int = 2):
        super().__init__()
        hidden = bert.config.d_model if is_t5(bert) else bert.config.hidden_size
        self.bert = bert
        self.head = nn.Sequential(nn.Dropout(HEAD_DROPOUT), nn.Linear(hidden, 1 if n_labels == 2 else n_labels))
        self.t5 = t5
        self.mark_attention = False
        self.mark_layers = (-1,)  # the layers whose [CLS] attention the mark loss reads (plan, section 10.2)
        self.distill = None  # rte_destilacao.Distillation: a frozen teacher the student imitates
        self.projections = None  # with_projections: student size -> teacher size, for the hidden-state loss
        self.token_head = None  # with_token_head: one logit per input position, trained on the marks
        self.group_head = None  # with_group_head: one logit per group of rationale words, read off the [CLS] vector
        self.group_label_bias = None
        self.decoder_calendar = False  # no decoder, but the decoder arm's schedule (rte_treino, arm bert_calendar)
        self.bridge = None
        if t5 is not None:
            if not self.shares_t5_encoder:
                freeze_t5_encoder(t5)
            if hidden != t5.config.d_model:  # smaller encoders (small 512, tiny 128) and the CPU smoke test
                self.bridge = nn.Linear(hidden, t5.config.d_model)

    @property
    def shares_t5_encoder(self) -> bool:
        """True in the T5-encoder arm with decoder: the classifier's encoder is the T5's own, and it trains."""
        return self.t5 is not None and self.bert is self.t5.encoder

    @classmethod
    def from_pretrained(cls, bert_name: str, t5_name: str | None, n_labels: int = 2) -> "RationaleBert":
        bert = AutoModel.from_pretrained(bert_name, add_pooling_layer=False)  # the head reads [CLS] directly
        t5 = T5ForConditionalGeneration.from_pretrained(t5_name) if t5_name else None
        return cls(bert, t5, n_labels)

    @classmethod
    def with_mark_attention(cls, bert_name: str, n_labels: int = 2, layers: tuple[int, ...] = (-1,)) -> "RationaleBert":
        """No decoder; the auxiliary loss is mark_loss on the [CLS] attention of `layers` (the last one by default;
        with several, the sum of each layer's loss, so each layer is pulled as hard as when it is alone) when the
        batch carries `marks` (rte_marcas). Eager attention: the default implementation does not return the
        probabilities."""
        model = cls(AutoModel.from_pretrained(bert_name, add_pooling_layer=False, attn_implementation="eager"), None,
                    n_labels)
        model.mark_attention = True
        model.mark_layers = layers
        return model

    @classmethod
    def with_token_head(cls, bert_name: str, n_labels: int = 2) -> "RationaleBert":
        """No decoder and no attention loss; a linear layer on each token's last vector learns the marks directly
        (token_mark_loss). The reference for the highlight read off the [CLS] attention (10/11)."""
        model = cls(AutoModel.from_pretrained(bert_name, add_pooling_layer=False), None, n_labels)
        model.token_head = nn.Linear(model.bert.config.hidden_size, 1)
        return model

    def with_projections(self, teacher_hidden: int) -> "RationaleBert":
        """Adds the two learned matrices of TinyBERT (Jiao et al. 2020, eq. 8 and 9): one takes the student's
        embedding output to the teacher's size, the other its layers' hidden states (shared by the layers: our
        reading of eq. 8). Trained with the student, absent from the evaluation copy."""
        hidden = self.bert.config.hidden_size
        self.projections = nn.ModuleDict({name: nn.Linear(hidden, teacher_hidden)
                                          for name in ("embeddings", "hidden")})
        return self

    def with_group_head(self, label_bias: torch.Tensor) -> "RationaleBert":
        """Adds the head of plan section 11.8: a linear layer on the [CLS] vector the classifier reads, one logit
        per group of new rationale words, plus one bias per gold label and group. `label_bias` (labels x groups) is
        where that bias starts (rte_destilacao.label_rate_logits): what the label alone explains sits there, and the
        encoder never sees it. Trained with the student, absent from the evaluation copy."""
        n_labels, n_groups = label_bias.shape
        self.group_head = nn.Linear(self.bert.config.hidden_size, n_groups, bias=False)
        self.group_label_bias = nn.Embedding(n_labels, n_groups)
        with torch.no_grad():
            self.group_label_bias.weight.copy_(label_bias)
        return self

    def group_logits(self, h: torch.Tensor, y: torch.Tensor) -> torch.Tensor:
        """One logit per pair and group, in fp32 as the classifier's head."""
        with torch.autocast(h.device.type, enabled=False):
            return self.group_head(h[:, 0].float()) + self.group_label_bias(y.long())

    def distill_terms(self, batch: dict) -> tuple[torch.Tensor, dict[str, torch.Tensor]]:
        """Logits and each distillation loss by name (rte_destilacao); the auxiliary loss is their sum."""
        out = run_encoder(self.bert, batch, output_attentions=True, output_hidden_states=True)
        logit = logits_of(self.bert, self.head, out.last_hidden_state, batch["attention_mask"])
        return logit, self.distill.terms(self, out, logit, batch)

    def token_logits(self, h: torch.Tensor) -> torch.Tensor:
        with torch.autocast(h.device.type, enabled=False):
            return self.token_head(h.float()).squeeze(-1)

    @classmethod
    def from_t5(cls, t5_name: str, with_decoder: bool, n_labels: int = 2) -> "RationaleBert":
        """T5 encoder as the classifier's encoder; with the decoder, both from the same checkpoint."""
        if with_decoder:
            t5 = T5ForConditionalGeneration.from_pretrained(t5_name)
            return cls(t5.encoder, t5, n_labels)
        return cls(T5EncoderModel.from_pretrained(t5_name), None, n_labels)

    def encode(self, batch: dict) -> tuple[torch.Tensor, torch.Tensor]:
        return classify(self.bert, self.head, batch)

    def decode(self, h: torch.Tensor, batch: dict):
        """T5 decoder over the encoder vectors, teacher-forced on the rationale; `.loss` is L_aux."""
        memory = self.bridge(h) if self.bridge is not None else h
        return self.t5(encoder_outputs=(memory,), attention_mask=batch["attention_mask"], labels=batch["labels"])

    def forward(self, batch: dict) -> tuple[torch.Tensor, torch.Tensor | None]:
        """Logits and the auxiliary loss: L_aux of the decoder, the mark loss (attention or token head), the
        distillation loss against a teacher, or None."""
        if self.distill is not None:
            logit, terms = self.distill_terms(batch)
            return logit, sum(terms.values())
        if self.token_head is not None:
            h, logit = self.encode(batch)
            if "marks" not in batch:
                return logit, None
            return logit, token_mark_loss(self.token_logits(h), batch["marks"], batch["attention_mask"])
        if self.mark_attention:
            out = run_encoder(self.bert, batch, output_attentions="marks" in batch)
            logit = logits_of(self.bert, self.head, out.last_hidden_state, batch["attention_mask"])
            if "marks" not in batch:
                return logit, None
            losses = [mark_loss(out.attentions[k], batch["marks"]) for k in self.mark_layers]
            return logit, (None if losses[0] is None else sum(losses))
        h, logit = self.encode(batch)
        return logit, (self.decode(h, batch).loss if self.t5 is not None else None)


def freeze_t5_encoder(t5: T5ForConditionalGeneration):
    """Freezes the encoder blocks only: its embedding is the `shared` matrix the decoder and lm_head also use."""
    t5.encoder.block.requires_grad_(False)
    t5.encoder.final_layer_norm.requires_grad_(False)


class Classifier(nn.Module):
    """What evaluation sees: a copy of the encoder and the head, with no decoder in the object (I8)."""

    def __init__(self, bert: nn.Module, head: nn.Module):
        super().__init__()
        self.bert, self.head = bert, head

    def forward(self, batch: dict) -> torch.Tensor:
        return classify(self.bert, self.head, batch)[1]


def classifier_only(model: RationaleBert) -> Classifier:
    return Classifier(copy.deepcopy(model.bert), copy.deepcopy(model.head))
