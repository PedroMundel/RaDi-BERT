# Ledger - gaps da replicação do Agrawal (18/11)

Sources: mensagem do Pedro de 18/11 ("duas condições rapidas no note, depois capreolus, depois 16mil pares");
`docs/2026-11-18-gaps-da-argumentacao.md`; `HANDOFF.md` de 18/11 (regras de trabalho: critério antes de rodar,
`training-auditor` e `train-watch` em rodada acima de 10 min).

| # | Item | Source | Done when | Status | Evidence |
|---|---|---|---|---|---|
| 1 | Critério das duas condições rápidas escrito antes de rodar | handoff: critério antes | `grep -n "Gap 2b" docs/2026-11-18-gaps-da-argumentacao.md` acerta, com data anterior ao CSV | done | secao Gap 2b na linha 92, escrita antes do CSV (so existia o de fumaca) |
| 2 | Script `resultados/rte-msmarco/condicoes_baseline.py` com encoder congelado e treino de 1 época | msg | `ruff check` limpo e uma rodada de fumaça termina | done | ruff limpo; fumaca: one_epoch_prop semente 1 -> 0,7548 em 195 s; auditoria: micro-lote 4 |
| 3 | Encoder congelado rodado, 5 sementes | msg | 5 linhas `frozen` em `resultados/rte-msmarco/condicoes-baseline.csv` | done | 5 linhas frozen no CSV, media 0,590 |
| 4 | Poucos passos rodado, 5 sementes por aquecimento | msg | 5 linhas `one_epoch` por aquecimento no mesmo CSV | done | 5 linhas one_epoch_500 (0,635) e 5 one_epoch_prop (0,741) |
| 5 | Leitura das condições rápidas registrada contra o critério | convention: leitura por rodada | seção nova em `resultados/rte-msmarco/leitura-grade.md` | done | secao 'Duas condicoes rapidas do baseline (18/11)' em resultados/rte-msmarco/leitura-grade.md |
| 6 | `Capreolus/bert-base-msmarco` conferido no Hub (existe, vocabulário, cabeça) | CLAUDE.md EXISTS-FIRST | saída do `model_info` e MD5 do `vocab.txt` citados | done | model_info: existe, BertForSequenceClassification; vocab MD5 64800d5d igual ao BERT base; auditoria: missing_keys vazio |
| 7 | Critério do Capreolus escrito antes de rodar | handoff: critério antes | `grep -n "Gap 3" docs/2026-11-18-gaps-da-argumentacao.md` acerta | done | secao Gap 3 na linha 113, escrita antes de lancar |
| 8 | Grade do Capreolus rodada no PC, 2 braços x 5 sementes | msg | 10 linhas em `resultados/rte-capreolus/pc/resultados.csv` | done | 10 linhas em resultados/rte-capreolus/pc/resultados.csv; vigia DONE, saida 0, 64 min |
| 9 | Leitura do Capreolus registrada | convention: leitura por rodada | `resultados/rte-capreolus/leitura-grade.md` existe | done | resultados/rte-capreolus/leitura-grade.md: baseline 0,743; decoder -0,022 (-0,040 a -0,004) |
| 10 | Desenho e critério do decoder com 16 mil pares escritos | msg; handoff: critério antes | seção no plano ou no doc dos gaps, com tempo medido de um treino | done | secao Gap 4 em docs/2026-11-18-gaps-da-argumentacao.md; tempo medido na propria grade: 384 s sem decoder, ~1.905 s com; regra de leitura sem a confirmacao do Pedro |
| 11 | Decoder com 16 mil pares rodado | msg | linhas no CSV da rodada | done | 10 linhas em resultados/esnli-treino-16k/pc/resultados.csv; vigia DONE, saida 0, 3h23 |
| 12 | Leitura dos 16 mil pares registrada | convention: leitura por rodada | arquivo de leitura existe | done | resultados/esnli-treino-16k/leitura-grade.md: ROC +0,003 (-0,004 a +0,010); l_C 3,63 -> 2,01 |
| 13 | `HANDOFF.md` e `CLAUDE.md` com o trabalho de 18/11 | promise (me) | `grep -n "18/11" HANDOFF.md` acerta nas seções novas | done | bloco 'ATUALIZACAO DE 18/11' no HANDOFF.md e bloco '18/11 - GAPS DA REPLICACAO' no CLAUDE.md |
| 14 | claim-check | skill | linha `CLAIM-CHECK` na mensagem final | done | rodado ao fim de cada turno de 18/11, com tabela de vereditos e a linha final em cada mensagem |
| 30 | Graficos da curva de arranque e da acuracia final dos quatro bracos | msg 18/11 | dois PNG em `resultados/esnli-treino-16k/figs/` abertos e conferidos | done | curva-de-arranque.png e acuracia-final-quatro-bracos.png, gerados por graficos_curva.py e enviados ao Pedro |
| 31 | Regra de leitura do gap 4 confirmada pelo Pedro | promise (me) | resposta dele registrada no doc dos gaps | blocked | espera o Pedro; perguntado tres vezes em 18/11, ele respondeu so sobre o calendario |
| 32 | Commit do trabalho desde 10/11 | handoff 18/11 | `git log` com commit novo | blocked | decisao do Pedro (NO-GIT); a suite esta verde desde 18/11 |
| 15 | Pedro confirma a regra de leitura do gap 4, as sementes e o controle de calendario | promise (me) | resposta dele registrada no doc dos gaps | done | Pedro, 18/11: 'faz so o controle de calendario' (5 sementes ficam; regra de leitura do gap 4 sem resposta, segue como proposta, dito no doc) |
| 16 | Criterio do controle de calendario escrito antes de rodar | msg 18/11 | `grep -n "Gap 4b" docs/2026-11-18-gaps-da-argumentacao.md` acerta | done | secao Gap 4b escrita antes do lancamento |
| 17 | Braco de calendario disponivel na tarefa esnli16k | msg 18/11 | fumaca `--tarefa esnli16k --encoder calendario` termina | done | fumaca na CPU terminou (bert_calendar prop seed 1); ruff limpo |
| 18 | Controle de calendario rodado no PC, 5 sementes | msg 18/11 | 5 linhas em `resultados/esnli-treino-16k-calendario/pc/resultados.csv` | done | 5 linhas em resultados/esnli-treino-16k-calendario/pc/resultados.csv; vigia DONE, 24 min; auditoria sem bloqueio |
| 19 | Leitura do controle registrada contra o criterio | convention: leitura por rodada | secao nova em `resultados/esnli-treino-16k/leitura-grade.md` | done | secao 'Controle de calendario (18/11)' em resultados/esnli-treino-16k/leitura-grade.md: calendario +0,007; decoder menos calendario -0,004 (ROC), -0,009 (acuracia) |
| 20 | Calendario nos 4.000 pares do e-SNLI rodado e lido | msg 18/11 | 5 linhas em `resultados/esnli-treino-calendario/pc/resultados.csv` e secao em `resultados/esnli-treino/leitura-grade.md` | done | 5 linhas; calendario +0,004 (-0,002 a +0,011); secao 'Controle de calendario com 4.000 pares' |
| 21 | Estimativa da justificativa embaralhada e avaliacao do dropout entregues | msg 18/11 | resposta ao Pedro com tempos e opiniao; registrado no HANDOFF | done | mensagem de 18/11; bloco 'Avaliado a pedido dele' no HANDOFF.md |
| 22 | Criterio da embaralhada escrito antes de codar | msg 18/11 | secao Gap 5 no doc dos gaps | done | secao Gap 5, com a correcao da checagem gravada antes do lancamento |
| 23 | Braco bert_decoder_shuffled implementado, 3 testes verdes | msg 18/11 | `pytest -q` sem falhas | done | 191 passam, 0 falham; fumaca do braco terminou; troca conferida nos 16.000 pares (0 iguais) |
| 24 | Embaralhada rodada no PC, 5 sementes | msg 18/11 | 5 linhas em `resultados/esnli-treino-16k-embaralhado/pc/resultados.csv` | done | 5 linhas; vigia DONE, 2h50; auditoria sem bloqueio |
| 25 | Leitura da embaralhada registrada contra o criterio | convention | secao no fim de `resultados/esnli-treino-16k/leitura-grade.md` | done | secao 'Justificativa embaralhada (18/11)': real menos embaralhado +0,016 ROC, +0,021 acuracia |
| 26 | Criterio da curva de arranque escrito antes de codar | msg 18/11 | secao Gap 6 no doc dos gaps | done | secao Gap 6 |
| 27 | Curva de arranque rodada, 5 sementes pareadas | msg 18/11 | 55 linhas por braco em `resultados/esnli-treino-16k-curva/{pc,amigo}/curva.csv` | done | sementes 1-3 no PC, 4-5 no PC do amigo; 110 linhas usadas; instrumento: diferenca maxima 0,001 |
| 28 | Leitura da curva registrada contra o criterio | convention | secao no fim de `resultados/esnli-treino-16k/leitura-grade.md` | done | secao 'Curva de arranque (18/11)': principal +4,1 (+3,3 a +5,0) |
| 29 | Maquina do amigo preparada e conferida | msg 18/11 | `ssh amigo` roda `pytest tests` verde | done | 191 passam; MD5 de 9 arquivos e impressao digital dos pares iguais |
