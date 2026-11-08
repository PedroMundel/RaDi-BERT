# Notas de leitura — Herrewijnen et al., EACL 2026

**Referência:** Herrewijnen, E.; Nguyen, D.; Bex, F.; Gatt, A. **"BERT, are you paying attention?
Attention regularisation with human-annotated rationales"**. Proceedings of EACL 2026, Volume 1:
Long Papers, pp. 720–751. https://aclanthology.org/2026.eacl-long.31
Instituições: Utrecht University + National Police Lab AI (polícia holandesa).
**Código:** github.com/UtrechtUniversity/attention-regularisation-with-rationales
⚠ **Procedência: quem leu foi o Claude, não o Pedro.** PDF integral baixado da ACL Anthology e
extraído em 10/09/2026 — leitura completa, não só resumo. Estas notas são leitura de terceiro:
servem para decidir se vale a pena ler, e para orientar a leitura quando o Pedro a fizer. **Não
substituem a leitura dele**, e nenhuma frase daqui deve ir para um texto assinado por ele sem que
tenha lido o original.

## O mecanismo estudado

Regularização de atenção = duas perdas somadas com peso λ:
`L = Lc + λ·Lr`, onde `Lc` é a perda de classificação (predito vs. rótulo humano) e `Lr` mede o
alinhamento entre o padrão de atenção do modelo (`ap`) e um padrão de referência (`ah`).

Racionalização humana é **binária** (token faz parte ou não); atenção é **distribuição de
probabilidade**. Por isso normalizam ou aplicam softmax sobre os valores binários para obter `ah`.
Nota deles: em textos longos, os valores por token ficam muito pequenos.

Regularizam a atenção do token `[CLS]`, seguindo trabalho anterior. Não há consenso na literatura
sobre quais camadas e cabeças regularizar.

Funções de perda `Lr` revisadas: erro quadrático e absoluto (MSE, SSE, MAE), divergência KL, Order
Loss (Joshi et al. 2022), Attention Mass (adaptado de Pruthi et al. 2020).

## Mapeamento no framework do coordenador

- **Objeto:** o procedimento de regularização de atenção (procedimento, não produto)
- **Propriedade:** efeitos sobre desempenho, robustez, sensibilidade a correlação espúria — e,
  no fundo, se o procedimento muda o **processo de decisão** do modelo
- **Interferências anteriores:** Stacey 2022, Mathew 2021 (HateXplain), Pruthi 2022, Jayaram &
  Allaway 2021, Joshi 2022 (ER-Test), Attanasio 2022 (EAR), Ferreira 2025
- **Interferência motivada:** o incômodo é que os ganhos podem não vir das racionalizações —
  trabalhos anteriores relataram ganhos **distribuindo atenção por todos os tokens** (Attanasio) e
  até **ignorando tokens informativos** (Pruthi 2020, Pieke 2023); Ferreira 2025 disputa que a
  regularização mude a decisão. A intervenção: **testar um baseline que ninguém tinha testado —
  tokens aleatórios**
- **Medição:** F1 macro ID e OOD; AUC de alinhamento atenção↔racionalização; SHAP; dataset sintético
  com correlação espúria plantada; treino com rótulos embaralhados

## Desenho experimental

Modelos: BERT e DeBERTa. Padrões de referência comparados: racionalização humana · **tokens
aleatórios** (mesma quantidade r que a racionalização, evitando tokens de racionalização) ·
EAR (atenção uniforme, Attanasio et al.) · sem regularização.

Tarefas e dados: sentimento (IMDb com racionalização de Zaidan et al.; SST) com OOD em DynaSent,
Yelp, SFU · discurso de ódio (HateXplain) com OOD em Dynahate, Ethos, WSF · detecção de posição
(VAST) com OOD em SemEval-2016 e PStance. Treinam em subconjuntos para simular escassez de dados.

