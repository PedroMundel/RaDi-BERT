"""ROC-AUC of the MS-MARCO reranker on the RTE dev set with NO training on RTE (10/11).

Question: is Agrawal's 0.4754 baseline (Table 2) what an MS-MARCO BERT gives on RTE when it is not fine-tuned on it?
The checkpoint's own relevance head scores each pair; entailment is the positive class. Both orders of the pair.

    uv run --frozen python resultados/rte-msmarco/zero_shot.py
"""
import torch
from sklearn.metrics import roc_auc_score
from transformers import AutoModelForSequenceClassification, AutoTokenizer

from radibert import rte_dados as dados


@torch.no_grad()
def relevance(model, tok, first: list[str], second: list[str]) -> torch.Tensor:
    scores = []
    for i in range(0, len(first), 32):
        enc = tok(first[i:i + 32], second[i:i + 32], truncation=True, max_length=dados.MAX_INPUT_TOKENS,
                  padding=True, return_tensors="pt")
        logits = model(**enc).logits
        scores.append(logits[:, 1] - logits[:, 0] if logits.shape[1] == 2 else logits[:, 0])
    return torch.cat(scores)


def main():
    tok = AutoTokenizer.from_pretrained(dados.BERT)
    model, info = AutoModelForSequenceClassification.from_pretrained(dados.MSMARCO, output_loading_info=True)
    print("missing keys (must be empty, or the head is random):", info["missing_keys"])
    model.eval()
    pairs = dados.dev_pairs()
    premise, hypothesis, y = list(pairs["sentence1"]), list(pairs["sentence2"]), pairs["y"].to_numpy()
    print(f"{len(pairs)} dev pairs, {y.mean():.3f} entailment, head with {model.config.num_labels} labels")
    for name, (a, b) in {"hypothesis as query, premise as passage": (hypothesis, premise),
                         "premise as query, hypothesis as passage": (premise, hypothesis)}.items():
        print(f"{name}: ROC-AUC {roc_auc_score(y, relevance(model, tok, a, b).numpy()):.4f}")


if __name__ == "__main__":
    main()
