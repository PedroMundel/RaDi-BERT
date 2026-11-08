# Como o método de screening foi construído — o método do método

**Para responder:** *"Você criou esse documento como? De cabeça? Como sabia disso tudo?"*
**Resposta curta:** não foi de cabeça. As decisões que o método fecha são os **componentes-padrão de
qualquer protocolo de revisão bibliográfica** — os mesmos de uma revisão sistemática, de um *scoping
study* ou de um *mapping study*. O que o método faz de próprio é **adaptar esses componentes ao
screening**: retira a exaustividade (que é o que o professor pediu para não fazer) e troca a regra de
parada por saturação. Cada decisão foi ditada pelo Pedro, está datada, e a trilha inteira está em
arquivo. **Ferramentas usadas:** o Claude, para estruturar o questionário a partir desses componentes
e para revisar o rascunho contra dois critérios definidos pelo Pedro. Nenhuma decisão é do Claude.

---

## 1. De onde vêm as perguntas — mapeamento para a literatura de método

Os frameworks abaixo são os de referência para método de revisão em computação e áreas afins.
**Procedência (atualizada 19/09):** Kitchenham & Charters 2007 e Wohlin 2014 — **nível 4** (Claude
leu na fonte; notas em `docs/artigos/notas-kitchenham-charters-2007.md` e `notas-wohlin-2014.md`;
tabela conferida, sem divergência). Glaser & Strauss 1967 — **abaixo de 4**: original não lido; a
definição vem de fonte secundária (Saunders et al. 2018; nota em `notas-glaser-strauss-1967.md`).
Petersen 2008, Arksey & O'Malley 2005 e Tricco 2018 — leitura declarada pelo Pedro na Fundamentação;
não conferidas pelo Claude. Nada citado em texto assinado sem leitura dele (§4).

| # | Pergunta do formulário (`docs/formulario-metodo-screening.md`) | Componente-padrão | Onde está na literatura |
|---|---|---|---|
| P1 | Screening de quê? (unidade de busca) | **Questão de pesquisa / escopo** | Kitchenham & Charters 2007, *research questions*; Arksey & O'Malley 2005, estágio 1 *identifying the research question* |
| P2 | Divisões antes ou depois da busca? | **Esquema de classificação** — a priori ou emergente | Petersen et al. 2008, *classification scheme* construído por *keywording* dos resumos (bottom-up); é a origem direta da decisão "bottom-up no conteúdo" |
| P3 | Tipos de fonte aceitos | **Critérios de inclusão por tipo de publicação** | Kitchenham & Charters 2007, *study selection criteria*; Arksey & O'Malley 2005, estágio 3 *study selection* |
| P4 | Como se identifica o seminal | **Snowballing e conjunto inicial** | Wohlin 2014, *backward snowballing* a partir de um *start set*; a interseção de referências entre surveys é snowballing com voto |
| P5 | Regra de parada | **Saturação teórica** (em vez de exaustividade) | Glaser & Strauss 1967, *theoretical saturation*; é a diferença formal entre screening e RSL |
| P6 | Profundidade de leitura por tipo | **Triagem em estágios** (título/resumo → texto integral) | Kitchenham & Charters 2007, seleção em dois passos; PRISMA-ScR (Tricco et al. 2018), fluxo de triagem |
| P7 | Procedência (3 → 2 → 1) | **Confiabilidade da extração** — quem extraiu, quem validou | Kitchenham & Charters 2007, extração por mais de um revisor e verificação |
| P8 | Registro | **Formulário de extração de dados** | Kitchenham & Charters 2007, *data extraction form*; Petersen et al. 2008, *data extraction* |
| P9 | Saída do screening | **Síntese / mapa** | Petersen et al. 2008, o produto é um *systematic map*; Arksey & O'Malley 2005, estágios 4–5 *charting* e *summarizing* |
| P10 | Orçamento de tempo | **Protocolo: recursos e cronograma** | Kitchenham & Charters 2007, o protocolo inclui *project timetable* |

**Leitura da tabela:** nenhuma pergunta é inventada. O formulário é um protocolo de revisão com os
nomes trocados para o vocabulário do professor (screening, Etapa 1, divisões, fundamentos).

## 2. O que o método muda em relação ao padrão — e por quê

| Padrão (RSL / mapping) | Este método | Motivo |
|---|---|---|
| Cobertura exaustiva das bases | **Saturação** por divisão e por mapa (§5) | O professor: screening ≠ revisão sistemática; o objetivo é *suportar o início da Etapa 1*, não esgotar |
| String de busca fixa, registrada no protocolo | **Pool de termos versionado** (§2.1); strings são composições | O vocabulário da área é o que o Pedro ainda não tem; a string v0 congelaria a ignorância de partida |
| Esquema de classificação fechado antes da extração | **União com consolidação** (§9): divisões vêm dos surveys, singulares ficam marcadas | Petersen já faz o esquema emergir; aqui isso é levado ao mapa inteiro, porque o Pedro não conhece a área |
| Qualidade avaliada por checklist | **Filtro de qualidade de survey em três pernas** (§3.2) | Surveys de arXiv sem revisão são comuns e às vezes bons; a citação cruzada resgata os recentes |
| Extração por dois revisores humanos | **Procedência 3 → 2 → 1** (§7): agente extrai, Claude lê, Pedro lê | Um revisor só; o agente substitui o segundo revisor **só na extração**, nunca na interpretação — lição do Agrawal (10/09) |
| Produto: mapa + contagens | **Lista por divisão + mapa + confronto do pool** (§9, §2.1) | O confronto antes/depois é o que torna o processo visível — critério do programa |

