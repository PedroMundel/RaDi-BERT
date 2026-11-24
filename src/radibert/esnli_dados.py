"""e-SNLI pairs and the 35B F rationales as training items, in the RTE training's columns (rte_dados.encode).

10/11 (AUTONOMIA.md): few pairs, as in the regime where Agrawal saw the largest gain: N_TRAIN pairs drawn once
(SAMPLE_SEED) from the 16,000 of the 35B batch, the same set for both arms; every rationale ended with `stop`. No
cleanup: the F prompt has no repeated opening to cut. Evaluation on the e-SNLI dev (9,842 pairs, disjoint from the
batch by pairID): the test split is not on disk, and nothing is tuned on the dev, which is read once per run.
"""
import numpy as np
import pandas as pd

from radibert.paths import ESNLI_DEV, LOTE_35B

RATIONALES = LOTE_35B / "racionalizacoes-F-35B.csv"
LABELS = {0: "entailment", 1: "neutral", 2: "contradiction"}  # y -> name; also the table's column order
ENTAILMENT = 0  # the y of entailment in LABELS
N_TRAIN, SAMPLE_SEED = 4000, 0
# the batch of 27/10: the PC copy of the CSV has 200 more rows appended on 09/11 (progresso.txt: 16,200), and the
# sample must be the same on both machines
BATCH_PAIRS = 16_000


def as_pairs(frame: pd.DataFrame) -> pd.DataFrame:
    """idx = row number in the source CSV; y from gold_label; sentence1/2 as RTE names them."""
    code = {name: y for y, name in LABELS.items()}
    return pd.DataFrame({"idx": range(len(frame)), "pairID": frame["pairID"], "y": frame["gold_label"].map(code),
                         "sentence1": frame["Sentence1"], "sentence2": frame["Sentence2"]}, index=frame.index)


def batch_pairs() -> pd.DataFrame:
    batch = pd.read_csv(RATIONALES, usecols=["pairID", "gold_label", "Sentence1", "Sentence2", "qwen"],
                        nrows=BATCH_PAIRS)
    return as_pairs(batch).assign(rationale=batch["qwen"])


def training_pairs() -> pd.DataFrame:
    return batch_pairs().sample(N_TRAIN, random_state=SAMPLE_SEED).sort_values("idx").reset_index(drop=True)


def other_pairs(n: int = N_TRAIN, seed: int = SAMPLE_SEED) -> pd.DataFrame:
    """`n` pairs of the batch that are NOT in training_pairs(): what a teacher trains on so that the student's
    pairs are new to it (plan, section 11.3)."""
    pairs = batch_pairs()
    rest = pairs.drop(index=pairs.sample(N_TRAIN, random_state=SAMPLE_SEED).index)
    return rest.sample(n, random_state=seed).sort_values("idx").reset_index(drop=True)


def choice_split() -> tuple[pd.DataFrame, pd.DataFrame]:
    """The 8,000 pairs of the batch that are in neither training_pairs() nor other_pairs(), split once in two halves
    (plan, section 11.4): the pairs that choose between variations (seen by no student and no teacher), and the
    extra pairs that, added to other_pairs(), train the larger teacher."""
    pairs = batch_pairs()
    used = set(training_pairs()["idx"]) | set(other_pairs()["idx"])
    rest = pairs[~pairs["idx"].isin(used)]
    choice = rest.sample(N_TRAIN, random_state=SAMPLE_SEED)
    extra = rest.drop(index=choice.index)
    return (choice.sort_values("idx").reset_index(drop=True), extra.sort_values("idx").reset_index(drop=True))


def rationale_in_input(pairs: pd.DataFrame, alone: bool = False) -> pd.DataFrame:
    """The pairs for a teacher that READS the rationale (docs/2026-11-18-professor-que-le-a-justificativa.md): it
    goes after the hypothesis, behind a separator, so the pair's tokens keep the positions they have without it.
    `alone`: the rationale is the whole input. The `rationale` column stays: the training step counts its tokens
    even for a model with no decoder, which never reads them (as for every teacher so far)."""
    if alone:
        return pairs.assign(sentence1=pairs["rationale"], sentence2="")
    return pairs.assign(sentence2=pairs["sentence2"] + " [SEP] " + pairs["rationale"])


def rationale_of_other_label(pairs: pd.DataFrame, seed: int) -> pd.DataFrame:
    """Every pair gets the rationale of a random pair of the NEXT label (the last label takes from the first), and
    `rationale_y` says which label that is: a rationale that argues for another answer."""
    labels = sorted(pairs["y"].unique())
    if len(labels) < 2:
        raise ValueError("one label only: there is no other label to take a rationale from")
    rng = np.random.default_rng(seed)
    swapped = pairs.assign(rationale_y=-1)
    for position, label in enumerate(labels):
        source = labels[(position + 1) % len(labels)]
        rows, donors = pairs.index[pairs["y"] == label], pairs.index[pairs["y"] == source]
        swapped.loc[rows, "rationale"] = pairs.loc[rng.choice(donors, len(rows)), "rationale"].to_numpy()
        swapped.loc[rows, "rationale_y"] = source
    return swapped


def dev_pairs() -> pd.DataFrame:
    dev = pd.read_csv(ESNLI_DEV, usecols=["pairID", "gold_label", "Sentence1", "Sentence2"])
    return as_pairs(dev).reset_index(drop=True)


def with_rte_labels(pairs: pd.DataFrame) -> pd.DataFrame:
    """The pairs with RTE's two labels (1 entailment, 0 not): neutral and contradiction become 0. For testing an
    RTE-trained model outside its distribution (docs/2026-11-10-plano-teste-fora-da-distribuicao.md)."""
    return pairs.assign(y=(pairs["y"] == 0).astype(int))
