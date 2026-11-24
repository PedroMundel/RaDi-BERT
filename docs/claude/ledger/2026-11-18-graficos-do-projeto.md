# Ledger - gráficos de todo o projeto desde a Semana 3 (18/11)

Sources: mensagem do Pedro de 18/11 ("gera graficos pra tudo do projeto, desde a Semana 3"); inventário dos dados em
disco feito por agente em 18/11 (caminhos, colunas e linhas de cada CSV e JSON); skill `dataviz` (forma, cores
validadas, conferir a figura renderizada).

| # | Item | Source | Done when | Status | Evidence |
|---|---|---|---|---|---|
| 1 | Inventário dos dados em disco por etapa | msg | lista de arquivos com colunas e linhas por etapa | done | relatório do agente de 18/11: 9 etapas, CSV e JSON com colunas; tabelas só em `.md` listadas |
| 2 | Script único que gera todas as figuras | msg | `ruff check` limpo e a rodada imprime `ok` para cada figura | done | `resultados/figuras/graficos_projeto.py`: ruff limpo, 22 linhas `ok` |
| 3 | Screening (Semanas 3 a 5): figuras 01 a 04 | msg | 4 PNG em `resultados/figuras/` | done | 01 funil, 02 vereditos da F2, 03 classificador, 04 lista v2 |
| 4 | Geração das justificativas (outubro): figuras 05 e 06 | msg | 2 PNG | done | 05 piloto do prompt, 06 lote 35B |
| 5 | Replicação do Agrawal e controles: figuras 07 a 11 | msg | 5 PNG | done | 07 decoder em todas as grades, 08 baseline do artigo, 09 perda por tipo de palavra, 10 embaralhada, 11 curva de arranque |
| 6 | Marcas de atenção e destaque: figuras 12 a 16 | msg | 5 PNG | done | 12 nota, 13 atenção por camada, 14 destaque, 15 marca por camada, 16 intervenção |
| 7 | Destilação: figuras 17 a 19 | msg | 3 PNG | done | 17 respostas, 18 atenção contra respostas, 19 juntar |
| 8 | Palavras novas e cabeça de grupos: figuras 20 a 22 | msg | 3 PNG | done | 20 palavras e rótulo, 21 cabeça de grupos, 22 pares difíceis |
| 9 | Cada figura aberta e conferida | skill dataviz | folhas de contato lidas; correções reaplicadas e relidas | done | 6 folhas lidas; legendas de 5 figuras movidas para fora da área de dados, rótulos da 13 e eixo da 21 corrigidos; 07, 13, 21 e 22 relidas |
| 10 | Índice com fonte e como ler de cada figura | promise (me) | `resultados/figuras/INDICE.md` com uma linha por figura | done | 22 linhas em 6 seções |
| 11 | Avaliação humana de 29/10 em gráfico | msg ("tudo") | figura com os votos | blocked | espera o Pedro: sem resultado em arquivo: `leitura-50-gabarito.csv` só tem os votos do artigo de Wiegreffe; dito ao Pedro em 18/11 |
| 12 | Semanas 4 e 5 (seleção e leituras) em gráfico | msg ("tudo") | figura | blocked | espera o Pedro: só há listas de obras, sem medida além da figura 04; dito ao Pedro em 18/11 |
| 13 | Custo da geração por API (13/10) em gráfico | msg ("tudo") | figura | blocked | espera o Pedro: os números só existem em tabela de `.md`, três linhas; ficou de fora e foi dito ao Pedro em 18/11 |
| 14 | claim-check | skill | linha `CLAIM-CHECK` na mensagem final | done | rodado ao fim do turno de 18/11 |
| 15 | Mapa dos clusters do HDBSCAN (figura 24) | msg 18/11 ("um pros clusters do hdbscan") | PNG aberto e conferido; 2.323 palavras, grupos lidos do CSV de 17/11 | done | `24-grupos-hdbscan-mapa.png`; posições em `resultados/rte-pequenos/grupos-palavras-novas-mapa.csv`, geradas por `mapa_grupos_palavras.py` (2.323 palavras, 29 grupos, 1.069 sem grupo) |
| 16 | Composição de cada cluster (figura 23) | promise (me) | PNG aberto e conferido; 30 linhas | done | `23-grupos-hdbscan-composicao.png`, de `grupos-palavras-novas.csv` |
| 17 | Índice com as duas figuras novas | convention | `grep -c` de linhas de figura no `INDICE.md` dá 24 | done | 24 linhas |
| 18 | Diagrama do método (figura 25) | msg 18/11 ("pode criar todos") | PNG aberto e conferido | done | `25-artigo-metodo.png`; seta do LLM corrigida e relida |
| 19 | Esquema dos quatro braços (figura 26) | msg 18/11 | PNG aberto e conferido; passos lidos do `resultados.csv` | done | `26-artigo-bracos.png`; rótulo sobreposto corrigido e relido |
| 20 | Cosseno dos gradientes ao longo do treino (figura 27) | msg 18/11 | PNG aberto e conferido | done | `27-artigo-cosseno-dos-gradientes.png`; título trocado depois de ver o pico com 16.000 pares |
| 21 | Empurrão do decoder por tipo de palavra (figura 28) | msg 18/11 | PNG aberto e conferido | done | `28-artigo-empurrao-por-tipo-de-palavra.png` |
| 22 | Tabela de resultados e de diferenças pareadas | msg 18/11 | `resultados/figuras/tabelas-artigo.md`, seções 1 a 3 | done | números conferidos contra as leituras de 18/11 (83,7; 82,8; 80,7; -0,9; -3,0; +2,1) |
| 23 | Tabela de exemplos com a justificativa trocada | msg 18/11 | `tabelas-artigo.md`, seção 4, um par por rótulo | done | gerada com `shuffle_within_label(pairs, 0)`, a mesma troca do treino |
| 24 | Curva de arranque do braço embaralhado, sementes 1 a 3 (PC) | msg 18/11 | 33 linhas `bert_decoder_shuffled` em `esnli-treino-16k-curva/pc/curva.csv` | done | 33 linhas bert_decoder_shuffled (sementes 1 a 3) em pc/curva.csv; vigia DONE, 1h38; lida no fim de resultados/esnli-treino-16k/leitura-grade.md |
| 25 | Curva de arranque do braço embaralhado, sementes 4 e 5 (no PC; Pedro, 18/11: "Rodar no meu PC") | msg 18/11 | 22 linhas `bert_decoder_shuffled` das sementes 4 e 5 em `pc/curva.csv` | todo | a GPU do amigo estava em uso por ele; roda no PC quando as sementes 1 a 3 terminarem; regra de leitura ajustada antes no Gap 6b |
| 26 | Figura 29: as três curvas | msg 18/11 | PNG aberto e conferido | done | 29-artigo-curva-tres-bracos.png com 3 sementes do braço embaralhado, aberta e conferida; o subtítulo diz quantas sementes cada braço tem |
| 27 | Qualidade das justificativas em gráfico | msg 18/11 ("todos") | figura | blocked | sem dado: as respostas do formulário de 29/10 não estão em disco; espera o Pedro |
| 28 | Mais sementes ou outra tarefa | msg 18/11 ("todos") | rodadas novas | blocked | não é gráfico, é decisão de GPU (cerca de 4 h para mais 5 sementes dos quatro braços); espera o Pedro |
