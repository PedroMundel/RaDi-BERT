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
from collections.abc import Callable
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from torch.optim.lr_scheduler import LambdaLR
from torch.utils.data import DataLoader

from radibert import esnli_dados as esnli
from radibert import rte_dados as dados
from radibert import rte_gradientes as grads
from radibert import rte_marcas as marcas
from radibert.paths import RESULTADOS, RTE_TREINO
from radibert.rte_modelo import RationaleBert, classifier_only, cls_loss

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
# Memory and logging (09/11: batch 32 at once spilled the 5060's VRAM into shared system memory)
MICRO_BATCH = 16
PROGRESS_EVERY = 100

# Mark arms (10/11, rte_marcas): pull the last layer's [CLS] attention onto the marked input positions. Weight 1 and
# the last layer are the Claude's defaults, not swept (the dev set is the test).
MARK_WEIGHT = 1.0
MARK_ARMS = ("marks_none", "marks_real", "marks_random")  # the suffix is the column of rte_marcas.mark_table

HELD_OUT_FROM = 1000  # --pares: train pairs from this position of the fixed shuffle on are test, never train

# Calendar control (10/11, H1 of docs/2026-11-10-hipoteses-do-nulo.md): plain BERT on the decoder arm's schedule,
# i.e. no classification step in phase B and BERT's rate peaking at its end. Nothing trains in phase B here.
CALENDAR_ARM = "bert_calendar"
# the decoder arm with every rationale swapped for another pair's of the same label (rte_dados.shuffle_within_label)
SHUFFLED_ARM, SHUFFLE_SEED = "bert_decoder_shuffled", 0

ARMS = ("bert", "bert_decoder")
T5_ARMS = ("t5enc", "t5enc_decoder")  # 10/11: the same training with the T5 encoder in place of BERT
WARMUPS = ("500", "prop")
SMOKE_BERT = dados.TINY


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
    encoder = list(model.bert.parameters())
    heads = list(model.head.parameters()) + (list(model.token_head.parameters()) if model.token_head is not None
                                             else [])
    heads += list(model.projections.parameters()) if model.projections is not None else []
    if model.group_head is not None:
        heads += list(model.group_head.parameters()) + list(model.group_label_bias.parameters())
    groups = [{"params": encoder, "weight_decay": 0.0}, {"params": heads, "weight_decay": 0.0}]
    if model.t5 is not None:
        # T5-encoder arm: the encoder (and the `shared` embedding it reads) is already in the first group
        in_encoder = {id(p) for p in encoder}
        decoder = [p for p in model.t5.parameters() if p.requires_grad and id(p) not in in_encoder]
        decoder += list(model.bridge.parameters()) if model.bridge is not None else []
        groups.append({"params": decoder, "weight_decay": DECODER_WEIGHT_DECAY})
    return groups


def lr_factors(model: RationaleBert, plan: Plan) -> list:
    """E1: BERT warms up over phase B when there is a decoder; head and decoder over the Table 4 warmup."""
    table4 = linear_schedule(plan.warmup_steps, plan.total)
    if model.t5 is None and not model.decoder_calendar:
        return [table4, table4]
    return [linear_schedule(plan.phase_b, plan.total), table4] + ([table4] if model.t5 is not None else [])


def uses_marks(model: RationaleBert) -> bool:
    """Mark models (attention loss or token head): no phases, the mark loss from step 1."""
    return model.mark_attention or model.token_head is not None


def marked_loss(l_cls: torch.Tensor, l_marks: torch.Tensor | None) -> torch.Tensor:
    """Mark arms: no phases, both losses from step 1 (the classification schedule is the plain BERT's)."""
    return l_cls if l_marks is None else l_cls + MARK_WEIGHT * l_marks


def internal_only(l_cls: torch.Tensor, l_aux: torch.Tensor) -> torch.Tensor:
    """The first phase of the sequence arms (plan, section 11.5; TinyBERT's intermediate-layer distillation): the
    student only imitates the teacher's internals, so the classification loss stays out and the head never moves."""
    return l_aux


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


