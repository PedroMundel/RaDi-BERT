"""Lista rápida, etapa 2 (27/09): marca subárea (grupos do pool + hardware), época e tipo provável de cada candidata,
e imprime as mais votadas pelo júri validado (sem a reserva). Serve para fixar as regras da etapa 3 olhando os dados.
Grava candidatas-marcadas.csv."""
import csv, os, re, sys
ROOT = r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial"
OUT = os.path.join(ROOT, "Screening", "fase1", "lista-rapida")
POOL = open(os.path.join(ROOT, "docs/screening/pool-termos-etapa1.md"), encoding="utf-8").read()
ACR = {"LoRA", "MoE", "PEFT", "SLMs", "SLM", "PTQ", "QAT", "KV cache", "CoT distillation"}
def termos(g):
    sec = POOL.split(f"### Grupo `{g}`", 1)[1].split("\n### ", 1)[0].split("\n## ", 1)[0]; out = []
    for line in sec.splitlines():
        if not line.lstrip().startswith("|"): continue
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) < 4 or c[0] in ("termo (en)", "") or set(c[0]) <= set("-") or "aposentado" in c[3]: continue
        out += [h.strip() for h in c[0].split("/")] + re.findall(r'"([^"]+)"', c[1]) + \
               [x.strip() for x in re.sub(r'"[^"]+"', "", c[1]).split(",") if x.strip()]
    return [re.compile(r"(?<![A-Za-z0-9])" + re.escape(t) + r"(?![A-Za-z0-9])", 0 if (t.isupper() or t in ACR) else re.I) for t in out if t]
SUB = {g: termos(g) for g in ["compressão", "inferência/serving", "adaptação", "edge", "dado/confiança", "ferramentas"]}
SUB["hardware"] = [re.compile(r"accelerat|FPGA|ASIC|hardware|\bNPU|in-memory|systolic|\bchip|dataflow|TPU", re.I)]
SURVEY = re.compile(r"\b(survey|review|overview|taxonomy|tutorial|primer)\b", re.I)
SISTEMA = re.compile(r"\b(system|engine|framework|library|compiler|runtime|toolkit|open[- ]source)\b", re.I)
CONCEITO = re.compile(r"attention|transformer|language model|pre-?train|\bBERT\b|\bGPT|scaling law|\bT5\b|LLaMA|foundation model", re.I)
DATASET = re.compile(r"dataset|benchmark|ImageNet|COCO|CIFAR|GLUE|SQuAD|Adam:|optimi[sz]ation method|Dropout|Batch Normalization", re.I)
C = list(csv.DictReader(open(os.path.join(OUT, "candidatas.csv"), encoding="utf-8-sig")))
for c in C:
    txt = (c["title"] or "") + " " + (c["abstract"] or "")
    c["votos_val"] = int(c["votos"]) - int(c["votos_hw"])
    c["subareas"] = "|".join(g for g, rs in SUB.items() if any(r.search(txt) for r in rs))
    y = int(c["year"] or 0); c["epoca"] = "até 2017" if y <= 2017 else "2018-21" if y <= 2021 else "2022+"
    c["tipo"] = "survey" if SURVEY.search(c["title"] or "") else "sistema?" if SISTEMA.search(c["title"] or "") else \
        "dataset/técnica geral?" if DATASET.search(c["title"] or "") else "conceito?" if (not c["subareas"] and CONCEITO.search(txt)) else ""
with open(os.path.join(OUT, "candidatas-marcadas.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(C[0].keys())); w.writeheader(); w.writerows(C)
n = int(sys.argv[1]) if len(sys.argv) > 1 else 120
for c in sorted(C, key=lambda c: -c["votos_val"])[:n]:
    print(f"{c['votos_val']:>3} hw{c['votos_hw']:>3} {c['espec']:>6} {c['year']} {c['epoca']:8} {c['tipo'][:10]:10} {c['subareas'][:34]:34} {c['title'][:80]}")
