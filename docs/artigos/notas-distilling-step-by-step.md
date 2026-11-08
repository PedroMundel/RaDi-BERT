# Notas de leitura — Distilling Step-by-Step (Hsieh et al., ACL 2023 Findings)

**Referência:** Hsieh, C.-Y.; Li, C.-L.; Yeh, C.-K.; Nakhost, H.; Fujii, Y.; Ratner, A.; Krishna, R.;
Lee, C.-Y.; Pfister, T. **"Distilling Step-by-Step! Outperforming Larger Language Models with Less
Training Data and Smaller Model Sizes"**. arXiv:2305.02301v2 (05/07/2023), ACL 2023 Findings.
https://arxiv.org/abs/2305.02301 · Código: github.com/google-research/distilling-step-by-step

⚠ **Procedência:** Pedro **leu e escreveu resumo próprio** (`Downloads/Distilling Step-by-Step.pdf`,
cobre resumo, introdução, trabalhos relacionados, método, experimentos, ablações, discussão e
limitações) — **nível 1**. Claude leu §1, §2 (parcial), §3, §4.4 e *Limitations* via extração de PDF,
em 10/09/2026 — nível 2.

**Seção de entregável derivada desta leitura:** `docs/pesquisa/secao-dsbs-cabeca-auxiliar.md` (raiz) — as extrações
que licenciam treinar cabeça auxiliar e descartá-la, com o que é nível 1 e nível 2 separado item por
item.

## A pergunta que motivou esta leitura

Pedro levantou, lendo: o mecanismo só funciona para modelos que geram raciocínio junto da resposta?
Se sim, um encoder (uma passagem só) não teria como receber o benefício, e a resposta seria "use um
T5" — o tema v3 morreria.

## A resposta, textual (§3.2)

> *"Compared with Eq. 2, the rationale r̂i is **not required in the test time**, which removes the
> need for an LLM at test-time."*

**A racionalização NÃO é gerada na inferência.** O mecanismo é sinal de treino apenas.

Como operam: prefixos de tarefa `[label]` e `[rationale]` prependidos à entrada; o modelo aprende a
emitir `ŷ` com o primeiro e `r̂` com o segundo. Na inferência usa-se só `[label]`.

**Consequência para o tema v3:** o ganho não vem de computação em tempo de inferência — vem de sinal
de treino, e sinal de treino é transferível em princípio para outra arquitetura. Consistente com o
DHRD desligar a cabeça no teste e ainda funcionar.

## O que mais a seção 3.2 estabelece

Eles discutem e **rejeitam** a alternativa de dar a racionalização como **entrada adicional**
(Eq. 2 — Rajani et al. 2019; Wang et al. 2022a / PINTO), com o motivo de que exigiria um LLM na
hora de responder. Citam o PINTO pelo nome: *"relies on an LLM to generate rationales at test-time,
and thus does not fully solve deployment challenges."*

→ **Custo de implantação é o eixo central do paper**, não detalhe. É o mesmo eixo do tema v3, e
encoder é o extremo barato dessa reta. A motivação do Pedro é a motivação declarada do trabalho
que ele quer transportar.

Formalmente: `L = L_label + L_rationale`, ambas entropia cruzada sobre tokens (Eq. 1 e 4).

## Trabalhos concorrentes citados por eles (para o levantamento)

Wang et al. 2022a (PINTO — LLM no teste), Ho et al. 2022, Magister et al. 2022, Li et al. 2023.
Eles se posicionam como indo além de Ho e Magister por fazer *"a granular study by varying training
dataset size, exploring downstream model sizes, and demonstrating the effectiveness of our method on
fully unlabeled datasets."* — **esse é o formato de estudo, e é imitável.**

## Setup

Professor: PaLM 540B. Aluno: T5, com T5-Base 220M nos experimentos de redução de dados.
Datasets: **e-SNLI e ANLI** (inferência textual), **CQA** (senso comum), **SVAMP** (aritmética).
Resultados de redução: e-SNLI **12,5%** dos dados supera ajuste padrão com 100%; ANLI 75%,
CQA 25%, SVAMP 20% de redução.

### Os dois números de e-SNLI não são o mesmo — conferido na fonte (15/09, nível 2)

O resumo do Pedro fala em **"0,1% dos dados"**. O número **existe no paper e está certo**, mas é de
outra comparação, e dizer um no lugar do outro erra por duas ordens de grandeza:

