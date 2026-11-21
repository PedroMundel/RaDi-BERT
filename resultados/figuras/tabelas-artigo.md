# Tabelas para o artigo (geradas por `graficos_projeto.py` em 18/11/2026)

Todas saem dos mesmos arquivos das figuras; nenhuma traz número digitado à mão.

## 1. e-SNLI, 16.000 pares: os quatro braços

Como ler: média e desvio padrão entre 5 sementes, no dev do e-SNLI (9.842 pares).

| Braço | ROC-AUC | Acurácia (%) | Sementes |
|---|---|---|---|
| Sem decoder, treino comum | 0,929 ± 0,005 | 83,4 ± 0,3 | 5 |
| Sem decoder, mesmo calendário | 0,936 ± 0,005 | 83,7 ± 0,4 | 5 |
| Com decoder, justificativa do par | 0,932 ± 0,001 | 82,8 ± 0,3 | 5 |
| Com decoder, justificativa de outro par | 0,916 ± 0,002 | 80,7 ± 0,6 | 5 |

## 2. e-SNLI, 16.000 pares: diferenças pareadas

Como ler: primeiro braço menos o segundo, semente a semente; entre parênteses o intervalo de 95%; acurácia em pontos percentuais.

| Comparação | ROC-AUC | Acurácia (pontos) |
|---|---|---|
| Sem decoder, mesmo calendário menos sem decoder, treino comum | +0,007 (+0,006 a +0,008) | +0,4 (+0,3 a +0,5) |
| Com decoder, justificativa do par menos sem decoder, mesmo calendário | -0,004 (-0,011 a +0,003) | -0,9 (-1,6 a -0,3) |
| Com decoder, justificativa de outro par menos sem decoder, mesmo calendário | -0,020 (-0,027 a -0,013) | -3,0 (-4,2 a -1,9) |
| Com decoder, justificativa do par menos com decoder, justificativa de outro par | +0,016 (+0,014 a +0,019) | +2,1 (+1,3 a +2,9) |

## 3. Decoder menos sem decoder, em todas as condições

Como ler: diferença pareada de ROC-AUC com o intervalo de 95%; a coluna do meio é o ROC-AUC do braço sem decoder.

| Condição | Sem decoder | Decoder menos sem decoder | Sementes |
|---|---|---|---|
| RTE, BERT base, aquecimento proporcional | 0,736 | -0,028 (-0,071 a +0,014) | 5 |
| RTE, BERT base, aquecimento da Tabela 4 | 0,711 | +0,007 (-0,031 a +0,045) | 5 |
| RTE, BERT MS-MARCO (nboost) | 0,767 | -0,049 (-0,077 a -0,021) | 5 |
| RTE, BERT MS-MARCO (Capreolus) | 0,743 | -0,022 (-0,040 a -0,004) | 5 |
| RTE, T5 v1.1 como encoder | 0,636 | -0,114 (-0,140 a -0,089) | 5 |
| RTE, BERT small | 0,682 | -0,004 (-0,020 a +0,012) | 5 |
| RTE, BERT tiny | 0,622 | -0,010 (-0,029 a +0,009) | 5 |
| e-SNLI, 4.000 pares | 0,916 | -0,007 (-0,015 a +0,002) | 5 |
| e-SNLI, 16.000 pares | 0,929 | +0,003 (-0,004 a +0,010) | 5 |

## 4. Três pares com a justificativa do par e a trocada

Como ler: o primeiro par de cada rótulo no lote de 16.000; a justificativa trocada é a que o braço 'de outro par' recebe (outro par do mesmo rótulo, troca fixa com semente 0).

| Rótulo | Premissa | Hipótese | Justificativa do par (Qwen 35B) | Justificativa trocada |
|---|---|---|---|---|
| entailment | A small white dog climbs over a log. | An animal is near a log. | A dog is an animal, and climbing over a log implies it is positioned adjacent to or on top of the log. | The premise explicitly states that two blond women are sitting outside, and the other details about passersby are additional context that does not contradict this fact. |
| neutral | A man in a white shirt is walking across the street. | A guy crosses the street to enter the bar. | A man and a guy are synonyms, but walking across the street does not specify the destination is a bar; he could be going anywhere. | Shouting into a microphone is common in concerts or public speaking to project volume, which does not necessarily indicate anger but rather a need for audibility. |
| contradiction | A big outdoor market along a fence. | An empty field. | A market involves many people and stalls, while an empty field lacks such presence, making them mutually exclusive states for the same location. | A computer is used for websites, while a television is used for watching programs; they are distinct devices that cannot perform both functions simultaneously in the same instance. |
