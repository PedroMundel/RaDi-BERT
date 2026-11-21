"""Invariants I1-I15 of the RTE training (docs/2026-11-09-codigo-treino-rte.md), on tiny random models: CPU, no network."""
from dataclasses import fields, replace

import pandas as pd
import pytest
import torch
from transformers import BertConfig, BertModel, T5Config, T5EncoderModel, T5ForConditionalGeneration

from radibert import esnli_dados as esnli
from radibert import rte_dados as dados
from radibert import rte_gradientes as grads
from radibert import rte_treino as treino
from radibert.rte_modelo import RationaleBert, classifier_only, cls_loss
from radibert.rte_racionalizacoes import TRAIN, rte_examples

needs_rte = pytest.mark.skipif(not TRAIN.exists(), reason="dados/rte não baixado (ver dados/README.md)")


def tiny_model(with_decoder: bool = True, hidden: int = 32, d_model: int = 32) -> RationaleBert:
    torch.manual_seed(0)
    bert = BertModel(BertConfig(vocab_size=50, hidden_size=hidden, num_hidden_layers=1, num_attention_heads=2,
                                intermediate_size=37, max_position_embeddings=64), add_pooling_layer=False)
    t5 = T5ForConditionalGeneration(T5Config(vocab_size=40, d_model=d_model, d_kv=8, d_ff=37, num_layers=1,
                                             num_decoder_layers=1, num_heads=2, decoder_start_token_id=0,
                                             pad_token_id=0, eos_token_id=1)) if with_decoder else None
    return RationaleBert(bert, t5)


def fake_items(n: int = 12) -> list[dict]:
    g = torch.Generator().manual_seed(1)
    items = []
    for i in range(n):
        n_in, n_out = int(torch.randint(5, 12, (1,), generator=g)), int(torch.randint(3, 8, (1,), generator=g))
        items.append({"idx": i, "y": i % 2, "input_ids": torch.randint(2, 50, (n_in,), generator=g).tolist(),
                      "token_type_ids": [0] * n_in,
                      "labels": torch.randint(2, 40, (n_out - 1,), generator=g).tolist() + [1]})
    return items


def fake_probe(items: list[dict]) -> grads.Probe:
    """Every target position its own unit, groups cycling S, F, C, N."""
    batch = dados.collate(items)
    groups = torch.full_like(batch["labels"], -1)
    units = []
    for i, item in enumerate(items):
        n = len(item["labels"])
        groups[i, :n] = torch.arange(n) % len(grads.Group)
        units.append([grads.Unit(f"w{p}", grads.Group(p % len(grads.Group)), (p,)) for p in range(n)])
    return grads.Probe(batch, groups, units)


def weights(model) -> dict:
    return {k: v.detach().clone() for k, v in model.state_dict().items()}


def same(a: dict, b: dict, prefix: str) -> bool:
    return all(torch.equal(a[k], b[k]) for k in a if k.startswith(prefix))


# --- data ---------------------------------------------------------------------------------------------------------

@needs_rte
def test_i1_train_and_dev_share_no_pair():
    train, dev = dados.training_pairs(), dados.dev_pairs()  # idx is per split in GLUE, so only the text counts
    assert not set(zip(train.sentence1, train.sentence2)) & set(zip(dev.sentence1, dev.sentence2))


@needs_rte
def test_i2_examples_out_and_one_training_set():
    train = dados.training_pairs()
    assert len(train) == 2470 and not set(train.idx) & {ex["idx"] for ex in rte_examples()}


@needs_rte
def test_i3_entailment_is_the_positive_class():
    raw = pd.read_parquet(TRAIN)
    pairs = dados.read_rte("train")
    assert (pairs.loc[raw.label == 0, "y"] == 1).all() and (pairs.loc[raw.label == 1, "y"] == 0).all()


def shuffle_pairs() -> pd.DataFrame:
    return pd.DataFrame({"idx": range(9), "y": [1, 1, 1, 0, 0, 0, 0, 1, 0],
                         "sentence1": [f"p{i}" for i in range(9)], "sentence2": [f"h{i}" for i in range(9)],
                         "rationale": [f"r{i}" for i in range(9)]})


def test_shuffled_control_gives_every_pair_another_rationale_of_its_label():
    pairs = shuffle_pairs()
    shuffled = dados.shuffle_within_label(pairs, seed=0)
    assert (shuffled["rationale"] != pairs["rationale"]).all()  # nobody keeps its own
    for y in (0, 1):
        assert sorted(shuffled.loc[shuffled.y == y, "rationale"]) == sorted(pairs.loc[pairs.y == y, "rationale"])
    assert shuffled.drop(columns="rationale").equals(pairs.drop(columns="rationale"))


def test_shuffled_control_is_fixed_by_its_seed():
    pairs = shuffle_pairs()
    assert dados.shuffle_within_label(pairs, 0).equals(dados.shuffle_within_label(pairs, 0))
    assert not dados.shuffle_within_label(pairs, 0).equals(dados.shuffle_within_label(pairs, 1))