def place(model: RationaleBert, device: torch.device) -> RationaleBert:
    """Moves the model to the device but keeps the T5 encoder blocks, frozen and never run, on the CPU (~340 MB);
    in the T5-encoder arm they are the classifier's encoder and stay on the device."""
    model.to(device)
    if model.t5 is not None and not model.shares_t5_encoder:
        model.t5.encoder.block.to("cpu")
        model.t5.encoder.final_layer_norm.to("cpu")
    return model


def make_optimizer(model: RationaleBert) -> torch.optim.Optimizer:
    return torch.optim.AdamW(param_groups(model), lr=LR, eps=ADAM_EPS, betas=ADAM_BETAS)


def finish_step(model: RationaleBert, opt: torch.optim.Optimizer):
    torch.nn.utils.clip_grad_norm_(model.parameters(), CLIP_NORM)
    opt.step()
    opt.zero_grad()


def target_tokens(batch: dict) -> int:
    return int((batch["labels"] != dados.IGNORED).sum())


def aux_units(batch: dict) -> int:
    """What the auxiliary loss averages over: marked pairs (mark arms) or target tokens (decoder)."""
    return marcas.marked_pairs(batch) if "marks" in batch else target_tokens(batch)


def pair_units(batch: dict) -> int:
    """The distillation loss (rte_destilacao) is a mean over the pairs."""
    return len(batch["y"])


def accumulated_backward(model: RationaleBert, batch: dict, combine, micro: int = MICRO_BATCH) -> tuple:
    """Backward of one batch in micro-batches, each loss weighted by its share of the batch's pairs (L_cls) and
    auxiliary units (L_aux), so the summed gradient is the full batch's (I16) with about half the activation memory
    (09/11: batch 32 spilled the 5060's VRAM into shared memory). `combine(l_cls, l_aux)` is the phase's loss.
    Returns the batch's L_cls and L_aux (None without one). Backward runs outside autocast."""
    device = batch["input_ids"].device
    units = pair_units if model.distill is not None else aux_units
    n_pairs, n_tokens = len(batch["y"]), units(batch)
    l_cls_total, l_aux_total = 0.0, None
    for start in range(0, n_pairs, micro):
        part = grads.rows_of(batch, start, start + micro)
        with autocast(device):
            logit, l_aux = model(part)
            l_cls = cls_loss(logit, part["y"]) * (len(part["y"]) / n_pairs)
            if l_aux is not None:
                l_aux = l_aux * (units(part) / n_tokens)
            loss = combine(l_cls, l_aux)
        loss.backward()
        l_cls_total += l_cls.item()
        if l_aux is not None:
            l_aux_total = (l_aux_total or 0.0) + l_aux.item()
    return l_cls_total, l_aux_total


