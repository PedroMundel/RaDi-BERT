# Modo autônomo — 10/11/2026, madrugada (Pedro dormindo)

Pedido do Pedro (09/11, ~00:55): "rodar a análise da grade, colocar o controle — bert cru, baseline, a gente não
testou ele [...] — para rodar, depois, se não tiver acordado ainda, roda o controle embaralhado. Qualquer erro pode
corrigir pra manter o treino rodando, só salva no arquivo de autonomia". Esclarecimento dele logo depois: "o baseline
eu pedi pq não dá pra comparar diretamente com o dele" (o do Agrawal é um BERT treinado no MS MARCO).

## Fila

1. Análise da grade do RTE (20 treinos: BERT sozinho × BERT + decoder, aquecimento 500 e prop, sementes 1–5).
2. Controle embaralhado: código e testes.
3. Controle embaralhado: rodar no PC depois que a grade terminar.
4. Análise final com o controle.
5. Relatório final neste arquivo.

## Decisões

- **00:58 — O "BERT cru" já é o braço `bert` da grade.** É o `google-bert/bert-base-uncased` só pré-treinado,
  ajustado no RTE com L_cls, mesmos hiperparâmetros: exatamente o baseline que permite comparar o método sem o
  problema do MS MARCO do Agrawal. Os 10 treinos dele já rodaram. Não criei braço novo para isso.
- **00:58 — Braço com o BERT do MS MARCO: não roda agora.** O Pedro disse "não imediatamente". Fica em Próximos passos.
- **01:05 — Análise: script `resultados/rte-treino/analise_grade.py`, relatório `analise-grade.md`.** Comparação
  pareada por semente (mesma semente = mesma ordem de lotes e mesma cabeça inicial nos braços), intervalo t com n − 1.
  Sem gráficos: o projeto não tem matplotlib e não vou acrescentar dependência sem você; as medidas vão em tabela por
  passo. Os CSVs do PC são copiados por `scp` para `resultados/rte-treino/pc/` (cópia; o PC continua sendo a fonte).
- **01:05 — Controle embaralhado = justificativa de OUTRO par do MESMO rótulo**, permutação fixa (semente 0), nenhum
  par com a própria. Escolhi "mesmo rótulo" e não "qualquer par" porque é o controle mais afiado: mantém tudo o que
  a justificativa carrega sobre o rótulo (as palavras S, "not/never" etc.) e tira só o conteúdo específico do par.
  Se o embaralhado empatar com o decoder normal, o ganho (se houver) vem do rótulo escrito, não do porquê. O
  embaralhado em qualquer rótulo mediria outra coisa (justificativa que contradiz o rótulo = ruído) e fica como
  próximo passo. Mesmas fases, aquecimentos e sementes do `bert_decoder`; braço `bert_decoder_shuffled`.
- **Regras que seguem valendo:** sem commit/push (hard stop do modo autônomo): o código novo chega ao PC por `scp` e as
  rodadas ficam marcadas `-dirty` na coluna `code`; o diff exato fica salvo em `resultados/rte-treino/run/` para
  rastrear. Nada apagado.

---

# Modo autônomo — 10/11/2026, 01:50 (segunda rodada, Pedro dormindo)

Pedido do Pedro (10/11, ~01:50): "enquanto eu to dormindo, pode rodar a analise da grade, depois roda o mesmo treino
com o T5 de encoder. Se ainda n tiver acordado, roda o e-SNLI." A fila da rodada anterior (controle embaralhado) não
foi retomada: ficou como decisão dele (passo 3 do HANDOFF de 01:45, arquivado em `docs/handoffs/2026-11-10-0145.md`).

## Fila

1. Análise da grade do RTE quando os 20 treinos terminarem (vigia rearmado às 01:50).
2. Treino com o T5 como encoder: código e testes.
3. Treino com o T5 como encoder: rodar no PC depois da grade.
4. e-SNLI: código (3 classes) e testes.
5. e-SNLI: rodar no PC depois do T5.
6. Relatório final neste arquivo e HANDOFF.

## Decisões

