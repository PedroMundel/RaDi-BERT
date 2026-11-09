"""Qwen3.6-35B-A3B rationales for the GLUE RTE train set: variant F adapted to RTE's two labels (Pedro, 09/11).

F asks a "why" question about the pair, never naming the label nor "premise"/"hypothesis"; the gold label only picks
the question's shape. RTE has two labels, so `not_entailment` takes the neutral shape ("why does that not necessarily
mean"), which also holds when the pair is a contradiction. Adaptations for RTE's text:
  - F  (literal):   the e-SNLI template, "If {p}, why does that mean {h}?", where names keep their capital
                    (see inner()); 35% of RTE premises have 2+ sentences, so the "if" clause can be long.
  - FP (paragraph): the premise paragraph first, then "Why does that (not necessarily) mean that {h}?".
  - FP2:            FP, but the answer asks for what the passage says or leaves unsaid instead of "the world knowledge
                    behind the answer" (09/11: F's ask fits e-SNLI captions; in RTE the deciding fact is in the text).
  - FP3:            FP2 without naming "the passage": FP2's ask made 14/20 answers open with "The text states". As in
                    e-SNLI (E4 -> F), the trigger is removed instead of banning the phrase (Pedro, 09/11).
  - F3:             F's literal question with FP3's ask (F had 2/20 openings citing the text, FP 6, FP3 9).
  - FA:             FP3 with RTE examples instead of Pedro's 12 e-SNLI ones: the examples are the strongest lever on
                    style, and the e-SNLI ones teach world knowledge over captions. The examples come from
                    resultados/rte-35B/candidatos-exemplos-rte.md (Pedro's version when written, else the draft;
                    only the ones ticked "[x] usar" when any is ticked), and their pairs never enter any batch.
F to F3 keep Pedro's 12 e-SNLI example answers, each under the question its own pair asks in that variant.

Server: the same llama-server and LLAMA_ARGS as the e-SNLI batch (scripts/rodar_lote.sh, config/maquina.env).
Usage (safe to re-run: it skips idx already in the output):
    python -m radibert.rte_racionalizacoes gerar FA --n 20    # first 20 of the train set shuffled with seed 42
    python -m radibert.rte_racionalizacoes comparar FP3 FA    # checada-FP3-FA.md: two variants side by side
"""
import argparse
import csv
import datetime as dt
import os
import re
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd

from radibert import lote, piloto_qwen
from radibert.paths import RTE, RTE_35B

TRAIN = RTE / "rte_train.parquet"
EXAMPLES_MD = RTE_35B / "candidatos-exemplos-rte.md"
LABELS = {0: "entailment", 1: "not_entailment"}  # GLUE RTE ClassLabel order
SHAPE = {"entailment": "entailment", "not_entailment": "neutral"}  # which e-SNLI question shape each label takes
SEED = 42
WORKERS = int(os.environ.get("QWEN_WORKERS", "4"))
FIELDS = ["idx", "label", "sentence1", "sentence2", "variante", "qwen", "finish_reason", "tokens_in", "tokens_out",
          "seconds", "feito_em"]
PARAGRAPH_QUESTIONS = {"entailment": "{p}\n\nWhy does that mean that {h}?",
                       "neutral": "{p}\n\nWhy does that not necessarily mean that {h}?",
                       "contradiction": "{p}\n\nWhy can't it also be that {h}?"}


# Common non-name openers of RTE and e-SNLI sentences (from the most frequent first words of the RTE train set).
FUNCTION_STARTS = {"A", "An", "The", "There", "This", "That", "These", "Those", "It", "He", "She", "They", "We", "Some",
                   "One", "Two", "Three", "Four", "Five", "Several", "Many", "Most", "More", "Thousands", "In", "On",
                   "At", "As", "After", "According", "For", "With", "Although", "If", "Since", "Last", "About", "When",
                   "To", "By", "But", "While", "Over", "Meanwhile,", "Women", "People", "Police", "Humans",
                   "Scientists"}