**Técnica do Petersen testada e não adotada (22/09).** Petersen et al. 2008 excluem paper cujo termo
aparece só nas frases de abertura do resumo. Protótipo sobre os 89 resumos do arXiv da execução 2:
dos 7 nessa condição, **6 estavam dentro da área**. O ruído desta busca tem o mecanismo inverso —
survey de outro assunto com uma seção de eficiência cita o termo no meio do resumo. Confirmado pelo
Pedro em 22/09 (D1).

## 3. Como o documento foi produzido — a trilha, com datas

1. **15/09 — o gatilho.** O professor explica as três Etapas e define screening. O Pedro diz: *"antes
   de montar o screening precisamos definir um método; tudo tem que ter método, e eles sempre serão
   ditados por mim."*
2. **15/09 — o questionário.** O Claude estrutura as dez decisões que um protocolo de revisão precisa
   fechar (tabela de §1), cada uma com *por que a pergunta existe · como responder · efeito de errar
   · influência nas três Etapas* — a pedido do Pedro. Arquivo: `docs/formulario-metodo-screening.md`.
3. **15/09 — as respostas.** O Pedro dita as dez decisões, em aula, pelo celular. Delegou ao Claude
   apenas P6 (profundidade por tipo de fonte), com o objetivo da Etapa 1 como critério. Consolidado
   em prosa: `docs/screening/metodo-screening-etapa1.md` v1.
4. **15/09 — a revisão.** O Pedro define dois critérios de aceite (*sem lacuna de conhecimento*;
   *documento robusto, com todas as seções e explicações*) e pede uma rodada de revisão. O Claude
   devolve **21 achados** com correção proposta e severidade, cada um marcado `⟨rev-N⟩` no texto.
   Arquivo: `docs/revisao-metodo-screening-2026-09-15.md`. Isso corresponde à etapa de **avaliação
   do protocolo** de Kitchenham.
5. **16/09 — as decisões da revisão.** O Pedro responde às nove que exigiam escolha: aceita seis,
   **derruba uma** (espinha dorsal do mapa por recência — "nem recência nem citação decidem") e delega
   duas por omissão com regra de calibração. Discute e fecha a profundidade dos fundamentos item a
   item. Versões v2.1 → v2.2.
6. **17/09 — a §2 refeita pelo Pedro.** Ele julga a própria lista de 15/09 "muito vaga para top-down
   literal" e reorienta a seção: top-down no contorno, bottom-up no conteúdo. Propõe string-mãe,
   depois **pool de termos** em vez de string decretada. Versões v2.3 → v2.4; `docs/screening/pool-termos-etapa1.md`
   v0.
7. **17/09 — critérios de aceite e rejeição.** A pedido do Pedro, consolidados no fim do método.
8. **17/09 — este documento**, a pedido do Pedro: *"faltou um método para eu ter criado esse método."*

**O que o Pedro decidiu, o que o Claude fez.** Pedro: todas as dez decisões, os dois critérios de
revisão, as nove respostas à revisão, a reorientação da §2, o pool, os critérios de aceite. Claude:
a estrutura do questionário, a redação em prosa, a revisão de 21 achados, a profundidade por tipo de
fonte (P6, delegada), os defaults numéricos (§3.2, §4, adotados por omissão com calibração), a lista
de fundamentos de §1.1 (editada pelo Pedro), as sementes de origem `claude` no pool.

## 4. Como responder na arguição

**"Você criou isso como?"**
> "As decisões do método são as que qualquer protocolo de revisão tem que fechar — questão, critérios
> de inclusão, seleção, extração, síntese, cronograma. Peguei esses componentes e adaptei ao screening
> que o professor pediu: sem exaustividade, com saturação como parada, e com o esquema de divisões
> emergindo dos surveys, como num *mapping study*. Cada decisão é minha e está datada; a trilha
> inteira está em arquivo — o questionário, as respostas, uma rodada de revisão com 21 achados, e as
> minhas respostas a cada um."

**"Você usou IA?"**
> "Sim, como ferramenta: para estruturar o questionário a partir dos componentes de protocolo, para
> redigir em prosa o que eu ditei, e para revisar o rascunho contra dois critérios que eu defini. As
> decisões são minhas — inclusive as em que eu derrubei a proposta da ferramenta, que estão marcadas."

**"Como você sabia desses componentes?"** — a resposta honesta é a tabela de §1: são os de
Kitchenham, Arksey & O'Malley, Petersen, Wohlin. Kitchenham & Charters 2007 e Wohlin 2014 foram
**confirmados na fonte em 19/09** (nível 4, notas em `docs/artigos/`): os componentes existem com
esses nomes; o §8 de K&C (*mapping study*) descreve o screening melhor que a RSL, e o §9 (versão leve
para um pesquisador só) responde "um aluno consegue?". Ainda por ler: Petersen 2008 e Arksey &
O'Malley 2005 — são os dois mais próximos do que o método faz. Sem leitura, não citar nome nem ano em
voz alta; dizer "os protocolos padrão de revisão sistemática e de mapping study".

## 5. O que este documento não é

Não é uma alegação de que o método é original — ele é uma adaptação, e diz isso. Não é uma alegação
de que o Pedro conhecia a literatura de método antes de 15/09 — ele conheceu os componentes pelo
questionário, e isso é aprendizado do ciclo, não constrangimento. E não é uma história em que a
ferramenta não existiu: a trilha (§3) mostra o que ela fez e o que ela não decidiu.
