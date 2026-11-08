# Revisão do método de screening — 15/09/2026

**O que foi revisado:** `docs/screening/metodo-screening-etapa1.md` v1 (dez decisões do Pedro, consolidadas).
**Critérios do Pedro:** (1) método sem lacuna de conhecimento — se o alvo é arquitetura transformer,
não pode faltar self-attention; (2) documento robusto, com todas as seções, decisões e explicações.
**Quem revisou:** Claude, leitura seção a seção, testando cada uma contra os dois critérios e contra
as outras seções. **Resultado:** 21 achados. Cada um recebeu uma correção **proposta** na v2 do
método, marcada `⟨rev-N⟩` no texto. **Nenhuma decisão foi tomada pelo Claude** — o que está na v2 é
proposta até o Pedro confirmar; as que exigem escolha real dele estão marcadas **DECISÃO**.

Severidade: **A** = lacuna que faria o método falhar no critério 1 ou 2 · **B** = inconsistência
interna ou regra sem número · **C** = omissão operacional.

---

## Critério 1 — lacunas de conhecimento

### R1 [A] Não existe mecanismo que garanta a cobertura de fundamentos
A parada (§5) é por saturação de **divisões e seminais**. Fundamento não é divisão nem seminal: é o
que toda fonte *assume* sem explicar (self-attention, KV cache, decodificação autorregressiva,
tokenização, precisão numérica, regime *memory-bound* × *compute-bound*). Nada no método v1 faz um
fundamento entrar no registro — ele só entra por acidente, se algum survey o discutir.
**Correção (v2 §6, §8):** toda fonte screenada produz uma lista de **conceitos assumidos** (termos
usados sem definição). Cada conceito assumido vira candidato a fundamento; um fundamento está
coberto quando tem uma fonte própria (seminal ou livro/capítulo) no registro. É o teste
"self-attention" do Pedro, transformado em regra.

### R2 [A] O pilar fixo (arquiteturas) não tem lista de fundamentos a priori
Foi fixado top-down (§1) mas sem dizer o que contém. Top-down sem conteúdo é bottom-up disfarçado.
**Correção (v2 §1.1):** checklist a priori de fundamentos do pilar arquiteturas. O pilar só fecha
quando cada item tem fonte em nível 1. **DECISÃO:** o Pedro edita a lista (é o mapa dele do que quer
aprender).

### R3 [A] Sem regra para o pilar história
Nenhum tipo de fonte de §3 produz história de forma confiável; prefácio de livro e introdução de
survey produzem *fragmentos*. E não há decisão sobre **até onde a história volta**: poda começa em
LeCun 1990 (*Optimal Brain Damage*) e quantização/poda modernas em Han 2015, sobre CNNs; atenção
começa em Bahdanau 2014, sobre RNNs. Sem regra, o screening ou ignora o pré-transformer ou se afoga
nele.
**Correção (v2 §2.1):** história de cada divisão = *o paper que a abriu* + *a narrativa de um survey*;
pré-transformer e CNN entram **só no pilar história**, não em fundamentos nem ferramentas.
**DECISÃO:** confirmar a fronteira.

### R4 [A] Vocabulário não tem onde ser registrado
§3 aceita "qualquer tipo" para vocabulário; §8 não tem coluna nem arquivo de glossário. O pilar
existe no nome e não no registro.
**Correção (v2 §8):** coluna **termos** na tabela (introduzidos + assumidos) e um **glossário**
`glossario-etapa1.md` alimentado por ela.

### R5 [A] Sem critério de pertencimento à área
As divisões emergem dos surveys (§2), mas não há regra para decidir se uma divisão candidata
*pertence* à área. "Efficient training", PEFT/LoRA, MoE, atenção eficiente, decodificação
especulativa, compressão de KV cache, long-context: entram ou não? Sem critério, a área cresce sem
limite ou encolhe por gosto.
**Correção (v2 §1.2):** uma divisão pertence se reduz **custo de implantação** em pelo menos um de
três eixos — inferência (latência/throughput), memória/hardware, ou dado rotulado. Os três eixos são
os da proposta de tema (rev. 2). **DECISÃO:** confirmar os eixos; decidir se "eficiência de treino"
fica fora.

