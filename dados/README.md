# Dados

`dados/esnli/` fica fora do git (188 MB). Baixar da fonte, Camburu et al. 2018:

```bash
mkdir -p dados/esnli
for f in esnli_dev.csv esnli_train_1.csv esnli_train_2.csv; do
  curl -L -o dados/esnli/$f https://raw.githubusercontent.com/OanaMariaCamburu/e-SNLI/master/dataset/$f
done
```

`resultados/lote-35B/amostra-treino.csv` também fica fora (112 MB): é a amostra embaralhada do treino com semente 42,
regenerada por `src/radibert/lote.py`.

`dados/wiegreffe2022/snli_test.csv` está no git (616 KB).
