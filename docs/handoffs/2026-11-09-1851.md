# HANDOFF — 09/11/2026, noite (justificativas do RTE prontas; próximo: explicar e escrever o código do treino)

## Status

**Contexto (sem mudança):** ~3 semanas para as explorações (contado em 31/10), 2 semanas de atraso; base da replicação
= Agrawal 2025; IA liberada para acelerar; notebook (`WKST-001`) = contexto, PC (`DESKTOP-2VBC5EC`, RTX 5060) = GPU,
ligados por `ssh pc`. HANDOFF anterior (09/11, manhã) em `docs/handoffs/2026-11-09-1200.md`.

**Feito nesta sessão (09/11):**
- **Git:** PR #5 mergeado por squash (`21d880c` no `main`). Trabalho novo no branch **`docs/retomada-09-11`**, 2
  commits **sem push**: `72ca7da` (módulo do RTE, docs, checadas, exemplos) e `0dc149c` (lote FA).
- **PC:** `git push` a partir do PC funciona (branch descartável `test/push-pc` no GitHub). Lote do e-SNLI no PC
  ~25–35% mais lento que em 27/10 no regime (~6,5 s/pedido contra ~5,0); não investigado. PC deixado no `main` com
  200 pares a mais no `racionalizacoes-F-35B.csv` e no `progresso.txt` (rastreados, modificados) — decisão do Pedro.
- **Planilha do Forms** (3 respostas: Guilherme, Fernando, Junior = Claude): Qwen aceito 26/29/28 de 30; GPT-3 12/15/4
  de 20; κ contra a maioria do Wiegreffe 0,20/0,30/0,40. Pedro: pouca utilidade com 3 avaliadores; ele não terminou a
  dele. Nada escrito em `entrega/`.
- **Replicação no RTE decidida** (D0–D6) em `docs/2026-11-09-treino-agrawal-rte-explicado.md`. Nenhum código de treino.
- **RTE baixado** (notebook e PC, mesmo SHA-256) em `dados/rte/`, fora do git; `pyarrow==26.0.1` no projeto.
- **Justificativas do RTE:** 6 variantes testadas em 20 pares (F, FP, FP2, FP3, F3, FA; FC descartada).
  **FA** = pergunta com a premissa em parágrafo + pedido "o fato que decide, ou o que falta" + **20 exemplos de RTE**
  (rascunhos do Claude, aprovados pelo Pedro como "bons"). Lote FA completo: **2.470 pares** (treino − 20 exemplos),
  1h20m a 1,96 s/par, todos `stop`, 0 vazios, 1.239/1.231 por rótulo, 20 palavras na mediana.
  Abertura "The text/premise" em 884 (36%) → 434 (18%) depois da limpeza C. 57 nomeiam o rótulo. **Ninguém leu o lote.**
- **Rascunhos não enviados:** pergunta aos autores do Agrawal (`docs/2026-11-09-pergunta-autores-agrawal.md`) e à
  Anthropic sobre o decoder (`docs/2026-11-09-pergunta-anthropic-decoder.md`).
- **Ledger:** `docs/claude/ledger/2026-11-09-retomada.md` (linhas 1–45; todas done/dropped).

## Decisions

- **Pedro (09/11):**
  - RTE primeiro, e-SNLI depois. **Não escrever o código do treino sem ele entender antes.**
  - D0 professor = Qwen3.6-35B-A3B (desvio declarado Mixtral → Qwen); Claude fora pela Usage Policy.
  - D1 prompt = F adaptada com checada rápida → virou **FA**. O Agrawal não publicou justificativas nem código.
  - D2 aquecimento: rodar a cópia fiel (500 passos ≈ 80% de ~623) **e** a proporcional.
  - D3 leitura literal das fases (A = uma passada por metade dos pares, só decoder, BERT congelado, só L_aux;
    B = passos 1–187, taxa do BERT subindo, só L_aux; C = passos 188–623, L_cls + 0,1·L_aux) + perguntar aos autores.
  - D4 métricas: ROC-AUC, Recall e Precision a 0,7 (as do Agrawal) + acurácia + F1 macro + F1 por classe.
  - D5 5 sementes; 10 se a 1ª rodada mostrar que é barato. D6 teste na CPU com adaptador 128 → 768.
  - Marca de discordância **adiada** (3/10 agora; volta se o e-SNLI der ganho pequeno ou instável).
  - "Abertura repetida", nunca "cacoete" (memória).
- **Rejeitados (logados no CLAUDE.md):** FC; proibir a frase no prompt; Claude como gerador do RTE.
- **Claude, declarado:** túnel SSH para rodar o lote sem commit (o código só existia no notebook); 3 pedidos
  simultâneos porque o prompt da FA tem ~1.800 tokens; a C fica fora do CSV (texto original guardado).
