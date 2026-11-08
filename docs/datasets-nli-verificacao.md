# Verificação concreta de ASSIN2 e e-SNLI — insumo para a pendência 7

**Data:** 10/09/2026 · **Autor da verificação:** Claude · **Decisão:** do Pedro, não deste arquivo.

## PROCEDÊNCIA (regra permanente do projeto)

| Nível | O que significa | O que aqui está nesse nível |
|---|---|---|
| **1 — Pedro leu** | citável, assinável | **nada neste arquivo** |
| **2 — Claude leu a fonte primária** | citável com revisão do Pedro | ASSIN2 (overview CEUR completo, extraído do PDF) · e-SNLI (paper NeurIPS 2018, arXiv:1812.01193, trechos lidos) |
| **3 — página/metadado apenas** | **triagem, NUNCA citação** | cartões do HF (assin, assin2, esnli, faquad-nli) · SICK-BR (só busca) · número do BERTimbau-Large · BERTomelo e ModBERTBr |

Tudo abaixo está marcado **[N2]** ou **[N3]**.

---

## 1. ASSIN2 — os números

**Fonte primária:** Real, Fonseca & Gonçalo Oliveira, *Organizing the ASSIN 2 Shared Task*,
CEUR-WS Vol-2583, paper 1. Lido integralmente por Claude. **[N2]**

| Item | Valor |
|---|---|
| Divisão | **6.500 treino · 500 validação · 2.448 teste** (~10k pares) |
| Rótulos RTE | **2 classes: entailment / non-entailment** |
| Escala STS | 1–5 (`relatedness_score`) |
| Métrica oficial | **F1 macro** (principal) + acurácia |
| Formato | XML, `<pair entailment="..." similarity="...">` com `<t>` e `<h>` |
| Variante | **só pt-BR** (não tem pt-PT) |
| Licença | CC BY 4.0 no paper; "unknown" no cartão HF **[N3]** |

### 1.1 De onde vêm as sentenças — e por que isso é o achado que importa

Citação direta do overview, §2.1 **[N2]** (tradução minha; o original está em inglês):

> "o corpus ASSIN 2 foi baseado no **SICK-BR**, uma tradução e adaptação manual do SICK […]
> O SICK é conhecido por ser baseado em **legendas de imagens** e por ter **menos fenômenos
> linguísticos complexos**, o que serve perfeitamente aos nossos propósitos."

E, sobre o design da tarefa, §2.3 **[N2]**:

> "optamos por ter **apenas dois rótulos de RTE**; entailment e non-entailment. Diferentemente do
> ASSIN 1, **não usamos o rótulo de paráfrase** […] nossa intenção original era seguir a tradição
> que presta atenção a contradições […] **porém**, ter um corpus anotado de forma sólida para
> contradições não é tarefa trivial."

**Consequência direta para a pendência 8 do `tema-v3`.** O critério que elegeu inferência textual
como tarefa foi: *a racionalização carrega um passo de inferência que não está na superfície do
texto*. O ASSIN2 foi **deliberadamente construído para o oposto** — fatos simples, poucos fenômenos
complexos, e a classe que mais exige raciocínio (contradição) **removida por decisão de projeto**,
com neutro e contradição colapsados em `NONE`.

Isso não elimina o ASSIN2. Mas o move da coluna "escolha natural" para a coluna "candidato com um
risco nomeado": ele pode ser exatamente o caso de análise de sentimento que o `tema-v3` descarta —
racionalização que só aponta para o que o modelo já vê.

O corpus também é **balanceado artificialmente**: os organizadores geraram pares de entailment a
partir de pares existentes do SICK-BR trocando sinônimos e removendo sintagmas adverbiais ou
adjetivais. É um vetor de atalho superficial (sobreposição lexical) declarado na própria fonte. **[N2]**

### 1.2 O teto

| Sistema | F1 macro RTE | Acurácia | Nível |
|---|---|---|---|
| Melhor do shared task 2019 (Deep Learning Brasil, run 2) | **0,883** | 88,32 | **[N2]** tabela do overview |
| IPR run 1 | 0,876 | 87,58 | **[N2]** |
| NILC run 1 | 0,871 | 87,17 | **[N2]** |
| BERTimbau-Large (2020) | **90,0** | — | **[N3]** resultado de busca, **não conferido na fonte** |

