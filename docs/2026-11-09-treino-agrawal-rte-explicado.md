# O treino do Agrawal no RTE, em passos (09/11/2026)

Para o Pedro entender o treino **antes** de existir uma linha de código dele. Nada aqui foi rodado.

**Procedência.** O que vem do paper está marcado com a seção ou a tabela (Agrawal, Ahemad & Sembium 2025, PDF em
`docs/artigos/2025.coling-industry.12-agrawal.pdf`; o Claude releu §4.3, §4.4, §5, Tabela 4 e Tabela 7 em 09/11, nível 2).
O resto é proposta ou conta do Claude e está marcado como tal. Os nomes de modelo e dataset foram conferidos no
HF Hub em 09/11: `google-bert/bert-base-uncased`, `google-t5/t5-base`, `google/bert_uncased_L-2_H-128_A-2`,
`nyu-mll/glue` (config `rte`: 2.490 de treino, 277 de validação).

---

## A ideia numa frase

Treina-se um BERT para classificar (o par implica ou não implica) e, **ao mesmo tempo**, um decoder pendurado
nele aprende a escrever a justificativa que o LLM escreveu. O decoder obriga o BERT a guardar nos seus vetores o que
é preciso para justificar. Na entrega, o decoder vai para o lixo e só o BERT classifica.

## As peças

| Peça | O que é | Tamanho | Vai para a entrega? |
|---|---|---|---|
| Encoder | BERT base (12 camadas, vetor de 768 por token) | 110M | sim |
| Cabeça de classificação | uma camada linear sobre o vetor do `[CLS]` | 768 → 1 | sim |
| Cabeça auxiliar | **só a metade decoder** do T5 base | ~110–120M (conta do Claude) | **não** |
| Professor | quem escreve as justificativas do treino; no paper, Mixtral 8×7B; aqui, o Qwen3.6-35B-A3B | — | não |

Por que o T5 base e não outro decoder? O T5 base também trabalha com vetores de 768. O decoder lê os vetores do BERT
sem precisar de camada de adaptação no meio. (O paper não dá esse motivo; é leitura do Claude.)

---

## Passo 0. Os dados

- RTE: pares (premissa, hipótese) com 2 rótulos, `entailment` e `not_entailment`. 2.490 de treino e 277 de
  validação. **O teste do GLUE não traz rótulo**, então a validação faz o papel de teste.
- As premissas do RTE são mais longas que as do e-SNLI: muitas vezes um parágrafo de notícia, não uma legenda.

## Passo 1. Gerar as justificativas (só para o treino)

- O RTE não traz justificativa. O professor gera uma para cada um dos 2.490 pares de treino, **recebendo o rótulo
  certo** e perguntando "por quê". É o que o paper faz (§4.3, Apêndice C: o prompt recebe o rótulo e pede "Reasoning").
- Aqui seria o Qwen 35B com uma adaptação da variante F (a decidida em 27/10) para 2 rótulos. Tempo previsto: 2.490 pares
  a ~1,6 s/par (medida de hoje no PC), ~1 h 10 min (conta do Claude).
- A validação **não** precisa de justificativa, porque na avaliação o decoder já foi descartado.

## Passo 2. Transformar texto em números

Aqui aparece algo que confunde: **são dois tokenizadores**.

- Entrada do BERT: `[CLS] premissa [SEP] hipótese [SEP]`, com o vocabulário do BERT.
- Alvo do decoder: a justificativa, com o vocabulário **do T5**.

Os dois nunca trocam tokens. A ponte entre eles são os vetores: o decoder lê os 768 números de cada posição do BERT,
não as palavras.

## Passo 3. Uma passada para frente (um lote de 32 pares)

1. O BERT lê o par e devolve **um vetor de 768 por token** (chame de `h`).
2. **Classificação:** o vetor do `[CLS]` passa pela camada linear e vira um número; a sigmoide vira probabilidade de
   `entailment`. Erro medido por entropia cruzada binária: `L_cls`.