| Número | Figura | Contra quem | Modelo |
|---|---|---|---|
| **12,5%** do e-SNLI | Fig. 4 (§ ajuste fino) | **ajuste padrão com 100%** dos dados | T5 220M |
| **0,1%** do e-SNLI | Fig. 8 | **Few-shot CoT do PaLM 540B** | T5 220M (2000× menor) |

Texto do paper, Fig. 8: *"better performance than Few-shot CoT with a model over 2000× smaller (220M
T5) and only 0.1% of the full dataset"*, repetido logo abaixo: *"on e-SNLI in Figure 8, we observe
that Distilling step-by-step outperform the LLM using only 0.1% of the dataset"*.

**Condições que precisam vir junto quando o número for dito em voz alta:** (a) o alvo é o LLM com
CoT de poucos exemplos, **não** o T5 ajustado — bater um LLM promptado em e-SNLI é barra baixa;
(b) a Fig. 8 sai de uma **busca de granularidade grossa** (*"coarse-grained search"*, palavra deles),
então 0,1% é o ponto mais baixo da grade testada, não um limiar medido; (c) 0,1% de 549.367 são
**~550 exemplos** — é o que dá a ele o argumento de eficiência de rótulo, e é a versão do número que
importa para o nosso desenho.

## ⚠ Hipótese nova, formada ao cruzar com o Herrewijnen

**As tarefas deste paper exigem raciocínio de múltiplos passos** (NLI, QA de senso comum,
aritmética). **As tarefas onde o Herrewijnen achou ruído são classificações** (sentimento, discurso
de ódio, posição).

→ **Talvez a diferença entre os dois resultados não seja encoder vs. gerador, e sim tarefa de
raciocínio vs. tarefa de classificação.** Se for, portar o mecanismo para encoder pode falhar por
motivo que não tem nada a ver com arquitetura: encoders são usados justamente em tarefas onde não há
raciocínio para transferir.

Isso é hipótese do Claude formada em 10/09, não afirmação de nenhum dos dois papers. Mas é testável,
e muda o desenho: **a escolha de tarefa deixa de ser detalhe e vira variável crítica.**

**Saída possível:** inferência textual é o cruzamento — é classificação (encoder resolve) e exige
raciocínio. O **e-SNLI tem racionalização humana anotada**. Em português, o equivalente de tarefa é
o **ASSIN2** (RTE), presente em quase todos os papers pt-BR levantados — mas **não se sabe se tem
racionalização anotada; precisa ser verificado.**

## §4.4 e Limitations — lido em 10/09/2026 (o que sustenta o H2)

**Tabela 2 (T5 220M, 100% dos dados) — a ablação de design de treino.** Conferida na ordem de
leitura da página 9 do PDF v2, porque a extração em duas colunas embaralha os números:

| Método | e-SNLI | ANLI | CQA | SVAMP |
|---|---|---|---|---|
| Fine tuning padrão | 88,38 | 43,58 | 62,19 | 62,63 |
| Tarefa única (concatena `[r̂ᵢ, ŷᵢ]`, Eq. 5) | 88,88 | 43,50 | 61,37 | 63,00 |
| Multi-tarefa (saídas separadas) | 89,51 | 49,58 | 63,29 | 65,50 |

Concatenar racionalização e rótulo na mesma sequência de saída fica **abaixo do fine tuning padrão**
em ANLI e CQA. Eles citam Wiegreffe et al. 2021, Magister et al. 2022 e Ho et al. 2022 como tendo
observado o mesmo.

→ **O ganho depende de onde a saída sai.** No T5 a separação é lógica (prefixos `[label]` /
`[rationale]`); uma cabeça fisicamente separada é a forma extrema da mesma separação. **A ablação
aponta na direção do H2.** E rende previsão testável: cabeças separadas devem superar qualquer
variante que ponha racionalização e rótulo na mesma sequência.

**Tabela 1 — professor menor.** GPT-NeoX 20B em lugar do PaLM 540B ainda supera o fine tuning padrão
(e-SNLI 89,12 vs. 88,38; SVAMP 63,00 vs. 62,63), com ganho **menor**. Licencia professor aberto
local, com perda declarada de parte do efeito.

**Limitations.** Os autores declaram o custo como *training-time overhead* e afirmam que no teste o
desenho multi-tarefa evita o custo, permitindo prever só o rótulo. **A remoção na entrega é
propriedade declarada do método, não adaptação nossa.**

**O que o paper NÃO dá:** nenhum teste em encoder; a Tabela 2 é uma configuração por linha, sem
sementes nem IC; e **nenhum controle com racionalização aleatória ou embaralhada** — quem fecha isso
é o DHRD (embaralhamento) e o Herrewijnen (tokens aleatórios).
