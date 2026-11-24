"""Mark loss on other layers (plan docs/2026-11-10-plano-teste-fora-da-distribuicao.md, section 10.2, written before
this ran; Pedro's ablation, 16/11): does pulling the [CLS] attention onto the words the rationale copies in layer 1,
2 or 3, or in a combination of layers, change the classification of BERT small?

Same split and training as medir_destaque.py --pares 2000. Arms: no marks; real marks and random marks (same count)
on each layer set of rte_intervencao.layer_sets (each layer, each pair, all four); with several layers the loss is the
sum of each layer's mark loss. Per trained model: classification ROC-AUC on the RTE dev and on the held pairs.

`--tarefa esnli` (Pedro, 16/11) runs the same arms on e-SNLI: the 4,000 train pairs of esnli_dados with the 35B F
rationales, 3 labels, graded on the e-SNLI dev (ROC-AUC one-vs-rest and accuracy); there is no held set.

One row is appended per trained model and a rerun skips the rows already there, so a dropped run resumes.

Usage:  uv run --frozen python resultados/rte-pequenos/medir_camadas.py [--fumaca] [--pares 2000] [--tarefa esnli]
"""
import argparse
import time
from pathlib import Path

import pandas as pd
import torch

from radibert import esnli_dados as esnli
from radibert import rte_dados as dados
from radibert import rte_gradientes as grads
from radibert import rte_intervencao as intervencao
from radibert import rte_marcas as marcas
from radibert import rte_treino as treino
from radibert.rte_modelo import RationaleBert, classifier_only

HERE = Path(__file__).parent
N_TRAIN, SEEDS = 2000, 5
KINDS = ("real", "random")


def label(layers: tuple[int, ...]) -> str:
    return "+".join(str(k + 1) for k in layers)


def rte_sets(n_train: int, smoke: bool, tok) -> tuple:
    """Train items, the mark table and the graded sets: the RTE dev and the train pairs never trained on."""
    pairs = dados.training_pairs()
    table = marcas.mark_table(pairs, tok, grads.expression_pattern(grads.expression_table(pairs)))
    shuffled = pairs.sample(frac=1, random_state=0)  # the split of rte_treino.load_data(held_out=True)
    held_pairs = shuffled.iloc[max(n_train, treino.HELD_OUT_FROM):]
    held_pairs = held_pairs.iloc[:64] if smoke else held_pairs
    dev_pairs = dados.dev_pairs()
    graded = {"dev": (dados.encode(dev_pairs, tok), dev_pairs["y"].to_numpy()),
              "held": (dados.encode(held_pairs.drop(columns="rationale"), tok), held_pairs["y"].to_numpy())}
    return dados.encode(shuffled.iloc[:n_train], tok), table, graded


def esnli_sets(smoke: bool, tok) -> tuple:
    """The same for e-SNLI: every train pair of esnli_dados trains, the e-SNLI dev grades."""
    pairs, dev_pairs = esnli.training_pairs(), esnli.dev_pairs()
    if smoke:
        pairs, dev_pairs = pairs.iloc[:48], dev_pairs.iloc[:64]
    table = marcas.mark_table(pairs, tok, grads.expression_pattern(grads.expression_table(pairs, esnli.LABELS)))
    return dados.encode(pairs, tok), table, {"dev": (dados.encode(dev_pairs, tok), dev_pairs["y"].to_numpy())}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fumaca", action="store_true", help="CPU, 48 train pairs, 64 graded, 1 seed, tiny BERT")
    parser.add_argument("--pares", type=int, default=N_TRAIN, help="RTE only; e-SNLI trains on all its 4,000 pairs")
    parser.add_argument("--tarefa", choices=("rte", "esnli"), default="rte")
    parser.add_argument("--max-treinos", type=int, help="stop after this many new trainings (a rerun goes on)")
    args = parser.parse_args()
    name = dados.TINY if args.fumaca else dados.SMALL
    seeds = 1 if args.fumaca else SEEDS
    device = torch.device("cuda" if torch.cuda.is_available() and not args.fumaca else "cpu")
    tok = dados.load_tokenizers(dados.BERT)
    if args.tarefa == "esnli":
        labels, measures = esnli.LABELS, ("roc_auc", "accuracy")
        train, table, graded = esnli_sets(args.fumaca, tok)
        out = HERE / f"camadas-esnli-{'fumaca' if args.fumaca else len(train)}.csv"
    else:
        labels, measures = grads.RTE_LABELS, ("roc_auc",)
        n_train = 48 if args.fumaca else args.pares
        train, table, graded = rte_sets(n_train, args.fumaca, tok)
        out = HERE / f"camadas-{'fumaca' if args.fumaca else n_train}.csv"
    plan = treino.make_plan(len(train), "prop")
    trained_ids = {item["idx"] for item in train}
    marked = table[table["idx"].isin(trained_ids)]
    print(f"{args.tarefa}: {len(train)} pares de treino, {(marked['real'].map(len) == 0).sum()} sem marca, "
          f"{marked['real'].map(len).sum() / marked['n_tokens'].sum():.1%} dos tokens marcados", flush=True)
    n_layers = 2 if args.fumaca else 4  # tiny has 2 layers, small has 4
    arms = [("none", (n_layers - 1,))] + [(kind, layers) for layers in intervencao.layer_sets(n_layers)
                                          for kind in KINDS]
    done = set()
    if out.exists():
        seen = pd.read_csv(out, dtype={"layers": str})
        done = set(zip(seen["kind"], seen["layers"], seen["seed"]))
    trained = 0
    for kind, layers in arms:
        for seed in range(1, seeds + 1):
            key = (kind, "-" if kind == "none" else label(layers), seed)
            if key in done:
                continue
            if args.max_treinos is not None and trained >= args.max_treinos:
                print(f"parado em {trained} treinos novos (--max-treinos)", flush=True)
                return
            trained += 1
            start = time.perf_counter()
            torch.manual_seed(seed)
            model = RationaleBert.with_mark_attention(name, n_labels=len(labels), layers=layers)
            if len(model.bert.encoder.layer) != n_layers:
                raise RuntimeError(f"{name} has {len(model.bert.encoder.layer)} layers, expected {n_layers}")
            treino.train(model, plan, train if kind == "none" else marcas.with_marks(train, table, kind), seed,
                         device)
            classifier = classifier_only(model)
            row = {"kind": key[0], "layers": key[1], "seed": seed}
            for split, (items, y) in graded.items():
                scores = treino.metrics(y, treino.predict(classifier, items, device), labels)
                row |= {f"{split}_{measure}": scores[measure] for measure in measures}
            row["seconds"] = round(time.perf_counter() - start)
            treino.append_csv(out, [row])
            shown = " ".join(f"{k} {v:.3f}" for k, v in row.items() if k.endswith(measures))
            print(f"{key[0]} camadas {key[1]} seed {seed}: {shown} ({row['seconds']} s)", flush=True)
    print(f"completo {out}", flush=True)


if __name__ == "__main__":
    main()
