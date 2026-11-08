"""F1 — segunda fonte de referências: OpenAlex (referenced_works), por DOI, para todas as obras da camada C
que têm DOI. Guarda o id OpenAlex de cada obra (para casar as referências dentro do conjunto). Retomável."""
import csv, json, os, time, urllib.request, urllib.parse

F1 = r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial\Screening\fase1"
OUT = os.path.join(F1, "raw", "2026-09-23-camadaC-F1-openalex.json")
BASE = "https://api.openalex.org/works?per-page=50&select=id,doi,referenced_works_count,referenced_works&filter=doi:"

rows = [r for r in csv.DictReader(open(os.path.join(F1, "2026-09-22-floresta-obras.csv"), encoding="utf-8-sig"))
        if r["para_camada_C"] == "sim"]
dois = sorted({r["doi"].lower() for r in rows if r["doi"]})
res = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
pend = [d for d in dois if d not in res]
print(f"{len(dois)} DOIs, {len(pend)} pendentes", flush=True)

def get(url):
    for tent in range(8):
        try:
            return json.load(urllib.request.urlopen(url, timeout=90))
        except Exception as e:
            print(f"erro {e!r}; espera", flush=True)
            time.sleep(min(3 * 2 ** tent, 120))
    return None

for k in range(0, len(pend), 50):
    lote = pend[k:k + 50]
    d = get(BASE + "|".join(urllib.parse.quote(x, safe="/") for x in lote))
    if d is None:
        print(f"lote {k // 50} falhou, segue", flush=True)
        continue
    achou = {}
    for w in d["results"]:
        doi = (w.get("doi") or "").lower().replace("https://doi.org/", "")
        achou[doi] = {"id": w["id"], "n": w["referenced_works_count"], "refs": w["referenced_works"]}
    for x in lote:
        res[x] = achou.get(x)  # None = OpenAlex não achou o DOI
    if (k // 50) % 20 == 0:
        json.dump(res, open(OUT, "w", encoding="utf-8"))
        print(f"{len(res)}/{len(dois)}", flush=True)
    time.sleep(0.15)
json.dump(res, open(OUT, "w", encoding="utf-8"))
print("FIM", len(res), "não achados:", sum(1 for v in res.values() if v is None),
      "com refs:", sum(1 for v in res.values() if v and v["n"] > 0), flush=True)
