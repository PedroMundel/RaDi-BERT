"""Figuras estáticas da árvore de citação (para o docx de entrega)."""
import json, math, os
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.collections import LineCollection
SCR = os.path.dirname(os.path.abspath(__file__))
FIG = r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial\Screening\fase1\figs"
D = json.load(open(os.path.join(SCR, "f1_viz.json"), encoding="utf-8"))
N = D["nodes"]; E = D["edges"]
COR = {"ligada": "#2f7d5b", "golden": "#b8901a", "penúltima": "#7457d0", "solta recente (2025-26)": "#d0822a",
       "sem dado de citação": "#8b9690", "solta (desce)": "#b4473a"}
ROT = {"ligada": "ligada ao bloco da área", "golden": "golden ticket", "penúltima": "penúltima (bilhete 21-50)",
       "solta recente (2025-26)": "solta recente (fica)", "sem dado de citação": "sem dado de citação", "solta (desce)": "solta (desce)"}
x = np.array([n[0] for n in N]); y = np.array([n[1] for n in N])
rng = np.random.default_rng(42)
yr = np.clip([n[2] for n in N], 2020, 2026)
tx = (np.array(yr) - 2020) + 0.12 + 0.76 * rng.random(len(N))
ty = (y - y.min()) / (y.max() - y.min())
inn = np.array([n[5] for n in N]); size = 2 + 9 * np.sqrt(inn)
col = [COR[n[7]] for n in N]; gab = np.array([bool(n[9]) for n in N])

def fig(px, py, fname, title, arvore):
    f, ax = plt.subplots(figsize=(14, 9), dpi=150)
    seg = [[(px[a], py[a]), (px[b], py[b])] for a, b in E]
    ax.add_collection(LineCollection(seg, colors="#1c2420", linewidths=0.25, alpha=0.05))
    o = np.argsort(inn)
    ax.scatter(px[o], py[o], s=size[o], c=[col[i] for i in o], alpha=0.85, linewidths=0)
    ax.scatter(px[gab], py[gab], s=size[gab] + 60, facecolors="none", edgecolors="#1d5fc4", linewidths=1.4)
    for i in np.argsort(-inn)[:12]:
        t = N[i][3]; t = t if len(t) <= 48 else t[:46] + "..."
        ax.annotate(t, (px[i], py[i]), xytext=(6, 3), textcoords="offset points", fontsize=7.5, color="#1c2420")
    if arvore:
        for k in range(8): ax.axvline(k, color="#1c2420", alpha=0.08, lw=0.8)
        ax.set_xticks([k + 0.5 for k in range(7)]); ax.set_xticklabels([str(2020 + k) for k in range(7)])
        ax.set_yticks([]); ax.set_xlim(0, 7)
        ax.set_xlabel("raízes (antigas) -> folhas (recentes)")
    else:
        ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_visible(False)
    h = [Line2D([], [], marker="o", ls="", color=c, label=ROT[k]) for k, c in COR.items()]
    h.append(Line2D([], [], marker="o", ls="", markerfacecolor="none", markeredgecolor="#1d5fc4", label="gabarito"))
    ax.legend(handles=h, loc="lower left", fontsize=8, frameon=False)
    ax.set_title(title, loc="left", fontsize=12)
    f.tight_layout(); f.savefig(os.path.join(FIG, fname)); plt.close(f)

fig(x, y, "arvore_F1_rede.png", f"Rede de citação interna - {len(N)} obras com ligação (bloco da área: {D['main']}); tamanho = citações recebidas no conjunto", False)
fig(tx, ty, "arvore_F1_por_ano.png", "Árvore por ano - mesma rede, com o eixo horizontal no ano de publicação", True)
print("ok")
