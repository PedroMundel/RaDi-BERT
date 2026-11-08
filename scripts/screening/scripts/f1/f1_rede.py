"""F1 (árvore de citação) — rede interna quem-cita-quem nas 14.901 da camada C.
Regra (desenho-agentes M2): obra sem ligação com o componente onde estão os cajuzeiros conhecidos (metade de
ajuste) desce para o fim da fila; exceção 2025–26; golden ticket e penúltima (⟨rev-36⟩) não passam pela F1.
Ordena, não apaga: grava coluna camada_C_F1 na tabela-mestra."""
import csv, glob, json, os, random, re
from collections import Counter, defaultdict

ROOT = r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial"
F1 = os.path.join(ROOT, "Screening", "fase1")
MESTRA = os.path.join(F1, "2026-09-22-floresta-obras.csv")
REFS = json.load(open(os.path.join(F1, "raw", "2026-09-23-camadaC-F1-referencias.json"), encoding="utf-8"))
SCR = os.path.dirname(os.path.abspath(__file__))

allrows = list(csv.DictReader(open(MESTRA, encoding="utf-8-sig")))
cols = [c for c in allrows[0].keys() if c != "camada_C_F1"] + ["camada_C_F1"]
rows = [r for r in allrows if r["para_camada_C"] == "sim"]
key = lambda x: x["s2"] if x["s2"] else f"ARXIV:{x['arxiv']}"
K = [key(r) for r in rows]
byk = dict(zip(K, rows))

# --- bilhetes (mesmo casamento de termos do bubble_plots.py, 23/09) ---
POOL = open(os.path.join(ROOT, "docs/screening/pool-termos-etapa1.md"), encoding="utf-8").read()
ACRONYM_CASE = {"LoRA", "MoE", "PEFT", "SLMs", "SLM", "PTQ", "QAT", "KV cache", "CoT distillation"}
def heads(group):
    sec = POOL.split(f"### Grupo `{group}`", 1)[1].split("\n### ", 1)[0].split("\n## ", 1)[0]
    out = {}
    for line in sec.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) < 4 or c[0] in ("termo (en)", "") or set(c[0]) <= set("-") or "aposentado" in c[3]:
            continue
        v = re.findall(r'"([^"]+)"', c[1]) + [x.strip() for x in re.sub(r'"[^"]+"', "", c[1]).split(",") if x.strip()]
        out[c[0]] = [h.strip() for h in c[0].split("/")] + v
    return out
def term_re(t):
    flags = 0 if (t.isupper() or t in ACRONYM_CASE) else re.I
    return re.compile(r"(?<![A-Za-z0-9])" + re.escape(t) + r"(?![A-Za-z0-9])", flags)
GROUPS = ["compressão", "inferência/serving", "adaptação", "edge", "dado/confiança", "ferramentas"]
TECH = {h: [term_re(t) for t in terms] for g in GROUPS for h, terms in heads(g).items()}
abs_by = {}
for path in glob.glob(os.path.join(F1, "raw", "2026-09-22-exec3-*-*.json")):
    if "passo0" in path:
        continue
    for p in json.load(open(path, encoding="utf-8"))["papers"]:
        a = p.get("abstract") or p.get("summary") or ""
        k = p.get("paperId") or ("ARXIV:" + re.sub(r"v\d+$", "", p.get("id") or ""))
        if a and len(a) > len(abs_by.get(k, "")):
            abs_by[k] = a
techs = {k: [t for t, rs in TECH.items() if any(x.search(byk[k]["title"] + " " + abs_by.get(k, "")) for x in rs)] for k in K}
tcount = Counter(t for v in techs.values() for t in v)
def bilhete(k):
    n = min((tcount[t] for t in techs[k]), default=10**9)
    return "golden" if n <= 20 else "penúltima" if n <= 50 else None

# --- rede: união S2 (lote + obra a obra) e OpenAlex; ligação vale nos dois sentidos ---
PORO = os.path.join(F1, "raw", "2026-09-23-camadaC-F1-referencias-porobra.json")
PORO = json.load(open(PORO, encoding="utf-8")) if os.path.exists(PORO) else {}
OA = json.load(open(os.path.join(F1, "raw", "2026-09-23-camadaC-F1-openalex.json"), encoding="utf-8"))
pid2k, oa2k = {}, {}
for k in K:
    p = REFS.get(k)
    if p and p.get("paperId"):
        pid2k[p["paperId"]] = k
    o = OA.get(byk[k]["doi"].lower()) if byk[k]["doi"] else None
    if o:
        oa2k[o["id"]] = k
def s2refs(k):
    p = REFS.get(k)
    if not p:
        return None
    if p.get("references"):
        return [r.get("paperId") for r in p["references"] if r]
    q = PORO.get(p["paperId"])
    return q["refs"] if q and q["estado"] == "ok" and q["refs"] else None
def oarefs(k):
    o = OA.get(byk[k]["doi"].lower()) if byk[k]["doi"] else None
    return o["refs"] if o and o["refs"] else None