Com 2.448 exemplos de teste, o intervalo de confiança de 95% sobre acurácia perto de 90% fica em
torno de **±1,2 ponto**. Os ganhos do DHRD sobre decoders foram de **+0,65% a +5,47% relativos**.
Um ganho na faixa baixa dessa distribuição **não é separável do ruído** neste conjunto de teste sem
múltiplas sementes. Isso é orçamento de experimento, não impedimento: exige rodar sementes, e o
modelo é pequeno o bastante para permitir.

---

## 2. e-SNLI — os números

**Fonte primária:** Camburu et al., *e-SNLI: Natural Language Inference with Natural Language
Explanations*, NeurIPS 2018 (arXiv:1812.01193). PDF baixado; §1, §2, §4.5 e conclusão lidos. **[N2]**

| Item | Valor |
|---|---|
| Divisão | **549.367 treino · 9.842 validação · 9.824 teste** **[N3, cartão HF]** |
| Rótulos | **3 classes: entailment (0) / neutral (1) / contradiction (2)** |
| Racionalização humana | **1 explicação por par no treino; 3 por par em validação e teste** **[N2]** — citação literal: *"We collected one explanation for each pair in the training set and three explanations for each pair in the validation and test sets."* |
| Anotadores | 6.325 trabalhadores, média de 860 explicações cada (dp 403) **[N2]** |
| Ressalva declarada | a pontuação não foi separada das palavras; ignorar os campos `Sentence_Highlighted_*` e usar `Sentence_marked_*` **[N3, README do repositório]** |

Atenção ao esquema do HF: as três colunas `explanation_1/2/3` existem em **todos** os splits, mas
pela fonte primária só validação e teste têm as três preenchidas. Conferir na carga antes de usar.

### 2.1 O protocolo fora de domínio consagrado

O próprio paper do e-SNLI define e executa o protocolo (§4.5) **[N2]**:

> "Transferência sem fine-tuning para conjuntos de entailment fora de domínio é conhecida por
> exibir desempenho ruim. Por exemplo, Bowman et al. obtiveram acurácia de **apenas 46,7%** ao
> treinar em SNLI e avaliar em **SICK-E**."

Eles testam em **SICK-E** e **MultiNLI**, sem fine-tuning.

**Achado deles que é diretamente relevante ao `tema-v3`:** a melhoria de acurácia trazida pelo sinal
de explicação na transferência foi **"muito pequena"** (palavra deles), e a qualidade das explicações
geradas fora de domínio desabou — 30,64% corretas em SICK-E e **1,92%** em MultiNLI. Ou seja: **já
existe na literatura um resultado fraco de transferência OOD com racionalização**, sobre arquitetura
antiga (InferSent, sem Transformer). Isso é ao mesmo tempo um risco para o tema (o efeito pode não
existir) e uma abertura (ninguém refez isso com racionalização de LLM e cabeça auxiliar descartada).

---

## 3. O problema do fora de domínio em pt-BR — o achado bloqueante

A pendência 10 do `tema-v3` torna a avaliação fora de domínio **obrigatória**. Em pt-BR isso esbarra
num obstáculo específico:

> **SICK-BR NÃO serve como conjunto fora de domínio para o ASSIN2, porque o ASSIN2 foi construído
> A PARTIR do SICK-BR.** Mesmas sentenças, mesma origem. **[N2]** — declarado no overview, §2.1.

O que sobra em pt-BR:

| Candidato OOD | Tamanho | Rótulos | Domínio | Distância real do ASSIN2 | Nível |
|---|---|---|---|---|---|
| **ASSIN 1** | 10.000 pares (config `ptbr`: 2.500 / 500 / 2.000) | **3**: NONE / ENTAILMENT / **PARAPHRASE** | **Notícias** (Google News PT e BR) | **Alta** — outro gênero, sentenças longas, expressões temporais, discurso indireto | [N3] cartão HF; o gênero e os desafios linguísticos são [N2], declarados no overview do ASSIN 2 |
| **FaQuAD-NLI** | 3.128 / 731 / 650 | **2**: resposta adequada / inadequada | Documentos oficiais de uma universidade federal + Wikipédia sobre ensino superior | **Alta demais** — é adequação de resposta a pergunta, não premissa→hipótese clássica | [N3] |
| SICK-BR | ~9.840 | 3 | Legendas de imagem | **Zero — é a fonte do ASSIN2** | [N2] para a relação; [N3] para o tamanho |

