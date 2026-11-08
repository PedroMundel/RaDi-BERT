# Riscos do classificador de relevância: medição e correções (27/09)

**Pedido do Pedro (27/09):** *"meça todos os problemas que podem ser causados por esse método pra gente patchear o
melhor possível cada um pra no final termos obras relevantes. Lembrando, o objeto final não é só destilação, mas
oferecer uma base pra área como um todo."*

**Procedência: nível 3.** Os rótulos são vereditos de agentes (F2); as subáreas são uma aproximação por
palavras do pool de termos no título e no abstract. Nenhum número aqui foi conferido por leitura humana.

**Contrato desta medição:** entrada de 797 rótulos da F2 + 28 obras de ajuste do gabarito · custo de 0 token de
agente e alguns minutos de CPU · não tocou a tabela-mestra nem a metade de teste do gabarito (dela, só se contou em
que grupo cada obra está) · saída: cada risco com um número, ou com o motivo de não ter.

**Como os números foram feitos:** regressão logística sobre os vetores SPECTER2; validação cruzada estratificada
de 5 dobras, repetida com 5 sementes. Toda métrica é **ponderada** pelo inverso da chance de a obra ter sido sorteada
na F2 (tamanho do grupo ÷ amostra), para valer para as 11.544 obras e não só para a amostra. Scripts:
`scripts/screening/classificador/diag_riscos.py` e `diag_patches.py`; números brutos em `resultados*.json`.

## 1. Resultado geral

| Ordem | Lendo 10% da lista, acha | Lendo 25%, acha | Para achar 95%, lê (K95) | Precisão média (AP) |
|---|---|---|---|---|
| **Classificador (regressão logística)** | **41%** | **72%** | **67% (± 5)** | **0,50** |
| kNN (15 vizinhos) | 30% | 61% | 78% | 0,32 |
| Palavra núcleo no título | 13% | 34% | 94% | 0,16 |
| Ordem pela F1 | 9% | 29% | 93% | 0,15 |
| Aleatória | 11% | 28% | 92% | 0,15 |

**Leitura:** o classificador é **muito melhor** que qualquer linha de base: acha 2,5 vezes mais relevantes que o
acaso nos primeiros 25%. Mas **não cumpre o critério proposto na D3** (achar 95% lendo até 25%). As últimas
relevantes estão espalhadas pela lista: para passar de 72% para 95% é preciso ler quase tudo. As §2 e §3 explicam
por que isso acontece, e a §4 propõe trocar o critério.

## 2. Registro de riscos

