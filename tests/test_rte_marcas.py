"""Marks for the [CLS] attention experiment: which positions are marked, the random control, and the loss."""
import re

import pandas as pd
import pytest
import torch
from transformers import AutoTokenizer

from radibert import rte_dados as dados
from radibert import rte_marcas as marcas
from radibert import rte_treino as treino
from radibert.rte_modelo import RationaleBert, classifier_only, mark_loss, run_encoder, token_mark_loss

TINY = "google/bert_uncased_L-2_H-128_A-2"
NO_LABEL_EXPR = re.compile(r"(?!x)x")  # matches nothing: no word is a label word in these tests
PREMISE = "The company opened a factory in Recife in 2019."
HYPOTHESIS = "The company opened a factory in Salvador."
RATIONALE = "It says the factory is in Recife, and Salvador is another city."


@pytest.fixture(scope="module")
def tok():
    return dados.Tokenizers(AutoTokenizer.from_pretrained(TINY), AutoTokenizer.from_pretrained(dados.T5))


def marked_words(tok, positions: list[int]) -> set[str]:
    ids = tok.bert(PREMISE, HYPOTHESIS)["input_ids"]
    return {tok.bert.convert_ids_to_tokens(ids[p]) for p in positions}


def test_real_marks_are_the_pair_words_the_rationale_copies(tok):
    positions = marcas.real_marks(PREMISE, HYPOTHESIS, RATIONALE, NO_LABEL_EXPR, tok.bert)
    # "factory", "recife" and "salvador" are copied; "the", "in", "is" are function words; "company" is not copied
    words = marked_words(tok, positions)
    assert {"factory", "salvador"} <= words and "company" not in words and "the" not in words
    assert "[CLS]" not in words and "[SEP]" not in words
    # "factory" is in both sentences and "recife" may split in word pieces: every piece of every occurrence is marked
    ids = tok.bert(PREMISE, HYPOTHESIS)["input_ids"]
    factory = tok.bert.convert_tokens_to_ids("factory")
    assert sum(ids[p] == factory for p in positions) == 2


def test_rationale_that_copies_nothing_marks_nothing(tok):
    assert marcas.real_marks(PREMISE, HYPOTHESIS, "Unrelated words only.", NO_LABEL_EXPR, tok.bert) == []


def pairs_frame() -> pd.DataFrame:
    return pd.DataFrame({"idx": [7, 8], "y": [0, 1], "sentence1": [PREMISE, PREMISE],
                         "sentence2": [HYPOTHESIS, "The company opened a factory."],
                         "rationale": [RATIONALE, "Unrelated words only."]})


def test_random_marks_keep_the_count_avoid_special_tokens_and_reproduce(tok):
    table = marcas.mark_table(pairs_frame(), tok, NO_LABEL_EXPR)
    again = marcas.mark_table(pairs_frame(), tok, NO_LABEL_EXPR)
    assert list(table["random"]) == list(again["random"])
    for row in table.itertuples():
        seq_ids = tok.bert(*pairs_frame().set_index("idx").loc[row.idx, ["sentence1", "sentence2"]]).sequence_ids()
        assert len(row.random) == len(row.real) == len(set(row.random))
        assert all(seq_ids[p] is not None for p in row.random) and row.n_tokens == len(seq_ids)
    assert table.set_index("idx").loc[8, "real"] == []


def test_with_marks_aligns_marks_to_the_input_and_collate_pads_them(tok):
    pairs = pairs_frame()
    table = marcas.mark_table(pairs, tok, NO_LABEL_EXPR)
    items = marcas.with_marks(dados.encode(pairs, tok), table, "real")
    assert all(len(it["marks"]) == len(it["input_ids"]) for it in items)
    assert [i for i, m in enumerate(items[0]["marks"]) if m] == table.set_index("idx").loc[7, "real"]
    batch = dados.collate(items)
    assert batch["marks"].shape == batch["input_ids"].shape and marcas.marked_pairs(batch) == 1
    assert "marks" not in dados.collate(dados.encode(pairs, tok))


