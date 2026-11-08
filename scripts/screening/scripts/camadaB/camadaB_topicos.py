"""Camada B: mapa de tópicos (BERTopic + SPECTER2 base) sobre as obras mantidas pela camada A.
Não exclui nada: atribui um tópico a cada obra e produz a tabela de tópicos para o Pedro marcar lixo."""
import csv, json, os, random, re, sys, time
import numpy as np

ROOT = r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial"
F1 = os.path.join(ROOT, "Screening", "fase1")
SCR = os.path.dirname(os.path.abspath(__file__))
FLO = os.path.join(F1, "2026-09-22-floresta-obras.csv")
MIN_TOPIC = 100          # tamanho mínimo de tópico (declarado antes de rodar)
SEED = 42

rows = list(csv.DictReader(open(FLO, encoding="utf-8-sig")))
keep = [x for x in rows if x["camada_A"].startswith("mantida")]
print(f"obras mantidas pela camada A: {len(keep)}", flush=True)

# abstracts: vêm do bruto (o CSV da floresta só tem sim/não)
import glob
abs_by = {}
for path in glob.glob(os.path.join(F1, "raw", "2026-09-22-exec3-*-*.json")):
    if "passo0" in path:
        continue
    d = json.load(open(path, encoding="utf-8"))
    for p in d["papers"]:
        a = p.get("abstract") or p.get("summary") or ""
        k = p.get("paperId") or ("ARXIV:" + re.sub(r"v\d+$", "", p.get("id") or ""))
        if a and len(a) > len(abs_by.get(k, "")):
            abs_by[k] = a
    print(f"  abstracts carregados de {os.path.basename(path)}", flush=True)
key = lambda x: x["s2"] if x["s2"] else f"ARXIV:{x['arxiv']}"

from sentence_transformers import SentenceTransformer
model = SentenceTransformer("allenai/specter2_base", device="cuda")
sep = model.tokenizer.sep_token
docs = [x["title"] + (sep + abs_by[key(x)] if abs_by.get(key(x)) else "") for x in keep]
titles = [x["title"] for x in keep]
EMB = os.path.join(SCR, "camadaB_emb_specter2.npy")
if os.path.exists(EMB):
    emb = np.load(EMB).astype(np.float32)
else:
    t0 = time.time()
    emb = model.encode(docs, batch_size=64, show_progress_bar=False, convert_to_numpy=True)
    np.save(EMB, emb.astype(np.float16))
    print(f"embeddings: {emb.shape} em {time.time()-t0:.0f}s", flush=True)

from umap import UMAP
from hdbscan import HDBSCAN
from sklearn.feature_extraction.text import CountVectorizer
from bertopic import BERTopic
umap = UMAP(n_neighbors=15, n_components=5, min_dist=0.0, metric="cosine", random_state=SEED)
hdb = HDBSCAN(min_cluster_size=MIN_TOPIC, metric="euclidean", cluster_selection_method="eom", prediction_data=True)
vec = CountVectorizer(stop_words="english", ngram_range=(1, 2), min_df=5)
tm = BERTopic(embedding_model=model, umap_model=umap, hdbscan_model=hdb, vectorizer_model=vec, verbose=True)
t0 = time.time()
topics, _ = tm.fit_transform(titles, embeddings=emb)   # palavras-chave pelos títulos (legíveis); agrupamento pelos embeddings de título+abstract
print(f"BERTopic: {len(set(topics))} tópicos em {time.time()-t0:.0f}s", flush=True)

for x, t in zip(keep, topics):
    x["camada_B_topico"] = str(t)
json.dump({key(x): x["camada_B_topico"] for x in keep}, open(os.path.join(F1, "raw", "2026-09-23-camadaB-topicos.json"), "w"))
info = tm.get_topic_info()
kw = {int(r.Topic): ", ".join(w for w, _ in (tm.get_topic(int(r.Topic)) or [])[:8]) for r in info.itertuples()}
json.dump({"kw": kw, "min_topic": MIN_TOPIC, "seed": SEED, "n_docs": len(keep)},
          open(os.path.join(F1, "raw", "2026-09-23-camadaB-palavras.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("CAMADA B CONCLUIDA", flush=True)
