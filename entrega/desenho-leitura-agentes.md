# Desenho da leitura por agentes

## Para que serve este documento

Depois da limpeza por metadado e por citação (documento Árvore de Citação), sobram cerca de 11 mil
obras. Ainda é volume demais para eu ler, e é cedo para decidir obra por obra. Este documento
descreve como uso agentes de LLM para uma leitura resumida dessas obras, de modo que a minha leitura
e a minha decisão caiam só sobre o que sobrar.

Cada parte deste desenho foi decidida por mim. Os agentes executam; nenhum agente decide sozinho o
que entra no screening.

## O mecanismo de filtragem

Considerei três mecanismos:

| mecanismo | o que faz | custo | limite |
|---|---|---|---|
| árvore de citação | liga cada obra à área por quem cita quem, sem leitura | só consulta às bases | obra recente ainda não foi citada |
| amostragem por grupo com a regra do três (Hanley & Lippman-Hand, 1983) | lê uma amostra de cada grupo; se nenhuma é relevante, a proporção de relevantes no grupo é baixa, com 95% de confiança | 15 a 50 resumos por grupo | dá um teto de proporção, não zero |
| keywording (Petersen et al., 2008) | anota palavras-chave dos resumos, monta categorias e classifica cada obra nelas | leitura de resumos | o esquema nasce do que a amostra viu |

Os três não se excluem, então usei os três em sequência, do mais barato para o mais caro: primeiro a
árvore, que não lê nada; depois a amostragem, que decide grupos inteiros com um número; depois o
keywording, que dá nome às categorias, e esse é o começo do mapa da área.

## As fases

| fase | o que acontece | entra | sai |
|---|---|---|---|
| F1 - árvore de citação | obra sem ligação com o bloco da área desce para o fim da fila | obras da limpeza | ligadas, recentes e sem dado |
| F2 - amostragem | em cada grupo, uma amostra passa pela leitura dos agentes; grupo sem nenhuma relevante desce inteiro | saída da F1 | grupos que seguem |
| F3 - keywording | categorias nascem dos resumos; categoria inteira fora da área sai em bloco | grupos que seguem + técnicas com 21 a 50 obras | obras em categorias da área |
| F4 - leitura completa | cada obra passa pela cadeia de agentes e depois pela minha decisão | saída da F3 + técnicas com até 20 obras | lista para o registro |

Técnicas com poucas obras pulam etapas porque um corte estatístico em grupo pequeno arrisca derrubar
uma divisão inteira da área. Até 20 obras vão direto para a F4; de 21 a 50, para a F3.

### O tamanho da amostra na F2

A regra do três diz que, se nenhuma de n obras sorteadas é relevante, a proporção de relevantes no
grupo é, com 95% de confiança, menor que 3/n. Ela limita a proporção, não o número de obras
relevantes que podem sobrar escondidas, e esse número cresce com o tamanho do grupo. Por isso a
amostra cresce com o grupo:

| tamanho do grupo | amostra | se nenhuma é relevante, o grupo tem menos de |
|---|---|---|
| 1.000 ou mais | 50 | 6% de relevantes |
| 800 a 999 | 40 | 7,5% |
| 100 a 799 | 30 | 10% |
| 50 a 99 | proporcional ao grupo | cerca de 3/n |
| menos de 50 | leio o grupo inteiro | - |

Grupo que desce não é apagado: fica na tabela com o motivo e volta se algum membro dele aparecer na
bola de neve.

## Três agentes, uma tarefa cada

A leitura de cada obra passa por três agentes em cadeia. Separei em três para que nenhum deles se
perca misturando tarefas diferentes e importantes.

| agente | tarefa | recebe | devolve |
|---|---|---|---|
| 1 - triagem do óbvio | eliminar só o que é claramente de outra área | título e resumo | "claramente fora" com motivo, ou "passa" |
| 2 - extração | transcrever, sem julgar, as frases que dizem do que a obra trata | título e resumo das que passaram | frases copiadas do texto |
| 3 - julgamento | aplicar os critérios de pertencimento do método | só as frases do agente 2 | relevante, fora ou dúvida, com a frase e a regra usada |

Se as frases não bastam para decidir, o agente 3 devolve "dúvida", e a obra sobe um degrau na escada
de leitura (resumo, depois introdução, depois conclusão). O registro do screening continua só com
extração; os vereditos dos agentes ficam fora dele e servem para ordenar a fila, não para apagar.

| agente | modelo | por quê |
|---|---|---|
| 1 | Haiku | tarefa mecânica e de baixo risco |
| 2 | Haiku | transcrever, sem julgar |
| 3 | Sonnet | aplicar regras do método exige entendimento |

Cada agente recebe um roteiro fixo e versionado, com as regras do método copiadas e exemplos, e grava
a saída num formato fixo por obra. Nada fica só na conversa.

## Obra que o agente não consegue acessar

Um artigo importante para o meu tema já ficou parado porque o agente não conseguiu acessá-lo e o
aviso virou uma pendência solta, sem prazo. Para não repetir isso:

- Existe um estado próprio, "sem acesso". Nenhum agente decide sobre obra sem acesso, e nenhuma obra
  sem acesso é eliminada;
- Antes de declarar, o agente tenta rotas automáticas: Semantic Scholar, arXiv, OpenAlex e PDF de
  acesso aberto, anotando cada tentativa;
- O fluxo não para: o agente segue com as outras obras;
- No fim de cada volta há uma lista única das obras sem acesso, e o número delas aparece no relato da
  volta, ao lado dos outros estágios;
- Obra sem acesso de técnica pequena, ou com termo central no título, vai para o topo da lista.

## Como sei que os agentes acertam

1. Calibração antes de rodar: a cadeia roda sobre os 28 surveys de ajuste da referência e sobre 30
   obras de outra área já conhecidas. Metas: o agente 1 não elimina nenhum dos 28; o agente 3 marca
   relevante ou dúvida em pelo menos 90% deles;
2. Dupla leitura: 10% das obras de cada lote passam por uma segunda cadeia independente, e a
   concordância entra no relato;
3. Auditoria minha: 30 vereditos sorteados por volta, com a frase transcrita ao lado, para eu
   conferir;
4. Teste final: a metade de teste da referência só é usada no fim, para medir a perda do processo
   inteiro.

## Leituras

Petersen et al. (2008) li inteiro. Hanley & Lippman-Hand (1983) foi lido inteiro pelo orquestrador
(nível 2), e a tabela de tamanhos de amostra vem da Tabela 2 do artigo.
