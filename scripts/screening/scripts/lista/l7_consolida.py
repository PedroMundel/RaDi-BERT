"""Leitura por agentes, passo 3 (27/09): consolida as fichas em relatório legível + tabela.
Lê leitura/fichas/NN.json (tolerante a BOM e barra de LaTeX), cruza com manifesto e lista-v2.
Grava leitura/fichas-consolidadas.csv e o relatório docs/screening/fase1/<data>-lista-v2-fichas.md (data em argv[1])."""
import csv, json, os, re, sys
from collections import Counter
ROOT = r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial"
LR = os.path.join(ROOT, "Screening", "fase1", "lista-rapida"); LE = os.path.join(LR, "leitura")
data = sys.argv[1] if len(sys.argv) > 1 else "2026-09-27"
man = json.load(open(os.path.join(LE, "manifesto.json"), encoding="utf-8"))
L = list(csv.DictReader(open(os.path.join(LR, "lista-v2.csv"), encoding="utf-8-sig")))
def le(p):
    t = open(p, encoding="utf-8-sig").read()
    try: return json.loads(t)
    except json.JSONDecodeError: return json.loads(re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', t))
F = {}
for n in range(1, len(L) + 1):
    p = os.path.join(LE, "fichas", f"{n:02d}.json")
    if os.path.exists(p):
        try: F[f"{n:02d}"] = le(p)
        except Exception as e: print("ficha inválida", n, e)
Q = ["P1", "P2", "P3", "P6", "P4a", "P4b", "V", "A", "R"]
sim = lambda f, q: ((f.get("perguntas") or {}).get(q) or {}).get("r", "")
rows = []
for n, it in enumerate(L, 1):
    i = f"{n:02d}"; f = F.get(i)
    if not f: continue
    rows.append({"id": i, "bloco": it["bloco"], "divisao": it["divisao"], "ano": it["ano"], "titulo": it["titulo"],
                 "acesso": (f.get("lido") or {}).get("acesso", ""), "nivel": f.get("nivel", ""), "objetivo": f.get("objetivo", ""),
                 **{q: sim(f, q) for q in Q}, "veredito": f.get("veredito", ""), "bloco_sugerido": f.get("bloco_sugerido", ""),
                 "confianca": f.get("confianca", ""), "veredito_por": f.get("veredito_por", ""), "substituto": f.get("substituto_sugerido", "")})
if not rows: sys.exit("nenhuma ficha")
with open(os.path.join(LE, "fichas-consolidadas.csv"), "w", encoding="utf-8-sig", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
mk = lambda v: {"sim": "●", "parcial": "◐", "não": "·", "nao": "·"}.get((v or "").lower(), "?")
out = [f"# Fichas de leitura da lista rápida v2 ({data})\n",
       "**Procedência:** cada ficha foi escrita por um agente (Claude Sonnet) que leu a obra. Com texto completo, o agente leu",
       "as seções listadas em cada ficha (**nível 2 por agente**: texto lido, mas por subagente e não pela sessão principal).",
       "Só com abstract, é **nível 3**. Nada disto foi lido pelo Pedro. Roteiro: `docs/screening/agentes/roteiro-leitura-lista-v1.md`.\n",
       f"**Fichas prontas: {len(rows)} de {len(L)}.** Acesso: " + ", ".join(f"{k}: {v}" for k, v in Counter(r['acesso'][:15] for r in rows).items()) + ".\n",
       "## 1. Vereditos\n", "| Veredito | Obras |", "|---|---|"]
for v, c in Counter(r["veredito"] for r in rows).most_common(): out.append(f"| {v} | {c} |")
out += ["", "**Os que não são 'manter':**\n", "| id | Título | Bloco atual | Veredito | Sugestão | Por quê | Confiança |", "|---|---|---|---|---|---|---|"]
for r in rows:
    if r["veredito"] != "manter":
        out.append(f"| {r['id']} | {r['titulo'][:70]} | {r['bloco']} | {r['veredito']} | {r['bloco_sugerido'] or r['substituto']} | {r['veredito_por'].replace('|', '/')} | {r['confianca']} |")
out += ["", "## 2. Matriz de cobertura (● sim · ◐ parcial · · não)\n",
        "| id | Título | " + " | ".join(Q) + " | Nível | Objetivo |", "|---|---|" + "---|" * (len(Q) + 2)]
for r in rows:
    out.append(f"| {r['id']} | {r['titulo'][:55]} | " + " | ".join(mk(r[q]) for q in Q) + f" | {r['nivel']} | {r['objetivo']} |")
tot = {q: sum(1 for r in rows if (r[q] or '').lower() == 'sim') for q in Q}
out.append("| | **total com 'sim'** | " + " | ".join(str(tot[q]) for q in Q) + " | | |")
out += ["", "## 3. As fichas\n"]
for r in rows:
    f = F[r["id"]]; l = f.get("lido") or {}
    out += [f"### {r['id']}. {r['titulo']} ({r['ano']})\n",
            f"**Bloco:** {r['bloco']} · **Divisão:** {r['divisao'] or '—'} · **Lido:** {l.get('acesso', '')}; {l.get('secoes_lidas', '')} · "
            f"**Nível:** {f.get('nivel', '')} · **Objetivo:** {f.get('objetivo', '')}\n",
            f.get("resumo", ""), "",
            "**O que responde:** " + "; ".join(f"{q} {sim(f, q)}: {((f.get('perguntas') or {}).get(q) or {}).get('por', '')}" for q in Q if sim(f, q).lower() in ("sim", "parcial")), "",
            f"**Termos que ensina:** {', '.join(f.get('termos_chave') or [])}  ", f"**Pré-requisitos:** {', '.join(f.get('pre_requisitos') or [])}  ",
            f"**Por onde ler:** {f.get('por_onde_ler', '')}  ", f"**Acréscimo:** {f.get('acrescimo', '')}  ",
            f"**Sobreposição:** {'; '.join(f.get('sobreposicao') or []) or '—'}  ",
            f"**Veredito:** {f.get('veredito', '')} ({f.get('confianca', '')}) — {f.get('veredito_por', '')}\n"]
open(os.path.join(ROOT, "Screening", "fase1", f"{data}-lista-v2-fichas.md"), "w", encoding="utf-8").write("\n".join(out))
print("fichas:", len(rows), "| vereditos:", dict(Counter(r["veredito"] for r in rows)))