def inner(sentence: str) -> str:
    """'The Pope died.' -> 'the Pope died', to sit inside a question. Unlike piloto_qwen.clause, a first word that is
    not an article, demonstrative or number keeps its capital: RTE sentences open with names ('Lina Joy, 42, ...')."""
    sentence = sentence.strip().rstrip(".!")
    first = sentence.split(" ", 1)[0]
    return sentence[0].lower() + sentence[1:] if first in FUNCTION_STARTS else sentence


def literal_question(premise: str, hypothesis: str, shape: str) -> str:
    return piloto_qwen.QUESTIONS[shape].format(p=inner(premise), h=inner(hypothesis))


def paragraph_question(premise: str, hypothesis: str, shape: str) -> str:
    return PARAGRAPH_QUESTIONS[shape].format(p=premise.strip(), h=inner(hypothesis))


def rte_examples() -> list[dict]:
    """The RTE example pairs of candidatos-exemplos-rte.md, interleaved by label so no label sits last."""
    blocks = re.split(r"\n## \d+\. ", EXAMPLES_MD.read_text(encoding="utf-8"))[1:]
    examples = []
    for block in blocks:
        field = lambda name: re.search(rf"^- \*\*{name}:\*\*[ \t]*(.*)$", block, re.M).group(1).strip()  # noqa: B023  called in this same iteration
        label, idx = re.match(r"(\w+) · idx (\d+)", block).groups()
        examples.append({"idx": int(idx), "label": label, "premise": field("P"), "hypothesis": field("H"),
                         "explanation": field("Sua versão") or field("Rascunho do Claude"),
                         "ticked": bool(re.search(r"^- \[x\] usar", block, re.M | re.I))})
    if any(ex["ticked"] for ex in examples):
        examples = [ex for ex in examples if ex["ticked"]]
    by_label = [[ex for ex in examples if ex["label"] == label] for label in LABELS.values()]
    interleaved = [ex for pair in zip(*by_label) for ex in pair]
    return interleaved + [ex for group in by_label for ex in group[len(interleaved) // 2:]]


def rte_examples_block() -> str:
    examples = [piloto_qwen.QA_EXAMPLE.format(
        question=paragraph_question(ex["premise"], ex["hypothesis"], SHAPE[ex["label"]]), explanation=ex["explanation"])
        for ex in rte_examples()]
    return "Examples:\n\n" + "\n\n".join(examples) + "\n\nNow the question to answer:"


QUESTION_MAKERS = {"F": literal_question, "FP": paragraph_question, "FP2": paragraph_question,
                   "FP3": paragraph_question, "F3": literal_question, "FA": paragraph_question}
ASK_FROM_TEXT = ("Answer in one sentence (about 30 words at most) with what the passage says, or leaves unsaid, that "
                 "decides the answer; use world knowledge only when the passage relies on it. Follow the style of the "
                 "examples. Write only the answer.")
ASK_DECIDING_FACT = ("Answer in one sentence (about 30 words at most) with the fact that decides it, or the fact that "
                     "is missing; use world knowledge only when it is needed. Follow the style of the examples. Write "
                     "only the answer.")
ASKS = {"F": piloto_qwen.ASK_ANSWER, "FP": piloto_qwen.ASK_ANSWER, "FP2": ASK_FROM_TEXT, "FP3": ASK_DECIDING_FACT,
        "F3": ASK_DECIDING_FACT, "FA": ASK_DECIDING_FACT}


def prompt_for(premise: str, hypothesis: str, label: str, variant: str) -> str:
    make = QUESTION_MAKERS[variant]
    examples = rte_examples_block() if variant == "FA" else piloto_qwen.question_examples(make)
    return piloto_qwen.PROMPT_QUESTION.format(definitions=examples, ask=ASKS[variant],
                                              question=make(premise, hypothesis, SHAPE[label]))


# Path C (Pedro, 09/11: only if neither the examples nor the framing removed the opening): drop a leading
# "The text (explicitly) states (that)" when what follows is a whole clause. Openers followed by a noun phrase
# ("The text mentions an indictment but...") are left alone: cutting them would leave a broken sentence.
CITED_OPENING = re.compile(r"^The (?:text|premise|passage|sentence)(?: \w+ly)? (?:states|says|notes|reports)(?: that)? ")


def clean_opening(answer: str) -> str:
    rest = CITED_OPENING.sub("", answer, count=1)
    if rest == answer:
        return answer
    keep_case = rest[:1].islower() and rest[1:2].isupper()  # "iTunes"
    return rest if keep_case else rest[:1].upper() + rest[1:]


def shuffled_train() -> pd.DataFrame:
    train = pd.read_parquet(TRAIN)
    train["label"] = train["label"].map(LABELS)
    return train.sample(frac=1, random_state=SEED).reset_index(drop=True)


def output_path(variant: str):
    return RTE_35B / f"racionalizacoes-{variant}.csv"


def generate(row, variant: str) -> dict:
    out = piloto_qwen.ask_qwen(prompt_for(row.sentence1, row.sentence2, row.label, variant))
    return {"idx": row.idx, "label": row.label, "sentence1": row.sentence1, "sentence2": row.sentence2,
            "variante": variant, **out, "feito_em": dt.datetime.now().isoformat(timespec="seconds")}


def cmd_gerar(variant: str, n: int):
    lote.keep_awake()
    out = output_path(variant)
    out.parent.mkdir(parents=True, exist_ok=True)
    done = set(pd.read_csv(out, usecols=["idx"])["idx"]) if out.exists() else set()
    skip = done | {ex["idx"] for ex in rte_examples()}  # an example pair never becomes a training target
    todo = [row for row in shuffled_train().head(n).itertuples(index=False) if row.idx not in skip]
    start = time.perf_counter()
    with open(out, "a", newline="", encoding="utf-8") as f, ThreadPoolExecutor(WORKERS) as pool:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if not done:
            writer.writeheader()
        for i, result in enumerate(pool.map(lambda row: generate(row, variant), todo), 1):
            writer.writerow(result)
            f.flush()
            if i % 50 == 0:
                print(f"{dt.datetime.now():%H:%M:%S} {len(done) + i} no arquivo, {i}/{len(todo)} nesta rodada, "
                      f"{(time.perf_counter() - start) / i:.2f} s/par", flush=True)
    print(f"{variant}: {len(todo)} novos, {len(done) + len(todo)} no arquivo {out}", flush=True)


def cmd_comparar(a: str, b: str):
    left, right = (pd.read_csv(output_path(v)) for v in (a, b))
    both = left.merge(right[["idx", "qwen"]], on="idx", suffixes=("_a", "_b"))
    lines = [f"# RTE: {a} x {b}, {len(both)} pares do treino (Qwen3.6-35B-A3B)", "",
             "Para a checada rápida da D1. Ordem = treino embaralhado com semente 42. Nada aqui foi lido ainda.", ""]
    for i, r in enumerate(both.itertuples(index=False), 1):
        lines += [f"## {i}. idx {r.idx} · {r.label}", "", f"- **Premissa:** {r.sentence1}",
                  f"- **Hipótese:** {r.sentence2}", f"- **{a}:** {r.qwen_a}", f"- **{b}:** {r.qwen_b}", ""]
    path = RTE_35B / f"checada-{a}-{b}.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(both)} pares -> {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", choices=["gerar", "comparar"])
    parser.add_argument("variantes", nargs="*", choices=sorted(QUESTION_MAKERS), default=["F"])
    parser.add_argument("--n", type=int, default=20)
    args = parser.parse_args()
    if args.cmd == "gerar":
        cmd_gerar(args.variantes[0], args.n)
    else:
        cmd_comparar(*args.variantes)
