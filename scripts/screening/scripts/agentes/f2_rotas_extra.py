"""Rotas extras do M6 (26/09) para as obras da amostra F2 ainda sem abstract: Crossref (DOI) e busca do S2 por
título (obra sem arXiv nem DOI). Atualiza entrada.json e refaz os lotes do agente 1."""
import json, os, re, time, urllib.parse, urllib.request
ROOT = r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial"
OUT = os.path.join(ROOT, "Screening", "fase1", "F2")
E = json.load(open(os.path.join(OUT, "entrada.json"), encoding="utf-8"))
M = json.load(open(os.path.join(OUT, "mapa.json"), encoding="utf-8"))
def get(url):
    for t in range(4):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "screening-ufg"}), timeout=40))
        except urllib.error.HTTPError as e:
            if e.code == 404: return None
            time.sleep(5 * (t + 1))
        except Exception:
            time.sleep(5 * (t + 1))
    return None
limpa = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()
for e in E:
    if e["acesso"] == "ok":
        continue
    m = M[e["id"]]; a = ""
    if m["doi"]:
        x = get("https://api.crossref.org/works/" + urllib.parse.quote(m["doi"]))
        a = limpa(((x or {}).get("message") or {}).get("abstract") or "")
        e["rotas"].append("Crossref:" + ("ok" if a else "vazio"))
    else:
        x = get("https://api.semanticscholar.org/graph/v1/paper/search/match?fields=title,abstract&query="
                + urllib.parse.quote(m["title"]))
        d = ((x or {}).get("data") or [{}])[0]
        if d.get("abstract") and re.sub(r"\W", "", d.get("title", "").lower()) == re.sub(r"\W", "", m["title"].lower()):
            a = d["abstract"]
        e["rotas"].append("S2 título:" + ("ok" if a else "vazio"))
        time.sleep(1.5)
    if a:
        e["abstract"], e["acesso"] = a, "ok"
json.dump(E, open(os.path.join(OUT, "entrada.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for j in range(0, len(E), 40):
    json.dump(E[j:j + 40], open(os.path.join(OUT, "a1", f"lote{j // 40 + 1:02d}-entrada.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
print("com abstract:", sum(e["acesso"] == "ok" for e in E), "de", len(E))