| # | Risco | Como medi | Número | Gravidade | Correção proposta (efeito medido, quando houver) |
|---|---|---|---|---|---|
| **R1** | **Poucos positivos:** 55 relevantes para aprender 768 dimensões | curva de aprendizado (treino com 25/50/75/100% dos rótulos) | K95: 81% -> 76% -> 76% -> **67%**; **ainda caindo** com 100% | **alta** | **mais rótulos, escolhidos a dedo** (aprendizado ativo, §4.2); a curva diz que rótulo novo ainda compra melhoria |
| **R2** | **Validação frágil:** o peso concentra a medida em poucas obras | tamanho efetivo dos positivos ponderados | **n efetivo = 20**; 11 obras dos grupos 2 e 5 carregam **69%** do peso | **alta** | rótulos novos concentrados nos grupos 2 e 5; relatar sempre o intervalo, não só a média |
| **R3** | **Ruído de rótulo:** o classificador aprende os erros dos agentes | trocar 5/10/20% dos rótulos de treino ao acaso; tirar as 13 discordâncias da dupla | 5% trocados: K95 67% -> 76%; 20%: -> 82%. Sem as discordâncias: 66% | **alta** | a sua auditoria dos 30 (D2) mede a taxa real de erro; se passar de 5%, dupla leitura em todos os positivos (~212 obras, ~1,6 M tokens) |
| **R4** | **Viés de amostragem:** a F2 superamostrou grupos pequenos | K95 sem peso × com peso | sem peso: **56%**; com peso: 67%. Sem o peso, a validação seria **11 pontos otimista** | média (já corrigido) | peso sempre ligado; já está no script |
| **R5** | **Cobertura desigual por subárea — o risco central para "base da área toda"** | acerto nos primeiros 25%, por subárea | compressão **96%** (18 rel.) · serving **98%** (3) · adaptação **79%** (5) · edge **75%** (33) · **hardware 56%** (20) · dado/confiança 76% (3) · **ferramentas: 0 relevantes rotuladas** · 8 relevantes sem subárea | **alta** | (a) **cota por subárea** na leitura: ler o topo de cada subárea, não só o topo geral; (b) conjunto LR + kNN: hardware 56% -> **60%**, adaptação 79% -> **96%**, compressão 96% -> 95%; (c) ferramentas não vêm do classificador: vêm da filha `ferramentas` (⟨rev-29⟩), porque não são survey |
| **R6** | **Gabarito concentrado:** ele puxa o modelo para um assunto só | grupo de cada obra do gabarito | ajuste: **21/28 no grupo 2**; teste: **23/29 no grupo 2**. As 28 de ajuste como positivos melhoram o K95 (76% -> 67%), mas empurram para compressão e serving | **alta** | **revisar o gabarito por subárea antes do teste final** (você já pediu a revisão em 24/09); medir a perda final **por subárea**, não só no total |
| **R7** | **Survey × paper primário:** o vetor mede o assunto, não o tipo de obra | composição dos primeiros 25% | **32% do topo é "não é survey"**, 23% é fora por outro motivo, 33% relevante, 12% dúvida. 11 das 55 relevantes não têm palavra de tipo no título | média (custo) | multiplicar a nota por 0,5 quando não há palavra de tipo: AP 0,50 -> **0,58**, acerto em 25% 72% -> 71%. Com 0,25 perde demais (-> 60%) |
| **R8** | **Obras sem abstract:** vetor feito só do título | reavaliar as rotuladas com vetor só do título | AP 0,50 -> **0,33**; acerto em 25% 72% -> **50%**. São **1.923 no pool (17%)** | média | fila separada: primeiro a rota de PDF aberto (M6); o que continuar sem abstract ganha corte próprio e vai para a lista `sem acesso` |
| **R9** | **Recência desigual** | acerto em 25%, por período | até 2022: 69% (6 rel.) · **2023–24: 54%** (15) · 2025–26: 86% (34) | média | cota por período junto com a de subárea; olhar de perto o que o 2023–24 perde |
| **R10** | **Obras quase iguais em dobras diferentes** inflam a validação | pares com cosseno > 0,97 entre rotuladas; validação agrupada | 96 pares. **Não são a mesma obra** (0 com o mesmo título): são grupos de tema (câncer cervical, blockchain leve). Validação agrupada: K95 67% -> 70%; acerto em 25% 72% -> 71% | baixa | validação agrupada passa a ser a oficial (custa ~2 pontos de otimismo a menos) |
| **R11** | **Laço de confirmação:** os agentes só leem o topo, e o que ficou embaixo nunca é visto | não mensurável sem ler abaixo do corte | — | alta (invisível) | **amostra de controle** sorteada abaixo do corte: 0 relevantes em 100 -> menos de 3% de relevantes lá embaixo (95%); ~0,8 M tokens |
| **R12** | **Concentração no topo** | grupo das obras nos primeiros 25% do pool (nota diagnóstica) | **71% do topo é do grupo 2** (2.042 de 2.886); nenhum grupo sem rótulo no topo | média | mesma correção de R5 (cota por subárea) |
| **R13** | **O alvo muda o que a nota significa (D1)** | ordenar por P1 e medir contra P2 | a ordem por "relevante" acha só **52%** das "relevante + dúvida" nos primeiros 25%. Treinado em P2: K95 71%, AP 0,63 | média | decidir a D1 sabendo que as dúvidas (c) são **outro assunto** (aplicação específica), não relevantes mal classificadas |
| **R14** | **Regras do método que não aparecem no assunto** (§1.2.1 c, §3.4) | indireto: R7 e R13 | ver R7 e R13 | média | as regras continuam com o agente 3; o classificador só **ordena** |