### R6 [B] Escopo de "modelos" não declarado
Só LLMs? Transformers? Visão? Os surveys de compressão cobrem CNNs; os de serving cobrem só LLMs.
**Correção (v2 §1.3):** fundamentos e ferramentas = **modelos de linguagem baseados em transformer**;
história = sem restrição de família (ver R3). **DECISÃO.**

### R7 [B] "Ferramenta" × "técnica" não distinguidos
vLLM é ferramenta; PagedAttention é técnica dentro de uma divisão; o mesmo paper apresenta os dois.
**Correção (v2 §3.1):** ferramenta = software instalável; técnica = vai para a divisão. Um paper de
sistema gera **duas linhas** no registro (a técnica na divisão; a ferramenta no pilar ferramentas).

## Critério 2 — consistência e robustez do documento

### R8 [A] Circularidade entre divisões e saturação
§5 define parada *por divisão*; §2 diz que as divisões *emergem* dos surveys. Não dá para saturar
uma divisão que ainda não existe. O v1 mistura dois níveis de saturação sem os separar.
**Correção (v2 §5):** saturação em **dois níveis, em ordem**: (i) do **mapa** — surveys *da área* não
trazem divisão nova; (ii) de **cada divisão** — surveys *da divisão* não trazem seminal novo. O mapa
satura primeiro.

### R9 [B] Saturação sem mínimo
Com um survey lido, "o próximo não trouxe nada" é indistinguível de "não li o suficiente".
**Correção (v2 §5):** mínimo de **3 surveys** antes de declarar saturação em qualquer nível.

### R10 [B] Critério (b) do seminal sem limiar
"O que os surveys citam em comum" — em comum a quantos? 2 de 3? Todos?
**Correção (v2 §4):** citado por **≥ 2 dos ≥ 3 surveys** da divisão. **DECISÃO:** o número.

### R11 [B] Inclusão forçada sem número
"Tão relevante quanto o Attention is All You Need" não é operacional.
**Correção (v2 §4):** gatilho = está entre os **3 mais citados da divisão** (Semantic Scholar) e não
saiu por (b)/(c). **DECISÃO:** o número.

### R12 [A] Não existe regra de entrada — de onde vem o primeiro survey?
O pipeline (§10) começa em "screening geral" sem dizer o que alimenta ele. Não há lista de bases,
nem estratégia de busca de surveys, nem janela temporal, nem língua. É a lacuna operacional maior
do v1: o método não diz como começar.
**Correção (v2 §11 Procedimento):** três portas de entrada para surveys — (1) busca por título em
Semantic Scholar / arXiv / ACL Anthology com `survey | review | overview` + nome da área ou da
divisão; (2) ementas dos cursos de referência (R14); (3) referências dos surveys já lidos (bola de
neve). Bases: arXiv, ACL Anthology, Semantic Scholar, Google Scholar; livros via ementas. Janela:
surveys **2020+** para mapa e divisões; sem janela para seminais e história. Língua: inglês.
**DECISÃO:** bases e janela.

### R13 [B] Sem filtro de qualidade para survey
Há dezenas de "surveys" de eficiência de LLM no arXiv, muitos rasos. Sem filtro, o primeiro que
aparece define o mapa.
**Correção (v2 §3.2):** survey entra se (venue com revisão por pares) **ou** (≥ 100 citações no
Semantic Scholar) **ou** (citado por ≥ 2 outros surveys já registrados). **DECISÃO:** os números.

### R14 [C] "Cursos de referência" sem lista
§4 usa cursos como critério de seminal, mas não diz quais. Verificados em 15/09 (página existe,
título confere — nível 3): **MIT 6.5940** *TinyML and Efficient Deep Learning Computing* (Song Han),
**Stanford CS336** *Language Modeling from Scratch*, **CMU 11-868** *Large Language Model Systems*.
**Correção (v2 §4.1):** lista inicial com esses três; o Pedro adiciona ou remove.

