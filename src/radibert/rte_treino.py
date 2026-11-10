"""Training loop of the Agrawal replication on RTE: BERT alone vs BERT + T5 decoder (docs/2026-11-09-codigo-treino-rte.md).

Phases (D3, read literally): A = one pass over half the pairs, BERT frozen, decoder only, L_aux; B = the first 30% of the
steps, L_aux only, BERT's rate rising from 0; C = the rest, L_cls + 0.1 L_aux. Rate schedule (E1): every group warms
up linearly and then decays linearly to 0 at the last step (Hugging Face's linear schedule); BERT warms up over phase B,
head and decoder over the Table 4 warmup (500 steps, D2 "copy", or 10% of the steps, "prop"). The dev set is the test
set (GLUE's test has no labels): it is read once, at the end, with no early stopping.

Usage:
    uv run python -m radibert.rte_treino --fumaca                # D6 smoke test on CPU: tiny BERT + bridge + T5 base
    uv run python -m radibert.rte_treino --grade --seeds 5       # both arms x both warmups; skips runs in the CSV
    uv run python -m radibert.rte_treino --arm bert_decoder --warmup prop --seed 1
"""
import argparse
import contextlib
import functools
import math
import subprocess
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from torch.optim.lr_scheduler import LambdaLR
from torch.utils.data import DataLoader

from radibert import rte_dados as dados
from radibert import rte_gradientes as grads
from radibert.paths import RTE_TREINO
from radibert.rte_modelo import RationaleBert, classifier_only

# Table 4 of the paper
LR = 5e-5
BATCH_SIZE, EPOCHS = 32, 8
COPY_WARMUP_STEPS = 500
DECODER_WEIGHT_DECAY = 0.001  # 0 on the encoder; 0 on the head (the paper does not say)
ADAM_EPS, ADAM_BETAS = 1e-8, (0.9, 0.999)
CLIP_NORM = 1.0
# §4.3-4.4 of the paper and the decisions D2/D3
AUX_WEIGHT = 0.1
PHASE_B_SHARE = 0.3
PROPORTIONAL_WARMUP_SHARE = 0.1
# Evaluation (D4)
PRECISION_RECALL_THRESHOLD = 0.7
# Gradient measures
MEASURE_EVERY = 25

ARMS = ("bert", "bert_decoder")
WARMUPS = ("500", "prop")
SMOKE_BERT = "google/bert_uncased_L-2_H-128_A-2"


@dataclass(frozen=True)
class Plan:
    per_epoch: int
    total: int
    phase_a: int
    phase_b: int
    warmup_steps: int  # not "warmup": the results row already has the run's warmup kind ("500"/"prop")