def test_shuffled_arm_trains_on_shuffled_items_and_others_on_the_original():
    data = treino.Data(train=["orig"], dev=[], dev_y=None, probes="probes", train_shuffled=["shuf"],
                       probes_shuffled="probes_shuf")
    assert treino.arm_inputs(data, "bert_decoder_shuffled") == (["shuf"], "probes_shuf")
    assert treino.arm_inputs(data, "bert_decoder") == treino.arm_inputs(data, "bert") == (["orig"], "probes")


def test_collate_pads_inputs_with_zero_and_targets_with_ignored():
    batch = dados.collate(fake_items(3))
    assert batch["input_ids"].shape == batch["attention_mask"].shape
    assert ((batch["attention_mask"] == 0) == (batch["input_ids"] == 0)).all()
    assert (batch["labels"] == dados.IGNORED).any() and not (batch["labels"] == 0).any()


# --- model --------------------------------------------------------------------------------------------------------

def test_i4_baseline_has_no_decoder_and_matching_sizes_have_no_bridge():
    assert tiny_model(with_decoder=False).t5 is None
    assert tiny_model(hidden=32, d_model=32).bridge is None
    assert tiny_model(hidden=16, d_model=32).bridge is not None


def test_decoder_group_trains_the_shared_embedding_but_not_the_t5_encoder():
    model = tiny_model()
    in_groups = {id(p) for group in treino.param_groups(model) for p in group["params"]}
    assert id(model.t5.shared.weight) in in_groups and model.t5.shared.weight.requires_grad
    assert not any(id(p) in in_groups for p in model.t5.encoder.block.parameters())


def test_i7_aux_loss_alone_reaches_bert():
    model = tiny_model()
    _, l_aux = model(dados.collate(fake_items(4)))
    l_aux.backward()
    assert model.bert.encoder.layer[0].attention.self.query.weight.grad.abs().sum() > 0


def test_i8_evaluation_object_has_no_decoder_and_same_logits():
    model = tiny_model(hidden=16, d_model=32).eval()
    clf = classifier_only(model).eval()
    batch = dados.collate(fake_items(4))
    assert not any(k.startswith(("t5.", "bridge.")) for k in clf.state_dict())
    assert torch.allclose(clf(batch), model.encode(batch)[1])


# --- training -----------------------------------------------------------------------------------------------------

def test_i11_step_counts():
    assert treino.make_plan(2470, "500") == treino.Plan(per_epoch=78, total=624, phase_a=39, phase_b=187,
                                                        warmup_steps=500)
    assert treino.make_plan(2470, "prop").warmup_steps == 62


def test_plan_fields_do_not_overwrite_the_run_keys_in_the_results_row():
    # the smoke test of 09/11 wrote warmup=62 over warmup="prop", and --grade could not skip finished runs
    assert not {f.name for f in fields(treino.Plan)} & {"arm", "warmup", "seed"}


def test_linear_schedule_rises_then_falls_to_zero():
    f = treino.linear_schedule(62, 624)
    assert (f(0), f(31), f(62), f(624)) == (0.0, 0.5, 1.0, 0.0)


def test_e1_bert_warms_up_over_phase_b_and_the_rest_over_table_4():
    plan = treino.make_plan(2470, "prop")
    enc, head, dec = treino.lr_factors(tiny_model(), plan)
    assert enc(93) == pytest.approx(93 / 187) and head(31) == dec(31) == 0.5
    assert len(treino.lr_factors(tiny_model(with_decoder=False), plan)) == 2


def test_i5_phase_a_leaves_bert_untouched_and_moves_the_decoder():
    model = tiny_model()
    before = weights(model)
    opt = torch.optim.AdamW(treino.param_groups(model), lr=1e-2)
    treino.run_phase_a(model, opt, fake_items(), seed=0, batch_size=4, device=torch.device("cpu"))
    after = weights(model)
    assert same(before, after, "bert.") and same(before, after, "head.") and not same(before, after, "t5.decoder.")


def test_i6_phase_b_loss_gives_the_head_no_gradient():
    model = tiny_model()
    plan = treino.make_plan(12, "prop", batch_size=4, epochs=4)
    logit, l_aux = model(dados.collate(fake_items(4)))
    l_cls = torch.nn.functional.binary_cross_entropy_with_logits(logit, torch.ones_like(logit))
    treino.training_loss(plan.phase_b, plan, l_cls, l_aux).backward()
    assert all(p.grad is None for p in model.head.parameters())


@pytest.mark.parametrize("phase_step", [1, 99])  # phase B (L_aux only) and phase C (L_cls + 0.1 L_aux)
def test_i16_micro_batches_give_the_full_batch_gradient(phase_step):
    # 09/11: batch 32 spilled the 5060's VRAM into shared memory; two halves of 16 must not change the math
    plan = treino.make_plan(40, "prop", batch_size=8, epochs=10)  # phase_b = 30
    batch = dados.collate(fake_items(7))
    grads_by = []
    for micro in (7, 3):
        model = tiny_model().eval()  # no dropout, so both passes see the same function
        treino.accumulated_backward(model, batch, lambda c, a: treino.training_loss(phase_step, plan, c, a), micro)
        grads_by.append([p.grad.clone() for p in model.bert.parameters()])
    assert all(torch.allclose(a, b, atol=1e-6) for a, b in zip(*grads_by))