### R15 [B] Nível 3 "versão simples" não definido — e é onde o Agrawal escapou
§7 delega o screening a agente em "versão mais simples" de §6, sem dizer o que é. A lição registrada
do Agrawal: o nível 3 *interpretou* ("incógnita") em vez de *extrair*, e perdeu o mecanismo.
**Correção (v2 §7):** o nível 3 devolve **extração, não interpretação**: seção de taxonomia
transcrita, títulos de seções, contribuições declaradas *verbatim*, lista de referências
estruturada, conceitos assumidos. O agente não julga relevância; a filtragem (§10) é do Pedro.
Regra adicional: se a extração de PDF falhar, tentar outra rota (URL do publisher) antes de registrar
"ilegível" — regra já em memória, agora no método.

### R16 [B] Fase 2B precisa de identificadores normalizados
Interseção de listas de referências só funciona se cada referência tiver identificador único.
**Correção (v2 §8):** coluna **identificador** (DOI ou arXiv id); referência sem identificador é
resolvida antes de entrar na interseção.

### R17 [B] "Dúvida" nunca se resolve
§6 manda registrar "dúvida"; §7/§8 dizem que se resolve "na Etapa 1" — mas a Etapa 1 só lê o que
*entrou*. Dúvida fica dúvida para sempre.
**Correção (v2 §8.1):** dúvida = Claude lê **a seção em questão** (nível 2 parcial, limitado) e
devolve o fato; o Pedro decide entra/não entra. Prazo: até o fim do screening da divisão.

### R18 [B] Mapa das divisões sem regra de reconciliação
Surveys dividem a área de jeitos diferentes. §9 diz "o Pedro decide" sem critério.
**Correção (v2 §9):** espinha dorsal = taxonomia do survey mais recente que passou no filtro de R13
e cobre a área inteira; divergências dos outros anotadas no mapa como alternativas. **DECISÃO.**

### R19 [C] Registro sem colunas de rastreabilidade
Faltam: **data**, **fonte de origem** (qual survey/curso levou até ela — é a bola de neve visível),
**venue** (com a regra já rejeitada: rodapé de PDF não é venue; *Comments* do arXiv é), **identificador**
(R16), **termos** (R4).
**Correção (v2 §8):** colunas adicionadas.

### R20 [B] Etapa 3 já screenou uma divisão — sem regra de reaproveitamento
`docs/pesquisa/artigos-verificados.md` tem ~50 artigos verificados de *destilação de raciocínio* (a divisão do tema
v3). Refazer é desperdício; ignorar é perder procedência já feita.
**Correção (v2 §12):** os artigos de `docs/pesquisa/artigos-verificados.md` entram no registro novo com o nível de
procedência que já têm, marcados `origem: etapa-3`. Os quatro em nível 2 com notas continuam citáveis.
**DECISÃO.**

### R21 [C] Falta o procedimento e faltam os critérios de conclusão
O v1 é um conjunto de decisões, não um procedimento executável; e não diz quando a **Etapa 1**
(não o screening) está concluída, nem o que "planejado × feito" mede em cada gate.
**Correção (v2 §11, §13):** §11 Procedimento passo a passo (o pipeline do Pedro, com entradas e
saídas por fase); §13 critérios de conclusão do screening e da Etapa 1, e as quatro métricas de
gate: divisões saturadas · fontes registradas · fontes em nível 2 · fontes em nível 1.

---

## O que NÃO foi alterado

- As dez decisões do Pedro (objeto, híbrido, tipos de fonte, seminal b+c, saturação, profundidade por
  tipo, 3→2→1, registro c, saída c, 16–24 h). Todas continuam na v2 com o texto original.
- O rascunho a priori de divisões (§2).
- A regra de documentação (§3).

## Como usar esta revisão

Ler a v2 procurando os marcadores `⟨rev-N⟩`. Os marcados **DECISÃO** precisam de resposta sua; os
demais são preenchimento de lacuna com o default mais defensável, e você derruba se discordar. Depois
da rodada, os marcadores saem e o método vira v2 limpo.
