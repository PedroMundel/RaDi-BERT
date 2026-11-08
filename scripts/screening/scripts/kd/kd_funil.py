"""Funil de destilação (24/09, pedido do Pedro): lista curta de leitura de destilação de conhecimento.
Votantes = obras da camada C com 'distill' no título, fora de escopo removidas (visão/CNN, dataset distillation,
federada). Candidatos = obras citadas por votantes. Poda de genéricos por especificidade (votos de destilação /
citações dentro da camada C inteira). Cotas por época; era LLM votada só por votantes 2024-26.
Ordena, não apaga: grava a tabela completa de candidatos, a lista curta é um recorte dela."""
import csv, json, os, re, sys, time, urllib.request
from collections import Counter

ROOT = r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial"
F1 = os.path.join(ROOT, "Screening", "fase1")
OUT = os.path.join(ROOT, "Screening", "scripts", "kd")
META = os.path.join(OUT, "kd_funil_meta.json")

rows = [r for r in csv.DictReader(open(os.path.join(F1, "2026-09-22-floresta-obras.csv"), encoding="utf-8-sig"))
        if r["para_camada_C"] == "sim"]
key = lambda x: x["s2"] if x["s2"] else f"ARXIV:{x['arxiv']}"
R = json.load(open(os.path.join(F1, "raw", "2026-09-23-camadaC-F1-referencias.json"), encoding="utf-8"))
P = json.load(open(os.path.join(F1, "raw", "2026-09-23-camadaC-F1-referencias-porobra.json"), encoding="utf-8"))

def refs(r):
    p = R.get(key(r))
    if not p:
        return set()
    out = [x.get("paperId") for x in (p.get("references") or []) if x]
    if not any(out):
        out = (P.get(p["paperId"]) or {}).get("refs") or []
    return {x for x in out if x}

# --- escopo (decisão do Pedro 24/09: visão/CNN, dataset distillation e federada ficam fora) ---
FORA = {
    "visão/CNN": re.compile(r"\b(image|visual|vision|object detect|detector|segmentation|CNN|convolutional|video|"
                            r"point cloud|pose|person re-?id|face|ImageNet|CIFAR|pixel|remote sensing)", re.I),
    "dataset distillation": re.compile(r"(dataset|data) (distillation|condensation)|condensed data", re.I),
    "federada": re.compile(r"federated|\bFedMD\b", re.I),
}
LINGUAGEM = re.compile(r"\b(language|NLP|BERT|GPT|LLM|text|translation|sentence|token|transformer|speech|"
                       r"question answering|GLUE|reasoning|rationale)", re.I)
VENUE_VISAO = re.compile(r"Computer Vision|CVPR|ICCV|ECCV|Image Processing", re.I)
def escopo(title, abstract=""):
    for nome, rx in FORA.items():
        if nome == "visão/CNN":
            # visão só exclui se não houver sinal de linguagem (título + resumo)
            if rx.search(title) or (rx.search(abstract) and not LINGUAGEM.search(title + " " + abstract)):
                return nome
        elif rx.search(title + " " + abstract):
            return nome
    return ""

kd = re.compile(r"distill", re.I)
votantes = [r for r in rows if kd.search(r["title"])]
excl_vot = Counter(escopo(r["title"]) for r in votantes)
votantes = [r for r in votantes if not escopo(r["title"])]
vot_refs = {key(r): refs(r) for r in votantes}
com_refs = [r for r in votantes if vot_refs[key(r)]]
recentes = [r for r in com_refs if r["year"] in ("2024", "2025", "2026")]

n_kd = Counter(x for r in com_refs for x in vot_refs[key(r)])
n_kd_rec = Counter(x for r in recentes for x in vot_refs[key(r)])
n_all = Counter(x for r in rows for x in refs(r))   # camada C inteira (14.901) como base de comparação
cand = sorted({x for x, n in n_kd.items() if n >= 3} | {x for x, n in n_kd_rec.items() if n >= 3})

# --- metadados dos candidatos (S2 /paper/batch serve para metadado; o problema de 23/09 era só referências) ---
meta = json.load(open(META, encoding="utf-8")) if os.path.exists(META) else {}
falta = [c for c in cand if c not in meta]
for i in range(0, len(falta), 400):
    lote = falta[i:i + 400]
    for t in range(6):
        try:
            req = urllib.request.Request(
                "https://api.semanticscholar.org/graph/v1/paper/batch?fields=title,year,citationCount,abstract,venue,externalIds",
                data=json.dumps({"ids": lote}).encode(), headers={"Content-Type": "application/json"})
            res = json.load(urllib.request.urlopen(req, timeout=120)); break
        except Exception as e:
            print("retry", e, file=sys.stderr); time.sleep(10 * (t + 1))
    else:
        sys.exit("S2 indisponível")
    meta.update({c: m for c, m in zip(lote, res) if m})
    json.dump(meta, open(META, "w", encoding="utf-8"))

def era(y):
    y = int(y or 0)
    return "história (até 2017)" if y <= 2017 else "era BERT (2018-2021)" if y <= 2021 else "era LLM (2022+)"

tab = []
for c in cand:
    m = meta.get(c) or {}
    t, a = m.get("title") or "", m.get("abstract") or ""
    tab.append({
        "s2": c, "title": t, "year": m.get("year") or "", "citacoes_s2": m.get("citationCount") or 0,
        "venue": m.get("venue") or "", "arxiv": (m.get("externalIds") or {}).get("ArXiv", ""),
        "votos": n_kd[c], "votos_2024_26": n_kd_rec[c], "citada_na_camadaC": n_all[c],
        "especificidade": round(n_kd[c] / max(n_all[c], 1), 3),
        "era": era(m.get("year")),
        "fora_escopo": escopo(t, a) or ("visão/CNN (venue)" if VENUE_VISAO.search(m.get("venue") or "")
                                        and not LINGUAGEM.search(t + " " + a) else ""),
        "linguagem": "sim" if LINGUAGEM.search(t + " " + a) else "",
    })
json.dump({"votantes": len(votantes) + sum(v for k, v in excl_vot.items() if k), "excl_votantes": excl_vot,
           "votantes_escopo": len(votantes), "com_refs": len(com_refs), "recentes": len(recentes),
           "candidatos": len(cand)}, open(os.path.join(OUT, "kd_funil_resumo.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
with open(os.path.join(OUT, "kd_funil_candidatos.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(tab[0].keys())); w.writeheader(); w.writerows(tab)
# surveys de entrada: votantes que são survey, no escopo
surv = sorted([r for r in votantes if r["tipo_no_titulo"] == "True"], key=lambda r: -int(r["cit"] or 0))
with open(os.path.join(OUT, "kd_funil_surveys.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f); w.writerow(["title", "year", "cit", "camada_C_F1", "s2", "arxiv"])
    for r in surv:
        w.writerow([r["title"], r["year"], r["cit"], r["camada_C_F1"], r["s2"], r["arxiv"]])
print(open(os.path.join(OUT, "kd_funil_resumo.json"), encoding="utf-8").read())
