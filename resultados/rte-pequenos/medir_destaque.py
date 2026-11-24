"""Highlight test (10/11; criterion in docs/2026-11-10-plano-teste-fora-da-distribuicao.md, section 8, written before
this ran): do the tokens BERT small's [CLS] attends to most, after training with the real marks, match the words the
LLM rationale copies, on pairs never trained on, and better than a rule with no training?

Same split and training as medir_atencao.py. Per pair with a mark: average precision and ROC-AUC of the token scores
against the real marks, over the pair's own tokens ([CLS] and [SEP] are never marks); then the mean over pairs.

`--pares N` (default 1,000) trains on the first N pairs and measures on the pairs after max(N, 1,000); with another
N the output is destaque-N.csv. Every trained model also gets its classification ROC-AUC on the RTE dev and on the
held pairs, and seed 1 of the real and no-mark arms dumps the token scores of the first EXAMPLES held pairs
(destaque-exemplos-N.json, read by pagina_destaque.py).

Usage:  uv run --frozen python resultados/rte-pequenos/medir_destaque.py [--fumaca] [--pares 2000]
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import average_precision_score, roc_auc_score
from torch.utils.data import DataLoader

from radibert import rte_dados as dados
from radibert import rte_gradientes as grads
from radibert import rte_marcas as marcas
from radibert import rte_treino as treino
from radibert.rte_modelo import RationaleBert, classifier_only, run_encoder

HERE = Path(__file__).parent
N_TRAIN, SEEDS = 1000, 5
RULE_SEED = 0
EXAMPLES = 20


def classification(model: RationaleBert, sets: dict, device: torch.device) -> dict:
    """ROC-AUC of the trained classifier on each (items, y) set."""
    classifier = classifier_only(model)
    return {f"{name}_roc_auc": treino.metrics(y, treino.predict(classifier, items, device))["roc_auc"]
            for name, (items, y) in sets.items()}


@torch.no_grad()
def attention_scores(model: RationaleBert, items: list[dict], device: torch.device) -> list[np.ndarray]:
    """Per pair, the last layer's [CLS] attention (mean over heads) on each input position, in fp32."""
    model.eval()
    out = []
    for batch in DataLoader(items, batch_size=treino.BATCH_SIZE, collate_fn=dados.collate):
        batch = treino.to_device(batch, device)
        attention = run_encoder(model.bert, batch, output_attentions=True).attentions[-1][:, :, 0, :].float().mean(1)
        out += [row[:n].cpu().numpy() for row, n in zip(attention, batch["attention_mask"].sum(1).tolist())]
    return out


@torch.no_grad()
def head_scores(model: RationaleBert, items: list[dict], device: torch.device) -> list[np.ndarray]:
    """Per pair, the token head's probability of a mark on each input position."""
    model.eval()
    out = []
    for batch in DataLoader(items, batch_size=treino.BATCH_SIZE, collate_fn=dados.collate):
        batch = treino.to_device(batch, device)
        probs = torch.sigmoid(model.token_logits(model.encode(batch)[0]))
        out += [row[:n].cpu().numpy() for row, n in zip(probs, batch["attention_mask"].sum(1).tolist())]
    return out


def is_content(word: str) -> bool:
    """The marks' own definition of a word that can be marked (rte_gradientes.word_groups, group F excluded)."""
    return not ((len(word) == 1 and not word.isdigit()) or word in grads.DROP or word in grads.SOURCE_WORDS)


def rule_scores(premise: str, hypothesis: str, bert_tok, rng: np.random.Generator) -> dict[str, np.ndarray]:
    """Token scores of the rules with no training, on the same positions as the model's input."""
    enc = bert_tok(premise, hypothesis, return_offsets_mapping=True, truncation="only_first",
                   max_length=dados.MAX_INPUT_TOKENS)
    texts = (premise, hypothesis)
    spans = [[(m.start(), m.end(), m.group().lower()) for m in grads.WORD.finditer(text)] for text in texts]
    vocab = [set(grads.words_of(text)) for text in texts]
    n = len(enc["input_ids"])
    scores = {name: np.zeros(n) for name in ("content", "content_hypothesis", "content_both")}
    for pos, ((a, b), seq) in enumerate(zip(enc["offset_mapping"], enc.sequence_ids())):
        if seq is None:
            continue
        words = [word for start, end, word in spans[seq] if start < b and a < end and is_content(word)]
        if words:
            scores["content"][pos] = 1
            scores["content_hypothesis"][pos] = float(seq == 1)
            scores["content_both"][pos] = float(any(w in vocab[1 - seq] for w in words))
    return scores | {"random": rng.random(n)}


