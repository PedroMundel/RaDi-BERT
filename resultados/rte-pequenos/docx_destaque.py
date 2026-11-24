"""Builds entrega/Exemplos do Destaque.docx from destaque-exemplos-2000.json: the same content as the HTML page
(pagina_destaque.py), in the plain style of the delivered documents (Arial 12, default headings in black), with
Word highlight colors: yellow = marked by the LLM, green = the model picked it and so did the LLM, pink = the model
picked it and the LLM did not.

Usage:  uv run --frozen python resultados/rte-pequenos/docx_destaque.py
"""
import json
from pathlib import Path

from docx import Document
from docx.enum.text import WD_COLOR_INDEX
from docx.shared import Pt, RGBColor

from pagina_destaque import SOURCE, top_k, words_of

OUT = Path(__file__).parents[2] / "entrega" / "Exemplos do Destaque.docx"
LABELS = {1: "implica", 0: "nao implica"}
GOLD, HIT, MISS = WD_COLOR_INDEX.YELLOW, WD_COLOR_INDEX.BRIGHT_GREEN, WD_COLOR_INDEX.PINK
ROWS = (("real", "BERT small treinado com marca real: "), ("none", "BERT small treinado sem marcas: "))


def add_words(par, words: list[dict], chosen: set[int] | None):
    """The words of one row; chosen=None paints the LLM's marks, otherwise the model's picks (hit or miss)."""
    for i, word in enumerate(words):
        text = "|" if word["sep"] else word["text"]
        run = par.add_run(text + " ")
        if word["sep"]:
            continue
        if chosen is None and word["gold"]:
            run.font.highlight_color = GOLD
        elif chosen is not None and i in chosen:
            run.font.highlight_color = HIT if word["gold"] else MISS


def legend(doc):
    par = doc.add_paragraph("Cores: ")
    for text, color in (("marcada pelo LLM", GOLD), ("o modelo apontou e o LLM também", HIT),
                        ("o modelo apontou e o LLM não", MISS)):
        par.add_run(text).font.highlight_color = color
        par.add_run("   ")


def main():
    examples = json.loads(SOURCE.read_text(encoding="utf-8"))
    rows = [(e, words_of(e, None), {k: words_of(e, e["scores"][k]) for k, _ in ROWS}) for e in examples]
    total = sum(w["gold"] for _, gold, _ in rows for w in gold)
    hits = {k: sum(by_kind[k][i]["gold"] for _, _, by_kind in rows for i in top_k(by_kind[k])) for k, _ in ROWS}

    doc = Document()
    for name in ("Normal", "Heading 1", "Heading 2"):
        doc.styles[name].font.name = "Arial"
        doc.styles[name].font.color.rgb = RGBColor(0, 0, 0)
    doc.styles["Normal"].font.size = Pt(12)
    doc.add_heading("Exemplos do Destaque", level=1)
    doc.add_paragraph(
        f"Os {len(examples)} primeiros pares do RTE entre os 470 que o modelo nunca viu no treino (ele treinou em "
        "outros 2.000). Não escolhi os exemplos: é a ordem fixa do embaralhamento. O texto está em minúsculas, como "
        "o modelo lê, e a barra separa a premissa da hipótese.")
    doc.add_paragraph(
        "Em cada par, a primeira linha mostra as palavras do par que a justificativa do LLM (Qwen) repete. As duas "
        "linhas seguintes mostram as palavras em que cada modelo mais presta atenção: o mesmo número de palavras que "
        "o LLM marcou, as de maior atenção do [CLS] na última camada.")
    legend(doc)
    doc.add_paragraph(
        f"Nestes {len(examples)} pares o LLM marcou {total} palavras. Das palavras apontadas por cada modelo, "
        f"coincidem com as do LLM {hits['real']} ({hits['real'] / total:.0%}) no treino com marca real e "
        f"{hits['none']} ({hits['none'] / total:.0%}) no treino sem marcas.")
    doc.add_paragraph(
        "Limites: o gabarito é o que o LLM copiou do par ao justificar o rótulo, e não o que uma pessoa marcaria; o "
        "destaque não mostra o que o modelo usou para decidir. A página e as rodadas foram feitas com LLM (Claude).")
    for n, (example, gold, by_kind) in enumerate(rows, 1):
        doc.add_heading(f"Par {n}: {LABELS[example['y']]}", level=2)
        doc.add_paragraph().add_run("Justificativa do LLM: " + example["rationale"]).italic = True
        par = doc.add_paragraph()
        par.add_run("LLM: ").bold = True
        add_words(par, gold, None)
        for kind, who in ROWS:
            par = doc.add_paragraph()
            par.add_run(who).bold = True
            add_words(par, by_kind[kind], top_k(by_kind[kind]))
    doc.save(OUT)
    print(f"gravado {OUT}: {len(examples)} pares, {total} palavras, real {hits['real']}, none {hits['none']}")


if __name__ == "__main__":
    main()
