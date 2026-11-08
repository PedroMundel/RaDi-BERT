# Proposta — como tirar o lixo da floresta (23/09/2026)

**Status: PROPOSTA, nada executado.** Pedido do Pedro: *"pode prosseguir, com método científico
comprovado"*. A escolha do método é dele; este arquivo traz as opções, com o que cada uma é, a
evidência de que funciona, o custo e o risco.

**Procedência:** os métodos abaixo foram verificados quanto à **existência** (pacote no PyPI /
modelo no Hugging Face / artigo no Crossref, em 23/09) — **nível 3**. Nenhum dos artigos foi lido
inteiro por mim nem pelo Pedro: servem para escolher, não para citar em texto assinado dele.

---

## O problema, em termos de método

A floresta tem **118.659 obras**. Os cajuzeiros — surveys da área de eficiência de modelos para
implantação — são uma fração pequena (a volta 1 sugeria algumas centenas a poucos milhares). Na
literatura de revisão sistemática, isso tem nome: **triagem de títulos e resumos** com
**prevalência baixa** de relevantes. Há três famílias de solução estabelecidas, que podem ser usadas
sozinhas ou em camadas.

## As opções

| | Método | O que faz | Evidência | Custo para você | Risco |
|---|---|---|---|---|---|
| **A** | **Critérios de exclusão por metadado** (Kitchenham & Charters 2007) — campo de estudo do Semantic Scholar (`s2FieldsOfStudy`) | exclui obra cujo campo é **só** Física, Química, Matemática, Medicina… | é o procedimento-padrão de exclusão em revisão sistemática: critério declarado antes, aplicado igual a tudo | nenhum (mecânico) | o campo do S2 é atribuído por modelo e erra; obra de eficiência publicada em revista de física pode cair |
| **B** | **Mapa de tópicos** — BERTopic (Grootendorst 2022; `bertopic` 0.17.4, MIT) | agrupa as obras por assunto a partir de título + resumo; cada grupo vem com palavras-chave; você marca grupos inteiros como lixo | método de modelagem de tópicos consolidado e muito usado; **não** foi desenhado para decidir exclusão em revisão | baixo: olhar ~50–200 grupos, não 118 mil obras | um grupo "lixo" pode esconder cajuzeiros; precisa de amostragem dentro de cada grupo descartado |
| **C** | **Triagem com aprendizado ativo** — ASReview (van de Schoot et al. 2021, *Nature Machine Intelligence*; `asreview` 3.0.8) + regra de parada **SAFE** (Boetje & van de Schoot 2023, preprint) | você marca obras como relevante/irrelevante; o modelo reordena a fila a cada marcação, pondo os prováveis cajuzeiros na frente; para-se pela regra SAFE | é a família com mais validação específica para **triagem** de revisão sistemática; open source, usada por grupos de revisão | **alto**: você lê título + resumo e marca, uma obra por vez (é o 1º degrau da escada); o número de marcações depende da base — não prometo um valor | o modelo aprende o seu critério, inclusive os seus vieses; a parada é heurística |

**Opção fora da tabela, por não ter validação para triagem:** ordenar por similaridade de embedding
com um conjunto-semente (SPECTER2, `allenai/specter2_base`, Apache-2.0). Existe e é bom para
representar papers, mas a evidência dele é de benchmark de representação (SciRepEval, EMNLP 2023),
não de triagem.

## A proposta: camadas, cada uma medida

Nenhum método sozinho resolve bem: A é barato mas grosseiro, B mostra onde está o lixo mas decide em
bloco, C é o mais confiável mas custa o seu tempo. Em camadas, cada uma reduz o trabalho da seguinte:

1. **Camada A — exclusão por campo de estudo.** Baixar `s2FieldsOfStudy` das obras (lote de 500 por
   chamada, ~240 chamadas) e excluir quem **não tem** Ciência da Computação entre os campos. Critério
   declarado antes de olhar o resultado.
2. **Camada B — mapa de tópicos** sobre o que sobrar. Você marca grupos-lixo (química, física,
   medicina, *quantum*…); de cada grupo descartado sorteio uma amostra para conferir que não há
   cajuzeiro ali.
3. **Camada C — ASReview** sobre o que sobrar, com parada SAFE. É aqui que os cajuzeiros aparecem.

**Em toda camada, medir a perda** com o conjunto de referência (as 57 obras da execução 2, metade de
teste): se uma camada derruba obra do gabarito, ela está cortando cajuzeiro e é revista antes de
seguir. Esta é a salvaguarda que torna o processo defensável na arguição: cada corte tem critério
declarado **e** perda medida.

**Tudo continua "ordena, não apaga":** cada obra ganha uma coluna dizendo em que camada caiu e por quê;
o bruto não é tocado.

## Decisões suas

1. Qual método, ou qual combinação: **A + B + C** (a proposta), só **A + C**, só **C**, ou outra?
2. **Camada C** implica você marcar obras no ASReview (roda local, CPU basta). Topa esse trabalho?
   Ele é a sua Fase 3 antecipada — a decisão sobre obra continua sendo sua.
3. Instalar `asreview` e `bertopic` no seu ambiente Python (py311) — só com o seu ok.

---

**DECIDIDO pelo Pedro (23/09): A -> B -> C.** (Instalação de `asreview`/`bertopic` e a disposição
dele para marcar obras na camada C: ainda não respondidas — perguntar antes da camada B.)

**Premissa da camada A derrubada por teste (23/09):** amostra de 40 obras — **todas** têm Ciência da
Computação entre os campos, porque a busca já filtrou por CS. Logo "excluir quem não é CS" não tira
nada. O lixo de outra área aparece **junto** com CS (ex.: CS + Physics, CS + Environmental Science).
Na amostra: CS + Engineering 5 · CS + Engineering + Environmental Science 4 · só CS 3 · CS + Medicine 3
· CS + Linguistics 3 · CS + Education 2 · CS + Business 2 · CS + Physics (+ Materials) 2.
**Novo passo:** coletar os campos de todas as obras (só coleta), mostrar a distribuição e a dos
cajuzeiros conhecidos (metade de ajuste do gabarito), e o Pedro escolhe o critério; a perda se mede
na metade de teste.

**Decisões do Pedro (23/09), depois da camada A:** instalar `bertopic` — **pode** (instalado 0.17.4;
efeito colateral: `transformers` 4.57.6 -> 5.17.0 no py311 — Pedro: **"pode deixar"**). Modelo de
embedding da camada B: **SPECTER2 base** (`allenai/specter2_base`), escolhido entre SPECTER2, MPNet e
MiniLM. Camada C (marcar no ASReview): **"não sei, depende de quantas tiver"** — decide depois de ver
quanto sobra da camada B.
**Parâmetros da camada B, declarados antes de rodar:** tamanho mínimo de tópico 100; UMAP
(15 vizinhos, 5 dimensões, cosseno, semente 42); HDBSCAN; agrupamento pelos embeddings de
título + abstract; palavras-chave de cada tópico tiradas dos títulos (inglês, 1–2 palavras).