## 3. A causa comum

Três números explicam quase tudo: **55 relevantes, n efetivo de 20 e 71% do topo no grupo 2.** O classificador
aprendeu bem o "centro" da área, que é compressão e serving de LLM, onde está o gabarito. Ele acha pior o que
fica na borda: hardware, edge, adaptação, e os surveys de 2023–24. Para uma base da **área toda**, esse é o
problema que importa. Perder 30% das relevantes do centro custa pouco, porque sobram centenas iguais. Perder a
subárea de hardware inteira deixa um buraco no mapa.

## 4. O que muda no plano (propostas; decisões na §5)

### 4.1 Trocar o critério de sucesso: de "95% de tudo" para "cobertura de cada subárea"

O alvo final é ~50 obras que cubram a área, não as ~1.400 relevantes. Proposta:
- **(i)** cada subárea com pelo menos **N relevantes encontradas** (proposta N = 5, o que um mapa por divisão pede);
- **(ii)** a amostra de controle abaixo do corte mostra menos de 3% de relevantes (R11);
- **(iii)** a perda no gabarito revisado é medida por subárea (R6).

O K95 global continua sendo relatado, mas deixa de decidir.

### 4.2 Aprendizado ativo: o classificador e os agentes em rodadas

Em vez de treinar uma vez e mandar os agentes lerem 2.300 obras, cada rodada funciona assim:
1. O classificador ordena o pool.
2. Os agentes leem **~200 obras** escolhidas de três faixas: **o topo de cada subárea** (cota, R5/R12), **a faixa de
   incerteza** (nota perto do corte, onde um rótulo novo ensina mais, R1) e **uma amostra de controle** abaixo do
   corte (R11).
3. Os vereditos viram rótulos novos, e o classificador é retreinado.

**Contrato de cada rodada:** entram ~200 obras; saem ~200 rótulos, dos quais ~60–100 relevantes pela precisão
medida no topo; custam ~1,5 M tokens (cerca de meia janela de limite, com ESTADO.md e lotes idempotentes). **Para
quando** (i) e (ii) da §4.1 forem cumpridos, ou quando uma rodada não mudar a cobertura de nenhuma subárea.

### 4.3 Correções que entram de qualquer jeito (medidas, baratas)

- Peso por probabilidade de inclusão (R4): já está.
- Validação agrupada como oficial (R10).
- Nota × 0,5 para obra sem palavra de tipo (R7): AP de 0,50 para 0,58.
- Fila separada para obra sem abstract (R8).

## 5. Decisões do Pedro

- **R-D1. Critério de sucesso:** trocar "95% de tudo em 25% da lista" (D3 do plano) por **cobertura por subárea +
  controle abaixo do corte** (§4.1)? Se sim, qual o N por subárea (proposta: 5)?
- **R-D2. Aprendizado ativo em rodadas de ~200 (§4.2)** em vez de uma leitura única de ~2.300?
- **R-D3. Modelo:** regressão logística sozinha (melhor K95 global) ou **LR + kNN** (melhor nas subáreas de borda:
  adaptação 79% -> 96%, hardware 56% -> 60%)?
- **R-D4. Penalidade de 0,5** para obra sem palavra de tipo no título?
- **R-D5. Revisão do gabarito por subárea antes do teste final** (R6): fazer agora?
- Seguem abertas do plano: **D1** (alvo P1/P2/P3; ver R13), **D2** (auditoria antes de treinar; ver R3, que agora
  tem número: 5% de rótulo errado custam ~8 pontos de K95) e **D5** (a etapa C3 de ~1.100 para ~50).

## 6. Limites desta medição

- As subáreas vêm de palavras do pool, não de divisões declaradas por surveys. São uma aproximação, e há 8
  relevantes que nenhuma palavra pegou.
- Com n efetivo de 20, as diferenças de 2–3 pontos entre variantes estão dentro do ruído (desvio-padrão do K95 é
  de 4–7 pontos). Só as diferenças grandes (R1, R3, R5, R7, R8) são firmes.
- A nota do pool em E13 é **diagnóstica**: não é a lista oficial e não foi usada para nada.
