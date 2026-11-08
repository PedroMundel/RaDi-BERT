# Relatório — Fase 1, execução 3, volta 1 (22/09/2026)

**Procedência:** tudo aqui é **nível 3** — contagens e filtros mecânicos sobre metadados (título,
ano, venue, citação, abstract) devolvidos pelas bases. **Nenhum paper foi lido**, nem por mim nem por
agente. Os números são confiáveis como contagem; nenhuma interpretação aqui decide se uma obra entra.
Quem decide é o Pedro, na Fase 3.

**Arquivos de apoio** (todos em `docs/screening/fase1/`): `2026-09-22-plano-fase1-exec3.md` (plano e
aprovações) · `2026-09-22-exec3-passo0.md` (contagens) · `2026-09-22-volta-1-funil.md` (funil e teste de
perda) · `2026-09-22-volta-1-agrupamento.md` (grupos com todos os membros) ·
`2026-09-22-volta-1-radicais.md` (filtro por radicais) · `2026-09-22-volta-1-obras.csv` (todas as
104.640 obras, com o estágio que cada uma atingiu) · `2026-09-22-volta-1-radicais-selecao.csv` ·
bruto em `raw/2026-09-22-exec3-*.json`.

---

## 1. Resumo em uma página

**O que fizemos.** Rodamos, pela terceira vez, a busca da Fase 1 do screening — agora com todas as
strings que o pool de termos gera (a string-mãe e as sete filhas), nas duas bases com API (Semantic
Scholar e arXiv), sem piso de citação. Baixamos tudo (~120 mil registros) e passamos um **filtro
mecânico** para ordenar: primeiro exigindo palavra de tipo ("survey", "review"…) e termo do pool **no
título**.

**O que achamos.**
1. O volume bruto é enorme (104.640 obras únicas), e a maior parte é inflação do Semantic Scholar:
   ele acha "review" em qualquer lugar do resumo. Exigir a palavra no **título** cortou para 33.430,
   e exigir também o termo do pool no título cortou para **2.604 surveys candidatos**.
2. **Esse filtro perde obra boa.** Testado contra 58 obras que já sabíamos serem da área, ele
   recuperou só **62%**. A sua crítica ("não estamos deixando passar conteúdo crítico?") estava certa.
3. Trocar os termos exatos por **radicais** (pedaços de palavra, como `compress` para compression,
   compressing, compressed) sobe a recuperação para **79%** numa metade de teste que não foi usada para
   ajustar nada — mas o volume dobra (5.655), e cerca de 2.100 dessas obras entram por radicais curtos
   demais, que casam com palavras sem relação (`quant` pega *quantum*).
4. As perdas que sobram revelam **lacunas no pool**: faltam `lightweight` e `embedded`, e `small
   language models` quase não casa.

**O que falta você decidir** (detalhe na seção 9): corrigir os radicais curtos; emendar o pool com as
lacunas; tipo estrito ou ampliado; e, depois, o que sobe para a volta 2 (onde começa a leitura de
abstract pela escada).

---

## 2. Onde isto está no método

O screening da Etapa 1 (`docs/screening/metodo-screening-etapa1.md`) tem quatro fases. A **Fase 1** é achar
candidatos: surveys que possam dizer quais são as divisões da área, seu vocabulário, seus conceitos,
suas ferramentas e sua história. Ela acontece em **voltas** (§11.1): cada volta pega um conjunto grande,
**ordena** (nunca apaga) e termina numa decisão sua sobre o que sobe para a volta seguinte, até o número
caber no orçamento de leitura.

A **execução 1** (21/09) mostrou que três termos de "dispositivo limitado" traziam ~94% de ruído; eles
viraram uma string separada (`edge`). A **execução 2** (21/09) rodou só a string-mãe, com piso de 60
citações, e devolveu 154 obras — você a declarou **calibração** ("só pra ter um feeling"). Esta
**execução 3** é a primeira que roda o método inteiro: todas as strings, sem piso de citação (o piso
agora só vale na hora de registrar, §3.2, porque na busca ele esconde os surveys recentes).

---

## 3. Vocabulário deste relatório