def pair_metrics(scores: list[np.ndarray], items: list[dict], marks: dict, special: set) -> dict:
    """Mean over the pairs with a mark of the per-pair AP and ROC-AUC, on the pair's own tokens."""
    ap, auc = [], []
    for score, item in zip(scores, items):
        keep = np.array([i not in special for i in item["input_ids"]])
        truth = np.zeros(len(item["input_ids"]), dtype=int)
        truth[marks[item["idx"]]] = 1
        truth, score = truth[keep], score[keep]
        if truth.sum() == 0 or truth.sum() == len(truth):
            continue
        ap.append(average_precision_score(truth, score))
        auc.append(roc_auc_score(truth, score))
    return {"ap": float(np.mean(ap)), "auroc": float(np.mean(auc)), "n_pairs": len(ap)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fumaca", action="store_true", help="CPU, 48 train pairs, 64 held, 1 seed, tiny BERT")
    parser.add_argument("--pares", type=int, default=N_TRAIN)
    parser.add_argument("--cabeca", action="store_true",
                        help="adds the token-head arm (plan, section 9); the output gets the suffix -cabeca")
    args = parser.parse_args()
    name = dados.TINY if args.fumaca else dados.SMALL
    n_train, seeds = (48, 1) if args.fumaca else (args.pares, SEEDS)
    device = torch.device("cuda" if torch.cuda.is_available() and not args.fumaca else "cpu")
    tok = dados.load_tokenizers(dados.BERT)
    pairs = dados.training_pairs()
    label_expr = grads.expression_pattern(grads.expression_table(pairs))
    table = marcas.mark_table(pairs, tok, label_expr)
    marks = dict(zip(table["idx"], table["real"]))
    special = {tok.bert.cls_token_id, tok.bert.sep_token_id}
    shuffled = pairs.sample(frac=1, random_state=0)  # the split of rte_treino.load_data(held_out=True)
    held_pairs = shuffled.iloc[max(n_train, treino.HELD_OUT_FROM):]
    held_pairs = held_pairs.iloc[:64] if args.fumaca else held_pairs
    train = dados.encode(shuffled.iloc[:n_train], tok)
    held = dados.encode(held_pairs.drop(columns="rationale"), tok)
    dev_pairs = dados.dev_pairs()
    graded = {"dev": (dados.encode(dev_pairs, tok), dev_pairs["y"].to_numpy()),
              "held": (held, held_pairs["y"].to_numpy())}
    plan = treino.make_plan(n_train, "prop")
    shown = held_pairs.iloc[:EXAMPLES]
    examples = [{"idx": int(i), "y": int(y), "premise": p, "hypothesis": h, "rationale": r,
                 "tokens": tok.bert.convert_ids_to_tokens(item["input_ids"]), "marks": marks[int(i)], "scores": {}}
                for i, y, p, h, r, item in zip(shown["idx"], shown["y"], shown["sentence1"], shown["sentence2"],
                                               shown["rationale"], held)]

    rng = np.random.default_rng(RULE_SEED)
    per_pair = [rule_scores(p, h, tok.bert, rng) for p, h in zip(held_pairs["sentence1"], held_pairs["sentence2"])]
    rows = [{"method": f"rule_{rule}", "seed": 0} | pair_metrics([s[rule] for s in per_pair], held, marks, special)
            for rule in per_pair[0]]
    untrained = treino.place(RationaleBert.with_mark_attention(name), device)
    rows.append({"method": "untrained", "seed": 0} | pair_metrics(attention_scores(untrained, held, device), held,
                                                                 marks, special))
    for arm in treino.MARK_ARMS + (("token_head",) if args.cabeca else ()):
        for seed in range(1, seeds + 1):
            torch.manual_seed(seed)
            if arm == "token_head":  # learns the real marks directly, one logit per token
                kind, model = "head", RationaleBert.with_token_head(name)
                treino.train(model, plan, marcas.with_marks(train, table, "real"), seed, device)
                scores = head_scores(model, held, device)
            else:
                kind, model = arm.removeprefix("marks_"), RationaleBert.with_mark_attention(name)
                treino.train(model, plan, train if kind == "none" else marcas.with_marks(train, table, kind), seed,
                             device)
                scores = attention_scores(model, held, device)
            rows.append({"method": arm, "seed": seed} | pair_metrics(scores, held, marks, special)
                        | classification(model, graded, device))
            if seed == 1 and kind != "random":
                for example, score in zip(examples, scores):
                    example["scores"][kind] = [round(float(s), 5) for s in score]
            print(f"{arm} seed {seed}: ap {rows[-1]['ap']:.3f} dev {rows[-1]['dev_roc_auc']:.3f}", flush=True)
    tag = ("fumaca" if args.fumaca else str(n_train)) + ("-cabeca" if args.cabeca else "")
    out = HERE / ("destaque.csv" if tag == str(N_TRAIN) else f"destaque-{tag}.csv")
    pd.DataFrame(rows).to_csv(out, index=False)
    (HERE / f"destaque-exemplos-{tag}.json").write_text(json.dumps(examples, ensure_ascii=False), encoding="utf-8")
    print(f"gravado {out} ({len(rows)} linhas)", flush=True)


if __name__ == "__main__":
    main()
