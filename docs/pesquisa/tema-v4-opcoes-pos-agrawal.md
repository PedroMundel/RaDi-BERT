# Tema v4 — opções que ficam no mesmo eixo sem colidir com o Agrawal

> ⚠ **FEITO SOB A RÉGUA ERRADA (ver CLAUDE.md, critério do programa, 11/09).** Este documento ranqueia
> opções por *risco de novidade*. O professor declarou que a Residência avalia processo e especialização,
> não inovação. **Os fatos (leituras, custos, lacunas) continuam válidos; o ranking e a pergunta-guia
> não.** A tabela precisa ser refeita com "qual opção ensina mais da especialização?" — depois que o
> Pedro nomear a especialização. Reproduzir o Agrawal fielmente, descartado aqui como "ocupado", volta a
> ser passo legítimo do ciclo. **Correção adicional (10/09, tarde):** o apoio empírico "+1,4% → +6%"
> para a hipótese de comprimento foi retirado (baseline de GLUE quebrado; ver notas do Agrawal), e o
> Agrawal **rodou BR (português)** com resultado não-significante — pt-BR é cenário, não contribuição.

**Data:** 10/09/2026 · **Autor:** Claude · **A decisão é do Pedro.**
Contexto: `docs/artigos/notas-agrawal-coling2025.md` e a pendência 5 do `tema-v3`.

## PROCEDÊNCIA

- **Nível 2 (Claude leu a fonte):** Agrawal (COLING 2025), DHRD, Distilling Step-by-Step,
  Herrewijnen, Li et al.
- **Nível 3 (só resultado de busca — NÃO citar, NÃO decidir por cima):** todos os arXiv IDs
  nomeados na seção "risco de novidade" de cada opção. Foram levantados para **medir lotação do
  espaço**, não para afirmar conteúdo. Antes de fechar qualquer opção, o candidato escolhido exige
  leitura nível 2 dos vizinhos dela. **É exatamente a lição do Agrawal.**

---

## O que o Agrawal ocupa — e os cinco eixos que sobram

Ele fixou **uma célula**, não o espaço:

| Eixo | Onde o Agrawal está | Dá para mover? |
|---|---|---|
| Arquitetura do estudante | cross-encoder (par entra junto) | **sim** → bi-encoder |
| Cabeça auxiliar | decoder T5 gerando racionalização | não (é o mecanismo, está ocupado) |
| **Métrica** | **ROC-AUC / acurácia** | **sim** → calibração, abstenção |
| **Regime de teste** | **dentro da distribuição** | **sim** → deslocamento, atalho |
| **Tamanho do texto** | **query + título de produto (~12 tokens)** | **sim** → documento longo |

## A reformulação que faz tudo funcionar

> **O Agrawal respondeu "funciona?". Ninguém perguntou "o que a racionalização compra além de
> acurácia?".**

Nessa moldura o Agrawal **deixa de ser concorrente e vira fundação**: você cita, reimplementa como
baseline, e pergunta outra coisa em cima. Três vantagens concretas:

