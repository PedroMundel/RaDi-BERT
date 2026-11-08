# Seção para o entregável — o que o DHRD autoriza na transferência para encoder

Destino: seção nova do resumo `DHRD Resumo.pdf`. Reúne as extrações do paper que **licenciam** levar
o mecanismo de cabeça auxiliar descartada para um encoder bidirecional — e as que **não** licenciam.

## ⚠ Procedência desta seção

| Item | Quem leu | Nível |
|---|---|---|
| Toda a base do resumo — mecanismo, ablação, eficiência, e em especial o item 1 do trabalho relacionado (via bidirecional considerada e rejeitada) | **Pedro**, lendo o paper | **1 — citável** |
| Números das Tabelas 1 e 2, localização de seções, trechos em inglês e as três correções abaixo | Claude, extraindo o PDF v2 (arXiv:2509.21487v2) em 10/09/2026 | **2 — conferir na fonte antes de assinar** |

Tudo marcado **[C]** é acréscimo do Claude. O resto já é seu.

**[C] Venue:** citar como **NeurIPS 2025 Efficient Reasoning Workshop** — é o que diz o campo
*Comments* do arXiv, preenchido pelos autores. A linha "39th Conference on NeurIPS" no rodapé do PDF
é só o texto padrão do estilo LaTeX e sai em qualquer submissão; não é evidência de venue.

---

## 1. A licença central: cabeça auxiliar descartada funciona, e o ganho é CONTEÚDO

Isto é o que você já extraiu, e é a alegação que o paper isola melhor:

> O ganho do DHRD decorre do alinhamento lógico da tripla [entrada — justificativa — rótulo], e não
> de uma simples regularização do modelo de linguagem.

**[C] Onde:** §4.3, Tabela 2 (Llama-3.1-8B e Llama-3.2-3B, α=β=1). A frase deles atribui o ganho ao
alinhamento *"rather than generic LM regularization"*.

| Configuração | Llama-3.1-8B | Llama-3.2-3B |
|---|---|---|
| Alinhado (ConsistentReasoningLabel) | 87,52 (referência) | 81,57 (referência) |
| Sem justificativa (OnlyLabel) | −1,75% | −3,84% |
| Justificativa de outro exemplo (ShuffleReasoning) | −5,70% | −20,24% |
| Tudo desalinhado (ShuffleReasoningLabel) | −48,48% | −45,27% |

**O que autoriza:** a ordem **alinhado > nenhum > errado** é o que separa conhecimento de
regularização. Se o efeito fosse só "ter um objetivo auxiliar qualquer", justificativa errada
empataria com nenhuma justificativa — e ela é **muito pior**. É a evidência de que existe conteúdo
sendo transferido, e conteúdo é o que se pode esperar transferir para outra arquitetura.

**[C] Correção de precisão:** ShuffleReasoning **não é justificativa aleatória** — é a justificativa
**de outro exemplo** do próprio dataset (texto coerente, alinhamento errado). A distinção importa
porque "aleatório" é o nome do outro controle, o de tokens aleatórios do Herrewijnen, que mede coisa
diferente (ruído como regularização). Vale trocar no resumo para "justificativa de outro exemplo".

## 2. O espaço negativo — por que ninguém foi para o encoder

Esta é a peça mais forte da seção, e ela é **sua**: você registrou que o DHRD considerou a via
bidirecional (Gemma Encoder: atenção bidirecional + pooling + MLP) e a **rejeitou** para evitar
vazamento de token futuro e casar com o pré-treino autorregressivo.

**[C] Onde:** §2, primeiro parágrafo. E a razão tem **duas metades** — *"to prevent future-token
leakage and match autoregressive pretraining"*. Nenhuma das duas sobrevive num encoder:

| Metade da razão deles | Por que não se aplica ao encoder |
|---|---|
| Evitar vazamento de token futuro | **[C]** A Eq. (1) põe `xᵢ`, `rᵢ` e `yᵢ` na **mesma sequência**, e a cabeça de classificação faz pooling do último token real da entrada. Com atenção bidirecional, os tokens de `xᵢ` enxergariam a justificativa e o rótulo. O medo é legítimo **no desenho deles**. No desenho do tema, a justificativa sai por cabeça separada e **nunca entra na sequência do encoder** — não há o que vazar. |
| Casar com o pré-treino autorregressivo | Um encoder **é** pré-treinado bidirecionalmente. Não há pré-treino autorregressivo a respeitar. |