def run_phase_a(model: RationaleBert, opt: torch.optim.Optimizer, items: list[dict], seed: int, batch_size: int,
                device: torch.device, micro: int = MICRO_BATCH) -> int:
    """One pass over a random half of the pairs: BERT frozen (no graph through it), decoder learns to read it."""
    half = torch.randperm(len(items), generator=torch.Generator().manual_seed(seed))[: len(items) // 2]
    loader = DataLoader([items[i] for i in half], batch_size=batch_size, collate_fn=dados.collate)
    for batch in loader:
        batch = to_device(batch, device)
        n_tokens = target_tokens(batch)
        for start in range(0, len(batch["y"]), micro):
            part = grads.rows_of(batch, start, start + micro)
            with autocast(device):
                with torch.no_grad():
                    h, _ = model.encode(part)
                l_aux = model.decode(h, part).loss * (target_tokens(part) / n_tokens)
            l_aux.backward()
        if model.shares_t5_encoder:  # `shared` is also the encoder's input: frozen with it here (audit 10/11)
            model.t5.shared.weight.grad = None
        finish_step(model, opt)
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


def measure(model, probes: Probes | None, plan: Plan, step: int, log: TrainLog, device, chunk: int):
    """Group measure at step 1 and every MEASURE_EVERY steps; word measure at 1, end of phase B and the last step."""
    if probes is None:
        return
    amp = lambda: autocast(device)  # noqa: E731  forward under bf16 like training; gradients outside it
    if step == 1 or step % MEASURE_EVERY == 0:
        log.group_rows.append({"phase": "B" if step <= plan.phase_b else "C"}
                              | grads.measure_groups(model, probes.groups, step, amp, chunk))
    if probes.words is not None and step in {1, plan.phase_b, plan.total}:
        log.word_rows += grads.measure_words(model, probes.words, step, amp, chunk)


def train(model: RationaleBert, plan: Plan, items: list[dict], seed: int, device: torch.device,
          batch_size: int = BATCH_SIZE, probes: Probes | None = None, micro: int = MICRO_BATCH,
          loss_of=None, after_step=None) -> TrainLog:
    """Trains in place. `loss_of(l_cls, l_aux)` replaces the model's own way of joining the two losses. `micro` splits each batch (and each probe) without changing the gradient (I16). Same seed, same batch order in both arms (the loader has its own generator). Same seed, same
    weights on CPU (I10); on CUDA the embedding backward uses atomic adds, so reruns differ slightly."""
    place(model, device).train()
    opt = make_optimizer(model)
    log = TrainLog()
    start = time.perf_counter()
    if model.t5 is not None:
        log.phase_a_steps = run_phase_a(model, opt, items, seed, batch_size, device, micro)
        if log.phase_a_steps != plan.phase_a:
            raise RuntimeError(f"phase A ran {log.phase_a_steps} steps, the plan says {plan.phase_a}")
    sched = LambdaLR(opt, lr_factors(model, plan))  # created after phase A: its constant 5e-5 is the base rate
    loader = DataLoader(items, batch_size=batch_size, shuffle=True, collate_fn=dados.collate,
                        generator=torch.Generator().manual_seed(seed))
    step = 0
    for epoch in range(plan.total // plan.per_epoch):
        for batch in loader:
            step += 1
            if model.decoder_calendar and step <= plan.phase_b:
                sched.step()  # calendar control: the classifier gets no step in phase B, as in the decoder arm
                continue
            batch = to_device(batch, device)
            combine = loss_of or (marked_loss if uses_marks(model)
                                  else functools.partial(training_loss, step, plan))
            _, l_aux = accumulated_backward(model, batch, combine, micro)
            finish_step(model, opt)
            sched.step()
            if l_aux is not None and epoch == plan.total // plan.per_epoch - 1:
                log.last_epoch_aux.append(l_aux)
            if model.t5 is not None:
                measure(model, probes, plan, step, log, device, micro)
            if step % PROGRESS_EVERY == 0:  # so the watchdog can tell slow from stuck
                print(f"  passo {step}/{plan.total} ({time.perf_counter() - start:.0f} s)", flush=True)
            if after_step is not None:  # called with the step just trained (never for the calendar arm's skipped steps)
                after_step(step)
    return log


def memory_check(model: RationaleBert, items: list[dict], probe: grads.Probe, device: torch.device,
                 batch_size: int = BATCH_SIZE, micro: int = MICRO_BATCH) -> float:
    """One phase-C step on the longest pairs, then one group measure: the peak GPU memory in GB (0 on CPU). --grade
    runs it first, so an out-of-memory error shows up in seconds instead of hours into the grid (audit 09/11)."""
    place(model, device).train()
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)
    longest = sorted(items, key=lambda it: len(it["input_ids"]), reverse=True)[:batch_size]
    accumulated_backward(model, to_device(dados.collate(longest), device), lambda c, a: c + AUX_WEIGHT * a, micro)
    finish_step(model, make_optimizer(model))
    grads.measure_groups(model, probe.to(device), step=0, amp=lambda: autocast(device), chunk=micro)
    return torch.cuda.max_memory_allocated(device) / 2**30 if device.type == "cuda" else 0.0


@torch.no_grad()
def predict(classifier, items: list[dict], device: torch.device) -> np.ndarray:
    classifier.to(device).eval()
    out = []
    for batch in DataLoader(items, batch_size=BATCH_SIZE, collate_fn=dados.collate):
        with autocast(device):
            logits = classifier(to_device(batch, device)).float()
        out.append((torch.sigmoid(logits) if logits.dim() == 1 else torch.softmax(logits, -1)).cpu())
    return torch.cat(out).numpy()


def metrics(y: np.ndarray, p: np.ndarray, labels: dict[int, str] = grads.RTE_LABELS) -> dict:
    """D4: the paper's ROC-AUC and precision/recall at 0.7, plus accuracy and F1 at 0.5. With more than two labels
    (e-SNLI): accuracy and F1 of the most probable label, ROC-AUC one-vs-rest averaged over the labels."""
    if p.ndim == 2:
        guess = p.argmax(1)
        f1_each = f1_score(y, guess, average=None, labels=list(labels), zero_division=0)
        return {"roc_auc": roc_auc_score(y, p, multi_class="ovr", average="macro", labels=list(labels)),
                "accuracy": accuracy_score(y, guess), "f1_macro": f1_score(y, guess, average="macro", zero_division=0)
                } | {f"f1_{name}": f for name, f in zip(labels.values(), f1_each)}
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
    micro_batch: int = MICRO_BATCH  # not in the results row: the RTE grid's CSV keeps its columns
    save_weights: bool = False  # --salvar-pesos: the trained classifier (no decoder) goes to <out_dir>/pesos


@dataclass
class Data:
    train: list[dict]
    dev: list[dict]
    dev_y: np.ndarray
    probes: Probes
    labels: dict[int, str] = field(default_factory=lambda: dict(grads.RTE_LABELS))
    marks: pd.DataFrame | None = None  # rte_marcas.mark_table, only for the mark arms
    held: list[dict] | None = None  # --pares: train pairs no size trains on, a second and larger test set
    held_y: np.ndarray | None = None
    outside: list[dict] | None = None  # --fora: the task's outside_pairs, RTE's two labels, outside the distribution
    outside_y: np.ndarray | None = None
    train_shuffled: list[dict] | None = None  # the shuffled arm's items and probes: same pairs, swapped rationales
    probes_shuffled: Probes | None = None


def training_items(arm: str, data: Data) -> list[dict]:
    """The arm's train items: with real or random marks in those two arms, the plain items otherwise."""
    if arm in MARK_ARMS and arm != "marks_none":
        return marcas.with_marks(data.train, data.marks, arm.removeprefix("marks_"))
    return data.train


def arm_inputs(data: Data, arm: str) -> tuple[list[dict], Probes]:
    """What the arm trains on and what its gradient measures read."""
    if arm == SHUFFLED_ARM:
        return data.train_shuffled, data.probes_shuffled
    return training_items(arm, data), data.probes


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


def outside_scores(y: np.ndarray, p: np.ndarray) -> dict:
    """--fora: the two scores of the out-of-distribution test, under their own columns of the results row. A
    three-label model (trained on e-SNLI) is read on RTE's two labels: the score is the probability of entailment
    and the guess is entailment when that is the most probable label."""
    if p.ndim == 2:
        return {"fora_roc_auc": roc_auc_score(y, p[:, esnli.ENTAILMENT]),
                "fora_accuracy": accuracy_score(y, p.argmax(1) == esnli.ENTAILMENT), "n_fora": len(y)}
    scores = metrics(y, p)
    return {"fora_roc_auc": scores["roc_auc"], "fora_accuracy": scores["accuracy"], "n_fora": len(y)}


def save_classifier(classifier, out_dir: Path, cfg: RunConfig) -> Path:
    """--salvar-pesos: the encoder and the head as trained, so another test set later costs no new training."""
    path = out_dir / "pesos" / f"{cfg.arm}-{cfg.warmup}-semente-{cfg.seed}.pt"
    path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(classifier.state_dict(), path)
    return path


def has_decoder(arm: str) -> bool:
    return "_decoder" in arm


def build_model(arm: str, encoder_name: str, n_labels: int = 2) -> tuple[RationaleBert, str | None]:
    """The arm's model and the checkpoint of its decoder (None without one). T5-encoder arms take the decoder from
    the encoder's own checkpoint; BERT arms from t5-base, as in the paper."""
    if arm in MARK_ARMS:
        return RationaleBert.with_mark_attention(encoder_name, n_labels), None
    if arm in T5_ARMS:
        t5_name = encoder_name if has_decoder(arm) else None
        return RationaleBert.from_t5(encoder_name, has_decoder(arm), n_labels), t5_name
    t5_name = dados.T5 if has_decoder(arm) else None
    model = RationaleBert.from_pretrained(encoder_name, t5_name, n_labels)
    model.decoder_calendar = arm == CALENDAR_ARM
    return model, t5_name


def run_one(cfg: RunConfig, data: Data, device: torch.device, out_dir: Path):
    torch.manual_seed(cfg.seed)  # head (and bridge) initialization; from_pretrained draws nothing else
    model, t5_name = build_model(cfg.arm, cfg.bert_name, len(data.labels))
    plan = make_plan(len(data.train), cfg.warmup, cfg.batch_size, cfg.epochs)
    items, arm_probes = arm_inputs(data, cfg.arm)
    probes = Probes(arm_probes.groups.to(device), arm_probes.words.to(device) if cfg.measure_words else None)
    start = time.perf_counter()
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)
    log = train(model, plan, items, cfg.seed, device, cfg.batch_size, probes,
                cfg.micro_batch)
    seconds = time.perf_counter() - start
    peak = f", pico {torch.cuda.max_memory_allocated(device) / 2**30:.1f} GB" if device.type == "cuda" else ""
    keys = {"arm": cfg.arm, "warmup": cfg.warmup, "seed": cfg.seed}
    classifier = classifier_only(model)
    scores = metrics(data.dev_y, predict(classifier, data.dev, device), data.labels)
    if data.held is not None:
        held = metrics(data.held_y, predict(classifier, data.held, device), data.labels)
        scores |= {"held_roc_auc": held["roc_auc"], "held_accuracy": held["accuracy"],
                   "n_train": len(data.train), "n_held": len(data.held)}
    if data.outside is not None:
        scores |= outside_scores(data.outside_y, predict(classifier, data.outside, device))
    if cfg.save_weights:  # before the results row: a run marked as done has its weights on disk
        save_classifier(classifier, out_dir, cfg)
    row = keys | scores | asdict(plan) | {
        "phase_a_steps": log.phase_a_steps, "l_aux_last_epoch": np.mean(log.last_epoch_aux) if log.last_epoch_aux
        else None, "seconds": round(seconds, 1), "device": str(device), "bert": cfg.bert_name,
        "t5": t5_name, "code": code_version()}
    append_csv(out_dir / "gradientes.csv", [keys | r for r in log.group_rows])
    append_csv(out_dir / "palavras.csv", [keys | r for r in log.word_rows])
    append_csv(out_dir / "resultados.csv", [row])  # last: this row is what marks the run as done for --grade
    print(f"{cfg.arm} {cfg.warmup} seed {cfg.seed}: roc_auc {row['roc_auc']:.4f} acc {row['accuracy']:.4f} "
          f"({seconds:.0f} s{peak})", flush=True)


