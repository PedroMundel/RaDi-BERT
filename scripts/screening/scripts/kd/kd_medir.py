import csv, json, re, glob
from collections import Counter
F1="."
rows=[r for r in csv.DictReader(open("2026-09-22-floresta-obras.csv",encoding="utf-8-sig"))]
print("floresta", len(rows))
abs_by={}
for path in glob.glob("raw/2026-09-22-exec3-*-*.json"):
    if "passo0" in path: continue
    for p in json.load(open(path,encoding="utf-8"))["papers"]:
        a=p.get("abstract") or p.get("summary") or ""
        k=p.get("paperId") or ("ARXIV:"+re.sub(r"v\d+$","",p.get("id") or ""))
        if a and len(a)>len(abs_by.get(k,"")): abs_by[k]=a
key=lambda x: x["s2"] if x["s2"] else f"ARXIV:{x['arxiv']}"
kd=re.compile(r"distill", re.I)
t_all=[r for r in rows if kd.search(r["title"])]
ta_all=[r for r in rows if kd.search(r["title"]) or kd.search(abs_by.get(key(r),""))]
print("KD no titulo (floresta toda):", len(t_all), " titulo+abstract:", len(ta_all))
C=[r for r in rows if r["para_camada_C"]=="sim"]
t=[r for r in C if kd.search(r["title"])]
print("KD titulo na camada C:", len(t), Counter(r["camada_C_F1"] for r in t))
print("  com palavra de tipo:", sum(1 for r in t if r["tipo_no_titulo"] not in ("","0","nao","não","False")), Counter(r["tipo_no_titulo"] for r in t).most_common(4))
print("  fora da camada C (por que):", Counter((r["camada_A"],r["camada_B"]) for r in t_all if r["para_camada_C"]!="sim").most_common(8))
# referencias externas
R=json.load(open("raw/2026-09-23-camadaC-F1-referencias.json",encoding="utf-8"))
P=json.load(open("raw/2026-09-23-camadaC-F1-referencias-porobra.json",encoding="utf-8"))
cnt=Counter(); comref=0
for r in t:
    p=R.get(key(r))
    if not p: continue
    refs=[x.get("paperId") for x in (p.get("references") or []) if x and x.get("paperId")]
    if not refs:
        q=P.get(p["paperId"]); refs=(q or {}).get("refs") or []
    refs=[x for x in refs if x]
    if refs: comref+=1
    cnt.update(set(refs))
print("KD com lista de referencias S2:", comref, "de", len(t), "| refs unicas:", len(cnt))
print("citadas por >=5 KD:", sum(1 for v in cnt.values() if v>=5), ">=10:", sum(1 for v in cnt.values() if v>=10))
json.dump(cnt.most_common(60), open("C:/Users/Pedro/AppData/Local/Temp/claude/C--Users-Pedro-Documents-Projects-UFG-2026-2-Residencia-Bacharelado-em-Inteligencia-Artificial/87770566-18a0-4fdc-b87c-d2659c37b08e/scratchpad/kd_top.json","w"))
yrs=Counter(r["year"] for r in t); print("anos:", sorted(yrs.items()))
