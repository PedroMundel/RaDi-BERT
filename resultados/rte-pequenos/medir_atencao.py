"""Redundancy measure (10/11): does BERT small, trained on RTE with no marks, already put its [CLS] attention on the
words the rationale copies? Explains (or not) why the real marks tie with plain training (leitura-grade.md).

Not a new attempt at a gain: nothing here is compared on accuracy. Same split as `--pares 1000`: the first 1,000
pairs of the fixed shuffle train, the 1,470 after them are never trained on. For each arm (no marks, real marks,
random marks) and seed, and for the model before any training, the mean over pairs of the [CLS] attention mass
(mean over heads) on the real-marked positions, on the random-marked positions and what uniform attention would
give, per layer, on the train pairs and on the pairs never trained on.

Usage:  uv run --frozen python resultados/rte-pequenos/medir_atencao.py [--fumaca]
"""
import argparse
from pathlib import Path

import pandas as pd
import torch
from torch.utils.data import DataLoader

from radibert import rte_dados as dados
from radibert import rte_gradientes as grads
from radibert import rte_marcas as marcas
from radibert import rte_treino as treino
from radibert.rte_modelo import RationaleBert, run_encoder

OUT = Path(__file__).with_name("atencao.csv")
N_TRAIN, SEEDS = 1000, 5
KINDS = ("real", "random")


@torch.no_grad()
def cls_mass(model: RationaleBert, items: list[dict], device: torch.device) -> torch.Tensor:
    """(layers, pairs): [CLS] attention mass on each pair's marked positions, mean over heads, in fp32."""
    model.eval()
    per_batch = []
    for batch in DataLoader(items, batch_size=treino.BATCH_SIZE, collate_fn=dados.collate):
        batch = treino.to_device(batch, device)
        attentions = run_encoder(model.bert, batch, output_attentions=True).attentions
        per_batch.append(torch.stack([(a[:, :, 0, :].float().mean(1) * batch["marks"]).sum(1) for a in attentions]))
    return torch.cat(per_batch, dim=1).cpu()


def rows_for(model, arm: str, seed: int, sets: dict, table: pd.DataFrame, device) -> list[dict]:
    rows = []
    n_marks, n_tokens = dict(zip(table["idx"], table["real"].map(len))), dict(zip(table["idx"], table["n_tokens"]))
    for split, items in sets.items():
        marked = torch.tensor([n_marks[it["idx"]] > 0 for it in items])
        uniform = torch.tensor([n_marks[it["idx"]] / n_tokens[it["idx"]] for it in items])[marked].mean().item()
        mass = {kind: cls_mass(model, marcas.with_marks(items, table, kind), device)[:, marked].mean(1)
                for kind in KINDS}
        for layer in range(len(mass["real"])):
            rows.append({"arm": arm, "seed": seed, "split": split, "layer": layer + 1,
                         "mass_real": mass["real"][layer].item(), "mass_random": mass["random"][layer].item(),
                         "uniform": uniform, "n_pairs": int(marked.sum())})
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fumaca", action="store_true", help="CPU, 48 train pairs, 64 held, 1 seed, tiny BERT")
    args = parser.parse_args()
    name = dados.TINY if args.fumaca else dados.SMALL
    n_train, seeds = (48, 1) if args.fumaca else (N_TRAIN, SEEDS)
    device = torch.device("cuda" if torch.cuda.is_available() and not args.fumaca else "cpu")
    tok = dados.load_tokenizers(dados.BERT)
    pairs = dados.training_pairs()
    label_expr = grads.expression_pattern(grads.expression_table(pairs))
    table = marcas.mark_table(pairs, tok, label_expr)
    shuffled = pairs.sample(frac=1, random_state=0)  # the split of rte_treino.load_data(held_out=True)
    held_pairs = shuffled.iloc[treino.HELD_OUT_FROM:]
    sets = {"train": dados.encode(shuffled.iloc[:n_train], tok),
            "held": dados.encode((held_pairs.iloc[:64] if args.fumaca else held_pairs).drop(columns="rationale"), tok)}
    plan = treino.make_plan(n_train, "prop")

    untrained = treino.place(RationaleBert.with_mark_attention(name), device)
    rows = rows_for(untrained, "untrained", 0, sets, table, device)
    for arm in treino.MARK_ARMS:
        for seed in range(1, seeds + 1):
            torch.manual_seed(seed)
            model = RationaleBert.with_mark_attention(name)
            kind = arm.removeprefix("marks_")
            items = sets["train"] if kind == "none" else marcas.with_marks(sets["train"], table, kind)
            treino.train(model, plan, items, seed, device)
            rows += rows_for(model, arm, seed, sets, table, device)
            print(f"{arm} seed {seed}: ok", flush=True)
    out = OUT.with_name("atencao-fumaca.csv") if args.fumaca else OUT
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f"gravado {out} ({len(rows)} linhas)", flush=True)


if __name__ == "__main__":
    main()
