# Leitura 3 — Anotação: active learning + crowdsourcing

**Referência:** Ren, P.; Xiao, Y.; Chang, X.; Huang, P.-Y.; Li, Z.; Gupta, B. B.; Chen, X.; Wang, X. **"A Survey of Deep Active Learning"**. arXiv:2009.00236, v2 (05/12/2021; ACM Computing Surveys 2021). https://arxiv.org/abs/2009.00236
**Verificado em:** 28/08/2026 (arXiv ao vivo). Sucessor moderno do clássico de Settles (2009); classifica 250+ trabalhos.
**Alternativa (verificada):** Li, Y.; Gao, J. et al. "A Survey on Truth Discovery". arXiv:1505.02463, v2 (2015; SIGKDD Explorations 2016). https://arxiv.org/abs/1505.02463 — cobre o lado crowdsourcing (agregar rótulos conflitantes de vários anotadores), que o anchor não cobre.

## Por que esta leitura

É a leitura 3 do plano da Fase 4 (ver `../clusters.md`): cobre a etapa de **anotação e aquisição** da âncora — **I17 active learning, M14 crowdsourcing, B40 aquisição de conhecimento**. Base parcial: I17 é "nunca toquei" (mas o porquê pessoal — anotação eficiente — está registrado), M14 é só teoria (anotou imagens 1x em disciplina, ouvinte na anotação do Ultimatum), B40 tem prática (regras BRMS em PoC). Anotação assistida por LLM fica FORA daqui — é assunto da leitura 6; aqui o foco é a anotação humana e a seleção do que anotar.

## Como o survey organiza o campo (do abstract)

Active learning = o modelo **escolhe** o que vai ser rotulado a seguir, para máximo ganho por custo de anotação. O survey sistematiza:

1. **Estratégias de consulta** — incerteza, diversidade, híbridas: como decidir qual exemplo pedir ao anotador.
2. **AL + deep learning** — os atritos específicos (DL quer muito dado, AL quer pouco; custo de retreinar).
3. **Cenários de aplicação** — visão, NLP etc.

A alternativa (truth discovery) cobre o passo seguinte: dado que vários humanos anotaram e discordam, como inferir o rótulo verdadeiro.

## Perguntas-guia (responder durante a leitura)

1. Quais são as famílias de estratégia de consulta e qual é o vocabulário (uncertainty sampling, query-by-committee, diversity)? — mapa mínimo de I17.
2. Quanto AL economiza de anotação na prática, nos números do survey? Quando NÃO vale a pena?
3. Como AL se conecta com anotação humana em escala (M14): o survey fala de anotadores ruidosos/múltiplos? O que fica para a alternativa (truth discovery)?
4. Se o Ultimatum tivesse usado AL na anotação do corpus jurídico, onde entraria no pipeline? (exercício de transferência)
5. O que do fluxo "aquisição de conhecimento" (B40 — estruturar conhecimento de fontes/especialistas) aparece aqui, e o que é assunto de outra literatura?

## Protocolo

- Ler: abstract → intro → taxonomia de estratégias de consulta com calma → seção de NLP; aplicações de visão em leitura rápida.
- Folhear a alternativa (truth discovery): só abstract + figura da taxonomia, para ter o vocabulário de agregação de rótulos.
- Ao final, extrair **2–3 papers apontados** (título + abstract + figuras) e listar abaixo.
- Tempo-alvo: 1 sessão de leitura + 1 de fichamento (base parcial, ritmo normal).

## Notas do Pedro

_(preencher durante a leitura)_

## Papers apontados para olhar depois (2–3)

_(preencher ao final)_
