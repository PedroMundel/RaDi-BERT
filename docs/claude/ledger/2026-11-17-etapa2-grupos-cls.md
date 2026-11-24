# Ledger - etapa 2 da seção 11.8: baseline no recorte dos grupos

Sources: mensagens do Pedro de 17/11 (noite); `docs/2026-11-10-plano-teste-fora-da-distribuicao.md`, seção 11.8;
`HANDOFF.md` de 17/11, Next steps 1 e 2.

| # | Item | Source | Done when | Status | Evidence |
|---|---|---|---|---|---|
| 1 | Decisões da rediscussão (sete grupos, dev só se passar, 10 braços, baseline) na seção 11.8 do plano | msg | `grep -n "Rediscussão com o Pedro" docs/2026-11-10-plano-teste-fora-da-distribuicao.md` acha a tabela | done | grep -> linha 645 |
| 2 | `medir_grupos_cls.py` treina "sem nada" e "respostas" e grava o acerto par a par | msg | `--fumaca` termina com "completo" e o CSV tem 2 linhas por aluno | done | fumaça: "completo", 4 linhas, 48 acertos cada |
| 3 | `medir_recorte.py` lê os acertos e dá acurácia no recorte, fora e geral, por semente | plano 11.8 | roda sobre o CSV real e imprime a tabela | done | rodou: recorte 1.249 de 4.000; `recorte-baseline.csv` |
| 4 | `ruff check` limpo nos dois scripts | convention | `uv run --frozen ruff check <os dois>` -> All checks passed | done | All checks passed, depois da última edição |
| 5 | Script do baseline no PC, MD5 igual ao do notebook | handoff | MD5 dos dois lados igual | done | d95620ae... nos dois lados; os outros 6 arquivos usados também iguais |
| 6 | Baseline rodado no PC: 2 braços x 5 sementes | msg | CSV com 20 linhas (10 alunos x 2 conjuntos), copiado para o notebook | done | train-watch DONE em 10 min; `wc -l` 21 (cabeçalho + 20); acurácia geral idêntica à de `juntar-esnli-4000.csv` |
| 7 | Leitura do baseline em `leitura-grade.md`, com legenda | convention | seção nova com a tabela e "Conferido / Não conferido" | done | seção "Baseline no recorte dos sete grupos"; números refeitos por script |
| 10 | Baseline com as sementes 6 a 15 (Pedro: "Mais sementes antes"; o número é do Claude) | msg | CSV com 61 linhas no notebook; leitura atualizada com 15 sementes | done | train-watch DONE em 19 min; `wc -l` 61; subseção "O baseline com 15 sementes" na leitura |
| 8 | Critério dos braços com a cabeça | plano 11.8 | escrito no plano depois do baseline; decisão do Pedro | done | Pedro: "5 e depois 10"; tabela "Critério dos braços com a cabeça de grupos" no plano, seção 11.8 |
| 9 | Código da cabeça de grupos: modelo, perda, otimizador, 8 braços no script | msg ("Pode escrever") | 5 testes novos verdes; suíte 188 verdes e os 3 vermelhos antigos; fumaça de braços com a cabeça termina com "completo" | done | pytest: 188 passed, 3 failed (embaralhado); ruff limpo; fumaça `head_cut` e `head_all_swapped_answers` ok |
| 11 | Viés por rótulo nasce na taxa de cada rótulo (achado A da auditoria de treino) | training-auditor | teste `test_the_label_bias_starts_at_the_logit_of_each_labels_group_rate` verde; brute-test: erro máximo 0,0004 nos alvos reais | done | os dois verdes |
| 12 | Brute-test antes de rodar | msg ("roda o brute test antes tbm") | `docs/claude/brute-test-grupos-cls.md` com a tabela | done | 25 casos, 23 OK, 2 notas, nenhum S1 a S4 novo |
| 13 | Os 5 arquivos no PC com MD5 igual | handoff | MD5 dos dois lados | done | 5 de 5 iguais; GPU 589 MiB antes de lançar |
| 14 | 8 braços x 5 sementes rodados no PC | msg | CSV de acertos com 141 linhas no notebook | done | train-watch DONE em 43 min; `wc -l` 141 |
| 16 | Sementes 6 a 15 de `head_cut` e `head_cut_swapped` (exceção ao critério; Pedro, 18/11: "sim, roda as 10 sementes") | msg | CSV de acertos com 181 linhas no notebook; leitura com 15 sementes na `leitura-grade.md` | done | train-watch DONE em 15 min; `wc -l` 181; subseção "O braço dos sete grupos com 15 sementes" na leitura: não conta pela regra |
| 15 | Leitura pelo critério em `leitura-grade.md` | plano 11.8 | seção nova com a tabela das 8 comparações e o veredito por braço | done | seção "Etapa 2 da seção 11.8"; nenhum candidato; checagem "a cabeça aprendeu" 0,619 -> 0,699 |
