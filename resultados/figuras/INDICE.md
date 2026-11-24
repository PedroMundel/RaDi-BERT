# Figuras do projeto, da Semana 3 a 18/11

Geradas por `graficos_projeto.py` em 18/11/2026, a pedido do Pedro. Cada figura sai só de números lidos de arquivo; a coluna da fonte diz qual. Títulos que afirmam uma conclusão são leitura do Claude sobre os números da figura.

## Screening (Semanas 3 a 5)

| Figura | Fonte dos números | Como ler |
|---|---|---|
| `01-screening-funil.png`: Do levantamento à árvore de citação | docs/screening/fase1/2026-09-22-floresta-obras.csv (colunas camada_A, para_camada_C, camada_C_F1) | Cada barra é uma contagem de obras. À esquerda, quantas sobram a cada camada; à direita, o que a árvore de citação fez com as que chegaram à camada C. |
| `02-screening-f2-vereditos.png`: F2: vereditos das 962 obras lidas | docs/screening/fase1/F2/vereditos.csv (coluna veredito) | Contagem de obras por veredito. 'Relevante' são 55 de 962. |
| `03-screening-classificador.png`: Classificador da triagem: recuperação nos 25% do topo | docs/screening/fase1/C1-diagnostico/resultados.json (chave E1_P1, campo rec@25%) | Cada barra é um jeito de ordenar a lista. A linha tracejada é o que se acha lendo 25% ao acaso. |
| `04-screening-lista-v2.png`: As 56 obras da lista v2, por bloco e ano | docs/screening/fase1/lista-rapida/lista-v2.csv (colunas bloco, ano) | Cada ponto é uma obra, na linha do seu bloco e na posição do seu ano; o número entre parênteses é o total do bloco. A posição vertical dentro da linha é só para os pontos não se cobrirem. |

## Geração das justificativas (outubro)

| Figura | Fonte dos números | Como ler |
|---|---|---|
| `05-geracao-piloto-comprimento.png`: Piloto do prompt: comprimento da justificativa por variante | resultados/piloto-qwen/resultados*.csv (coluna qwen; Explanation_1 para a humana) | Cada ponto pequeno é uma justificativa, o grande é a média da variante. Conta palavras separadas por espaço. |
| `06-geracao-lote-35B.png`: O lote de 16.000 justificativas | resultados/lote-35B/run/train.log (linhas 'N pares no total'), marcas.csv (coluna eco) e racionalizacoes-F-35B.csv (gold_label) | À esquerda, pares gerados ao longo das horas. À direita, a parcela das justificativas de cada rótulo que a regra de eco marcou. No arquivo só há marcas em entailment; não foi conferido na regra se isso é por desenho. |

## Replicação do Agrawal e controles (9 a 18/11)

| Figura | Fonte dos números | Como ler |
|---|---|---|
| `07-decoder-todas-as-grades.png`: Decoder menos sem decoder, em todas as grades | resultados/{rte-treino,rte-msmarco,rte-capreolus,rte-t5enc,rte-small,rte-tiny,esnli-treino,esnli-treino-16k,rte-calendario,esnli-treino-calendario,esnli-treino-16k-calendario}/pc/resultados.csv (coluna roc_auc) | Cada linha é uma condição de treino. O ponto é a diferença média entre sementes e a barra o intervalo de 95%; à direita da linha vertical o decoder ajuda. n é o número de sementes pareadas. No RTE o T5 como encoder tem causa própria (desequilíbrio de gradiente). |
| `08-baseline-do-artigo.png`: Condições do baseline MS-MARCO no RTE | resultados/rte-msmarco/condicoes-baseline.csv, resultados/rte-msmarco/pc/resultados.csv e resultados/rte-capreolus/pc/resultados.csv (braço bert); linhas tracejadas: Tabela 2 de Agrawal, Ahemad & Sembium (2025), conferida no PDF | Cada ponto pequeno é uma semente e o grande a média. As linhas tracejadas são os dois números que o artigo relata para o RTE. |
| `09-decoder-perda-por-tipo-de-palavra.png`: Perda do decoder por tipo de palavra, 4 mil e 16 mil pares | resultados/esnli-treino/pc/gradientes.csv e resultados/esnli-treino-16k/pc/gradientes.csv (colunas l_C, l_N, l_S, l_F) | Cada linha é a perda do decoder num tipo de palavra-alvo ao longo do treino; menor é melhor. O número no fim de cada linha é o valor no último passo. As sondas das duas grades são 63 pares sorteados do treino de cada uma, não os mesmos pares. |
| `10-justificativa-embaralhada.png`: Acurácia final dos quatro braços nos 16 mil pares | resultados/{esnli-treino-16k,esnli-treino-16k-calendario,esnli-treino-16k-embaralhado}/pc/resultados.csv (coluna accuracy) | Cada ponto pequeno é uma semente e o grande a média do braço. |
| `11-curva-de-arranque.png`: Curva de arranque: com decoder contra sem decoder | resultados/esnli-treino-16k-curva/pc/curva.csv (sementes 1 a 3) e amigo/curva.csv (sementes 4 e 5) | Linha grossa: média de 5 sementes; linhas finas: cada semente. O eixo horizontal conta os passos desde o passo 1.200, em escala logarítmica. A versão com o painel da diferença está em resultados/esnli-treino-16k/figs/curva-de-arranque.png. |

