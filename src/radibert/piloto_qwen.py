"""Pilot: Qwen3.5-9B rationales for 45 e-SNLI dev pairs, served locally by llama-server.

The 45 pairs (15 per label) come from the Claude pilot sample, so every Qwen text sits next to the
human, Haiku and Sonnet texts for the same pair. Same prompt as the Claude pilot (post-hoc, gold label given).

Start the server first (thinking off, OpenAI-compatible endpoint on port 8080):
    llama-server -m Qwen3.5-9B-Q4_K_M.gguf -ngl 999 -c 4096 --jinja --port 8080

Usage (paths are absolute; safe to re-run, it skips pairs already generated):
    python -m radibert.piloto_qwen amostra   # pick the 45 pairs and show one prompt; no server needed
    python -m radibert.piloto_qwen amostra90 # the 45 pairs + 45 new ones -> amostra-90.csv; run with QWEN_SAMPLE=amostra-90.csv
    python -m radibert.piloto_qwen gerar     # prompt A -> resultados.csv + lado-a-lado.md + vazao.md
    python -m radibert.piloto_qwen gerar B   # prompt B (no label definitions) -> resultados-B.csv + lado-a-lado-B.md + vazao-B.md
    python -m radibert.piloto_qwen gerar D   # prompt D (B + one sentence with the deciding fact) -> files with suffix -D
    python -m radibert.piloto_qwen gerar E   # prompt E (linking knowledge + Pedro's 12 examples) -> files with suffix -E
    python -m radibert.piloto_qwen gerar E2  # prompt E + one near-literal entailment example -> files with suffix -E2
    python -m radibert.piloto_qwen gerar E3  # prompt E + "no filler when the hypothesis repeats the premise" -> suffix -E3
    python -m radibert.piloto_qwen gerar E4  # prompt E3 + no "the premise says" and no relation words -> suffix -E4
    python -m radibert.piloto_qwen gerar F   # E's 12 answers, but each pair asked as a "why" question, no label -> suffix -F
    python -m radibert.piloto_qwen gerar FR  # F, but Qwen first rewrites each pair into one natural question -> suffix -FR
    python -m radibert.piloto_qwen gerar FRG # FR, falling back to F's template when the rewrite leaves its label's shape -> -FRG
QWEN_WORKERS=4 sends 4 requests at once (the server needs -np >= 4); results come back in sample order.
"""
import functools
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import pandas as pd
import requests

from radibert.paths import PILOTO_PROFESSORES, PILOTO_QWEN

CLAUDE_PILOT = PILOTO_PROFESSORES / "resultados.csv"
# QWEN_SAMPLE=amostra-90.csv runs the 90-pair sample (python -m radibert.piloto_qwen amostra90) instead of the original 45.
SAMPLE = PILOTO_QWEN / os.environ.get("QWEN_SAMPLE", "amostra.csv")
EXAMPLES_MD = PILOTO_QWEN / "candidatos-exemplos.md"  # Pedro's final "Sua versão" per pair, 12 dev pairs outside the sample
EXAMPLES_CSV = PILOTO_QWEN / "candidatos-exemplos.csv"

# Another teacher behind the same server: QWEN_MODEL names it in the reports, QWEN_TAG suffixes its output files.
MODEL = os.environ.get("QWEN_MODEL", "Qwen3.5-9B")
TAG = os.environ.get("QWEN_TAG", "")
# Requests in flight at once; the server needs at least as many slots (llama-server -np, default auto = 4).
WORKERS = int(os.environ.get("QWEN_WORKERS", "1"))

N_PER_LABEL = 15
SEED = 42
SERVER = "http://127.0.0.1:8080/v1/chat/completions"
# Qwen3.5-9B model card, "Instruct (or non-thinking) mode for general tasks".
SAMPLING = {"temperature": 0.7, "top_p": 0.8, "top_k": 20, "min_p": 0.0, "presence_penalty": 1.5}

LABEL_DEFINITIONS = """
Labels:
- entailment: if the premise is true, the hypothesis must be true.
- neutral: the hypothesis might be true, but the premise does not guarantee it.
- contradiction: if the premise is true, the hypothesis cannot be true (both describe the same scene).
"""
PROMPT = """You are annotating a natural language inference dataset.
{definitions}
Premise: {premise}
Hypothesis: {hypothesis}
Label: {label}

{ask} Do not name the label. Write only the explanation."""
ASK_TWO_SENTENCES = "Explain in one or two sentences why this label is correct."
ASK_DECIDING_FACT = ("Explain in one sentence (at most 25 words) why this label is correct, "
                     "stating the fact from the premise that decides it.")
