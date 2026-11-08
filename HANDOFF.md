# HANDOFF — 31/10/2026 (Semana 8 entregue; próxima: fechar a avaliação e desenhar o primeiro treino)

## Status

**Feito (27–29/10):**
- **Lote 35B + variante F no TREINO do e-SNLI:** 16.000 pares em 5h20, 1,20 s/par, todos com `stop`, na ordem da
  amostra embaralhada (semente 42). `resultados/lote-35B/racionalizacoes-F-35B.csv`.
- **Eco marcado:** `marcar_eco.py` -> `marcas.csv`; 1.252 pares (7,8%; 23,5% das implicações); a regra reproduz o dev.
  **Discordância NÃO marcada** (precisa de GPU).
- **Avaliação humana cega** pela rubrica de Wiegreffe et al. 2022 (App. B.3): 30 do Qwen + 20 do GPT-3 já julgados
  pelos avaliadores do paper (5 por contagem de votos), embaralhados. Gabarito `leitura-50-gabarito.csv` (não mostrar
  a avaliadores). Google Forms via Apps Script (`criar_formulario.gs` em inglês; `criar_formulario_pt.gs` com
  `traducao-pt.json` para amigo sem inglês — respostas PT à parte). Respondida por Pedro e amigos; **sem resultado**.
- **Termo da Semana 8 entregue pelo Pedro em 29/10** (versão dele em `entrega/termos-entregues/Termo Semana 8.docx`;
  rascunho meu em `docs/residencia/termo-de-entrega-Semana-8.md`). Documento linkado: `entrega/Geracao do Primeiro Lote.docx`
  (fonte `entrega/geracao-primeiro-lote.md`: pedido E × F, velocidade, lote, eco) + o Forms.
  Planejamento entregue: juntar respostas e medir aceitáveis; marcar discordância; definir encoder, decoder, como o
  decoder recebe a justificativa e as primeiras versões do treino.
- **Skill `termogate` atualizada** (29/10) a partir da comparação dos termos entregues S3–S8 com os rascunhos: regras
  12–16 (4–6 itens curtos; número só se for o achado; sem itens de higiene de processo; sem regra externa como motivo;
  espaço para a frase dele), regra 3 (LLM dentro do item, sem item de fechamento) e 6 (obstáculo concreto pode entrar),
  tabela de evidência. Termos entregues S2–S8 copiados em `entrega/termos-entregues/` (o de S5 era
  `PEDRO MUNDEL BIFFI_071026.docx`).
- **Preparação de arguição** (no chat, não salva em arquivo): perguntas prováveis e "fdp" com respostas — cross-attention
  e por que ajuda; braços de controle; risco do decoder ignorar o encoder e como medir; teto do SNLI; sementes.

**Em aberto quando parou:**
- Pedro não respondeu se quer a **folha extra com +50 justificativas do Qwen só para ele** (30 dá ±14 pontos a 80%; 80
  dá ±9).
- **Nome do aluno:** DR-BERT descartado (DrBERT existe, biomédico francês); RaDiO-BERT desaconselhado (choca com a
  família RADIO da NVIDIA, destilação; "Optimized" vago; grafia "Rationale"). Recomendação: **RaDiBERT** (livre no HF e
  arXiv; GitHub user `radibert` já existe, vazio) ou WhyBERT. **Decisão do Pedro pendente.**
- **Contingência GPU:** se o PC for para RMA (~3 semanas), recomendado NÃO trocar o tema por survey; fazer o que roda em
  CPU (análise da avaliação, leituras, código do treino testado com `google/bert_uncased_L-2_H-128_A-2`) e alugar GPU
  só para os treinos (opções e preços a pesquisar se acontecer). Antes do RMA: WHEA-Logger, teste de estresse com ASPM
  desligado, placa em outro PC.

## Decisions

- **Pedro:** 35B + F; 16 mil pares; baixar o treino do e-SNLI (27/10). Rubrica do Wiegreffe 2022 com itens do paper
  para calibrar; Forms para amigos; versão em português (29/10).
- **Pedro:** documentação da semana num .docx de entrega (Forms sozinho não serve) (29/10).
- **Rejeitado:** SCOTT (já no `## Rejected` do CLAUDE.md).
- **Becos técnicos (não rejeições do Pedro):** conector Composio para Google Forms (exige projeto próprio no Google
  Cloud); juízes treinados do Wiegreffe (links 404); gerações GPT-3 do Wiegreffe como dado de treino (~1.250 pares,
  qualidade baixa, licença OpenAI incerta).
- **Recomendações do Claude, sem decisão do Pedro:** encoder em dois tamanhos (BERT base para comparar com o Agrawal +
  um pequeno: DistilBERT 66M ou `google/bert_uncased_L-4_H-512_A-8` ~29M; todos Apache-2.0, conferidos no HF);
  braços mínimos = base, justificativa certa, justificativa trocada; medir em todo treino a perda auxiliar com o H do
  par certo × H de outro par (detecta decoder ignorando o encoder); remédios: aquecimento do Agrawal, dropout de
  palavra no decoder (Bowman et al. 2016 — conferir antes de citar), tirar palavras de molde da perda.
