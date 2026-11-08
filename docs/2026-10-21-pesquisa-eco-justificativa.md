# Eco nas justificativas: o que a literatura diz e faz (pesquisa de 21/10/2026)

**Procedência: nível 3 (agente). O Pedro não leu nenhum destes artigos. Serve para triagem e para decidir o que ler; não serve para citação em texto assinado.**
Etiquetas: `N3-txt` = agente leu o texto completo (via HTML ar5iv/arXiv com extração automática, **sem numeração de página**; cito seção/tabela/apêndice); `N3-abs` = só resumo ou trecho de busca. Em dois casos o texto foi lido só até ~100 mil dos ~120-140 mil caracteres (apêndices finais de Wiegreffe 2022 e §7 em diante de Wiegreffe & Marasović 2021). Nomes, autores, ano e ids foram conferidos nas páginas do arXiv e da ACL Anthology.

**Conferido pelo Claude no PDF (21/10):**
- Camburu 2018, p. 3, §3: 11% reanotados como template; erro de 19,55% na implicação; e a frase "many of the
  entailment pairs have the hypothesis as almost a subset of the premise, prompting the annotators to just repeat that
  as a statement". Batem.
- REV, Chen 2023, Tab. 2, p. 6: REV do ouro de 0,0752 no e-SNLI, contra 0,7943 no ECQA e 1,3919 no QuaRTz. Bate.

O resto segue em nível 3.

**Tamanho do problema no e-SNLI (medido pelo Claude, 21/10, dev inteiro, 9.842 pares).** Conta de palavras de conteúdo
da hipótese que não estão na premissa, com as palavras de `copia.py` e sem lematização:

| Rótulo | 0 novas | 1 | 2 | 3 ou mais |
|---|---|---|---|---|
| implicação | 25,4% | 38,3% | 22,2% | 14,0% |
| neutro | 0,7% | 23,3% | 32,3% | 43,7% |
| contradição | 3,6% | 19,4% | 31,2% | 45,8% |

- A zona de eco puro (implicação com 0 palavras novas) é ~25% das implicações, ou **~8,5% do dataset**.
- Com 1 palavra nova muitas vezes ainda existe ponte (cap → hat, man → human). Por isso, os 21,6% do dataset que são
  implicação com até 1 palavra nova são o **teto**, não a taxa.
- Sem lematização, "boy" e "boys" contam como palavras diferentes. Então o grupo de 0 novas está **subestimado**.

## Veredito curto

1. O fenômeno **tem nome e medida** na literatura (template, vacuous, "new information"), inclusive no e-SNLI, e o e-SNLI já documenta que o caso de "hipótese quase subconjunto da premissa" induz repetição.
2. Nenhum método de geração removeu o eco por completo; SCOTT e o filtro de Wiegreffe reduzem, não eliminam, e nenhum foi testado no e-SNLI da forma que o projeto usa.
3. Para a perda de treino: **não encontrei nenhum artigo que mascare ou pese a perda de justificativa por informatividade (nova informação) por exemplo, nem que permita justificativa vazia**. Os vizinhos pesam por correção ou qualidade geral, ou selecionam entre candidatos.

## 1. Trabalhos que nomeiam ou medem justificativas triviais

