"""Lista rápida, etapa 1 (27/09): júri de surveys vota nas obras que cita.
Júri = 57 do gabarito ('entra') + 55 relevantes da F2 + reserva de hardware (surveys da camada C com termo de hardware
no título e contexto de modelo/IA; decisão do Pedro 27/09: 'hardware é bem importante').
Votos por S2 (referências obra a obra) e OpenAlex (referenced_works), unificados por DOI ou título normalizado.
Grava docs/screening/fase1/lista-rapida/candidatas.csv e juri.csv. Metadado em cache (idempotente)."""
import csv, json, os, re, time, urllib.parse, urllib.request
from collections import Counter, defaultdict

ROOT = r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial"
F1 = os.path.join(ROOT, "Screening", "fase1")
OUT = os.path.join(F1, "lista-rapida"); os.makedirs(OUT, exist_ok=True)
CACHE_S2 = os.path.join(OUT, "cache_s2.json"); CACHE_OA = os.path.join(OUT, "cache_oa.json")

rows = list(csv.DictReader(open(os.path.join(F1, "2026-09-22-floresta-obras.csv"), encoding="utf-8-sig")))
key = lambda x: x["s2"] if x["s2"] else f"ARXIV:{x['arxiv']}"
byk = {key(r): r for r in rows}
norm = lambda t: re.sub(r"[^a-z0-9]", "", (t or "").lower())

# ---- júri ----
v1 = list(csv.DictReader(open(os.path.join(F1, "2026-09-22-volta-1-obras.csv"), encoding="utf-8-sig"))); gi = {}
for x in v1:
    for kk in (x["arxiv"], x["doi"]):
        if kk: gi[kk.lower()] = x
refids = [[c.strip() for c in l.strip().strip("|").split("|")][9].lower()
          for l in open(os.path.join(F1, "2026-09-21-candidatos-string-mae-exec2.md"), encoding="utf-8") if re.match(r"\| \d+ \| entra \|", l)]
juri = {key(gi[i]): "gabarito" for i in refids if i in gi}
M = json.load(open(os.path.join(F1, "F2", "mapa.json"), encoding="utf-8"))
V = json.load(open(os.path.join(F1, "F2", "consolidado.json"), encoding="utf-8"))["V"]
for i in V:
    if V[i] == "relevante": juri.setdefault(M[i]["chave"], "F2")
HW = re.compile(r"accelerat|FPGA|ASIC|hardware|\bNPU|in-memory|processing-in-memory|neuromorphic|systolic|\bchip", re.I)
CTX = re.compile(r"\bLLMs?\b|language model|transformer|deep learning|neural|\bDNN|\bAI\b|inference|machine learning|model", re.I)
for r in rows:
    if r.get("para_camada_C") == "sim" and r["tipo_no_titulo"] == "True" and HW.search(r["title"]) and CTX.search(r["title"]) \
            and r["camada_C_F1"] in ("ligada", "solta recente (2025-26)", "sem dado de citação"):
        juri.setdefault(key(r), "reserva-hardware")

R = json.load(open(os.path.join(F1, "raw", "2026-09-23-camadaC-F1-referencias.json"), encoding="utf-8"))
P = json.load(open(os.path.join(F1, "raw", "2026-09-23-camadaC-F1-referencias-porobra.json"), encoding="utf-8"))
OA = json.load(open(os.path.join(F1, "raw", "2026-09-23-camadaC-F1-openalex.json"), encoding="utf-8"))
def s2refs(k):
    p = R.get(k)
    if not p: return []
    out = [x.get("paperId") for x in (p.get("references") or []) if x and x.get("paperId")]
    if not out: out = (P.get(p["paperId"]) or {}).get("refs") or []
    return sorted({x for x in out if x})
def oarefs(k):
    r = byk.get(k); o = OA.get(r["doi"].lower()) if r and r["doi"] else None
    return sorted(set((o or {}).get("refs") or []))
jr = {k: {"s2": s2refs(k), "oa": oarefs(k)} for k in juri}
votantes = {k: v for k, v in jr.items() if v["s2"] or v["oa"]}

# ---- metadado ----
def get(url, data=None):
    for t in range(6):
        try:
            req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", "User-Agent": "ufg-screening"})
            return json.load(urllib.request.urlopen(req, timeout=120))
        except Exception:
            time.sleep(8 * (t + 1))
    return None
