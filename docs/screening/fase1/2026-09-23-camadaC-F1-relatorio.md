# Camada C, F1 — árvore de citação: relatório (23/09/2026)

**Status: executada, coluna `camada_C_F1` gravada na tabela-mestra** (`2026-09-22-floresta-obras.csv`).
Nada apagado: quem "desce" vai para o fim da fila e continua no bruto. **Nível 3:** citação é metadado
de base, não leitura. Ordem do Pedro: "roda a f1" (23/09).

---

## 1. O que a F1 faz e por quê

É a primeira fase da leitura por agentes (desenho `2026-09-23-desenho-agentes.md`, M1 = b). Ninguém lê nada.
A pergunta é só: **esta obra está ligada, por citação, ao mesmo bloco de literatura em que estão os
surveys que já sabemos serem da área?** Quem cita ou é citado por esse bloco fica; quem não tem ligação
nenhuma com ele desce para o fim da fila. A lógica é que uma área de pesquisa se cita entre si: um survey
de compressão de LLM cita (e é citado por) outros trabalhos de eficiência, enquanto um survey de
escalonamento de projetos não cita nenhum deles.

**Três exceções, decididas antes de rodar:**
- **Bilhetes** (⟨rev-36⟩): obras com técnica pequena não passam pela F1 — golden ticket (<= 20 obras) vai
  para a última fase, 21–50 para a penúltima.
- **Recentes (2025–26):** ainda não tiveram tempo de ser citadas; ficam mesmo soltas.
- **Sem dado de citação:** obra sem referências em nenhuma fonte e que ninguém do conjunto cita **não
  desce** — falta de dado não é evidência de estar fora (mesma lógica do `sem acesso`, M6).

## 2. O problema que apareceu, e como foi resolvido

**Primeira rodada descartada.** O Semantic Scholar, pelo endpoint em lote, devolveu a lista de
referências **vazia** para 9.343 das 14.901 obras (63%), embora o próprio registro diga que elas têm
referências. A rede saiu com 3.740 ligações e 12.594 obras isoladas — isolamento por falta de dado, não
por falta de ligação. Essa rodada não foi gravada.

**Diagnóstico:** duas causas diferentes.
1. O endpoint em lote esconde referências que o endpoint **obra a obra** devolve. Recoletei as 9.343 uma
   a uma (4h35): 4.348 vieram; **4.993 continuaram ocultas** mesmo assim.
2. As ocultas são, na maioria, de **editoras** (IEEE, Elsevier, ACM): o S2 não expõe as referências
   delas por licença. O **OpenAlex** expõe. Em teste com 21 ocultas, o OpenAlex tinha as referências de
   21/21. O inverso também vale: o OpenAlex é fraco em preprints do arXiv, onde o S2 é bom.

**Solução (Pedro pediu "uma maneira mais confiável", 23/09):** duas fontes, **união das ligações**. A
cita B se o S2 **ou** o OpenAlex disser, e a ligação vale nos dois sentidos — obra com referências
escondidas ainda se liga se alguém do conjunto a cita.

**Cobertura final das referências:**

| fonte com referências | obras |
|---|---|
| S2 e OpenAlex | 3.734 |
| só S2 | 3.756 |
| só OpenAlex | 4.417 |
| nenhuma | 2.994 |

Das 2.994 sem referência própria, 280 se ligam mesmo assim porque alguém do conjunto as cita; as outras
2.714 viram `sem dado de citação`.

## 3. A rede

- **20.222 ligações** entre as 14.901 obras (só citações **dentro** do conjunto contam).
- **Um bloco dominante de 6.332 obras**; o segundo maior tem 21. Não há "outra área" grande e conectada:
  fora do bloco, o que existe são obras isoladas (7.927) e ilhas minúsculas.
- O bloco dominante é o que contém os surveys conhecidos: **27 das 28** obras de ajuste do gabarito estão
  nele (a 28ª tem bilhete e nem passou pela F1).
- No bloco, a mediana é de 3 ligações por obra; 1.654 obras têm só uma.

## 4. Resultado

| destino | obras | o que acontece |
|---|---|---|
| ligada | 6.228 | segue para a F2 |
| solta recente (2025–26) | 2.350 | segue para a F2 (exceção de ano) |
| sem dado de citação | 2.714 | segue para a F2 (não desce por falta de dado) |
| penúltima (bilhete 21–50) | 125 | pula para a F3 |
| golden (bilhete <= 20) | 3 | pula para a F4 |
| **solta (desce)** | **3.481** | fim da fila |

**Seguem para a F2: 11.292** (6.228 + 2.350 + 2.714). Das 3.481 que descem, 1.214 têm palavra de tipo
("survey", "review"…) no título.