- **Ultimatum (outro projeto, nada alterado lá):** ARTEMIS = "Automação do Reconhecimento Textual de Entidades por
  Marcação e Identificação de Spans", sem sufixo (ARTEMIS v1); o Artemis v1 hoje é só trabalhista (model card).

## Files touched

- `resultados/lote-35B/`: `lote.py`, `rodar.sh`, `racionalizacoes-F-35B.csv`, `amostra-treino.csv`, `marcar_eco.py`,
  `marcas.csv`, `montar_leitura_cega.py`, `leitura-50-cega.md`, `leitura-50-gabarito.csv`, `formulario-leitura.html`
  (artifact https://claude.ai/artifact/7inknzM26QzFB8Fy6HRe53, sem uso), `montar_google_forms.py`,
  `criar_formulario.gs`, `criar_formulario_pt.gs`, `traducao-pt.json`.
- `dados/esnli/esnli_train_{1,2}.csv`; `dados/wiegreffe2022/snli_test.csv`.
- `resultados/piloto-qwen/`: `gerar.py`, `medir.py`, `relatorio.md`, `vazao-paralelo/`.
- `docs/residencia/termo-de-entrega-Semana-8.md`; `entrega/geracao-primeiro-lote.md`; `entrega/Geracao do Primeiro Lote.docx`;
  `entrega/termos-entregues/` (S2–S8).
- `.claude/skills/termogate/SKILL.md`; `docs/ideias-de-desenho.md`; `CLAUDE.md`; `HANDOFF.md`.
- Memória: `pc-instavel-out-2026.md`.

**Lixo a confirmar com o Pedro (não apagar sem pedido):** `resultados/lote-35B/google-forms-requests.json`,
`resultados/lote-35B/leitura-50.md`; em `resultados/piloto-qwen/vazao-paralelo/`: `erro.txt`,
`resultados-F-9B-90-w2.csv`, `resultados-F-35B-90-ub128-w4.csv`, `resultados-F-35B-ontem-30.csv`.

## Next steps

1. Perguntar ao Pedro: **folha extra com +50 do Qwen** (sim/não) e **nome do aluno** (RaDiBERT, WhyBERT ou outro).
   Se a folha for sim: 50 pares do lote balanceados por rótulo, pulando os 30 pairIDs de `leitura-50-gabarito.csv`,
   mesma rubrica, sem itens do Wiegreffe.
2. Quando houver respostas: exportar o Forms (planilha); por avaliador, taxa de aceitáveis do Qwen (Wilson 95%);
   concordância entre avaliadores (Krippendorff α) e com os votos do Wiegreffe (aceitável = 2/3 ou 3/3); PT à parte.
   **Pedro, 03/11:** a resposta "Junior" é do Claude e conta como avaliador (mais rigoroso; 3–4 humanos além dele).
   Declarar como LLM e não cego no relato e dar os números com e sem ele.
   Seção nova em `entrega/geracao-primeiro-lote.md` e regerar o .docx.
3. Desenho do primeiro treino com o Pedro: encoder (tabela acima), cabeça auxiliar (blueprint Agrawal 2025: decoder T5
   pré-treinado, L = L_cls + 0,1·L_aux, aquecimento em 2 fases, com/sem `[CLS]`), braços, nº de pares e sementes.
   Primeira rodada sugerida: base sem justificativa em 2/4/8/16 mil pares (mede espaço para ganho).
4. Escrever o código do treino e testá-lo na CPU com `google/bert_uncased_L-2_H-128_A-2` e poucos pares.
5. Marca de discordância (passada do Qwen pedindo só o rótulo, sem ouro; retomável; PC instável).
6. Baixar `esnli_test.csv` só com OK do Pedro.

## Resume commands

```
cd "C:/Users/Pedro/Documents/Projects/UFG/2026-2/Residencia Bacharelado em Inteligencia Artificial/experimentos/lote-35B"
C:/Users/Pedro/Documents/Projects/py311/python.exe montar_leitura_cega.py      # folha cega + gabarito (semente 42)
C:/Users/Pedro/Documents/Projects/py311/python.exe montar_google_forms.py [pt] # -> criar_formulario[_pt].gs
C:/Users/Pedro/Documents/Projects/py311/python.exe marcar_eco.py [dev]         # marca de eco / conferência no dev
C:/Users/Pedro/Documents/Projects/py311/python.exe ../../Screening/scripts/f1/md2docx_plain.py ../../entrega/geracao-primeiro-lote.md "../../entrega/Geracao do Primeiro Lote.docx" <pasta-de-imagens>
bash rodar.sh <alvo> <HH:MM>                                                    # novo lote (servidor 35B, retomável)
```
Python: `C:/Users/Pedro/Documents/Projects/py311/python.exe` (sem `-I`: quebra o pandas). Servidor 35B:
`llama-server -m Qwen3.6-35B-A3B-UD-IQ4_XS.gguf -ngl 999 --n-cpu-moe 30 -c 8192 -np 4 -kvu -cms 0 -ub 128 --jinja`.
Termos entregues: `entrega/termos-entregues/Termo Semana <N>.docx` (a skill `termogate` lê o anterior daqui).