## Marcas de atenção e destaque (10 a 16/11)

| Figura | Fonte dos números | Como ler |
|---|---|---|
| `12-marcas-nota.png`: Marcas de atenção: ROC-AUC por braço | resultados/rte-marcas/pc/resultados.csv, rte-marcas-small/pc/resultados.csv (roc_auc) e rte-marcas-small-fora/pc/resultados.csv (fora_roc_auc) | Três painéis, um por condição. Em cada um, ponto pequeno é uma semente e ponto grande a média do braço. Os eixos horizontais não são os mesmos entre os painéis. |
| `13-marcas-atencao-por-camada.png`: Atenção do [CLS] nas palavras marcadas, por camada | resultados/rte-pequenos/atencao.csv (split held, coluna mass_real; linha tracejada: coluna uniform) | Cada linha é um modelo; o eixo vertical é quanto da atenção do [CLS] cai nas palavras que a justificativa copia. A marca foi cobrada na camada 4. |
| `14-destaque.png`: Destaque: quem aponta melhor as palavras copiadas pelo LLM | resultados/rte-pequenos/destaque-2000-cabeca.csv (coluna ap) | Cada linha é um jeito de dar nota às palavras do par; quanto mais à direita, melhor ele ordena as palavras que a justificativa copia. As regras e o modelo sem treino têm um valor só. |
| `15-marcas-por-camada.png`: Marca real cobrada em cada combinação de camadas | resultados/rte-pequenos/camadas-esnli-4000.csv (kind real menos kind none, coluna dev_accuracy) | Cada linha é uma combinação de camadas onde a marca foi cobrada; o ponto é a diferença para o modelo sem marcas, pareada por semente, com o intervalo de 95%. |
| `16-intervencao-por-camada.png`: Tapar a atenção do [CLS] por camada | resultados/rte-pequenos/intervencao-2000.csv (arm marks_none, operation block, rows cls, coluna flip) | Cada linha é um conjunto de palavras cuja atenção foi tapada na linha do [CLS]; o eixo vertical é a parcela dos 470 pares em que a decisão do modelo muda. Média das sementes. |

## Destilação (16 a 18/11)

| Figura | Fonte dos números | Como ler |
|---|---|---|
| `17-destilacao-respostas.png`: Destilação das respostas do professor | resultados/rte-pequenos/respostas-esnli-4000.csv (coluna choice_accuracy, cada braço menos none) | Cada linha é um jeito de usar o professor; o ponto é o ganho sobre o aluno sem professor, pareado por semente, com intervalo de 95%. Os controles mostram se o ganho vem do que o professor diz de cada par. |
| `18-destilacao-atencao.png`: Destilar a atenção contra destilar as respostas | resultados/rte-pequenos/destilacao-esnli-fora-4000.csv (coluna dev_accuracy, cada braço menos none) | Cada linha é o que o aluno imita do professor; ganho sobre o aluno sem professor, pareado por semente. |
| `19-destilacao-juntar.png`: Juntar o interior do professor com as respostas | resultados/rte-pequenos/juntar-esnli-4000.csv (coluna choice_accuracy, cada braço menos answers) | Cada linha é um braço comparado com o aluno que só imita as respostas; à direita da linha vertical o braço é melhor. n é o número de sementes pareadas (a sequência tem 15, os demais 5). |

## Palavras novas e cabeça de grupos (17 e 18/11)