def test_t5_encoder_blocks_stay_on_cpu_after_placing():
    model = tiny_model()
    treino.place(model, torch.device("cpu"))
    assert next(model.t5.encoder.block.parameters()).device.type == "cpu"
    assert model.t5.shared.weight.device.type == "cpu"


def test_i10_same_seed_same_weights():
    plan = treino.make_plan(12, "prop", batch_size=4, epochs=2)
    runs = []
    for _ in range(2):
        model = tiny_model()
        treino.train(model, plan, fake_items(), seed=3, device=torch.device("cpu"), batch_size=4)
        runs.append(weights(model))
    assert same(runs[0], runs[1], "")


def without_dropout(model: RationaleBert) -> RationaleBert:
    for module in model.modules():
        if isinstance(module, torch.nn.Dropout):
            module.p = 0.0
    return model


@pytest.mark.parametrize("aux_weight", [0.0, 0.1])
def test_i17_decoder_arm_with_zero_aux_weight_and_no_phase_b_is_the_plain_bert(monkeypatch, aux_weight):
    """Equivalence (10/11): carrying the decoder must have no side effect on the classifier. With the auxiliary
    weight at 0, no phase B and one schedule for every group, the decoder arm has to end on the plain BERT's weights.
    Dropout is off because the decoder's forward would otherwise shift the random stream of BERT's masks. With the
    paper's weight (0.1) the weights must differ, or this test would compare nothing."""
    monkeypatch.setattr(treino, "AUX_WEIGHT", aux_weight)
    monkeypatch.setattr(treino, "lr_factors", lambda model, plan: [
        treino.linear_schedule(plan.warmup_steps, plan.total)] * len(treino.param_groups(model)))
    plan = replace(treino.make_plan(12, "prop", batch_size=4, epochs=3), phase_b=0)
    with_decoder = without_dropout(tiny_model())
    plain = without_dropout(tiny_model(with_decoder=False))
    plain.bert.load_state_dict(with_decoder.bert.state_dict())
    plain.head.load_state_dict(with_decoder.head.state_dict())
    start = weights(plain)
    for model in (with_decoder, plain):
        treino.train(model, plan, fake_items(), seed=3, device=torch.device("cpu"), batch_size=4)
    a, b = weights(with_decoder), weights(plain)
    assert not same(start, b, "bert.")  # the training did move the classifier
    assert all(torch.allclose(a[k], b[k], atol=1e-7) for k in b) == (aux_weight == 0.0)


def calendar_model() -> RationaleBert:
    model = tiny_model(with_decoder=False)
    model.decoder_calendar = True
    return model


def test_calendar_control_has_the_decoder_arm_schedule_and_no_step_in_phase_b():
    plan = treino.make_plan(12, "prop", batch_size=4, epochs=4)  # 12 steps, phase B = 3
    bert_factor, head_factor = treino.lr_factors(calendar_model(), plan)
    decoder_bert_factor = treino.lr_factors(tiny_model(), plan)[0]
    assert [bert_factor(s) for s in range(plan.total)] == [decoder_bert_factor(s) for s in range(plan.total)]
    assert head_factor(plan.warmup_steps) == 1.0
    # phase B covering the whole run: the classifier never takes a step
    frozen = calendar_model()
    start = weights(frozen)
    treino.train(frozen, replace(plan, phase_b=plan.total), fake_items(), seed=3, device=torch.device("cpu"),
                 batch_size=4)
    assert same(start, weights(frozen), "")
    trained = calendar_model()
    treino.train(trained, plan, fake_items(), seed=3, device=torch.device("cpu"), batch_size=4)
    assert not same(start, weights(trained), "bert.") and not same(start, weights(trained), "head.")
    assert treino.ENCODERS["calendario"].arms == (treino.CALENDAR_ARM,) and not treino.has_decoder(treino.CALENDAR_ARM)


def test_i14_measuring_does_not_change_training():
    plan = treino.make_plan(12, "prop", batch_size=4, epochs=2)
    probe = fake_probe(fake_items(4))
    runs = []
    for probes in (None, treino.Probes(probe, probe)):
        model = tiny_model()
        log = treino.train(model, plan, fake_items(), seed=3, device=torch.device("cpu"), batch_size=4,
                           probes=probes)
        runs.append(weights(model))
    assert same(runs[0], runs[1], "") and log.group_rows and log.word_rows


def test_metrics_treat_entailment_as_the_positive_class():
    # y = 1 is entailment. One not_entailment pair scored 0.75: a false positive at both thresholds.
    m = treino.metrics(torch.tensor([1, 1, 0, 0]).numpy(), torch.tensor([0.9, 0.8, 0.75, 0.1]).numpy())
    assert (m["precision_at_0_7"], m["recall_at_0_7"]) == (pytest.approx(2 / 3), 1.0)
    assert (m["f1_entailment"], m["f1_not_entailment"]) == (pytest.approx(0.8), pytest.approx(2 / 3))


