"""Builds destaque-exemplos.html from destaque-exemplos-2000.json (medir_destaque.py --pares 2000): for each held
pair, the words the LLM rationale copies next to the words BERT small's [CLS] attends to most, with and without the
real marks in training. Each model highlights as many words as the LLM marked (top-k of its attention).

Usage:  uv run --frozen python resultados/rte-pequenos/pagina_destaque.py
"""
import html
import json
from pathlib import Path

HERE = Path(__file__).parent
SOURCE, OUT = HERE / "destaque-exemplos-2000.json", HERE / "destaque-exemplos.html"
LABELS = {1: "entailment", 0: "not entailment"}

CSS = """
body { font-family: Arial, sans-serif; max-width: 980px; margin: 24px auto; padding: 0 16px; color: #111; background: #fff; }
h1 { font-size: 22px; } h2 { font-size: 16px; margin: 28px 0 6px; }
p.note { color: #444; font-size: 14px; line-height: 1.45; }
table { border-collapse: collapse; width: 100%; font-size: 15px; }
td { border: 1px solid #ccc; padding: 6px 8px; vertical-align: top; line-height: 1.7; }
td.who { width: 150px; font-size: 13px; color: #333; background: #f4f4f4; }
.gold { background: #ffe066; } .hit { background: #8fd694; } .miss { background: #f4a6a6; }
.sep { color: #888; padding: 0 6px; } .rationale { font-size: 14px; color: #333; font-style: italic; }
.legend span { padding: 1px 6px; margin-right: 10px; }
"""


def words_of(example: dict, scores: list[float] | None) -> list[dict]:
    """Wordpieces merged into words: text, whether the LLM marked it, its score (max of its pieces)."""
    marked, words = set(example["marks"]), []
    for pos, token in enumerate(example["tokens"]):
        if token == "[CLS]":
            continue
        score = scores[pos] if scores else 0.0
        if token.startswith("##") and words:
            last = words[-1]
            last["text"] += token[2:]
            last["gold"] = last["gold"] or pos in marked
            last["score"] = max(last["score"], score)
        else:
            words.append({"text": token, "gold": pos in marked, "score": score, "sep": token == "[SEP]"})
    return words[:-1] if words and words[-1]["sep"] else words


def line(words: list[dict], chosen: set[int] | None) -> str:
    """One row of words: the LLM's marks in yellow (chosen=None), or the model's picks, green when the LLM marked
    the word too and red when not."""
    out = []
    for i, word in enumerate(words):
        text = html.escape(word["text"])
        if word["sep"]:
            out.append('<span class="sep">|</span>')
        elif chosen is None:
            out.append(f'<span class="gold">{text}</span>' if word["gold"] else text)
        elif i in chosen:
            out.append(f'<span class="{"hit" if word["gold"] else "miss"}">{text}</span>')
        else:
            out.append(text)
    return " ".join(out)


def top_k(words: list[dict]) -> set[int]:
    k = sum(word["gold"] for word in words)
    ranked = sorted((i for i, word in enumerate(words) if not word["sep"]), key=lambda i: -words[i]["score"])
    return set(ranked[:k])


def main():
    examples = json.loads(SOURCE.read_text(encoding="utf-8"))
    blocks, hits = [], {"real": 0, "none": 0}
    total = 0
    for n, example in enumerate(examples, 1):
        gold = words_of(example, None)
        rows = [f'<tr><td class="who">LLM (palavras que a justificativa copia)</td><td>{line(gold, None)}</td></tr>']
        total += sum(word["gold"] for word in gold)
        for kind, who in (("real", "BERT small treinado com marca real"), ("none", "BERT small treinado sem marcas")):
            words = words_of(example, example["scores"][kind])
            chosen = top_k(words)
            hits[kind] += sum(words[i]["gold"] for i in chosen)
            rows.append(f'<tr><td class="who">{who}</td><td>{line(words, chosen)}</td></tr>')
        blocks.append(f'<h2>Par {n} (idx {example["idx"]}): {LABELS[example["y"]]}</h2>'
                      f'<p class="rationale">Justificativa do LLM: {html.escape(example["rationale"])}</p>'
                      f'<table>{"".join(rows)}</table>')
    summary = (f'Nestes {len(examples)} pares o LLM marcou {total} palavras. Das palavras que cada modelo aponta, '
               f'coincidem com as do LLM: {hits["real"]} ({hits["real"] / total:.0%}) com marca real e '
               f'{hits["none"]} ({hits["none"] / total:.0%}) sem marcas.')
    page = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>Destaque: exemplos</title><style>{CSS}</style></head><body>
<h1>O que o BERT small aponta em pares que nunca viu</h1>
<p class="note">RTE, {len(examples)} primeiros pares dos 470 reservados (o modelo treinou em outros 2.000). Texto em
minúsculas, como o modelo lê; a barra separa premissa e hipótese. Em cada par, cada modelo aponta o mesmo número de
palavras que o LLM marcou: as de maior atenção do [CLS] na última camada. Semente 1.</p>
<p class="note legend"><span class="gold">marcada pelo LLM</span><span class="hit">modelo apontou, LLM também</span>
<span class="miss">modelo apontou, LLM não</span></p>
<p class="note"><b>{summary}</b></p>
<p class="note">Limites: o gabarito é o que o LLM (Qwen 35B) copiou do par ao justificar o rótulo, não o que uma
pessoa marcaria; o destaque não mostra o que o modelo usou para decidir. Exemplos não escolhidos: são os {len(examples)} primeiros
da ordem fixa do embaralhamento.</p>
{"".join(blocks)}
</body></html>"""
    OUT.write_text(page, encoding="utf-8")
    print(summary)
    print(f"gravado {OUT}")


if __name__ == "__main__":
    main()
