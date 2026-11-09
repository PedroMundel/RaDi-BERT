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

`resultados/lote-35B/amostra-treino.csv` também fica fora (112 MB): é a amostra embaralhada do treino com semente 42,
regenerada por `src/radibert/lote.py`.

`dados/wiegreffe2022/snli_test.csv` está no git (616 KB).
