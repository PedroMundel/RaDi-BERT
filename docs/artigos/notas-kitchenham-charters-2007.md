# Notas — Kitchenham & Charters (EBSE 2007)

**Título:** *Guidelines for performing Systematic Literature Reviews in Software Engineering*
**Tipo:** relatório técnico **EBSE-2007-01**, versão 2.3, 9 de julho de 2007. Keele University e
University of Durham. 65 páginas de corpo + apêndices (79 no PDF). Não é paper revisado por pares;
é o documento de referência da área (o Wohlin 2014 o chama de "the guidelines [7]").
**Autores:** Barbara Kitchenham (Keele) e Stuart Charters (Durham).
**PDF:** `docs/artigos/kitchenham-charters-2007-ebse.pdf` (baixado de
`legacyfileshare.elsevier.com/promis_misc/525444systematicreviewsguide.pdf`, 19/09/2026 — cópia
hospedada pela Elsevier; o original da Keele não está mais no ar).

## PROCEDÊNCIA

**Nível 4 — Claude leu em 19/09/2026 as seções que a tabela §1 cita: 0.4–0.5 (sumário e glossário),
2.3–2.5 (características, mapping, terciária), 5.3–5.6 (perguntas, protocolo, avaliação, lições), 6.1
(busca), 6.2 (seleção), 6.4 (extração), 8 (mapping studies) e 9 (observações finais).** NÃO li: 3, 4,
6.3 (avaliação de qualidade), 6.5 (síntese), 7 (relato), apêndices. **Pedro NÃO leu.** Nada daqui
entra em texto assinado por ele sem leitura.

---

## Veredito de uma linha

**Confirma todas as linhas da tabela §1 que o citam (P1, P3, P6, P7, P8, P10)** — os componentes
existem com os nomes usados — e traz dois achados que a tabela não tem: (a) o §8 descreve o *mapping
study* de um jeito que descreve o nosso screening melhor que a RSL; (b) o §9 dá a "versão leve para
um pesquisador só" que é o argumento de defesa do método na arguição.

## O que o documento é

Diretrizes para RSL em engenharia de software, derivadas de três guias médicos e dois livros de
ciências sociais, adaptadas ao fato de que ES tem pouca pesquisa empírica e dados proprietários. Três
fases: planejar, conduzir, relatar. **Glossário (0.5):** *systematic mapping study (também scoping
study)* — "uma revisão ampla de estudos primários numa área de tópico, que visa identificar que
evidência existe sobre o tópico". É esta a definição que o screening usa.

## Componentes que a tabela §1 cita — o que o texto diz

**Pergunta de pesquisa (5.3) — P1.** "Especificar as perguntas é a parte mais importante de qualquer
revisão": busca, extração e análise derivam delas. Estrutura PICOC (população, intervenção,
comparação, resultado, contexto) de Petticrew & Roberts. Diz explicitamente que "uma RSL numa tese de
doutorado deve identificar a base existente para o trabalho do estudante e deixar claro onde a
pesquisa proposta se encaixa" — é a função da Etapa 1.

**Protocolo (5.4) — P10 e o formulário inteiro.** Lista verbatim dos componentes: *background;
research questions; search strategy (termos e recursos); study selection criteria; study selection
procedures (quantos avaliadores, como resolver desacordo); quality assessment; data extraction
strategy; synthesis; dissemination; **project timetable***. Dez componentes; o formulário do método
tem dez perguntas. "Um estudo de mapeamento inicial pode ajudar a determinar a estratégia" (5.4) e "um
mapeamento pré-revisão pode ajudar a escopar as perguntas" (5.6) — o screening é isso.

**Busca (6.1).** Estratégia iterativa: buscas preliminares, tentativas de string, **conferir a string
contra papers já conhecidos**, consultar especialistas. Quebrar a pergunta em facetas, listar
sinônimos/abreviações/grafias, montar com AND/OR. Bases não bastam: **listas de referências de
primários e de revisões**, periódicos, literatura cinzenta, anais, contato com pesquisadores. **6.1.4
Documentar a busca:** "os resultados de busca **não filtrados** devem ser salvos e retidos para
possível reanálise"; mudanças anotadas e justificadas; Tabela 2 lista o que registrar por fonte (nome
da base, string, data, anos cobertos). **6.1.5 (lição de Brereton et al.):** nenhuma fonte acha tudo;
buscadores de ES não foram feitos para RSL. No exemplo, a string "muito específica" de Kitchenham et
al. 2007 ainda deu muitos falsos positivos — "uma string mais simples poderia ter sido igualmente
eficaz".