**Leitura:** o eixo pt-BR **tem** caminho fora de domínio — é **ASSIN2 → ASSIN 1**, colapsando
`PARAPHRASE` em `ENTAILMENT` para casar com o rótulo binário. É um protocolo legítimo (treinar em
legendas simples e testar em notícias é mudança de domínio genuína e severa), mas é **montado por
nós**, não consagrado. Toda pergunta de revisor sobre o mapeamento de rótulos cai sobre o Pedro.

---

## 4. Os dois eixos, lado a lado

| Critério | **pt-BR (ASSIN2 → ASSIN 1)** | **Inglês (e-SNLI → SICK-E / MultiNLI)** |
|---|---|---|
| Classes | 2 (entailment / não) | 3 (entailment / neutral / contradiction) |
| Treino | 6.500 | 549.367 |
| Teste | 2.448 | 9.824 |
| Exige raciocínio? | **Fraco** — legendas de imagem, "fatos simples", por decisão declarada dos organizadores | **Forte** — contradição presente; é um dos datasets do próprio Distilling Step-by-Step |
| Racionalização humana (teto) | **Não existe** | **Existe** — 1 no treino, 3 em validação e teste |
| Protocolo OOD | Existe, mas **montado por nós**; exige mapear PARAPHRASE→ENTAILMENT | **Consagrado e citável**, com piso de referência (46,7% de Bowman et al.) |
| Teto atual | ~88,3 F1 (shared task, [N2]) / ~90 (BERTimbau-L, [N3]) | SOTA alto, mas o regime de comparação é outro |
| Custo por época na RTX 5060 8GB | **Baixo** — 6,5k exemplos | **Alto** — 549k exemplos; exige subamostrar |
| Argumento de mercado | Sustenta "não existe T5 adaptado ao português" | **Derruba** esse argumento |
| Risco de resultado nulo | **Alto** — se a tarefa é superficial, a cabeça auxiliar não tem o que ensinar | Menor, mas o §4.5 do e-SNLI já mostrou transferência OOD fraca |
| Novidade | Maior (ninguém fez isso em pt-BR) | Menor (terreno mais pisado) |

### Recomendação (é do Claude; a decisão é do Pedro)

⭐ **Inglês, e-SNLI, com subamostragem do treino** — por **um motivo só**: é o único eixo em que a
hipótese do `tema-v3` pode **falhar de forma informativa**. Se o ASSIN2 der ganho nulo, não se sabe
se foi porque racionalização não transfere para encoder (o achado) ou porque a tarefa era superficial
demais para haver o que transferir (o artefato) — exatamente a mesma estrutura de confundidor da
pendência 9b, agora na tarefa em vez de na cabeça auxiliar. O e-SNLI separa as duas: tem contradição,
tem racionalização humana como teto, e subamostrar para 30–50k resolve o custo de GPU (o Distilling
Step-by-Step é inteiro sobre a tese de que menos dados bastam).

**Caminho de compromisso, se o argumento pt-BR pesar mais:** treinar em e-SNLI e avaliar **também**
em ASSIN2 traduzido/adaptado. Mas isso é um terceiro projeto, não uma variação — não recomendo
dentro de 3–4 meses.

**O que NÃO recomendo:** ASSIN2 como tarefa única. Não pelo tamanho — pelo design declarado.

---

## 5. Achados laterais (não pedidos; registrados para a pendência 5, encoder base)

Dois encoders pt-BR recentes apareceram na busca e **não foram verificados** — relevantes para a
decisão do encoder base, não para a de dataset:

- **BERTomelo: Your Portuguese Encoder Best Friend** — arXiv:2606.28999. **[N3, só título e URL]**
- **ModBERTBr: A ModernBERT-based Model for Brazilian Portuguese** — ENIAC/SBC. **[N3]**

Confirmar existência, tamanho, licença e disponibilidade no HF antes de considerar qualquer um.

## 6. Fontes

- ASSIN 2 overview: https://ceur-ws.org/Vol-2583/1_ASSIN-2.pdf — **lido integralmente [N2]**
- e-SNLI paper: https://arxiv.org/abs/1812.01193 — **lido em parte [N2]**
- HF `nilc-nlp/assin2`, `nilc-nlp/assin`, `esnli/esnli`, `ruanchaves/faquad-nli` — **[N3]**
- Napolab (agregador de benchmarks pt): https://github.com/ruanchaves/napolab — **[N3]**
