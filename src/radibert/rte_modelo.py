"""BERT + classification head, with the T5 decoder as auxiliary head (Agrawal, Ahemad & Sembium 2025, §4.3).

The T5 decoder reads the BERT vectors as if they were its own encoder's output: T5ForConditionalGeneration only runs
its encoder when `encoder_outputs` is empty (modeling_t5.py v5.20.2, l. 1009), and the attention mask passed with it
becomes the cross-attention mask (l. 1037). The T5 encoder stays loaded but frozen and out of the optimizer.
"""
import copy

import torch
from torch import nn
from transformers import AutoModel, T5ForConditionalGeneration

HEAD_DROPOUT = 0.1  # E7: BERT's own default; the paper does not say


def classify(bert: nn.Module, head: nn.Module, batch: dict) -> tuple[torch.Tensor, torch.Tensor]:
    """BERT vectors of every token, and the entailment logit from the [CLS] vector. Training and evaluation both
    call this, so the classifier evaluated is the one trained. The head runs in fp32 even under bf16 autocast:
    with 8 mantissa bits, 277 dev probabilities would tie and coarsen ROC-AUC (audit 09/11)."""
    h = bert(input_ids=batch["input_ids"], attention_mask=batch["attention_mask"],
             token_type_ids=batch["token_type_ids"]).last_hidden_state
    with torch.autocast(h.device.type, enabled=False):
        return h, head(h[:, 0].float()).squeeze(-1)


class RationaleBert(nn.Module):
    def __init__(self, bert: nn.Module, t5: T5ForConditionalGeneration | None):
        super().__init__()
        hidden = bert.config.hidden_size
        self.bert = bert
        self.head = nn.Sequential(nn.Dropout(HEAD_DROPOUT), nn.Linear(hidden, 1))
        self.t5 = t5
        self.bridge = None
        if t5 is not None:
            freeze_t5_encoder(t5)
            if hidden != t5.config.d_model:  # only the CPU smoke test (D6): tiny BERT, 128 -> 768
                self.bridge = nn.Linear(hidden, t5.config.d_model)

    @classmethod
    def from_pretrained(cls, bert_name: str, t5_name: str | None) -> "RationaleBert":
        bert = AutoModel.from_pretrained(bert_name, add_pooling_layer=False)  # the head reads [CLS] directly
        t5 = T5ForConditionalGeneration.from_pretrained(t5_name) if t5_name else None
        return cls(bert, t5)

    def encode(self, batch: dict) -> tuple[torch.Tensor, torch.Tensor]:
        return classify(self.bert, self.head, batch)

    def decode(self, h: torch.Tensor, batch: dict):
        """T5 decoder over the BERT vectors, teacher-forced on the rationale; `.loss` is L_aux."""
        memory = self.bridge(h) if self.bridge is not None else h
        return self.t5(encoder_outputs=(memory,), attention_mask=batch["attention_mask"], labels=batch["labels"])

    def forward(self, batch: dict) -> tuple[torch.Tensor, torch.Tensor | None]:
        h, logit = self.encode(batch)
        return logit, (self.decode(h, batch).loss if self.t5 is not None else None)


def freeze_t5_encoder(t5: T5ForConditionalGeneration):
    """Freezes the encoder blocks only: its embedding is the `shared` matrix the decoder and lm_head also use."""
    t5.encoder.block.requires_grad_(False)
    t5.encoder.final_layer_norm.requires_grad_(False)


class Classifier(nn.Module):
    """What evaluation sees: a copy of BERT and the head, with no decoder in the object (I8)."""

    def __init__(self, bert: nn.Module, head: nn.Module):
        super().__init__()
        self.bert, self.head = bert, head

    def forward(self, batch: dict) -> torch.Tensor:
        return classify(self.bert, self.head, batch)[1]


def classifier_only(model: RationaleBert) -> Classifier:
    return Classifier(copy.deepcopy(model.bert), copy.deepcopy(model.head))