def test_different_seeds_give_different_weights():
    plan = treino.make_plan(12, "prop", batch_size=4, epochs=2)
    runs = []
    for seed in (3, 4):
        model = tiny_model()
        treino.train(model, plan, fake_items(), seed=seed, device=torch.device("cpu"), batch_size=4)
        runs.append(weights(model))
    assert not same(runs[0], runs[1], "")


def test_i9_refuses_to_run_when_text_would_be_cut():
    with pytest.raises(ValueError, match="would cut"):
        treino.refuse_cut_text({"inputs_cut": 1, "targets_cut": 0})
    treino.refuse_cut_text({"inputs_cut": 0, "targets_cut": 0})


def test_overlong_counts_compares_with_the_limits():
    class Tok:
        bert = staticmethod(lambda s1, s2: {"input_ids": [[0] * 513, [0] * 512]})
        t5 = staticmethod(lambda texts: {"input_ids": [[0] * 65, [0] * 64]})

    pairs = pd.DataFrame({"sentence1": ["a", "b"], "sentence2": ["c", "d"], "rationale": ["e", "f"]})
    assert dados.overlong_counts(pairs, Tok()) == {"inputs_cut": 1, "targets_cut": 1}


def test_single_command_needs_arm_warmup_and_seed(monkeypatch):
    def must_not_load(*args, **kwargs):
        raise AssertionError("main() went on to load data and train")

    monkeypatch.setattr(treino, "load_data", must_not_load)
    monkeypatch.setattr("sys.argv", ["rte_treino", "--seed", "1"])
    with pytest.raises(SystemExit):
        treino.main()


# --- gradient measures --------------------------------------------------------------------------------------------

def test_i12_group_parts_add_up_to_l_aux_and_to_its_gradient():
    model = tiny_model().eval()
    probe = fake_probe(fake_items(4))
    h, _ = model.encode(probe.batch)
    out = model.decode(h, probe.batch)
    parts = grads.split_aux_loss(out.logits, probe.batch["labels"], probe.groups, grads.probe_sizes(probe)[1])
    assert torch.allclose(sum(parts), out.loss)
    g_a = grads.bert_grad(out.loss, model)
    g_sum = [sum(layer) for layer in zip(*(grads.bert_grad(p, model) for p in parts))]
    assert all(torch.allclose(a, b, atol=1e-6) for a, b in zip(g_a, g_sum))


def test_measure_groups_in_chunks_equals_the_whole_probe():
    # the 09/11 audit: the whole 64-pair graph plus 6 BERT gradients would not fit the 5060
    model, probe = tiny_model(), fake_probe(fake_items(5))
    whole, chunked = (grads.measure_groups(model, probe, step=1, chunk=c) for c in (5, 2))
    assert all(chunked[k] == pytest.approx(v, rel=1e-4, abs=1e-6) for k, v in whole.items())


def test_chunk_narrower_than_the_probe_still_measures():
    # the PC run of 09/11 died here: a trimmed chunk of labels is not contiguous, and T5 calls labels.view(-1)
    items = fake_items(4)
    items[0]["labels"], items[1]["labels"] = [5, 1], [6, 7, 1]  # first chunk of 2 is narrower than the probe
    items[2]["labels"] = [5, 6, 7, 8, 9, 10, 1]
    probe = fake_probe(items)
    assert all(v.is_contiguous() for v in grads.rows_of(probe.batch, 0, 2).values())
    grads.measure_groups(tiny_model(), probe, step=1, chunk=2)


def test_head_logit_stays_fp32_under_bf16_autocast():
    model = tiny_model().eval()
    with torch.autocast("cpu", dtype=torch.bfloat16):
        _, logit = model.encode(dados.collate(fake_items(3)))
    assert logit.dtype == torch.float32


def test_training_and_measures_run_under_bf16(monkeypatch):
    monkeypatch.setattr(treino, "autocast", lambda device: torch.autocast("cpu", dtype=torch.bfloat16))
    probe = fake_probe(fake_items(4))
    log = treino.train(tiny_model(), treino.make_plan(12, "prop", batch_size=4, epochs=2), fake_items(), seed=3,
                       device=torch.device("cpu"), batch_size=4, probes=treino.Probes(probe, probe))
    values = [v for row in log.group_rows + log.word_rows for v in row.values() if isinstance(v, float)]
    assert values and all(v == v and abs(v) != float("inf") for v in values)


def test_append_csv_refuses_rows_with_other_columns(tmp_path):
    path = tmp_path / "r.csv"
    treino.append_csv(path, [{"arm": "bert_decoder", "warmup": "500", "seed": 1}])
    with pytest.raises(ValueError, match="columns"):
        treino.append_csv(path, [{"arm": "bert", "seed": 2, "warmup": "500"}])


def test_done_runs_reads_back_what_was_written(tmp_path):
    treino.append_csv(tmp_path / "resultados.csv", [{"arm": "bert_decoder", "warmup": "500", "seed": 1}])
    assert treino.done_runs(tmp_path) == {("bert_decoder", "500", 1)}


