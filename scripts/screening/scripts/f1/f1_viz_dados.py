"""Dados da visualização da árvore de citação da F1: posições (spring layout), arestas dirigidas, atributos."""
import json, math, os, runpy, sys, time
from collections import Counter
import networkx as nx

SCR = os.path.dirname(os.path.abspath(__file__))
sys.argv = ["f1_rede.py", "--preview"]
g = runpy.run_path(os.path.join(SCR, "f1_rede.py"))
K, byk, dest, comp, comps, s2refs, oarefs, pid2k, oa2k = (g[x] for x in
    ("K", "byk", "dest", "comp", "comps", "s2refs", "oarefs", "pid2k", "oa2k"))
aj, te = set(g["aj_k"]), set(g["te_k"])

# arestas dirigidas: k cita j
E = set()
for k in K:
    for j in [pid2k.get(x) for x in (s2refs(k) or [])] + [oa2k.get(x) for x in (oarefs(k) or [])]:
        if j and j != k:
            E.add((k, j))
nos = [k for k in K if len(comps[comp[k]]) >= 2]
idx = {k: i for i, k in enumerate(nos)}
indeg = Counter(j for _, j in E)
outdeg = Counter(k for k, _ in E)

G = nx.Graph(); G.add_nodes_from(nos); G.add_edges_from((a, b) for a, b in E)
main = max(nx.connected_components(G), key=len)
t0 = time.time()
pos = nx.spring_layout(G.subgraph(main), k=0.02, iterations=120, seed=42)
print("layout", round(time.time() - t0), "s", flush=True)
# escala radial por posto: o spring deixa um miolo denso e um halo de obras de grau 1; mantém a direção a
# partir do centro e troca a distância pelo posto (sqrt = densidade uniforme no disco)
import numpy as np
ks = list(main); M = np.array([pos[k] for k in ks]); c = np.median(M, axis=0); d = M - c
r = np.hypot(d[:, 0], d[:, 1]); ang = np.arctan2(d[:, 1], d[:, 0])
rank = np.argsort(np.argsort(r)) / (len(r) - 1)
rr = 0.5 * np.sqrt(rank)
for k, rad, an in zip(ks, rr, ang):
    pos[k] = (0.5 + rad * math.cos(an), 0.5 + rad * math.sin(an))
# ilhas pequenas: grade compacta numa faixa à direita do bloco
outras = sorted((c for c in nx.connected_components(G) if c != main), key=len, reverse=True)
ncol = 8; nrow = math.ceil(len(outras) / ncol); cw, rh = 0.3 / ncol, 1.0 / max(nrow, 1)
for t, c in enumerate(outras):
    cx, cy = 1.12 + (t % ncol) * cw, (t // ncol + 0.5) * rh
    sub = nx.spring_layout(G.subgraph(c), scale=min(cw, rh) * 0.35, seed=1) if len(c) > 1 else {next(iter(c)): (0, 0)}
    for n, (u, v) in sub.items():
        pos[n] = (cx + u, cy + v)

def gab(k):
    return "ajuste" if k in aj else "teste" if k in te else ""
nodes = [[round(float(pos[k][0]), 4), round(float(pos[k][1]), 4), int(byk[k]["year"] or 0), byk[k]["title"][:160],
          int(byk[k]["cit"] or 0), indeg[k], outdeg[k], dest[k], byk[k]["camada_B"], gab(k), int(k in main)] for k in nos]
edges = [[idx[a], idx[b]] for a, b in E if a in idx and b in idx]
soltas = Counter(dest[k] for k in K if len(comps[comp[k]]) < 2)
out = dict(nodes=nodes, edges=edges, isoladas=soltas, total=len(K), main=len(main), ilhas=len(outras),
           ilhas_nos=sum(len(c) for c in outras))
json.dump(out, open(os.path.join(SCR, "f1_viz.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print(len(nodes), "nós", len(edges), "arestas", dict(soltas), "main", len(main), "ilhas", len(outras))
