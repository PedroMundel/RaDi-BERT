"""F1 (árvore de citação) — coleta: referências das obras da camada C no Semantic Scholar.
Só coleta; grava bruto em raw/. Retoma de onde parou (cache por lote)."""
import csv, json, os, sys, time, urllib.request, urllib.error

ROOT = r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial"
F1 = os.path.join(ROOT, "Screening", "fase1")
OUT = os.path.join(F1, "raw", "2026-09-23-camadaC-F1-referencias.json")
URL = "https://api.semanticscholar.org/graph/v1/paper/batch?fields=paperId,externalIds,referenceCount,references.paperId"
LOTE = 500

rows = [r for r in csv.DictReader(open(os.path.join(F1, "2026-09-22-floresta-obras.csv"), encoding="utf-8-sig"))
        if r["para_camada_C"] == "sim"]
ids = [r["s2"] if r["s2"] else f"ARXIV:{r['arxiv']}" for r in rows]
res = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}

def post(batch):
    body = json.dumps({"ids": batch}).encode()
    for tent in range(12):
        try:
            req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
            return json.load(urllib.request.urlopen(req, timeout=120))
        except urllib.error.HTTPError as e:
            wait = min(5 * 2 ** tent, 120)
            print(f"HTTP {e.code}, espera {wait}s", flush=True)
            time.sleep(wait)
        except Exception as e:
            print(f"erro {e!r}, espera 30s", flush=True); time.sleep(30)
    sys.exit("desisti do lote")

pend = [i for i in ids if i not in res]
print(f"{len(ids)} ids, {len(pend)} pendentes", flush=True)
for k in range(0, len(pend), LOTE):
    batch = pend[k:k + LOTE]
    out = post(batch)
    for q, p in zip(batch, out):
        res[q] = p  # None = S2 não achou
    json.dump(res, open(OUT, "w", encoding="utf-8"))
    print(f"lote {k // LOTE + 1}: {len(res)}/{len(ids)}", flush=True)
    time.sleep(3)
print("FIM", len(res), "sem registro:", sum(1 for v in res.values() if v is None), flush=True)