def test_mark_loss_is_minus_log_of_the_cls_mass_on_the_marks():
    attention = torch.zeros(2, 2, 3, 3)
    attention[0, :, 0] = torch.tensor([[0.2, 0.6, 0.2], [0.2, 0.2, 0.6]])  # mean over heads: 0.2, 0.4, 0.4
    attention[1, :, 0] = torch.tensor([0.5, 0.25, 0.25])
    marks = torch.tensor([[0, 1, 0], [0, 0, 0]])  # the second pair has no mark and stays out of the mean
    assert torch.isclose(mark_loss(attention, marks), -torch.log(torch.tensor(0.4)))
    assert mark_loss(attention, torch.zeros(2, 3, dtype=torch.long)) is None


def test_one_step_on_the_mark_loss_moves_the_cls_attention_to_the_marks(tok):
    torch.manual_seed(0)
    pairs = pairs_frame()
    table = marcas.mark_table(pairs, tok, NO_LABEL_EXPR)
    batch = dados.collate(marcas.with_marks(dados.encode(pairs, tok), table, "real"))
    model = RationaleBert.with_mark_attention(TINY).eval()  # eval: no dropout, so the two losses are comparable
    _, before = model(batch)
    before.backward()
    assert any(p.grad is not None and p.grad.abs().sum() > 0 for p in model.bert.parameters())
    with torch.no_grad():
        for p in model.bert.parameters():
            if p.grad is not None:
                p -= 0.01 * p.grad
    assert model(batch)[1] < before
    plain = dados.collate(dados.encode(pairs, tok))
    assert model(plain)[1] is None  # marks_none: same model, no auxiliary loss


def test_micro_batches_add_up_to_the_full_batch_mark_loss(tok):
    """I16 for the mark arms: the pair without marks must not dilute or drop the other's loss."""
    torch.manual_seed(0)
    pairs = pd.concat([pairs_frame(), pairs_frame().assign(idx=[9, 10])], ignore_index=True)
    table = marcas.mark_table(pairs, tok, NO_LABEL_EXPR)
    batch = dados.collate(marcas.with_marks(dados.encode(pairs, tok), table, "real"))
    model = RationaleBert.with_mark_attention(TINY).eval()
    _, full = model(batch)
    _, summed = treino.accumulated_backward(model, batch, treino.marked_loss, micro=1)
    assert summed == pytest.approx(full.item(), rel=1e-4)


needs_rte = pytest.mark.skipif(not dados.FA_CSV.exists() or not (dados.RTE / "rte_train.parquet").exists(),
                               reason="dados/rte ou o lote FA não estão no disco")


@needs_rte
def test_low_data_sizes_are_nested_and_share_one_held_out_set_disjoint_from_both(tok, tmp_path):
    real = dados.Tokenizers(AutoTokenizer.from_pretrained(dados.BERT), tok.t5)
    small = treino.load_data(real, tmp_path, n_pairs=500, group_probe=8, word_probe=4, with_marks=True, held_out=True)
    large = treino.load_data(real, tmp_path, n_pairs=1000, group_probe=8, word_probe=4, held_out=True)
    ids = lambda items: [it["idx"] for it in items]  # noqa: E731
    assert ids(small.train) == ids(large.train)[:500] and len(large.train) == treino.HELD_OUT_FROM
    assert ids(small.held) == ids(large.held) and len(small.held) == 2470 - treino.HELD_OUT_FROM
    assert not set(ids(large.train)) & set(ids(small.held))
    assert len(small.held_y) == len(small.held) and "labels" not in small.held[0]
    assert sorted(small.marks["idx"]) == sorted(ids(small.train))
    with pytest.raises(ValueError, match="at most"):
        treino.load_data(real, tmp_path, n_pairs=treino.HELD_OUT_FROM + 1, held_out=True)


