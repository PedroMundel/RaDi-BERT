# O lote FA do RTE serve para treinar? (09/11/2026, noite)

**Pergunta:** as 2.470 justificativas do Qwen3.6-35B-A3B (variante FA) estão boas o bastante para virar alvo do
decoder no treino do Agrawal? **Quem leu:** o Claude (nível 2), a pedido do Pedro ("a análise pode fazer você e dar um
veredito"). **O Pedro não leu o lote.** Esta leitura é de um avaliador só, sem rubrica cega, e serve para decidir se
treina, não para citar.

**Como reproduzir:** `uv run --frozen python resultados/rte-35B/analise_lote_fa.py` imprime todas as contagens abaixo
e escreve `leitura-30-FA.md`, com 30 pares sorteados (15 por rótulo, semente 2026). A leitura par a par está na seção 2.

---

## 1. Contagens sobre os 2.470

| Medida | Valor | Leitura |
|---|---|---|
| Linhas, `idx` únicos, exemplos do prompt dentro | 2.470 · 2.470 · 0 | íntegro |
| Por rótulo | 1.239 entailment · 1.231 not_entailment | equilibrado |
| `finish_reason` | 2.470 `stop` | nenhuma cortada |
| Vazias · duplicadas | 0 · 0 | — |
| Palavras (depois da C): mediana · p95 · máx. | 20 · 26 · 34 | cabe com folga no teto de 64 tokens do T5 |
| Entrada do BERT (estimativa: palavras × 1,3): mediana · p95 · máx. | ~56 · ~158 · ~320 tokens | **nada passa de 512**; só 2 passam de 256 |
| Nomeiam o rótulo ("entail", "contradict") | 57 (9 · 48) | baixo, e para o decoder é inofensivo (ver 3.4) |
| Repetem palavras da pergunta ("implies", "not necessarily") | 270 | estilo, não erro |
| Eco da hipótese (nenhuma palavra de conteúdo além de H) | 2 | quase nenhum |
| Palavras novas fora de P + H, mediana | 4 | a justificativa se prende ao texto, como a FA pedia |
| Abertura "The text ..." depois da C | 433 (18%) | ver 3.1 |
| **A C cortou a abertura** | **450** | — |
| **... e deixou um verbo sem sujeito** ("X but never mentions Y") | **≥ 96** | **defeito da C, ver 3.2** |
| entailment com palavra de negação ou ressalva | 77 | sinal para ler, não erro (ver 3.3) |
| not_entailment sem nenhuma | 93 | lidos 15: os 15 defendem o rótulo certo |

## 2. Leitura de 30 pares sorteados

Para cada par perguntei: (a) a justificativa defende o rótulo certo? (b) o fato que ela usa está no texto e está
certo? (c) a frase está inteira?

| Resultado | Pares | Quantos |
|---|---|---|
| Certa, presa ao texto | 2, 3, 5, 7, 8, 13, 17, 21, 22, 23, 24, 25, 29, 30 | 14 |
| Certa, mas só reafirma a hipótese com "which means / confirming" | 1, 10, 14, 18, 20, 26 | 6 |
| Certa, com a abertura "The text discusses / describes / mentions / concerns" (a C não cobre esses verbos) | 9, 15, 19, 28 | 4 |
| Conteúdo certo, **frase quebrada pela C** | 4 ("A decline in hunting numbers but never claims..."), 11 ("He abdicated in 1946 but does not mention..."), 12 ("On specific tsunami events but does not define...") | 3 |
| Defende o rótulo, com uma imprecisão | 16 (o ministério negou a gravidade dos ferimentos, não os ferimentos) | 1 |
| **Defende o rótulo com um fato errado** | 6 (troca o título atual pelo futuro de Camilla), 27 (diz que Hitchens escreveu o romance; o autor é Reed) | **2** |
| Defende o rótulo errado | — | **0** |

Resumo: **30 de 30 defendem o rótulo certo; 27 usam o fato certo; 2 inventam ou trocam um fato (6,7%, intervalo de
95% ~2–21% com n = 30); 3 têm a frase quebrada pela nossa limpeza, não pelo Qwen.** Na mesma régua, a F do 35B errou
~3–4 em 90 no e-SNLI (leitura do Claude, 26/10). É a mesma ordem de grandeza, e com 30 pares não dá para separar.

## 3. O que a leitura achou

### 3.1 "The text" ainda abre 18%

A C cobre "states / says / notes / reports". Sobram "The text mentions / describes / discusses / concerns", que pedem
um nome depois e por isso não podem ser cortados sem quebrar a frase. **Para o treino, quase não pesa:** o decoder
aprende rápido a escrever as primeiras palavras, que são previsíveis, e o gradiente que importa vem das palavras de
conteúdo. É um custo pequeno no `L_aux` médio, não um alvo errado.

### 3.2 A limpeza C quebra frases (defeito nosso, corrigível)

O comentário da C no código diz que ela só corta quando o resto é frase inteira, mas a expressão regular não confere
isso. Dois padrões quebram:

- **verbo sem sujeito:** "The text states Titan has an atmosphere **but never mentions** its order" vira "Titan has an
  atmosphere but never mentions its order". Agora quem "não menciona" é Titã. São pelo menos 96 dos 450 cortes (o
  contador pega só os padrões "but/and/while + verbo de omissão").
