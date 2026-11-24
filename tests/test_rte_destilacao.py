"""Attention distillation (plan, section 11): the loss, the layer maps, and that the teacher stays frozen."""
import math

import pandas as pd
import pytest
import torch
from transformers import AutoTokenizer

from radibert import esnli_dados as esnli
from radibert import rte_dados as dados
from radibert import rte_destilacao as destilacao
from radibert import rte_treino as treino
from radibert.rte_modelo import RationaleBert, classifier_only

TINY = "google/bert_uncased_L-2_H-128_A-2"
MINI = "google/bert_uncased_L-4_H-256_A-4"  # 4 layers and 4 heads: a teacher with other sizes than the student


@pytest.fixture(scope="module")
def items():
    tok = dados.Tokenizers(AutoTokenizer.from_pretrained(TINY), AutoTokenizer.from_pretrained(dados.T5))
    pairs = pd.DataFrame({"idx": range(5), "y": [0, 1, 2, 1, 0],
                          "sentence1": ["A man plays a guitar on a stage.", "Two dogs run in a park.", "A girl sleeps.",
                                        "The company opened a factory in Recife in 2019.", "Kids eat."],
                          "sentence2": ["A man plays music.", "The dogs are outside.", "A girl is running a marathon.",
                                        "The company opened a factory.", "Children are eating lunch at school."],
                          "rationale": ["Playing a guitar is playing music."] * 5})
    return dados.encode(pairs, tok)


@pytest.fixture(scope="module")
def batch(items):
    return dados.collate(items)


def student_with(teacher_name: str, layer_map_of) -> RationaleBert:
    torch.manual_seed(0)
    teacher = classifier_only(RationaleBert.with_mark_attention(teacher_name, n_labels=3))
    student = RationaleBert.with_mark_attention(TINY, n_labels=3).eval()
    n_teacher = len(teacher.bert.encoder.layer)
    student.distill = destilacao.Distillation(teacher, layer_map_of(2, n_teacher) if layer_map_of else None,
                                              answers=layer_map_of is None)
    return student


def student_imitating(**maps_of) -> RationaleBert:
    """TINY (2 layers, 128, 2 heads) imitating MINI (4 layers, 256, 4 heads): the answers plus the losses named in
    `maps_of` (layer_map, hidden_map, value_map -> last_map or uniform_map)."""
    torch.manual_seed(0)
    teacher = classifier_only(RationaleBert.with_mark_attention(MINI, n_labels=3))
    student = RationaleBert.with_mark_attention(TINY, n_labels=3).with_projections(256).eval()
    maps = {name: map_of(2, 4) for name, map_of in maps_of.items()}
    student.distill = destilacao.Distillation(teacher, answers=True, **maps)
    return student


def test_layer_maps_are_last_to_last_and_evenly_spaced():
    assert destilacao.last_map(4, 12) == {3: 11}
    assert destilacao.uniform_map(4, 12) == {0: 2, 1: 5, 2: 8, 3: 11}  # teacher layers 3, 6, 9, 12
    assert destilacao.uniform_map(2, 4) == {0: 1, 1: 3}
    with pytest.raises(ValueError):
        destilacao.uniform_map(4, 6)


def test_attention_kl_is_zero_for_equal_attention_and_matches_a_hand_computed_case():
    teacher = torch.tensor([[[[0.5, 0.5, 0.0], [1.0, 0.0, 0.0], [0.2, 0.3, 0.5]]]])  # (1 pair, 1 head, 3, 3)
    student = torch.tensor([[[[0.25, 0.75, 0.0], [1.0, 0.0, 0.0], [0.5, 0.25, 0.25]]]])
    mask = torch.tensor([[1, 1, 0]])  # the third row is padding and stays out
    assert destilacao.attention_kl(teacher, teacher, mask).item() == pytest.approx(0, abs=1e-7)
    row0 = 0.5 * math.log(0.5 / 0.25) + 0.5 * math.log(0.5 / 0.75)
    assert destilacao.attention_kl(student, teacher, mask).item() == pytest.approx(row0 / 2, rel=1e-5)


