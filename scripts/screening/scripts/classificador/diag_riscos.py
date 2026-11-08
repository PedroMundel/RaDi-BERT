"""Diagnóstico de riscos do classificador de relevância (27/09). Mede, com os rótulos da F2, os problemas que o
método pode causar, ANTES de usá-lo para ordenar a leitura. Zero token de agente; não grava na tabela-mestra;
não usa a metade de teste do gabarito (só metadado de grupo/termo dela, E12).
Avaliação sempre ponderada pelo inverso da probabilidade de inclusão na amostra da F2 (tam/amostra por grupo),
para que os números valham para a população e não para a amostra."""
import csv, glob, json, os, random, re, sys
from collections import Counter, defaultdict
import numpy as np
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.metrics import average_precision_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial"
F1 = os.path.join(ROOT, "Screening", "fase1")
F2 = os.path.join(F1, "F2")
OUT = os.path.join(F1, "C1-diagnostico")
os.makedirs(OUT, exist_ok=True)
SEEDS = [1, 2, 3, 4, 5]
R = {}   # resultados

# ---------- dados ----------
rows = list(csv.DictReader(open(os.path.join(F1, "2026-09-22-floresta-obras.csv"), encoding="utf-8-sig")))
keep = [r for r in rows if r["camada_A"].startswith("mantida")]
assert len(keep) == 74791, len(keep)
key = lambda x: x["s2"] if x["s2"] else f"ARXIV:{x['arxiv']}"
idx = {key(r): i for i, r in enumerate(keep)}
byk = {key(r): r for r in keep}
X = np.load(os.path.join(F1, "emb", "camadaB_emb_specter2.npy")).astype(np.float32)
Xn = X / np.linalg.norm(X, axis=1, keepdims=True)

