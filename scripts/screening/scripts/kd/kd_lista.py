"""Lista curta de destilação a partir de kd_funil_candidatos.csv (24/09). Regras declaradas no relatório
docs/screening/fase1/2026-09-24-kd-lista-leitura.md. Imprime markdown; não grava nada na tabela-mestra."""
import csv, os

OUT = os.path.dirname(os.path.abspath(__file__))
T = list(csv.DictReader(open(os.path.join(OUT, "kd_funil_candidatos.csv"), encoding="utf-8-sig")))
S = list(csv.DictReader(open(os.path.join(OUT, "kd_funil_surveys.csv"), encoding="utf-8-sig")))
ESPEC_MIN = 0.06   # genéricos ficam <= 0.05, linhagem de destilação >= 0.07 (vão observado nos dados)
COTA = {"história (até 2017)": 5, "era BERT (2018-2021)": 5, "era LLM (2022+)": 5}
for t in T:
    t["y"] = int(t["year"] or 0)
    t["espec"] = float(t["especificidade"])

def ok(t):
    if t["fora_escopo"] or t["espec"] < ESPEC_MIN:
        return False
    if t["y"] >= 2018 and not t["linguagem"]:
        return False
    return not (t["era"] == "era LLM (2022+)" and t["y"] >= 2025)   # 2025-26 = fronteira, fora da base

def linha(t, v):
    arx = f"arXiv {t['arxiv']}" if t["arxiv"] else ""
    return f"| {t[v]} | {t['citada_na_camadaC']} | {t['especificidade']} | {t['year']} | {t['title']} | {arx} |"

cab = "| votos | citada na camada C | especificidade | ano | título | id |\n|---|---|---|---|---|---|"
geral = [s for s in S if "Large Language" not in s["title"]][0]
llm = [s for s in S if "Large Language" in s["title"]][0]
print("## Surveys de entrada\n\n| ano | citações | título | id |\n|---|---|---|---|")
for s in (geral, llm):
    print(f"| {s['year']} | {s['cit']} | {s['title']} | arXiv {s['arxiv']} |")
for era, n in COTA.items():
    v = "votos_2024_26" if "LLM" in era else "votos"
    pool = sorted([t for t in T if t["era"] == era and ok(t)], key=lambda t: (-int(t[v]), -t["espec"]))
    print(f"\n## {era} — lista\n\n{cab}")
    for t in pool[:n]:
        print(linha(t, v))
    print(f"\n**Próximas 3 (quase entraram):**\n\n{cab}")
    for t in pool[n:n + 3]:
        print(linha(t, v))
excecao = sorted([t for t in T if t["fora_escopo"].startswith("visão/CNN") and t["espec"] >= ESPEC_MIN],
                 key=lambda t: -int(t["votos"]))[:6]
print(f"\n## Fora por visão/CNN, mais votadas (exceção possível)\n\n{cab}")
for t in excecao:
    print(linha(t, "votos"))
front = sorted([t for t in T if t["y"] >= 2025 and not t["fora_escopo"] and t["linguagem"] and t["espec"] >= ESPEC_MIN],
               key=lambda t: (-int(t["votos_2024_26"]), -t["espec"]))[:5]
print(f"\n## Fronteira 2025-26 (fora da base)\n\n{cab}")
for t in front:
    print(linha(t, "votos_2024_26"))