def test_attention_kl_averages_the_heads_so_head_counts_may_differ():
    one_head = torch.tensor([[[[0.4, 0.6], [0.5, 0.5]]]])
    two_heads = torch.tensor([[[[0.2, 0.8], [0.9, 0.1]], [[0.6, 0.4], [0.1, 0.9]]]])  # their mean is one_head
    mask = torch.ones(1, 2, dtype=torch.long)
    assert destilacao.attention_kl(two_heads, one_head, mask).item() == pytest.approx(0, abs=1e-7)


def test_output_kl_is_zero_for_equal_logits_and_positive_otherwise():
    logits = torch.tensor([[2.0, 0.0, -1.0], [0.0, 0.0, 0.0]])
    assert destilacao.output_kl(logits, logits).item() == pytest.approx(0, abs=1e-7)
    assert destilacao.output_kl(logits, logits.flip(-1)).item() > 0


@pytest.mark.parametrize("layer_map_of", [destilacao.last_map, destilacao.uniform_map, None])
def test_one_step_on_the_distillation_loss_brings_the_student_closer_and_never_touches_the_teacher(batch,
                                                                                                    layer_map_of):
    student = student_with(MINI, layer_map_of)
    teacher = student.distill.teacher
    before_teacher = [p.clone() for p in teacher.parameters()]
    assert not {id(p) for p in teacher.parameters()} & {id(p) for p in student.parameters()}
    _, before = student(batch)
    assert before > 0
    before.backward()
    assert all(p.grad is None for p in teacher.parameters())
    with torch.no_grad():
        for p in student.parameters():
            if p.grad is not None:
                p -= 0.01 * p.grad
    assert student(batch)[1] < before
    assert all(torch.equal(a, b) for a, b in zip(before_teacher, teacher.parameters()))


def test_micro_batches_add_up_to_the_full_batch_distillation_loss(batch):
    student = student_with(MINI, destilacao.uniform_map)
    full = student(batch)[1].item()
    _, summed = treino.accumulated_backward(student, batch, treino.marked_loss, micro=2)
    assert summed == pytest.approx(full, rel=1e-4)


def test_the_evaluation_copy_has_no_teacher(batch):
    student = student_with(MINI, destilacao.last_map)
    classifier = classifier_only(student)
    assert not hasattr(classifier, "distill")
    assert sum(p.numel() for p in classifier.parameters()) == sum(p.numel() for p in student.parameters())


def test_temperature_spreads_the_targets_and_at_one_changes_nothing():
    student, teacher = torch.tensor([[1.0, 0.0, -1.0]]), torch.tensor([[4.0, 0.0, -2.0]])
    assert destilacao.output_kl(student, teacher, 1.0).item() == pytest.approx(
        destilacao.output_kl(student, teacher).item())
    spread = torch.softmax(teacher / 4, -1)
    by_hand = (spread * (torch.log(spread) - torch.log_softmax(student / 4, -1))).sum() * 16
    assert destilacao.output_kl(student, teacher, 4.0).item() == pytest.approx(by_hand.item(), rel=1e-5)
    assert destilacao.output_kl(teacher, teacher, 4.0).item() == pytest.approx(0, abs=1e-6)


def test_smoothed_targets_put_the_rest_evenly_on_the_other_labels():
    targets = destilacao.smoothed_targets([2, 0], n_labels=3, smoothing=0.1)
    assert torch.allclose(targets, torch.tensor([[0.05, 0.05, 0.9], [0.9, 0.05, 0.05]]))


def test_swapped_targets_stay_inside_the_label_keep_the_rows_and_move_them():
    probs = torch.arange(24, dtype=torch.float).reshape(8, 3)
    labels = [0, 0, 0, 0, 1, 1, 1, 1]
    swapped = destilacao.swapped_within_label(probs, labels, seed=0)
    assert sorted(swapped[:4].tolist()) == sorted(probs[:4].tolist())  # label 0 keeps its own rows
    assert sorted(swapped[4:].tolist()) == sorted(probs[4:].tolist())
    assert not torch.equal(swapped, probs)
    assert torch.equal(swapped, destilacao.swapped_within_label(probs, labels, seed=0))


