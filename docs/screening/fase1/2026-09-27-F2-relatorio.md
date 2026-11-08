# F2 — amostragem por grupo com a cadeia de agentes: relatório (27/09)

**Procedência: nível 3.** Vereditos de agentes: Haiku leu título e abstract (agentes 1 e 2), Sonnet leu só as frases
transcritas (agente 3). Ninguém leu as obras. **Nada foi gravado na tabela-mestra:** a proposta por grupo (§4)
espera a sua revisão grupo a grupo, como manda a regra de 23/09.

## 1. O que foi feito

A F2 decide **grupos inteiros** a partir de uma amostra lida pela cadeia de agentes calibrada em 26/09. A amostra
seguiu a tabela decidida em 23/09 (50 / 40 / 30 / 30% / tudo, conforme o tamanho do grupo).

| Item | Número |
|---|---|
| Entrada da F2 (decisões da F1 de 24/09) | 12.506 obras em 63 grupos |
| Sorteadas (semente 2609) | **962**: 363 em 11 grupos amostrados + 599 em 52 grupos pequenos, lidos inteiros |
| Sem abstract depois de todas as rotas | **165 (17%)** — lista `F2/sem-acesso.md` |
| Agente 1 (Haiku, 25 lotes) | 250 claramente fora |
| Agente 2 (Haiku) | 2.207 frases; **4,1% não verbatim** (eram 10% na calibração; a v2 do roteiro reduziu) |
| Agente 3 (Sonnet) | **55 relevante · 157 dúvida · 335 fora** |
| Objetivo (entre as relevantes) | 38 `saber` · 17 `saber + saber fazer` · 0 só `saber fazer` |
| Dupla leitura (97 obras, cadeia independente) | concordância exata 78/97 (80%); **segue × fora: 84/97 (87%)** |

**Como ler "dúvida":** 122 das 157 dúvidas são a regra §1.2.1 (c), *aplicação específica* (compressão para YOLO,
IA embarcada em agricultura etc.), que o roteiro manda marcar como dúvida porque só entra se nenhum survey geral
cobrir a divisão. **Dúvida aqui quase nunca é "frase insuficiente"**; é "aplicação específica, esperando o mapa".

**Motivos de "fora" (agente 3; 333 dos 335 têm regra classificável):** não é survey 166 (fora da área 74, primário da área 43) · sem eixo de §1.2 / fora
da área 134 · CNN/GNN/difusão (b) 23 · §1.3 modelo fora de escopo 6 · treino puro 4.

## 2. Achado 1: a F2 quase não filtrou

A regra do três só derruba grupo com **zero** relevantes na amostra. Os grupos grandes são misturados: todos têm
alguma relevante. Resultado: **1 grupo desce** (o 9, com 55 obras) e **11,5 mil obras não lidas continuam**.

| Grupo | Obras | Amostra | Lidas | Relevante | Dúvida | Fora | Sem acesso | Taxa de relevante (IC 95%, Wilson) | Relevantes estimadas | Proposta |
|---|---|---|---|---|---|---|---|---|---|---|
| 2 | 3.988 | 50 | 44 | 8 | 5 | 31 | 6 | 18% (10–32%) | ~725 | segue |
| 5 | 3.134 | 50 | 46 | 3 | 3 | 40 | 4 | 7% (2–18%) | ~204 | segue |
| 43 | 998 | 40 | **8** | 1 | 0 | 7 | **32** | 12% (2–47%) | ~125 (sem valor) | segue — **ver §3** |
| 52 | 870 | 40 | 38 | 2 | 2 | 34 | 2 | 5% (1–17%) | ~46 | segue |
| 16 | 774 | 30 | 29 | 2 | 2 | 25 | 1 | 7% (2–22%) | ~53 | segue |
| 36 | 734 | 30 | 29 | 4 | 3 | 22 | 1 | 14% (5–31%) | ~101 | segue |
| 46 | 597 | 30 | 24 | 4 | 2 | 18 | 6 | 17% (7–36%) | ~100 | segue |
| 49 | 461 | 30 | 23 | 3 | 3 | 17 | 7 | 13% (5–32%) | ~60 | segue |
| 1 | 239 | 30 | 25 | **0** | 4 | 21 | 5 | 0% (0–13%) | ~0 | segue **só pelas dúvidas (c)** |
| 14 | 57 | 17 | 14 | **0** | 3 | 11 | 3 | 0% (0–22%) | ~0 | segue **só pelas dúvidas (c)** |
| 9 | 55 | 16 | 15 | 0 | 0 | 15 | 1 | 0% (0–20%) | 0 | **desce inteiro** |
| 52 grupos pequenos | 599 | tudo | 502 | 28 | 130 | 344 | 97 | — | — | cada obra segue o próprio veredito |

**Estimativa:** cerca de **1.400 surveys relevantes** nos grupos que seguem (cerca de 2.400 contando as dúvidas).
O alvo provisório do método é de **~50 documentos** (⟨rev-31⟩). A F3 como desenhada (keywording sobre o que sobrou)
teria de trabalhar sobre **11.505 obras** para achar essas ~1.400.

**Custo medido:** a cadeia completa gastou cerca de 7,3 milhões de tokens de subagente para 962 obras (~7,6 mil por
obra). Rodar a mesma cadeia sobre 11.505 obras custaria **cerca de 87 milhões de tokens**. Na F2, o limite de uso
estourou duas vezes com 7 a 13 milhões; seriam uma dúzia de janelas de limite.

## 3. Achado 2: o grupo 43 não foi lido

