# Notas — Agrawal, Ahemad & Sembium (COLING 2025 Industry)

**Título:** *Rationale-Guided Distillation for E-Commerce Relevance Classification: Bridging Large
Language Models and Lightweight Cross-Encoders*
**Venue:** Proceedings of the 31st International Conference on Computational Linguistics: **Industry
Track**, pp. 136–148, jan. 2025, Abu Dhabi. **Verificado na ACL Anthology** (`2025.coling-industry.12`).
**Afiliação:** Amazon, Índia (os três autores).
**PDF:** `docs/artigos/2025.coling-industry.12-agrawal.pdf`

## PROCEDÊNCIA

**Nível 2 — Claude leu o texto completo em 10/09/2026.** Abstract, §1, §2, §3, §4.1–4.4, §5 e §5.2
lidos no PDF extraído. **Pedro NÃO leu.** Nada daqui entra em texto assinado por ele sem leitura.

---

## Veredito de uma linha

**Este paper ocupa o H2 e, numa variante, também o H1.** É a arquitetura do tema v3, publicada em
janeiro de 2025, sobre BERT 110M, com a cabeça descartada na entrega. A pendência 5 fecha com o
resultado ruim.

---

## O método (§4.3) — a citação que decide

> "Our method integrates LLM-generated rationales as an **auxiliary task** during cross-encoder
> training, utilizing a **cross-encoder-decoder architecture**. In this framework, the cross-encoder
> handles the primary binary classification task, while the **decoder generates rationales** based on
> LLM outputs. For inference, we streamline the process by deploying **only the cross-encoder model,
> removing the need for the LLM-based rationale generator or decoder module**."

Arquitetura, literal do §4.3:

| Componente | O que é |
|---|---|
| Encoder | **BERT base, 110M, 12 camadas, hidden 768** |
| Cabeça de classificação | camada linear sobre o token `[CLS]`, saída binária |
| Cabeça auxiliar | **decoder T5 base**, geração autorregressiva da racionalização |
| Entrada do decoder | as representações de token do encoder (testam com e sem o `[CLS]`) |
| Professor | **Mixtral 8×7B Instruct** (AWS Bedrock) |
| Prompt do professor | recebe a tripla (query, produto, **rótulo**) e pede "Explain why" |

**Perda:**

```
L_total = L_classification + λ · L_aux
L_classification = BCE(y, ŷ)
L_aux            = − (1/N) Σ Σ log P(r_{i,t} | r_{i,<t}, h_i)     [cross-entropy de token]
λ = 0,1  —  "based on our early experiments"
```

## §4.4 "Practical Modifications" — fecha a pendência 9b do tema v3

- **Warmup do decoder:** treinam **só o decoder**, com o **BERT congelado**, em 50% dos dados. Depois
  um warmup linear do encoder nos primeiros 30% do treino, com `L_warmup = L_aux` apenas. Só então
  ligam a perda de classificação.
- **Ignorar o `[CLS]` na entrada do decoder** — testado nas duas formas.
- **"Embedding-based Reasoning"** — alternativa barata: compara o embedding da racionalização
  (gerado por **BGE-M3**) com a saída da última camada do cross-encoder **mean-pooled**.
  → **isto é o H1 do tema v3.**

A pendência 9b do tema v3 supunha que a cabeça auxiliar nasceria do zero. **Não precisa** — eles
usam um T5 base pré-treinado e ainda adicionam warmup em duas fases. O confundidor tem solução
publicada.

## Resultados — LEITURA DAS TABELAS (10/09, tarde; substitui o bloco de manchete abaixo)

**Linha 481 do PDF:** *"mean and the **95% confidence interval** in our tables."* Os parênteses são IC
de 95%, não desvio padrão — dá para ler significância direto.

### Tabela 1 — 9 mercados de e-commerce, ganho relativo ao BERT baseline (BERT + Reasoning)

| Mercado | 10K amostras | 100K amostras |
|---|---|---|
| AU | +2,21 (±0,70) | +1,21 (±1,20) |
| ES | +2,84 (±1,11) | +1,45 (±1,39) |
| **BR (português)** | **+0,37 (±1,05)** | **+1,14 (±1,21)** |
| AE | +1,45 (±0,94) | +1,83 (±1,20) |
| FR | +2,11 (±0,96) | +2,16 (±1,24) |
| MX | +0,32 (±0,84) | +2,16 (±1,23) |
| Arábia | +1,56 (±0,95) | +2,20 (±1,21) |
| DE | +2,14 (±0,85) | +1,81 (±1,15) |
| IN | +1,76 (±1,05) | +0,87 (±1,24) |