def test_target_table_is_looked_up_by_pair_idx_and_trains_towards_the_target(batch):
    torch.manual_seed(0)
    student = RationaleBert.with_mark_attention(TINY, n_labels=3).eval()
    targets = destilacao.smoothed_targets(batch["y"].long().tolist(), 3, 0.1)
    student.distill = destilacao.TargetTable(dict(zip(batch["idx"].tolist(), targets)))
    logits, before = student(batch)
    assert before.item() == pytest.approx(destilacao.target_kl(logits, targets).item(), rel=1e-5)
    reordered = {k: v.flip(0) for k, v in batch.items()}
    assert student(reordered)[1].item() == pytest.approx(before.item(), rel=1e-4)  # by idx, not by position
    before.backward()
    with torch.no_grad():
        for p in student.parameters():
            if p.grad is not None:
                p -= 0.01 * p.grad
    assert student(batch)[1] < before


def test_hidden_mse_is_zero_through_an_identity_projection_and_leaves_padding_out():
    teacher = torch.tensor([[[1.0, 2.0], [3.0, 4.0], [9.0, 9.0]]])  # (1 pair, 3 tokens, 2 dimensions)
    student = torch.tensor([[[1.0, 0.0], [3.0, 4.0], [0.0, 0.0]]])
    mask = torch.tensor([[1, 1, 0]])  # the third token is padding: its large error stays out
    identity = torch.nn.Identity()
    assert destilacao.hidden_mse(teacher, teacher, identity, mask).item() == 0
    assert destilacao.hidden_mse(student, teacher, identity, mask).item() == pytest.approx((4 / 2 + 0) / 2)


def test_value_relation_is_one_distribution_per_row_and_head_over_the_real_tokens(batch):
    torch.manual_seed(0)
    student = RationaleBert.with_mark_attention(TINY, n_labels=3).eval()
    layer, mask = student.bert.encoder.layer[1], batch["attention_mask"]
    hidden = student.bert(input_ids=batch["input_ids"], attention_mask=mask, output_hidden_states=True).hidden_states
    relation = destilacao.value_relation(layer, hidden[1], mask)
    assert relation.shape == (5, 2, mask.shape[1], mask.shape[1])  # pairs, heads, tokens, tokens
    assert torch.allclose(relation.sum(-1), torch.ones(5, 2, mask.shape[1]), atol=1e-5)
    assert relation[mask[:, None, None, :].expand_as(relation) == 0].abs().max().item() == 0
    assert destilacao.attention_kl(relation, relation, mask).item() == pytest.approx(0, abs=1e-6)


def test_each_map_turns_its_own_losses_on(batch):
    names = {"layer_map": {"attention"}, "hidden_map": {"embeddings", "hidden"}, "value_map": {"values"}}
    for name, expected in names.items():
        _, terms = student_imitating(**{name: destilacao.uniform_map}).distill_terms(batch)
        assert set(terms) == {"answers"} | expected
        assert all(term.item() > 0 for term in terms.values())


@pytest.mark.parametrize("maps_of", [{"hidden_map": destilacao.uniform_map},
                                     {"value_map": destilacao.last_map},
                                     {"layer_map": destilacao.uniform_map, "hidden_map": destilacao.uniform_map},
                                     {"layer_map": destilacao.last_map, "value_map": destilacao.last_map}])
def test_one_step_on_the_joined_losses_brings_the_student_closer_and_never_touches_the_teacher(batch, maps_of):
    student = student_imitating(**maps_of)
    teacher = student.distill.teacher
    before_teacher = [p.clone() for p in teacher.parameters()]
    _, before = student(batch)
    before.backward()
    assert all(p.grad is None for p in teacher.parameters())
    with torch.no_grad():
        for p in student.parameters():
            if p.grad is not None:
                p -= 0.01 * p.grad
    assert student(batch)[1] < before
    assert all(torch.equal(a, b) for a, b in zip(before_teacher, teacher.parameters()))


def test_micro_batches_add_up_to_the_full_batch_loss_with_every_term_on(batch):
    student = student_imitating(layer_map=destilacao.uniform_map, hidden_map=destilacao.uniform_map,
                                value_map=destilacao.last_map)
    full = student(batch)[1].item()
    _, summed = treino.accumulated_backward(student, batch, treino.marked_loss, micro=2)
    assert summed == pytest.approx(full, rel=1e-4)