| Obra | Id verificado | Achado relevante | Local | Tag |
|---|---|---|---|---|
| Camburu, Rocktäschel, Lukasiewicz, Blunsom (2018), *e-SNLI: Natural Language Inference with Natural Language Explanations*, NeurIPS 2018 | arXiv:1812.01193 | Pedia-se ao anotador focar nos elementos "não óbvios" e **não** nas partes da premissa repetidas idênticas na hipótese; no entailment, justificar todas as partes da hipótese ausentes da premissa. Checagens no navegador: >= 3 tokens e não ser cópia da premissa/hipótese. Filtro de templates (distância de edição <= 10; lista no Apêndice A, ex. "<premissa> implies <hipótese>"). 11% do dataset detectado como template-like e reanotado. Em amostra de 1.000 exemplos, taxa de erro 9,62% (entailment 19,55%, neutro 7,26%, contradição 9,38%); os autores dizem que no entailment "many of the entailment pairs have the hypothesis as almost a subset of the premise, prompting the annotators to just repeat that as a statement". | §3 ("Collecting explanations"; parágrafo "Analysis and refinement of the collected dataset"); Apêndice A | N3-txt |
| Wiegreffe & Marasović (2021), *Teach Me to Explain: A Review of Datasets for Explainable Natural Language Processing*, NeurIPS 2021 (D&B) | arXiv:2102.12060 | Lista de 56 templates; 11% reanotado; mesmo depois, as explicações do e-SNLI "still largely follow 28 label-specific templates" (citando Camburu et al. 2020); templates são descartados por serem "uninformative" e podem virar artefato (modelo ignora a semântica e prediz pelo tipo de template). | §5 | N3-txt (parcial) |
| Wiegreffe, Hessel, Swayamdipta, Riedl, Choi (2022), *Reframing Human-AI Collaboration for Generating Free-Text Explanations*, NAACL 2022 | arXiv:2112.08674; ACL 2022.naacl-main.47 | Atributo "new information" ("Does the explanation provide new facts, information or reasoning not stated in the question and answer?"), definido para pegar explicações vácuas que só reafirmam a entrada. Nota média (Fig. 2): GPT-3 0,1 nas duas tarefas; humanos 0,6 (ECQA) e **0,2 (SNLI)**. | §2.3, Fig. 2, Apêndice B.3 | N3-txt |
| Chen et al. (2023), *REV: Information-Theoretic Evaluation of Free-Text Rationales*, ACL 2023 | arXiv:2210.04982; ACL 2023.acl-long.112 | REV = log g[r,b](y) - log g'[b](y), com baseline b = entrada + rótulo ("any vacuous rationale which simply (and declaratively) combines an input with a given label"). **No e-SNLI, a maioria das justificativas segue um template "A implies (that) B"** (§4.1) e o REV é baixíssimo: Tabela 2, e-SNLI = 0,0752 (humana) e 0,0079/0,0055/0,0047 (variantes geradas), contra 0,79 (ECQA) e 1,39 (QuaRTz). Isto é **compatível com a hipótese I(R;X\|Y) ~ 0**. Interpretação das colunas da Tabela 2 é do agente. | §1, §2.1-2.2 (Eq. 6), §4.1, Tabela 2 | N3-txt |
| Jiang et al. (2024), *RORA: Robust Free-Text Rationale Evaluation*, arXiv preprint (sem venue na página) | arXiv:2402.18678 | Corrige o REV, que pode dar nota alta a justificativa que vaza o rótulo ou reafirma a pergunta (0,436 em teste dos autores); condiciona em X. Tabela 2 (StrategyQA): RORA vácuo 0,043 vs. ouro 0,115; REV ouro -0,038 vs. vazante 0,145. Não usa e-SNLI. | §2.2, §3.1-3.3, Tabelas 2-4 | N3-txt |

## 2. Mitigações no lado da geração

