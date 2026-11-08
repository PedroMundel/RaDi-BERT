# Dinâmica de afunilamento — 36/42 respondidas (28/08/2026)

Rodada de sim/não + escolha forçada, feita depois de Pedro reprovar ~200 opções de tema e
declarar que não conseguia decidir. Objetivo: extrair preferência revelada em vez de declarada.

## Respostas

**Sim:** demo (mostrar algo funcionando) · entrevista (explicar em entrevista) · finetune-llm ·
dado-br · publicar · inedito-ptbr (basta ser inédito em português) · sem-terceiros (evitar
dependência de acesso externo)

**Não:** reuso (não precisa ser usável por outros) · **ultimatum** · audio-sobre-texto ·
games · **lgpd** · publico-tedio (ou seja: setor público NÃO dá tédio)

**Tanto faz (12):** anotar · fora-juridico · exclusivo · chato-leigo · treinar-zero · sem-gpu ·
impacto-social · mercado · continuar · startup · base-pronta · risco-baixo

**Escolha forçada:** medir algo que ninguém mediu (vs. construir sistema) · **extrair** (vs.
verificar) · texto (vs. áudio) · dado público sem graça (vs. difícil de conseguir) · problema
verificável (vs. aberto) · **LLM grande de terceiro** (vs. modelo pequeno próprio) · **melhorar
o modelo** (vs. melhorar o dado) · economiza dinheiro (vs. descobre algo) · portfólio (vs.
artigo) · sozinho no próprio ritmo (vs. depender de externos) · útil pra empresa (vs. sociedade)

**Não respondidas (6):** gerente-vs-pesquisador · muitos-vs-poucos documentos ·
conhecido-vs-novo domínio · automático-vs-assistente · profundo-vs-amplo · orgulho-vs-emprego

## Leitura

1. **A âncora revelada é ML, não dados.** "Melhorar o modelo" + "fine-tuning de LLM: sim" +
   "extrair > verificar". Isso contradiz a config C2 fechada em 18/08 e explica por que nenhum
   tema de qualidade de dados o empolgou: ele vinha se forçando a uma âncora que o instinto
   recusa. A objeção O6 (`objecoes-e-respostas.md`) previa reabrir isso só se ele reagisse
   melhor à lista B — ele não reagiu a nenhuma lista, mas a escolha forçada respondeu.
2. **O verificador aprendido — coração do tema entregue — não é o que ele quer fazer.**
   Ele escolheu extração sobre verificação.
3. **O Ultimatum não pode ser base** (correção explícita dele: é trabalho profissional, não
   emprego fixo, não dá para contar com o acervo). O tema entregue depende de "corpus jurídico
   próprio" — perna quebrada.
4. **C6 (privacidade) está morto na prática:** lgpd = não.
5. **Ineditismo regional basta:** "tudo bem existir em inglês se não existe em pt-BR" = sim.
   Isso abaixa muito a barra de originalidade exigida e amplia o espaço viável.
6. **Contradição a resolver:** "sem-terceiros: sim" vs. "LLM grande de terceiro". API é
   dependência externa e custo recorrente; modelo aberto grande exige GPU alugada. Precisa de
   decisão explícita dele.
7. Note-se que "mercado: tanto faz" no sim/não, mas em TODA escolha forçada ele foi para o lado
   do mercado (empresa, economiza dinheiro, portfólio). A régua do empregador é real; ele só não
   a verbaliza como prioridade única.

## Direção que as respostas apontam

Estudo de **medição** (não de construção), com âncora em ML, sobre **extração** em documentos
públicos brasileiros em texto, usando **fine-tuning de LLM**, com resposta verificável, sem
dependência de terceiros, terminando em demo e em publicação.