| termo | o que quer dizer aqui |
|---|---|
| **string-mãe** | a busca que descreve a área inteira: sinônimos do nome da área + palavra de tipo. |
| **string-filha** | uma busca por grupo do pool (compressão, edge, ferramentas…), para achar o que a mãe não pega. |
| **bruto** | tudo o que a base devolveu, sem filtro nenhum. Fica guardado para sempre (regra "ordena, não apaga"). |
| **dedup** | juntar registros que são a mesma obra (mesmo DOI, mesmo arXiv id ou mesmo id do Semantic Scholar). |
| **estágio** | até onde uma obra chegou no filtro mecânico (1, 2 ou 3). Estágio não é decisão; é ordem. |
| **recuperação** (*recall*) | de um conjunto de obras que sabemos serem boas, que fração o filtro deixa passar. 62% = de cada 10 boas, perdemos ~4. |
| **conjunto de referência** | obras que já sabemos serem da área, usadas como gabarito para medir a recuperação. |
| **ajuste × teste** | dividimos o gabarito em duas metades: uma pode ser olhada para ajustar o filtro; a outra só serve para medir. Se medíssemos na mesma metade que olhamos, o número sairia otimista — o filtro "decoraria" o gabarito. |
| **radical** | o pedaço comum de uma família de palavras (`compress` em compression/compressing/compressed). Casar por radical pega variações de escrita que o termo exato perde. |
| **ruído** | obra que passa no filtro mas não é da área (ex.: survey de computação quântica passando por causa de `quant`). |

---

## 4. Passo 0 — medir antes de baixar

**Por quê.** Antes de baixar qualquer coisa, contamos quantos resultados cada string devolveria. Você
tinha pedido para decidir sobre números, e o tamanho de cada string decide o custo do resto.

**Como.** As strings foram **geradas direto do pool** (termo + variantes de cada grupo), não escritas
à mão — assim a busca não diverge do vocabulário registrado. Todas levam a palavra de tipo, menos a
filha `ferramentas`, que procura paper de sistema (vLLM, TensorRT…), e paper de sistema não se chama
"survey". Filtros: 2020 em diante, Ciência da Computação (S2) ou cs.CL/cs.LG/cs.AI (arXiv).

**Resultado.**

| string | Semantic Scholar | arXiv |
|---|---|---|
| mãe (forma da execução 2, para conferência) | 863 | 99 |
| mãe (com todas as variantes do pool) | 2.561 | 193 |
| edge | 42.202 | 396 |
| compressão | 9.141 | 385 |
| inferência/serving | 579 | 43 |
| ferramentas (sem palavra de tipo) | 13.201 | 1.496 |
| dado/confiança | 7.490 | 305 |
| adaptação | 1.322 | 899 |
| arquiteturas | 24.107 | 1.232 |
| uso? | 12.643 | 532 |

**Como ler.**
- A primeira linha reproduz exatamente os 863 medidos antes — prova de que a string gerada do pool é
  a mesma.
- **O Semantic Scholar devolve de 10 a 100 vezes mais que o arXiv.** Duas causas: no S2 a palavra de
  tipo pode estar no **resumo** ("we review the literature…"), no arXiv exigimos no **título**; e
  "Ciência da Computação" no S2 inclui redes, IoT e aplicações, enquanto o arXiv foi restrito a três
  categorias de IA. A etiqueta "Review" do próprio S2 quase não ajuda (863 -> 819).
- **As variantes da mãe triplicam o volume** (863 -> 2.561): variantes soltas como "compressing" e
  "compression techniques" casam com muita coisa.
- **`edge` repete o ruído da execução 1** (42 mil): "resource-constrained" e "edge devices" aparecem
  em IoT, redes e sensores.

---

## 5. Passo 1 — baixar o bruto

**O que.** Tudo de todas as strings, sem filtro, com título, ano, venue, citações, identificadores e
abstract. **119.686 registros**, 343 MB de JSON (acima da minha estimativa de 100–200 MB).
Nenhum PDF foi baixado.

**Incidentes, para registro:**
- O arXiv dá erro interno quando se pede "zero resultados" só para ler o total — resolvido pedindo 1.
- Um falso alarme parou o download: o detector de erro procurava a palavra "Error" num título, e um
  paper legítimo tinha título começando por "Error…". Corrigido; o download retomou de onde parou.
- **Correção de um fato registrado antes:** o Semantic Scholar **devolve o abstract** quando ele é
  pedido. A execução 2 é que não pedia. O CLAUDE.md e o método foram corrigidos.

**Sobreposição das bases** (depois do dedup): 100.114 obras só no S2 · 3.316 nas duas · 1.210 só no
arXiv. O arXiv acrescenta pouco de novo; quase tudo o que ele acha o S2 também acha.

---

## 6. Volta 1 — o filtro de título

**Como funciona, com exemplo.** Cada obra passa por três perguntas, em ordem:
1. O título tem palavra de tipo (survey, review, overview, taxonomy)? — *"A Survey on Efficient
   Inference for LLMs"* sim; *"Sparsity in Deep Learning: Pruning and growth…"* não.