@dataclass(frozen=True)
class Task:
    """What --tarefa picks: the label names (y -> name), where the pairs come from and where each encoder's results
    go. Every pairs frame has idx, y, sentence1, sentence2 (and rationale for train), as rte_dados.encode reads."""
    labels: dict[int, str]
    training_pairs: Callable[[], pd.DataFrame]
    dev_pairs: Callable[[], pd.DataFrame]
    out_dirs: dict[str, Path]
    # the pairs the label-expression table (group S) is built from, when not the train pairs: its count cut is
    # absolute, so a larger train set would move words into S and the groups would stop being comparable
    expression_pairs: Callable[[], pd.DataFrame] | None = None
    # --fora: pairs of another source, with RTE's two labels (y 1 entailment), that no arm of the task trains on
    outside_pairs: Callable[[], pd.DataFrame] | None = None


TASKS = {"rte": Task(grads.RTE_LABELS, dados.training_pairs, dados.dev_pairs,
                     {"bert": RTE_TREINO, "t5": RESULTADOS / "rte-t5enc", "msmarco": RESULTADOS / "rte-msmarco",
                      "capreolus": RESULTADOS / "rte-capreolus",
                      "marcas": RESULTADOS / "rte-marcas", "calendario": RESULTADOS / "rte-calendario",
                      "small": RESULTADOS / "rte-small", "tiny": RESULTADOS / "rte-tiny",
                      "marcas-small": RESULTADOS / "rte-marcas-small",
                      "marcas-tiny": RESULTADOS / "rte-marcas-tiny"},
                     outside_pairs=lambda: esnli.with_rte_labels(esnli.dev_pairs())),
         "esnli": Task(esnli.LABELS, esnli.training_pairs, esnli.dev_pairs,
                       {"bert": RESULTADOS / "esnli-treino", "t5": RESULTADOS / "esnli-t5enc",
                        "calendario": RESULTADOS / "esnli-treino-calendario"}, outside_pairs=dados.all_pairs),
         # 18/11: every pair of the 35B batch, the first size at which Table 4 fits (4,000 steps, phase A of 250)
         "esnli16k": Task(esnli.LABELS, esnli.batch_pairs, esnli.dev_pairs,
                          {"bert": RESULTADOS / "esnli-treino-16k",
                           "calendario": RESULTADOS / "esnli-treino-16k-calendario",
                           "embaralhado": RESULTADOS / "esnli-treino-16k-embaralhado"},
                          expression_pairs=esnli.training_pairs, outside_pairs=dados.all_pairs)}


