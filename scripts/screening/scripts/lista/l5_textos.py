"""Leitura por agentes, passo 1 (27/09): resolve acesso e baixa o texto completo das obras da lista v2.
Rotas, na ordem (M6): arXiv (id da lista ou do S2) -> PDF aberto do S2 -> PDF aberto do OpenAlex.
Grava leitura/textos/NN.txt + leitura/manifesto.json. Idempotente: pula quem já tem texto."""
import csv, json, os, re, time, urllib.parse, urllib.request
import fitz

ROOT = r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial"
LR = os.path.join(ROOT, "Screening", "fase1", "lista-rapida")
LE = os.path.join(LR, "leitura"); TX = os.path.join(LE, "textos"); os.makedirs(TX, exist_ok=True)
MAN = os.path.join(LE, "manifesto.json")
man = json.load(open(MAN, encoding="utf-8")) if os.path.exists(MAN) else {}
L = list(csv.DictReader(open(os.path.join(LR, "lista-v2.csv"), encoding="utf-8-sig")))
UA = {"User-Agent": "Mozilla/5.0 (academic screening; UFG)"}

def get(url, raw=False, tries=4):
    for t in range(tries):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read()
            return r if raw else json.loads(r)
        except urllib.error.HTTPError as e:
            if e.code in (403, 404): return None
            time.sleep(6 * (t + 1))
        except Exception:
            time.sleep(6 * (t + 1))
    return None

def pdf_texto(url):
    b = get(url, raw=True)
    if not b or not b[:5].startswith(b"%PDF"): return None, 0
    d = fitz.open(stream=b, filetype="pdf")
    return "\n".join(f"\n=== [página {i + 1}] ===\n" + p.get_text() for i, p in enumerate(d)), len(d)

# metadado do S2 em UM pedido em lote (a versão obra-a-obra levava ~1 min por obra por causa das pausas)
pend = [it["s2"] for n, it in enumerate(L, 1) if it["s2"] and not it["s2"].startswith("ARXIV:")
        and man.get(f"{n:02d}", {}).get("acesso") != "texto completo"]
lote = {}
if pend:
    req = urllib.request.Request("https://api.semanticscholar.org/graph/v1/paper/batch?fields=externalIds,openAccessPdf,title",
                                 data=json.dumps({"ids": pend}).encode(), headers={**UA, "Content-Type": "application/json"})
    for t in range(5):
        try:
            lote = dict(zip(pend, json.load(urllib.request.urlopen(req, timeout=120)))); break
        except Exception:
            time.sleep(8 * (t + 1))
for n, it in enumerate(L, 1):
    nid = f"{n:02d}"
    if man.get(nid, {}).get("acesso") == "texto completo" and os.path.exists(os.path.join(TX, nid + ".txt")):
        continue
    rotas = []; txt = None; pags = 0
    s2 = it["s2"] if it["s2"] and not it["s2"].startswith("ARXIV:") else ""
    meta = lote.get(s2) if s2 else None
    if not meta:
        q = get("https://api.semanticscholar.org/graph/v1/paper/search/match?fields=externalIds,openAccessPdf,title&query=" + urllib.parse.quote(it["titulo"]))
        meta = ((q or {}).get("data") or [None])[0]
    ext = (meta or {}).get("externalIds") or {}
    arx = it["arxiv"] or ext.get("ArXiv") or (it["s2"][6:] if it["s2"].startswith("ARXIV:") else "")
    if arx:
        txt, pags = pdf_texto(f"https://arxiv.org/pdf/{arx}"); rotas.append(f"arXiv {arx}: " + ("ok" if txt else "falhou")); time.sleep(3)
    if not txt and (meta or {}).get("openAccessPdf", {}) and meta["openAccessPdf"].get("url"):
        u = meta["openAccessPdf"]["url"]; txt, pags = pdf_texto(u); rotas.append(f"S2 PDF aberto {u[:60]}: " + ("ok" if txt else "falhou"))
    doi = ext.get("DOI")
    if not txt and doi:
        w = get(f"https://api.openalex.org/works/doi:{doi}")
        for loc in ((w or {}).get("locations") or []):
            if loc.get("pdf_url"):
                txt, pags = pdf_texto(loc["pdf_url"]); rotas.append(f"OpenAlex {loc['pdf_url'][:60]}: " + ("ok" if txt else "falhou"))
                if txt: break
        if not any(r.startswith("OpenAlex") for r in rotas): rotas.append("OpenAlex: sem PDF aberto")
    if txt:
        open(os.path.join(TX, nid + ".txt"), "w", encoding="utf-8").write(txt)
    man[nid] = {"titulo": it["titulo"], "bloco": it["bloco"], "divisao": it["divisao"], "ano": it["ano"], "arxiv": arx, "doi": doi or "",
                "acesso": "texto completo" if txt else "sem texto completo", "paginas": pags, "caracteres": len(txt or ""), "rotas": rotas}
    json.dump(man, open(MAN, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(nid, man[nid]["acesso"], pags, "|", it["titulo"][:60], "|", "; ".join(rotas)[:90], flush=True)
print("com texto:", sum(v["acesso"] == "texto completo" for v in man.values()), "de", len(L))