def test_memory_check_runs_one_real_step_and_one_measure():
    model, probe = tiny_model(), fake_probe(fake_items(4))
    peak = treino.memory_check(model, fake_items(), probe, torch.device("cpu"), batch_size=4)
    assert peak == 0.0  # CPU has no CUDA counter; on the PC it is the peak in GB


def test_measure_groups_shares_and_fractions_sum_to_one():
    row = grads.measure_groups(tiny_model(), fake_probe(fake_items(4)), step=1)
    names = [g.name for g in grads.Group]
    assert sum(row[f"share_{n}"] for n in names) == pytest.approx(1.0, abs=1e-4)
    assert sum(row[f"frac_tokens_{n}"] for n in names) == pytest.approx(1.0)


def test_i15_words_split_the_whole_alignment():
    model = tiny_model()
    probe = fake_probe(fake_items(4))
    rows = grads.measure_words(model, probe, step=1)
    assert model.training  # measuring puts the model back in train mode
    model.eval()
    h, logit = model.encode(probe.batch)
    g_c = grads.bert_grad(torch.nn.functional.binary_cross_entropy_with_logits(logit, probe.batch["y"]), model)
    g_a = grads.bert_grad(model.decode(h, probe.batch).loss, model)
    whole = grads.dot(g_c, g_a) / grads.dot(g_c, g_c) ** 0.5
    assert sum(r["align_t"] for r in rows) == pytest.approx(whole, rel=1e-3, abs=1e-6)
    assert len(rows) == sum(len(u) for u in probe.units)


class WhitespaceTokenizer:
    """Stands in for the T5 fast tokenizer: one token per whitespace chunk, then </s> at (0, 0)."""

    def __call__(self, text, return_offsets_mapping=True, truncation=True, max_length=64):
        spans = [(m.start(), m.end()) for m in __import__("re").finditer(r"\S+", text)]
        return {"input_ids": list(range(2, len(spans) + 2)) + [1], "offset_mapping": spans + [(0, 0)]}

    def convert_ids_to_tokens(self, ids):
        return ["</s>" if i == 1 else f"t{i}" for i in ids]


def test_i13_groups_fall_on_the_right_words():
    label_expr = grads.expression_pattern(pd.DataFrame({"expression": ["but", "never mentions"]}))
    units = grads.token_units("Titan has an atmosphere but the text never mentions its orbit.",
                              "Titan is a moon with a thick atmosphere.", "Titan is the largest moon.",
                              WhitespaceTokenizer(), label_expr)
    got = {u.word: u.group.name for u in units}
    assert got == {"titan": "C", "has": "F", "an": "F", "atmosphere": "C", "but": "S", "the": "F", "text": "F",
                   "never": "S", "mentions": "S", "its": "F", "orbit": "N", "</s>": "F"}
    assert sorted(p for u in units for p in u.positions) == list(range(12))


def test_expression_rule_keeps_only_frequent_one_sided_expressions():
    rows = ([(0, "it does not say so")] * 30 + [(1, "it does say so")] * 30 + [(1, "rare word")] * 5)
    table = grads.expression_table(pd.DataFrame(rows, columns=["y", "rationale"]))
    kept = set(table.expression)
    assert {"not", "does not", "not say"} <= kept and "say so" not in kept and "rare" not in kept


def test_expression_pattern_matches_across_apostrophes():
    assert grads.expression_pattern(pd.DataFrame({"expression": ["doesn t"]})).search("It doesn't say.")


def test_probe_rejects_offsets_that_miss_target_positions(monkeypatch):
    pairs = pd.DataFrame({"idx": [0, 1], "y": [0, 1], "sentence1": ["a b", "c d"], "sentence2": ["e", "f"],
                          "rationale": ["x y", "z w"]})

    class Tok:
        bert = staticmethod(lambda s1, s2, **kw: {"input_ids": [[2, 3]] * len(s1), "token_type_ids": [[0, 0]] * len(s1)})
        t5 = staticmethod(lambda texts, **kw: {"input_ids": [[5, 6, 1]] * len(texts)})

    monkeypatch.setattr(grads, "token_units", lambda *a: [grads.Unit("x", grads.Group.C, (0,))])
    with pytest.raises(ValueError, match="without a group"):
        grads.build_probe(pairs, Tok(), grads.expression_pattern(pd.DataFrame({"expression": ["x"]})), 2)


def test_classifier_copy_does_not_share_weights_with_the_model():
    model = tiny_model()
    clf = classifier_only(model)
    with torch.no_grad():
        next(clf.bert.parameters()).add_(1.0)
    assert not torch.equal(next(clf.bert.parameters()), next(model.bert.parameters()))


# --- T5-encoder arms (10/11) ----------------------------------------------------------------------------------------