ASK_LINKING_KNOWLEDGE = ("Explain in one sentence (about 30 words at most) why this label is correct, stating the "
                         "world knowledge that links the premise to the hypothesis. For entailment, cover what the "
                         "hypothesis adds; for neutral, give an alternative the premise allows; for contradiction, "
                         "say why both cannot happen in the same scene. Follow the style of the examples.")
ASK_NO_FILLER = ASK_LINKING_KNOWLEDGE + (" When the hypothesis only repeats part of the premise, answer in a few "
                                         "words with no filler.")
ASK_NO_META = ASK_NO_FILLER + (' Do not refer to the premise or the hypothesis (no "the premise says", "the hypothesis '
                               'states"), and do not use relation words such as contradicts, confirms, supports or '
                               'entails.')
EXAMPLE = "Premise: {premise}\nHypothesis: {hypothesis}\nLabel: {label}\nExplanation: {explanation}"

# F (Pedro, 25/10): no label, no "premise"/"hypothesis", no annotation framing. The gold label only picks the
# shape of a "why" question about the scene, so the model answers the question instead of defending a label.
PROMPT_QUESTION = """{definitions}
Question: {question}

{ask}"""
QUESTIONS = {"entailment": "If {p}, why does that mean {h}?",
             "neutral": "If {p}, why does that not necessarily mean {h}?",
             "contradiction": "If {p}, why can't it also be that {h}, in the same place and moment?"}
ASK_ANSWER = ("Answer in one sentence (about 30 words at most) with the world knowledge behind the answer. "
              "Follow the style of the examples. Write only the answer.")
QA_EXAMPLE = "Question: {question}\nAnswer: {explanation}"


def clause(sentence: str) -> str:
    """'A man is painting.' -> 'a man is painting', to sit inside a question; keeps 'I' and all-caps first words."""
    sentence = sentence.strip().rstrip(".!")
    first = sentence.split(" ", 1)[0]
    keep = first == "I" or (len(first) > 1 and first.isupper())
    return sentence if keep else sentence[0].lower() + sentence[1:]


def question(premise: str, hypothesis: str, label: str) -> str:
    return QUESTIONS[label].format(p=clause(premise), h=clause(hypothesis))


# FR (Pedro, 26/10): instead of the template, Qwen fuses the two sentences into one question, as in Pedro's
# "why can't a man riding a motorcycle be climbing a tree?". The label only picks the shape, never named.
REWRITE_PROMPT = """Turn the two sentences into one short, natural "why" question about the scene, in the given shape.
Keep the details that matter, drop the rest, and do not answer it. Write only the question.

{examples}

Sentence 1: {premise}
Sentence 2: {hypothesis}
Shape: {shape}
Question:"""
SHAPES = {"entailment": "Why does ... mean ...?",
          "neutral": "Why is ... not necessarily ...?",
          "contradiction": "Why can't ... be ...?"}
REWRITE_EXAMPLE = "Sentence 1: {premise}\nSentence 2: {hypothesis}\nShape: {shape}\nQuestion: {question}"
# Three of Pedro's 12 example pairs (outside the sample); the contradiction is Pedro's own question, fitted to its pair.
REWRITE_EXAMPLES = "\n\n".join(REWRITE_EXAMPLE.format(shape=SHAPES[label], **ex) for label, ex in [
    ("entailment", {"premise": "Man builds detailed sand castle on the beach.",
                    "hypothesis": "An adult is working with sand.",
                    "question": "Why does a man building a sand castle mean an adult is working with sand?"}),
    ("neutral", {"premise": "Two Asian women wear sandals, long silk robes and hold umbrellas.",
                 "hypothesis": "Two women stand in the rain",
                 "question": "Why are two women holding umbrellas not necessarily standing in the rain?"}),
    ("contradiction", {"premise": "A biker wearing a white t-shirt is jumping over dirt hills.",
                       "hypothesis": "A biker climbs a tree in a shirt.",
                       "question": "Why can't a biker jumping over dirt hills be climbing a tree?"})])