def load_data(tok: dados.Tokenizers, out_dir: Path, task: Task = TASKS["rte"], n_pairs: int | None = None,
              group_probe: int = grads.GROUP_PROBE_SIZE, word_probe: int = grads.WORD_PROBE_SIZE,
              with_marks: bool = False, held_out: bool = False, outside: bool = False,
              swap_rationales: bool = False) -> Data:
    """Encodes train and dev, refuses to run if anything would be cut (I9), builds the probes, saves the groups
    (and, for the mark arms, the marks of every train pair in marcas.csv)."""
    train_pairs, dev_pairs = task.training_pairs(), task.dev_pairs()
    refuse_cut_text(dados.overlong_counts(train_pairs, tok)
                    | {"dev_" + k: v for k, v in dados.overlong_counts(dev_pairs, tok).items()})
    table = grads.expression_table(task.expression_pairs() if task.expression_pairs else train_pairs, task.labels)
    label_expr = grads.expression_pattern(table)
    out_dir.mkdir(parents=True, exist_ok=True)
    table.to_csv(out_dir / "expressoes-rotulo.csv", index=False)
    grads.group_word_table(train_pairs, label_expr).to_csv(out_dir / "grupos-palavras.csv", index=False)
    probes = Probes(grads.build_probe(train_pairs, tok, label_expr, group_probe),
                    grads.build_probe(train_pairs, tok, label_expr, word_probe))
    held_pairs = None
    if held_out:
        # --pares (10/11): the first n pairs of one fixed shuffle train; the pairs after HELD_OUT_FROM are never
        # trained on, whatever n, so every size is tested on the same held-out pairs (Pedro's idea)
        if n_pairs is None or n_pairs > HELD_OUT_FROM:
            raise ValueError(f"held-out runs train on at most {HELD_OUT_FROM} pairs, got {n_pairs}")
        shuffled = train_pairs.sample(frac=1, random_state=0)
        train_pairs, held_pairs = shuffled.iloc[:n_pairs], shuffled.iloc[HELD_OUT_FROM:]
    elif n_pairs is not None:
        train_pairs = train_pairs.sample(n_pairs, random_state=0)
    marks = None
    if with_marks:
        marks = marcas.mark_table(train_pairs, tok, label_expr)
        marks.to_csv(out_dir / "marcas.csv", index=False)
        print(f"marcas: {marks['real'].map(len).sum() / marks['n_tokens'].sum():.1%} dos tokens de entrada, "
              f"{(marks['real'].map(len) == 0).sum()} de {len(marks)} pares sem marca", flush=True)
    data = Data(dados.encode(train_pairs, tok), dados.encode(dev_pairs, tok), dev_pairs["y"].to_numpy(), probes,
                dict(task.labels), marks)
    if swap_rationales:
        swapped = dados.shuffle_within_label(train_pairs, SHUFFLE_SEED)
        data.train_shuffled = dados.encode(swapped, tok)
        data.probes_shuffled = Probes(grads.build_probe(swapped, tok, label_expr, group_probe),
                                      grads.build_probe(swapped, tok, label_expr, word_probe))
    if held_pairs is not None:
        data.held, data.held_y = dados.encode(held_pairs.drop(columns="rationale"), tok), held_pairs["y"].to_numpy()
    if outside:
        outside_pairs = task.outside_pairs()
        refuse_cut_text({"fora_" + k: v for k, v in dados.overlong_counts(outside_pairs, tok).items()})
        data.outside, data.outside_y = dados.encode(outside_pairs, tok), outside_pairs["y"].to_numpy()
    return data


