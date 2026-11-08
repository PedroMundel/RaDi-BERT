# Fase 1, execução 3 — plano (22/09/2026)

**Status: PLANO, NÃO EXECUTADO.** Ordem do Pedro (22/09): *"não dispara a fase 1 antes de me dizer o
que você vai fazer nela"*. Nada abaixo roda antes da aprovação dele. As perguntas marcadas **P1–P6**
são decisões dele; nenhuma foi preenchida por default.

**Base:** método v3.7 (§11 Fase 1, §11.1 voltas, §6.1 escada, §1.2 + §1.2.1, §3.2, §3.4) e pool v0
emendas 1–4 (§2 composição, §4 strings). A execução 2 (21/09) foi calibração e **não** é entrada.

---

## O que a Fase 1 faz, pelo método

Três fontes de candidatos (§11 Fase 1): **(1)** string-mãe + 7 strings-filhas nas bases ·
**(2)** ementas dos 3 cursos de §4.1 · **(3)** bola de neve pelas referências dos surveys que
entrarem (uma rodada). Tudo em voltas (§11.1): bruto -> dedup -> triagem pela escada -> proposta de
agrupamento -> **decisão do Pedro** -> volta seguinte. Saída: lista de surveys candidatos com decisão
por obra + relato de funil. O alvo de 05/10 vai até o mapa v1 (Fases 1–3).

## Passo 0 — medir antes de baixar (custo: minutos, só contagem)

Rodar **cada string só para ler o total**, sem baixar registros, e entregar uma tabela:

| string | S2 (sem piso, 2020+, CS) | arXiv (2020+) |
|---|---|---|
| mãe | 863 (já medido) | ? |
| filha `edge` | ? | ? |
| filha `compressão` | ? | ? |
| filha `inferência/serving` | ? | ? |
| filha `ferramentas` (**sem** `filtro-tipo`) | ? | ? |
| filha `dado/confiança` | ? | ? |
| filha `adaptação` | ? | ? |
| filha `arquiteturas` | ? | ? |
| filha `uso?` | ? | ? |

Motivo: filhas como `compressão` (quantization | pruning | sparsity + review) e `arquiteturas`
(transformers + review) podem voltar com milhares. O tamanho de cada uma decide o resto do plano, e
você quer decidir sobre números. **Paro aqui e te mostro a tabela.**

## Passo 1 — bruto (depois da sua aprovação sobre o passo 0)

- Baixar o retorno completo das strings aprovadas, **sem filtro**, para `screening/fase1/raw/`
  com data, versão do pool e query no cabeçalho (padrão das execuções 1 e 2).
- Buscar os **abstracts** já nesta etapa, porque a escada começa por eles: S2 `paper/batch` com
  o campo `abstract`; arXiv API para quem tem arXiv id; OpenAlex para quem só tem DOI (N4).
- Dedup por identificador (DOI / arXiv id / paperId do S2), guardando **em que strings e bases cada
  obra apareceu** — esse cruzamento é dado para a revisão do pool (ruído, direção a).

## Passo 2 — triagem, volta 1 (nível 3)

- Pela escada de §6.1: **abstract -> introdução -> conclusão**; o degrau em que decidiu vai no registro.
- Critérios: §1.2 + §1.2.1 (pertencimento de survey), §3.4 (não é survey), §3.2 (piso 60 **no
  registro**, venue revisado ou citação cruzada).
- Decisões possíveis por obra: entra · não entra — sem filtro de qualidade · espera divisão (§1.2.1 c)
  · fora (com a letra da regra) · não é survey (com o destino de §3.4) · dúvida (topo da escada).
- **Ordena, não apaga**: tudo fica no bruto com motivo e volta em que caiu.

## Passo 3 — entregas da volta 1

1. `screening/fase1/<data>-volta-1-funil.md` — **relato de funil** (L1): bruto por base e string ->
   após dedup -> por decisão -> por grupo.
2. `screening/fase1/<data>-volta-1-candidatos.md` — decisão por obra, com o degrau.
3. `screening/fase1/<data>-volta-1-agrupamento.md` — **proposta** de agrupamento (§11.1, quatro
   salvaguardas: ordena e não apaga; membros sempre visíveis; proposta nível 3; agrupamento não é
   divisão).
4. Retorno por termo do pool — revisão por evidência (a) ruído, se algum termo poluir.
5. Primeira versão do bubble plot A **não** sai aqui: ele depende da extração (Fase 2).

Depois: **sua decisão** sobre a volta 1 -> volta 2 (se necessária) -> bola de neve sobre os que
entraram -> ementas.

---

## Perguntas para o Pedro antes de executar

- **P1. Bases.** O método lista arXiv · ACL Anthology · Semantic Scholar · Google Scholar.
  - ACL Anthology não tem API de busca; o S2 indexa os venues da ACL. Cobrir a ACL **pelo S2**, ou
    procurar outra rota?
  - Google Scholar é **manual** e bloqueia automação (CAPTCHA — eu não posso contornar). Você roda a
    string de §4.1 na interface e me passa o resultado, ou fica para uma volta posterior?