def make_plan(n_pairs: int, warmup: str, batch_size: int = BATCH_SIZE, epochs: int = EPOCHS) -> Plan:
    per_epoch = math.ceil(n_pairs / batch_size)
    total = per_epoch * epochs
    warmup_steps = COPY_WARMUP_STEPS if warmup == "500" else int(PROPORTIONAL_WARMUP_SHARE * total)
    return Plan(per_epoch, total, math.ceil((n_pairs // 2) / batch_size), int(PHASE_B_SHARE * total), warmup_steps)


def linear_schedule(warmup: int, total: int):
    """Hugging Face's get_linear_schedule_with_warmup factor: 0 -> 1 over `warmup` steps, then 1 -> 0 at `total`."""
    def factor(step: int) -> float:
        if step < warmup:
            return step / max(1, warmup)
        return max(0.0, (total - step) / max(1, total - warmup))
    return factor


def param_groups(model: RationaleBert) -> list[dict]:
    """Encoder, head and decoder (+ bridge) as separate groups; the frozen T5 encoder is in none."""
    groups = [{"params": list(model.bert.parameters()), "weight_decay": 0.0},
              {"params": list(model.head.parameters()), "weight_decay": 0.0}]
    if model.t5 is not None:
        decoder = [p for p in model.t5.parameters() if p.requires_grad]
        decoder += list(model.bridge.parameters()) if model.bridge is not None else []
        groups.append({"params": decoder, "weight_decay": DECODER_WEIGHT_DECAY})
    return groups


def lr_factors(model: RationaleBert, plan: Plan) -> list:
    """E1: BERT warms up over phase B when there is a decoder; head and decoder over the Table 4 warmup."""
    table4 = linear_schedule(plan.warmup_steps, plan.total)
    if model.t5 is None:
        return [table4, table4]
    return [linear_schedule(plan.phase_b, plan.total), table4, table4]


def training_loss(step: int, plan: Plan, l_cls: torch.Tensor, l_aux: torch.Tensor | None) -> torch.Tensor:
    if l_aux is None:
        return l_cls
    if step <= plan.phase_b:
        return l_aux  # phase B: the head learns nothing here
    return l_cls + AUX_WEIGHT * l_aux  # phase C (§4.3)


def autocast(device: torch.device):
    if device.type == "cuda":
        return torch.autocast("cuda", dtype=torch.bfloat16)
    return contextlib.nullcontext()


def to_device(batch: dict, device: torch.device) -> dict:
    return {k: v.to(device) for k, v in batch.items()}


def make_optimizer(model: RationaleBert) -> torch.optim.Optimizer:
    return torch.optim.AdamW(param_groups(model), lr=LR, eps=ADAM_EPS, betas=ADAM_BETAS)


def optimizer_step(model: RationaleBert, opt: torch.optim.Optimizer, loss: torch.Tensor):
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), CLIP_NORM)
    opt.step()
    opt.zero_grad()


def run_phase_a(model: RationaleBert, opt: torch.optim.Optimizer, items: list[dict], seed: int, batch_size: int,
                device: torch.device) -> int:
    """One pass over a random half of the pairs: BERT frozen (no graph through it), decoder learns to read it."""
    half = torch.randperm(len(items), generator=torch.Generator().manual_seed(seed))[: len(items) // 2]
    loader = DataLoader([items[i] for i in half], batch_size=batch_size, collate_fn=dados.collate)
    for batch in loader:
        batch = to_device(batch, device)
        with autocast(device):
            with torch.no_grad():
                h, _ = model.encode(batch)
            l_aux = model.decode(h, batch).loss
        optimizer_step(model, opt, l_aux)  # backward outside autocast, as PyTorch recommends
    return len(loader)


@dataclass
class Probes:
    groups: grads.Probe
    words: grads.Probe | None = None


@dataclass
class TrainLog:
    phase_a_steps: int = 0
    last_epoch_aux: list = field(default_factory=list)
    group_rows: list = field(default_factory=list)
    word_rows: list = field(default_factory=list)


def measure(model, probes: Probes | None, plan: Plan, step: int, log: TrainLog, device):
    """Group measure at step 1 and every MEASURE_EVERY steps; word measure at 1, end of phase B and the last step."""
    if probes is None:
        return
    amp = lambda: autocast(device)  # noqa: E731  forward under bf16 like training; gradients outside it
    if step == 1 or step % MEASURE_EVERY == 0:
        log.group_rows.append({"phase": "B" if step <= plan.phase_b else "C"}
                              | grads.measure_groups(model, probes.groups, step, amp))
    if probes.words is not None and step in {1, plan.phase_b, plan.total}:
        log.word_rows += grads.measure_words(model, probes.words, step, amp)


def train(model: RationaleBert, plan: Plan, items: list[dict], seed: int, device: torch.device,
          batch_size: int = BATCH_SIZE, probes: Probes | None = None) -> TrainLog:
    """Trains in place. Same seed, same batch order in both arms (the loader has its own generator). Same seed, same
    weights on CPU (I10); on CUDA the embedding backward uses atomic adds, so reruns differ slightly."""
    model.to(device).train()
    opt = make_optimizer(model)
    log = TrainLog()
    if model.t5 is not None:
        log.phase_a_steps = run_phase_a(model, opt, items, seed, batch_size, device)
        if log.phase_a_steps != plan.phase_a:
            raise RuntimeError(f"phase A ran {log.phase_a_steps} steps, the plan says {plan.phase_a}")
    sched = LambdaLR(opt, lr_factors(model, plan))  # created after phase A: its constant 5e-5 is the base rate
    loader = DataLoader(items, batch_size=batch_size, shuffle=True, collate_fn=dados.collate,
                        generator=torch.Generator().manual_seed(seed))
    step = 0
    for epoch in range(plan.total // plan.per_epoch):
        for batch in loader:
            step += 1
            batch = to_device(batch, device)
            with autocast(device):
                logit, l_aux = model(batch)
                l_cls = F.binary_cross_entropy_with_logits(logit.float(), batch["y"])
                loss = training_loss(step, plan, l_cls, l_aux)
            optimizer_step(model, opt, loss)
            sched.step()
            if l_aux is not None and epoch == plan.total // plan.per_epoch - 1:
                log.last_epoch_aux.append(float(l_aux.detach()))
            if model.t5 is not None:
                measure(model, probes, plan, step, log, device)
    return log


def memory_check(model: RationaleBert, items: list[dict], probe: grads.Probe, device: torch.device,
                 batch_size: int = BATCH_SIZE) -> float:
    """One phase-C step on the longest pairs, then one group measure: the peak GPU memory in GB (0 on CPU). --grade
    runs it first, so an out-of-memory error shows up in seconds instead of hours into the grid (audit 09/11)."""
    model.to(device).train()
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)
    longest = sorted(items, key=lambda it: len(it["input_ids"]), reverse=True)[:batch_size]
    batch = to_device(dados.collate(longest), device)
    with autocast(device):
        logit, l_aux = model(batch)
        loss = F.binary_cross_entropy_with_logits(logit, batch["y"]) + AUX_WEIGHT * l_aux
    optimizer_step(model, make_optimizer(model), loss)
    grads.measure_groups(model, probe.to(device), step=0, amp=lambda: autocast(device))
    return torch.cuda.max_memory_allocated(device) / 2**30 if device.type == "cuda" else 0.0


@torch.no_grad()
def predict(classifier, items: list[dict], device: torch.device) -> np.ndarray:
    classifier.to(device).eval()
    out = []
    for batch in DataLoader(items, batch_size=BATCH_SIZE, collate_fn=dados.collate):
        with autocast(device):
            out.append(torch.sigmoid(classifier(to_device(batch, device)).float()).cpu())
    return torch.cat(out).numpy()


def metrics(y: np.ndarray, p: np.ndarray) -> dict:
    """D4: the paper's ROC-AUC and precision/recall at 0.7, plus accuracy and F1 at 0.5."""
    at_half, at_cut = p >= 0.5, p >= PRECISION_RECALL_THRESHOLD
    f1_each = f1_score(y, at_half, average=None, labels=[1, 0], zero_division=0)
    return {"roc_auc": roc_auc_score(y, p), "accuracy": accuracy_score(y, at_half),
            "f1_macro": f1_score(y, at_half, average="macro", zero_division=0),
            "f1_entailment": f1_each[0], "f1_not_entailment": f1_each[1],
            "precision_at_0_7": precision_score(y, at_cut, zero_division=0),
            "recall_at_0_7": recall_score(y, at_cut, zero_division=0)}


@dataclass(frozen=True)
class RunConfig:
    arm: str
    warmup: str
    seed: int
    bert_name: str = dados.BERT
    batch_size: int = BATCH_SIZE
    epochs: int = EPOCHS
    measure_words: bool = False


@dataclass
class Data:
    train: list[dict]
    dev: list[dict]
    dev_y: np.ndarray
    probes: Probes


@functools.cache
def code_version() -> str:
    """Commit of the code, '-dirty' if src/ has uncommitted changes. main() calls it before any training, so a
    missing git fails at once instead of after an hour of runs (weights are not saved, E8)."""
    def git(*args):
        return subprocess.run(["git", *args], capture_output=True, text=True, check=True,
                              cwd=RTE_TREINO.parents[1]).stdout.strip()
    return git("rev-parse", "--short", "HEAD") + ("-dirty" if git("status", "--porcelain", "src") else "")


def refuse_cut_text(cut: dict):
    """I9: nothing may be truncated, in inputs or targets."""
    if any(cut.values()):
        raise ValueError(f"truncation would cut text {cut}: raise MAX_INPUT_TOKENS/MAX_TARGET_TOKENS in rte_dados.py")


def append_csv(path: Path, rows: list[dict]):
    """Appends rows; refuses columns that differ from the file's header, which would land values under wrong names."""
    if not rows:
        return
    frame = pd.DataFrame(rows)
    if path.exists():
        header = list(pd.read_csv(path, nrows=0).columns)
        if header != list(frame.columns):
            raise ValueError(f"{path}: columns {list(frame.columns)} differ from the file's {header}; "
                             "write to a new file instead of mixing schemas")
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, mode="a", header=not path.exists(), index=False)


def run_one(cfg: RunConfig, data: Data, device: torch.device, out_dir: Path):
    torch.manual_seed(cfg.seed)  # head (and bridge) initialization
    t5_name = dados.T5 if cfg.arm == "bert_decoder" else None
    model = RationaleBert.from_pretrained(cfg.bert_name, t5_name)
    plan = make_plan(len(data.train), cfg.warmup, cfg.batch_size, cfg.epochs)
    probes = Probes(data.probes.groups.to(device), data.probes.words.to(device) if cfg.measure_words else None)
    start = time.perf_counter()
    log = train(model, plan, data.train, cfg.seed, device, cfg.batch_size, probes)
    seconds = time.perf_counter() - start
    keys = {"arm": cfg.arm, "warmup": cfg.warmup, "seed": cfg.seed}
    row = keys | metrics(data.dev_y, predict(classifier_only(model), data.dev, device)) | asdict(plan) | {
        "phase_a_steps": log.phase_a_steps, "l_aux_last_epoch": np.mean(log.last_epoch_aux) if log.last_epoch_aux
        else None, "seconds": round(seconds, 1), "device": str(device), "bert": cfg.bert_name,
        "t5": t5_name, "code": code_version()}
    append_csv(out_dir / "gradientes.csv", [keys | r for r in log.group_rows])
    append_csv(out_dir / "palavras.csv", [keys | r for r in log.word_rows])
    append_csv(out_dir / "resultados.csv", [row])  # last: this row is what marks the run as done for --grade
    print(f"{cfg.arm} {cfg.warmup} seed {cfg.seed}: roc_auc {row['roc_auc']:.4f} acc {row['accuracy']:.4f} "
          f"({seconds:.0f} s)", flush=True)


def load_data(tok: dados.Tokenizers, out_dir: Path, n_pairs: int | None = None,
              group_probe: int = grads.GROUP_PROBE_SIZE, word_probe: int = grads.WORD_PROBE_SIZE) -> Data:
    """Encodes train and dev, refuses to run if anything would be cut (I9), builds the probes, saves the groups."""
    train_pairs, dev_pairs = dados.training_pairs(), dados.dev_pairs()
    refuse_cut_text(dados.overlong_counts(train_pairs, tok)
                    | {"dev_" + k: v for k, v in dados.overlong_counts(dev_pairs, tok).items()})
    table = grads.expression_table(train_pairs)
    label_expr = grads.expression_pattern(table)
    out_dir.mkdir(parents=True, exist_ok=True)
    table.to_csv(out_dir / "expressoes-rotulo.csv", index=False)
    grads.group_word_table(train_pairs, label_expr).to_csv(out_dir / "grupos-palavras.csv", index=False)
    probes = Probes(grads.build_probe(train_pairs, tok, label_expr, group_probe),
                    grads.build_probe(train_pairs, tok, label_expr, word_probe))
    if n_pairs is not None:
        train_pairs = train_pairs.sample(n_pairs, random_state=0)
    return Data(dados.encode(train_pairs, tok), dados.encode(dev_pairs, tok), dev_pairs["y"].to_numpy(), probes)


def done_runs(out_dir: Path) -> set:
    path = out_dir / "resultados.csv"
    if not path.exists():
        return set()
    done = pd.read_csv(path, dtype={"warmup": str})
    return set(zip(done["arm"], done["warmup"], done["seed"]))


def smoke_test():
    """D6 on CPU: tiny BERT (128) + bridge + T5 base, 48 pairs, batches of 16, 2 epochs, small probes.
    Each run writes to its own folder (resultados/rte-treino/fumaca/<time>, ignored by git)."""
    out_dir = RTE_TREINO / "fumaca" / time.strftime("%Y-%m-%d-%H%M%S")
    data = load_data(dados.load_tokenizers(SMOKE_BERT), out_dir, n_pairs=48, group_probe=8, word_probe=4)
    for arm in ARMS:
        run_one(RunConfig(arm, "prop", 1, SMOKE_BERT, batch_size=16, epochs=2, measure_words=True), data,
                torch.device("cpu"), out_dir)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fumaca", action="store_true")
    parser.add_argument("--grade", action="store_true")
    parser.add_argument("--seeds", type=int, default=5)
    parser.add_argument("--arm", choices=ARMS)
    parser.add_argument("--warmup", choices=WARMUPS)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--medir-palavras", action="store_true")
    args = parser.parse_args()
    if not (args.fumaca or args.grade) and None in (args.arm, args.warmup, args.seed):
        parser.error("a single run needs --arm, --warmup and --seed (or use --grade / --fumaca)")
    code_version()  # fails here, before any training, if git is missing
    if args.fumaca:
        smoke_test()
        return
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    data = load_data(dados.load_tokenizers(), RTE_TREINO)
    if args.grade:
        configs = [RunConfig(arm, warmup, seed, measure_words=(arm == "bert_decoder" and seed == 1))
                   for arm in ARMS for warmup in WARMUPS for seed in range(1, args.seeds + 1)]
    else:
        configs = [RunConfig(args.arm, args.warmup, args.seed, measure_words=args.medir_palavras)]
    done = done_runs(RTE_TREINO)
    pending = [cfg for cfg in configs if (cfg.arm, cfg.warmup, cfg.seed) not in done]
    if device.type == "cuda" and any(cfg.arm == "bert_decoder" for cfg in pending):
        peak = memory_check(RationaleBert.from_pretrained(dados.BERT, dados.T5), data.train, data.probes.groups, device)
        total = torch.cuda.get_device_properties(device).total_memory / 2**30
        print(f"memória: pico {peak:.1f} GB de {total:.1f} GB (passo com os 32 pares mais longos + medida)", flush=True)
        torch.cuda.empty_cache()
    for cfg in pending:
        run_one(cfg, data, device, RTE_TREINO)


if __name__ == "__main__":
    main()
