# Limpeza em camadas A e B

## Camada A - campo de estudo

Cada obra vem da base com os campos em que foi classificada (Física, Medicina, Educação...). Os candidatos a sair foram os 17 campos em que não caiu nenhum survey de referência. Sozinho, isso é evidência fraca, porque a referência é pequena. Por isso o corte teve travas:

- obra com termo central do pool no título nunca sai (salvou 1.142);
- conferi a olho uma amostra sorteada de 30 excluídas, todas de fora da área;
- medi a perda na metade de teste da referência: 1 de 29.

Medicina, Educação e Matemática ficaram porque têm surveys da área. Resultado: 118.659 -> 74.791.

## Camada B - assunto

Transformei título e resumo de cada obra num vetor com o SPECTER2, um encoder BERT treinado em artigos científicos. O BERTopic agrupou os vetores parecidos em 66 grupos e nomeou cada um pelas palavras típicas dos títulos. Revisei os grupos um a um e marquei os de outra área (segurança de IoT, redes 5G, língua de sinais, OCR...), com a mesma trava do título.

27 dos 28 surveys de ajuste ficaram concentrados em 3 grupos, sinal de que o agrupamento separa a área. Resultado: 74.791 -> 14.901. Perda acumulada na metade de teste: continua 1 de 29.

Nada foi apagado nas duas camadas: cada obra carrega em que camada caiu e por quê.