- **P2. A filha `arquiteturas`.** O grupo é o **pilar fixo** de §1.1 (transformer, atenção, encoder/
  decoder), **não** a área de eficiência. Se eu a triar por §1.2 ("reduz custo de implantação?"),
  quase tudo cai fora. Triar essa filha contra **§1.1** (cobre um conceito do pilar arquiteturas?) em
  vez de §1.2?
- **P3. A filha `uso?`.** Os três termos (prompt engineering, MLOps, model deployment) estão marcados
  "testar §1.2". Rodar na volta 1 e levar o teste para você, ou esperar o mapa?
- **P4. Quem faz a triagem.** A escada exige ler abstract (e às vezes introdução) de centenas a
  milhares de obras — é leitura de modelo, não script. Opções: eu na conversa principal (mais caro de
  contexto, mais consistente) ou agentes em paralelo com um roteiro fixo de critérios (mais barato,
  risco de critério aplicado de forma desigual — o risco do Agrawal). O custo depende do passo 0.
- **P5. Quando rodam as ementas e a bola de neve.** Depois da volta 1 (sobre os que entraram), como
  está acima, ou as ementas já na volta 1 (independem da busca)?
- **P6. Tamanho da volta.** Se o passo 0 mostrar milhares, triar tudo na volta 1, ou a volta 1 é a
  mãe + filhas pequenas, e as grandes entram na volta 2?

---

## Passo 0 feito (22/09) — ver `2026-09-22-exec3-passo0.md`. Proposta de próximo passo (NÃO aprovada)

Pedro (22/09): *"falei que ia retornar milhares de docs"* — o volume é o esperado pelo desenho do
funil por voltas (F, 22/09: "3000 -> filtragem por keywords -> resumo -> grupos -> decisão minha").

**Passo 1 — baixar o bruto completo** de todas as strings, nas duas bases: metadados (título, ano,
venue, citações, ids, abstract quando a base der), sem filtro. Estimativa: ~113 mil registros S2 +
~5,5 mil arXiv, antes do dedup; ordem de 100–200 MB em JSON. Motivo de baixar tudo em vez de cortar
termo antes: a cláusula anti-viés (pool §3) obriga termo ruidoso a rodar na filha — o bruto dele
precisa existir de qualquer forma.

**Volta 1 — filtro mecânico, reprodutível, que ORDENA** (sem leitura de modelo; a escada entra na
volta 2, quando o número couber):
1. dedup por DOI / arXiv id / paperId;
2. palavra de tipo **no título** (iguala o S2 ao arXiv — ataca a causa (a) do passo 0);
3. termo do pool no título;
4. ordenação por quantos grupos do pool a obra atravessa;
5. relato de funil + agrupamento proposto **por grupo do pool x ano** (mecânico, não por tema).

**Decisão do Pedro no fim da volta 1:** quais grupos/faixas sobem para a volta 2 (escada, nível 3).

**APROVADO pelo Pedro (22/09):** passo 1 + volta 1 como propostos. **P1:** ACL pelo S2; Google Scholar
não incluído ("talvez depois"). Passo 1 lançado em 22/09. Achado no teste: o S2 bulk **devolve
abstract** quando o campo é pedido (159/177 no teste) — a execução 2 é que não o pedia.

**Crítica do Pedro ao filtro de título (22/09)** e medição: ver fim de `2026-09-22-volta-1-funil.md`
(62% de recuperação contra a referência da execução 2). Proposta em 3 partes: (1) radicais no título,
(2) bola de neve como rede de segurança, (3) conjunto de referência independente para medir
recuperação por volta. **Pedro sobre (3) com ementas:** *"só ementa de curso que não sei se vou
colocar ainda, meu curso mesmo devia ter umas 5 matérias importantes, no máximo"* — dúvida sobre
ementa como fonte (vale também para a fonte (2) da Fase 1, §4.1). Pendente: confirmar (1) e (2);
escolher a fonte do conjunto de referência.

**Pedro (22/09) — a estratégia daqui para frente, nas palavras dele:** *"Vai ser isso mesmo, 105k obras.
Imagine como uma floresta inteira que a gente quer apenas os cajuzeiros. As 105k obras são a floresta
inteira. Depois, a gente vai ter que descobrir o que é lixo (outras áreas, como química, física,
matemática..., as que não têm a ver com o assunto (como quantum no radical quant)) e ir filtrando
cada vez mais pra descobrir onde os cajuzeiros estão."* Ordem: *"deixe tudo igual, só preencha as
lacunas do pool que foram reveladas. Roda a F1 pela última vez."* -> emenda 5 do pool; só a string
`edge` mudou e foi baixada de novo (a antiga ficou como `raw/*-edge-emenda4.superado.json`); as outras
nove strings são idênticas e não foram rebaixadas.