def test_the_projections_train_with_the_student_and_stay_out_of_the_evaluation_copy(batch):
    student = student_imitating(hidden_map=destilacao.uniform_map)
    trained = {id(p) for group in treino.param_groups(student) for p in group["params"]}
    assert {id(p) for p in student.projections.parameters()} <= trained
    extra = sum(p.numel() for p in student.projections.parameters())
    classifier = classifier_only(student)
    assert sum(p.numel() for p in classifier.parameters()) == sum(p.numel() for p in student.parameters()) - extra


def test_the_internal_only_phase_moves_the_encoder_and_never_the_head(items):
    student = student_imitating(layer_map=destilacao.uniform_map, hidden_map=destilacao.uniform_map)
    student.distill.answers = False
    head_before = [p.clone() for p in student.head.parameters()]
    encoder_before = [p.clone() for p in student.bert.parameters()]
    plan = treino.make_plan(len(items), "prop", batch_size=2, epochs=1)
    treino.train(student, plan, items, 0, torch.device("cpu"), batch_size=2, loss_of=treino.internal_only)
    assert all(torch.equal(a, b) for a, b in zip(head_before, student.head.parameters()))
    assert any(not torch.equal(a, b) for a, b in zip(encoder_before, student.bert.parameters()))


def test_attention_before_dropout_is_the_models_own_attention_in_eval_and_stays_whole_in_training(batch):
    torch.manual_seed(0)
    student = RationaleBert.with_mark_attention(TINY, n_labels=3)
    mask = batch["attention_mask"]
    for mode, same in (("eval", True), ("train", False)):
        getattr(student, mode)()
        out = student.bert(input_ids=batch["input_ids"], attention_mask=mask,
                           token_type_ids=batch["token_type_ids"], output_attentions=True, output_hidden_states=True)
        for k, layer in enumerate(student.bert.encoder.layer):
            rebuilt = destilacao.attention_before_dropout(layer, out.hidden_states[k], mask)
            assert torch.allclose(rebuilt.sum(-1), torch.ones_like(rebuilt.sum(-1)), atol=1e-5)
            assert torch.allclose(rebuilt, out.attentions[k], atol=1e-5) == same


def test_before_dropout_only_changes_the_attention_loss_in_training_mode(batch):
    after = student_imitating(layer_map=destilacao.uniform_map)
    before = student_imitating(layer_map=destilacao.uniform_map)
    before.distill.before_dropout = True
    assert before.distill_terms(batch)[1]["attention"].item() == pytest.approx(
        after.distill_terms(batch)[1]["attention"].item(), rel=1e-4)
    torch.manual_seed(1)
    noisy = after.train().distill_terms(batch)[1]["attention"].item()
    torch.manual_seed(1)
    clean = before.train().distill_terms(batch)[1]["attention"].item()
    assert noisy > clean


GROUP_ROWS = torch.tensor([[1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 1, 1], [1, 0, 1]])  # one row per pair of `items`


def student_with_groups(with_teacher: bool = False) -> RationaleBert:
    """TINY with the group head of plan section 11.8 on 3 groups; with the teacher, its answers join the sum."""
    student = student_with(TINY, None)
    teacher = student.distill if with_teacher else None
    student.with_group_head(torch.zeros(3, 3))
    student.distill = destilacao.GroupTargets(dict(enumerate(GROUP_ROWS)), teacher)
    return student


def test_the_label_bias_starts_at_the_logit_of_each_labels_group_rate():
    rows = torch.tensor([[1, 0], [1, 0], [1, 1], [0, 0]])
    logits = destilacao.label_rate_logits(rows, [0, 0, 0, 1], n_labels=2)
    assert torch.sigmoid(logits[0]).tolist() == pytest.approx([3.5 / 4, 1.5 / 4])  # 3 of 3 and 1 of 3, half a pair added
    assert torch.sigmoid(logits[1]).tolist() == pytest.approx([0.5 / 2, 0.5 / 2])  # never there: finite, below a half
    student = RationaleBert.with_mark_attention(TINY, n_labels=2).with_group_head(logits)
    assert torch.equal(student.group_label_bias.weight, logits)
    # with the head's linear layer at zero, the head says exactly what the label alone explains
    torch.nn.init.zeros_(student.group_head.weight)
    said = torch.sigmoid(student.group_logits(torch.randn(2, 4, 128), torch.tensor([0.0, 1.0])))
    assert torch.allclose(said, torch.sigmoid(logits), atol=1e-6)


