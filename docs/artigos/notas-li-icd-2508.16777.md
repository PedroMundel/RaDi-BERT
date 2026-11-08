# Notas de leitura — Li et al., racionalizações de codificação ICD

**Referência:** Li, M.; Schlegel, V.; Mu, T.; Oyewusi, W.; Kang, K.; Nenadic, G.
**"Evaluation and LLM-Guided Learning of ICD Coding Rationales"**. arXiv:2508.16777v2.
Submetido 22/08/2025, v2 de 12/03/2026. https://arxiv.org/abs/2508.16777
PDF: `2508.16777-li-icd.pdf` (20 páginas) nesta pasta.
Afiliação: University of Manchester + programa IN-CYPHER (Singapura).

⚠ **Procedência:** Claude leu em 10/09/2026 — §5 (método) integral, §6.1–6.2 (resultados), §7
(conclusão), §8 (limitações), Tabelas 3 e 4, resumo e partes de §1–2. **NÃO leu** §3, §4
(construção do dataset de racionalização e métricas de plausibilidade) nem os apêndices.
**Pedro não leu.** Notas de terceiro.

⚠ **Venue NÃO confirmado.** O registro anterior dizia "EACL 2026"; isso **não se sustenta na
fonte**: o arXiv não traz campo *Comments*, e o PDF usa o template genérico do ACL sem linha de
venue. O agradecimento cita *"anonymous ARR reviewers"*, o que indica passagem pelo ACL Rolling
Review — compatível com um venue *ACL, mas não é prova de aceitação na EACL 2026. **Verificar na
ACL Anthology antes de citar com venue.**

## Por que este paper estava na fila

Era a pendência 4 do tema v3: o "outro que pode derrubar a novidade". Motivo do medo: é
racionalização de LLM aplicada a modelo de classificação (não gerador), e o mecanismo de conversão
estava marcado como NÃO confirmado no `docs/pesquisa/artigos-verificados.md`.

## VEREDITO: não ocupa H1 nem H2 — e fortalece a premissa do tema

Os dois mecanismos deles são **extrativos sobre token**, não alvo latente:

**1. Multi-objective learning.** A racionalização do LLM é convertida numa **matriz de máscara
binária** `M_{i,l}` (1 = token pertence à racionalização), e a perda é **entropia cruzada binária
entre os pesos de atenção e essa máscara**:
`L_rationale = −(1/N_D) Σᵢ Σ_l Σⱼ [M log ã + (1−M) log(1−ã)]`, com treino em `L_coding + L_rationale`.
→ É **exatamente o canal de atenção** — a mesma família do Herrewijnen, Bao 2018, REFER. Não é
regressão para embedding (H1) nem cabeça geradora auxiliar (H2).

**2. Learning by NER formulation.** Cada racionalização vira uma **entidade** cujo rótulo de classe
é o próprio código ICD; o resto recebe classe nula. Codificação e extração de racionalização
colapsam numa única tarefa de NER padrão.
→ Também extrativo, e ainda mais distante: troca a tarefa de classificação por rotulagem de token.

**Consequência para o tema v3:** a racionalização de texto livre do LLM é usada aqui apenas como
**fonte de spans** — ela é reduzida a highlights antes de entrar no treino, e **nunca é alvo de
saída nem de representação**. Na taxonomia do Wiegreffe & Marasović, eles convertem free-text →
highlight *antes* do modelo. A célula do tema v3 (racionalização de texto livre como **objetivo de
saída** sobre encoder) continua vazia.

## O achado que vale mais que o veredito de novidade

Arquitetura deles: **PLM-ICD é encoder** (família RoBERTa clínica); CAML e LAAT são CNN/LSTM com
atenção por rótulo. Ou seja: **isto é racionalização de LLM supervisionando atenção de encoder** —
o cenário mais próximo do canal 1 do desenho do tema v3. E o resultado é:

| Tabela 3 (Top-50) | F1-Mac | F1-Mic |
|---|---|---|
| PLM-ICD (baseline) | 68,18 | 73,40 |
| **+ multi-objective (atenção supervisionada)** | **67,93** | **73,26** |
| PLM-ICD (setting do NER) | 61,09 | 68,18 |
| **NER formulation** | **53,46** (−12,49% rel.) | 67,75 |

**Supervisionar atenção com racionalização de LLM não melhorou acurácia — piorou de leve**
(−0,25 ponto macro-F1, −0,14 micro). A frase deles é *"does not degrade ICD coding performance;
instead, it improves plausibility by approximately 1% (F1)"* — o ganho é **só em plausibilidade**,
isto é, em parecer convincente para humano. E a via NER paga 12,49% de F1-macro para ganhar
plausibilidade.

→ **Terceira corroboração independente de que o canal de atenção não carrega conhecimento.**
Herrewijnen mostrou com racionalização **humana** (e que tokens aleatórios rendem quase o mesmo);
o DHRD mostrou pelo lado positivo que o canal de **saída** carrega conteúdo; e agora Li et al.
mostram que nem mesmo racionalização de **LLM** faz o canal de atenção render acurácia — em outro
domínio (clínico), outra tarefa (multi-rótulo), outro encoder.

Isso é citável na introdução do tema v3 como evidência de que a escolha de canal é a variável, não
a qualidade da fonte da racionalização.

## Ressalva honesta sobre esse argumento

Eles **não estavam otimizando acurácia** — o objetivo declarado é plausibilidade e explicabilidade,
e "não degradar" já é sucesso pelo critério deles. Não há busca em grade de peso da perda auxiliar
relatada, não há controle com tokens aleatórios, e o setup é multi-rótulo com milhares de códigos,
bem diferente de classificação de rótulo único. Então isto é **evidência convergente, não replicação
controlada**. Usar como "mais um ponto na mesma direção", nunca como prova.

## Coisas aproveitáveis para o desenho

- **Racionalização de LLM local é viável:** LLaMA-3.3 quantizado em **AWQ** fica "competitivo" com
  Gemini 2-Flash na qualidade da racionalização, com queda pequena. Reforça o caminho (2) da §7c do
  `docs/pesquisa/mapa-do-terreno.md` — professor aberto local. Ressalva: eles relatam **~40 GB de memória** para o
  AWQ, muito acima da 5060; o professor teria que ser bem menor, ou rodar em GPU gratuita na nuvem.
- **Few-shot com exemplos humanos melhora a racionalização do professor** em 39,9–50,3% nas métricas
  de plausibilidade. Se o tema usar HateBRXplain como teto humano, os mesmos exemplos servem para
  melhorar o professor — dois usos para a mesma anotação.
- **Métrica de plausibilidade** (Exact/PI Span Match, Exact/PI Token Match) — vocabulário pronto,
  caso o tema queira medir *quão parecida com a humana* é a racionalização do professor. Está na §4,
  que eu não li.
- O trabalho anterior que eles citam para multi-objetivo em ICD é **Cheng et al. 2023** e
  **Edin et al. 2024** — dois nomes novos, não estão no `docs/pesquisa/artigos-verificados.md`.

## O que fica em aberto daqui

1. Confirmar o venue na ACL Anthology.
2. Ler §4 se o tema for medir plausibilidade (métricas e construção do dataset de 150 amostras).
3. Registrar Cheng et al. 2023 e Edin et al. 2024 (multi-objetivo em ICD) e Edin et al. 2023
   (framework de reprodutibilidade MIMIC).
