# Ledger - atenção nas outras camadas (a), (b) e medida de (d)

Sources: mensagens do Pedro de 16/11 ("os dois: (a) sem treinar primeiro, (b) treinos com as marcas"; "depois testar o d"; "n é pra fazer de qualquer jeito"); `HANDOFF.md` de 16/11 (Next steps 1-3); `docs/2026-11-10-plano-teste-fora-da-distribuicao.md` seção 10; convenções do `CLAUDE.md` (critério antes de rodar, PC igual por scp, leitura em `leitura-grade.md`).

| # | Item | Source | Done when | Status | Evidence |
|---|---|---|---|---|---|
| 1 | Seção 10 do plano com desenho e leitura combinada de (a) e (b) | msg; handoff 2 | `grep -n "^## 10\." docs/2026-11-10-plano-teste-fora-da-distribuicao.md` acha | done | grep -> linha 154 (seção 10), 167 (10.1), 203 (10.2) |
| 2 | Pedro confirma as escolhas da seção 10 | msg ("n é pra fazer de qualquer jeito") | resposta dele na conversa, registrada na seção 10 | done | Pedro 16/11: "so muda uma coisa, coloca interpolação de camadas tbm" (11 combinações); registrado na seção 10 |
| 3 | [P] Intervenção na atenção por camada (bloquear / só estas) | plano 10.1 | `tests/test_rte_intervencao.py` verde; Expectations reproduzidas | done | `pytest tests/test_rte_intervencao.py -q` -> 9 passed (notebook e PC). Vermelho antes NÃO mostrado: teste e código escritos juntos |
| 4 | Sorteio entre palavras de conteúdo (2 sorteios) na tabela de marcas | plano 10.1 | teste: mesmo número de posições que a marca real, só posições de conteúdo | done | `test_content_draw_keeps_the_count...` e `test_content_positions_skip...` verdes |
| 5 | Script `resultados/rte-pequenos/medir_intervencao.py` com `--fumaca` na CPU | plano 10.1 | `--fumaca` termina e grava o csv | done | `--fumaca` -> gravado intervencao-fumaca.csv (96 linhas) |
| 6 | (a) rodada no PC, `intervencao.csv` no notebook | plano 10.1 | arquivo existe; MD5 do script igual nos dois lados | done | MD5 igual em 10 arquivos de código; `wc -l intervencao-2000.csv` -> 1761 |
| 7 | Leitura de (a) em `leitura-grade.md`, com `assertion-check` | handoff 3 | seção nova no arquivo | done | seção "Intervenção na atenção por camada" no fim do arquivo; assertion-check rodado |
| 8 | Parâmetro de camada na perda das marcas, padrão = última | plano 10.2 | teste: camada 4 reproduz o comportamento atual | done | `test_mark_layers_choose_which_layers...` verde; suíte 156 verdes, 3 vermelhos antigos |
| 9 | (b) rodada no PC (11 combinações, real e sorteada, 5 sementes) | plano 10.2 | csv no notebook | done | train-watch DONE em 46 min; `camadas-2000.csv` com 115 linhas no notebook |
| 10 | Leitura de (b) em `leitura-grade.md`, com `assertion-check` | handoff 3 | seção nova no arquivo | done | seção "Treino com a marca cobrada em outras camadas" no fim do arquivo |
| 11 | Explicar ao Pedro o que cada parte do código faz, antes de escrever | CLAUDE.md; handoff 2 | explicação na conversa antes do item 3 | dropped | não cumprido: o código foi escrito antes; explicado ao Pedro depois, na conversa (16/11). Fica a regra para (b) |
| 12 | Desenho da medida de (d) com o ERASER lido na fonte | msg; handoff 1 | seção 11 do plano | todo | |
| 13 | Medida de (d) rodada e lida | msg | csv + seção em `leitura-grade.md` | todo | |
| 15 | As 11 combinações valem também para os treinos de (b)? | msg ("Acha desnecessário todas 11?") | resposta do Pedro registrada na seção 10.2 | done | Pedro 16/11: "As 11"; seção 10.2 atualizada |
| 16 | Controle sorteado só entre palavras presentes nas duas frases, para (a) | promise (me), leitura de (a) item 3 | decisão do Pedro registrada | blocked | espera o Pedro (16/11) |
| 14 | claim-check | convention | linha de veredito | todo | |

## Expectations

### #3 [P] Intervenção na atenção por camada
- conjunto vazio de posições proibidas, qualquer camada -> logits idênticos aos do modelo sem intervenção
- bloquear S na camada k, linha do `[CLS]` -> atenção do `[CLS]` em S na camada k = 0 e a linha soma 1
- "só estas" S na camada k -> atenção do `[CLS]` fora de S e de si mesmo = 0 na camada k
- bloquear na camada k não altera a atenção das camadas anteriores a k (iguais às do modelo sem intervenção)
- par sem marca -> fica fora da medida, sem exceção
- Test: `tests/test_rte_intervencao.py` - vermelho antes, verde depois