- **4 das 18 células cruzam o zero** (BR 10K, BR 100K, MX 10K, IN 100K); AU 100K e ES 100K encostam.
- **Português é o único mercado em que nenhuma das duas medidas é significante.** Os dados de BR
  são proprietários da Amazon ("anonymized, aggregated, do not represent production distribution") —
  irreproduzíveis.
- Coluna "melhor LLM 7B fine-tunado": a 10K, BERT+Reasoning vence em 6 de 9; a 100K, em 1 de 9.
  A vantagem do método é **maior onde há pouco dado rotulado** — é a história de eficiência de dado.
- LLM zero/few-shot fica −23% a −36% / −7,5% a −20% abaixo do BERT fine-tunado.

### Tabela 2 — GLUE e QADSM, ROC-AUC absoluto

| Tarefa | BERT | + Reasoning | LLM 7B fine-tuned |
|---|---|---|---|
| QQP | 0,9571 | 0,9625 | 0,9728 |
| **RTE** | **0,4754** | **0,5873** | **0,8867** |
| MRPC | 0,7955 | 0,8811 | 0,9486 |
| QNLI | 0,9467 | 0,9531 | 0,9887 |
| CoLA | 0,5912 | 0,6130 | 0,9060 |
| SST-2 | 0,9488 | **0,9480** | 0,9907 |
| QADSM | 0,7174 | 0,9123 | 0,8787 |

- **O baseline de RTE é 0,4754 — abaixo do acaso.** Motivo declarado na §5: o baseline é *"BERT base
  further trained on MS-MARCO query-passage relevance"* — um BERT ajustado para relevância de busca,
  aplicado a GLUE. **Não é baseline de GLUE.**
- **O "+6% em GLUE" do resumo vem quase todo de RTE (+11,2 pts) e MRPC (+8,6)**, onde o baseline está
  quebrado ou fraco. Onde o baseline é forte, o ganho some: QQP +0,5, QNLI +0,6, **SST-2 piora 0,1**.
- **"Empata com LLM de 7B" só vale no e-commerce.** Em GLUE o 7B atropela (RTE 0,8867 vs 0,5873).
  O resumo generaliza uma alegação que a própria Tabela 2 contradiz.

### Correção a uma leitura minha de 10/09

Eu havia apresentado "+1,4% e-commerce → +6% GLUE" como evidência de que o ganho cresce com texto mais
longo e inferencial. **Retirado.** Com o baseline de RTE abaixo do acaso, o salto é artefato de
baseline, não efeito de comprimento. A hipótese de comprimento sobrevive só pelo argumento de
mecanismo (com ~12 tokens a racionalização é paráfrase da entrada; com parágrafo precisa selecionar)
— **sem apoio empírico prévio**.

### Veredito sobre a evidência

**Sólido:** e-commerce, +1 a +2% ROC-AUC, majoritariamente significante, eficiência de dado real.
**Fraco ou superalegado:** português dentro do ruído · GLUE contra baseline de domínio errado · SST-2
piorou · "empata com 7B" falso fora do e-commerce · sem controle · sem OOD · λ sem varredura.

## Resultados (manchete do resumo — mantido para referência; ver leitura acima)

- +1,4% ROC-AUC médio em 9 datasets multilíngues de e-commerce
- +2,4% em 3 datasets ESCI (US, JP, ES; 100K treino / 10K teste)
- **+6% em GLUE**
- estado da arte em QADSM, superando LLMs com fine-tuning
- **BERT de 110M empata com LLMs de 7B** (< 1% de diferença de ROC-AUC), **50× mais rápido por amostra**
- Ganho **maior com pouco dado**: com 10K amostras vence o melhor LLM fine-tunado em 6 de 9 casos;
  com 100K, em 1 de 9. (Mesma direção do Distilling Step-by-Step.)

**Tarefas de GLUE usadas (Tabela 2):** QQP, **RTE**, MRPC, **QNLI**, CoLA, SST-2, + QADSM.
→ Inferência textual **está** coberta, via RTE e QNLI. **MNLI e SNLI/e-SNLI não estão.**

