"""Diagnóstico, parte 2 (27/09): mede a fundo três riscos da parte 1 e o efeito de correções candidatas. Reusa o
estado de diag_riscos.py por import (roda a parte 1 de novo; ~minutos). Não grava na tabela-mestra."""
import runpy, json, os, sys, re
import numpy as np
from collections import Counter
from sklearn.model_selection import StratifiedGroupKFold
G = runpy.run_path(os.path.join(os.path.dirname(__file__), "diag_riscos.py"))
lab, M, V, w, yP1, Xl, Xaj, OOF, resumo, lr, knn_oof, SEEDS, byk, Xn, idx, subs, rec_at, k_at, A3 = (G[k] for k in
    "lab M V w yP1 Xl Xaj OOF resumo lr knn_oof SEEDS byk Xn idx subs rec_at k_at A3".split())
P = {}
# 1. tamanho efetivo dos positivos na validação ponderada
wp = w[yP1 == 1]; P["n_efetivo_positivos"] = round(float(wp.sum() ** 2 / (wp ** 2).sum()), 1)
P["massa_top11_positivos"] = round(float(np.sort(wp)[::-1][:11].sum() / wp.sum()), 3)
# 2. quase-duplicatas: exemplos e validação agrupada
Zl = Xn[[idx[M[i]["chave"]] for i in lab]]; S = Zl @ Zl.T; np.fill_diagonal(S, 0)
pares = np.argwhere(np.triu(S) > 0.97)
P["exemplos_pares"] = [(M[lab[a]]["title"][:70], M[lab[b]]["title"][:70], round(float(S[a, b]), 3)) for a, b in pares[:6]]
P["pares_mesmo_titulo"] = int(sum(1 for a, b in pares if re.sub(r"\W", "", M[lab[a]]["title"].lower()) == re.sub(r"\W", "", M[lab[b]]["title"].lower())))
comp = list(range(len(lab)))
def f(x):
    while comp[x] != x: comp[x] = comp[comp[x]]; x = comp[x]
    return x
for a, b in pares: comp[f(a)] = f(b)
grp = np.array([f(i) for i in range(len(lab))])
def oof_grp(y, seed):
    s = np.zeros(len(y))
    for tr, te in StratifiedGroupKFold(5, shuffle=True, random_state=seed).split(Xl, y, grp):
        m = lr().fit(np.vstack([Xl[tr], Xaj]), np.concatenate([y[tr], np.ones(len(Xaj), int)])); s[te] = m.predict_proba(Xl[te])[:, 1]
    return s
P["validacao_agrupada_P1"] = resumo([oof_grp(yP1, s) for s in SEEDS], yP1, w)
# 3. survey x primário
tipo = np.array([byk[M[i]["chave"]]["tipo_no_titulo"] == "True" for i in lab])
nao_surv = np.array(["3.4" in (A3.get(i, {}).get("regra") or "") and V[i] == "fora" for i in lab])
P["relevantes_sem_palavra_de_tipo"] = f"{int((yP1 & ~tipo).sum())} de {int(yP1.sum())}"
P["nao_survey_sem_palavra_de_tipo"] = f"{int((nao_surv & ~tipo).sum())} de {int(nao_surv.sum())}"
for beta in (1.0, 0.5, 0.25):
    ss = [s * np.where(tipo, 1.0, beta) for s in OOF["P1"]]
    r = resumo(ss, yP1, w)
    P[f"penalidade_sem_tipo_beta{beta}"] = {"K95": r["K95_media"], "rec@25%": r["rec@25%"], "AP": r["AP"]}
# 4. subárea minoritária: conjunto LR + kNN (média de posições)
def rank(s): return np.argsort(np.argsort(s)) / len(s)
kn = [knn_oof(yP1, s) for s in SEEDS]
ens = [0.5 * rank(a) + 0.5 * rank(b) for a, b in zip(OOF["P1"], kn)]
P["conjunto_LR_kNN"] = resumo(ens, yP1, w)
for nome, ss in (("LR", OOF["P1"]), ("LR+kNN", ens)):
    P[f"subarea_rec25_{nome}"] = {g: round(float(np.mean([rec_at(s, yP1 * np.array([g in subs[i] for i in lab]), w, .25) for s in ss])), 3)
                                 for g in ("compressão", "edge", "hardware (§1.2.1 e)", "adaptação")}
print(json.dumps(P, ensure_ascii=False, indent=1))
json.dump(P, open(os.path.join(G["OUT"], "resultados-patches.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