32 das 40 obras sorteadas não têm abstract em nenhuma rota. Os títulos parecem metadado ruim: editoriais ("Guest
Editorial Note"), páginas de repositório ("BIROn - Birkbeck Institutional Research Online"), planos de teste, nomes
de revista. Com 8 lidas, a regra do três não decide nada (o intervalo vai de 2% a 47%). Ele "segue" só porque 1 das 8
é relevante.

## 4. Achado 3: a F1 funcionou e o piso de citação não

Taxa de relevante na amostra, por situação na F1 (sem os `sem acesso`):

| Situação na F1 | Lidas | Relevante | Dúvida |
|---|---|---|---|
| ligada | 263 | 28 (**11%**) | 63 |
| sem dado de citação | 124 | 14 (**11%**) | 28 |
| solta recente (2025-26) | 175 | 11 (6%) | 41 |
| solta (desce), com palavra de tipo | 235 | 2 (**0,9%**) | 25 |

A decisão de 24/09 de mandar só as que desceram com palavra de tipo foi prudente: mesmo essas rendem menos de 1%.

**Piso de 60 citações:** 3 relevantes em 53 lidas com >= 60 (6%) contra 52 em 744 abaixo de 60 (7%). O piso **não
concentra** relevância. Além disso, 52% do que sobrou é de 2025-26 e ainda não teve tempo de ser citado. É mais uma
confirmação do registro de 22/09 no Rejected ("piso é idade disfarçada de qualidade").

## 5. Qualidade da cadeia

- **Dupla leitura:** 13 discordâncias entre seguir e sair, todas de borda: CNN leve para detecção (b × c), um survey de
  RAG, serverless (d), realidade aumentada embarcada. Não há padrão de erro sistemático. Em 2 casos o agente 1 tirou
  obras que a outra cadeia marcou como dúvida (patologia de fachadas por drone; otimização esparsa em matemática);
  as duas estão, pelo título, fora da área.
- **Não verbatim:** 91 frases (4,1%) ficaram marcadas. Nenhuma foi apagada.
- **Incidentes de execução (registrados em `docs/residencia/AUTONOMIA.md`):** o limite de uso derrubou 12 agentes; a retomada do
  workflow não reaproveitou o cache e rodou de novo parte dos agentes. O "JSON inválido" de 14 arquivos era só BOM
  (e uma barra de LaTeX), corrigido na leitura, sem relançar nada. Só o agente 3 do lote 20 rodou sozinho depois.

## 6. Decisões suas

1. **Grupos 1 e 14 (0 relevantes, só dúvidas (c)):** seguem (a dúvida conta, variante A) ou descem (só relevante
   conta, variante B)? A diferença é de 256 obras (11.717 × 11.461 para a F3).
2. **Grupo 43 (32 de 40 sem acesso):** segue como está, desce como metadado ruim, ou sorteio mais 40 dele para tentar
   ler?
3. **Como chegar de ~11,5 mil para ~50.** A F3 como desenhada custa ~87 milhões de tokens. Caminhos com número:
   - **(a) Ordem pela F1 antes da F3:** processar primeiro `ligada` e `sem dado de citação` (11% de relevante) e deixar
     `solta (desce)` (0,9%) para o fim. Não reduz o total, só a ordem.
   - **(b) Nova divisão por subgrupo dentro dos grupos 2 e 5** (7.122 obras, 62% do que sobrou), com nova amostra
     por subgrupo. É a mesma lógica da F2, um nível abaixo, e custaria outra F2 (~7 milhões de tokens).
   - **(c) Trocar o alvo da F3:** em vez de keywording sobre 11,5 mil obras, keywording só sobre as **55 relevantes +
     157 dúvidas já lidas**, para nascer o esquema de categorias; depois classificar o resto pelo esquema com um
     agente mais barato (só título).
   - **(d) Parar de filtrar por agente:** usar as 55 relevantes da F2 + o gabarito como conjunto inicial e ir para a
     **bola de neve** (Wohlin), que o método já prevê.
   Não escolhi nenhum; a decisão é sua.
4. **Auditoria:** 30 vereditos sorteados em `F2/auditoria.md`, cada um com a frase usada e o abstract completo para
   você conferir.
5. **Sem acesso:** 165 obras (92 com termo núcleo no título) em `F2/sem-acesso.md`. A rota de PDF aberto ainda não
   foi tentada.

## 7. Arquivos

`docs/screening/fase1/F2/`: `entrada.json` (962 obras) · `mapa.json` (id -> obra e grupo) · `a1/`, `a2/`, `a3/` (saída por
lote; `*-v1-invalido.json` são as primeiras tentativas dos lotes refeitos, guardadas) · `dupla/` · `consolidado.json`
· **`vereditos.csv`** (uma linha por obra: veredito, regra, objetivo, frase, rotas de acesso) · `sem-acesso.md` ·
`auditoria.md` · `ESTADO.md` (checkpoint). Scripts em `scripts/screening/agentes/`: `f2_prep.py`, `f2_rotas_extra.py`,
`f2_consolida.py`, `f2_artefatos.py`. Roteiros: `docs/screening/agentes/roteiro-agente-{1,2,3}` (2 em v2).

## 8. Adendo (27/09): o erro de desenho da F2

Diagnóstico depois da pergunta do Pedro ("fez isso tudo e ainda tem as mesmas 11k obras?"): **não é bug, é desenho.**
A regra do três por grupo só derruba grupo com zero relevantes. Com ~7% de relevância, 50 sorteadas trazem zero
só em 2,6% das vezes. E o maior grupo é a própria área (21 das 28 obras de ajuste do gabarito no grupo 2). Como a
camada B já tinha tirado os grupos de fora, a F2 repetiu o mesmo filtro na mesma unidade. **Isso era calculável
antes de rodar**, e não foi calculado. A regra que nasce daqui ("contrato de funil") e o plano que substitui a F3
estão em `2026-09-27-plano-classificador.md`. As decisões 1 e 2 do §6 perdem o objeto com esse plano.
