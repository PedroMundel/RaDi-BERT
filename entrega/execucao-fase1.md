# Execução da Fase 1 do screening

## Execução 1 - string inicial

Rodei a string composta do pool de termos no Semantic Scholar e no arXiv, com piso de 100 citações. O retorno foi de 1.721, 1.734 e 409 obras por base e filtro. Cerca de 94% vinha de dois termos meus, "resource-constrained" e "on-device", que puxavam obras de outras áreas.

Em vez de apagar os termos, movi os dois para uma string própria (edge). Assim eles continuam sendo buscados, mas não contaminam a busca principal.

## Execução 2 - calibração

Com a string corrigida, a busca devolveu 154 obras únicas. Classifiquei cada uma pelo título:

| decisão | obras |
|---|---|
| entra | 58 |
| dentro da área, sem filtro de qualidade | 9 |
| borda (decisão minha na leitura) | 36 |
| fora da área | 40 |
| não é survey | 12 |

As 58 que entram viraram a referência usada para medir a perda de cada corte seguinte.

## Execução 3 - busca final

Rodei a string principal e as 7 strings filhas, nas duas bases, sem piso de citação. Foram 138.789 registros e 118.659 obras únicas depois de remover duplicatas. Esse volume é a entrada da limpeza descrita no documento Arvore de Citacao.
