"""Artefatos da F2 (27/09) a partir de consolidado.json: vereditos.csv (uma linha por obra lida), sem-acesso.md
(M6, com prioridade), auditoria.md (30 vereditos sorteados para o Pedro) e contagens das duas variantes da regra
de grupo. Não grava na tabela-mestra."""
import csv, glob, json, os, re
from collections import Counter

ROOT = r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial"
F2 = os.path.join(ROOT, "Screening", "fase1", "F2")
C = json.load(open(os.path.join(F2, "consolidado.json"), encoding="utf-8"))
M = json.load(open(os.path.join(F2, "mapa.json"), encoding="utf-8"))
E = {e["id"]: e for e in json.load(open(os.path.join(F2, "entrada.json"), encoding="utf-8"))}
V = C["V"]

def le(q):
    t = open(q, encoding="utf-8-sig").read()
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        return json.loads(re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', t))
A1, A2, A3 = {}, {}, {}
for d, et in ((A1, "a1"), (A2, "a2"), (A3, "a3")):
    for q in glob.glob(os.path.join(F2, et, "lote??-saida.json")):
        for x in le(q):
            d[x["id"]] = x

with open(os.path.join(F2, "vereditos.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "grupo", "tam_grupo", "camada_C_F1", "ano", "titulo", "veredito", "regra", "objetivo", "frase",
                "motivo", "rotas_acesso", "s2", "doi", "arxiv"])
    for i in sorted(V):
        x = A3.get(i, {}) if V[i] not in ("claramente fora (a1)", "sem acesso") else {}
        mot = A1[i].get("motivo", "") if V[i] == "claramente fora (a1)" else x.get("motivo", "")
        m = M[i]
        w.writerow([i, m["grupo"], m["tam_grupo"], m["camada_C_F1"], m["year"], m["title"], V[i], x.get("regra", ""),
                    x.get("objetivo") or "", x.get("frase", ""), mot, " > ".join(E[i]["rotas"]), m["s2"], m["doi"], m["arxiv"]])

NUCLEO = re.compile(r"compress|quantiz|prun|distill|efficien|inference|serving|edge|lightweight|on-device|"
                    r"\bLLMs?\b|language model|transformer|accelerat|deploy|embedded|tinyml|low-rank|sparsit", re.I)
sa = sorted([i for i in V if V[i] == "sem acesso"], key=lambda i: (not NUCLEO.search(M[i]["title"]), -int(M[i]["cit"] or 0)))
with open(os.path.join(F2, "sem-acesso.md"), "w", encoding="utf-8") as f:
    f.write("# F2 — obras sem acesso (M6), 27/09\n\nNenhum agente decidiu sobre estas obras e nenhuma foi eliminada. Rotas tentadas: "
            "floresta -> S2 -> arXiv (se houver id) -> OpenAlex (se houver DOI) -> Crossref (DOI) / busca do S2 por título. "
            "Falta a rota de PDF aberto. **Prioridade:** termo núcleo da área no título primeiro, depois citações.\n\n"
            f"Total: **{len(sa)}**; com termo núcleo no título: **{sum(1 for i in sa if NUCLEO.search(M[i]['title']))}**.\n\n"
            "| prioridade | id | grupo | ano | cit. | título | DOI | rotas |\n|---|---|---|---|---|---|---|---|\n")
    for i in sa:
        p = "alta" if NUCLEO.search(M[i]["title"]) else "normal"
        f.write(f"| {p} | {i} | {M[i]['grupo']} | {M[i]['year']} | {M[i]['cit']} | {M[i]['title'].replace('|', '/')} | "
                f"{M[i]['doi']} | {' > '.join(E[i]['rotas'])} |\n")

aud = json.load(open(os.path.join(F2, "auditoria-ids.json")))
with open(os.path.join(F2, "auditoria.md"), "w", encoding="utf-8") as f:
    f.write("# F2 — auditoria do Pedro (M4.3): 30 vereditos sorteados do agente 3\n\nPara cada obra: o veredito, a regra e a "
            "frase que o agente usou, e o abstract completo para conferir. Marque na coluna da sua cabeça: **concordo / "
            "discordo**. Semente 2611.\n\n")
    for n, i in enumerate(aud, 1):
        x = A3[i]
        f.write(f"## {n}. {i} — {M[i]['title']} ({M[i]['year']})\n\n- **Veredito final:** {V[i]} · **regra:** "
                f"{x.get('regra', '')} · **objetivo:** {x.get('objetivo') or '—'}\n- **Frase usada:** \"{x.get('frase', '')}\"\n"
                f"- **Motivo do agente:** {x.get('motivo', '')}\n- **Abstract:** {E[i]['abstract'] or '(sem abstract)'}\n\n")

# variantes da regra de grupo
def f3(conta_duvida):
    seguem, descem, obras = [], [], 0
    for l in C["linhas"]:
        ids = l["ids"]; amostrado = l["amostra"] < l["tam"]
        pos = l["relevante"] + (l["dúvida"] if conta_duvida else 0)
        vivos = sum(1 for i in ids if V[i] == "relevante" or (V[i] == "dúvida"))
        if not amostrado:
            obras += vivos
        elif pos == 0:
            descem.append(l["grupo"])
        else:
            seguem.append(l["grupo"]); obras += (l["tam"] - l["amostra"]) + vivos
    return seguem, descem, obras
for cd in (True, False):
    s, d, o = f3(cd)
    print(("A (dúvida mantém o grupo)" if cd else "B (só relevante mantém)"), "| seguem", s, "| descem", d, "| obras para F3:", o)
print("sem acesso:", len(sa), "| alta:", sum(1 for i in sa if NUCLEO.search(M[i]["title"])))