**Por categoria da camada B** — a F1 corta mais onde a camada B já desconfiava:

| categoria B | obras | descem | % |
|---|---|---|---|
| núcleo | 5.682 | 1.091 | 19% |
| misto | 5.752 | 1.164 | 20% |
| a testar (`uso?`) | 1.194 | 437 | 37% |
| dentro (§1.2.1 d) | 767 | 314 | 41% |
| salvaguarda do título | 952 | 323 | 34% |
| arquiteturas (§1.1) | 554 | 152 | 27% |

## 5. Perda medida (metade de teste do gabarito)

**28 de 28** obras de teste que chegaram à F1 estão ligadas ao bloco — **nenhuma perda na F1**. Somando as
camadas anteriores, o processo mantém **28 de 29 (97%)**; a única perda continua sendo *A Survey on Green
Deep Learning*, na camada A. Duas obras de teste (*Efficient Large Language Models: A Survey* e *A Survey
of Resource-efficient LLM and Multimodal Foundation Models*) não têm referências em nenhuma fonte e se
ligam só porque são muito citadas pelo conjunto — é a regra "nos dois sentidos" funcionando.

**Limite desta medida:** o gabarito tem só surveys com 60+ citações, julgados por título (ver a conversa
de 23/09). Surveys conhecidos e citados são justamente os mais fáceis de ficar ligados; a medida não diz
quanto a F1 perde de obras recentes ou pouco citadas.

## 6. Como ler o que desceu

**As 25 soltas mais citadas** são, em quase tudo, ruído de outras áreas que sobreviveu às camadas A e B
por palavra ambígua: rastreamento de potência em painel solar (*MPPT … embedded board*), escalonamento
de projeto com recurso limitado (*resource-constrained project scheduling*, 2 obras), desenvolvimento
ágil, concreto leve (*Lightweight Concrete*), LoRa de rádio (*Recent Advances in LoRa*), MIP* = RE,
neurociência de redes.

**Mas há borda no meio**, e ela precisa ser vista, não esquecida:
- *Literature review: efficient deep neural networks techniques for medical image analysis* (2022, 281 cit.);
- *Investigations of Object Detection … Using Various Deep Learning Techniques and Embedded Platforms* (2020);
- na amostra aleatória de 25: *Accuracy and Resiliency of Analog Compute-in-Memory Inference Engines*
  (hardware, que §1.2.1 põe como divisão), *Embedded Neural Networks for Medical Image Classification*,
  *Lightweight Deep Learning Model for Weed Detection for IoT Devices* (aplicação específica).

A amostra aleatória de 25 teve **uns 3 casos de borda e o resto ruído**. Isso não pede mudar a F1, que
**ordena e não apaga**, mas pede uma decisão sua:

## 7. Decisões suas

1. **O que fazer com as 3.481 que desceram?** (a) ficam no fim da fila e só voltam se a bola de neve
   trouxer alguma; (b) passam pela F2 também, com a amostragem, e aí um grupo com relevante não
   desce; (c) só as 1.214 com palavra de tipo no título passam pela F2.
2. **"Sem dado de citação" (2.714)** segue para a F2 como qualquer ligada — confirma?
3. **Confirmação pendente da F2:** grupo de 50–99 obras lê 30% do grupo?

**Respostas do Pedro (24/09):** (1) **opção c** — das 3.481 que desceram, só as 1.214 com palavra de tipo no
título passam pela F2; as outras ficam no fim da fila. (2) **sim**, "sem dado de citação" segue para a F2.
(3) **sim**, grupo de 50–99 lê 30%. Gabarito: revisar (pedido "sim" à pergunta de revisão/acréscimo).

## 8. Arquivos

- Coluna `camada_C_F1` em `2026-09-22-floresta-obras.csv` (valores: `ligada`, `solta recente (2025-26)`,
  `sem dado de citação`, `penúltima`, `golden`, `solta (desce)`).
- Bruto: `raw/2026-09-23-camadaC-F1-referencias.json` (S2 em lote), `raw/2026-09-23-camadaC-F1-referencias-porobra.json`
  (S2 obra a obra, com estado `ok`/`oculto`), `raw/2026-09-23-camadaC-F1-openalex.json` (OpenAlex por DOI).
- Scripts em `scripts/screening/f1/` (copiados do scratchpad em 24/09, a pedido): `f1_coleta.py`,
  `f1_coleta_porobra.py`, `f1_coleta_openalex.py`, `f1_rede.py`, `f1_viz_*.py`, `md2docx_plain.py`. Os da camada B
  em `scripts/screening/camadaB/`. Caminhos internos ainda apontam para o scratchpad onde havia saída intermediária.
