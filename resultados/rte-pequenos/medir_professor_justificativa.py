"""A teacher that reads the rationale: the two cheap tests before any distillation (design and reading rules in
docs/2026-11-18-professor-que-le-a-justificativa.md, written before this was coded; Pedro, 18/11).

Test (a). BERT base teachers on the 4,000 e-SNLI pairs no student trains on, 3 seeds each:
  pair             premise and hypothesis (today's teacher, trained again on this machine)
  pair_rationale   premise, hypothesis and that pair's Qwen rationale
  rationale        the rationale alone
Graded on the student's own train pairs (they decide) and on the choice pairs (they confirm): no teacher trains on
either. The e-SNLI dev has no rationale, so it is out. `pair_rationale` is also graded with the rationale swapped at
test time: for another pair's of the same label, and for one of another label (then `follows` is the share of pairs
where its answer is the label the swapped rationale came from).

Test (b), no extra training: `pair_rationale` of seed 1 reads each choice pair three times (its own rationale, the
same-label swap, the other-label swap). On the pair's positions only, at four evenly spaced layers, 1 - cosine
between the vector with the right rationale and with the swapped one, and how much of those positions' attention
goes to the rationale. Layer 0 (the embeddings' output) must give 0. That teacher's weights are saved next to this
script (not in git): the teacher measured is the one a distillation would use.

One row is appended per trained teacher and a rerun skips the rows already there.

Usage:  uv run --frozen python resultados/rte-pequenos/medir_professor_justificativa.py [--fumaca]
"""
import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F

from radibert import esnli_dados as esnli
from radibert import rte_dados as dados
from radibert import rte_treino as treino
from radibert.rte_modelo import Classifier, RationaleBert, classifier_only, run_encoder

HERE = Path(__file__).parent
SEEDS, SWAP_SEED, INTERIOR_SEED, INTERIOR_LAYERS = 3, 0, 1, 4
READS = {"pair": lambda pairs: pairs,
         "pair_rationale": esnli.rationale_in_input,
         "rationale": lambda pairs: esnli.rationale_in_input(pairs, alone=True)}
GRADED = ("student", "choice")
SWAPS = ("same", "other")


def accuracy(probs: np.ndarray, y) -> float:
    return float((probs.argmax(1) == np.asarray(y)).mean())


def swapped_scores(teacher: Classifier, pairs: pd.DataFrame, tok: dados.Tokenizers, device) -> dict:
    """`pair_rationale` graded with the rationale swapped at test time (the pairs and their gold labels stay)."""
    same = dados.shuffle_within_label(pairs, SWAP_SEED)
    other = esnli.rationale_of_other_label(pairs, SWAP_SEED)
    scores = {}
    for name, swapped in (("same", same), ("other", other)):
        probs = treino.predict(teacher, dados.encode(esnli.rationale_in_input(swapped), tok), device)
        scores[f"{name}_accuracy"] = accuracy(probs, pairs["y"])
    scores["other_follows"] = accuracy(probs, other["rationale_y"])
    return scores


def pair_rows(lengths: torch.Tensor, width: int) -> torch.Tensor:
    """1 on each pair's own positions after [CLS] (its tokens and two separators), 0 elsewhere: (pairs, width)."""
    positions = torch.arange(width, device=lengths.device)[None]
    return ((positions >= 1) & (positions < lengths[:, None])).float()