def test_the_group_loss_is_near_zero_when_the_head_says_the_target(batch):
    student = student_with_groups()
    by_label = {int(y): GROUP_ROWS[i] for i, y in enumerate(batch["y"])}
    student.distill.targets = {i: by_label[int(y)] for i, y in enumerate(batch["y"])}  # the label decides the row
    with torch.no_grad():
        student.group_head.weight.zero_()
        for label, row in by_label.items():
            student.group_label_bias.weight[label] = (row * 2 - 1) * 20.0
    terms = student.distill_terms(batch)[1]
    assert set(terms) == {"groups"}
    assert terms["groups"].item() < 1e-6


def test_the_group_loss_reaches_the_encoder_the_head_and_the_label_bias(batch):
    student = student_with_groups()
    student(batch)[1].backward()
    assert student.group_label_bias.weight.grad.abs().sum() > 0
    assert student.group_head.weight.grad.abs().sum() > 0
    assert student.bert.encoder.layer[0].attention.self.query.weight.grad.abs().sum() > 0
    assert student.head[1].weight.grad is None  # the classifier's head is not in this loss


def test_swapped_group_rows_stay_inside_the_gold_label():
    labels = [0, 1, 2, 1, 0, 2, 0]
    rows = torch.eye(7)  # every pair has a row of its own
    swapped = destilacao.swapped_within_label(rows, labels, seed=0)
    for position, row in enumerate(swapped):
        assert labels[int(row.argmax())] == labels[position]
    assert sorted(swapped.argmax(1).tolist()) == list(range(7))
    assert not torch.equal(swapped, rows)


def test_the_group_head_trains_with_the_student_and_stays_out_of_the_evaluation_copy(batch):
    student = student_with_groups(with_teacher=True)
    assert set(student.distill_terms(batch)[1]) == {"answers", "groups"}
    trained = {id(p) for group in treino.param_groups(student) for p in group["params"]}
    extra_modules = (student.group_head, student.group_label_bias)
    assert {id(p) for module in extra_modules for p in module.parameters()} <= trained
    extra = sum(p.numel() for module in extra_modules for p in module.parameters())
    classifier = classifier_only(student)
    assert sum(p.numel() for p in classifier.parameters()) == sum(p.numel() for p in student.parameters()) - extra
    full = student(batch)[1].item()
    _, summed = treino.accumulated_backward(student, batch, treino.marked_loss, micro=2)
    assert summed == pytest.approx(full, rel=1e-4)


# --- a teacher that reads the rationale (docs/2026-11-18-professor-que-le-a-justificativa.md) ---

def labelled_pairs() -> pd.DataFrame:
    return pd.DataFrame({"idx": range(6), "y": [0, 1, 2, 0, 1, 2],
                         "sentence1": ["A man plays a guitar.", "Two dogs run.", "A girl sleeps."] * 2,
                         "sentence2": ["A man plays music.", "The dogs are brown.", "A girl runs."] * 2,
                         "rationale": [f"reason {i} of label {y}" for i, y in enumerate([0, 1, 2, 0, 1, 2])]})


def test_rationale_in_input_keeps_the_pair_tokens_where_they_were():
    tok = dados.Tokenizers(AutoTokenizer.from_pretrained(TINY), AutoTokenizer.from_pretrained(dados.T5))
    pairs = labelled_pairs()
    alone = dados.encode(pairs, tok)
    joined = dados.encode(esnli.rationale_in_input(pairs), tok)
    only = dados.encode(esnli.rationale_in_input(pairs, alone=True), tok)
    for a, j, o, rationale in zip(alone, joined, only, pairs["rationale"]):
        n = len(a["input_ids"])
        assert j["input_ids"][:n] == a["input_ids"] and len(j["input_ids"]) > n
        assert j["input_ids"].count(tok.bert.sep_token_id) == 3
        assert tok.bert.decode(o["input_ids"], skip_special_tokens=True) == rationale