| Figura | Fonte dos números | Como ler |
|---|---|---|
| `20-palavras-novas-e-rotulo.png`: Quanto cada conjunto de palavras diz sobre o rótulo | resultados/rte-pequenos/palavras-novas-esnli-4000.csv (coluna accuracy) | Cada barra é a acurácia de prever o rótulo vendo só aquele conjunto de palavras. O acaso é a última barra. |
| `21-cabeca-de-grupos.png`: Cabeça de grupos no [CLS], no recorte | resultados/rte-pequenos/recorte-acuracias.csv (coluna cut; braços sem professor menos none, com professor menos answers) | Cada linha é um braço menos a sua referência, pareado por semente; as linhas tracejadas são o critério de 0,64 ponto escrito antes. n é o número de sementes (15 nos dois primeiros braços de sete grupos). |
| `22-pares-dificeis.png`: Pares difíceis: conjunto de escolha contra o dev | resultados/rte-pequenos/grupos-cls-acertos-esnli-4000.csv (acertos par a par; mesma conta de medir_dificeis.py) | Dificuldade de um par = quantos dos 15 alunos do braço 'respostas' o acertam naquele conjunto. Cada linha é a diferença do braço de sete grupos para o aluno sem nada, pareada por semente. |
| `23-grupos-hdbscan-composicao.png`: Os grupos de palavras novas, um a um | resultados/rte-pequenos/grupos-palavras-novas.csv (colunas words, pairs_with_it, share_*, top_words) | Cada linha é um grupo, com as cinco palavras mais frequentes dele; a barra mostra a parcela dos pares com palavra do grupo em cada rótulo, e à direita vão o número de palavras e de pares. [alvo] marca os sete grupos escolhidos pelo Pedro em 17/11; [argumentar] é o único grupo de palavras de argumentar. Um par pode ter palavra de vários grupos. |
| `24-grupos-hdbscan-mapa.png`: Mapa das palavras novas e dos grupos | resultados/rte-pequenos/grupos-palavras-novas-mapa.csv (posições, de mapa_grupos_palavras.py) e grupos-palavras-novas-palavras.csv (o grupo de cada palavra, salvo em 17/11) | Cada ponto é uma palavra nova. O grupo de cada palavra é o que o HDBSCAN deu em 17/11, sobre uma projeção de 10 dimensões; a posição no mapa vem de uma segunda projeção, de 2 dimensões, feita só para o desenho, então a distância no mapa não é a que o agrupamento viu. Cinza claro: palavras sem grupo (1.069). Os eixos não têm unidade. |

## Figuras que faltavam para o artigo (18/11)

| Figura | Fonte dos números | Como ler |
|---|---|---|
| `25-artigo-metodo.png`: Diagrama do método | Sem dado: esquema do modelo de src/radibert/rte_modelo.py (RationaleBert) e do peso AUX_WEIGHT = 0,1 de src/radibert/rte_treino.py | Azul: o que classifica e fica na inferência. Laranja tracejado: o decoder auxiliar, que gera a justificativa a partir dos estados do encoder e é descartado depois do treino. |
| `26-artigo-bracos.png`: Os quatro braços e o calendário de cada um | resultados/esnli-treino-16k/pc/resultados.csv (colunas total, phase_a, phase_b) e as fases de src/radibert/rte_treino.py (training_loss, run_phase_a, braço bert_calendar) | Cada braço tem duas faixas: em cima, os passos em que a classificação treina; embaixo, os passos em que gerar a justificativa treina. Nos dois braços com decoder o peso da geração é 0,1 depois do passo 1.200. |
| `27-artigo-cosseno-dos-gradientes.png`: Cosseno entre o gradiente do decoder e o da classificação | resultados/{rte-treino,esnli-treino,esnli-treino-16k,esnli-treino-16k-embaralhado}/pc/gradientes.csv (coluna cos_c_a; no RTE, só o aquecimento proporcional) | Linha grossa: média das 5 sementes; linhas finas: cada semente. Zero quer dizer que gerar a justificativa empurra o encoder numa direção que nem ajuda nem atrapalha a classificação. A linha tracejada é o fim da fase em que só o decoder treina o encoder. Com 16.000 pares a média sobe a cerca de 0,15 logo depois que a classificação começa e volta a zero. O eixo vai de -0,35 a 0,35: picos de sementes isoladas saem do quadro (no RTE uma chega a -0,73), sobretudo antes da linha tracejada, quando o gradiente de classificação é medido num modelo que ainda não classifica. |
| `28-artigo-empurrao-por-tipo-de-palavra.png`: De que palavras vem o empurrão do decoder | resultados/{rte-treino,esnli-treino,esnli-treino-16k,esnli-treino-16k-embaralhado}/pc/gradientes.csv (colunas frac_tokens_* e share_*, fase C; no RTE, só o aquecimento proporcional) | Para cada condição, a barra de cima é quanto de cada tipo de palavra há no alvo do decoder, e a de baixo é quanto do gradiente do decoder no encoder vem de cada tipo (medido na sonda). No braço de outro par quase nada do alvo está no par, então 'copiada' some e as palavras passam a contar como 'nova'. |
| `29-artigo-curva-tres-bracos.png`: Curva de arranque: calendário, decoder e decoder embaralhado | resultados/esnli-treino-16k-curva/pc/curva.csv (sementes 1 a 3) e amigo/curva.csv (sementes 4 e 5) | Linha grossa: média das sementes disponíveis de cada braço; linhas finas: cada semente. O número à esquerda é a acurácia no primeiro passo medido (25 passos de classificação). |