@torch.no_grad()
def interior(teacher: Classifier, pairs: pd.DataFrame, tok: dados.Tokenizers, device) -> pd.DataFrame:
    """Test (b): one row per layer and place ("pair" positions or "cls"), means over the pairs."""
    teacher.to(device).eval()
    n_layers = len(teacher.bert.encoder.layer)
    layers = [0] + [n_layers * k // INTERIOR_LAYERS for k in range(1, INTERIOR_LAYERS + 1)]
    frames = {"real": pairs, "same": dados.shuffle_within_label(pairs, SWAP_SEED),
              "other": esnli.rationale_of_other_label(pairs, SWAP_SEED)}
    items = {name: dados.encode(esnli.rationale_in_input(frame), tok) for name, frame in frames.items()}
    lengths = [len(item["input_ids"]) for item in dados.encode(READS["pair"](pairs), tok)]
    sums = {(layer, place): np.zeros(len(SWAPS) + 1) for layer in layers for place in ("pair", "cls")}
    for start in range(0, len(pairs), treino.BATCH_SIZE):
        chunk = slice(start, start + treino.BATCH_SIZE)
        n = torch.tensor(lengths[chunk], device=device)
        out = {}
        for name in frames:
            batch = treino.to_device(dados.collate(items[name][chunk]), device)
            with treino.autocast(device):
                out[name] = run_encoder(teacher.bert, batch, output_attentions=name == "real",
                                        output_hidden_states=True)
        width = int(n.max())
        rows = pair_rows(n, width)
        for layer in layers:
            real = out["real"].hidden_states[layer][:, :width].float()
            values = {"pair": [], "cls": []}
            for swap in SWAPS:
                distance = 1 - F.cosine_similarity(real, out[swap].hidden_states[layer][:, :width].float(), dim=-1)
                values["pair"].append((distance * rows).sum(1) / rows.sum(1))
                values["cls"].append(distance[:, 0])
            if layer:  # attentions[layer - 1] is the attention that produced hidden_states[layer]
                attention = out["real"].attentions[layer - 1].float().mean(1)
                beyond = torch.arange(attention.shape[-1], device=device)[None, None] >= n[:, None, None]
                to_rationale = (attention * beyond).sum(-1)[:, :width]  # padding columns get no attention
                values["pair"].append((to_rationale * rows).sum(1) / rows.sum(1))
                values["cls"].append(to_rationale[:, 0])
            else:
                values["pair"].append(torch.full_like(n, float("nan"), dtype=torch.float))
                values["cls"].append(torch.full_like(n, float("nan"), dtype=torch.float))
            for place, columns in values.items():
                sums[layer, place] += torch.stack(columns, 1).sum(0).cpu().numpy()
    table = [{"layer": layer, "place": place, "distance_same_label": total[0] / len(pairs),
              "distance_other_label": total[1] / len(pairs), "attention_to_rationale": total[2] / len(pairs)}
             for (layer, place), total in sums.items()]
    return pd.DataFrame(table).assign(pairs=len(pairs))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fumaca", action="store_true", help="CPU, 48 pairs per set, 1 seed, BERT small teachers")
    args = parser.parse_args()
    name = dados.SMALL if args.fumaca else dados.BERT
    seeds = range(1, 2) if args.fumaca else range(1, SEEDS + 1)
    device = torch.device("cuda" if torch.cuda.is_available() and not args.fumaca else "cpu")
    tok = dados.load_tokenizers(dados.BERT)
    sets = {"teacher": esnli.other_pairs(), "student": esnli.training_pairs(), "choice": esnli.choice_split()[0]}
    if args.fumaca:
        sets = {split: pairs.iloc[:48] for split, pairs in sets.items()}
    plan = treino.make_plan(len(sets["teacher"]), "prop")
    tag = "fumaca" if args.fumaca else str(len(sets["teacher"]))
    out = HERE / f"professor-justificativa-esnli-{tag}.csv"
    done = set()
    if out.exists():
        seen = pd.read_csv(out)
        done = set(zip(seen["reads"], seen["seed"]))
    for reads, as_input in READS.items():
        items = {split: dados.encode(as_input(pairs), tok) for split, pairs in sets.items()}
        for seed in seeds:
            if (reads, seed) in done:
                continue
            start = time.perf_counter()
            torch.manual_seed(seed)
            model = RationaleBert.with_mark_attention(name, n_labels=len(esnli.LABELS))
            treino.train(model, plan, items["teacher"], seed, device)
            teacher = classifier_only(model)
            del model
            row = {"reads": reads, "seed": seed}
            for split in GRADED:
                probs = treino.predict(teacher, items[split], device)
                row |= {f"{split}_accuracy": accuracy(probs, sets[split]["y"]),
                        f"{split}_confidence": float(probs.max(1).mean())}
                swapped = (swapped_scores(teacher, sets[split], tok, device) if reads == "pair_rationale"
                           else dict.fromkeys(("same_accuracy", "other_accuracy", "other_follows"), float("nan")))
                row |= {f"{split}_{key}": value for key, value in swapped.items()}
            if reads == "pair_rationale" and seed == INTERIOR_SEED:
                # both files are written before the row, so a row in the CSV means they are there
                torch.save(teacher.state_dict(), HERE / f"professor-justificativa-{tag}.pt")
                interior(teacher, sets["choice"], tok, device).to_csv(
                    HERE / f"professor-justificativa-interior-{tag}.csv", index=False)
            row["seconds"] = round(time.perf_counter() - start)
            treino.append_csv(out, [row])
            print(f"{reads} seed {seed}: " + " ".join(f"{k} {v:.3f}" for k, v in row.items() if k.endswith("accuracy"))
                  + f" ({row['seconds']} s)", flush=True)
    print(f"completo {out}", flush=True)


if __name__ == "__main__":
    main()
