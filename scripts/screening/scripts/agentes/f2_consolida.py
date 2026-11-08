"""Consolida a F2 (26/09): confere saídas, verbatim do agente 2, concordância da dupla leitura, proposta por grupo
(regra do três), lista sem acesso e amostra de auditoria. NÃO grava na tabela-mestra: a classificação de grupo só
se aplica depois de o Pedro revisar grupo a grupo (Rejected, 23/09)."""
import csv, glob, json, os, random, re
from collections import Counter, defaultdict

ROOT = r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial"
F2 = os.path.join(ROOT, "Screening", "fase1", "F2")
E = {e["id"]: e for e in json.load(open(os.path.join(F2, "entrada.json"), encoding="utf-8"))}
M = json.load(open(os.path.join(F2, "mapa.json"), encoding="utf-8"))

def le(q):
    """Leitura tolerante: BOM e barra invertida sem escape (LaTeX copiado do abstract). O arquivo não é alterado."""
    t = open(q, encoding="utf-8-sig").read()
    try:
        return json.loads(t)
    except json.JSONDecodeError:
        return json.loads(re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', t))

def carrega(base, etapa):
    out, faltam = {}, []
    for p in sorted(glob.glob(os.path.join(base, "a1", "lote*-entrada.json"))):
        n = re.search(r"lote(\d+)", p).group(1)
        q = os.path.join(base, etapa, f"lote{n}-saida.json")
        if not os.path.exists(q):
            faltam.append(n); continue
        for x in le(q):
            out[x["id"]] = x
    return out, faltam

A1, f1 = carrega(F2, "a1"); A2, f2 = carrega(F2, "a2"); A3, f3 = carrega(F2, "a3")
print("lotes sem saída: a1", f1, "a2", f2, "a3", f3)
esperado2 = {i for i, x in A1.items() if x["decisao"] != "claramente fora"}
print("obras: a1", len(A1), "/", len(E), "| a2", len(A2), "/", len(esperado2), "| a3", len(A3), "/", len(esperado2))
falta3 = sorted(i for i in esperado2 - set(A3) if E[i]["acesso"] == "ok")
print("faltando em a3 (com acesso):", len(falta3), falta3[:30])
json.dump(falta3, open(os.path.join(F2, "faltantes-a3.json"), "w"))

# verbatim
norm = lambda s: re.sub(r"\s+", " ", s.replace("[título]", "").replace("’", "'").replace("‘", "'")
                        .replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-")).strip().lower()
nv, tot = [], 0
for i, x in A2.items():
    src = norm(E[i]["title"] + " " + E[i]["abstract"])
    for f in x.get("frases", []):
        tot += 1
        if norm(f["texto"]) not in src:
            nv.append((i, f["item"], f["texto"]))
print(f"frases {tot} | não verbatim {len(nv)} ({100 * len(nv) / max(tot, 1):.1f}%)")

# veredito final por obra
def final(i):
    if A1.get(i, {}).get("decisao") == "claramente fora": return "claramente fora (a1)"
    if E[i]["acesso"] != "ok": return "sem acesso"
    if i in A3: return A3[i]["veredito"]
    return "sem saída"
V = {i: final(i) for i in E}
print("vereditos:", Counter(V.values()))
print("objetivo:", Counter(A3[i].get("objetivo") for i in A3 if A3[i]["veredito"] == "relevante"))

# dupla leitura
D = os.path.join(F2, "dupla")
B1, _ = carrega(D, "a1"); B3, _ = carrega(D, "a3")
def fd(i): return "claramente fora (a1)" if B1.get(i, {}).get("decisao") == "claramente fora" else "sem acesso" if E[i]["acesso"] != "ok" else B3[i]["veredito"] if i in B3 else "sem saída"
grosso = lambda v: "passa" if v in ("relevante", "dúvida") else v if v == "sem acesso" else "fora"
par = [(V[i], fd(i)) for i in B1 if i in V]
conc = sum(a == b for a, b in par); conc_g = sum(grosso(a) == grosso(b) for a, b in par)
print(f"dupla: {len(par)} obras | concordância exata {conc}/{len(par)} | segue x fora {conc_g}/{len(par)}")
discord = [(i, V[i], fd(i)) for i in B1 if i in V and grosso(V[i]) != grosso(fd(i))]

# proposta por grupo
G = defaultdict(list)
for i, m in M.items():
    G[m["grupo"]].append(i)
linhas = []
for g, ids in sorted(G.items(), key=lambda kv: -M[kv[1][0]]["tam_grupo"]):
    tam = M[ids[0]]["tam_grupo"]; c = Counter(V[i] for i in ids)
    lidas = sum(v for k, v in c.items() if k not in ("sem acesso", "sem saída"))
    pos = c["relevante"] + c["dúvida"]
    amostrado = len(ids) < tam
    if not amostrado:
        prop = "lido inteiro: cada obra segue o próprio veredito"
    elif pos == 0:
        prop = f"**desce inteiro** (0/{lidas}: < {300 / max(lidas, 1):.0f}% relevantes, 95%)"
    else:
        prop = "segue para a F3"
    linhas.append({"grupo": g, "tam": tam, "amostra": len(ids), "lidas": lidas, "relevante": c["relevante"],
                   "dúvida": c["dúvida"], "fora": c["fora"] + c["claramente fora (a1)"], "sem acesso": c["sem acesso"],
                   "proposta": prop, "ids": ids})
json.dump({"linhas": linhas, "nv": nv, "discord": discord, "V": V}, open(os.path.join(F2, "consolidado.json"), "w",
          encoding="utf-8"), ensure_ascii=False, indent=1)
# auditoria: 30 vereditos sorteados entre os que o agente 3 julgou
aud = random.Random(2611).sample(sorted(A3), min(30, len(A3)))
json.dump(aud, open(os.path.join(F2, "auditoria-ids.json"), "w"))
print("grupos que descem:", sum(1 for l in linhas if l["proposta"].startswith("**desce")),
      "| seguem:", sum(1 for l in linhas if l["proposta"] == "segue para a F3"),
      "| lidos inteiros:", sum(1 for l in linhas if l["proposta"].startswith("lido")))