**O que autoriza — e é o argumento de posicionamento do trabalho:** o DHRD é o paper que **documenta
a razão declarada** para o buraco no encoder existir. Mostrar que a razão não se aplica é diferente,
e mais forte, do que dizer "ninguém fez ainda". Sai de *preencher lacuna* e vira *remover a
justificativa da lacuna*.

→ Corolário útil: **o DHRD ser decoder-only não é o que enfraquece a relevância dele para o tema —
é o que a cria.** Se ele fosse sobre encoders, este argumento não existiria.

## 3. A escolha de tarefa pode zerar o efeito — e o paper mostra onde

Este item não licencia o desenho; ele diz **se o desenho consegue medir alguma coisa**. É a única
parte do paper que fala sobre isso, e por isso entra.

Você registrou: "tarefas que dependem menos do raciocínio passo a passo apresentaram variações mais
discretas". **[C]** Os números por trás, §4.1:

- **CB: +8,7%** relativo nos **dois** modelos de 8B (Llama 81,9 → 89,0; Qwen 83,5 → 90,8 — são +7,1
  e +7,3 **pontos**; os 8,7% são relativos, não pontos).
- **COPA: +23,5%** relativo no Llama-3.2-3B (72,2 → 89,2).
- Melhorias consistentes em RTE, MultiRC e BoolQ.
- **WiC e WSC estáveis** — explicação deles: sentido de palavra e correferência são
  *"less reliant on multi-step verbalization"*.

**Por que isso é pré-condição e não detalhe de setup:** WiC e WSC **estáveis** é evidência empírica
de que existe escolha de tarefa capaz de **anular o efeito**. O desenho do tema é cinco condições ×
~5 sementes; com uma tarefa do tipo errado, essas 25–50 rodadas medem ruído, e o resultado nulo não
diz nada sobre a hipótese — diz que a tarefa não tinha raciocínio para transferir. É risco que se
paga **antes** de rodar, não depois.

O mecanismo por trás: racionalização ajuda onde existe um passo de inferência que **não está na
superfície do texto**; onde a decisão é reconhecimento de padrão, a justificativa só aponta para uma
palavra que o modelo já vê, e não sobra o que a cabeça auxiliar ensine.

**E é o que dá base à escolha de tarefa — sem fazer a escolha.** O critério que sai daqui é:
a tarefa precisa ser classificação (que encoder resolve) **e** exigir raciocínio. Inferência textual
satisfaz os dois, o que a torna candidata forte. **A tarefa e o dataset seguem indefinidos** — é a
pendência 7 do `docs/pesquisa/tema-v3-racionalizacao-encoder.md`, e a decisão é do Pedro. O que este item entrega é
o critério com fonte, não o veredito.

**[C] Nota de trilha:** isto era **hipótese do Claude** (registrada em
`docs/artigos/notas-distilling-step-by-step.md` ao cruzar Distilling com Herrewijnen). O DHRD é o que
a converteu em resultado publicado. Vale saber, porque muda o que se pode escrever: passou de "nossa
conjectura" para "confirmado pelos autores do trabalho vizinho".

## 4. A régua metodológica que o tema bate barato

**[C]** §4 e Apêndice A: **rodada única por configuração, sem intervalo de confiança, declaradamente
por restrição de computação**, em backbones de 3B a 8B.

**O que autoriza:** com encoder de ~110M, uma rodada leva minutos. Cinco condições × ~5 sementes ×
1–2 tarefas cabe na RTX 5060. **A restrição de hardware viabiliza o desenho que o time do Google não
pôde pagar** — eles tiveram escala e uma rodada por configuração; o tema tem grade completa com
estatística. É contribuição metodológica declarável, e é sobre o vizinho mais próximo.

---

## O que o DHRD NÃO autoriza — declarar junto

### 5.1 [C] Correção: "maior impacto em modelos menores" não se sustenta

Tabela 1, conferida na ordem de leitura da página 4:

| Modelo | Baseline (pooled) | DHRD | Relativo |
|---|---|---|---|
| Gemini 2.5 Flash (professor, CoT zero-shot) | — | 86,40 | — |
| Llama-3.1-8B | 86,29 | **87,52** | +1,43% |
| Qwen-3-8B | 86,09 | **87,23** | +1,32% |
| Llama-3.2-3B | 77,34 | **81,57** | **+5,47%** |
| Qwen-3-4B | 84,50 | 85,05 | **+0,65%** |

