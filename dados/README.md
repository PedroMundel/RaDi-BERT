# Dados

`dados/esnli/` fica fora do git (188 MB). Baixar da fonte, Camburu et al. 2018:

```bash
mkdir -p dados/esnli
for f in esnli_dev.csv esnli_train_1.csv esnli_train_2.csv; do
  curl -L -o dados/esnli/$f https://raw.githubusercontent.com/OanaMariaCamburu/e-SNLI/master/dataset/$f
done
```

`dados/rte/` fica fora do git (653 KB). RTE do GLUE (Wang et al. 2018), no Parquet que o HF Hub converte de
`nyu-mll/glue`, config `rte`; só treino (2.490 pares) e validação (277). O teste do GLUE não traz rótulo. Baixado em
09/11/2026; colunas `sentence1`, `sentence2`, `label` (0 = `entailment`, 1 = `not_entailment`), `idx`:

```bash
mkdir -p dados/rte
for s in train validation; do
  curl -L -o dados/rte/rte_$s.parquet "https://huggingface.co/datasets/nyu-mll/glue/resolve/refs%2Fconvert%2Fparquet/rte/$s/0000.parquet"
done
sha256sum dados/rte/*.parquet
# a6252ab17015d718f6de1effe0980f7b158df63e3d16207cd8bd396b608e5147  rte_train.parquet
# fb2aa2e04f551133ba663617a15ae133dc22b0f6a969bc0629b5ea6003ee9cf8  rte_validation.parquet
```

`dados/mnli/` fica fora do git (10 MB). MultiNLI (Williams et al. 2018), só as duas validações (9.815 pares matched,
9.832 mismatched), do Parquet de `nyu-mll/multi_nli` no HF Hub. Baixado em 18/11/2026, com o OK do Pedro, para o
teste fora de domínio; colunas usadas `premise`, `hypothesis`, `label` (0 = `entailment`, 1 = `neutral`,
2 = `contradiction`, como no e-SNLI), `genre`:

```bash
mkdir -p dados/mnli
for s in matched mismatched; do
  curl -L -o dados/mnli/validation_$s.parquet "https://huggingface.co/datasets/nyu-mll/multi_nli/resolve/main/data/validation_$s-00000-of-00001.parquet"
done
sha256sum dados/mnli/*.parquet
# 350c26950b55f460b50d36c76aef87d64b49c78812d7abf7bf97e5fede10f186  validation_matched.parquet
# 6b0e1231cebedd255000a7d1732af37ad0500902239db625e231ed77c0c8f2f8  validation_mismatched.parquet
```

`dados/hans/` fica fora do git (15 MB). HANS (McCoy, Pavlick & Linzen 2019), o conjunto de avaliação (30.000 pares,
metade `entailment`, metade `non-entailment`, 10.000 por heurística), do GitHub dos autores. Baixado em 18/11/2026,
com o OK do Pedro; a licença aparece como "unknown" no HF Hub e não foi conferida no repositório:

```bash
mkdir -p dados/hans
curl -L -o dados/hans/heuristics_evaluation_set.txt https://raw.githubusercontent.com/tommccoy1/hans/master/heuristics_evaluation_set.txt
sha256sum dados/hans/heuristics_evaluation_set.txt
# c55b62feef9913070e88f38938dc2492018c945ac81f70139346472494124e79  heuristics_evaluation_set.txt
```

`resultados/lote-35B/amostra-treino.csv` também fica fora (112 MB): é a amostra embaralhada do treino com semente 42,
regenerada por `src/radibert/lote.py`.

`dados/wiegreffe2022/snli_test.csv` está no git (616 KB).