def test_mark_arms_are_wired_to_their_encoder_folder_and_items():
    enc = treino.ENCODERS["marcas"]
    assert enc.arms == treino.MARK_ARMS and enc.name == dados.BERT
    assert "marcas" in treino.TASKS["rte"].out_dirs and not treino.has_decoder("marks_real")
    assert {a.removeprefix("marks_") for a in treino.MARK_ARMS} == {"none", "real", "random"}


# --- token head (10/11): the direct way to learn the highlight, reference for the attention marks ------------------

def test_token_mark_loss_is_the_mean_bce_over_real_tokens_of_the_marked_pairs():
    marks = torch.tensor([[0, 1, 0], [0, 0, 0]])  # the second pair has no mark and stays out of the mean
    mask = torch.tensor([[1, 1, 0], [1, 1, 1]])  # the first pair's last position is padding
    ln2 = torch.log(torch.tensor(2.0))
    assert torch.isclose(token_mark_loss(torch.zeros(2, 3), marks, mask), ln2)  # logit 0: ln 2 per token
    padded = torch.tensor([[0.0, 0.0, 100.0], [5.0, 5.0, 5.0]])  # the padding's logit must not count
    assert torch.isclose(token_mark_loss(padded, marks, mask), ln2)
    right = torch.tensor([[-20.0, 20.0, 0.0], [0.0, 0.0, 0.0]])
    assert token_mark_loss(right, marks, mask) < 1e-6
    assert token_mark_loss(torch.zeros(2, 3), torch.zeros(2, 3, dtype=torch.long), mask) is None


def test_token_head_trains_with_the_marks_and_stays_out_of_the_classifier(tok):
    torch.manual_seed(0)
    pairs = pd.concat([pairs_frame(), pairs_frame().assign(idx=[9, 10])], ignore_index=True)
    table = marcas.mark_table(pairs, tok, NO_LABEL_EXPR)
    batch = dados.collate(marcas.with_marks(dados.encode(pairs, tok), table, "real"))
    model = RationaleBert.with_token_head(TINY).eval()
    in_groups = {id(p) for group in treino.param_groups(model) for p in group["params"]}
    assert all(id(p) in in_groups for p in model.token_head.parameters())
    _, full = model(batch)
    assert model(dados.collate(dados.encode(pairs, tok)))[1] is None  # no marks in the batch, no auxiliary loss
    _, summed = treino.accumulated_backward(model, batch, treino.marked_loss, micro=1)  # I16
    assert summed == pytest.approx(full.item(), rel=1e-4)
    assert all(p.grad is not None and p.grad.abs().sum() > 0 for p in model.token_head.parameters())
    assert not any(k.startswith("token_head") for k in classifier_only(model).state_dict())
    assert treino.uses_marks(model) and treino.uses_marks(RationaleBert.with_mark_attention(TINY))


def test_mark_layers_choose_which_layers_the_loss_reads_and_several_layers_add_up(tok):
    pairs = pairs_frame()
    table = marcas.mark_table(pairs, tok, NO_LABEL_EXPR)
    batch = dados.collate(marcas.with_marks(dados.encode(pairs, tok), table, "real"))
    torch.manual_seed(0)
    model = RationaleBert.with_mark_attention(TINY).eval()
    attentions = run_encoder(model.bert, batch, output_attentions=True).attentions
    per_layer = [mark_loss(a, batch["marks"]) for a in attentions]
    assert not torch.isclose(per_layer[0], per_layer[1])  # the two layers differ, so the test can tell them apart
    assert torch.equal(model(batch)[1], per_layer[-1])  # default: the last layer, as before
    for layers, expected in (((0,), per_layer[0]), ((1,), per_layer[1]), ((0, 1), per_layer[0] + per_layer[1])):
        model.mark_layers = layers
        assert torch.isclose(model(batch)[1], expected)
    torch.manual_seed(0)
    assert RationaleBert.with_mark_attention(TINY, layers=(0,)).mark_layers == (0,)