3. **Justificativa:** o decoder do T5 olha para todos os vetores `h` (por *cross-attention*, a atenção que lê outra
   sequência) e tenta prever a justificativa **um token por vez**. Em cada posição ele recebe os tokens *verdadeiros*
   anteriores, não os que ele mesmo previu (isso se chama *teacher forcing*). Erro medido por entropia cruzada média
   por token: `L_aux`.
4. Detalhe do §4.4: eles testaram passar ou não o vetor do `[CLS]` para o decoder ("Ignore CLS"). Na Tabela 3 as
   duas formas trocam de lugar conforme o tamanho do dado.

## Passo 4. A perda

```
L_total = L_cls + 0,1 · L_aux        (§4.3; λ = 0,1 "based on our early experiments", sem varredura)
```

O que faz o método funcionar (se funcionar) é o caminho do gradiente de `L_aux`: ele atravessa o decoder e **entra
no BERT**. O BERT é empurrado a manter nos vetores a informação de que o decoder precisa para escrever a justificativa.
O 0,1 deixa a classificação mandar e a justificativa só puxar.

## Passo 5. O aquecimento em duas fases (§4.4)

O decoder do T5 nunca viu vetores do BERT, só do encoder do próprio T5. Se tudo começar junto, a *cross-attention*
lê ruído nas primeiras centenas de passos, e o gradiente dessa bagunça entra no BERT e estraga o pré-treino dele.
Por isso:

- **Fase A:** BERT **congelado**, treina só o decoder, em **50% dos dados**. O decoder aprende a "ler" o BERT.
- **Fase B:** o BERT é liberado com **aquecimento linear nos primeiros 30% do treino**, e nesse trecho a perda é
  **só `L_aux`**.
- **Depois:** liga `L_total`.

O paper deixa três pontos em aberto, e cada um vira decisão no código:
1. "50% dos dados" quer dizer uma passada sobre metade do treino? Ou metade das épocas?
2. "Aquecimento linear do encoder" é a taxa de aprendizado do BERT subindo de 0 até 5e-5?
3. Os 30% contam sobre o treino inteiro ou sobre o que vem depois da Fase A?

## Passo 6. Os hiperparâmetros (Tabela 4) e a conta no RTE

| Item | Valor no paper |
|---|---|
| Lote | 32 |
| Taxa de aprendizado | 5e-5 |
| Épocas | 8 |
| Passos de aquecimento da taxa | 500 |
| Weight decay | 0,001 no decoder, 0 no encoder |
| Adam | ε 1e-8, β1 0,9, β2 0,999 |
| Corte de gradiente | 1,0 |

**A conta que muda tudo no RTE (Claude):** 2.490 / 32 ≈ 78 passos por época; × 8 épocas ≈ **623 passos no total**.
Os 500 passos de aquecimento ocupariam **80% do treino**. A Tabela 4 parece pensada para os conjuntos de 100K do
e-commerce, e o paper não diz se usou a mesma tabela no GLUE. Copiar ao pé da letra no RTE quase não deixa treino com
taxa cheia.

## Passo 7. Avaliação

- Só o BERT + a camada linear. O decoder é descartado.
- O paper mede **ROC-AUC** com média e intervalo de 95% (Tabela 2). No RTE a métrica de costume é **acurácia**.
  Proposta do Claude: as duas.
- O paper não diz quantas sementes. No RTE, pequeno, o resultado de um BERT varia muito de semente para semente
  (conhecimento geral do Claude, sem fonte conferida aqui). Proposta: 10 sementes por braço.

## Passo 8. O que se compara, e o que esperar

- **Braço 1:** BERT sozinho (só `L_cls`, mesmos hiperparâmetros).
- **Braço 2:** BERT + decoder (o método).
- O baseline deles **não é um BERT de GLUE**: é um BERT ajustado para relevância de busca (MS-MARCO), e no RTE deu
  ROC-AUC **0,4754, abaixo do acaso** (Tabela 7). Por isso o +11 pontos deles no RTE quase certamente não se
  repete contra um BERT normal.
