# Leitura da grade do RTE com o segundo checkpoint MS-MARCO (Capreolus), 18/11/2026

**Procedência:** pedido do Pedro ("depois capreolus"); critério escrito antes de rodar em
`docs/2026-11-18-gaps-da-argumentacao.md`, "Gap 3". Checkpoint `Capreolus/bert-base-msmarco`. Mesma grade de 10/11
com o nboost: dois braços, aquecimento `500` (Tabela 4), fases A/B/C, 5 sementes, micro-lote 8, PC (RTX 5060),
código `59278b8-dirty`, 64 minutos. Dev do RTE (277 pares) no papel de teste. CSVs copiados para `pc/`.

**Conferido:** as 10 linhas de `pc/resultados.csv`, as médias e a diferença pareada calculadas sobre o arquivo; os
pesos do encoder carregam inteiros (auditoria de treino: nenhuma chave faltando, 197 tensores iguais ao arquivo do
Hub, diferentes do BERT base e do nboost). **Não conferido:** as medidas de gradiente desta grade
(`pc/gradientes.csv`, `pc/palavras.csv`) não foram lidas.

**Como ler:** ROC-AUC e acurácia médios de 5 sementes, com o desvio padrão entre sementes; na linha da diferença,
decoder menos sem decoder, pareada por semente, com o intervalo de 95% e em quantas sementes o decoder vence.

| | ROC-AUC | Acurácia |
|---|---|---|
| Agrawal 2025, Tabela 2: BERT (MS-MARCO) | 0,4754 (±0,011) | |
| Agrawal 2025, Tabela 2: + Reasoning | 0,5873 (±0,007) | |
| Aqui, Capreolus ajustado no RTE | 0,743 ± 0,013 | 0,682 ± 0,025 |
| Aqui, Capreolus + decoder | 0,721 ± 0,006 | 0,659 ± 0,014 |
| Decoder menos sem decoder | **−0,022 (−0,040 a −0,004), vence 0 de 5** | −0,023 (−0,067 a +0,021), vence 1 de 5 |
| (10/11) nboost ajustado no RTE | 0,767 ± 0,013 | 0,721 |
| (10/11) nboost + decoder | 0,718 ± 0,013 | 0,665 |

As três perguntas do critério:

1. **O baseline dá o número do artigo? Não.** 0,743, fora da faixa de 0,44 a 0,51; a menor das 5 sementes dá 0,729.
2. **O 0,767 era do checkpoint nboost? Não.** O Capreolus fica a 0,024 dele, dentro do 0,03 que 5 sementes no RTE
   não distinguem. Os dois checkpoints contam a mesma história.
3. **O decoder ajuda aqui? Não: perde.** No ROC-AUC o intervalo fica inteiro abaixo de zero e o decoder perde nas
   5 sementes (de −0,009 a −0,040). Na acurácia o intervalo cruza o zero.

**O que isso sustenta:** nos dois checkpoints "BERT base MS-MARCO" que existem no Hub com esse nome, o baseline
ajustado no RTE fica entre 0,74 e 0,77 e o decoder piora o ROC-AUC com intervalo fora do zero. **O que não
sustenta:** que seja assim com o checkpoint dos autores, que o artigo não nomeia; nem "o decoder atrapalha" em
geral (é o RTE, 2.470 pares, a receita da Tabela 4, justificativas do Qwen).

**Observação, sem conclusão:** como em 10/11, o braço com decoder dos dois checkpoints e do BERT cru cai no mesmo
valor (0,721 aqui; 0,718 no nboost; 0,718 no BERT cru). É compatível com a H2 de
`docs/2026-11-10-hipoteses-do-nulo.md` (a fase B desfaz o que o encoder trazia), que continua sem teste próprio.