M = json.load(open(os.path.join(F2, "mapa.json"), encoding="utf-8"))
E = {e["id"]: e for e in json.load(open(os.path.join(F2, "entrada.json"), encoding="utf-8"))}
V = json.load(open(os.path.join(F2, "consolidado.json"), encoding="utf-8"))["V"]
A3 = {}
for q in glob.glob(os.path.join(F2, "a3", "lote??-saida.json")):
    t = open(q, encoding="utf-8-sig").read()
    try: L = json.loads(t)
    except json.JSONDecodeError: L = json.loads(re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', t))
    for x in L: A3[x["id"]] = x
discord = {d[0] for d in json.load(open(os.path.join(F2, "consolidado.json"), encoding="utf-8"))["discord"]}

# gabarito: ajuste (pode treinar) e teste (nunca treina), mesma divisão da camada B/F1/calibração
v1 = list(csv.DictReader(open(os.path.join(F1, "2026-09-22-volta-1-obras.csv"), encoding="utf-8-sig")))
gi = {}
for x in v1:
    for kk in (x["arxiv"], x["doi"]):
        if kk: gi[kk.lower()] = x
refids = [[c.strip() for c in l.strip().strip("|").split("|")][9].lower()
          for l in open(os.path.join(F1, "2026-09-21-candidatos-string-mae-exec2.md"), encoding="utf-8")
          if re.match(r"\| \d+ \| entra \|", l)]
ref = [gi[i] for i in refids if i in gi]; random.Random(42).shuffle(ref)
aj_k = [key(r) for r in ref[:len(ref) // 2]]; te_k = [key(r) for r in ref[len(ref) // 2:]]

# rótulos da F2 (só com acesso e com vetor)
lab = [i for i in V if V[i] in ("relevante", "dúvida", "fora", "claramente fora (a1)") and M[i]["chave"] in idx]
vaz = [i for i in lab if M[i]["chave"] in set(te_k)]
R["E0_vazamento_teste_gabarito_na_F2"] = len(vaz)
lab = [i for i in lab if i not in set(vaz)]                       # teste do gabarito nunca entra
Xl = X[[idx[M[i]["chave"]] for i in lab]]
yP1 = np.array([V[i] == "relevante" for i in lab], int)
yP2 = np.array([V[i] in ("relevante", "dúvida") for i in lab], int)
w = np.array([M[i]["tam_grupo"] / M[i]["amostra_grupo"] for i in lab], float)   # inverso da prob. de inclusão
aj_in = [k for k in aj_k if k in idx]
Xaj = X[[idx[k] for k in aj_in]]
R["n_rotulos"] = {"total": len(lab), "P1_pos": int(yP1.sum()), "P2_pos": int(yP2.sum()), "ajuste_extra": len(aj_in)}

# população a ordenar: entrada da F2 não lida
entra = lambda r: r["para_camada_C"] == "sim" and (r["camada_C_F1"] in ("ligada", "solta recente (2025-26)", "sem dado de citação")
                                                   or (r["camada_C_F1"] == "solta (desce)" and r["tipo_no_titulo"] == "True"))
lidos = {M[i]["chave"] for i in M}
pool = [key(r) for r in keep if entra(r) and key(r) not in lidos]
R["n_pool"] = len(pool)

# ---------- métricas ponderadas ----------
def k_at(s, y, ww, r=0.95):
    o = np.argsort(-s); cy = np.cumsum((ww * y)[o]) / (ww * y).sum(); cw = np.cumsum(ww[o]) / ww.sum()
    return float(cw[np.searchsorted(cy, r - 1e-12)])
def rec_at(s, y, ww, f):
    o = np.argsort(-s); cw = np.cumsum(ww[o]) / ww.sum(); top = o[cw <= f]
    return float((ww[top] * y[top]).sum() / (ww * y).sum())
def resumo(ss, y, ww):
    k = [k_at(s, y, ww) for s in ss]; ap = [average_precision_score(y, s, sample_weight=ww) for s in ss]
    return {"K95_media": round(float(np.mean(k)), 3), "K95_dp": round(float(np.std(k)), 3),
            "K90_media": round(float(np.mean([k_at(s, y, ww, .90) for s in ss])), 3),
            "AP": round(float(np.mean(ap)), 3),
            "rec@10%": round(float(np.mean([rec_at(s, y, ww, .10) for s in ss])), 3),
            "rec@25%": round(float(np.mean([rec_at(s, y, ww, .25) for s in ss])), 3)}

def lr():
    return make_pipeline(StandardScaler(), LogisticRegressionCV(Cs=[1e-4, 3e-4, 1e-3, 3e-3, 1e-2, 3e-2, 1e-1], cv=3,
                         scoring="average_precision", class_weight="balanced", max_iter=3000))

def oof(y, seed, extra=True, frac=1.0, flip=0.0, drop=None, Xtest=None):
    """Previsão fora da dobra para cada rótulo. extra = junta as 28 de ajuste como positivos no treino."""
    s = np.zeros(len(y)); rng = np.random.RandomState(seed)
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=seed).split(Xl, y):
        if drop is not None: tr = np.array([t for t in tr if lab[t] not in drop])
        if frac < 1.0:
            tr = np.concatenate([rng.choice(tr[y[tr] == c], max(2, int(round(frac * (y[tr] == c).sum()))), replace=False) for c in (0, 1)])
        ytr = y[tr].copy()
        if flip:
            f = rng.rand(len(ytr)) < flip; ytr[f] = 1 - ytr[f]
        Xtr = Xl[tr]
        if extra:
            Xtr = np.vstack([Xtr, Xaj]); ytr = np.concatenate([ytr, np.ones(len(Xaj), int)])
        m = lr().fit(Xtr, ytr)
        s[te] = m.predict_proba((Xtest if Xtest is not None else Xl)[te])[:, 1]
    return s

def knn_oof(y, seed, k=15):
    s = np.zeros(len(y)); Z = Xl / np.linalg.norm(Xl, axis=1, keepdims=True)
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=seed).split(Xl, y):
        sim = Z[te] @ Z[tr].T; nn = np.argsort(-sim, axis=1)[:, :k]; s[te] = y[tr][nn].mean(1)
    return s

NUCLEO = re.compile(r"compress|quantiz|prun|distill|efficien|inference|serving|edge|lightweight|on-device|"
                    r"\bLLMs?\b|language model|transformer|accelerat|deploy|embedded|tinyml|low-rank|sparsit", re.I)
F1rank = {"ligada": 3, "sem dado de citação": 3, "solta recente (2025-26)": 2, "solta (desce)": 1}
def baselines(seed):
    rng = np.random.RandomState(seed); eps = rng.rand(len(lab)) * 1e-3
    return {"aleatória": rng.rand(len(lab)),
            "ordem F1": np.array([F1rank[M[i]["camada_C_F1"]] for i in lab]) + eps,
            "palavra núcleo no título": np.array([1.0 if NUCLEO.search(M[i]["title"]) else 0.0 for i in lab]) + eps}

# ---------- E1: modelo x linhas de base, P1 e P2 ----------
OOF = {}
for alvo, y in (("P1", yP1), ("P2", yP2)):
    OOF[alvo] = [oof(y, s) for s in SEEDS]
    R[f"E1_{alvo}"] = {"regressão logística": resumo(OOF[alvo], y, w),
                       "kNN (k=15)": resumo([knn_oof(y, s) for s in SEEDS], y, w)}
    for nome in ("aleatória", "ordem F1", "palavra núcleo no título"):
        R[f"E1_{alvo}"][nome] = resumo([baselines(s)[nome] for s in SEEDS], y, w)
    print(alvo, json.dumps(R[f"E1_{alvo}"], ensure_ascii=False), flush=True)
# P3: ordem por P1, medida contra P2 (quanto das dúvidas o P1 também traz)
R["E1_P3_ordemP1_medida_em_P2"] = resumo(OOF["P1"], yP2, w)

# ---------- E2: curva de aprendizado ----------
R["E2_curva"] = {f: resumo([oof(yP1, s, frac=f) for s in SEEDS], yP1, w)["K95_media"] for f in (0.25, 0.5, 0.75, 1.0)}
print("E2", R["E2_curva"], flush=True)
# ---------- E3: ruído de rótulo ----------
R["E3_ruido"] = {p: resumo([oof(yP1, s, flip=p) for s in SEEDS], yP1, w)["K95_media"] for p in (0.05, 0.10, 0.20)}
print("E3", R["E3_ruido"], flush=True)
# ---------- E4: sem as discordâncias da dupla leitura no treino ----------
R["E4_sem_discordantes"] = resumo([oof(yP1, s, drop=discord) for s in SEEDS], yP1, w)["K95_media"]
# ---------- E5: sem as 28 de ajuste como positivos extras ----------
R["E5_sem_ajuste"] = resumo([oof(yP1, s, extra=False) for s in SEEDS], yP1, w)["K95_media"]
# ---------- E6: viés de amostragem (sem peso x com peso; rótulos por grupo x população) ----------
R["E6_K95_sem_peso"] = resumo(OOF["P1"], yP1, np.ones(len(lab)))["K95_media"]
pg = Counter(byk[k]["camada_B_grupo_final"] for k in pool); lg = Counter(M[i]["grupo"] for i in lab)
R["E6_grupos_top"] = [(g, pg[g], lg[g]) for g, _ in pg.most_common(8)]
print("E4/E5/E6", R["E4_sem_discordantes"], R["E5_sem_ajuste"], R["E6_K95_sem_peso"], flush=True)

# ---------- E7: cobertura por subárea (proxy = grupos de termos do pool + hardware) ----------
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
SUB["hardware (§1.2.1 e)"] = [re.compile(r"accelerat|FPGA|ASIC|hardware|GPU|NPU|in-memory comput", re.I)]
txt = {i: E[i]["title"] + " " + E[i]["abstract"] for i in lab}
subs = {i: [g for g, rs in SUB.items() if any(r.search(txt[i]) for r in rs)] for i in lab}
e7 = {}
for g in SUB:
    mask = np.array([g in subs[i] for i in lab])
    ypos = yP1 * mask
    e7[g] = {"relevantes_rotuladas": int(ypos.sum()),
             "rec@25%": round(float(np.mean([rec_at(s, ypos, w, .25) for s in OOF["P1"]])), 3) if ypos.sum() else None,
             "K95": round(float(np.mean([k_at(s, ypos, w) for s in OOF["P1"]])), 3) if ypos.sum() >= 3 else None}
R["E7_subarea"] = e7
R["E7_relevantes_sem_subarea"] = int(sum(1 for i, yy in zip(lab, yP1) if yy and not subs[i]))
print("E7", json.dumps(e7, ensure_ascii=False), flush=True)

# ---------- E8: por ano ----------
def faixa(y): y = int(y or 0); return "até 2022" if y <= 2022 else "2023-24" if y <= 2024 else "2025-26"
e8 = {}
for f in ("até 2022", "2023-24", "2025-26"):
    mask = np.array([faixa(M[i]["year"]) == f for i in lab]); ypos = yP1 * mask
    e8[f] = {"relevantes": int(ypos.sum()), "rec@25%": round(float(np.mean([rec_at(s, ypos, w, .25) for s in OOF["P1"]])), 3) if ypos.sum() else None}
R["E8_ano"] = e8

# ---------- E9: survey x primário no topo ----------
top = Counter()
for s in OOF["P1"]:
    o = np.argsort(-s); cw = np.cumsum(w[o]) / w.sum()
    for t in o[cw <= .25]:
        i = lab[t]; v = V[i]
        k = "relevante" if v == "relevante" else "dúvida" if v == "dúvida" else \
            "fora: não é survey" if "3.4" in (A3.get(i, {}).get("regra") or "") else "fora: outro motivo" if v == "fora" else "claramente fora (a1)"
        top[k] += w[t] / len(SEEDS)
tot = sum(top.values()); R["E9_composicao_topo25"] = {k: round(v / tot, 3) for k, v in top.most_common()}

# ---------- E10: quase-duplicatas ----------
Zl = Xn[[idx[M[i]["chave"]] for i in lab]]
S = Zl @ Zl.T; np.fill_diagonal(S, 0)
R["E10_pares_rotulados_cos>0.97"] = int((np.triu(S) > 0.97).sum())
Zp = Xn[[idx[k] for k in pool]]
mx = np.max(Zl @ Zp.T, axis=0)
R["E10_pool_com_gemea_rotulada_cos>0.97"] = int((mx > 0.97).sum())

# ---------- E11: obras só com título ----------
sem_abs_pool = sum(1 for k in pool if byk[k]["tem_abstract"] != "sim")
R["E11_pool_sem_abstract"] = sem_abs_pool
try:
    from sentence_transformers import SentenceTransformer
    st = SentenceTransformer("allenai/specter2_base", device="cuda")
    Xt = st.encode([M[i]["title"] for i in lab], batch_size=64, convert_to_numpy=True).astype(np.float32)
    ss = [oof(yP1, s, Xtest=Xt) for s in SEEDS]
    R["E11_so_titulo"] = resumo(ss, yP1, w)
except Exception as ex:
    R["E11_so_titulo"] = f"não medido: {ex}"
print("E11", R["E11_so_titulo"], flush=True)

# ---------- E12: onde está o gabarito (só metadado) ----------
R["E12_grupos_ajuste"] = Counter(byk[k]["camada_B_grupo_final"] for k in aj_k if k in byk).most_common()
R["E12_grupos_teste"] = Counter(byk[k]["camada_B_grupo_final"] for k in te_k if k in byk).most_common()

# ---------- E13: deslocamento de domínio — nota diagnóstica no pool, por grupo ----------
mfin = lr().fit(np.vstack([Xl, Xaj]), np.concatenate([yP1, np.ones(len(Xaj), int)]))
sp = mfin.predict_proba(X[[idx[k] for k in pool]])[:, 1]
cut = np.quantile(sp, 0.75)
gtop = Counter(byk[k]["camada_B_grupo_final"] for k, v in zip(pool, sp) if v >= cut)
R["E13_topo25_por_grupo"] = [(g, gtop[g], pg[g], lg[g]) for g, _ in gtop.most_common(10)]
R["E13_topo25_sem_rotulo_no_grupo"] = sum(v for g, v in gtop.items() if lg[g] == 0)
# ---------- E14: amostra de controle abaixo do corte (custo) ----------
R["E14_controle"] = {n: f"0 relevantes em {n} -> < {300 / n:.1f}% abaixo do corte (95%)" for n in (60, 100, 150)}

json.dump(R, open(os.path.join(OUT, "resultados.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps({k: v for k, v in R.items() if not k.startswith("E1_")}, ensure_ascii=False, indent=1, default=str))
