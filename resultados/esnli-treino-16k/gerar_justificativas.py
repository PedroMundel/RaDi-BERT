"""What does the decoder arm write for pairs it never saw? (docs/2026-11-18-o-que-o-decoder-gera.md, written before
this ran; Pedro, 18/11: "bota pra gerar so por gerar".)

Trains the `bert_decoder` arm once (seed 1) on the 16,000 e-SNLI pairs with the recipe of the 16k grid, without the
gradient measures (they read a copy and do not change training), saves its weights, grades the classifier on the
whole dev, and has the decoder write a rationale for 200 dev pairs drawn once. The decoder reads the encoder's
vectors of the pair alone, as in training: it is never told the predicted label.

    uv run --frozen python resultados/esnli-treino-16k/gerar_justificativas.py [--fumaca]
A rerun loads the saved weights instead of training again.
"""
import argparse
import time
from pathlib import Path

import pandas as pd
import torch
from transformers.modeling_outputs import BaseModelOutput

from radibert import esnli_dados as esnli
from radibert import rte_dados as dados
from radibert import rte_treino as treino
from radibert.paths import ESNLI_DEV
from radibert.rte_modelo import RationaleBert, classifier_only, run_encoder

OUT_DIR = Path(__file__).parent.with_name("esnli-treino-16k-gerado")
ARM, SEED, WARMUP = "bert_decoder", 1, "500"
N_GENERATED, SAMPLE_SEED, MAX_NEW_TOKENS, GENERATE_BATCH = 200, 0, 64, 32


@torch.no_grad()
def generate(model: RationaleBert, items: list[dict], tok_t5, device: torch.device) -> list[str]:
    """Greedy decoding over the encoder's vectors of each pair (through the bridge when there is one), as decode()
    feeds the decoder in training. In fp32."""
    model.to(device).eval()
    texts = []
    for start in range(0, len(items), GENERATE_BATCH):
        batch = treino.to_device(dados.collate(items[start:start + GENERATE_BATCH]), device)
        h = run_encoder(model.bert, batch).last_hidden_state
        memory = model.bridge(h) if model.bridge is not None else h
        ids = model.t5.generate(encoder_outputs=BaseModelOutput(last_hidden_state=memory),
                                attention_mask=batch["attention_mask"], max_new_tokens=MAX_NEW_TOKENS,
                                do_sample=False, num_beams=1)
        texts += tok_t5.batch_decode(ids, skip_special_tokens=True)
    return texts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fumaca", action="store_true", help="CPU, tiny BERT, 48 pairs, 10 generated, own folder")
    args = parser.parse_args()
    treino.code_version()  # fails at once without git, not after the training
    if args.fumaca:
        out_dir, device, encoder = OUT_DIR / "fumaca", torch.device("cpu"), dados.TINY
        batch_size, epochs, n_generated = 16, 2, 10
        tok = dados.load_tokenizers(encoder)
        data = treino.load_data(tok, out_dir, treino.TASKS["esnli16k"], n_pairs=48, group_probe=9, word_probe=3)
    else:
        out_dir, device, encoder = OUT_DIR, torch.device("cuda"), dados.BERT
        batch_size, epochs, n_generated = treino.BATCH_SIZE, treino.EPOCHS, N_GENERATED
        tok = dados.load_tokenizers(encoder)
        data = treino.load_data(tok, out_dir, treino.TASKS["esnli16k"])
    weights = out_dir / f"modelo-{ARM}-semente-{SEED}.pt"

    torch.manual_seed(SEED)  # as run_one: head initialization
    model, _ = treino.build_model(ARM, encoder, len(data.labels))
    start = time.perf_counter()
    if weights.exists():
        model.load_state_dict(torch.load(weights, map_location="cpu"))
        print(f"pesos carregados de {weights.name}", flush=True)
    else:
        plan = treino.make_plan(len(data.train), WARMUP, batch_size, epochs)
        treino.train(model, plan, data.train, SEED, device, batch_size)
        torch.save(model.state_dict(), weights)
    seconds = round(time.perf_counter() - start)

    probs = treino.predict(classifier_only(model), data.dev, device)
    scores = treino.metrics(data.dev_y, probs, data.labels)
    pd.DataFrame([{"arm": ARM, "seed": SEED, "warmup": WARMUP, "accuracy": scores["accuracy"],
                   "roc_auc": scores["roc_auc"], "n_train": len(data.train), "seconds": seconds,
                   "device": str(device), "code": treino.code_version()}]).to_csv(out_dir / "resultados.csv",
                                                                                 index=False)
    print(f"dev: acuracia {scores['accuracy']:.4f} roc_auc {scores['roc_auc']:.4f}", flush=True)

    dev = esnli.dev_pairs()
    human = pd.read_csv(ESNLI_DEV, usecols=["Explanation_1"])["Explanation_1"]
    chosen = dev.sample(n_generated, random_state=SAMPLE_SEED).index  # positions in dev, data.dev and probs
    texts = generate(model, [data.dev[i] for i in chosen], tok.t5, device)
    rows = [{"idx": int(dev.at[i, "idx"]), "premise": dev.at[i, "sentence1"], "hypothesis": dev.at[i, "sentence2"],
             "gold": esnli.LABELS[int(dev.at[i, "y"])], "predicted": esnli.LABELS[int(probs[i].argmax())],
             **{f"p_{name}": round(float(probs[i][y]), 4) for y, name in esnli.LABELS.items()},
             "generated": text, "human_explanation_1": human.iat[int(dev.at[i, "idx"])]}
            for i, text in zip(chosen, texts)]
    pd.DataFrame(rows).to_csv(out_dir / "geradas.csv", index=False)
    print(f"completo: {len(rows)} justificativas em {out_dir / 'geradas.csv'}", flush=True)


if __name__ == "__main__":
    main()
