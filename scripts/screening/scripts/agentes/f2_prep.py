"""F2 (26/09): sorteio por grupo (camada_B_grupo_final) com a tabela de amostra decidida em 23/09 e as rotas do M6
para abstract ausente (floresta -> S2 -> arXiv -> OpenAlex). Entrada = decisões da F1 de 24/09. Semente 2609.
Grava docs/screening/fase1/F2/entrada.json (ids F0001...), mapa.json (id -> obra) e lotes do agente 1 (40 por lote)."""
import csv, glob, json, os, random, re, time, urllib.request
from collections import defaultdict

ROOT = r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial"
F1 = os.path.join(ROOT, "Screening", "fase1")
OUT = os.path.join(F1, "F2")
os.makedirs(OUT, exist_ok=True)
SEED = 2609

rows = [r for r in csv.DictReader(open(os.path.join(F1, "2026-09-22-floresta-obras.csv"), encoding="utf-8-sig"))
        if r["para_camada_C"] == "sim"]
entra = lambda r: r["camada_C_F1"] in ("ligada", "solta recente (2025-26)", "sem dado de citação") or \
    (r["camada_C_F1"] == "solta (desce)" and r["tipo_no_titulo"] == "True")
f2 = [r for r in rows if entra(r)]
key = lambda x: x["s2"] if x["s2"] else f"ARXIV:{x['arxiv']}"

def amostra(n):
    return 50 if n >= 1000 else 40 if n >= 800 else 30 if n >= 100 else round(0.3 * n) if n >= 50 else n

grupos = defaultdict(list)
for r in f2:
    grupos[r["camada_B_grupo_final"]].append(r)
rng = random.Random(SEED)
sel = []
for g in sorted(grupos, key=lambda g: (len(g), g)):
    membros = sorted(grupos[g], key=key)
    sel += [(g, len(membros), r) for r in rng.sample(membros, amostra(len(membros)))]

abs_by = {}
for path in glob.glob(os.path.join(F1, "raw", "2026-09-22-exec3-*-*.json")):
    if "passo0" in path:
        continue
    for p in json.load(open(path, encoding="utf-8"))["papers"]:
        a = p.get("abstract") or p.get("summary") or ""
        k = p.get("paperId") or ("ARXIV:" + re.sub(r"v\d+$", "", p.get("id") or ""))
        if a and len(a) > len(abs_by.get(k, "")):
            abs_by[k] = a

def get(url, data=None, tries=5):
    for t in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"} if data else {})
            return urllib.request.urlopen(req, timeout=60).read()
        except Exception:
            time.sleep(6 * (t + 1))
    return None

rotas = {key(r): ["floresta:" + ("ok" if abs_by.get(key(r)) else "vazio")] for _, _, r in sel}
falta = [r for _, _, r in sel if not abs_by.get(key(r))]
s2 = [r for r in falta if r["s2"]]
for i in range(0, len(s2), 400):
    lote = s2[i:i + 400]
    res = get("https://api.semanticscholar.org/graph/v1/paper/batch?fields=abstract",
              json.dumps({"ids": [r["s2"] for r in lote]}).encode())
    res = json.loads(res) if res else [None] * len(lote)
    for r, m in zip(lote, res):
        ok = bool(m and m.get("abstract"))
        if ok:
            abs_by[key(r)] = m["abstract"]
        rotas[key(r)].append("S2:" + ("ok" if ok else "vazio"))
for r in falta:
    if abs_by.get(key(r)):
        continue
    if r["arxiv"]:
        x = get(f"http://export.arxiv.org/api/query?id_list={r['arxiv']}")
        m = re.search(r"<entry>.*?<summary>(.*?)</summary>", x.decode(), re.S) if x else None
        if m:
            abs_by[key(r)] = re.sub(r"\s+", " ", m.group(1)).strip()
        rotas[key(r)].append("arXiv:" + ("ok" if m else "vazio"))
        time.sleep(3)
    if not abs_by.get(key(r)) and r["doi"]:
        x = get(f"https://api.openalex.org/works/doi:{r['doi']}")
        inv = (json.loads(x).get("abstract_inverted_index") or {}) if x else {}
        if inv:
            abs_by[key(r)] = " ".join(t for _, t in sorted((i, t) for t, ii in inv.items() for i in ii))
        rotas[key(r)].append("OpenAlex:" + ("ok" if inv else "vazio"))
    if not abs_by.get(key(r)) and not r["arxiv"] and not r["doi"]:
        rotas[key(r)].append("sem arXiv nem DOI")

ordem = list(range(len(sel))); random.Random(SEED + 1).shuffle(ordem)   # lotes misturam grupos
entrada, mapa = [], {}
for n, i in enumerate(ordem):
    g, tam, r = sel[i]
    fid = f"F{n + 1:04d}"
    a = abs_by.get(key(r), "")
    entrada.append({"id": fid, "title": r["title"], "year": r["year"], "abstract": a,
                    "acesso": "ok" if a else "sem acesso", "rotas": rotas[key(r)]})
    mapa[fid] = {"grupo": g, "tam_grupo": tam, "amostra_grupo": amostra(tam), "chave": key(r), "s2": r["s2"],
                 "arxiv": r["arxiv"], "doi": r["doi"], "title": r["title"], "year": r["year"],
                 "camada_C_F1": r["camada_C_F1"], "cit": r["cit"]}
json.dump(entrada, open(os.path.join(OUT, "entrada.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(mapa, open(os.path.join(OUT, "mapa.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
os.makedirs(os.path.join(OUT, "a1"), exist_ok=True)
for j in range(0, len(entrada), 40):
    json.dump(entrada[j:j + 40], open(os.path.join(OUT, "a1", f"lote{j // 40 + 1:02d}-entrada.json"), "w",
                                      encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(entrada), "obras |", len(grupos), "grupos |", sum(e["acesso"] == "ok" for e in entrada), "com abstract |",
      (len(entrada) + 39) // 40, "lotes do agente 1")