1. **Some a colisão de novidade.** Você não alega mecanismo novo — alega variável dependente nova.
2. **Você sai do terreno que rejeitou em 10/09** ("reanálise de resultado publicado como objeto de
   pesquisa"). Não se julga a análise deles; faz-se outra pergunta.
3. **O risco nº 1 do tema v3 morre.** A capacidade latente de um encoder de 110M deixa de ser aposta:
   o Agrawal já mostrou +6% em GLUE nesse tamanho. Você parte de um efeito conhecido.

---

## As quatro opções

### A — Mover a MÉTRICA: o classificador sabe quando não sabe?

**Pergunta:** supervisão por racionalização melhora a **calibração** e a **abstenção** de um encoder,
ou só o ranqueamento?

Arquitetura idêntica à do Agrawal. O que muda é o que se mede: **ECE, Brier, e curva risco-cobertura
(AURC)** em vez de acurácia. Braços: sem cabeça · cabeça com racionalização alinhada · cabeça com
racionalização embaralhada (o controle que ninguém rodou nesse canal).

**Por que está aberto:** nenhum dos quatro papers lidos em nível 2 reporta calibração. O Agrawal
reporta **ROC-AUC, que é métrica de ranqueamento e é cega a calibração** — um modelo pode ganhar
ROC-AUC e piorar a confiança. DHRD, Distilling e Herrewijnen reportam acurácia.

**História para empregador:** triagem automática em volume. A pergunta que toda equipe de produção
tem é *"quando esse modelo passa o caso para um humano?"* — porque o custo de um erro automático não
é igual ao custo de uma revisão. É a pergunta mais concretamente cara desta lista.

**Custo:** o mais baixo dos quatro. As rodadas são as mesmas; o que muda são as métricas e a avaliação
seletiva. Cabe folgado em 8GB.

**Risco de novidade:** médio. Existe destilação por **soft label** para calibração — o achado nível 3
mais próximo é uma queda de ECE de 0,408 para 0,228 destilando probabilidades de LLM para BERT. **Isso
não é racionalização em texto livre**, e a distinção é a sua tese; mas exige leitura nível 2 antes de
fechar. Também existe *Self-Filtered Distillation*, que trata racionalização como sinal de confiança
[nível 3].

---

### B — Mover o REGIME DE TESTE: racionalização protege contra atalho?

**Pergunta:** no canal de **saída** de um encoder, a racionalização protege contra correlação espúria —
e ganha de texto aleatório quando protege?

**Por que esta pergunta já vem meio pronta:** o Herrewijnen (que você tem em nível 2) tem **um único
resultado positivo sobrevivente**. No canal de atenção, tokens aleatórios empatam com racionalização
humana em quase tudo — **exceto contra correlação espúria**, onde a racionalização humana vence, e λ
maior reduz a dependência do atalho. Isso é uma **previsão registrada por outro autor** para o canal
que o Agrawal usa e nunca testou. O código do Herrewijnen é aberto
(`github.com/UtrechtUniversity/attention-regularisation-with-rationales`).

**História para empregador:** o modelo aprendeu a pista errada e quebra quando os dados mudam. Todo
mundo que colocou classificador em produção viveu isso.

**Custo:** baixo a médio. Precisa de um conjunto com atalho injetado (o do Herrewijnen, reaproveitado)
ou de um par consagrado de deslocamento.

**Risco de novidade:** médio. Debiasing por destilação é campo cheio, e há trabalho sobre correlação
espúria em destilação de CoT [nível 3, arXiv 2509.05602] — mas em SLM gerador, não em encoder com
cabeça auxiliar e controle aleatório.

---

### C — Mover a ARQUITETURA: bi-encoder em vez de cross-encoder

**Pergunta:** dá para injetar racionalização num **bi-encoder**, onde os dois textos nunca se veem?

O Agrawal é o estágio de **reranqueamento**. O estágio de **recuperação** é bi-encoder, e lá a
racionalização teria que caber num vetor único por texto, sem atenção cruzada. É arquiteturalmente
diferente de verdade.

**História para empregador:** a mais forte da lista — é o retriever de qualquer pipeline de RAG.

**Custo: ALTO.** Treino contrastivo é faminto por batch grande, e 8GB é restrição real. Precisa de
corpus e índice.

**Risco de novidade: ALTO e subindo.** A busca já devolveu dois trabalhos de 2026 destilando sinal de
LLM para retriever denso [nível 3: arXiv 2604.22722 "Aligning Dense Retrievers with LLM Utility via
Distillation"; arXiv 2604.23336 "Efficient Rationale-based Retrieval: On-policy Distillation"]. Área
quente, com grupos bem financiados. **Não recomendo para primeira pesquisa em 8GB.**

---

### D — Mover o TAMANHO DO TEXTO: documento longo

**Pergunta:** o efeito sobrevive quando o texto é um documento e não uma frase?

**Por que está aberto:** o Herrewijnen declara como limitação que os datasets dele são de **texto
curto** e convida explicitamente trabalho futuro em texto longo. O Agrawal usa query + título de
produto — uma dúzia de tokens. Existe encoder para isso: ModernBERT, 8192 de contexto nativo
[arXiv 2412.13663, nível 3].

**História para empregador:** triagem de documento — contrato, laudo, relatório.

**Custo: médio-alto.** ModernBERT em 8k numa 5060 de 8GB é apertado, e resolve-se com sequência menor
e acumulação de gradiente — mas é risco de engenharia somado ao risco de pesquisa.

**Risco extra que as outras não têm:** o que um LLM racionaliza sobre um documento de 5 mil tokens é
um objeto mal definido. Multiplica partes móveis.

---

## Comparação

| Critério | **A — Calibração/abstenção** | **B — Atalho/deslocamento** | C — Bi-encoder | D — Documento longo |
|---|---|---|---|---|
| Colide com o Agrawal? | não | não | não | não |
| Cabe em 8GB / 3–4 meses | **sim, folgado** | sim | **não** | apertado |
| Risco de novidade | médio | médio | **alto** | médio-baixo |
| Partes móveis novas | **mínimas** | poucas | muitas | muitas |
| Grita para empregador | **muito forte** (quando escalar para humano) | forte (quebra em produção) | **muito forte** (RAG) | forte (triagem) |
| Herda das suas leituras | DHRD (controle), Agrawal (arquitetura) | **Herrewijnen (previsão pronta)** | pouco | Herrewijnen (limitação declarada) |
| Resultado nulo é publicável? | **sim** — "não melhora calibração" é achado útil | sim | não | parcialmente |
| Cai no que você rejeitou? | não | não | não | não |

### Recomendação — ⭐ **A, com B acoplada**

**A é a recomendação isolada** por três motivos: é a mais barata em GPU, tem a menor quantidade de
partes móveis novas (a arquitetura já está publicada e descrita em detalhe, inclusive o warmup do
decoder), e é a que tem a história mais concreta para empregador.

**Mas A e B são a mesma tese**, e juntas ficam mais fortes do que separadas:

> **"O que a racionalização de LLM compra num encoder, além de acurácia?"**
> Dois eixos: **confiança** (o modelo sabe quando não sabe?) e **deslocamento** (o modelo aguenta
> quando os dados mudam?). Com o controle de racionalização embaralhada nos dois, que é o baseline
> que o Agrawal não rodou.

Isso é um trabalho, não dois. As rodadas de treino são as mesmas; o que muda é o conjunto de
avaliação e as métricas. E fecha a pendência 10 do tema v3 (fora de domínio obrigatório) de brinde,
porque o eixo B **é** a avaliação fora de domínio.

**C fica de fora** por custo e lotação. **D fica estacionada** como extensão, se sobrar tempo — é a
limitação declarada do Herrewijnen e continua valendo.

---

## O que fazer antes de fechar (não pule — é a lição do Agrawal)

1. **Ler em nível 2** os dois vizinhos mais próximos da opção escolhida. Para A: o trabalho de
   soft-label para calibração e o *Self-Filtered Distillation*. Para B: o de correlação espúria em
   destilação de CoT. **Ler o método, não o resumo.**
2. **Confirmar que o Agrawal realmente não reporta calibração** — está confirmado na leitura das
   tabelas 1, 2 e da §5.2, mas vale reconferir o apêndice antes de escrever a alegação.
3. Só então mexer no `tema-v3` e escrever o v4.

## Fontes de nível 3 citadas (para verificar depois, nunca para citar agora)

- arXiv 2604.22722 · arXiv 2604.23336 (bi-encoder / retriever)
- arXiv 2509.05602 (correlação espúria em destilação de CoT)
- arXiv 2412.13663 (ModernBERT)
- *Self-Filtered Distillation* e o trabalho de soft-label→BERT com queda de ECE (IDs não capturados)
