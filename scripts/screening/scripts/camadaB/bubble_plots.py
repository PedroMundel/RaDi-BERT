"""Bubble plots (estilo Petersen 2008: eixo Y compartilhado, dois painéis) sobre as obras que seguem para a
camada C. Facetas escolhidas para ajudar a desenhar a leitura por agentes. Nível 3: casamento de palavras em
título + abstract, sem leitura."""
import csv, glob, json, os, re
from collections import Counter
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial"
F1 = os.path.join(ROOT, "Screening", "fase1")
FIG = os.path.join(F1, "figs"); os.makedirs(FIG, exist_ok=True)
POOL = open(os.path.join(ROOT, "docs/screening/pool-termos-etapa1.md"), encoding="utf-8").read()
INK, INK2, SURF, BLUE, GRID = "#0b0b0b", "#52514e", "#fcfcfb", "#2a78d6", "#e6e5e0"
ACRONYM_CASE = {"LoRA", "MoE", "PEFT", "SLMs", "SLM", "PTQ", "QAT", "KV cache", "CoT distillation"}

def heads(group):
    sec = POOL.split(f"### Grupo `{group}`", 1)[1].split("\n### ", 1)[0].split("\n## ", 1)[0]
    out = {}
    for line in sec.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(c) < 4 or c[0] in ("termo (en)", "") or set(c[0]) <= set("-") or "aposentado" in c[3]:
            continue
        v = re.findall(r'"([^"]+)"', c[1]) + [x.strip() for x in re.sub(r'"[^"]+"', "", c[1]).split(",") if x.strip()]
        out[c[0]] = [h.strip() for h in c[0].split("/")] + v
    return out

def term_re(t):
    flags = 0 if (t.isupper() or t in ACRONYM_CASE) else re.I
    return re.compile(r"(?<![A-Za-z0-9])" + re.escape(t) + r"(?![A-Za-z0-9])", flags)

GROUPS = ["compressão", "inferência/serving", "adaptação", "edge", "dado/confiança", "ferramentas"]
TECH = {f"{h}  [{g}]": [term_re(t) for t in terms] for g in GROUPS for h, terms in heads(g).items()}

ARCH = [("encoder-only", r"(?i:encoder-only|masked language model)|\bBERT\b|RoBERTa|DeBERTa|DistilBERT|ALBERT|ELECTRA"),
        ("encoder-decoder", r"(?i:encoder-decoder|sequence-to-sequence|seq2seq)|\bT5\b|\bBART\b|Flan-T5|\bmT5\b"),
        ("decoder-only", r"(?i:decoder-only|autoregressive|causal language model)|\bGPT|LLaMA|Llama|\bMistral\b|\bQwen"),
        ("LLM (família n/d)", r"(?i:large language model)|\bLLMs?\b"),
        ("vision transformer", r"(?i:vision transformer)|\bViTs?\b"),
        ("transformer (família n/d)", r"(?i:transformer)"),
        ("CNN / RNN", r"(?i:convolutional|recurrent)|\bCNNs?\b|ResNet|MobileNet|\bLSTM|\bRNNs?\b")]
ARCH = [(n, re.compile(p)) for n, p in ARCH]
FAMILIAS = ("encoder-only", "encoder-decoder", "decoder-only", "vision transformer")

rows = [r for r in csv.DictReader(open(os.path.join(F1, "2026-09-22-floresta-obras.csv"), encoding="utf-8-sig"))
        if r["para_camada_C"] == "sim"]
abs_by = {}
for path in glob.glob(os.path.join(F1, "raw", "2026-09-22-exec3-*-*.json")):
    if "passo0" in path:
        continue
    for p in json.load(open(path, encoding="utf-8"))["papers"]:
        a = p.get("abstract") or p.get("summary") or ""
        k = p.get("paperId") or ("ARXIV:" + re.sub(r"v\d+$", "", p.get("id") or ""))
        if a and len(a) > len(abs_by.get(k, "")):
            abs_by[k] = a
key = lambda x: x["s2"] if x["s2"] else f"ARXIV:{x['arxiv']}"

recs = []
for r in rows:
    text = r["title"] + " " + abs_by.get(key(r), "")
    arch = [n for n, rx in ARCH if rx.search(text)]
    if any(a in arch for a in FAMILIAS):          # família declarada: tira os rótulos genéricos
        arch = [a for a in arch if a not in ("transformer (família n/d)", "LLM (família n/d)") or
                (a == "LLM (família n/d)" and "decoder-only" not in arch and "encoder-only" not in arch and "encoder-decoder" not in arch)]
    cit = int(r["cit"] or 0)
    recs.append(dict(techs=[t for t, rs in TECH.items() if any(x.search(text) for x in rs)],
                     arch=arch or ["indeterminado"], camadaB=r["camada_B"],
                     tipo=("ferramenta (trilha)" if r["trilha"] == "ferramentas"
                           else "survey (tipo no título)" if r["tipo_no_titulo"] == "True" else "primário / sem tipo"),
                     cit=("60+" if cit >= 60 else "10–59" if cit >= 10 else "0–9")))