def tiny_t5_model(with_decoder: bool = True) -> RationaleBert:
    torch.manual_seed(0)
    config = T5Config(vocab_size=50, d_model=32, d_kv=8, d_ff=37, num_layers=1, num_decoder_layers=1, num_heads=2,
                      decoder_start_token_id=0, pad_token_id=0, eos_token_id=1)
    if with_decoder:
        t5 = T5ForConditionalGeneration(config)
        return RationaleBert(t5.encoder, t5)
    return RationaleBert(T5EncoderModel(config), None)


def test_t5_decoder_arm_trains_its_own_encoder_once():
    model = tiny_t5_model()
    assert model.shares_t5_encoder and model.bridge is None
    assert all(p.requires_grad for p in model.t5.encoder.parameters())
    groups = treino.param_groups(model)
    ids = [id(p) for g in groups for p in g["params"]]
    assert len(ids) == len(set(ids))  # AdamW refuses a parameter in two groups
    assert set(ids) == {id(p) for p in model.parameters() if p.requires_grad}
    assert {id(p) for p in model.t5.encoder.parameters()} <= {id(p) for p in groups[0]["params"]}


def test_t5_encoder_stays_with_the_model_when_it_is_the_classifier(monkeypatch):
    moved = []
    for arm, label in ((tiny_t5_model(), "t5"), (tiny_model(), "bert")):
        monkeypatch.setattr(arm.t5.encoder.block, "to", lambda *a, label=label: moved.append(label))
        treino.place(arm, torch.device("cpu"))
    assert moved == ["bert"]  # only the BERT arm parks its unused T5 encoder on the CPU


def test_t5_mean_pooling_ignores_padding():
    model = tiny_t5_model(with_decoder=False).eval()
    items = fake_items(4)
    alone = model.encode(dados.collate(items[:1]))[1]
    longest = max(items, key=lambda it: len(it["input_ids"]))
    padded = model.encode(dados.collate([items[0], longest]))[1][0]
    assert len(longest["input_ids"]) > len(items[0]["input_ids"])
    assert torch.allclose(alone[0], padded, atol=1e-6)


def test_t5_evaluation_object_has_no_decoder_and_same_logits():
    model = tiny_t5_model().eval()
    clf = classifier_only(model).eval()
    batch = dados.collate(fake_items(4))
    assert not any(k.startswith(("t5.", "bridge.")) for k in clf.state_dict())
    assert torch.allclose(clf(batch), model.encode(batch)[1])


def test_t5_phase_a_leaves_the_encoder_blocks_untouched_and_moves_the_decoder():
    model = tiny_t5_model()
    before = weights(model)
    opt = torch.optim.AdamW(treino.param_groups(model), lr=1e-2)
    treino.run_phase_a(model, opt, fake_items(), seed=0, batch_size=4, device=torch.device("cpu"))
    after = weights(model)
    assert same(before, after, "bert.") and same(before, after, "t5.shared.") and same(before, after, "head.")
    assert not same(before, after, "t5.decoder.")


def test_t5_measures_leave_out_the_shared_embedding_the_decoder_also_reads():
    model = tiny_t5_model()
    measured = {id(p) for p in grads.measured_params(model)}
    assert id(model.t5.shared.weight) not in measured
    assert measured == {id(p) for p in model.bert.parameters()} - {id(model.t5.shared.weight)}
    bert_arm = tiny_model()
    assert [id(p) for p in grads.measured_params(bert_arm)] == [id(p) for p in bert_arm.bert.parameters()]
    grads.measure_groups(model, fake_probe(fake_items(4)), step=1, chunk=2)  # runs with the narrower list


def test_t5_aux_loss_reaches_the_encoder_and_both_arms_train():
    model = tiny_t5_model()
    _, l_aux = model(dados.collate(fake_items(4)))
    l_aux.backward()
    assert model.bert.block[0].layer[0].SelfAttention.q.weight.grad.abs().sum() > 0
    plan = treino.make_plan(12, "prop", batch_size=4, epochs=2)
    for arm in (tiny_t5_model(), tiny_t5_model(with_decoder=False)):
        before = weights(arm)
        treino.train(arm, plan, fake_items(), seed=1, device=torch.device("cpu"), batch_size=4)
        after = weights(arm)
        blocks = [k for k in before if k.startswith("bert.") and ".block." in k]
        assert blocks and not all(torch.equal(before[k], after[k]) for k in blocks)


def test_cls_loss_is_bce_for_one_logit_and_cross_entropy_for_many():
    logit, y = torch.tensor([0.3, -1.2]), torch.tensor([1.0, 0.0])
    assert torch.allclose(cls_loss(logit, y), torch.nn.functional.binary_cross_entropy_with_logits(logit, y))
    logits, y3 = torch.tensor([[0.1, 2.0, -1.0], [1.0, 0.0, 0.5]]), torch.tensor([1.0, 2.0])
    assert torch.allclose(cls_loss(logits, y3), torch.nn.functional.cross_entropy(logits, y3.long()))


