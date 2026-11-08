"""Camada B, aplicação (Pedro 23/09: 'pode seguir' — aceita a proposta de classificação).
1) reatribui o grupo -1 ao grupo mais próximo (cosseno entre o embedding da obra e o centróide do grupo —
   equivalente à estratégia 'embeddings' do reduce_outliers do BERTopic); guarda a similaridade;
2) marca camada_B: núcleo / regra / verificar / fora; 3) mede a perda na metade de teste;
4) sorteia amostras dos grupos 'verificar' e dos 'fora'. Nada é apagado."""
import csv, json, os, random, re
import numpy as np
from collections import Counter, defaultdict

ROOT = r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial"
F1 = os.path.join(ROOT, "Screening", "fase1")
SCR = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(F1, "2026-09-22-floresta-obras.csv")
rows = list(csv.DictReader(open(PATH, encoding="utf-8-sig"))); cols = list(rows[0].keys())
keep = [x for x in rows if x["camada_A"].startswith("mantida")]
emb = np.load(os.path.join(SCR, "camadaB_emb_specter2.npy")).astype(np.float32)
assert len(emb) == len(keep)
emb /= np.linalg.norm(emb, axis=1, keepdims=True) + 1e-9
top = np.array([int(x["camada_B_topico"]) for x in keep])
ids = sorted(set(top) - {-1})
cent = np.stack([emb[top == t].mean(0) for t in ids]); cent /= np.linalg.norm(cent, axis=1, keepdims=True)
sim = emb @ cent.T
best = np.array(ids)[sim.argmax(1)]; bsim = sim.max(1)
CAT = {2: "núcleo", 36: "núcleo",
       6: "regra §1.2.1 c", 12: "regra §1.2.1 c", 34: "regra §1.2.1 b", 40: "regra §1.2.1 b",
       46: "regra §1.2.1 d", 52: "regra uso?", 49: "regra P2",
       5: "verificar", 4: "verificar", 16: "verificar", 25: "verificar", 14: "verificar", 11: "verificar", 21: "verificar"}
cat = lambda t: CAT.get(t, "fora")
for i, x in enumerate(keep):
    t = int(x["camada_B_topico"])
    if t == -1:
        x["camada_B_reatribuido"] = f"{best[i]} (sim {bsim[i]:.2f})"; t = int(best[i])
    else:
        x["camada_B_reatribuido"] = ""
    x["camada_B_grupo_final"] = str(t)
    x["camada_B"] = cat(t)
for x in rows:
    for c in ("camada_B_reatribuido", "camada_B_grupo_final", "camada_B"):
        x.setdefault(c, "")
with open(PATH, "w", encoding="utf-8-sig", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols + [c for c in ("camada_B_reatribuido", "camada_B_grupo_final", "camada_B") if c not in cols])
    w.writeheader(); w.writerows(rows)

out = {}
out["por_categoria"] = Counter(x["camada_B"] for x in keep)
out["reatribuidas"] = Counter(cat(int(x["camada_B_grupo_final"])) for x in keep if x["camada_B_reatribuido"])
out["sim_reatrib_quartis"] = [float(np.percentile(bsim[top == -1], q)) for q in (10, 25, 50, 75, 90)]
out["tam_grupo_final"] = Counter(x["camada_B_grupo_final"] for x in keep)

# perda no teste (mesma divisão de sempre)
v1 = list(csv.DictReader(open(os.path.join(F1, "2026-09-22-volta-1-obras.csv"), encoding="utf-8-sig")))
idx = {}
for x in v1:
    for k in (x["arxiv"], x["doi"]):
        if k: idx[k.lower()] = x
refids = [[c.strip() for c in l.strip().strip("|").split("|")][9].lower()
          for l in open(os.path.join(F1, "2026-09-21-candidatos-string-mae-exec2.md"), encoding="utf-8")
          if re.match(r"\| \d+ \| entra \|", l)]
ref = [idx[i] for i in refids if i in idx]; random.Random(42).shuffle(ref)
aj, te = ref[:len(ref) // 2], ref[len(ref) // 2:]
key = lambda x: x["s2"] if x["s2"] else f"ARXIV:{x['arxiv']}"
byk = {key(x): x for x in rows}
def dest(r):
    x = byk[r["s2"] or f"ARXIV:{r['arxiv']}"]
    return "excluída A" if x["camada_A"].startswith("excluída") else x["camada_B"]
out["teste"] = [(r["title"], dest(r)) for r in te]
out["ajuste"] = Counter(dest(r) for r in aj)

# amostras
rng = random.Random(2309)
G = defaultdict(list)
for x in keep: G[x["camada_B_grupo_final"]].append(x)
out["amostra_verificar"] = {t: [(x["year"], x["title"]) for x in rng.sample(G[str(t)], min(15, len(G[str(t)])))]
                            for t in sorted(k for k, v in CAT.items() if v == "verificar")}
fora = [x for x in keep if x["camada_B"] == "fora"]
out["amostra_fora"] = [(x["camada_B_grupo_final"], x["title"]) for x in rng.sample(fora, 40)]
core = {"área", "compressão", "inferência/serving", "adaptação", "edge"}
sus = [x for x in fora if x["tipo_no_titulo"] == "True" and set(x["grupos_titulo"].split("; ")) & core]
out["fora_suspeitas_n"] = len(sus)
out["fora_suspeitas_top"] = [(x["camada_B_grupo_final"], x["cit"], x["title"]) for x in sorted(sus, key=lambda x: -int(x["cit"] or 0))[:25]]
json.dump(out, open(os.path.join(SCR, "camadaB_aplicar.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(json.dumps({k: out[k] for k in ("por_categoria", "reatribuidas", "sim_reatrib_quartis", "ajuste", "fora_suspeitas_n")}, ensure_ascii=False, default=str))
print("TESTE:", Counter(d for _, d in out["teste"]))
for t, d in out["teste"]:
    if d not in ("núcleo",): print("   ", d, "|", t[:90])
