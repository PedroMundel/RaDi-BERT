"""T5 alone against the decoder fed by BERT: does putting BERT in place of T5's encoder make the generated rationale
worse? Criterion written before: docs/2026-11-18-o-que-o-decoder-gera.md, "T5 sozinho contra o decoder ligado ao
BERT" (Pedro, 18/11: "teria que comparar com o t5 sem nada pra n precisar julgar as justificativas").

1. Trains `google-t5/t5-base` whole (encoder and decoder) to write the Qwen rationale from the pair, on the same
   16,000 e-SNLI pairs, with the decoder group's optimizer of the Agrawal recipe (5e-5, warmup 500, decay 0.001,
   clip 1.0, 4,000 steps of 32, bf16), seed 1; saves the weights. A rerun loads them.
2. Greedy rationales for the same 200 dev pairs as gerar_justificativas.py (the BERT + decoder ones are read from
   its geradas.csv).
3. Measure 1: the label each rationale argues for, as judged by the BERT base teacher that reads pair + rationale
   (medir_professor_justificativa.py); also on the first human explanation of the same pairs, as a reference.
4. Measure 2: each decoder's mean loss per token on the first human explanation of every dev pair (fp32).
Both measures are paired by pair, with a bootstrap 95% interval of the difference T5 alone minus BERT + decoder.

    uv run --frozen python resultados/esnli-treino-16k/comparar_t5_sozinho.py [--fumaca]
"""
import argparse
import time

import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from torch.optim.lr_scheduler import LambdaLR
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, T5ForConditionalGeneration

from radibert import esnli_dados as esnli
from radibert import rte_dados as dados
from radibert import rte_gradientes as grads
from radibert import rte_treino as treino
from radibert.paths import ESNLI_DEV, RESULTADOS
from radibert.rte_modelo import RationaleBert, classifier_only, run_encoder

OUT_DIR = RESULTADOS / "esnli-treino-16k-gerado"
JUDGE_DIR = RESULTADOS / "rte-pequenos"
SEED, WARMUP_STEPS, MAX_NEW_TOKENS, EVAL_BATCH, BOOTSTRAP = 1, 500, 64, 64, 10_000


def train_t5(items: list[dict], epochs: int, batch_size: int, device) -> T5ForConditionalGeneration:
    """Generation only, from the first step to the last; each batch in micro-batches weighted by their share of the
    batch's target tokens, so the summed gradient is the whole batch's (as rte_treino.accumulated_backward)."""
    torch.manual_seed(SEED)
    model = T5ForConditionalGeneration.from_pretrained(dados.T5).to(device).train()
    opt = torch.optim.AdamW(model.parameters(), lr=treino.LR, eps=treino.ADAM_EPS, betas=treino.ADAM_BETAS,
                            weight_decay=treino.DECODER_WEIGHT_DECAY)
    total = -(-len(items) // batch_size) * epochs
    # the 500 of the criterion; the smoke run (a handful of steps) warms up over a tenth of them
    warmup = WARMUP_STEPS if total > WARMUP_STEPS else max(1, total // 10)
    sched = LambdaLR(opt, treino.linear_schedule(warmup, total))
    loader = DataLoader(items, batch_size=batch_size, shuffle=True, collate_fn=dados.collate,
                        generator=torch.Generator().manual_seed(SEED))
    step, start = 0, time.perf_counter()
    for _ in range(epochs):
        for batch in loader:
            batch = treino.to_device(batch, device)
            n_tokens = int((batch["labels"] != dados.IGNORED).sum())
            for first in range(0, len(batch["y"]), treino.MICRO_BATCH):
                part = grads.rows_of(batch, first, first + treino.MICRO_BATCH)
                with treino.autocast(device):
                    loss = model(input_ids=part["input_ids"], attention_mask=part["attention_mask"],
                                 labels=part["labels"]).loss
                (loss * (int((part["labels"] != dados.IGNORED).sum()) / n_tokens)).backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), treino.CLIP_NORM)
            opt.step()
            opt.zero_grad()
            sched.step()
            step += 1
            if step % treino.PROGRESS_EVERY == 0:
                print(f"  passo {step}/{total} ({time.perf_counter() - start:.0f} s)", flush=True)
    if step != total:
        raise RuntimeError(f"trained {step} steps, planned {total}")
    return model


