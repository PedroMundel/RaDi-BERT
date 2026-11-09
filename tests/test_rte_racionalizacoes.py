"""RTE prompts keep F's rules (no label, no premise/hypothesis words), and the batch resumes without duplicates."""
import pandas as pd
import pytest

from radibert import rte_racionalizacoes as rte

P = "Lina Joy, 42, was born Azlina Jailani to Malay parents. Joy converted to Christianity at age 26."
H = "Lina Joy's parents are from Malaysia."


def item_question(prompt: str) -> str:
    return prompt.split("Now the question to answer:", 1)[1]


def test_inner_keeps_names_and_lowers_articles():
    assert rte.inner(H) == "Lina Joy's parents are from Malaysia"
    assert rte.inner("The Pope died.") == "the Pope died"
    assert rte.inner("A man is painting.") == "a man is painting"
    assert rte.inner("In 2003, Yunus brought microcredit.") == "in 2003, Yunus brought microcredit"


@pytest.mark.parametrize("variant", ["F", "FP", "FP2", "FP3", "F3"])
@pytest.mark.parametrize("label", ["entailment", "not_entailment"])
def test_item_question_hides_the_label(variant, label):
    question = item_question(rte.prompt_for(P, H, label, variant)).lower()
    for word in ("entail", "neutral", "contradict", "premise", "hypothesis", "label"):
        assert word not in question
    assert ("not necessarily" in question) == (label == "not_entailment")
    assert "Lina Joy's parents" in item_question(rte.prompt_for(P, H, label, variant))


def test_paragraph_variant_keeps_the_whole_premise():
    assert P in rte.prompt_for(P, H, "entailment", "FP")


def test_fp2_differs_from_fp_only_in_the_ask():
    fp, fp2 = (rte.prompt_for(P, H, "not_entailment", v) for v in ("FP", "FP2"))
    assert "world knowledge behind the answer" in fp and "world knowledge behind the answer" not in fp2
    assert fp.replace(rte.piloto_qwen.ASK_ANSWER, rte.ASK_FROM_TEXT) == fp2


def test_fp3_ask_does_not_name_the_text():
    ask = rte.ASKS["FP3"].lower()
    assert "passage" not in ask and "text" not in ask


def test_gerar_resumes_without_duplicates(tmp_path, monkeypatch):
    train = pd.DataFrame({"sentence1": [P] * 5, "sentence2": [H] * 5, "label": ["entailment"] * 5, "idx": range(5)})
    monkeypatch.setattr(rte, "shuffled_train", lambda: train)
    monkeypatch.setattr(rte, "output_path", lambda variant: tmp_path / f"out-{variant}.csv")
    monkeypatch.setattr(rte.piloto_qwen, "ask_qwen", lambda prompt: {
        "qwen": "x", "finish_reason": "stop", "tokens_in": 1, "tokens_out": 1, "seconds": 0.0})
    monkeypatch.setattr(rte, "rte_examples", lambda: [{"idx": 1}])  # pair 1 is an example: never generated
    rte.cmd_gerar("F", 3)
    rte.cmd_gerar("F", 5)
    out = pd.read_csv(tmp_path / "out-F.csv")
    assert sorted(out["idx"]) == [0, 2, 3, 4]


EXAMPLES = """# head

## 1. entailment · idx 10 · tipo
- **P:** Premise one.
- **H:** Hypothesis one.
- **Rascunho do Claude:** Draft one.
- **Sua versão:** Pedro one.
- [ ] usar

## 2. entailment · idx 11 · tipo
- **P:** Premise two.
- **H:** Hypothesis two.
- **Rascunho do Claude:** Draft two.
- **Sua versão:**
- [x] usar

## 3. not_entailment · idx 12 · tipo
- **P:** Premise three.
- **H:** Hypothesis three.
- **Rascunho do Claude:** Draft three.
- **Sua versão:**
- [ ] usar
"""


def test_rte_examples_prefer_pedro_then_draft_and_interleave(tmp_path, monkeypatch):
    path = tmp_path / "ex.md"
    path.write_text(EXAMPLES.replace("[x]", "[ ]"), encoding="utf-8")
    monkeypatch.setattr(rte, "EXAMPLES_MD", path)
    examples = rte.rte_examples()
    assert [ex["idx"] for ex in examples] == [10, 12, 11]  # interleaved by label, the extra one last
    assert [ex["explanation"] for ex in examples] == ["Pedro one.", "Draft three.", "Draft two."]


def test_rte_examples_keep_only_the_ticked_when_any(tmp_path, monkeypatch):
    path = tmp_path / "ex.md"
    path.write_text(EXAMPLES, encoding="utf-8")
    monkeypatch.setattr(rte, "EXAMPLES_MD", path)
    assert [ex["idx"] for ex in rte.rte_examples()] == [11]


def test_fa_uses_rte_examples_not_the_esnli_ones():
    fa = rte.prompt_for(P, H, "entailment", "FA")
    assert "sand castle" not in fa.lower() and rte.rte_examples()[0]["explanation"] in fa
    assert fa.endswith(rte.ASK_DECIDING_FACT)


@pytest.mark.parametrize(("answer", "cleaned"), [
    ("The text states he was given a lethal injection.", "He was given a lethal injection."),
    ("The premise explicitly states that iTunes software sold well.", "iTunes software sold well."),
    ("The text explicitly states the WTO has its headquarters in Madrid.", "The WTO has its headquarters in Madrid."),
    ("The text mentions an indictment but says nothing about the attorneys.",
     "The text mentions an indictment but says nothing about the attorneys."),  # noun phrase follows: left alone
    ("Ratan Tata is 70 years old.", "Ratan Tata is 70 years old."),
])
def test_clean_opening_drops_only_a_cited_clause_opener(answer, cleaned):
    assert rte.clean_opening(answer) == cleaned


@pytest.mark.skipif(not rte.TRAIN.exists(), reason="dados/rte não baixado (ver dados/README.md)")
def test_example_file_matches_the_data():
    train = pd.read_parquet(rte.TRAIN).set_index("idx")
    examples = rte.rte_examples()
    assert len(examples) == 20 and sum(ex["label"] == "entailment" for ex in examples) == 10
    for ex in examples:
        row = train.loc[ex["idx"]]
        assert (ex["premise"], ex["hypothesis"]) == (row.sentence1.strip(), row.sentence2.strip())
        assert rte.LABELS[row.label] == ex["label"]


@pytest.mark.skipif(not rte.TRAIN.exists(), reason="dados/rte não baixado (ver dados/README.md)")
def test_shuffled_train_is_fixed():
    a, b = rte.shuffled_train(), rte.shuffled_train()
    assert len(a) == 2490 and a["idx"].tolist() == b["idx"].tolist()
    assert set(a["label"]) == {"entailment", "not_entailment"}
