"""Attention intervention, no new training recipe (plan docs/2026-11-10-plano-teste-fora-da-distribuicao.md, section
10.1, written before this ran): in which layers does the [CLS] attention to the words the rationale copies weigh on
the decision of BERT small?

Same split and training as medir_destaque.py --pares 2000. For each trained model (no marks; real marks on the last
layer) and seed, the held pairs that have a mark are predicted once untouched and then once per combination of
  layers     each layer, each pair of layers, all four
  operation  block (cannot look at the set) / only (can look at nothing but the set and [CLS])
  set        real marks / random positions (same count) / two draws among content words (same count)
  rows       the [CLS] row / every row
Per combination: the share of pairs whose predicted class changes, the mean drop in the probability of the class the
untouched model chose, and the classification ROC-AUC.

Usage:  uv run --frozen python resultados/rte-pequenos/medir_intervencao.py [--fumaca] [--pares 2000]
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from torch.utils.data import DataLoader

from radibert import rte_dados as dados
from radibert import rte_gradientes as grads
from radibert import rte_intervencao as intervencao
from radibert import rte_marcas as marcas
from radibert import rte_treino as treino
from radibert.rte_modelo import RationaleBert

HERE = Path(__file__).parent
N_TRAIN, SEEDS = 2000, 5
ARMS = ("marks_none", "marks_real")
SETS = ("real", "random", "content_a", "content_b")
DRAW_SEEDS = {"content_a": 1, "content_b": 2}


def with_content_draws(table: pd.DataFrame, pairs: pd.DataFrame, bert_tok) -> pd.DataFrame:
    """The mark table plus two independent draws among each pair's content positions, as many as its real marks."""
    candidates = [intervencao.content_positions(p, h, bert_tok)
                  for p, h in zip(pairs["sentence1"], pairs["sentence2"])]
    table = table.copy()
    for name, seed in DRAW_SEEDS.items():
        generator = torch.Generator().manual_seed(seed)
        table[name] = [intervencao.content_draw(len(real), cand, generator)
                       for real, cand in zip(table["real"], candidates)]
    return table


@torch.no_grad()
def probabilities(model: RationaleBert, items: list[dict], device, layers=(), operation="block",
                  cls_only=True) -> np.ndarray:
    """P(entailment) per pair, with the items' `marks` as the set the attention is cut on in `layers`."""
    model.eval()
    out = []
    for batch in DataLoader(items, batch_size=treino.BATCH_SIZE, collate_fn=dados.collate):
        batch = treino.to_device(batch, device)
        forbidden = intervencao.forbidden_positions(batch["marks"], batch["attention_mask"], operation)
        with intervencao.restricted_attention(model.bert, layers, forbidden, cls_only), treino.autocast(device):
            out.append(torch.sigmoid(model.encode(batch)[1].float()).cpu())
    return torch.cat(out).numpy()


def effect(base: np.ndarray, cut: np.ndarray, y: np.ndarray) -> dict:
    chose = base >= 0.5
    confidence = lambda p: np.where(chose, p, 1 - p)  # probability of the class the untouched model chose
    return {"flip": float(((cut >= 0.5) != chose).mean()),
            "drop": float((confidence(base) - confidence(cut)).mean()),
            "roc_auc": treino.metrics(y, cut)["roc_auc"]}


def rows_for(model, arm: str, seed: int, held: list[dict], y: np.ndarray, table: pd.DataFrame, device) -> list[dict]:
    items = {name: marcas.with_marks(held, table, name) for name in SETS}
    base = probabilities(model, items["real"], device)
    head = {"arm": arm, "seed": seed, "n_pairs": len(held), "base_roc_auc": treino.metrics(y, base)["roc_auc"]}
    rows = []
    for layers in intervencao.layer_sets(len(model.bert.encoder.layer)):
        for operation in intervencao.OPERATIONS:
            for cls_only in (True, False):
                for name in SETS:
                    cut = probabilities(model, items[name], device, layers, operation, cls_only)
                    rows.append(head | {"layers": "+".join(str(k + 1) for k in layers), "operation": operation,
                                        "rows": "cls" if cls_only else "all", "set": name} | effect(base, cut, y))
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fumaca", action="store_true", help="CPU, 48 train pairs, 64 held, 1 seed, tiny BERT")
    parser.add_argument("--pares", type=int, default=N_TRAIN)
    args = parser.parse_args()
    name = dados.TINY if args.fumaca else dados.SMALL
    n_train, seeds = (48, 1) if args.fumaca else (args.pares, SEEDS)
    device = torch.device("cuda" if torch.cuda.is_available() and not args.fumaca else "cpu")
    tok = dados.load_tokenizers(dados.BERT)
    pairs = dados.training_pairs()
    label_expr = grads.expression_pattern(grads.expression_table(pairs))
    table = with_content_draws(marcas.mark_table(pairs, tok, label_expr), pairs, tok.bert)
    n_marks = dict(zip(table["idx"], table["real"].map(len)))
    shuffled = pairs.sample(frac=1, random_state=0)  # the split of rte_treino.load_data(held_out=True)
    held_pairs = shuffled.iloc[max(n_train, treino.HELD_OUT_FROM):]
    held_pairs = held_pairs.iloc[:64] if args.fumaca else held_pairs
    held_pairs = held_pairs[[n_marks[int(i)] > 0 for i in held_pairs["idx"]]]  # only pairs with a mark are measured
    train = dados.encode(shuffled.iloc[:n_train], tok)
    held = dados.encode(held_pairs.drop(columns="rationale"), tok)
    y = held_pairs["y"].to_numpy()
    plan = treino.make_plan(n_train, "prop")
    measured = table[table["idx"].isin(held_pairs["idx"])]
    for draw in DRAW_SEEDS:
        shared = np.mean([len(set(r) & set(c)) / len(r) for r, c in zip(measured["real"], measured[draw])])
        print(f"{draw}: {shared:.3f} das posições coincidem com a marca real", flush=True)

    rows = []
    for arm in ARMS:
        for seed in range(1, seeds + 1):
            torch.manual_seed(seed)
            kind, model = arm.removeprefix("marks_"), RationaleBert.with_mark_attention(name)
            treino.train(model, plan, train if kind == "none" else marcas.with_marks(train, table, kind), seed,
                         device)
            rows += rows_for(model, arm, seed, held, y, table, device)
            print(f"{arm} seed {seed}: base {rows[-1]['base_roc_auc']:.3f}, {len(held)} pares", flush=True)
    tag = "fumaca" if args.fumaca else str(n_train)
    out = HERE / f"intervencao-{tag}.csv"
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f"gravado {out} ({len(rows)} linhas)", flush=True)


if __name__ == "__main__":
    main()
