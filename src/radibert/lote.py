"""First generation batch: Qwen3.6-35B-A3B, variant F, on a random sample of the e-SNLI train set.

The sample is the whole train set shuffled with a fixed seed, so any prefix of it is a random sample (the learning
curve can be cut from whatever finished). The prompt comes from src/radibert/piloto_qwen.py, variant F.

Server (measured 27/10; QWEN_WORKERS=4 matches -np 4):
    llama-server -m Qwen3.6-35B-A3B-UD-IQ4_XS.gguf -ngl 999 --n-cpu-moe 30 -c 8192 -np 4 -kvu -cms 0 -ub 128
                 --jinja --host 127.0.0.1 --port 8080

Usage (safe to re-run: it skips pairIDs already in the output):
    python -m radibert.lote amostra                       # shuffled train -> amostra-treino.csv
    python -m radibert.lote gerar --alvo 16000 --ate 07:50   # stop at 16000 pairs or at 07:50, whichever comes first
"""
import argparse
import csv
import datetime as dt
import os
import sys
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait

import pandas as pd

from radibert import piloto_qwen
from radibert.paths import ESNLI, LOTE_35B

TRAIN = [ESNLI / f"esnli_train_{i}.csv" for i in (1, 2)]
SAMPLE = LOTE_35B / "amostra-treino.csv"
OUT = LOTE_35B / "racionalizacoes-F-35B.csv"
PROGRESS = LOTE_35B / "progresso.txt"
VARIANT = "F"
SEED = 42
WORKERS = int(os.environ.get("QWEN_WORKERS", "4"))
KEEP = ["pairID", "gold_label", "Sentence1", "Sentence2", "Explanation_1"]
FIELDS = KEEP + ["qwen", "finish_reason", "tokens_in", "tokens_out", "seconds", "feito_em"]


def cmd_amostra():
    train = pd.concat([pd.read_csv(p, usecols=KEEP) for p in TRAIN], ignore_index=True)
    usable = train.dropna(subset=["Sentence1", "Sentence2", "Explanation_1"])  # every arm needs the human text too
    usable.sample(frac=1, random_state=SEED).to_csv(SAMPLE, index=False)
    print(f"{len(train)} train pairs, {len(train) - len(usable)} without text dropped -> {len(usable)} in {SAMPLE}")


def generate(row) -> dict:
    out = piloto_qwen.ask_qwen(piloto_qwen.prompt_for(row, VARIANT))
    return {**{k: getattr(row, k) for k in KEEP}, **out, "feito_em": dt.datetime.now().isoformat(timespec="seconds")}


def keep_awake():
    """Ask Windows not to idle-sleep while this process runs (released when it exits; no setting is changed)."""
    if sys.platform == "win32":
        import ctypes
        ES_CONTINUOUS, ES_SYSTEM_REQUIRED = 0x80000000, 0x00000001
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)


def cmd_gerar(target: int, until: dt.datetime):
    keep_awake()
    done =set(pd.read_csv(OUT, usecols=["pairID"])["pairID"]) if OUT.exists() else set()
    todo = (row for row in pd.read_csv(SAMPLE).itertuples(index=False) if row.pairID not in done)
    new, start = 0, time.perf_counter()
    with open(OUT, "a", newline="", encoding="utf-8") as f, ThreadPoolExecutor(WORKERS) as pool:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        if not done:
            writer.writeheader()
        running = set()
        while True:
            # keep WORKERS requests in flight; stop feeding at the target or the deadline
            while len(running) < WORKERS and len(done) + new + len(running) < target and dt.datetime.now() < until:
                row = next(todo, None)
                if row is None:
                    break
                running.add(pool.submit(generate, row))
            if not running:
                break
            finished, running = wait(running, return_when=FIRST_COMPLETED)
            for future in finished:
                writer.writerow(future.result())
                new += 1
            f.flush()
            if new % 100 < len(finished):
                elapsed = time.perf_counter() - start
                line = (f"{dt.datetime.now():%H:%M:%S} {len(done) + new} pares no total, {new} nesta rodada, "
                        f"{elapsed / new:.2f} s/par")
                PROGRESS.write_text(line + "\n", encoding="utf-8")
                print(line, flush=True)
    elapsed = time.perf_counter() - start
    PROGRESS.write_text(f"FIM {dt.datetime.now():%H:%M:%S} {len(done) + new} pares no total, {new} nesta rodada"
                        + (f", {elapsed / new:.2f} s/par" if new else "") + "\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cmd", choices=["amostra", "gerar"])
    parser.add_argument("--alvo", type=int, default=16000)
    parser.add_argument("--ate", default="07:50", help="HH:MM, next occurrence")
    args = parser.parse_args()
    if args.cmd == "amostra":
        cmd_amostra()
    else:
        now = dt.datetime.now()
        until = dt.datetime.combine(now.date(), dt.time.fromisoformat(args.ate))
        cmd_gerar(args.alvo, until if until > now else until + dt.timedelta(days=1))