- **verbo com objeto nominal:** "The text reports **on** specific tsunami events" vira "On specific tsunami events...".
  O contador não pega esse padrão, então os 96 são piso.

Um alvo agramatical ensina o decoder a escrever frase quebrada. O fato continua certo, então o dano ao BERT é
provavelmente pequeno. Mesmo assim é ruído que **nós** pusemos e que sai com uma regra mais estreita: cortar só quando
o resto não tem um segundo verbo que dependia de "the text", e não cortar "reports on". O custo é "The text" voltar em
parte dos 96. Detalhe no E5 de `docs/2026-11-09-codigo-treino-rte.md`.

### 3.3 Justificativas que discordam do rótulo: ~1%, concentradas em entailment

Dos 77 pares de entailment com negação ou ressalva, li 15. **4 argumentam pelo rótulo oposto** (idx 1945: "he may not
be American"; 1833: o texto não dá o papel de Budapeste; 2424: 40% não quer dizer o uso mais comum; 2240: o texto
"never mentions" colegas). Em pares assim o professor discorda do gabarito, e às vezes com razão: no 2424 o gabarito do
RTE é generoso. Extrapolando, são ~20 pares, perto de 1% do lote. Nos 93 de not_entailment sem negação, os 15 lidos
defendem o rótulo certo (negam por contraste: "rose, rather than dropped").

Isso é a **marca de discordância** que o Pedro adiou em 09/11 ("3/10 agora; volta se o e-SNLI der ganho pequeno ou
instável"). Com ~1% não há motivo para trazê-la de volta antes do primeiro treino.

### 3.4 Nomear o rótulo não é vazamento aqui

57 justificativas dizem "contradicts" ou "entails". No e-SNLI isso preocupava porque o decoder poderia copiar o rótulo
da justificativa. Aqui o decoder só existe no treino e o rótulo já está no `L_cls`. Na pior hipótese o `L_aux`
reforça o mesmo sinal. Não muda a avaliação, que nunca vê justificativa.

### 3.5 O que não foi checado

- Ninguém além do Claude leu. Os 3 avaliadores do Forms julgaram o e-SNLI, não o RTE.
- A estimativa de tokens é por palavras. O tokenizador de verdade entra na invariante I9 do treino.
- Não houve controle de leitura cega: eu sabia o rótulo ao ler.
- Os 20 exemplos do prompt são rascunhos do Claude (aprovados pelo Pedro como "bons") e moldam o estilo do Qwen. Eles
  não são alvo de treino, porque saem do lote. Se a pergunta à Anthropic voltar com um "não" estrito sobre saída
  usada como exemplo, isto precisa ser revisto.

---

## Correção da C feita (09/11, noite; E5 aceita pelo Pedro)

`clean_opening` passou a não cortar quando o resto tem um segundo verbo que dependia de "the text" e quando começa com
preposição ("reports on"). Os testes têm os casos de Titã, da abdicação e do tsunami. Rodando o script de novo:

| | Antes | Depois |
|---|---|---|
| Aberturas cortadas | 450 | 347 |
| Abertura "The text" que sobra | 433 (18%) | 536 (22%) |

**Não há número de "cortes que ainda quebram".** O contador antigo usava os mesmos padrões que a regra nova recusa,
então daria 0 por construção, e isso não provaria nada; ele saiu do script (o redutor de código apontou a
circularidade em 09/11). O que existe de evidência:
- os casos de teste (Titã, abdicação, tsunami, "specifies", "contains no");
- uma leitura independente da auditoria do código, que achou 4 cortes que a primeira versão da regra deixava passar
  ("and specifies", "but contains no", "and explicitly identifies", "but also ..."). A regra passou a cobri-los, e os
  cortes foram de 351 para 347.

Pode sobrar algum padrão que nem a regra nem a auditoria viram. Só uma leitura dos 347 cortes diria quantos.

O script **regerou** `leitura-30-FA.md` com a C nova. Os pares 4, 11 e 12, que a seção 2 dá como "frase quebrada pela
C", agora aparecem com a abertura original ("The text notes / states / reports on ..."). A leitura da seção 2 foi
feita sobre a versão antiga.

## Veredito

**O lote FA serve para treinar.** Nada nele bloqueia a primeira rodada:

- os 30 pares sorteados defendem o rótulo certo; ~7% trazem um fato trocado e ~1% do lote discorda do gabarito. Para
  alvo **auxiliar** com peso 0,1, que nunca é avaliado, isso é ruído tolerável. O paper do Agrawal não reporta
  qualidade das justificativas do Mixtral, então não há régua melhor para comparar;
- o tamanho e o comprimento não pedem corte nenhum.

**Uma correção antes de montar o dado de treino:** estreitar a limpeza C (E5). É defeito do nosso código, não do Qwen.
Atinge pelo menos 4% do lote, e a correção é uma regra com teste, sem gerar nada de novo.

**O que não vale fazer agora:** regerar o lote, marcar discordância ou filtrar os pares com fato errado (só daria para
achá-los lendo os 2.470). Se o braço com decoder não ganhar do BERT sozinho, a qualidade do alvo vira suspeita e a
ordem é: (1) os ~20 pares que discordam do rótulo, (2) uma leitura cega maior.