@torch.no_grad()
def generate_t5(model: T5ForConditionalGeneration, items: list[dict], tok, device) -> list[str]:
    model.to(device).eval()
    texts = []
    for first in range(0, len(items), EVAL_BATCH):
        batch = treino.to_device(dados.collate(items[first:first + EVAL_BATCH]), device)
        ids = model.generate(input_ids=batch["input_ids"], attention_mask=batch["attention_mask"],
                             max_new_tokens=MAX_NEW_TOKENS, do_sample=False, num_beams=1)
        texts += tok.batch_decode(ids, skip_special_tokens=True)
    return texts


def nll_per_pair(logits: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
    """Mean loss per target token of each pair, in fp32."""
    per_token = F.cross_entropy(logits.float().transpose(1, 2), labels, ignore_index=dados.IGNORED, reduction="none")
    real = (labels != dados.IGNORED).float()
    return (per_token * real).sum(1) / real.sum(1)


@torch.no_grad()
def human_loss(forward, items: list[dict], device) -> np.ndarray:
    """Measure 2 for one decoder: `forward(batch)` returns its logits over the target."""
    out = []
    for first in range(0, len(items), EVAL_BATCH):
        batch = treino.to_device(dados.collate(items[first:first + EVAL_BATCH]), device)
        out.append(nll_per_pair(forward(batch), batch["labels"]).cpu())
    return torch.cat(out).numpy()


def judged_labels(judge, pairs: pd.DataFrame, texts, tok_bert, device) -> np.ndarray:
    """The label the judge gives to each pair read with `texts` as its rationale."""
    framed = esnli.rationale_in_input(pairs.assign(rationale=list(texts)))
    items = dados.encode(framed, dados.Tokenizers(tok_bert, tok_bert))
    return treino.predict(judge, items, device).argmax(1)


def paired_interval(diff: np.ndarray) -> tuple[float, float, float]:
    """Mean of a per-pair difference and its bootstrap 95% interval (resampling pairs)."""
    rng = np.random.default_rng(0)
    means = diff[rng.integers(0, len(diff), (BOOTSTRAP, len(diff)))].mean(1)
    return float(diff.mean()), float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fumaca", action="store_true",
                        help="CPU, 48 train pairs, 2 epochs, the smoke files of gerar_justificativas.py and the "
                             "smoke judge, 48 dev pairs in measure 2")
    args = parser.parse_args()
    treino.code_version()
    tok_t5 = AutoTokenizer.from_pretrained(dados.T5)
    tok_bert = AutoTokenizer.from_pretrained(dados.BERT)
    t5_only = dados.Tokenizers(tok_t5, tok_t5)  # the T5 tokenizer joins the pair with </s>
    if args.fumaca:
        out_dir, device, encoder, judge_name, tag = OUT_DIR / "fumaca", torch.device("cpu"), dados.TINY, dados.SMALL, "fumaca"
        train_pairs, batch_size, epochs, n_dev = esnli.batch_pairs().iloc[:48], 16, 2, 48
    else:
        out_dir, device, encoder, judge_name, tag = OUT_DIR, torch.device("cuda"), dados.BERT, dados.BERT, "4000"
        train_pairs, batch_size, epochs, n_dev = esnli.batch_pairs(), treino.BATCH_SIZE, treino.EPOCHS, None

    weights = out_dir / f"modelo-t5-sozinho-semente-{SEED}.pt"
    if weights.exists():
        t5 = T5ForConditionalGeneration.from_pretrained(dados.T5)
        t5.load_state_dict(torch.load(weights, map_location="cpu"))
        print(f"pesos carregados de {weights.name}", flush=True)
    else:
        items = dados.encode(train_pairs, t5_only)
        t5 = train_t5(items, epochs, batch_size, device)
        torch.save(t5.state_dict(), weights)

    # the 200 pairs (10 in the smoke run) of gerar_justificativas.py, in its order
    other = pd.read_csv(out_dir / "geradas.csv")
    dev = esnli.dev_pairs()
    chosen = dev.set_index("idx").loc[other["idx"]].reset_index()
    if not (chosen["sentence2"].to_numpy() == other["hypothesis"].to_numpy()).all():
        raise RuntimeError("the dev pairs do not line up with geradas.csv")
    t5_texts = generate_t5(t5, dados.encode(chosen, t5_only), tok_t5, device)

    judge = classifier_only(RationaleBert.with_mark_attention(judge_name, n_labels=len(esnli.LABELS)))
    judge.load_state_dict(torch.load(JUDGE_DIR / f"professor-justificativa-{tag}.pt", map_location="cpu"))
    judge = judge.to(device).eval()
    human = pd.read_csv(ESNLI_DEV, usecols=["Explanation_1"])["Explanation_1"]
    sources = {"t5_sozinho": t5_texts, "bert_decoder": other["generated"].fillna("").tolist(),
               "humana": human.iloc[chosen["idx"]].tolist()}
    gold = chosen["y"].to_numpy()
    judged = {name: judged_labels(judge, chosen, texts, tok_bert, device) for name, texts in sources.items()}
    rows = pd.DataFrame({"idx": chosen["idx"], "gold": [esnli.LABELS[y] for y in gold],
                         "t5_sozinho": t5_texts} | {f"juiz_{name}": [esnli.LABELS[y] for y in labels]
                                                   for name, labels in judged.items()})
    rows.to_csv(out_dir / "t5-sozinho-geradas.csv", index=False)

    # measure 2 on the first human explanation of every dev pair (48 in the smoke run)
    explained = dev.assign(rationale=human.to_numpy())
    explained = explained.iloc[:n_dev] if n_dev else explained
    t5.to(device).eval()
    loss_t5 = human_loss(lambda b: t5(input_ids=b["input_ids"], attention_mask=b["attention_mask"],
                                      labels=b["labels"]).logits, dados.encode(explained, t5_only), device)
    torch.manual_seed(SEED)
    mixed, _ = treino.build_model("bert_decoder", encoder, len(esnli.LABELS))
    mixed.load_state_dict(torch.load(out_dir / "modelo-bert_decoder-semente-1.pt", map_location="cpu"))
    mixed.to(device).eval()
    del judge

    def mixed_logits(b):
        h = run_encoder(mixed.bert, b).last_hidden_state
        return mixed.t5(encoder_outputs=(mixed.bridge(h) if mixed.bridge is not None else h,),
                        attention_mask=b["attention_mask"], labels=b["labels"]).logits

    loss_mixed = human_loss(mixed_logits, dados.encode(explained, dados.Tokenizers(tok_bert, tok_t5)), device)
    pd.DataFrame({"idx": explained["idx"], "perda_t5_sozinho": loss_t5,
                  "perda_bert_decoder": loss_mixed}).to_csv(out_dir / "perdas-explicacao-humana.csv", index=False)

    right = {name: (labels == gold).astype(float) for name, labels in judged.items()}
    summary = [{"medida": f"juiz da o rotulo certo ({name})", "media": right[name].mean(), "pares": len(gold)}
               for name in sources]
    for name, diff in (("medida 1: t5_sozinho - bert_decoder", right["t5_sozinho"] - right["bert_decoder"]),
                       ("medida 2: perda t5_sozinho - bert_decoder", loss_t5 - loss_mixed)):
        mean, low, high = paired_interval(diff)
        summary.append({"medida": name, "media": mean, "ic95_baixo": low, "ic95_alto": high, "pares": len(diff)})
    summary += [{"medida": "perda media t5_sozinho", "media": float(loss_t5.mean()), "pares": len(loss_t5)},
                {"medida": "perda media bert_decoder", "media": float(loss_mixed.mean()), "pares": len(loss_mixed)}]
    pd.DataFrame(summary).to_csv(out_dir / "comparacao-t5-sozinho.csv", index=False)
    print(pd.DataFrame(summary).to_string(index=False), flush=True)
    print(f"completo {out_dir / 'comparacao-t5-sozinho.csv'}", flush=True)


if __name__ == "__main__":
    main()