- **A replicação responde a uma pergunta:** contra um baseline são, o ganho existe, e de que tamanho? Um nulo bem medido
  também conta (critério do programa: processo, não produto).

## Passo 9. Cabe na RTX 5060?

Conta do Claude, a medir:
- ~230M parâmetros treináveis (BERT + decoder). Com AdamW em fp32, são ~16 bytes por parâmetro (peso, gradiente e
  dois momentos): **~3,7 GB** antes das ativações.
- Com lote 32 e textos longos do RTE, as ativações provavelmente estouram os 8 GB. Saídas: precisão mista (bf16),
  lote de 8 com acumulação de 4 (o mesmo lote efetivo de 32) e corte das sequências (256 tokens, por exemplo).
- O BERT minúsculo (`google/bert_uncased_L-2_H-128_A-2`) **não serve** para o teste na CPU com o decoder do T5 base,
  porque tem vetor de 128 e não de 768. Para o teste de fumaça há duas saídas: uma camada linear 128 → 768 só no
  teste, ou um T5 menor do mesmo tamanho. Ver D6 abaixo.

---

## Decisões antes do código

| # | Decisão | Opções | Decidido |
|---|---|---|---|
| D0 | Professor no RTE | Qwen 35B · Mixtral 8×7B (o do paper) · Claude | **Qwen3.6-35B-A3B** (Pedro, 09/11). Desvio declarado: Mixtral → Qwen, mesma classe (MoE aberto, 35–47B). Claude fora: a Usage Policy proíbe saída como alvo de treino; espera a pergunta à Anthropic |
| D1 | Prompt do professor no RTE | variante F adaptada para 2 rótulos · prompt do Apêndice C do paper | **F adaptada, com uma checada rápida da saída** (Pedro, 09/11). Justificativas do Agrawal como baseline: não publicadas (busca de 09/11) |
| D2 | Aquecimento de 500 passos num treino de ~623 | copiar · proporcional (~10%) · reportar as duas | **as duas: cópia fiel (500) e proporcional** (Pedro, 09/11) |
| D3 | As três ambiguidades da Fase A/B (passo 5) | uma leitura escrita e declarada | **Leitura literal, declarada como interpretação, e pergunta aos autores em paralelo** (Pedro, 09/11). Fase A = uma passada por metade dos pares, só o decoder, BERT congelado, só `L_aux`; Fase B = passos 1–187 (30% de 623), taxa do BERT subindo de 0 a 5e-5, só `L_aux`; Fase C = passos 188–623, `L_cls + 0,1·L_aux`. Se os autores responderem, roda-se também a leitura deles e comparam-se os resultados. Rascunho do e-mail: `docs/2026-11-09-pergunta-autores-agrawal.md` |
| D4 | Métrica | ROC-AUC · acurácia · as duas | **ROC-AUC, Recall e Precision a 0,7 (as do Agrawal, Tabela 7) + acurácia + F1 macro + F1 por classe** (Pedro, 09/11) |
| D5 | Sementes | 3 · 5 · 10 | **5; 10 se a medida da primeira rodada mostrar que é barato** (Pedro, 09/11) |
| D6 | Teste de fumaça na CPU | BERT minúsculo + adaptador · T5 menor | **adaptador 128 → 768 só no teste** (Pedro, 09/11) |

## O que o código vai ter (descrição, sem código)

1. Gerar as justificativas do RTE com o Qwen no PC (reaproveita o `lote.py`).
2. Montar o modelo: BERT + camada linear + decoder do T5, com a cross-attention lendo o BERT.
3. Laço de treino com as três fases e os hiperparâmetros da Tabela 4.
4. Avaliação no dev do RTE, por semente, salvando um CSV por braço.
5. Invariantes: treino e dev sem par em comum; mesma semente reproduz o mesmo número; o braço 1 nunca chama o decoder;
   o modelo salvo para avaliação não contém o decoder.
