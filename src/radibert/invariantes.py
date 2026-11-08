"""Project invariants: each gate checks a fact the results depend on, and proves on corrupted data that it can fail.

Usage: python -m radibert.invariantes [--only I1 I3]
Exit 0 = every gate passed or was skipped; 1 = a gate failed; 2 = a positive control did not fail (the gate rotted).
A gate whose input is missing (the e-SNLI is outside git) is reported as PULOU, never as a pass.
"""
import argparse
import re
import sys
from collections.abc import Callable
from dataclasses import dataclass

import pandas as pd

from radibert import eco, lote
from radibert.paths import ESNLI_DEV, LOTE_35B

BATCH = LOTE_35B / "racionalizacoes-F-35B.csv"
MARKS = LOTE_35B / "marcas.csv"
SHEET = LOTE_35B / "leitura-50-cega.md"
KEY = LOTE_35B / "leitura-50-gabarito.csv"

BATCH_ROWS = 16000  # batch of 27/10 (HANDOFF 31/10)
BATCH_ECHO = 1252  # echo marks of 28/10 (HANDOFF 31/10)
DEV_ECHO_PCT_OF_ENTAILMENT = 25.4  # docs/2026-10-21-pesquisa-eco-justificativa.md:19
LABELS = {"entailment", "neutral", "contradiction"}
SOURCE_WORDS = re.compile(r"qwen|wiegreffe|gpt|votos", re.IGNORECASE)


@dataclass
class Gate:
    title: str
    load: Callable[[], object | None]  # None = input missing
    check: Callable[[object], list[str]]  # problems found; empty = pass
    corrupt: Callable[[object], object]  # a copy with one known defect


def batch_problems(df: pd.DataFrame) -> list[str]:
    problems = []
    if len(df) != BATCH_ROWS:
        problems.append(f"{len(df)} linhas, esperado {BATCH_ROWS}")
    if list(df.columns) != lote.FIELDS:
        problems.append(f"colunas {list(df.columns)}")
    if df["pairID"].duplicated().any():
        problems.append("pairID repetido")
    if df[["qwen", "Sentence1", "Sentence2"]].isna().any().any() or (df["qwen"].str.strip() == "").any():
        problems.append("texto vazio")
    if (df["finish_reason"] != "stop").any():
        problems.append(f"{(df['finish_reason'] != 'stop').sum()} sem finish_reason=stop")
    if not set(df["gold_label"]) <= LABELS:
        problems.append(f"rótulos {set(df['gold_label']) - LABELS}")
    return problems


def corrupt_batch(df: pd.DataFrame) -> pd.DataFrame:
    bad = df.copy()
    bad.loc[0, "finish_reason"] = "length"
    return bad


def load_sample_ids() -> tuple[set, set] | None:
    if not all(p.exists() for p in lote.TRAIN):
        return None
    first = lote.shuffle_usable(lote.read_train())["pairID"].head(BATCH_ROWS)
    return set(pd.read_csv(BATCH, usecols=["pairID"])["pairID"]), set(first)


def sample_problems(ids: tuple[set, set]) -> list[str]:
    batch, sample = ids
    return [] if batch == sample else [f"{len(batch - sample)} pares do lote fora dos {BATCH_ROWS} primeiros da amostra"]


def corrupt_sample(ids: tuple[set, set]) -> tuple[set, set]:
    batch, sample = ids
    return (batch - {next(iter(batch))}) | {"par-inexistente"}, sample


def sheet_items(text: str) -> list[str]:
    return re.split(r"\n## \d+\. ", text)[1:]


def sheet_problems(data: tuple[str, pd.DataFrame]) -> list[str]:
    text, key = data
    items = sheet_items(text)
    problems = [] if len(items) == len(key) else [f"{len(items)} itens na folha, {len(key)} no gabarito"]
    for n, (item, expl) in enumerate(zip(items, key.sort_values("n")["justificativa"]), start=1):
        if SOURCE_WORDS.search(item):
            problems.append(f"item {n} cita a fonte")
        if expl not in item:
            problems.append(f"item {n} não traz a justificativa do gabarito")
    return problems


def corrupt_sheet(data: tuple[str, pd.DataFrame]) -> tuple[str, pd.DataFrame]:
    text, key = data
    return text.replace("\n## 1. ", "\n## 1. (Qwen) ", 1), key


def batch_echo_problems(data: tuple[pd.DataFrame, pd.DataFrame]) -> list[str]:
    batch, marks = data
    fresh = eco.mark(batch).drop(columns="gold_label").reset_index(drop=True)
    problems = [] if fresh.equals(marks) else ["marcas.csv difere da regra aplicada ao lote"]
    if marks["eco"].sum() != BATCH_ECHO:
        problems.append(f"eco = {marks['eco'].sum()}, esperado {BATCH_ECHO}")
    return problems


def corrupt_batch_echo(data: tuple[pd.DataFrame, pd.DataFrame]) -> tuple[pd.DataFrame, pd.DataFrame]:
    batch, marks = data
    bad = marks.copy()
    bad.loc[0, "eco"] = not bad.loc[0, "eco"]
    return batch, bad


def dev_echo_problems(dev: pd.DataFrame) -> list[str]:
    marks = eco.mark(dev)
    pct = round(100 * marks.loc[marks["gold_label"] == "entailment", "eco"].mean(), 1)
    return [] if pct == DEV_ECHO_PCT_OF_ENTAILMENT else [f"eco em {pct}% das implicações, esperado 25.4%"]


def corrupt_dev(dev: pd.DataFrame) -> pd.DataFrame:
    bad = dev.copy()
    bad.loc[bad["gold_label"] == "entailment", "Sentence2"] = "zzz"
    return bad


GATES = {
    "I1": Gate("lote: 16.000 linhas, colunas, sem texto vazio, todos com stop",
               lambda: pd.read_csv(BATCH), batch_problems, corrupt_batch),
    "I2": Gate("lote = os 16.000 primeiros da amostra com semente 42 (precisa do e-SNLI)",
               load_sample_ids, sample_problems, corrupt_sample),
    "I3": Gate("folha cega sem a fonte e igual ao gabarito",
               lambda: (SHEET.read_text(encoding="utf-8"), pd.read_csv(KEY)), sheet_problems, corrupt_sheet),
    "I4": Gate("marcas.csv = regra de eco aplicada ao lote; 1.252 ecos",
               lambda: (pd.read_csv(BATCH), pd.read_csv(MARKS)), batch_echo_problems, corrupt_batch_echo),
    "I5": Gate("regra de eco no dev: 25,4% das implicações (precisa do e-SNLI)",
               lambda: pd.read_csv(ESNLI_DEV) if ESNLI_DEV.exists() else None, dev_echo_problems, corrupt_dev),
}


def run(names: list[str]) -> int:
    worst = 0
    for name in names:
        gate = GATES[name]
        data = gate.load()
        if data is None:
            print(f"{name} PULOU  {gate.title}: entrada ausente")
            continue
        if not gate.check(gate.corrupt(data)):
            print(f"{name} CONTROLE MORTO  {gate.title}: o dado estragado passou")
            worst = 2
            continue
        problems = gate.check(data)
        print(f"{name} {'FALHOU' if problems else 'ok'}  {gate.title}" + "".join(f"\n    {p}" for p in problems))
        worst = max(worst, 1 if problems else 0)
    return worst


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--only", nargs="+", choices=list(GATES), default=list(GATES))
    sys.exit(run(parser.parse_args().only))