def test_encoder_choice_picks_arms_checkpoint_and_folder():
    t5 = treino.ENCODERS["t5"]
    assert t5.arms == treino.T5_ARMS and t5.name == dados.T5_ENCODER and t5.input_tokenizer == dados.T5
    msmarco = treino.ENCODERS["msmarco"]
    assert msmarco.arms == treino.ARMS and msmarco.name == dados.MSMARCO and msmarco.input_tokenizer == dados.BERT
    assert "msmarco" in treino.TASKS["rte"].out_dirs and "msmarco" not in treino.TASKS["esnli"].out_dirs
    for size, name in (("small", dados.SMALL), ("tiny", dados.TINY)):
        plain, marked = treino.ENCODERS[size], treino.ENCODERS[f"marcas-{size}"]
        assert plain.arms == treino.ARMS and marked.arms == treino.MARK_ARMS
        assert plain.name == marked.name == name and plain.input_tokenizer == marked.input_tokenizer == dados.BERT
        assert {size, f"marcas-{size}"} <= set(treino.TASKS["rte"].out_dirs)
    folders = [d for task in treino.TASKS.values() for d in task.out_dirs.values()]
    assert len(folders) == len(set(folders)) and treino.TASKS["rte"].out_dirs["bert"] == treino.RTE_TREINO


# --- e-SNLI, three labels (10/11) -----------------------------------------------------------------------------------

def test_three_labels_give_three_logits_cross_entropy_and_train():
    torch.manual_seed(0)
    bert = BertModel(BertConfig(vocab_size=50, hidden_size=32, num_hidden_layers=1, num_attention_heads=2,
                                intermediate_size=37, max_position_embeddings=64), add_pooling_layer=False)
    t5 = T5ForConditionalGeneration(T5Config(vocab_size=40, d_model=32, d_kv=8, d_ff=37, num_layers=1,
                                             num_decoder_layers=1, num_heads=2, decoder_start_token_id=0,
                                             pad_token_id=0, eos_token_id=1))
    model = RationaleBert(bert, t5, n_labels=3)
    items = [it | {"y": i % 3} for i, it in enumerate(fake_items())]
    logits, l_aux = model(dados.collate(items[:4]))
    assert logits.shape == (4, 3) and l_aux is not None
    plan = treino.make_plan(12, "prop", batch_size=4, epochs=2)
    treino.train(model, plan, items, seed=1, device=torch.device("cpu"), batch_size=4)
    probs = treino.predict(classifier_only(model), items, torch.device("cpu"))
    assert probs.shape == (12, 3) and torch.allclose(torch.tensor(probs.sum(1)), torch.ones(12), atol=1e-5)


def test_metrics_for_three_labels_use_the_most_probable_label():
    labels = {0: "entailment", 1: "neutral", 2: "contradiction"}
    y = torch.tensor([0, 1, 2, 2]).numpy()
    p = torch.tensor([[0.8, 0.1, 0.1], [0.2, 0.7, 0.1], [0.1, 0.2, 0.7], [0.6, 0.3, 0.1]]).numpy()
    m = treino.metrics(y, p, labels)
    assert m["accuracy"] == 0.75 and m["f1_neutral"] == 1.0 and set(m) >= {"roc_auc", "f1_macro", "f1_contradiction"}


def test_expression_table_with_three_labels_keeps_one_sided_expressions():
    rows = [(0, "is an animal")] * 30 + [(1, "could be anywhere")] * 30 + [(2, "cannot both be")] * 30
    rows += [(y, "the man") for y in (0, 1, 2)] * 10
    table = grads.expression_table(pd.DataFrame(rows, columns=["y", "rationale"]), esnli.LABELS)
    assert list(table.columns) == ["expression", "n_entailment", "n_neutral", "n_contradiction"]
    kept = set(table.expression)
    assert {"animal", "anywhere", "cannot"} <= kept and "man" not in kept


def test_rte_expression_table_keeps_its_columns():
    rows = [(0, "it does not say so")] * 30
    assert list(grads.expression_table(pd.DataFrame(rows, columns=["y", "rationale"])).columns) == [
        "expression", "n_entailment", "n_not_entailment"]


@pytest.mark.skipif(not (esnli.RATIONALES.exists() and esnli.ESNLI_DEV.exists()), reason="e-SNLI ou lote 35B fora")
def test_esnli_pairs_are_few_labelled_and_disjoint_from_the_dev():
    train, dev = esnli.training_pairs(), esnli.dev_pairs()
    assert len(train) == esnli.N_TRAIN and train["idx"].is_unique and train["rationale"].notna().all()
    assert set(train["y"]) == set(dev["y"]) == set(esnli.LABELS)
    assert not set(train["pairID"]) & set(dev["pairID"])
    assert train.equals(esnli.training_pairs())  # the same sample every time


@pytest.mark.skipif(not esnli.RATIONALES.exists(), reason="lote 35B fora")
def test_esnli_other_pairs_share_nothing_with_the_training_pairs():
    train, other = esnli.training_pairs(), esnli.other_pairs()
    assert len(other) == esnli.N_TRAIN and other["idx"].is_unique
    assert not set(other["pairID"]) & set(train["pairID"]) and not set(other["idx"]) & set(train["idx"])
    assert set(other["y"]) == set(esnli.LABELS)
    assert other.equals(esnli.other_pairs())  # the same sample every time