2. O título tem um termo do pool? — *"A Survey on Efficient Inference…"* tem `efficient inference`.
3. Quantos grupos do pool a obra toca (título + abstract)? — usado só para ordenar.

Quem responde sim a 1 e 2 chega ao **estágio 3**. A filha `ferramentas` segue uma trilha própria: como
paper de sistema não tem "survey" no título, ela só precisa do termo do pool.

**Funil.**

| etapa | obras |
|---|---|
| registros baixados | 119.686 |
| obras únicas (dedup) | 104.640 |
| trilha survey, com palavra de tipo no título | 33.430 |
| **trilha survey, estágio 3** (tipo + termo no título) | **2.604** |
| trilha ferramentas, estágio 3 (termo no título) | 3.413 (de 13.209) |

**O que há dentro dos 2.604.**

| recorte | obras | o que significa |
|---|---|---|
| só `arquiteturas` no título | 1.174 | "transformer" aparece em survey de qualquer assunto (visão, medicina, séries temporais). É o grupo do pilar de arquiteturas, não da área de eficiência. |
| algum grupo núcleo | 893 | `área`, `compressão`, `inferência/serving`, `adaptação` ou `edge` — o coração da especialização. |
| só `dado/confiança` | 339 | calibração, poucos rótulos — eixo (iii) de §1.2. |
| só `uso?` | 187 | prompting, MLOps, deployment — termos ainda "a testar". |

**Uma observação sobre a ordenação.** Ordenar por "quantos grupos a obra toca" pôs no topo um survey
de diagnóstico médico com LLM em hospital de poucos recursos — ele toca muitos termos sem ser da área.
É sinal fraco: serve para ordenar dentro de um recorte, não para escolher o recorte.

---

## 7. Sua crítica, e o teste de perda

**A pergunta:** exigir o termo no título não deixa passar obra importante que não tem o termo no
título?

**Como respondemos com número.** Precisávamos de um **gabarito**: obras que sabemos serem da área,
obtidas por outro caminho que não este filtro. Usamos as **58 obras "entra" da execução 2** — julgadas
dentro da área por título em 21/09, num processo independente deste filtro. 57 delas estão no bruto
da execução 3. A pergunta vira: quantas das 57 o filtro deixa passar?

**Resultado: 36 de 58 (62%).** Perde ~4 em cada 10. Os dois modos de perda:

| modo | quantas | exemplos |
|---|---|---|
| **o título não tem palavra de tipo** | 8 | *Sparsity in Deep Learning: Pruning and growth for efficient inference…* (1.019 citações — um dos surveys mais citados da área); *Large Language Model Inference Acceleration: A Comprehensive Hardware Perspective* |
| **o título usa forma diferente do termo do pool** | 13 | *A Survey on **Transformer Compression*** — o pool tem `model compression`, o título diz "transformer compression"; *A Review on **Edge LLMs***; *LLM **Inference** Unveiled*; *A Survey on **Green** Deep Learning* |
| identificador divergente | 1 | *Efficient Large Language Models: A Survey* |

**Por que não usar o abstract no lugar do título.** Testamos: 3.794 obras do estágio 2 têm termo da
área no abstract, e as mais citadas entre elas são *A Survey on Vision Transformer*, *YOLOv11*,
*Industry 5.0* — ruído. Quase todo abstract de IA menciona eficiência de passagem. O abstract serve
para **julgar** (é o primeiro degrau da escada, na volta 2), mas é fraco para **cortar** 100 mil obras
por palavra.

**Ressalva sobre o gabarito:** as 58 foram julgadas por título, em nível 3. São um gabarito razoável,
não perfeito — e pequeno.

---

## 8. Radicais — a correção aprovada, e o que ela mostrou

**A ideia.** Em vez de exigir o termo exato (`model compression`), aceitar qualquer palavra da mesma
família (`compress…`). Isso resolve o modo de perda nº 2.

**O cuidado com o gabarito.** Eu já tinha visto quais obras o filtro perdia. Se escolhesse os radicais
olhando essas perdas e depois medisse nas mesmas obras, o número sairia inflado — eu estaria ajustando
a resposta à prova. Por isso:
1. os radicais foram **gerados mecanicamente** das palavras dos termos dos grupos núcleo do pool,
   tirando uma **lista de palavras genéricas** (model, language, deep, network, attention…) fixada
   antes do teste;
2. o gabarito foi **dividido por sorteio** (semente 42) em metade de ajuste (28) e metade de teste
   (29); **o número que vale é o da metade de teste.**

