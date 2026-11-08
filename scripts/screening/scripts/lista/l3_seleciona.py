"""Lista rápida, etapa 3 (27/09): seleção por regras declaradas sobre candidatas-marcadas.csv.
Divisão pelo TÍTULO (o abstract deu ruído na etapa 2), com prioridade de técnica sobre "hardware-aware".
Blocos: A mapas (surveys co-citados), B fundadores (cota por divisão, espalhada por época), C conceitos (família
transformer + base), D sistemas. Hardware usa votos do júri + reserva e tem cota maior (Pedro, 27/09).
Grava lista-v1.csv; não apaga nada."""
import csv, os, re
OUT = os.path.join(r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial", "Screening", "fase1", "lista-rapida")
C = list(csv.DictReader(open(os.path.join(OUT, "candidatas-marcadas.csv"), encoding="utf-8-sig")))
seen = set(); U = []
for c in C:   # duplicatas de título (ex.: ProxylessNAS com quebra de linha)
    k = re.sub(r"[^a-z0-9]", "", c["title"].lower())
    if k in seen: continue
    seen.add(k); U.append(c)
for c in U:
    c["vv"], c["vh"] = int(c["votos_val"]), int(c["votos_hw"]); c["y"] = int(c["year"] or 0)

DIV = [  # ordem = prioridade na atribuição
    ("destilação", r"distill|teacher|student|mutual learning|FitNets|born again|MiniLM|TinyBERT|LaMini|\bModel compression$"),
    ("quantização", r"quantiz|binar|ternary|XNOR|low.?bit|int8|\bbit\b|bitwidth|precision|GPTQ|AWQ|SmoothQuant|DoReFa|PACT|HAWQ|\bHAQ\b|ZeroQuant|Q-BERT"),
    ("poda e esparsidade", r"prun|sparse|sparsity|lottery|brain damage|brain surgeon|slimming|SparseGPT|heads really|weights and connections"),
    ("fatoração de baixo posto", r"low.?rank|factori[sz]|linear structure|low rank expansion|predicting parameters|tensor decomposition"),
    ("ajuste eficiente (PEFT)", r"LoRA|QLoRA|adapter|prefix-tuning|prompt tuning|parameter-efficient"),
    ("computação condicional", r"mixture.?of.?experts|\bMoE\b|Switch Transformer|GShard|GLaM|early exit|DeeBERT|FastBERT|conditional computation|adaptive inference|runtime neural"),
    ("atenção e sequência eficientes", r"Reformer|Linformer|Longformer|efficient transformer|linear.?time|state space|Mamba|sparse attention|Performer|BigBird|linear complexity"),
    ("inferência e serving", r"serving|PagedAttention|speculative|FlashAttention|KV cache|Orca|batching|prefill|decoding"),
    ("arquitetura eficiente e NAS", r"architecture search|\bNAS\b|MobileNet|ShuffleNet|SqueezeNet|EfficientNet|FBNet|MnasNet|Once for All|NetAdapt|MobileBERT|ProxylessNAS|DARTS|AutoML"),
    ("hardware", r"(?<!-)accelerat|FPGA|ASIC|(?<!Hardware-)(?<!hardware-)hardware(?!-aware)|\bchip|supercomputer|DianNao|\bEIE\b|\bTPU|Eyeriss|systolic|in-memory|dataflow|processor|Cambricon|Bit Fusion|SCNN|\bESE\b"),
    ("edge e on-device", r"mobile|on-device|edge|embedded|microcontroller|TinyML|IoT"),
]
def divisao(t):
    for d, rx in DIV:
        if re.search(rx, t, re.I): return d
    return ""
SURVEY = re.compile(r"\b(survey|review|overview|tutorial)\b", re.I)
CONCEITOS = [r"^Attention is All you Need", r"^BERT: Pre-training", r"^Exploring the Limits of Transfer Learning", r"^Language Models are Few-Shot",
             r"^LLaMA: Open and Efficient", r"^Long Short-Term Memory", r"^A Survey of Large Language Models"]
SISTEMAS = [r"^PyTorch: An Imperative", r"^TVM: An Automated", r"^Efficient Memory Management for Large Language Model Serving",
            r"^DeepSpeed- ?Inference", r"^TensorFlow Lite Micro", r"^FINN: A Framework"]
GENERICO = re.compile(r"Residual Learning|Very Deep Convolutional|Going deeper|ImageNet|Densely Connected|Gradient-based learning|Batch Normalization|"
                      r"Tiny Images|Xception|Few-Shot|Unsupervised Multitask|RoBERTa|Llama 2|OPT:|PaLM|BLOOM|GPT-4|instructions with human|"
                      r"Image is Worth|Improving Language Understanding|Transfer Learning|Adam|Dropout|Generative AI|Health Supplement", re.I)
def votos(c): return c["vv"] + (c["vh"] if c["div"] == "hardware" else 0)
for c in U: c["div"] = divisao(c["title"])

sel = []
def pega(c, bloco, motivo):
    if any(s["title"] == c["title"] for s in sel): return
    sel.append({**c, "bloco": bloco, "motivo": motivo})
# C e D primeiro (listas nomeadas, escolhidas pelos votos na etapa 2; ver relatório)
for rx in CONCEITOS:
    c = next((c for c in U if re.search(rx, c["title"])), None)
    if c: pega(c, "C conceitos", f"{c['vv']} votos; conceito que os surveys assumem")
for rx in SISTEMAS:
    c = next((c for c in U if re.search(rx, c["title"])), None)
    if c: pega(c, "D sistemas", f"{votos(c)} votos; ferramenta/sistema citado pelo júri")
# A: o survey mais co-citado de cada divisão + mapas de LLM (2023+)
surv = [c for c in U if SURVEY.search(c["title"]) and not any(re.search(r, c["title"]) for r in CONCEITOS)]
for d, _ in DIV:
    cs = sorted([c for c in surv if divisao(c["title"]) == d or (d == "destilação" and "Distillation" in c["title"])], key=lambda c: -votos({**c, "div": d}))
    if cs: pega(cs[0], "A mapas", f"survey mais co-citado da divisão {d} ({cs[0]['vv']} votos{', +' + str(cs[0]['vh']) + ' da reserva' if d == 'hardware' else ''})")
for c in sorted([c for c in surv if c["y"] >= 2023], key=lambda c: -c["vv"])[:3]:
    pega(c, "A mapas", f"mapa da era LLM ({c['vv']} votos)")
for c in sorted([c for c in surv if c["y"] <= 2021 and re.search(r"compression and (hardware )?acceleration", c["title"], re.I)], key=lambda c: -votos(c))[:2]:
    pega(c, "A mapas", f"mapa geral de compressão ({c['vv']} votos)")
# B: fundadores por divisão, espalhados por época
COTA = {"destilação": 2, "quantização": 3, "poda e esparsidade": 3, "fatoração de baixo posto": 2, "ajuste eficiente (PEFT)": 2,
        "computação condicional": 2, "atenção e sequência eficientes": 2, "inferência e serving": 3, "arquitetura eficiente e NAS": 2,
        "hardware": 4, "edge e on-device": 1}
ep = lambda y: "até 2017" if y <= 2017 else "2018-21" if y <= 2021 else "2022+"
for d, n in COTA.items():
    cs = sorted([c for c in U if c["div"] == d and not SURVEY.search(c["title"]) and not GENERICO.search(c["title"])
                 and not any(s["title"] == c["title"] for s in sel)], key=lambda c: -votos(c))
    escolhidos = []
    for e in ("até 2017", "2018-21", "2022+"):          # um por época primeiro
        c = next((c for c in cs if ep(c["y"]) == e and c not in escolhidos), None)
        if c and len(escolhidos) < n: escolhidos.append(c)
    for c in cs:                                          # completa pela ordem de votos
        if len(escolhidos) >= n: break
        if c not in escolhidos: escolhidos.append(c)
    for c in sorted(escolhidos, key=lambda c: c["y"]):
        pega(c, "B fundadores", f"{votos(c)} votos{' (júri + reserva)' if d == 'hardware' else ''}; {d}, {ep(c['y'])}")
cols = ["bloco", "div", "year", "title", "vv", "vh", "motivo", "s2", "arxiv", "cit", "venue"]
with open(os.path.join(OUT, "lista-v1.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader(); w.writerows(sel)
from collections import Counter
print(len(sel), Counter(s["bloco"] for s in sel))
for s in sel: print(f"{s['bloco'][:12]:12} {s['div'][:24]:24} {s['year']} v{s['vv']:>2} h{s['vh']:>2} {s['title'][:78]}")