- **Correção registrada:** eu disse que o prompt do Agrawal era simples; o Apêndice C é elaborado (só e-commerce,
  assimétrico: só defende "relevante"). Ver `docs/2026-11-09-prompt-agrawal-padroes.md`.
- **Becos técnicos:**
  - O guardrail do projeto olha o branch do **notebook**: commit/push no PC por SSH é barrado se o notebook estiver no
    `main`; e barra `--delete-branch` (padrão de deleção) e heredoc Python com aspas que ele não lê (usar Edit).
  - O `llama-server` sobrevive à queda da sessão SSH: sempre `ssh pc 'Stop-Process -Name llama-server -Confirm:$false'`.
  - O 1º `git pull` do PC no dia caiu com "Connection closed by remote host"; o 2º passou.

## Files touched

- Commitados no `docs/retomada-09-11`: `src/radibert/rte_racionalizacoes.py`, `src/radibert/paths.py`,
  `tests/test_rte_racionalizacoes.py` (71 testes no total, verdes), `pyproject.toml`, `uv.lock`, `requirements.txt`,
  `.gitignore`, `dados/README.md`, `docs/2026-11-09-*.md` (4), `docs/claude/ledger/2026-11-09-retomada.md`,
  `resultados/rte-35B/` (candidatos-exemplos-rte.md, checada-FP-FP2/FP2-FP3/FP3-F3/FP3-FA.md,
  racionalizacoes-F/FP/FP2/FP3/F3/FA.csv).
- Sem commit: `CLAUDE.md` (bloco da replicação + 3 rejeitados), este `HANDOFF.md`.
- Fora do repo: memória `sem-palavra-cacoete.md`; `dados/rte/` (notebook e PC); `D:\tools\rte-servidor.log` (PC).
- **Lixo (apagar é decisão do Pedro):** `resultados/rte-35B/racionalizacoes-FC.csv`, `checada-FP3-FC.md`,
  `checada.md` (nome antigo), `docs/claude/ledger/2026-11-09-retomada.md.new` (vazio, erro meu; comando do
  gatekeeper já entregue), `resultados/rte-35B/run/` (log do lote, ignorado pelo git); no PC `D:\tools\teste-*`,
  `D:\tools\rte-servidor.log`, os 200 pares extras do e-SNLI; no GitHub o branch `test/push-pc`; branches antigos
  de 08/11.

## Next steps

1. **(Claude, só explicação)** Explicar o **código** do treino antes de escrevê-lo (pedido do Pedro): arquivos,
   classes (BERT + cabeça + decoder do T5 com cross-attention), laço com as fases A/B/C, onde entra a C e os 20
   exemplos fora do treino, invariantes. Esperar o OK dele.
2. **(Pedro: decisão)** Ler uma amostra do lote FA (sugestão: 30 pares sorteados) antes de treinar.
3. **(Claude, depois do OK)** Escrever o treino num branch `feat/treino-rte`, testar na CPU com
   `google/bert_uncased_L-2_H-128_A-2` + adaptador, rodar no PC (código pelo git; `ssh pc`).
4. **(Pedro: git)** Push e PR do `docs/retomada-09-11`; commitar `CLAUDE.md` e este `HANDOFF.md`.
5. **(Pedro: decisão)** Enviar ou não os e-mails aos autores e à Anthropic; decidir o lixo listado acima.
6. **(Pedro: decisão)** Pendências antigas: folha extra +50 do Qwen, nome do aluno (RaDiBERT/WhyBERT),
   `esnli_test.csv`.

## Resume commands

```bash
cd "C:/Users/Pedro/Documents/Projects/UFG/2026-2/Residencia Bacharelado em Inteligencia Artificial"
git status -sb                                   # docs/retomada-09-11, 2 commits sem push
uv run --frozen pytest -q                        # 71 passed
cat docs/2026-11-09-treino-agrawal-rte-explicado.md
uv run --frozen python -c "import pandas as pd; d=pd.read_csv('resultados/rte-35B/racionalizacoes-FA.csv'); print(len(d))"
ssh pc hostname                                  # DESKTOP-2VBC5EC
# servidor no PC + túnel (o lote usa localhost:8080 no notebook):
ssh -o ServerAliveInterval=30 -L 8080:127.0.0.1:8080 pc '& "C:/Program Files/Git/bin/bash.exe" -s' <<'EOF'
cd /d/RaDi-BERT && source config/maquina.env && timeout 10800 "$LLAMA_SERVER" -m "$MODELO_35B" $LLAMA_ARGS --host 127.0.0.1 --port 8080
EOF
ssh pc 'Stop-Process -Name llama-server -Confirm:$false'   # sempre, ao terminar
```