tcount = Counter(t for x in recs for t in x["techs"])
Y = [t for t, _ in sorted(tcount.items(), key=lambda kv: kv[1])]      # maior no topo
sem_tecnica = sum(1 for x in recs if not x["techs"])
N = len(recs)

def panel(ax, cats, attr, title):
    cnt = Counter()
    for x in recs:
        vals = x[attr] if isinstance(x[attr], list) else [x[attr]]
        for t in x["techs"]:
            for v in vals:
                cnt[(t, v)] += 1
    mx = max(cnt.values())
    for i, t in enumerate(Y):
        for j, c in enumerate(cats):
            n = cnt.get((t, c), 0)
            if n:
                ax.scatter(j, i, s=1500 * (n / mx) ** 0.5 + 10, color=BLUE, alpha=0.55,
                           edgecolors=SURF, linewidths=2, zorder=3)
                ax.text(j, i, str(n), ha="center", va="center", fontsize=7, color=INK, zorder=4)
    ax.set_xticks(range(len(cats))); ax.set_xticklabels(cats, rotation=30, ha="right", fontsize=8, color=INK2)
    ax.set_xlim(-0.6, len(cats) - 0.4); ax.set_title(title, fontsize=10, color=INK, loc="left")
    ax.grid(color=GRID, lw=0.6, zorder=0); ax.set_axisbelow(True)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(length=0)

def figure(left, right, fname, suptitle, note):
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(16, 0.34 * len(Y) + 3.2), sharey=True, facecolor=SURF,
                                 gridspec_kw={"width_ratios": [len(left[0]) + 1, len(right[0]) + 1]})
    for a in (a1, a2):
        a.set_facecolor(SURF)
    panel(a1, *left); panel(a2, *right)
    a1.set_yticks(range(len(Y))); a1.set_yticklabels([f"{t}  ({tcount[t]})" for t in Y], fontsize=8, color=INK)
    fig.suptitle(suptitle, x=0.01, ha="left", fontsize=12, color=INK, fontweight="bold")
    fig.text(0.01, 0.005, note, fontsize=7.5, color=INK2, ha="left", va="bottom", wrap=True)
    fig.tight_layout(rect=(0, 0.045, 1, 0.97))
    fig.savefig(os.path.join(FIG, fname), dpi=130, facecolor=SURF); plt.close(fig)

NOTE = (f"Nível 3: casamento de palavras em título + abstract, nada lido. Eixo Y = termo do pool (cabeça + variantes) "
        f"e seu grupo; o número entre parênteses é o total de obras que casam. Uma obra conta em cada termo que casa. "
        f"{sem_tecnica} das {N} obras não casam termo nenhum e não aparecem.")
figure((["survey (tipo no título)", "primário / sem tipo", "ferramenta (trilha)"], "tipo", "Tipo de obra"),
       (["0–9", "10–59", "60+"], "cit", "Citações no Semantic Scholar (piso de registro = 60)"),
       "bubble_A_tipo_citacao.png",
       f"A — onde estão os surveys e quão citados são, por técnica  ·  {N} obras da camada C", NOTE)
cats_B = ["núcleo", "misto", "arquiteturas (§1.1)", "dentro (§1.2.1 d)", "a testar (uso?)", "salvaguarda (título)"]
figure((cats_B, "camadaB", "Categoria da camada B"),
       ([n for n, _ in ARCH] + ["indeterminado"], "arch", "Arquitetura declarada no título/abstract"),
       "bubble_B_camadaB_arquitetura.png",
       f"B — em que grupos cada técnica está, e sobre que arquitetura  ·  {N} obras da camada C",
       NOTE + " Arquitetura: só o que o texto declara; 'LLM (família n/d)' = diz LLM sem dizer decoder/encoder.")
json.dump({"N": N, "sem_tecnica": sem_tecnica, "tcount": tcount,
           "arch": Counter(a for x in recs for a in x["arch"]), "tipo": Counter(x["tipo"] for x in recs),
           "cit": Counter(x["cit"] for x in recs)},
          open(os.path.join(FIG, "bubble_dados.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", N, sem_tecnica)