Correlação espúria sintética: 500 exemplos do IMDb, modificando 25/50/75% — trocam pontos e
interrogações por exclamação nos positivos, e pontos e exclamações por interrogação nos negativos.
Três conjuntos de teste: com a correlação, com a correlação invertida, e não modificado.

## Achados

1. **Regularização melhora ID e OOD**, sobretudo com pouco dado (100–200 exemplos). Order Loss
   prejudica o DeBERTa (não converge). Melhora OOD em todos os datasets exceto HateXplain.
2. **Tokens aleatórios rendem melhora parecida com racionalização humana** — no texto:
   *"the above performance improvements can be achieved by regularising using either
   human-annotated rationale tokens, or randomly selected tokens."* EAR (atenção uniforme) tem
   desempenho parecido com não regularizar.
3. **A explicação é ruído, não conhecimento.** Testam com rótulos embaralhados: sem regularização o
   modelo começa a decorar (~passo 100 no BERT, ~70 no DeBERTa); com regularização não converge. As
   curvas de perda de racionalização humana e de tokens aleatórios são praticamente iguais.
   Conclusão deles: o ganho vem do ruído impedindo sobreajuste — citam **Bishop (1995)**, treinar
   com ruído ≈ regularização de Tikhonov.
4. **Exceção real: correlação espúria.** No dataset sintético, racionalização humana **vence**
   tokens aleatórios; λ maior reduz a dependência da correlação falsa. É onde o sinal humano prova
   ter conteúdo.
5. **SHAP não muda.** As explicações post-hoc não se alinham mais às racionalizações após a
   regularização. Ou a decisão muda só sutilmente, ou o SHAP não detecta. Ferreira et al. 2025
   relata o mesmo para outros métodos post-hoc.
6. **λ precisa ser ajustado por tarefa e dataset** — a escala de `Lr` depende da função de perda e
   do comprimento dos textos e das racionalizações.

## Limitações declaradas pelos autores

- Os datasets usados têm **textos curtos com alta proporção de tokens de racionalização**; nesse
  regime a regularização tem efeito limitado, porque o modelo não precisa dividir atenção entre
  muitos tokens. **Convidam explicitamente trabalho futuro em textos longos.**
- Racionalização humana não é exaustiva (outros tokens também seriam justificativas plausíveis);
  anotadores discordam; token informativo para humano pode não ser informativo para o modelo.

## O que isso significa para o tema v3

**A pancada:** o canal mais óbvio de injetar racionalização num encoder — regularização de atenção —
é majoritariamente ruído. Se a racionalização humana mal se distingue de tokens aleatórios no
desempenho geral, racionalização de LLM (mais barata e mais ruidosa) tem ainda menos espaço nesse
eixo. **O teto é baixo.**

**As aberturas:**
1. **Eixo de correlação espúria** — é onde o sinal humano prova ter conteúdo, o protocolo sintético
   existe e o código é público.
2. **Textos longos** — limitação declarada, convite explícito, e é o território de interesse do
   Pedro (documento jurídico, diário oficial).
3. **O resultado negativo é sobre UM canal.** Objetivo de saída (Distilling Step-by-Step, DHRD) não
   é tocado por este paper.
4. **Argumento teórico que o paper sustenta sem explorar:** atenção não é o processo de decisão —
   eles mostram isso quando o SHAP não muda. Restringir atenção não restringe a decisão; um objetivo
   de saída obriga a representação a carregar o conteúdo.

**Regra que passou a ser obrigatória:** controle com tokens aleatórios em qualquer experimento deste
espaço. Um baseline faltante invalidou boa parte de uma literatura.

## Lição de método

Eles não inventaram técnica nova — **acrescentaram um controle que ninguém tinha testado**. Custo
baixo, resultado que reposiciona um campo. É o exemplo mais concreto do instrumento "baseline" do
`docs/pesquisa/mapa-do-terreno.md`, e é o tipo de contribuição que cabe no regime do Pedro.