@functools.cache
def rewrite_question(premise: str, hypothesis: str, label: str) -> str:
    """One Qwen call per pair; cached because the 12 example questions are rebuilt for every item."""
    out = ask_qwen(REWRITE_PROMPT.format(examples=REWRITE_EXAMPLES, premise=premise, hypothesis=hypothesis,
                                         shape=SHAPES[label]))
    return out["qwen"].splitlines()[0].strip().strip('"')


# FRG guard (Pedro, 26/10): in FR, #126 came back as a neutral question for an entailment pair.
SHAPE_CHECKS = {"entailment": re.compile(r"^Why (?:does|do) (?!.*not necessarily).* mean "),
                "neutral": re.compile(r"^Why .*not necessarily"),
                "contradiction": re.compile(r"^Why can.t ")}


def guarded_question(premise: str, hypothesis: str, label: str) -> str:
    rewritten = rewrite_question(premise, hypothesis, label)
    return rewritten if SHAPE_CHECKS[label].search(rewritten) else question(premise, hypothesis, label)


# E2's 13th example: a near-literal entailment with a short answer, in the form Pedro gave
# ("Gray-haired means having gray hair."). That sentence answers sample pair 126, so a dev pair outside the
# sample with the same shape stands in for it.
NEAR_LITERAL = EXAMPLE.format(premise="A man is leaning out of a window to paint some decorative iron white.",
                              hypothesis="A man is painting.", label="entailment",
                              explanation="Painting the iron white means he is painting.")


def pedro_examples() -> list[dict]:
    """Pedro's 12 examples from candidatos-exemplos.md, interleaved by label so no label sits last."""
    blocks = re.split(r"\n## \d+\. ", EXAMPLES_MD.read_text(encoding="utf-8"))[1:]
    by_label = {}
    for block in blocks:
        label = block.split(" ", 1)[0]
        field = lambda name: re.search(rf"^- \*\*{name}:\*\* (.+)$", block, re.M).group(1).strip()  # noqa: B023  called in this same iteration
        by_label.setdefault(label, []).append(
            {"premise": field("P"), "hypothesis": field("H"), "label": label, "explanation": field("Sua versão")})
    interleaved = [ex for trio in zip(*by_label.values()) for ex in trio]
    assert len(interleaved) == 12, len(interleaved)
    return interleaved


def load_examples(extra: str | None = None) -> str:
    """The 12 examples in the Premise/Hypothesis/Label form; `extra` goes right after the first trio."""
    examples = [EXAMPLE.format(**ex) for ex in pedro_examples()]
    if extra:
        examples.insert(3, extra)
    return "\nExamples:\n\n" + "\n\n".join(examples) + "\n\nNow the item to explain:\n"


def question_examples(make_question=question) -> str:
    """The same 12 answers, each under the question its pair asks in F (template) or FR (rewritten)."""
    examples = [QA_EXAMPLE.format(question=make_question(ex["premise"], ex["hypothesis"], ex["label"]),
                                  explanation=ex["explanation"]) for ex in pedro_examples()]
    return "Examples:\n\n" + "\n\n".join(examples) + "\n\nNow the question to answer:"


# A is identical to src/radibert/piloto_professores.py, so the teachers differ only in the model.
# B drops the label definitions; D also asks for one sentence with the deciding fact.
# E replaces D's ask with the linking knowledge and puts Pedro's 12 examples where the definitions were.
# E2 adds the near-literal entailment example; E3 keeps E's examples and adds a no-filler line to the ask;
# E4 is E3 plus a ban on naming the premise/hypothesis and on relation words.
# F keeps E's 12 answers and swaps the framing: a "why" question per pair, in PROMPT_QUESTION.
VARIANTS = {"A": (LABEL_DEFINITIONS, ASK_TWO_SENTENCES),
            "B": ("", ASK_TWO_SENTENCES),
            "D": ("", ASK_DECIDING_FACT),
            "E": (load_examples, ASK_LINKING_KNOWLEDGE),
            "E2": (lambda: load_examples(NEAR_LITERAL), ASK_LINKING_KNOWLEDGE),
            "E3": (load_examples, ASK_NO_FILLER),
            "E4": (load_examples, ASK_NO_META),
            "F": (question_examples, ASK_ANSWER),
            "FR": (lambda: question_examples(rewrite_question), ASK_ANSWER),
            "FRG": (lambda: question_examples(guarded_question), ASK_ANSWER)}