s2c = json.load(open(CACHE_S2, encoding="utf-8")) if os.path.exists(CACHE_S2) else {}
oac = json.load(open(CACHE_OA, encoding="utf-8")) if os.path.exists(CACHE_OA) else {}
s2cnt = Counter(x for v in votantes.values() for x in v["s2"])
oacnt = Counter(x for v in votantes.values() for x in v["oa"])
s2ids = [x for x, n in s2cnt.items() if n >= 2 and x not in s2c]
for i in range(0, len(s2ids), 400):
    res = get("https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,year,citationCount,abstract,venue,externalIds,publicationTypes",
              json.dumps({"ids": s2ids[i:i + 400]}).encode()) or []
    for x, m in zip(s2ids[i:i + 400], res): s2c[x] = m
    json.dump(s2c, open(CACHE_S2, "w", encoding="utf-8"))
oaids = [x for x, n in oacnt.items() if x not in oac]
for i in range(0, len(oaids), 50):
    ids = "|".join(x.rsplit("/", 1)[-1] for x in oaids[i:i + 50])
    res = get(f"https://api.openalex.org/works?per-page=50&filter=openalex_id:{ids}&select=id,title,doi,publication_year,cited_by_count")
    for w in (res or {}).get("results", []): oac[w["id"]] = w
    for x in oaids[i:i + 50]: oac.setdefault(x, None)
    json.dump(oac, open(CACHE_OA, "w", encoding="utf-8"))

# ---- unificação: DOI > título normalizado ----
cand = {}
def uid(doi, title): return ("doi:" + doi.lower().replace("https://doi.org/", "")) if doi else ("t:" + norm(title))
alias = {}
for x, m in s2c.items():
    if not m: continue
    u = uid((m.get("externalIds") or {}).get("DOI"), m.get("title")); alias["t:" + norm(m.get("title"))] = u
    c = cand.setdefault(u, {"title": m.get("title"), "year": m.get("year"), "cit": m.get("citationCount") or 0, "abstract": m.get("abstract") or "",
                            "venue": m.get("venue") or "", "tipos": ",".join(m.get("publicationTypes") or []), "s2": x,
                            "arxiv": (m.get("externalIds") or {}).get("ArXiv", ""), "votantes": set()})
for k, v in votantes.items():
    for x in v["s2"]:
        m = s2c.get(x)
        if m: cand[uid((m.get("externalIds") or {}).get("DOI"), m.get("title"))]["votantes"].add(k)
    for x in v["oa"]:
        w = oac.get(x)
        if not w or not w.get("title"): continue
        u = uid(w.get("doi"), w["title"])
        u = u if u in cand else alias.get("t:" + norm(w["title"]), u)
        c = cand.setdefault(u, {"title": w["title"], "year": w.get("publication_year"), "cit": w.get("cited_by_count") or 0, "abstract": "",
                                "venue": "", "tipos": "", "s2": "", "arxiv": "", "votantes": set()})
        c["votantes"].add(k)
# especificidade: votos / citações dentro da camada C (S2), como na lista de destilação
nall = Counter(x for r in rows if r.get("para_camada_C") == "sim" for x in s2refs(key(r)))
out = []
for u, c in cand.items():
    n = len(c["votantes"])
    if n < 3: continue
    out.append({"uid": u, "votos": n, "votos_gab": sum(1 for k in c["votantes"] if juri[k] == "gabarito"),
                "votos_hw": sum(1 for k in c["votantes"] if juri[k] == "reserva-hardware"),
                "cit_camadaC": nall.get(c["s2"], 0), "espec": round(n / max(nall.get(c["s2"], 0), 1), 3) if c["s2"] else "",
                "title": c["title"], "year": c["year"], "cit": c["cit"], "venue": c["venue"], "tipos": c["tipos"],
                "s2": c["s2"], "arxiv": c["arxiv"], "abstract": c["abstract"][:1500],
                "e_jurado": "sim" if c["s2"] in {byk[k]["s2"] for k in juri if k in byk} else ""})
out.sort(key=lambda d: -d["votos"])
with open(os.path.join(OUT, "candidatas.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
with open(os.path.join(OUT, "juri.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["chave", "origem", "title", "year", "cit", "refs_s2", "refs_oa"])
    for k in juri:
        r = byk.get(k, {}); w.writerow([k, juri[k], r.get("title", ""), r.get("year", ""), r.get("cit", ""), len(jr[k]["s2"]), len(jr[k]["oa"])])
print("júri:", Counter(juri.values()), "| votantes com refs:", Counter(juri[k] for k in votantes))
print("candidatas com >=3 votos:", len(out), "| >=5:", sum(d["votos"] >= 5 for d in out), "| >=10:", sum(d["votos"] >= 10 for d in out))