def done_runs(out_dir: Path) -> set:
    path = out_dir / "resultados.csv"
    if not path.exists():
        return set()
    done = pd.read_csv(path, dtype={"warmup": str})
    return set(zip(done["arm"], done["warmup"], done["seed"]))


@dataclass(frozen=True)
class Encoder:
    """What --encoder picks: the arms, the checkpoint and the input tokenizer. The T5 v1.1 tokenizer does not load
    in transformers 5 (only spiece.model, the converter asks for tiktoken), and its spiece.model is the t5-base one
    (same git oid on the Hub, 10/11): both T5 arms tokenize with t5-base."""
    arms: tuple[str, ...]
    name: str
    input_tokenizer: str


ENCODERS = {"bert": Encoder(ARMS, dados.BERT, dados.BERT), "t5": Encoder(T5_ARMS, dados.T5_ENCODER, dados.T5),
            "msmarco": Encoder(ARMS, dados.MSMARCO, dados.BERT),  # RTE only: Agrawal's own baseline (Table 2)
            "capreolus": Encoder(ARMS, dados.CAPREOLUS, dados.BERT),  # RTE only: the other MS-MARCO checkpoint
            "marcas": Encoder(MARK_ARMS, dados.BERT, dados.BERT),  # RTE only: plain BERT, [CLS] attention marks
            "calendario": Encoder((CALENDAR_ARM,), dados.BERT, dados.BERT),  # pairs with the bert grid (RTE, esnli16k)
            "embaralhado": Encoder((SHUFFLED_ARM,), dados.BERT, dados.BERT),  # esnli16k only: shuffled control
            # RTE only (10/11, Pedro's idea): weaker encoders; with the decoder, a linear bridge lifts them to 768
            "small": Encoder(ARMS, dados.SMALL, dados.BERT), "tiny": Encoder(ARMS, dados.TINY, dados.BERT),
            "marcas-small": Encoder(MARK_ARMS, dados.SMALL, dados.BERT),
            "marcas-tiny": Encoder(MARK_ARMS, dados.TINY, dados.BERT)}