- **Few-shot + filtro de aceitabilidade (Wiegreffe et al. 2022).** Prompts de 8-24 exemplos (SNLI: {12,18,24}), reformulando SNLI como pergunta-resposta (Ap. A). Filtro T5-Large/T0-3B treinado com julgamentos humanos binários de aceitabilidade (§4.1-4.2): em SNLI, acurácia select-1 de **38,7** (NLL: 32,0; oráculo 52,4) e AP 47,6 (**Tabela 8**). Os filtrados "mais prontamente introduzem informação nova" (§4.4, Fig. 3), mas "new info" é o atributo menos correlacionado com aceitabilidade (rho = 0,05, **Tabela 6**). Não há ablação de instrução. Tag: N3-txt.
- **SCOTT (Wang et al. 2023), ACL 2023, arXiv:2305.01879, ACL 2023.acl-long.304.** Atenção: o contraste **não é contra uma justificativa vazia**, e sim contra uma **resposta (rótulo) perturbada** a' (vazia ou errada): G(t_i|a*) = log P(t_i | p,q,a*,t_<i) / P(t_i | p,q,a',t_<i), decodificação por argmax da soma (Eq. 3-4, §3.1). Efeito: em StrategyQA (100 justificativas, Tabela 1) "New Info" 0,65 (guloso) -> 0,77 (contraste-vazio) -> 0,82 (contraste-errado). Datasets: CSQA, StrategyQA, CREAK, QASC; **sem NLI/e-SNLI** (§4.1). Os autores medem que 42% das justificativas do GPT-3 em StrategyQA não davam informação nova (§1, Fig. 1). Tag: N3-txt.
- **Amostrar vários e escolher por informatividade (REV/RORA).** Nenhum dos dois artigos propõe isso; ambos são só métricas (REV §6 cita como trabalho futuro; RORA §4). A ideia de usá-los como seletor **não tem evidência publicada que eu tenha achado**. Symbolic CoT Distillation (Li et al. 2023, ACL 2023, arXiv:2306.14050) amostra várias cadeias por instância e testa filtros (diversidade, verossimilhança do professor) em commonsense; **sem filtro de nova informação nem e-SNLI**. Tag: N3-abs.

## 3. Filtro ou reescrita pós-geração

- Filtro por template (Camburu 2018, Ap. A) e filtro treinado de aceitabilidade (Wiegreffe 2022, acima): ambos **removem/reanotam** e estão no e-SNLI/SNLI. Não achei trabalho que **reescreva** justificativa trivial para torná-la informativa.
- **MoRSD** (Yan et al. 2025, *Towards Efficient CoT Distillation: Self-Guided Rationale Selector for Better Performance with Fewer Rationales*, Findings of EMNLP 2025, ACL 2025.findings-emnlp.413, arXiv:2509.23574). Define a Dificuldade da Justificativa RD = PPL(resposta | pergunta+justificativa) / PPL(resposta | pergunta) com o **modelo aluno** e mantém as 3 de menor RD entre 6 candidatas (§ método; Eq. 8 é NLL padrão). É a razão mais próxima de "ganho de informação condicional" que vi, mas serve para **selecionar entre candidatas**, em aritmética (SingleEq, GSM8K etc.) e StrategyQA; não trata justificativa que repete a pergunta (apêndice mostra um caso, sem regra). Tag: N3-txt. Obs.: há inconsistências numéricas internas entre texto e Tabela 2 (59,51 vs. 60,70).

## 4. Mitigações no lado do treino

- **Distilling Step-by-Step** (Hsieh et al. 2023, Findings of ACL 2023, ACL 2023.findings-acl.507, arXiv:2305.02301): L = L_label + lambda · L_rationale (Eq. 3-4, §3.2), **lambda escalar único, todo exemplo usa sua justificativa como veio**; professor PaLM 540B, ~10 demonstrações; no §Limitations pede "characterize how rationale quality affects" o método. Sem filtro, sem peso por exemplo, sem justificativa vazia. Tag: N3-txt.
- **CoPeD** (Xie et al. 2025, arXiv:2509.05602, preprint): perda ponderada por exemplo a partir da perda combinada de justificativa e resposta ("Correctness-Aware Weighted loss"); mira justificativas **incorretas**, não vácuas. Tag: N3-abs.
- **QCRD** (Wang et al. 2025, EMNLP 2025 main, 2025.emnlp-main.724, arXiv:2405.13014): discriminador online dá peso de qualidade às justificativas nas perdas contrastivas; qualidade geral, não informatividade condicional. Tag: N3-abs.
- **Verbosity-Aware Rationale Reduction** (Jang et al. 2025, ACL 2025 Findings, arXiv:2412.21006): remove **frases** redundantes do raciocínio por critério de verossimilhança; nunca a justificativa inteira. Tag: N3-abs.
- **Conclusão: NENHUM artigo encontrado** zera, mascara ou pesa a perda auxiliar por informatividade (REV/RORA/RD) por exemplo, nem trata justificativa vazia ou curta como alvo válido. Busca feita em 21/10 em arXiv/ACL Anthology com buscas livres; ausência não é prova.