adj = defaultdict(set); arestas = 0; fonte = {}
for k in K:
    a, b = s2refs(k), oarefs(k)
    fonte[k] = "S2+OpenAlex" if a and b else "S2" if a else "OpenAlex" if b else "nenhuma"
    for j in [pid2k.get(x) for x in (a or [])] + [oa2k.get(x) for x in (b or [])]:
        if j and j != k and j not in adj[k]:
            adj[k].add(j); adj[j].add(k); arestas += 1
sem_refs = sum(1 for v in fonte.values() if v == "nenhuma")
comp = {}; comps = []
for k in K:
    if k in comp:
        continue
    stack, members = [k], []
    comp[k] = len(comps)
    while stack:
        u = stack.pop(); members.append(u)
        for v in adj[u]:
            if v not in comp:
                comp[v] = len(comps); stack.append(v)
    comps.append(members)

# --- gabarito (mesma divisão da camada B: semente 42, metade 1 = ajuste) ---
v1 = list(csv.DictReader(open(os.path.join(F1, "2026-09-22-volta-1-obras.csv"), encoding="utf-8-sig")))
idx = {}
for x in v1:
    for kk in (x["arxiv"], x["doi"]):
        if kk: idx[kk.lower()] = x
refids = [[c.strip() for c in l.strip().strip("|").split("|")][9].lower()
          for l in open(os.path.join(F1, "2026-09-21-candidatos-string-mae-exec2.md"), encoding="utf-8")
          if re.match(r"\| \d+ \| entra \|", l)]
ref = [idx[i] for i in refids if i in idx]; random.Random(42).shuffle(ref)
aj, te = ref[:len(ref) // 2], ref[len(ref) // 2:]
aj_k = [key(r) for r in aj if key(r) in byk]; te_k = [key(r) for r in te if key(r) in byk]
area = Counter(comp[k] for k in aj_k).most_common(1)[0][0]

def f1(k):
    b = bilhete(k)
    if b: return b
    if comp[k] == area: return "ligada"
    if not adj[k] and fonte[k] == "nenhuma": return "sem dado de citação"
    if byk[k]["year"] in ("2025", "2026"): return "solta recente (2025-26)"
    return "solta (desce)"
dest = {k: f1(k) for k in K}
PREVIEW = "--preview" in os.sys.argv
for r in ([] if PREVIEW else allrows):
    r["camada_C_F1"] = dest.get(key(r), "") if r["para_camada_C"] == "sim" else ""
if not PREVIEW:
  with open(MESTRA, "w", encoding="utf-8-sig", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(allrows)

sizes = sorted((len(c) for c in comps), reverse=True)
grau = [len(adj[k]) for k in comps[area]]
out = dict(
    n=len(K), cobertura=Counter(fonte.values()), porobra_coletadas=len(PORO), arestas=arestas,
    componentes=len(comps), maiores=sizes[:10], isoladas=sum(1 for s in sizes if s == 1),
    area_tamanho=len(comps[area]), area_eh_maior=len(comps[area]) == sizes[0],
    grau_area=dict(mediana=sorted(grau)[len(grau) // 2], grau1=sum(1 for g in grau if g == 1), max=max(grau)),
    destino=Counter(dest.values()),
    destino_por_camadaB={b: Counter(dest[k] for k in K if byk[k]["camada_B"] == b) for b in sorted({byk[k]["camada_B"] for k in K})},
    destino_por_ano={y: Counter(dest[k] for k in K if byk[k]["year"] == y) for y in sorted({byk[k]["year"] for k in K})},
    solta_por_tipo=Counter(("survey no título" if byk[k]["tipo_no_titulo"] == "True" else "sem tipo") for k in K if dest[k] == "solta (desce)"),
    ajuste=Counter(dest[k] for k in aj_k), ajuste_n=len(aj_k),
    cobertura_por_destino={d: Counter(fonte[k] for k in K if dest[k] == d) for d in set(dest.values())},
    teste=[(byk[k]["title"], dest[k], len(adj[k]), fonte[k]) for k in te_k], teste_n=len(te_k),
    teste_perdidos_antes=[r["title"] for r in te if key(r) not in byk],
    soltas_mais_citadas=[(byk[k]["cit"], byk[k]["year"], byk[k]["title"]) for k in
                         sorted((k for k in K if dest[k] == "solta (desce)"), key=lambda k: -int(byk[k]["cit"] or 0))[:25]],
    soltas_amostra=[(byk[k]["year"], byk[k]["title"]) for k in random.Random(2309).sample([k for k in K if dest[k] == "solta (desce)"], 25)],
)
json.dump(out, open(os.path.join(SCR, "f1_rede.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps({k: out[k] for k in out if k not in ("teste", "soltas_mais_citadas", "soltas_amostra", "destino_por_ano", "destino_por_camadaB")}, ensure_ascii=False, default=str))