**Seleção (6.2) — P3, P6.** Critérios de inclusão/exclusão decididos no protocolo, refinados durante a
busca, **pilotados**. Processo em estágios: interpretar liberalmente no título/resumo — se não der para
excluir claramente, obter o texto completo; **"a qualidade dos resumos em TI/ES é pobre demais para
confiar; revise também as conclusões"** (Brereton). Manter lista de excluídos **só depois de tirar os
totalmente irrelevantes**, com motivo. **6.2.3 Confiabilidade:** dois revisores + Cohen Kappa; um
pesquisador só (doutorando) discute com orientador/painel, ou faz **teste-reteste** numa amostra.

**Extração (6.4) — P7, P8.** Formulário definido e pilotado no protocolo; campos-padrão: nome do
revisor, data, título/autores/venue, espaço para notas. **6.4.3:** extração independente por ≥ 2;
desacordos por consenso ou árbitro; um pesquisador só: orientador extrai amostra e cruza, ou
teste-reteste. **6.4.6 (Brereton):** "um lê como *extrator* e outro como *checador*" quando há muitos
papers. **6.4.4:** não incluir publicações múltiplas do mesmo dado; usar a mais completa.

**Mapping study (8).** Diferenças em relação à RSL, verbatim em resumo: perguntas **mais amplas e
múltiplas**; termos de busca **menos focados**, retornam muitos estudos e "isso é menos problema" porque
o objetivo é cobertura; a extração "pode ser chamada mais precisamente de **estágio de classificação
ou categorização**"; a análise é **totais e resumos**, com "representações gráficas da distribuição
por tipo"; útil "a doutorandos que precisam preparar uma visão geral da área em que vão trabalhar".

**Versão leve (9).** Para um pesquisador só, os passos mais importantes: protocolo; pergunta; **o que
será feito para lidar com um único pesquisador aplicando os critérios e fazendo toda a extração**;
estratégia de busca; dados a extrair; listas de incluídos e excluídos; síntese; relato. "Esta versão
leve é gerenciável para doutorandos."

## O que licencia no método de screening (leitura do Claude)

- **O screening é um mapping study no sentido do §8**, ponto por ponto: pergunta ampla (divisões da
  área), termos largos (pool), extração = classificação (registro por divisão), saída = mapa com
  contagens. É a defesa mais curta do método: "não é RSL, é *mapping/scoping study*, conforme
  Kitchenham & Charters 2007 §8".
- **Procedência 3 → 2 → 1** tem análogo direto no 6.4.6 e 6.4.3: agente = *extrator*, Claude =
  *checador*, Pedro = decisão final; e a recomendação para pesquisador único (teste-reteste em amostra)
  é um check que o método pode adotar para o nível 3 — reextrair uma amostra e comparar.
- **"Salvar o retorno bruto"** (6.1.4) é exatamente o passo 1 da Fase 1 no handoff (mostrar o retorno
  bruto antes de filtrar). Está licenciado.
- **"String simples pode ser tão boa"** (6.1.5) apoia o pool de termos com poucas fixações contra a
  string-mãe longa (rejeitada em 17/09).
- **Ler a conclusão além do resumo** (6.2.2, Brereton) é o que a tabela §6 do método já faz para
  surveys e artigos.
- **Pilotar critérios e formulário** (6.2.1, 6.4.1) é a "calibração de §3.2" do handoff.

## O que NÃO licencia

- **Saturação como parada.** K&C não usam o termo; o objetivo declarado é "encontrar o máximo possível
  de estudos primários" (6.1). A parada por saturação vem de outra tradição (Glaser & Strauss 1967) e
  a Fundamentação precisa dizer que o método **troca** exaustividade por saturação, não que K&C
  autorizam.
- **Nível 3 por agente.** O documento pressupõe extratores humanos; extração por LLM não está nele.
  O que se aproveita é a *estrutura* (extrator/checador, amostra de controle), não uma autorização.
- **Seminal.** Não há conceito de paper seminal ou de contagem de citações como critério.
- **Qualidade (6.3)** não foi lida e o método não avalia qualidade dos estudos — coerente com mapping
  (§8 diz que a análise é totais), mas se alguém perguntar por *quality assessment*, a resposta é
  "mapping study não faz; K&C §8".

## Conferência da tabela §1 (`docs/metodo-de-construcao-do-metodo.md`)

| Linha | Cita | Confere? |
|---|---|---|
| P1 | "research questions" | Sim, §5.3 |
| P3 | "study selection criteria" | Sim, §6.2.1 |
| P6 | "seleção em dois passos" | Sim, §6.2.2 ("multistage"; título/resumo → texto completo; + conclusões) |
| P7 | "extração por mais de um revisor e verificação" | Sim, §6.4.3 e §6.2.3; acrescentar: para um só, teste-reteste |
| P8 | "data extraction form" | Sim, §6.4.1–6.4.2 |
| P10 | "project timetable" | Sim, §5.4, verbatim |

**Nenhuma divergência.** Sugestão de acréscimo (não obrigatória): uma linha de rodapé na tabela
apontando §8 (*mapping study*) como enquadramento do screening inteiro, e §9 (versão leve) para a
pergunta "um aluno só consegue fazer isso?".