def smoke_test(task: str, encoder: str, outside: bool = False, save_weights: bool = False):
    """D6 on CPU, 48 pairs, batches of 16, 2 epochs, small probes: tiny BERT (128) + bridge + T5 base, or the real
    T5 v1.1 base for --encoder t5. Each run writes to its own folder (<out_dir>/fumaca/<time>, ignored by git)."""
    enc = ENCODERS[encoder]
    name, tokenizer = (SMOKE_BERT, SMOKE_BERT) if enc.name == dados.BERT else (enc.name, enc.input_tokenizer)
    out_dir = TASKS[task].out_dirs[encoder] / "fumaca" / time.strftime("%Y-%m-%d-%H%M%S")
    data = load_data(dados.load_tokenizers(tokenizer), out_dir, TASKS[task], n_pairs=48, group_probe=8, word_probe=4,
                     with_marks=enc.arms == MARK_ARMS, outside=outside, swap_rationales=SHUFFLED_ARM in enc.arms)
    for arm in enc.arms:
        run_one(RunConfig(arm, "prop", 1, name, batch_size=16, epochs=2, measure_words=True,
                          save_weights=save_weights), data,
                torch.device("cpu"), out_dir)


def main():
    global AUX_WEIGHT
    parser = argparse.ArgumentParser()
    parser.add_argument("--fumaca", action="store_true")
    parser.add_argument("--grade", action="store_true")
    parser.add_argument("--tarefa", choices=TASKS, default="rte")
    parser.add_argument("--encoder", choices=ENCODERS, default="bert")
    parser.add_argument("--seeds", type=int, default=5)
    parser.add_argument("--warmups", nargs="+", choices=WARMUPS, default=list(WARMUPS), help="for --grade")
    parser.add_argument("--arm", choices=ARMS + T5_ARMS + MARK_ARMS + (CALENDAR_ARM, SHUFFLED_ARM))
    parser.add_argument("--warmup", choices=WARMUPS)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--medir-palavras", action="store_true")
    parser.add_argument("--pares", type=int, help=f"train on the first N pairs of a fixed shuffle (N <= "
                        f"{HELD_OUT_FROM}) and also test on the train pairs after the first {HELD_OUT_FROM}")
    parser.add_argument("--fora", action="store_true",
                        help="also test outside the distribution, on RTE's two labels: an RTE-trained model on the "
                             "e-SNLI dev, an e-SNLI-trained one on every RTE pair")
    parser.add_argument("--salvar-pesos", action="store_true",
                        help="keep each trained classifier (encoder and head, no decoder) in <out_dir>/pesos; "
                             "results go to their own folder (-pesos)")
    parser.add_argument("--peso-aux", type=float,
                        help=f"weight of the decoder loss in phase C instead of the paper's {AUX_WEIGHT} (phases A "
                             "and B do not use it); results go to their own folder (-aux-<weight>)")
    parser.add_argument("--micro", type=int, default=MICRO_BATCH,
                        help="pairs per forward pass; same gradient (I16), less memory (10/11: 8 when other apps hold VRAM)")
    args = parser.parse_args()
    enc, task = ENCODERS[args.encoder], TASKS[args.tarefa]
    if args.encoder not in task.out_dirs:
        parser.error(f"--encoder {args.encoder} has no results folder for --tarefa {args.tarefa}")
    out_dir = task.out_dirs[args.encoder]
    if not (args.fumaca or args.grade) and None in (args.arm, args.warmup, args.seed):
        parser.error("a single run needs --arm, --warmup and --seed (or use --grade / --fumaca)")
    if args.arm is not None and args.arm not in enc.arms:
        parser.error(f"--arm {args.arm} is not an arm of --encoder {args.encoder} ({', '.join(enc.arms)})")
    code_version()  # fails here, before any training, if git is missing
    if args.peso_aux is not None:  # 19/11, the weight sweep: training_loss and memory_check read the module's value
        AUX_WEIGHT = args.peso_aux
        print(f"peso da perda do decoder na fase C: {AUX_WEIGHT:g}", flush=True)
    if args.fumaca:
        smoke_test(args.tarefa, args.encoder, args.fora, args.salvar_pesos)
        return
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if args.pares is not None:  # its own folder: a run is "done" by arm, warmup and seed, not by size
        out_dir = out_dir.with_name(f"{out_dir.name}-{args.pares}")
    if args.fora:  # its own folder too: the results row gains columns
        out_dir = out_dir.with_name(f"{out_dir.name}-fora")
    if args.salvar_pesos:  # and here: a run counts as done only where its weights were kept
        out_dir = out_dir.with_name(f"{out_dir.name}-pesos")
    if args.peso_aux is not None:
        out_dir = out_dir.with_name(f"{out_dir.name}-aux-{args.peso_aux:g}")
    data = load_data(dados.load_tokenizers(enc.input_tokenizer), out_dir, task, n_pairs=args.pares,
                     with_marks=enc.arms == MARK_ARMS, held_out=args.pares is not None, outside=args.fora,
                     swap_rationales=SHUFFLED_ARM in enc.arms)
    if args.grade:
        configs = [RunConfig(arm, warmup, seed, enc.name, measure_words=(has_decoder(arm) and seed == 1),
                             micro_batch=args.micro, save_weights=args.salvar_pesos)
                   for arm in enc.arms for warmup in args.warmups for seed in range(1, args.seeds + 1)]
    else:
        configs = [RunConfig(args.arm, args.warmup, args.seed, enc.name, measure_words=args.medir_palavras,
                             micro_batch=args.micro, save_weights=args.salvar_pesos)]
    done = done_runs(out_dir)
    pending = [cfg for cfg in configs if (cfg.arm, cfg.warmup, cfg.seed) not in done]
    decoder_arm = next((cfg.arm for cfg in pending if has_decoder(cfg.arm)), None)
    if device.type == "cuda" and decoder_arm is not None:
        peak = memory_check(build_model(decoder_arm, enc.name, len(data.labels))[0], data.train,
                            data.probes.groups, device, micro=args.micro)
        total = torch.cuda.get_device_properties(device).total_memory / 2**30
        print(f"memória: pico {peak:.1f} GB de {total:.1f} GB (passo com os 32 pares mais longos + medida, "
              f"micro-lote {args.micro})", flush=True)
        torch.cuda.empty_cache()
    for cfg in pending:
        run_one(cfg, data, device, out_dir)


if __name__ == "__main__":
    main()
