"""Invariants I1-I15 of the RTE training (docs/2026-11-09-codigo-treino-rte.md), on tiny random models: CPU, no network."""
from dataclasses import fields

import pandas as pd
import pytest
import torch
from transformers import BertConfig, BertModel, T5Config, T5ForConditionalGeneration

from radibert import rte_dados as dados
from radibert import rte_gradientes as grads
from radibert import rte_treino as treino
from radibert.rte_modelo import RationaleBert, classifier_only
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


def test_i10_same_seed_same_weights():
    plan = treino.make_plan(12, "prop", batch_size=4, epochs=2)
    runs = []
    for _ in range(2):
        model = tiny_model()
        treino.train(model, plan, fake_items(), seed=3, device=torch.device("cpu"), batch_size=4)
        runs.append(weights(model))
    assert same(runs[0], runs[1], "")


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
