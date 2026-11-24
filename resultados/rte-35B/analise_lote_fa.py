"""Automatic counts over the FA batch and the 30-pair reading sample (09/11, before the first training run).

Usage: uv run --frozen python resultados/rte-35B/analise_lote_fa.py
Prints the counts quoted in analise-lote-FA.md and writes leitura-30-FA.md (15 + 15 pairs, seed 2026).
Input length is estimated from words (x 1.3 WordPiece tokens per word, a rough rule): the project has no tokenizer
installed yet.
"""
import re

import pandas as pd

from radibert.copia import new_words
from radibert.paths import RTE_35B
from radibert.rte_racionalizacoes import clean_opening, rte_examples

SAMPLE_SEED = 2026
NEGATION = re.compile(r"\b(?:not|no|never|neither|nor|without|only|unclear|unknown|missing|lacks?|but)\b|n't", re.I)
NAMES_LABEL = re.compile(r"entail|contradict", re.I)  # the label word itself
QUESTION_ECHO = re.compile(r"\bimpl(?:y|ies|ied)\b|not necessarily", re.I)  # words of the question's shape
TOKENS_PER_WORD = 1.3


def words(text) -> int:
    return len(str(text).split())


def main():
    df = pd.read_csv(RTE_35B / "racionalizacoes-FA.csv")
    examples = {ex["idx"] for ex in rte_examples()}
    df["clean"] = df["qwen"].map(clean_opening)
    df["n_words"] = df["clean"].map(words)
    df["input_tokens_est"] = (df["sentence1"].map(words) + df["sentence2"].map(words)) * TOKENS_PER_WORD + 3
    df["has_negation"] = df["clean"].str.contains(NEGATION)
    df["names_label"] = df["qwen"].str.contains(NAMES_LABEL)
    df["question_echo"] = df["qwen"].str.contains(QUESTION_ECHO)
    df["echo_h"] = [new_words(r, h) == 0 for r, h in zip(df["clean"], df["sentence2"])]
    df["new_vs_input"] = [new_words(r, p + " " + h) for r, p, h in zip(df["clean"], df["sentence1"], df["sentence2"])]

    ent, non = df[df.label == "entailment"], df[df.label == "not_entailment"]
    print(f"rows {len(df)} · unique idx {df.idx.nunique()} · examples inside {len(set(df.idx) & examples)}")
    print(f"labels {df.label.value_counts().to_dict()} · finish {df.finish_reason.value_counts().to_dict()}")
    print(f"empty {(df.clean.str.strip() == '').sum()} · duplicated rationale {df.clean.duplicated().sum()}")
    print(f"words: median {df.n_words.median():.0f}, p95 {df.n_words.quantile(.95):.0f}, max {df.n_words.max()}")
    q = df.input_tokens_est
    print(f"input tokens (est.): median {q.median():.0f}, p95 {q.quantile(.95):.0f}, max {q.max():.0f}, "
          f">256 {(q > 256).sum()}, >512 {(q > 512).sum()}")
    print(f"entailment with negation/hedge word {ent.has_negation.sum()}/{len(ent)}")
    print(f"not_entailment without any {(~non.has_negation).sum()}/{len(non)}")
    print(f"names the label {df.names_label.sum()} (ent {ent.names_label.sum()}, non {non.names_label.sum()})")
    print(f"repeats the question's words (implies / not necessarily) {df.question_echo.sum()}")
    print(f"echo of the hypothesis (no content word beyond H) {df.echo_h.sum()} "
          f"(ent {ent.echo_h.sum()}, non {non.echo_h.sum()})")
    print(f"rationales with 0 content words outside P+H {(df.new_vs_input == 0).sum()}; "
          f"median new words {df.new_vs_input.median():.0f}")
    # The count of cuts that leave a subjectless verb was dropped (09/11): since E5, clean_opening refuses exactly
    # those cuts, so the count was 0 by construction. The 450 -> >= 96 finding of the first reading is in the report.
    print(f"C cut an opening in {(df['qwen'] != df['clean']).sum()}")
    openers = df["clean"].str.split().str[:2].str.join(" ").value_counts().head(8)
    print("top openings after C:", openers.to_dict())

    sample = pd.concat([g.sample(15, random_state=SAMPLE_SEED) for _, g in df.groupby("label")])
    sample = sample.sample(frac=1, random_state=SAMPLE_SEED)
    lines = ["# Leitura de 30 pares do lote FA (15 por rótulo, semente 2026)", "",
             "Sorteio de `analise_lote_fa.py`. Texto = justificativa depois da limpeza C. Leitura do Claude em "
             "`analise-lote-FA.md`.", ""]
    for i, r in enumerate(sample.itertuples(index=False), 1):
        lines += [f"## {i}. idx {r.idx} · {r.label}", "", f"- **P:** {r.sentence1}", f"- **H:** {r.sentence2}",
                  f"- **FA:** {r.clean}", ""]
    (RTE_35B / "leitura-30-FA.md").write_text("\n".join(lines), encoding="utf-8")
    print("flagged entailment+negation idx:", ent[ent.has_negation].idx.tolist()[:40])
    print("flagged not_entailment w/o negation idx:", non[~non.has_negation].idx.tolist()[:40])


if __name__ == "__main__":
    main()