QUESTION_MAKERS = {"F": question, "FR": rewrite_question, "FRG": guarded_question}


def build_sample() -> pd.DataFrame:
    df = pd.read_csv(CLAUDE_PILOT, index_col="idx")
    parts = [df[df["gold_label"] == lab].sample(N_PER_LABEL, random_state=SEED)
             for lab in ("entailment", "neutral", "contradiction")]
    sample = pd.concat(parts)
    sample.to_csv(SAMPLE)
    return sample


def cmd_amostra90():
    """The original 45 pairs plus 15 more per label from the Claude pilot, never one of the 12 example pairs."""
    old = pd.read_csv(PILOTO_QWEN / "amostra.csv", index_col="idx")
    df = pd.read_csv(CLAUDE_PILOT, index_col="idx")
    rest = df.drop(index=old.index)
    rest = rest[~rest["pairID"].isin(pd.read_csv(EXAMPLES_CSV)["pairID"])]
    new = pd.concat([rest[rest["gold_label"] == lab].sample(N_PER_LABEL, random_state=SEED)
                     for lab in ("entailment", "neutral", "contradiction")])
    path = PILOTO_QWEN / "amostra-90.csv"
    pd.concat([old, new]).to_csv(path)
    print(f"{len(old)} + {len(new)} pairs -> {path}")


def outputs(variant: str) -> tuple[Path, Path, Path]:
    """results csv, side-by-side md, throughput md; variant A keeps the original file names."""
    suffix = ("" if variant == "A" else f"-{variant}") + (f"-{TAG}" if TAG else "")
    out = PILOTO_QWEN / os.environ.get("QWEN_OUT", "")  # QWEN_OUT=subfolder keeps measurement runs out of the main folder
    out.mkdir(exist_ok=True)
    return out / f"resultados{suffix}.csv", out / f"lado-a-lado{suffix}.md", out / f"vazao{suffix}.md"


def prompt_for(row, variant: str = "A") -> str:
    definitions, ask = VARIANTS[variant]
    if callable(definitions):
        definitions = definitions()
    if variant in QUESTION_MAKERS:
        return PROMPT_QUESTION.format(definitions=definitions, ask=ask, question=QUESTION_MAKERS[variant](
            row.Sentence1, row.Sentence2, row.gold_label))
    return PROMPT.format(definitions=definitions, premise=row.Sentence1,
                         hypothesis=row.Sentence2, label=row.gold_label, ask=ask)


def ask_qwen(prompt: str) -> dict:
    body = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200,
        "seed": SEED,
        "chat_template_kwargs": {"enable_thinking": False},
        **SAMPLING,
    }
    start = time.perf_counter()
    resp = requests.post(SERVER, json=body, timeout=300)
    resp.raise_for_status()
    seconds = time.perf_counter() - start
    data = resp.json()
    choice = data["choices"][0]
    return {
        "qwen": choice["message"]["content"].strip(),
        "finish_reason": choice["finish_reason"],
        "tokens_in": data["usage"]["prompt_tokens"],
        "tokens_out": data["usage"]["completion_tokens"],
        "seconds": round(seconds, 2),
    }


def cmd_amostra():
    sample = build_sample()
    print(f"{len(sample)} pairs -> {SAMPLE}")
    print(sample["gold_label"].value_counts().to_string())
    print("\nExample prompt:\n")
    print(prompt_for(sample.iloc[0]))


def generate(idx, row, variant: str) -> pd.DataFrame:
    start = time.perf_counter()
    out = ask_qwen(prompt_for(row, variant))
    if variant in ("FR", "FRG"):  # the rewrite counts in the time
        out["seconds"] = round(time.perf_counter() - start, 2)
        out["pergunta"] = QUESTION_MAKERS[variant](row.Sentence1, row.Sentence2, row.gold_label)
        out["guarda"] = out["pergunta"] != rewrite_question(row.Sentence1, row.Sentence2, row.gold_label)
    return pd.DataFrame([{**row.to_dict(), **out}], index=pd.Index([idx], name="idx"))