Posicionamento declarado deles no §2, contra o Distilling Step-by-Step:
> "Hsieh et al. demonstrate the effectiveness of distilling LLM-generated rationales using T5
> encoder-decoder models in a text-to-text framework. **In contrast, our work applies this concept to
> smaller BERT cross-encoder models (110M parameters) in a classification setting**."

Ou seja: eles **já escreveram a frase de abertura do tema v3**.

---

## O QUE ESTE PAPER NÃO TEM — e é aqui que sobra trabalho

Verificado lendo §5.2 e procurando por controle em todo o texto.

1. **NENHUM controle de racionalização aleatória ou embaralhada.** A seção intitulada "5.2 Ablations"
   **não é uma ablação** — é análise qualitativa de mapas de atenção e valores de Shapley, mais a
   afirmação de que as racionalizações geradas "are coherent and show deeper task understanding".
   Não há nenhuma condição em que a racionalização seja substituída por texto aleatório, embaralhado
   entre exemplos, ou desalinhado do rótulo.

   **Consequência:** a alegação causal central do paper — que o **conteúdo** da racionalização é o que
   ajuda — **não tem controle que a sustente**. Todo o ganho é compatível com a explicação alternativa
   de regularização por ruído, que é exatamente o que **Herrewijnen et al. (EACL 2026) demonstraram
   acontecer no canal de atenção**, onde tokens aleatórios rendem melhora parecida com racionalização
   humana.

2. **Nenhuma avaliação fora de domínio.** Treino e teste saem da mesma distribuição em todos os
   conjuntos.

3. **Nenhuma varredura de λ.** O valor 0,1 é justificado como "based on our early experiments", sem
   tabela. O **DHRD encontrou α=β=1 como ótimo em três modelos** — uma ordem de grandeza acima.
   Ninguém conciliou os dois.

4. **Nenhuma seção de Limitations.** (Industry track.)

5. **Sem sementes múltiplas na análise de §5.2** (as tabelas principais trazem ±, a §5.2 não).

---

## O que isso faz com o tema v3

**Morre:** "acoplar uma cabeça decodificadora auxiliar a um encoder e descartá-la na inferência" como
**contribuição de mecanismo**. Está publicado, com números melhores do que os que caberiam numa RTX
5060, por um time da Amazon, e em industry track de COLING.

**Morre também:** a célula vazia da taxonomia registrada em `tema-v3` ("racionalização de LLM em
texto livre → encoder, via canal de saída"). **Está ocupada.** O levantamento anterior por agente
(nível 3) classificou este paper como incógnita e não detectou o mecanismo; a leitura em nível 2
resolve — e mostra por que triagem nível 3 nunca serve para decidir novidade.

**Sobrevive:** a **contradição aberta de três vias sobre o que a racionalização de fato carrega**,
que agora é a pergunta mais bem posta do projeto:

| Trabalho | Arquitetura | Canal | Controle rodado? | Conclusão |
|---|---|---|---|---|
| **Herrewijnen** (EACL 2026) | encoder | atenção | **sim** (tokens aleatórios) | **é ruído** |
| **Li et al.** (2508.16777) | encoder (PLM-ICD) | atenção | não | sem ganho de acurácia |
| **DHRD** (Xu 2025) | **decoder** | saída | **sim** (embaralhamento) | **é conteúdo** |
| **Agrawal** (COLING 2025) | **encoder** | **saída** | **NÃO** | afirma conteúdo, **sem evidência** |

**A célula que continua vazia é a do controle, não a do mecanismo.** Ninguém rodou o controle de
racionalização embaralhada sobre o canal de **saída** de um **encoder**. Herrewijnen mostrou que a
ausência exata desse baseline invalidou boa parte de uma literatura — e é o paper que o Pedro
escolheu como modelo de boa pesquisa no `mapa-do-terreno`.

**Tensão a declarar:** isso se aproxima do que o `CLAUDE.md` rejeitou em 10/09 — "reanálise de
resultado publicado como objeto de pesquisa próprio". Não é idêntico (não se julga a análise deles;
roda-se uma **condição experimental nova** que eles não rodaram, que é replicação com extensão, o
desenho do próprio Herrewijnen). Mas é adjacente o bastante para exigir decisão explícita do Pedro,
não deslizamento.

## Fonte

https://aclanthology.org/2025.coling-industry.12/ — PDF baixado e lido em 10/09/2026.
