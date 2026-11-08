"""Figura única da rede (vista 'Rede' da página, tema escuro) + linha de números, texto no padrão do matplotlib."""
import json, os
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
SCR = os.path.dirname(os.path.abspath(__file__))
OUT = r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial\Screening\fase1\figs\arvore_F1_rede_escura.png"
D = json.load(open(os.path.join(SCR, "f1_viz.json"), encoding="utf-8")); N = D["nodes"]; E = D["edges"]
COR = {"ligada": "#4fb487", "golden": "#e0bb45", "penúltima": "#9d86ec", "solta recente (2025-26)": "#eda253",
       "sem dado de citação": "#7d8a83", "solta (desce)": "#e0705f"}
x = np.array([n[0] for n in N]); y = np.array([n[1] for n in N]); inn = np.array([n[5] for n in N])
size = 3 + 10 * np.sqrt(inn); gab = np.array([bool(n[9]) for n in N])
f, ax = plt.subplots(figsize=(9, 11), dpi=150); f.patch.set_facecolor("#121614"); ax.set_facecolor("#121614")
ax.add_collection(LineCollection([[(x[a], y[a]), (x[b], y[b])] for a, b in E], colors="#dce4de", linewidths=0.2, alpha=0.05))
o = np.argsort(inn)
ax.scatter(x[o], y[o], s=size[o], c=[COR[N[i][7]] for i in o], alpha=0.9, linewidths=0)
ax.scatter(x[gab], y[gab], s=size[gab] + 70, facecolors="none", edgecolors="#6aa3ff", linewidths=1.2)
for i in np.argsort(-inn)[:10]:
    t = N[i][3]; t = t if len(t) <= 44 else t[:42] + "..."
    ax.text(x[i] + 0.012, y[i], t, color="white", fontsize=8)
ax.invert_yaxis(); ax.set_xticks([]); ax.set_yticks([])
for s in ax.spines.values(): s.set_visible(False)
tot = sum(D["isoladas"].values())
fmt = lambda n: f"{n:,}".replace(",", ".")
f.text(0.02, 0.015, f"{fmt(D['total'])} obras    {fmt(len(E))} citações internas    bloco da área {fmt(D['main'])}    "
       f"{D['ilhas']} ilhas ({D['ilhas_nos']} obras)    isoladas {fmt(tot)}", color="white")
f.tight_layout(rect=(0, 0.03, 1, 1)); f.savefig(OUT, facecolor=f.get_facecolor()); print(OUT)
