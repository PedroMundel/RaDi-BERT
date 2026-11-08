"""Calibração M4 (26/09): 28 obras de ajuste do gabarito (mesma divisão da camada B e da F1: semente 42, metade 1)
+ 30 sorteadas das excluídas na camada A (semente 26). Monta título + abstract; abstract ausente passa pelas rotas
do M6 (S2 -> arXiv -> OpenAlex). Os ids são embaralhados e anonimizados para os agentes não verem a origem."""
import csv, glob, json, os, random, re, time, urllib.request

ROOT = r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial"
F1 = os.path.join(ROOT, "Screening", "fase1")
OUT = os.path.join(F1, "agentes", "calibracao")
os.makedirs(OUT, exist_ok=True)

allrows = list(csv.DictReader(open(os.path.join(F1, "2026-09-22-floresta-obras.csv"), encoding="utf-8-sig")))
key = lambda x: x["s2"] if x["s2"] else f"ARXIV:{x['arxiv']}"
abs_by = {}
for path in glob.glob(os.path.join(F1, "raw", "2026-09-22-exec3-*-*.json")):
    if "passo0" in path:
        continue
    for p in json.load(open(path, encoding="utf-8"))["papers"]:
        a = p.get("abstract") or p.get("summary") or ""
        k = p.get("paperId") or ("ARXIV:" + re.sub(r"v\d+$", "", p.get("id") or ""))
        if a and len(a) > len(abs_by.get(k, "")):
            abs_by[k] = a

# gabarito, igual a f1_rede.py
v1 = list(csv.DictReader(open(os.path.join(F1, "2026-09-22-volta-1-obras.csv"), encoding="utf-8-sig")))
idx = {}
for x in v1:
    for kk in (x["arxiv"], x["doi"]):
        if kk: idx[kk.lower()] = x
refids = [[c.strip() for c in l.strip().strip("|").split("|")][9].lower()
          for l in open(os.path.join(F1, "2026-09-21-candidatos-string-mae-exec2.md"), encoding="utf-8")
          if re.match(r"\| \d+ \| entra \|", l)]
ref = [idx[i] for i in refids if i in idx]; random.Random(42).shuffle(ref)
aj = ref[:len(ref) // 2]
byk = {key(r): r for r in allrows}
aj_rows = [byk.get(key(r), r) for r in aj]
lixo = [r for r in allrows if r["camada_A"].startswith("excluída")]
lixo_rows = random.Random(26).sample(lixo, 30)

def via_s2(ids):
    req = urllib.request.Request("https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,abstract",
                                 data=json.dumps({"ids": ids}).encode(), headers={"Content-Type": "application/json"})
    for t in range(6):
        try:
            return json.load(urllib.request.urlopen(req, timeout=60))
        except Exception:
            time.sleep(8 * (t + 1))
    return [None] * len(ids)

def via_arxiv(aid):
    try:
        x = urllib.request.urlopen(f"http://export.arxiv.org/api/query?id_list={aid}", timeout=30).read().decode()
        m = re.search(r"<summary>(.*?)</summary>", x, re.S)
        return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
    except Exception:
        return ""

def via_openalex(doi):
    try:
        w = json.load(urllib.request.urlopen(f"https://api.openalex.org/works/doi:{doi}", timeout=30))
        inv = w.get("abstract_inverted_index") or {}
        pos = sorted((i, t) for t, ii in inv.items() for i in ii)
        return " ".join(t for _, t in pos)
    except Exception:
        return ""

itens = [("ajuste", r) for r in aj_rows] + [("lixo_A", r) for r in lixo_rows]
faltam = [r for _, r in itens if not abs_by.get(key(r))]
s2ids = [r["s2"] for r in faltam if r["s2"]]
for r, m in zip([r for r in faltam if r["s2"]], via_s2(s2ids) if s2ids else []):
    if m and m.get("abstract"):
        abs_by[key(r)] = m["abstract"]
out, gab = [], {}
rng = random.Random(7)
ordem = list(range(len(itens))); rng.shuffle(ordem)
for n, i in enumerate(ordem):
    origem, r = itens[i]
    rotas = ["floresta" if abs_by.get(key(r)) else "floresta:vazio"]
    a = abs_by.get(key(r), "")
    if not a and r["s2"]:
        rotas.append("S2:vazio")
    if not a and r["arxiv"]:
        a = via_arxiv(r["arxiv"]); rotas.append("arXiv:" + ("ok" if a else "vazio"))
    if not a and r["doi"]:
        a = via_openalex(r["doi"]); rotas.append("OpenAlex:" + ("ok" if a else "vazio"))
    cid = f"C{n + 1:02d}"
    out.append({"id": cid, "title": r["title"], "year": r["year"], "abstract": a,
                "acesso": "ok" if a else "sem acesso", "rotas": rotas})
    gab[cid] = {"origem": origem, "s2": r["s2"], "arxiv": r["arxiv"], "doi": r["doi"], "title": r["title"]}
json.dump(out, open(os.path.join(OUT, "entrada.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(gab, open(os.path.join(OUT, "gabarito-oculto.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(out), "obras |", sum(1 for o in out if o["acesso"] == "ok"), "com abstract |",
      sum(1 for g in gab.values() if g["origem"] == "ajuste"), "ajuste")
for o in out:
    if o["acesso"] != "ok": print("sem acesso:", o["id"], o["title"][:70], o["rotas"])
