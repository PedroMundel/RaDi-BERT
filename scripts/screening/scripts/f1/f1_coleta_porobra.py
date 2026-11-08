"""F1 — recoleta obra a obra das referências que o endpoint em lote do S2 devolveu vazias
(referenceCount > 0 e lista vazia). O endpoint /paper/{id}/references devolve. Retomável."""
import json, os, time, urllib.request, urllib.error

F1 = r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial\Screening\fase1"
LOTE = os.path.join(F1, "raw", "2026-09-23-camadaC-F1-referencias.json")
OUT = os.path.join(F1, "raw", "2026-09-23-camadaC-F1-referencias-porobra.json")
URL = "https://api.semanticscholar.org/graph/v1/paper/{}/references?fields=paperId&limit=1000&offset={}"

R = json.load(open(LOTE, encoding="utf-8"))
alvo = [p["paperId"] for p in R.values() if p and not p.get("references") and (p.get("referenceCount") or 0) > 0]
res = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
pend = [i for i in alvo if i not in res]
print(f"alvo {len(alvo)}, pendentes {len(pend)}", flush=True)

def get(url):
    for tent in range(10):
        try:
            return json.load(urllib.request.urlopen(url, timeout=60))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(min(3 * 2 ** tent, 120))
        except Exception:
            time.sleep(20)
    return "falhou"

t0 = time.time()
for n, pid in enumerate(pend, 1):
    refs, off, estado = [], 0, "ok"
    while True:
        d = get(URL.format(pid, off))
        if d is None or d == "falhou":
            estado = "404" if d is None else "falhou"
            break
        if d.get("data") is None:
            estado = "oculto"
            break
        refs += [x["citedPaper"]["paperId"] for x in d["data"] if (x.get("citedPaper") or {}).get("paperId")]
        if d.get("next") is None:
            break
        off = d["next"]
    res[pid] = {"estado": estado, "refs": refs}
    if n % 100 == 0 or n == len(pend):
        json.dump(res, open(OUT, "w", encoding="utf-8"))
        print(f"{len(res)}/{len(alvo)}  ({(time.time() - t0) / 60:.0f} min)", flush=True)
    time.sleep(1)
print("FIM", len(res), "estados:", {e: sum(1 for v in res.values() if v["estado"] == e) for e in ("ok", "oculto", "404", "falhou")}, flush=True)
