"""Candidate few-shot examples for prompt variant E: 12 e-SNLI dev pairs (4 per label) for Pedro to pick 6.

Pairs come from the dev set but outside the 1,000-pair Claude pilot sample, so an example never shows up as a test pair
in any pilot. Only pairs whose hypothesis adds at least two content words to the premise are kept: those need a bridge
of knowledge, which is the shape the examples should teach. Each candidate gets the 3 human explanations plus Qwen
with prompts A and D.

Needs llama-server running (see piloto_qwen.py). Output: candidatos-exemplos.md + candidatos-exemplos.csv
"""
import re

import pandas as pd

from radibert.paths import ESNLI_DEV, PILOTO_QWEN
from radibert.piloto_qwen import CLAUDE_PILOT, SEED, ask_qwen, prompt_for

CSV_DEV = ESNLI_DEV
OUT_CSV = PILOTO_QWEN / "candidatos-exemplos.csv"
OUT_MD = PILOTO_QWEN / "candidatos-exemplos.md"
N_PER_LABEL = 4
STOP = set("a an the is are was were be of in on at to for with and or his her their its it this that there "
           "some two one three while by from".split())


def content_words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z]+", str(text).lower()) if w not in STOP and len(w) > 2}


def needs_bridge(row) -> bool:
    return len(content_words(row.Sentence2) - content_words(row.Sentence1)) >= 2


def build_candidates() -> pd.DataFrame:
    dev = pd.read_csv(CSV_DEV)
    used = set(pd.read_csv(CLAUDE_PILOT)["pairID"])
    pool = dev[~dev["pairID"].isin(used) & dev["gold_label"].isin(["entailment", "neutral", "contradiction"])]
    pool = pool[pool.apply(needs_bridge, axis=1)]
    return pd.concat([pool[pool["gold_label"] == lab].sample(N_PER_LABEL, random_state=SEED)
                      for lab in ("entailment", "neutral", "contradiction")])


def main():
    cands = build_candidates()
    for variant in ("A", "D"):
        cands[f"qwen_{variant}"] = [ask_qwen(prompt_for(row, variant))["qwen"] for _, row in cands.iterrows()]
    cands.to_csv(OUT_CSV, index=False)

    lines = ["# Candidatos a exemplo para a variante E (escolha 6: 2 por rótulo)", "",
             "12 pares do dev do e-SNLI fora da amostra do piloto do Claude, só pares em que a hipótese acrescenta",
             "ao menos duas palavras de conteúdo (pedem ponte de conhecimento). Para cada um: as 3 humanas e o Qwen",
             "com os prompts A e D. Marque os 6 e escreva a versão final na linha **Sua versão**. Ela pode ser uma",
             "das de cima, editada ou nova. Forma de referência (Wiegreffe 2022, Tab. 2): 1–2 frases, ~10–25",
             "palavras, a ponte de conhecimento, sem nomear o rótulo.", ""]
    for n, (_, r) in enumerate(cands.iterrows(), 1):
        lines += [f"## {n}. {r.gold_label} · `{r.pairID}`", "",
                  f"- **P:** {r.Sentence1}", f"- **H:** {r.Sentence2}", "",
                  "| Fonte | Justificativa |", "|---|---|",
                  f"| Humano 1 | {r.Explanation_1} |", f"| Humano 2 | {r.Explanation_2} |",
                  f"| Humano 3 | {r.Explanation_3} |", f"| Qwen A | {r.qwen_A} |", f"| Qwen D | {r.qwen_D} |", "",
                  "- [ ] escolher", "- **Sua versão:** ", ""]
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"{OUT_MD}\n{OUT_CSV}")


if __name__ == "__main__":
    main()