def cmd_gerar(variant: str):
    results_csv, side_md, throughput_md = outputs(variant)
    sample = pd.read_csv(SAMPLE, index_col="idx") if SAMPLE.exists() else build_sample()
    done = pd.read_csv(results_csv, index_col="idx") if results_csv.exists() else sample.iloc[0:0]
    todo = sample.drop(index=done.index, errors="ignore")
    definitions = VARIANTS[variant][0]
    if callable(definitions):
        definitions()  # FR/FRG rewrite the 12 example questions once, before the threads share the cache
    rows = [done]
    start = time.perf_counter()
    with ThreadPoolExecutor(WORKERS) as pool:
        futures = [pool.submit(generate, idx, row, variant) for idx, row in todo.iterrows()]
        for future in as_completed(futures):
            rows.append(future.result())
            pd.concat(rows).to_csv(results_csv)  # checkpoint after every pair
            r = rows[-1].iloc[0]
            print(f"{rows[-1].index[0]} {r.gold_label:13} {r.tokens_out:3} tok {r.seconds:5.1f}s  {r.qwen[:70]}")
    wall = time.perf_counter() - start
    results = pd.concat(rows)
    results = results.loc[sample.index.intersection(results.index, sort=False)]  # back to sample order
    results.to_csv(results_csv)
    write_side_by_side(results, side_md, variant)
    write_throughput(results, throughput_md, variant, wall, len(todo))
    print(f"\n{results_csv}\n{side_md}\n{throughput_md}")


def write_side_by_side(results: pd.DataFrame, path: Path, variant: str):
    prompt_note = ("Mesmo prompt do piloto do Claude." if variant == "A"
                   else f"Variante {variant} do prompt; Haiku e Sonnet são do prompt A.")
    lines = [f"# Piloto {MODEL}, variante {variant}: lado a lado ({len(results)} pares do dev do e-SNLI)", "",
             f"{prompt_note} Humano = `Explanation_1` do e-SNLI.", ""]
    if variant in ("FR", "FRG"):
        lines += ["## Perguntas reescritas dos 12 exemplos", ""] + [
            f"- ({ex['label']}) {QUESTION_MAKERS[variant](ex['premise'], ex['hypothesis'], ex['label'])}"
            for ex in pedro_examples()] + [""]
    for idx, r in results.iterrows():
        lines += [f"## {idx} · {r.gold_label}", "",
                  f"- **P:** {r.Sentence1}", f"- **H:** {r.Sentence2}", ""]
        if "pergunta" in r:
            lines += [f"- **Pergunta:** {r.pergunta}", ""]
        lines += ["| Fonte | Justificativa |", "|---|---|",
                  f"| Humano | {r.Explanation_1} |", f"| Haiku | {r.haiku} |",
                  f"| Sonnet | {r.sonnet} |", f"| **Qwen {variant}** | {r.qwen} |", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_throughput(results: pd.DataFrame, path: Path, variant: str, wall: float, n_new: int):
    out_tok, secs = int(results["tokens_out"].sum()), results["seconds"].sum()
    cut = results[results["finish_reason"] != "stop"]
    think = results[results["qwen"].str.contains("<think>|</think>", regex=True)]
    lines = [f"# Vazão e falhas do piloto {MODEL}, variante {variant} ({WORKERS} pedido(s) simultâneo(s), RTX 5060)",
             "",
             f"- Pares: {len(results)}",
             f"- Tokens de saída: {out_tok} (mediana {results['tokens_out'].median():.0f} por par)",
             f"- Soma dos tempos por pedido: {secs:.0f} s · {out_tok / secs:.1f} tok/s por fluxo (inclui prefill)",
             f"- Tempo de parede desta rodada: {wall:.0f} s para {n_new} pares novos"
             + (f" · {wall / n_new:.2f} s/par" if n_new else ""),
             f"- Cortes (`finish_reason` != stop): {len(cut)} {list(cut.index)}",
             f"- Vazamento de `<think>`: {len(think)} {list(think.index)}"]
    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    if sys.argv[1:] == ["amostra"]:
        cmd_amostra()
    elif sys.argv[1:] == ["amostra90"]:
        cmd_amostra90()
    elif len(sys.argv) in (2, 3) and sys.argv[1] == "gerar" and (sys.argv[2:] or ["A"])[0] in VARIANTS:
        cmd_gerar((sys.argv[2:] or ["A"])[0])
    else:
        sys.exit(__doc__)