- **01:50 — Leitura de "o mesmo treino com o T5 de encoder":** trocar o BERT pelo encoder do T5 nos dois braços
  (`t5enc` = encoder do T5 + cabeça, só L_cls; `t5enc_decoder` = encoder + decoder do MESMO T5, fases A/B/C iguais).
  Rejeitado: só o "teste da ponte" (T5 inteiro gerando a justificativa, sem classificar). Escolhi a leitura maior
  porque ela responde as duas perguntas: no braço com decoder, o decoder lê o próprio encoder, então a L_aux dele é
  o teste da ponte (fica abaixo de ~3,1 por token = o gargalo era ler o BERT); e a comparação pareada
  `t5enc` × `t5enc_decoder` repete a pergunta do Agrawal sem a ponte.
- **01:55 — Checkpoint: `google/t5-v1_1-base`, NÃO o `google-t5/t5-base`.** Conferido no cartão do HF: o t5-base
  original foi pré-treinado numa mistura com tarefas supervisionadas, **RTE e MNLI incluídos** ("multi-task mixture of
  unsupervised and supervised tasks", lista com RTE). Como encoder classificador ele já viu o treino do RTE com
  rótulo: bate no Rejected "encoder já ajustado para NLI como ponto de partida". O v1.1 foi "pre-trained on C4 only
  without mixing in the downstream tasks" (cartão do HF). Custo: o decoder do braço novo não é o mesmo do
  `bert_decoder` (v1.1 tem GEGLU, sem pesos atados), então a L_aux dos dois compara decoders T5 base de checkpoints
  diferentes; declarado na análise. **Achado colateral para o gate:** o decoder do `bert_decoder` (t5-base, como no
  Agrawal) também viu RTE/MNLI no pré-treino; como ele só escreve a justificativa e é descartado, não contamina a
  avaliação do BERT, mas vale a nota.
- **01:55 — Hiperparâmetros iguais aos da grade** (taxa 5e-5, AdamW, lote 32, 8 épocas, fases A/B/C, peso 0,1).
  O T5 costuma ser ajustado com taxa maior (1e-4 a 3e-4); não troquei porque o pedido é "o mesmo treino". Se o
  `t5enc` ficar muito abaixo do BERT, essa é a primeira suspeita.
- **01:55 — Só o aquecimento `prop`, 5 sementes, 2 braços = 10 treinos.** O `500` já se mostrou artefato da cópia
  (−0,025 no BERT) e cortar metade da grade é o que deixa o e-SNLI caber antes de você acordar.
- **01:55 — Como o T5 classifica:** média dos vetores dos tokens reais (sem padding) do último estado do encoder,
  na mesma cabeça (dropout 0,1 + linear). O T5 não tem [CLS]; a média é o pooling do Sentence-T5. Entrada = par pelo
  tokenizador do T5 (`premissa </s> hipótese </s>`), sem prefixo de tarefa.
- **01:55 — Embedding compartilhado (`shared`) do T5 no braço com decoder:** é a entrada do encoder e do decoder ao
  mesmo tempo. Fica no grupo do ENCODER (aquece pela fase B, sem decaimento de peso). Consequência: na fase A o
  encoder está congelado, mas o `shared` recebe gradiente pelo lado do decoder, então a entrada do encoder muda um
  pouco nos 39 passos. No `bert_decoder` isso não existe (o BERT tem embedding próprio). Declarado; não corrigi
  porque desatar o embedding mudaria o T5.
- **Regras que seguem valendo:** sem commit/push; o código novo vai ao PC por `scp` para o `D:\RaDi-BERT` (rodadas
  marcadas `-dirty`), resultados em pasta própria (`resultados/rte-t5enc/`), nada apagado. O download do
  `google/t5-v1_1-base` (~1 GB, HF, público) acontece no PC pela própria `from_pretrained`, como foi com o BERT e o
  t5-base.
- **02:00 — Tokenizador do T5 v1.1:** o do `google/t5-v1_1-base` não carrega no transformers 5 (o repo só tem
  `spiece.model` e o conversor pede `tiktoken`). O `spiece.model` dos dois checkpoints é o MESMO arquivo (mesmo oid
  git no HF, conferido via API), então os braços T5 tokenizam com o do `google-t5/t5-base`. Não instalei pacote novo.
- **02:05 — Pesos do v1.1 conferidos depois de carregar:** `lm_head` NÃO atado ao `shared` (o transformers vê os dois
  diferentes no checkpoint e não ata) e `scale_decoder_outputs = False` (o t5-base tem `True`). O `config` mostra
  `tie_word_embeddings = True`, mas é herança do código, não o que roda. Encoder lê o `shared` (atado), como deve.
- **02:05 — Fumaça na CPU:** e-SNLI com o BERT mínimo passou (os dois braços, L_cls inicial 1,2 ≈ ln 3, tabela de
  expressões com 202 linhas e 3 colunas de rótulo). T5: o braço `t5enc` passou na CPU (115 s); o `t5enc_decoder`
  estourou a RAM do notebook (7,8 GB, T5 base inteiro + AdamW + gradientes da medida). Não dá para fumaçar o braço
  completo aqui; ele fica coberto pelos testes com T5 mínimo (encoder compartilhado, grupos sem duplicata, fase A,
  L_aux chega ao encoder) e pelo `memory_check` que a grade roda na GPU antes do primeiro treino.
- **02:10 — e-SNLI:** 4.000 pares sorteados (semente 0) das 16.000 PRIMEIRAS linhas do lote 35B. O CSV do PC tem 200
  linhas a mais (anexadas em 09/11, `progresso.txt`: 16.200), por isso o corte por linha; a impressão MD5 do treino e
  do dev bate nas duas máquinas (treino 96399d30…, dev 3c434a65…). Avaliação no **dev** do e-SNLI (9.842 pares):
  o test não está no disco e nada é ajustado no dev, lido uma vez por treino. Sem filtrar os 7,8% marcados como eco:
  o Agrawal não filtra e os dois braços veem os mesmos pares. Só aquecimento `prop` (1.000 passos, 100 de
  aquecimento); o 500 seria meio treino subindo.
- **02:10 — A grade do BERT está ~3× mais lenta desde a semente 5 do `500`:** VRAM transbordando de novo (7,6 de
  8,1 GB usados, 654 MB do treino em memória compartilhada; no estado bom eram ~300 MB). Há apps abertos no PC
  segurando VRAM (Claude, WhatsApp, Edge). Não fechei apps seus. Acrescentei `--micro` (pares por passada; mesmo
  gradiente, I16 testado) e vou relançar o RESTO da grade com micro-lote 8 quando o treino em curso
  (`bert_decoder prop` semente 1) gravar a linha dele: `troca.sh` espera a 16ª linha no `resultados.csv` do PC, para
  o Python do PC (o 17º treino terá ~1 min) e lança `noite.sh` = resto da grade -> grade T5 -> e-SNLI, em sequência.
  Os treinos relançados ficam com `code` = `59278b8-dirty`; o micro-lote não entra no CSV (mudaria as colunas e o
  `append_csv` recusaria), fica no log e aqui.
- **02:10 — Código no PC por `scp`** para `D:\RaDi-BERT\src` e `tests` (cópia de trabalho do PC agora suja nesses 5
  arquivos + `esnli_dados.py` novo); 129 testes passam lá também. `google/t5-v1_1-base` baixado no PC (~1 GB).
- **02:10 — `.gitignore`:** `resultados/rte-treino/fumaca/` virou `resultados/**/fumaca/` (as pastas novas também
  recebem fumaça).
- **02:20 — Auditorias (code-auditor, code-reducer) antes de lançar.** Nada grave. Duas correções aplicadas no braço
  `t5enc_decoder`, as duas por causa do `shared` (embedding que o encoder lê E com que o decoder embute os tokens da
  justificativa): (1) as medidas de gradiente deixam o `shared` de fora nesse braço (`measured_params`), senão o
  g_a misturaria o decoder aprendendo os próprios embeddings com o empurrão no encoder; no BERT nada muda. Custo: no
  T5 a medida não vê o embedding de entrada, no BERT vê; declarado na análise. (2) Fase A: o gradiente do `shared` é
  zerado antes do passo, então o encoder fica congelado de verdade (inclusive a entrada); a decisão de 01:55 dizia
  que ele mudava um pouco, isso deixou de valer. Cortes do reducer: parâmetro `n_pairs` sem uso em
  `esnli_dados.training_pairs` e a constante `RTE_T5ENC` (inline). 130 testes passam no notebook e no PC (os 3
  vermelhos do embaralhado seguem vermelhos, decisão sua). Arquivos do PC conferidos por MD5 contra o notebook.
- **02:25 — Pré-voo (training-auditor): LAUNCH**, com a grade antiga parada antes (o `troca.sh` faz isso). Conferiu
  contas de passos (e-SNLI: 125 por época, 1.000 passos, fase A 63, B 300, aquecimento 100), rótulos, nada cortado
  (entrada máx. 83 tokens no e-SNLI, 308 no RTE com o tokenizador do T5), braço `t5enc_decoder` inteiro na CPU (fases
  B e C, medidas e predição; grupos 109,6M / 0 / 137,9M parâmetros, sem duplicata). Riscos que ele levantou e que
  NÃO mudei: (a) o `memory_check` subestima o pico (roda antes de o AdamW ter estado): vale a linha "pico" de cada
  treino; (b) **no T5 a L_aux começa com gradiente ~100× maior que o da L_cls** (268 × 0,22 no passo 1; no BERT
  9,5 × 0,98). Com o corte da norma em 1,0 e taxa 5e-5, o sinal da classificação fica espremido na fase C enquanto a
  L_aux for alta. Mantive porque o pedido é o mesmo treino; se o `t5enc_decoder` ficar abaixo do `t5enc`, essa é
  a primeira explicação a testar (peso da L_aux ou corte por grupo), e as normas g_c e g_a por passo estão no
  `gradientes.csv`. (c) embedding `shared` nas medidas: já corrigido (02:20).
- **03:07 — Grade do BERT completa (20/20) e analisada:** `resultados/rte-treino/analise-grade.md` (gerado) +
  `leitura-grade.md` (leitura). BERT cru `prop` 0,736; decoder `prop` −0,028 pareado (IC −0,071 a +0,015), perde nas
  5 sementes; no `500` empata. Leitura: nulo com tendência a atrapalhar. Com micro-lote 8 cada treino com decoder
  levou 530 s e pico de 5,6 GB, sem transbordo (antes: 800 a 2.770 s). `analise_grade.py` generalizado (base = mesmo
  encoder sem decoder, métricas presentes no CSV, `--saida`, `--titulo`, `--avaliacao`, `--agrawal`) para servir
  ao T5 e ao e-SNLI.
- **05:05 — Grade do T5 completa (10/10) e analisada:** `resultados/rte-t5enc/analise-grade.md` + `leitura-grade.md`
  + `comparar_ponte.py`. `t5enc` 0,636 (0,10 abaixo do BERT); `t5enc_decoder` 0,522, −0,115 pareado (IC −0,140 a
  −0,089), perde 5/5. Causa medida: no braço com decoder a L_cls da sonda fica em ln 2 o treino todo; o gradiente
  da L_cls pelo T5 é ~10× menor que pelo BERT e 0,1·L_aux domina de 2 a 11×. Leitura: desequilíbrio de escala com a
  receita do BERT, não evidência contra o método. Ponte: lendo o próprio encoder, as palavras copiadas custam 2,5
  contra 4,5 nats por token (a ponte custa ~2 nats por palavra copiada); no total os dois terminam ~3,1 porque o
  decoder do t5-base aprende o molde mais rápido (efeito de checkpoint). Não rodei variação de taxa nem de peso:
  fica em Próximos passos, decisão sua.
- **06:05 — e-SNLI completo (10/10) e analisado:** `resultados/esnli-treino/analise-grade.md` + `leitura-grade.md`.
  BERT 0,916 / acurácia 0,797; decoder 0,909 / 0,787; −0,007 pareado (IC −0,015 a +0,002), vence 1/5. Grupo N (palavra
  nova) = 24% dos tokens e ~40% do empurrão (no RTE 13% e ~15%), e ainda assim nada de ganho.

## Feito (rodada de 10/11, 01:50–06:05)

1. **Análise da grade do RTE (20 treinos).** Verificado: `analise_grade.py --agrawal` rodou sobre os CSVs copiados
   do PC às 03:07 (20 linhas). Leitura em `resultados/rte-treino/leitura-grade.md`. BERT cru `prop` 0,736; decoder
   nulo no `500` (+0,007) e com tendência a atrapalhar no `prop` (−0,028, perde 5/5, IC cruza o zero).
2. **T5 como encoder: código.** Verificado por 130 testes (notebook e PC; os 3 vermelhos do embaralhado seguem
   vermelhos), fumaça do `t5enc` na CPU, checagem dos pesos do v1.1, auditoria de código (2 correções) e pré-voo
   (LAUNCH). O braço `t5enc_decoder` não fumaçou na CPU do notebook (RAM); rodou direto na GPU, 5/5 sem erro.
3. **T5 como encoder: grade (10 treinos).** Verificado: exit 0, 10 linhas, analisado. Leitura em
   `resultados/rte-t5enc/leitura-grade.md`: com a receita do BERT o T5 classifica mal (0,636) e, com decoder, nem
   sai do acaso (0,522), porque a L_aux domina o gradiente; a ponte custa ~2 nats por palavra copiada.
4. **e-SNLI: código** (3 classes, `--tarefa esnli`, `esnli_dados.py`). Verificado: testes de 3 rótulos, fumaça na
   CPU com o BERT mínimo, impressão MD5 da amostra igual nas duas máquinas.
5. **e-SNLI: grade (10 treinos).** Verificado: exit 0, 10 linhas, analisado. Leitura em
   `resultados/esnli-treino/leitura-grade.md`: nulo de novo (−0,007).
6. **Resto da grade do BERT relançado com micro-lote 8** depois do transbordo de VRAM: 530 s por treino, sem erro.

## Bloqueado

- **Commit e PR** (hard stop do modo autônomo). Fica sem commit, no notebook: `src/radibert/rte_{modelo,dados,treino,
  gradientes}.py`, `src/radibert/esnli_dados.py` (novo), `tests/test_rte_treino.py`, `.gitignore`, os relatórios
  em `resultados/rte-treino/`, `resultados/rte-t5enc/`, `resultados/esnli-treino/` (sem `run/` e `fumaca/`, que o git
  ignora). No PC, `D:\RaDi-BERT` tem os mesmos 5 arquivos de `src` + o teste copiados por `scp` (cópia suja, MD5
  igual ao notebook): depois do commit no notebook, `git checkout -- src tests` e `git pull` no PC, ou commitar de
  um lado só. **Não commitar com os 3 testes vermelhos do embaralhado** (decisão sua, passo 3 do HANDOFF).

## Próximos passos

1. **(Pedro)** Ler as três leituras (`resultados/*/leitura-grade.md`) e decidir o que vai para o termo da Semana 9
   (gate de quarta 11/11). Achado central: três nulos bem medidos (RTE `500`, RTE `prop`, e-SNLI) e o porquê
   mecânico (empurrão ortogonal à L_cls; o decoder aprende o molde).
2. **(Pedro: decisão)** Se quiser um teste justo do T5: taxa de T5 (1e-4 a 3e-4) e/ou peso da L_aux pela escala do
   gradiente. São ~1 h no PC. Sem isso, o resultado do T5 é "a receita do BERT não serve ao T5", não um veredito
   sobre o método.
3. **(Pedro: decisão)** Varredura do peso da L_aux (0,5 e 1,0) no BERT, que nunca foi feita (o paper não varre), e
   o controle embaralhado (testes vermelhos esperando).
4. **(Pedro: git)** Commit no branch `feat/treino-rte` e sincronizar o PC.
