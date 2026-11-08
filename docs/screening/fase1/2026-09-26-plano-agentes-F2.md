# Plano de execução dos agentes: calibração (M4) e F2 (26/09)

**Status: plano. Nada rodou.** Pedido do Pedro (26/09): "vamos rodar os agentes". A regra dele é plano antes
de execução. Base: `2026-09-23-desenho-agentes.md` (M1–M6 decididos em 23/09) e as decisões da F1 de 24/09.

## 1. Critério novo do Pedro (26/09): os três objetivos

Nas palavras dele, as obras servem a três objetivos pessoais, ou a uma combinação deles:

1. **Saber**: conhecimento geral ou especializado; compreensão profunda das informações que recebe.
2. **Saber fazer**: demonstração prática do conhecimento para realizar atividades em contextos diferentes.
3. **Saber ser**: habilidades vistas no comportamento e no cotidiano, que mostram domínio pleno de uma área.
   *"Obras não ensinam isso; aprender com elas gera conhecimento para saber ser."*

**Como isso entra nos agentes: decisão do Pedro (§5, perguntas 1 e 2).** A proposta está em §3.

## 2. Os números

| Item | Obras |
|---|---|
| Entrada da F2 | **12.506**: ligada 6.228 + solta recente 2.350 + sem dado de citação 2.714 + desceram com palavra de tipo 1.214 |
| Grupos (camada B, grupo final) | 63: 2 com >= 1.000 · 2 com 800–999 · 5 com 100–799 · 2 com 50–99 · **52 com < 50 (leitura de tudo)** |
| **Leituras da F2** (tabela de amostra decidida em 23/09) | **962** |
| Sem abstract na entrada | 2.184 de 12.506 (17%). Na amostra, passam pelas rotas do M6 antes de qualquer veredito |
| Calibração (M4) | 58: as 28 de ajuste do gabarito + 30 sorteadas do lixo da camada A |

Os penúltimos (125) e os golden (3) não passam pela F2: vão para F3 e F4, como decidido.

## 3. Proposta para os três objetivos (a confirmar)

- O agente 3 ganha **um campo a mais**, `objetivo`, com um valor para cada obra que ele julgar relevante:
  `saber` · `saber fazer` · `saber + saber fazer` · `não dá para dizer pelo resumo`. Ele justifica com a frase
  transcrita, como já faz com o veredito.
- O rótulo **ordena, não filtra**. O veredito (relevante / fora / dúvida) continua saindo só das regras do
  método (§1.2, §1.2.1, §3.4).
- **Saber ser não vira rótulo de obra.** Pela sua própria frase, a obra não ensina isso. Proposta: registrar o
  saber ser **fora do screening**, como reflexão sua sobre o que leu (por exemplo, uma linha nas notas de
  leitura: "o que isso muda no modo como eu trabalho").
- Pistas de `saber fazer` que o agente procura: código ou ferramenta disponibilizada, tutorial, guia
  prático, benchmark reproduzível, estudo de caso de implantação, "lessons learned".

**Consequência que precisa ser dita:** a população do screening é **survey**, e survey serve sobretudo ao
**saber**. O **saber fazer** mora nos papers de sistema e de ferramenta, que o método já manda buscar fora de
survey (⟨rev-29⟩, filha `ferramentas`), e nos primários, que voltam como seminais (§3.4). Se o rótulo mostrar
pouco `saber fazer` na F2, isso é esperado pela construção, não defeito da busca.

## 4. Ordem de execução

| Passo | O quê | Agentes | Chamadas (aprox.) | Sai |
|---|---|---|---|---|
| 0 | Roteiros versionados dos 3 agentes (regras do método copiadas + exemplos do gabarito de ajuste + campo `objetivo`) | — | — | `docs/screening/agentes/roteiro-agente-{1,2,3}-v1.md` |
| 1 | **Calibração M4** sobre as 58 | 1 Haiku · 2 Haiku · 3 Sonnet | ~8 | metas: agente 1 não elimina nenhuma das 28; agente 3 marca relevante ou dúvida em >= 90% das 28 |
| 2 | **Você confere a calibração.** Se falhar, corrijo o roteiro e repito o passo 1 | — | — | ok para a F2 |
| 3 | Rotas do M6 para as obras da amostra sem abstract (S2 -> arXiv -> OpenAlex -> PDF aberto) | script | — | abstract recuperado ou `sem acesso` |
| 4 | **F2**: sorteio por grupo (semente fixa) e cadeia 1 -> 2 -> 3 nas 962 | 1 Haiku (40/lote) · 2 Haiku (20/lote) · 3 Sonnet (20/lote) | ~25 + ~40 + ~40 | JSON por lote em `docs/screening/fase1/F2/` |
| 5 | Dupla leitura em 10% de cada lote (M4.2) + 30 vereditos sorteados para a sua auditoria (M4.3) | mesma cadeia | ~10 | concordância no relatório |
| 6 | Relatório descritivo da F2: grupos que descem (0 relevante na amostra), grupos que seguem, `sem acesso`, distribuição de `objetivo` | — | — | `docs/screening/fase1/2026-09-XX-F2-relatorio.md` + coluna `F2` na tabela-mestra |

A execução é feita por subagentes do Claude Code: não usa API paga e respeita o "sem verba". O volume dos
passos 4 e 5 fica por volta de **115 chamadas de agente**, a maior execução do projeto até agora. A calibração
(passo 1) custa pouco e decide se vale gastar o resto.

**Ordena, não apaga:** grupo que desce fica no bruto com o motivo e volta se a bola de neve trouxer algum membro.

## 5. Decisões do Pedro antes do passo 1

1. **Objetivos:** o agente 3 rotula `saber` / `saber fazer` só como **ordenação** (proposta), ou o rótulo entra no
   **veredito**? Por exemplo: obra relevante sem nenhum dos dois objetivos desce.
2. **Saber ser** fica fora do rótulo das obras e vai para as suas notas de leitura?
3. **Ok para rodar o passo 1 (calibração, ~8 chamadas)** assim que os roteiros estiverem prontos?

**Respostas do Pedro (26/09):** (1) o rótulo **só ordena**; (2) **saber ser** fica fora do rótulo e vai para as notas
de leitura; (3) **pode rodar** a calibração. Calibração rodada no mesmo dia: `2026-09-26-calibracao-agentes-relatorio.md`.
