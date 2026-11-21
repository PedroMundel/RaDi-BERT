"""Attention intervention (plan, section 10.1): what is cut, where, and that nothing else moves."""
import pytest
import torch
from transformers import AutoTokenizer

from radibert import rte_intervencao as intervencao
from radibert.rte_modelo import RationaleBert, run_encoder

TINY = "google/bert_uncased_L-2_H-128_A-2"
PREMISE = "The company opened a factory in Recife in 2019."
HYPOTHESIS = "The company opened a factory in Salvador."


@pytest.fixture(scope="module")
def model():
    torch.manual_seed(0)
    return RationaleBert.with_mark_attention(TINY).eval()


@pytest.fixture(scope="module")
def batch():
    """Two pairs, the second padded; marks on two positions of the first and one of the second."""
    tok = AutoTokenizer.from_pretrained(TINY)
    enc = tok([PREMISE, "A dog runs."], [HYPOTHESIS, "It runs."], padding=True, return_tensors="pt")
    marks = torch.zeros_like(enc["input_ids"])
    marks[0, [3, 7]] = 1
    marks[1, 2] = 1
    return dict(enc) | {"marks": marks}


def attentions(model, batch):
    with torch.no_grad():
        return run_encoder(model.bert, batch, output_attentions=True).attentions


def logits(model, batch):
    with torch.no_grad():
        return model.encode(batch)[1]


def test_layer_sets_are_each_layer_each_pair_and_all():
    assert intervencao.layer_sets(4) == [(0,), (1,), (2,), (3,), (0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3),
                                         (0, 1, 2, 3)]
    assert intervencao.layer_sets(2) == [(0,), (1,), (0, 1)]


def test_nothing_forbidden_leaves_the_logits_identical(model, batch):
    nothing = torch.zeros_like(batch["marks"]).bool()
    plain = logits(model, batch)
    with intervencao.restricted_attention(model.bert, (0, 1), nothing, cls_only=False):
        assert torch.equal(logits(model, batch), plain)


def test_block_zeroes_the_cls_attention_on_the_marks_in_that_layer_only(model, batch):
    plain = attentions(model, batch)
    forbidden = intervencao.forbidden_positions(batch["marks"], batch["attention_mask"], "block")
    with intervencao.restricted_attention(model.bert, (1,), forbidden, cls_only=True):
        cut = attentions(model, batch)
    cls_row = cut[1][:, :, 0, :]
    assert cls_row[forbidden[:, None, :].expand_as(cls_row)].max() < 1e-6
    assert torch.allclose(cls_row.sum(-1), torch.ones(2, 2), atol=1e-5)
    assert torch.equal(cut[0], plain[0])  # the layer before the cut does not move
    assert torch.allclose(cut[1][:, :, 1:, :], plain[1][:, :, 1:, :], atol=1e-6)  # nor the other rows of the layer
    assert plain[1][:, :, 0, :][forbidden[:, None, :].expand_as(cls_row)].min() > 1e-6  # there was something to cut


def test_block_on_every_row_stops_all_tokens_from_looking_at_the_marks(model, batch):
    forbidden = intervencao.forbidden_positions(batch["marks"], batch["attention_mask"], "block")
    with intervencao.restricted_attention(model.bert, (0,), forbidden, cls_only=False):
        cut = attentions(model, batch)[0]
    assert cut[forbidden[:, None, None, :].expand_as(cut)].max() < 1e-6


def test_only_leaves_the_cls_attention_on_the_marks_and_on_cls(model, batch):
    forbidden = intervencao.forbidden_positions(batch["marks"], batch["attention_mask"], "only")
    assert forbidden[0].sum() == batch["attention_mask"][0].sum() - 3  # all real positions but 2 marks and [CLS]
    assert not forbidden[1, batch["attention_mask"][1] == 0].any()  # padding is BERT's own business
    with intervencao.restricted_attention(model.bert, (0, 1), forbidden, cls_only=True):
        cut = attentions(model, batch)
    allowed = batch["marks"].bool() | (torch.arange(batch["marks"].shape[1]) == 0)
    for layer in cut:
        mass = (layer[:, :, 0, :] * allowed[:, None, :]).sum(-1)
        assert torch.allclose(mass, torch.ones(2, 2), atol=1e-5)


def test_the_cut_changes_the_logits_and_is_gone_after_the_block(model, batch):
    plain = logits(model, batch)
    forbidden = intervencao.forbidden_positions(batch["marks"], batch["attention_mask"], "only")
    with intervencao.restricted_attention(model.bert, (0, 1), forbidden, cls_only=False):
        assert not torch.allclose(logits(model, batch), plain)
    assert torch.equal(logits(model, batch), plain)


def test_unknown_operation_is_refused(batch):
    with pytest.raises(ValueError):
        intervencao.forbidden_positions(batch["marks"], batch["attention_mask"], "erase")


def test_content_positions_skip_function_words_and_special_tokens():
    tok = AutoTokenizer.from_pretrained(TINY)
    ids = tok(PREMISE, HYPOTHESIS)["input_ids"]
    words = {tok.convert_ids_to_tokens(ids[p]) for p in intervencao.content_positions(PREMISE, HYPOTHESIS, tok)}
    assert {"company", "factory", "salvador", "2019"} <= words
    assert not words & {"the", "a", "in", "[CLS]", "[SEP]", "."}


def test_content_draw_keeps_the_count_stays_in_the_candidates_and_reproduces():
    candidates = [2, 3, 5, 8, 9, 12]
    draw = intervencao.content_draw(3, candidates, torch.Generator().manual_seed(1))
    assert len(draw) == 3 and set(draw) <= set(candidates)
    assert draw == intervencao.content_draw(3, candidates, torch.Generator().manual_seed(1))
    assert intervencao.content_draw(9, candidates, torch.Generator().manual_seed(1)) == candidates