Ressalva honesta: como eu já tinha visto as perdas, a lista de genéricas não é "cega" — mas não foi
ajustada ao teste.

**Resultado, na metade de teste:**

| filtro | selecionadas | recuperação no teste |
|---|---|---|
| atual (termo exato) | 2.604 | 19/29 — 66% |
| tipo + radical | 5.655 | **23/29 — 79%** |
| tipo ampliado (+ perspective, trends, challenges) + radical | 6.285 | 24/29 — 83% |

**O problema: o volume dobrou, e boa parte é ruído do meu corte de sufixo.** O corte automático deixou
alguns radicais curtos demais:

| radical | casa com |
|---|---|
| `quant` (de *quantization*) | **quantum** (254 títulos), quantitative, quantification |
| `factor` (de *factorization*) | **factors** (120) |
| `mobil`, `limit`, `early`, `depth`, `adapt` | palavras comuns em qualquer título |

**2.100 das 5.655** seleções se apoiam só num desses. Esse diagnóstico foi feito olhando a
**seleção**, não o gabarito — então corrigi-lo não contamina o teste.

**O que as perdas restantes ensinam — lacunas do pool.** As 6 que o filtro por radical ainda perde:
- *Lightweight Deep Learning: An Overview* — **`lightweight` não existe no pool**;
- *A Survey of Small Language Models* — "small" e "language" foram para a lista de genéricas, então
  só a sigla SLM casa;
- *Resource-Efficient Neural Networks for **Embedded** Systems* e *Enable Deep Learning on Mobile
  Devices* — sem palavra de tipo no título; **`embedded` não existe no pool**;
- *Adaptive Inference through Early-Exit Networks* e *Data-Free Knowledge Transfer* — formas que
  nenhum filtro de palavra pega.

É exatamente a direção (b) da regra de revisão do pool (pool §3): **lacuna vista no retorno -> o pool
ganha termo**. E o que nenhum filtro pega é o que a **bola de neve** existe para recuperar: surveys
muito citados, como o de esparsidade (1.019 citações), voltam porque outros surveys os citam.

---

## 9. Decisões pendentes

| # | decisão | opções | consequência |
|---|---|---|---|
| **D1** | corrigir os radicais curtos | (a) regra mecânica: radical com mínimo de 6 letras; radical curto só vale por igualdade exata (`quantiz`, `factoriz`) · (b) deixar como está | (a) deve tirar boa parte dos ~2.100 ruidosos; mede-se de novo na mesma metade de teste |
| **D2 — FEITO (22/09)** | emendar o pool (emenda 5, direção b) | `lightweight` e `embedded` entraram no grupo `edge`; *small language models* já estava no pool (a perda foi do filtro) | os dois termos novos ainda não rodaram |
| **D3** | tipo estrito ou ampliado | estrito (79%) · ampliado (83%, +630 obras) | ampliado pega "perspective/trends/challenges", que às vezes são surveys e às vezes não |
| **D4** | o que sobe para a volta 2 | núcleo · +`dado/confiança` · +`uso?` · `arquiteturas` com critério de §1.1 · trilha ferramentas com critério próprio | é aqui que começa a leitura de abstract; o custo depende do número |
| **D5** | quem aplica a escada na volta 2 | eu, nesta conversa · agentes com roteiro fixo | consistência × custo; risco "Agrawal" com agentes |

**Candidatos a apagar** (nada apagado): bruto da execução 1 (36 MB, string suja, já declarada fora da
população). Arquivos de trabalho desta volta que ficarão obsoletos depois da D1:
`2026-09-22-volta-1-radicais-selecao.csv`.

---

## 10. Limites deste relatório

- **Nível 3.** Nada foi lido. "Da área" aqui quer dizer "o título tem as palavras certas".
- **O gabarito é pequeno (58) e foi julgado por título.** A recuperação medida é indicativa, com
  margem larga: com 29 obras de teste, um acerto a mais ou a menos muda o número em ~3 pontos.
- **Sem Google Scholar** (decisão sua, "talvez depois") e **ACL só pelo Semantic Scholar**.
- **Os scripts** que geraram tudo isto estão no scratchpad da sessão (temporário). Se você quiser que
  a busca seja reproduzível por outra pessoa, eles precisam ir para o projeto — decisão sua.

**Atualização 22/09:** Pedro — *"deixe tudo igual, só preencha as lacunas do pool que foram reveladas"*. Feito como emenda 5 do pool; D1, D3, D4, D5 e os filtros desta volta ficam como estão.