O **menor** ganho de todos é de um modelo pequeno (Qwen-3-4B, +0,65%), e o maior também
(Llama-3.2-3B, +5,47%). Não há tendência por tamanho com quatro pontos. **O paper não afirma isso** —
diz apenas que o Llama-3.2-3B teve o maior ganho relativo. Sugestão de troca no resumo: *"o maior
ganho relativo foi do Llama-3.2-3B (+5,47%), sem tendência clara por tamanho"*.

**E a explicação alternativa que isso abre importa para o tema:** o Llama-3.2-3B tem o **baseline mais
fraco** de todos (77,34 contra 84,50–86,29). O ganho pode ser função de **espaço para melhorar**, não
de tamanho. As duas leituras fazem previsões **opostas** para um encoder de 110M — se é espaço, um
encoder com baseline fraco pode ganhar muito; se é capacidade latente de raciocínio (§5.2), pode
ganhar nada. **Quatro pontos não separam as duas**, e o tema pode separar.

### 5.2 A premissa da capacidade latente

A motivação declarada do paper é que o pooling *subutiliza a capacidade de raciocínio latente
adquirida no pré-treino* — como você registrou na introdução do resumo. **[C]** O mecanismo assume
que **a capacidade já existe** e o treino só a traz à tona, em modelos de 3B a 8B.

Um encoder de 110M provavelmente não tem essa capacidade. Se não tiver, a racionalização teria que
**ensinar** em vez de **revelar** — muito mais difícil, com ordens de magnitude menos parâmetros. É o
risco que questiona a **premissa** do tema, não o desenho. Mitigação a considerar: encoder maior e
mais moderno (DeBERTa-v3-large, ModernBERT) em vez de BERT-base.

### 5.3 [C] A cabeça auxiliar deles é de graça; a do tema não é

O DHRD **reaproveita a cabeça de LM do próprio modelo base** — já pré-treinada, já sabe gerar (você
registrou isso no método). Um encoder não tem cabeça de geração sequencial para reaproveitar: a MLM
do BERT não é geração autorregressiva. **A cabeça auxiliar do tema nasce inicializada do zero.**

Isso é confundidor, não só custo: se o braço de geração render pouco, há duas explicações opostas —
racionalização não transfere para encoder (achado sobre o tema), ou a cabeça nova era fraca demais
para dar gradiente útil (achado sobre a implementação). O braço de regressão para embedding **não
sofre disso**, então uma assimetria entre os dois canais pode ser artefato de inicialização.

### 5.4 O que mais fica fora

- **Nenhum teste em encoder, língua fora do inglês, ou domínio fora do SuperGLUE.** Eles declaram
  que generalização para outras línguas, modalidades, domínios e **arquiteturas** segue não testada.
  É literalmente o espaço do tema — e é limitação declarada por eles, que é a forma mais defensável
  de justificar um trabalho.
- **Sem controle de tokens aleatórios.** A ablação deles corrompe o **alinhamento**, não a
  **informatividade**. Quem cobre isso é o Herrewijnen, e é por isso que o controle aleatório é
  obrigatório no desenho do tema.
- **Sem comparação por orçamento contra compressão de CoT** (HiddenCoT, C3oT, CCoT) — eles declaram.

### 5.5 [C] Correção menor de fato, sem seção própria

α=β=1 é o ótimo para **três** modelos — Llama-3.1-8B, Qwen-3-8B **e Llama-3.2-3B**; o resumo diz "os
8B" e deixa o 3B de fora. Só o Qwen-3-4B prefere β=0,5. (A consequência de desenho — sensibilidade ao
peso da perda auxiliar — já está registrada no `docs/pesquisa/tema-v3-racionalizacao-encoder.md`, na seção de custo
do desenho mesclado; não se repete aqui.)

## Uma frase para fechar a seção

O DHRD prova que uma cabeça de raciocínio supervisionada por justificativa de LLM, **desligada na
inferência**, deixa conhecimento na representação — e que o ganho é conteúdo, não regularização. E
por ser decoder-only, é também o paper que **declara a razão** para ninguém ter feito isso num encoder
bidirecional: razão que, no desenho de cabeças fisicamente separadas, deixa de existir nas suas duas
metades. O que ele não entrega é a garantia de que um encoder de 110M tenha raciocínio latente para
revelar — e essa é a pergunta, não o pressuposto.
