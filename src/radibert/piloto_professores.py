"""Pilot: LLM rationales for 1,000 e-SNLI dev pairs, from two teachers (Haiku 5.5 and Sonnet 5.5).

Same pairs, same prompt, both models, via the Message Batches API (50% price).
Rationales are post-hoc: the prompt gives the gold label, as the e-SNLI annotators had it.

Usage (run from anywhere; paths are absolute):
    python -m radibert.piloto_professores amostra   # build the sample and show one prompt; no API call
    python -m radibert.piloto_professores enviar    # submit the batch (needs ANTHROPIC_API_KEY); saves the batch id
    python -m radibert.piloto_professores status    # check progress
    python -m radibert.piloto_professores coletar   # download results -> resultados.csv + custo.md
"""
import json
import sys

import pandas as pd

from radibert.paths import ESNLI_DEV, PILOTO_PROFESSORES

CSV_DEV = ESNLI_DEV
SAMPLE = PILOTO_PROFESSORES / "amostra.csv"
STATE = PILOTO_PROFESSORES / "estado.json"
RESULTS = PILOTO_PROFESSORES / "resultados.csv"
COST = PILOTO_PROFESSORES / "custo.md"

N_PER_LABEL = {"entailment": 334, "neutral": 333, "contradiction": 333}
SEED = 42
MODELS = {"haiku": "claude-haiku-5-5", "sonnet": "claude-sonnet-5-5"}
# USD per 1M tokens, Batch API (50% of standard). Source: claude-api skill table, cached 2026-10-06.
BATCH_PRICE = {"haiku": (0.05, 0.25), "sonnet": (1.00, 5.00)}

PROMPT = """You are annotating a natural language inference dataset.

Labels:
- entailment: if the premise is true, the hypothesis must be true.
- neutral: the hypothesis might be true, but the premise does not guarantee it.
- contradiction: if the premise is true, the hypothesis cannot be true (both describe the same scene).

Premise: {premise}
Hypothesis: {hypothesis}
Label: {label}

Explain in one or two sentences why this label is correct. Do not name the label. Write only the explanation."""


def build_sample() -> pd.DataFrame:
    df = pd.read_csv(CSV_DEV)
    df = df[df["gold_label"].isin(N_PER_LABEL)]
    parts = [df[df["gold_label"] == lab].sample(n, random_state=SEED) for lab, n in N_PER_LABEL.items()]
    sample = pd.concat(parts).reset_index(drop=True)
    sample.index.name = "idx"
    sample.to_csv(SAMPLE)
    return sample


def prompt_for(row) -> str:
    return PROMPT.format(premise=row.Sentence1, hypothesis=row.Sentence2, label=row.gold_label)


def cmd_amostra():
    sample = build_sample()
    print(f"{len(sample)} pairs -> {SAMPLE}")
    print(sample["gold_label"].value_counts().to_string())
    print(f"\n{len(sample) * len(MODELS)} requests would be sent. Example prompt:\n")
    print(prompt_for(sample.iloc[0]))


def cmd_enviar():
    import anthropic
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request

    if STATE.exists():
        sys.exit(f"{STATE} already exists: a batch was already submitted. Use 'status' or 'coletar'.")
    sample = build_sample()
    requests = [
        Request(
            custom_id=f"{short}-{idx}",
            params=MessageCreateParamsNonStreaming(
                model=model,
                max_tokens=1024,  # thinking counts toward max_tokens
                output_config={"effort": "low"},
                messages=[{"role": "user", "content": prompt_for(row)}],
            ),
        )
        for short, model in MODELS.items()
        for idx, row in sample.iterrows()
    ]
    batch = anthropic.Anthropic().messages.batches.create(requests=requests)
    STATE.write_text(json.dumps({"batch_id": batch.id, "models": MODELS, "n": len(requests)}, indent=2))
    print(f"Submitted {len(requests)} requests. Batch {batch.id} -> {STATE}")


def load_batch_id() -> str:
    if not STATE.exists():
        sys.exit("No batch submitted yet. Run 'enviar' first.")
    return json.loads(STATE.read_text())["batch_id"]


def cmd_status():
    import anthropic

    batch = anthropic.Anthropic().messages.batches.retrieve(load_batch_id())
    print(batch.processing_status, batch.request_counts)


def cmd_coletar():
    import anthropic

    client = anthropic.Anthropic()
    batch_id = load_batch_id()
    if client.messages.batches.retrieve(batch_id).processing_status != "ended":
        sys.exit("Batch still processing. Try 'status' later.")

    sample = pd.read_csv(SAMPLE, index_col="idx")
    tokens = {short: [0, 0] for short in MODELS}
    failures = []
    for result in client.messages.batches.results(batch_id):
        short, idx = result.custom_id.split("-")
        if result.result.type != "succeeded":
            failures.append(f"{result.custom_id}: {result.result.type}")
            continue
        msg = result.result.message
        text = next((b.text for b in msg.content if b.type == "text"), "")
        if msg.stop_reason != "end_turn":
            failures.append(f"{result.custom_id}: stop_reason={msg.stop_reason}")
        sample.loc[int(idx), short] = text.strip()
        tokens[short][0] += msg.usage.input_tokens
        tokens[short][1] += msg.usage.output_tokens

    cols = ["pairID", "gold_label", "Sentence1", "Sentence2", "Explanation_1", *MODELS]
    sample[cols].to_csv(RESULTS)

    lines = ["# Custo real do piloto", "", f"Batch `{batch_id}`.", "",
             "| Professor | Tokens entrada | Tokens saída | US$ (lote) |", "|---|---|---|---|"]
    total = 0.0
    for short, (tin, tout) in tokens.items():
        price_in, price_out = BATCH_PRICE[short]
        usd = tin / 1e6 * price_in + tout / 1e6 * price_out
        total += usd
        lines.append(f"| {MODELS[short]} | {tin:,} | {tout:,} | {usd:.3f} |")
    lines += ["", f"**Total: US$ {total:.3f}**", "", f"Falhas ou cortes: {len(failures)}", *[f"- {f}" for f in failures]]
    COST.write_text("\n".join(lines), encoding="utf-8")
    print(f"{RESULTS}\n{COST}\nTotal US$ {total:.3f}; failures: {len(failures)}")


if __name__ == "__main__":
    commands = {"amostra": cmd_amostra, "enviar": cmd_enviar, "status": cmd_status, "coletar": cmd_coletar}
    if len(sys.argv) != 2 or sys.argv[1] not in commands:
        sys.exit(__doc__)
    commands[sys.argv[1]]()