def test_rationale_of_other_label_never_keeps_the_own_label_and_says_whose_it_is():
    pairs = labelled_pairs()
    swapped = esnli.rationale_of_other_label(pairs, seed=0)
    assert (swapped["rationale_y"] != pairs["y"]).all()
    for rationale, source in zip(swapped["rationale"], swapped["rationale_y"]):
        assert rationale.endswith(f"label {source}")
    assert swapped.drop(columns=["rationale", "rationale_y"]).equals(pairs.drop(columns="rationale"))
    assert swapped.equals(esnli.rationale_of_other_label(pairs, seed=0))
    with pytest.raises(ValueError):
        esnli.rationale_of_other_label(pairs[pairs["y"] == 0], seed=0)


def imitating_internals(pairs: pd.DataFrame, teacher_pairs: pd.DataFrame | None):
    """TINY imitating MINI's attention and hidden states; with `teacher_pairs`, the teacher reads those instead."""
    tok = dados.Tokenizers(AutoTokenizer.from_pretrained(TINY), AutoTokenizer.from_pretrained(dados.T5))
    torch.manual_seed(0)
    teacher = classifier_only(RationaleBert.with_mark_attention(MINI, n_labels=3))
    student = RationaleBert.with_mark_attention(TINY, n_labels=3).with_projections(256).eval()
    inputs = None if teacher_pairs is None else {item["idx"]: item for item in dados.encode(teacher_pairs, tok)}
    student.distill = destilacao.Distillation(teacher, layer_map=destilacao.uniform_map(2, 4),
                                              hidden_map=destilacao.uniform_map(2, 4), teacher_inputs=inputs)
    return student, dados.collate(dados.encode(pairs, tok))


def test_a_teacher_reading_the_same_input_through_teacher_inputs_changes_no_loss():
    pairs = labelled_pairs()
    plain, batch = imitating_internals(pairs, None)
    same, _ = imitating_internals(pairs, pairs)
    with torch.no_grad():
        expected, got = plain.distill_terms(batch)[1], same.distill_terms(batch)[1]
    assert expected.keys() == got.keys() == {"attention", "embeddings", "hidden"}
    for name in expected:
        assert got[name].item() == pytest.approx(expected[name].item(), rel=1e-5)


def test_a_teacher_reading_the_rationale_is_cut_to_the_pair_and_its_attention_adds_up_to_one_again():
    pairs = labelled_pairs().assign(sentence2=["A man plays music.", "Dogs.", "A girl runs far away today."] * 2)
    student, batch = imitating_internals(pairs, esnli.rationale_in_input(pairs))
    distill, mask = student.distill, batch["attention_mask"]
    out, _ = distill.teacher_pass(batch)
    width = batch["input_ids"].shape[1]
    assert all(h.shape[1] == width for h in out.hidden_states)
    for attention in out.attentions:
        assert attention.shape[-2:] == (width, width)
        sums = attention.sum(-1)
        rows = sums[mask[:, None, :].expand_as(sums) == 1]
        assert torch.allclose(rows, torch.ones_like(rows), atol=1e-5)
        assert (attention * (1 - mask)[:, None, None, :]).abs().max() == 0  # nothing on the student's padding
    assert distill.teacher_batch(batch)["input_ids"].shape[1] > width  # the teacher did read more
    with torch.no_grad():
        terms = student.distill_terms(batch)[1]
    assert all(torch.isfinite(value) for value in terms.values())
    swapped = dict(distill.teacher_inputs)
    first, second = batch["idx"][:2].tolist()
    swapped[first], swapped[second] = swapped[second], swapped[first]
    distill.teacher_inputs = swapped
    with pytest.raises(ValueError, match="does not start with"):
        distill.teacher_pass(batch)


def test_teacher_inputs_refuses_the_losses_that_need_the_whole_input():
    teacher = classifier_only(RationaleBert.with_mark_attention(TINY, n_labels=3))
    with pytest.raises(ValueError):
        destilacao.Distillation(teacher, answers=True, teacher_inputs={})
    with pytest.raises(ValueError):
        destilacao.Distillation(teacher, value_map={1: 1}, teacher_inputs={})