## Opções para o nosso caso

Todas as recomendações abaixo são **inferência do agente**, não achado dos artigos.

**(a) Prompt.** Custo: nenhum extra (~1 s/par). Evidência: Wiegreffe 2022 mostra que a qualidade do prompt muda a qualidade, mas o "new info" do GPT-3 ficou em 0,1 mesmo assim (§2.3); nada na literatura garante que prompt tire o eco em par quase literal, e as três tentativas do projeto não tiraram. Conflito com marcar-em-vez-de-apagar: nenhum. Inferência do agente: o limite parece estar nos dados (o e-SNLI já tem 19,55% de erro no entailment justamente por este caso, §3), então mais engenharia de prompt tem retorno baixo.

**(b) Decodificação/seleção.** Contraste à la SCOTT exige duas passadas por token (com e sem o rótulo): em llama.cpp isso é implementação própria, ~2x o custo; é o mais caro de montar. Amostrar N=4 candidatas custa ~4 s/par (menos com lotes no `llama-server`) e a seleção pode usar a razão RD do MoRSD com o próprio aluno, ou REV/RORA, que exigem treinar um avaliador pequeno (custo não medido). Evidência: SCOTT sobe "New Info" de 0,65 para 0,77-0,82 em StrategyQA, **fora de NLI**; seleção por informatividade não tem teste publicado. Conflito: nenhum, desde que as candidatas descartadas fiquem guardadas e só o escolhido seja marcado. Risco: se I(R;X|Y) ~ 0 em pares quase literais, todas as candidatas são equivalentes e a seleção não ganha nada.

**(c) Filtro ou reescrita pós-geração.** Custo mínimo para um sinalizador lexical (sobreposição de palavras de conteúdo com o par, distância de edição a templates, como no Ap. A do e-SNLI); REV/RORA têm custo de treino do avaliador. Evidência: é o que o próprio e-SNLI fez (11% reanotado). Reescrita de trivial para informativo: sem evidência publicada. Conflito: filtrar-e-apagar conflita; **marcar com uma coluna** (`eco`, `rev`) e decidir depois não conflita, e alimenta (d).

**(d) Treino (mascarar/ponderar a perda).** Custo: zero de geração, é uma linha na perda por exemplo (peso w_i em lambda · L_rationale, com w_i vindo da coluna do item c). Evidência: indireta apenas, via CoPeD/QCRD (peso por qualidade) e MoRSD (RD); **nenhum artigo testa informatividade condicional** e o DSbS não varia lambda por exemplo. Conflito: nenhum, o dado permanece, só a perda muda; o braço "justificativa mascarada nos ecos" é um controle natural contra o braço "todas as justificativas". Inferência do agente: é a opção de menor custo e maior compatibilidade com a regra de marcar, e transforma a hipótese I(R;X|Y) ~ 0 em teste (ecos mascarados mudam a acurácia do aluno?).

**Ordem sugerida (inferência do agente):** (c) sinalizar primeiro, (d) como braço de ablação; (b) só se a sinalização mostrar que ecos vêm de variação da geração e não do par.

## Becos sem saída

- SCOTT não contrasta com justificativa vazia (corrige a premissa da pergunta).
- RORA e REV não selecionam nada; não há artigo usando-os como filtro de treino.
- A busca por "empty rationale" / "skip rationale loss" só devolveu trabalhos de raciocínio longo (Skip-Thinking, EMNLP 2025; REKD arXiv:2601.22531), que tratam outro problema; vistos só por trecho de busca, não incluídos.
- Não verificado: a afirmação de que as explicações humanas do e-SNLI copiam ~86% das palavras de conteúdo (número do projeto, não localizado nestas fontes).

## Regra do projeto

Nada aqui usa circularidade como veto (rejeitada em 20/10) nem propõe a variante D pura (rejeitada em 21/10).