@pytest.mark.skipif(not esnli.RATIONALES.exists(), reason="lote 35B fora")
def test_esnli_choice_split_covers_the_rest_of_the_batch_and_shares_nothing():
    choice, extra = esnli.choice_split()
    used = [set(esnli.training_pairs()["idx"]), set(esnli.other_pairs()["idx"]), set(choice["idx"]), set(extra["idx"])]
    assert len(choice) == len(extra) == esnli.N_TRAIN
    assert sum(len(u) for u in used) == len(set().union(*used)) == esnli.BATCH_PAIRS  # four disjoint quarters
    assert choice.equals(esnli.choice_split()[0])


# --- out-of-distribution test (10/11): RTE-trained model on the e-SNLI dev ---------------------------------------------

def test_esnli_labels_collapse_to_the_rte_ones():
    pairs = pd.DataFrame({"y": [0, 1, 2, 0], "sentence1": list("abcd"), "sentence2": list("efgh")})
    out = esnli.with_rte_labels(pairs)
    assert out["y"].tolist() == [1, 0, 0, 1]  # entailment -> 1; neutral and contradiction -> 0 (grads.RTE_LABELS)
    assert pairs["y"].tolist() == [0, 1, 2, 0] and out["sentence1"].tolist() == list("abcd")


def test_outside_scores_are_the_roc_auc_and_accuracy_under_their_own_columns():
    y = pd.Series([1, 0, 0, 1]).to_numpy()
    p = pd.Series([0.9, 0.2, 0.6, 0.7]).to_numpy()
    assert treino.outside_scores(y, p) == {"fora_roc_auc": 1.0, "fora_accuracy": 0.75, "n_fora": 4}


# --- out-of-distribution test (18/11): e-SNLI-trained model on every RTE pair -----------------------------------------

def test_outside_scores_read_a_three_label_model_on_rte_labels():
    y = pd.Series([1, 0, 0, 1]).to_numpy()  # RTE: 1 entailment
    # third row: entailment is the most probable label with 0.45, so the guess is entailment (wrong), though < 0.5
    p = torch.tensor([[0.6, 0.3, 0.1], [0.2, 0.5, 0.3], [0.45, 0.3, 0.25], [0.5, 0.25, 0.25]]).numpy()
    assert treino.outside_scores(y, p) == {"fora_roc_auc": 1.0, "fora_accuracy": 0.75, "n_fora": 4}


def test_peso_aux_sets_the_phase_c_weight_and_leaves_phase_b_alone(monkeypatch):
    monkeypatch.setattr(treino, "AUX_WEIGHT", treino.AUX_WEIGHT)  # restored after the test: main() rebinds it
    monkeypatch.setattr(treino, "code_version", lambda: "test")
    monkeypatch.setattr(treino, "smoke_test", lambda *a: None)
    monkeypatch.setattr("sys.argv", ["rte_treino", "--fumaca", "--tarefa", "esnli16k", "--peso-aux", "0.5"])
    treino.main()
    plan = treino.make_plan(16000, "500")
    l_cls, l_aux = torch.tensor(2.0), torch.tensor(4.0)
    assert treino.training_loss(plan.phase_b + 1, plan, l_cls, l_aux).item() == 2.0 + 0.5 * 4.0  # phase C
    assert treino.training_loss(plan.phase_b, plan, l_cls, l_aux).item() == 4.0  # phase B: only the decoder loss
    assert treino.training_loss(plan.phase_b + 1, plan, l_cls, None).item() == 2.0  # no decoder: the weight is unused


def test_saved_classifier_weights_give_back_the_same_predictions(tmp_path):
    trained = classifier_only(tiny_model(with_decoder=True))
    with torch.no_grad():
        trained.head[1].weight.add_(0.5)  # anything that tells it apart from a freshly built model
    cfg = treino.RunConfig("bert_decoder", "500", 3, save_weights=True)
    path = treino.save_classifier(trained, tmp_path, cfg)
    assert path == tmp_path / "pesos" / "bert_decoder-500-semente-3.pt" and path.exists()
    fresh = classifier_only(tiny_model(with_decoder=False))
    items = fake_items()
    device = torch.device("cpu")
    assert not (treino.predict(fresh, items, device) == treino.predict(trained, items, device)).all()
    fresh.load_state_dict(torch.load(path, map_location="cpu"))
    assert (treino.predict(fresh, items, device) == treino.predict(trained, items, device)).all()
    assert not any(name.startswith("t5") for name in torch.load(path, map_location="cpu"))  # no decoder in the file


@needs_rte
def test_every_rte_pair_is_the_outside_set_of_the_esnli_tasks_and_carries_no_rationale():
    pairs = dados.all_pairs()
    assert len(pairs) == len(dados.training_pairs()) + len(dados.dev_pairs()) == 2747
    assert "rationale" not in pairs.columns and set(pairs["y"]) == {0, 1}
    assert treino.TASKS["esnli16k"].outside_pairs is dados.all_pairs
    assert treino.TASKS["rte"].outside_pairs is not None and treino.TASKS["esnli"].outside_pairs is dados.all_pairs
