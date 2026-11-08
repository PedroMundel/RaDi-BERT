# Tema escolhido (PROVISÓRIO — adotado em 28/08/2026, dia da entrega)

> ⚠ **REVISÃO NECESSÁRIA (28/08, mesmo dia).** A dinâmica de preferências
> (`dinamica-preferencias.md`) invalidou três premissas deste tema:
> (1) o corpus previsto era o do Ultimatum, que Pedro declarou não poder usar (trabalho
> profissional, sem vínculo fixo); (2) ele prefere **extração** a **verificação** — e o
> verificador aprendido era o coração daqui; (3) ele prefere **melhorar o modelo** a melhorar o
> dado, ou seja, a âncora revelada é ML, não C2. O texto abaixo permanece como registro do que
> foi entregue; a direção nova está no fim do arquivo de dinâmica.

## Título

**Estruturação de acervos documentais com controle de qualidade aprendido**

(Título 2 da rodada final; adotado provisoriamente pelo Pedro. Funciona sem subtítulo. "Refinaria de dados" foi vetado.)

## Texto entregue

> Acervos documentais só geram valor quando viram datasets estruturados confiáveis — mas a extração com modelos de linguagem produz erro silencioso (campos alucinados, inconsistências entre campos), e depender de APIs externas é caro e inviável para dado sensível. Este trabalho constrói e avalia um pipeline de estruturação executado inteiramente com modelos abertos locais, em que o controle de qualidade do dado é responsabilidade de camadas de ML treinadas para isso: (i) triagem aprendida na entrada, separando conteúdo aproveitável de duplicatas e ruído; e (ii) verificação aprendida na saída, com um modelo detector de erros de extração treinado a partir de erros reais e sintetizados. A contribuição central é medir, por ablação, quanto cada camada melhora o dataset final — avaliado pelo desempenho de modelos treinados sobre ele — usando acervo público brasileiro (ex.: diários oficiais/jurisprudência). Como extensão natural, o mesmo verificador pode passar a gatear a admissão de dados sintéticos para lacunas do dataset. O resultado é um protocolo replicável, de custo previsível e executável localmente, para transformar acervo bruto em dado de treino confiável.

## Como o tema nasceu (trilha de decisão, 28/08/2026)

1. Régua nova do Pedro (ver CLAUDE.md ## Rejected e memória global): tema tem que gritar para empregador "eu resolvo um problema seu" + professional improvement. Os 20 do `temas-candidatos.md` reprovados em bloco.
2. Duas rodadas de gerações reprovadas: temas pesquisa-primeiro (gap sintético→real, auditoria de eval sets) = legíveis só para revisor; temas engenharia-primeiro (cascata de extração, observabilidade) = tarefas que todo profissional já fez.
3. Molde que sobreviveu: dores universais SEM método estabelecido. Pedro aprovou N2 (prospecção de acervos) + N5 (contaminação por IA) + exigiu camada de ML **que melhora o dado** (QA, síntese) — não surrogate/predição meta.
4. Restrição imposta pelo Pedro: **modelos locais/abertos apenas** (custo de sondar milhares de docs por API é proibitivo; bônus: soberania/LGPD).
5. Prazo real: **3–4 meses** → síntese gateada e filtro de texto-de-IA cortados da execução (síntese vira 1 frase de extensão no texto; filtro de IA sai).

## Pipeline (escopo de execução)

| Etapa | Conteúdo | Status |
|---|---|---|
| 1. Triagem aprendida | dedup (MinHash/embeddings) + filtro de ruído/boilerplate | Núcleo (enxuta) |
| 2. Estruturação local | modelo aberto 7–8B extrai registros (schema 4–6 campos) | Núcleo |
| 3. Verificador aprendido | detector de erro de extração (alucinação de campo, inconsistência), treinado com erros reais + injetados | **Coração do artigo** |
| 4. Síntese gateada | gerador preenche lacunas, verificador gateia | CORTADA — extensão futura |
| 5. Prova downstream | modelo treinado no dataset refinado vs. ingênuo; ablação por camada | Núcleo (R1) |

Pergunta de pesquisa: quanto cada camada aprendida de melhoria de dados contribui para a qualidade do dataset final, medida pelo modelo treinado nele, sob execução 100% local?

## Cronograma (16 semanas)

- S1–3: corpus + schema + gold (150–300 docs, pré-anotação LLM + revisão manual)
- S3–5: triagem enxuta + extração baseline
- S5–10: verificador (fatia protegida)
- S10–12: downstream + ablação
- S12–14: escrita
- S14–16: buffer

Condições: schema simples, UMA tarefa downstream, corpus decidido na S1. Gargalo real: o gold subset (tempo manual do Pedro). Probabilidades estimadas: ~80% resultado publicável, ~50% resultado forte. Fallbacks por etapa: até resultado negativo do verificador é achado ("erros injetados transferem X para erros reais").

## Encaixe na config

Âncora C2 (estruturação = ênfase declarada; G01, A02, I27, G06), C1 como ferramenta (extração via LLM local, E01), R1 cumprida no núcleo (verificador + downstream são modelos treinados/avaliados). C6 fica latente (dado sensível motiva o "local", sem módulo próprio). A dúvida âncora-dados-vs-ML se dissolve: objeto é pipeline de dados, contribuição é modelo treinado.

## Pendências

- Pedro confirmar o título (adotado "provisoriamente").
- Escolher o acervo concreto na semana 1 (diários oficiais vs. jurisprudência vs. outro).
- Fase 4 de leitura continua valendo — leituras 2 (estruturação) e 3 (anotação/AL) ficam ainda mais relevantes para o tema; leitura 8 (extração com LLM, Xu et al. 2024) virou leitura OBRIGATÓRIA, não opcional.
