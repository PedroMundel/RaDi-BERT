"""Teste (27/09): o classificador vai melhor quando o alvo é relevância de TÓPICO pura (Saracevic)?
Alvo T = relevante + dúvida (c) + 'não é survey: primário da área' + 'não é survey: sistema/ferramenta'.
Mesma validação ponderada de diag_riscos.py. Reusa as funções dele (runpy). Não grava nada fora de C1-diagnostico."""
import runpy, os, json, re
import numpy as np
G = runpy.run_path(os.path.join(os.path.dirname(__file__), "diag_riscos.py"))
lab, V, A3, w, yP1, yP2, oof, resumo, SEEDS, baselines, knn_oof = (G[k] for k in "lab V A3 w yP1 yP2 oof resumo SEEDS baselines knn_oof".split())
def sub(i):
    r = (A3.get(i, {}).get("regra") or "") + " " + (A3.get(i, {}).get("motivo") or "")
    return "primário" if re.search(r"prim[aá]rio", r, re.I) else "sistema" if re.search(r"sistema|ferramenta", r, re.I) else ""
yT = np.array([V[i] in ("relevante", "dúvida") or (V[i] == "fora" and "3.4" in (A3.get(i, {}).get("regra") or "") and sub(i) != "") for i in lab], int)
R = {"n_pos_T": int(yT.sum()), "composicao": {"relevante": int(yP1.sum()), "dúvida": int(yP2.sum() - yP1.sum()), "não é survey da área": int(yT.sum() - yP2.sum())}}
R["LR_alvo_T"] = resumo([oof(yT, s) for s in SEEDS], yT, w)
R["kNN_alvo_T"] = resumo([knn_oof(yT, s) for s in SEEDS], yT, w)
R["aleatória_alvo_T"] = resumo([baselines(s)["aleatória"] for s in SEEDS], yT, w)
R["referência_LR_alvo_P1"] = G["R"]["E1_P1"]["regressão logística"]
R["referência_LR_alvo_P2"] = G["R"]["E1_P2"]["regressão logística"]
print(json.dumps(R, ensure_ascii=False, indent=1))
json.dump(R, open(os.path.join(G["OUT"], "resultados-alvo-topico.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
