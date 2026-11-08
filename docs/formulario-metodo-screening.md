# Formulário — decisões do método de screening (Etapa 1)

**Para:** Pedro, 15/09/2026. **Preenche:** você, ditando; eu registro em `docs/screening/metodo-screening-etapa1.md`.
**Contexto:** o professor pediu um *screening* (não revisão sistemática) para suportar a **Etapa 1** do
processo de virar especialista — história, divisões, fundamentos, vocabulário e ferramentas da área.
A área, com suas palavras: **eficiência de modelos para implantação**.

Cada pergunta abaixo tem quatro partes: **por que** ela existe · **como responder** bem · **o que
acontece se errar** · **o que a resposta muda nas três Etapas** (1 história/fundamentos/ferramentas ·
2 frameworks de apoio · 3 trilhas de aplicação).

Responda na ordem. As primeiras condicionam as seguintes.

---

## P1. Screening de quê, exatamente?

**Opções:** (a) da área inteira · (b) da área, com as arquiteturas encoder/decoder/enc-dec como um dos
pilares de fundamentos · (c) das arquiteturas primeiro, área depois.

**Por que a pergunta existe.** "Eficiência de modelos para implantação" é uma área; "arquiteturas de
transformer" é um fundamento que ela usa. Você nomeou as duas coisas em respostas diferentes (o que vai
ser × o que quer aprender). O screening precisa de um único objeto, senão cada busca puxa para um lado
e você acaba com duas listas incompletas em vez de uma completa.

**Como responder.** Faça o teste do professor: complete a frase *"quando alguém me perguntar o que eu
sei fazer, eu digo ___"*. O que completa a frase é a unidade de busca. O outro item vira pilar dentro
dela. Se a frase sair com as arquiteturas, a resposta é (c); se sair com eficiência, é (a) ou (b).

**Efeito de errar.** Se escolher estreito demais (arquiteturas só), a Etapa 1 fica sem história de
compressão, quantização, destilação, serving — e a Etapa 3 (o seu tema) não tem chão. Se escolher
largo demais (área inteira sem pilar), você lê 30 surveys e não aprende a arquitetura que disse
querer aprender. O erro é assimétrico: largo demais custa tempo; estreito demais custa a
especialização.

**Influência nas Etapas.** Define o *título* da Etapa 1. Define de que área a Etapa 2 vai buscar
frameworks (frameworks de compressão são diferentes de frameworks de arquitetura). Define se o tema v3
é uma trilha dentro da Etapa 3 ou se ele *é* a Etapa 3.

**Decisão:** ___

---

## P2. As divisões da área vêm antes ou depois da busca?

**Opções:** (a) você propõe a taxonomia a priori e o screening preenche (top-down) · (b) a taxonomia
emerge dos surveys (bottom-up) · (c) híbrido: rascunho a priori, revisado pelos surveys.

**Por que a pergunta existe.** O professor disse que a Etapa 1 levanta "as divisões" da área. Você pode
levantá-las com o que já sabe ou deixar a literatura contar. Isso decide se o screening é uma busca
*guiada* (você sabe o que procura) ou *exploratória* (você descobre o que existe).

**Como responder.** Tente escrever, agora, em 2 minutos, as divisões da área de cabeça. Se saírem 5–8
nomes com confiança, você tem material para (a) ou (c). Se saírem 2–3 e o resto for chute, é (b) ou
(c). Não faça isso consultando nada — a pergunta é sobre o que você *já* sabe.

**Efeito de errar.** Top-down com taxonomia errada: você procura divisões que a área não usa e não
acha as que ela usa; o screening confirma o seu mapa em vez de corrigi-lo. Bottom-up sem nenhum mapa:
o primeiro survey que você abre vira a taxonomia por acidente, e surveys de grupos diferentes dividem
a área de jeitos diferentes.

**Influência nas Etapas.** As divisões viram os capítulos da Etapa 1 e as pastas do registro. Na Etapa
2, cada divisão tende a ter seus próprios frameworks. Na Etapa 3, a trilha de aplicação é escolhida
dentro de uma divisão — se a divisão estiver mal desenhada, o tema fica órfão.

**Decisão:** ___

---

## P3. O que conta como "fonte relevante" para cada pilar?

**Pilares (do professor):** história · divisões · fundamentos · vocabulário · ferramentas.
**Tipos possíveis:** survey · paper seminal · livro ou capítulo · documentação de ferramenta ·
tutorial de conferência · curso de referência (ementa + leituras).

**Por que a pergunta existe.** "Artigo relevante" não é o mesmo objeto em cada pilar. A história de
uma área raramente está num paper — está em surveys e em introduções de tese. Vocabulário está em
glossários e em surveys. Ferramentas estão em documentação e em papers de sistema. Se você definir
"relevante = paper com muitas citações" para tudo, o pilar de ferramentas fica vazio e o de história
fica com os papers errados.

**Como responder.** Preencha a tabela pilar × tipo. Para cada pilar, pergunte: *"se eu tivesse que
explicar isso para um colega em 10 minutos, de onde eu tiraria o conteúdo?"*. A resposta é o tipo de
fonte. Aceite mais de um tipo por pilar, mas nomeie o primário.

**Efeito de errar.** Pilar sem tipo de fonte definido é pilar que não vai ser preenchido — o screening
vai naturalmente para onde a busca é fácil (papers no arXiv) e deixa o resto. O resultado é uma Etapa
1 que sabe os papers e não sabe a história nem as ferramentas — exatamente o "muito produto" de
novo, em outra roupa.

**Influência nas Etapas.** Define o que entra na Etapa 1. Ferramentas encontradas aqui são
candidatas diretas à Etapa 2 (frameworks de apoio). Papers seminais são o vocabulário comum que a
Etapa 3 vai usar para se posicionar.

**Decisão:**

| Pilar | Tipo primário | Tipo secundário |
|---|---|---|
| História | ___ | ___ |
| Divisões | ___ | ___ |
| Fundamentos | ___ | ___ |
| Vocabulário | ___ | ___ |
| Ferramentas | ___ | ___ |

---

## P4. Como se identifica o seminal de cada divisão?

**Opções:** (a) mais citado da divisão · (b) o que os surveys citam em comum · (c) o que cursos de
referência usam como leitura · (d) combinação, com ordem de precedência.

**Por que a pergunta existe.** Toda divisão tem 1–3 papers que todo mundo cita — o "Attention is all
you need" dela. Eles são o fundamento e o vocabulário ao mesmo tempo. Mas "mais citado" tem
armadilhas: papers de benchmark e de dataset acumulam citações sem ser fundamento; papers recentes
importantes ainda não acumularam. A Fase 2B do seu `docs/pesquisa/metodo-busca-artigos.md` (descartada em 09/09)
propunha (b). Decidir se ela volta.

**Como responder.** Pegue uma divisão que você já conhece um pouco (destilação, por exemplo) e teste
os três critérios de cabeça: qual paper sai por citação, qual sai por "todo survey cita", qual sai
por "todo curso ensina". Se os três apontam o mesmo paper, qualquer critério serve e você escolhe o
mais barato. Se divergem, você precisa da ordem de precedência (d).

**Efeito de errar.** Seminal errado é fundamento errado: você aprende a área a partir de um paper
que a área não considera central, e na arguição cita o que ninguém cita. Sem critério nenhum, o
seminal vira "o que apareceu primeiro na busca" — o mesmo erro do nível 3 de procedência.

**Influência nas Etapas.** Os seminais são o núcleo da Etapa 1 — a leitura obrigatória em nível 1
(você leu). Na Etapa 3, são os papers que o seu tema tem que citar para ser legível pela área.

**Decisão:** ___

---

## P5. Regra de parada por divisão

**Opções:** (a) N fontes por pilar, fixo · (b) saturação — um survey novo não traz divisão nem
seminal novo · (c) tempo fixo por divisão · (d) combinação (ex.: saturação com teto de tempo).

**Por que a pergunta existe.** Screening sem parada vira revisão sistemática por acidente — o que o
professor explicitamente disse para não fazer. E a Etapa 1 tem de acabar para a 2 começar. A regra de
parada é o que torna o método um método e não uma intenção.

**Como responder.** Estime quanto tempo por semana você tem para isso até o fim da Etapa 1 (ver P10).
Divida pelo número de divisões que P2 produziu. O que couber nesse tempo é o teto; dentro dele,
escolha o critério de qualidade (saturação é o mais defensável, porque é observável: "abri o quarto
survey e ele não trouxe nada novo").

**Efeito de errar.** Sem parada: a Etapa 1 consome o semestre. Parada cedo demais: divisões inteiras
ficam com um único survey, e você não sabe que não sabe. Parada por N fixo: divisões grandes ficam
rasas e pequenas ficam infladas.

**Influência nas Etapas.** Define quando a Etapa 2 começa. Define a profundidade mínima que cada
divisão vai ter na Etapa 1 — e, portanto, quais divisões você vai conseguir defender numa arguição.

**Decisão:** ___

---

## P6. Profundidade de leitura durante o screening

**Opções:** (a) título + resumo · (b) resumo + figuras + conclusão · (c) introdução inteira ·
(d) varia por pilar (ex.: surveys em (c), seminais em (b), ferramentas em (a)).

**Por que a pergunta existe.** Screening é raso por definição — o objetivo é *achar* as fontes que
suportam a Etapa 1, não *fazer* a Etapa 1. Mas raso demais não separa um survey bom de um ruim, e a
Etapa 1 depende dessa separação. A linha entre "screening" e "leitura da Etapa 1" precisa estar
escrita, senão você lê tudo pela metade.

**Como responder.** Pergunte para cada tipo de fonte de P3: *"o que eu preciso ler para decidir se
esta fonte entra ou não?"*. Para um survey, normalmente a introdução e o sumário (a taxonomia dele).
Para um seminal, o resumo e a figura principal. Para uma ferramenta, a página inicial da documentação.
Isso dá a resposta (d) quase sempre — mas escreva os níveis.

**Efeito de errar.** Raso demais: entram fontes que não servem e você só descobre na Etapa 1, quando
já gastou tempo. Fundo demais: o screening vira a Etapa 1 sem método, e você chega em quinta sem
lista e sem leitura.

**Influência nas Etapas.** Marca a fronteira entre screening e Etapa 1 no seu registro — o que foi
lido em nível "screening" ainda não conta como fundamento aprendido. Na procedência (P7), é o que
separa o nível 3 do nível 1.

**Decisão:** ___

---

## P7. Procedência

**Regra existente:** (1) Pedro leu · (2) Claude leu o texto completo · (3) agente verificou página e
resumo apenas. Nível 3 serve para triagem, nunca para citação.

**Por que a pergunta existe.** A regra nasceu na busca de fronteira, onde o risco era citar resultado
que ninguém leu. No screening o risco é outro: fontes entram no nível 3 por natureza (é screening), e
precisam *subir* de nível na Etapa 1. A pergunta é se a escala serve como está ou se precisa de um
degrau intermediário ("lido em nível de screening", conforme P6).

**Como responder.** Olhe o que P6 decidiu. Se a profundidade de screening for maior que "título +
resumo", ela não é nível 3 nem nível 1 — precisa de nome. Se for título + resumo, é nível 3 e a
regra vale como está.

**Efeito de errar.** Sem o degrau: você não sabe, olhando o registro, quais fontes já foram
avaliadas de verdade e quais só foram achadas. Na arguição, cita coisa que só viu por cima. Com
degrau demais: burocracia que você para de manter na segunda semana.

**Influência nas Etapas.** A procedência é o que transforma o registro do screening na lista de
leitura da Etapa 1: tudo que está no nível de screening e foi aprovado sobe para "ler em nível 1". É
também a sua defesa na arguição — você sabe dizer exatamente o que leu.

**Decisão:** ___

---

## P8. Registro

**Opções:** (a) um arquivo por divisão · (b) um arquivo único com tabela · (c) arquivo único com
tabela + um arquivo de notas por fonte lida em nível 1.
**Colunas candidatas:** divisão · pilar · tipo de fonte · referência · como foi achada (P4) ·
nível de procedência · decisão (entra / não entra / dúvida) · motivo em uma linha.

**Por que a pergunta existe.** O professor avalia processo. O registro *é* o processo visível. Um
registro que só lista referências mostra o resultado; um que registra *como* cada fonte foi achada e
*por que* entrou ou não mostra o método funcionando. E o registro é o que sobrevive quando a
conversa some.

**Como responder.** Pense em quinta: o que você abriria na frente do professor para mostrar "este é
o meu screening"? Se for uma tabela, é (b) ou (c). Pense em daqui a um mês: onde ficam as notas de
leitura da Etapa 1? Se for junto, é (c).

**Efeito de errar.** Registro sem "como foi achada" e sem "motivo": você não consegue reconstruir o
método depois, e o professor vê uma lista, não um processo. Registro fragmentado demais: você para
de preencher.

**Influência nas Etapas.** É o artefato que atravessa as três Etapas. Na 2, os frameworks vêm de uma
coluna dele. Na 3, o tema cita a partir dele. E é o entregável natural para cada gate.

**Decisão:** ___

---

## P9. O que o screening entrega no fim?

**Opções:** (a) lista de fontes por divisão · (b) trilha de leitura ordenada (o que se lê antes do
quê, com dependências) · (c) lista + mapa das divisões da área (uma página) · (d) (b) + (c).

**Por que a pergunta existe.** "Suportar o início da Etapa 1" pode significar só ter as fontes ou já
ter a ordem em que lê-las. A diferença é grande: uma lista de 40 fontes sem ordem não inicia nada; uma
trilha de 12 com dependências ("leia o survey X antes do seminal Y") inicia a Etapa 1 no dia
seguinte.

**Como responder.** Pergunte o que você quer ter na mão na sexta, depois do gate: uma lista para
começar a triar, ou um plano para começar a ler? A segunda exige mais do screening (precisa saber o
que depende do quê), mas é o que faz a Etapa 1 começar.

**Efeito de errar.** Só lista: a Etapa 1 começa com outra rodada de decisão ("por onde eu começo?")
que ninguém planejou. Trilha sem mapa: você lê em ordem sem saber onde cada coisa cai na área.

**Influência nas Etapas.** A saída do screening é a entrada da Etapa 1. O mapa das divisões é o que
o professor pediu literalmente ("as suas divisões"). A trilha é o cronograma da Etapa 1.

**Decisão:** ___

---

## P10. Orçamento de tempo

**Perguntas:** quantas horas por semana para isto? Até quando a Etapa 1 precisa estar concluída
(há prazo do programa para a Etapa 2)? Quanto disso é screening e quanto é leitura?

**Por que a pergunta existe.** Todas as regras acima (parada, profundidade, número de divisões) são
funções do tempo. Sem orçamento, o método é uma lista de desejos.

**Como responder.** Número honesto de horas, contando as outras matérias e o trabalho. E a data
limite, se o professor deu uma. Se não deu, proponha uma e leve para ele quinta.

**Efeito de errar.** Superestimar: o método pede o que você não vai cumprir e o registro para na
segunda semana. Subestimar: a Etapa 1 fica rasa por decisão, não por falta de tempo.

**Influência nas Etapas.** Define o calendário das três Etapas. É a primeira coisa que o professor
vai poder verificar em cada gate: o que foi planejado × o que foi feito.

**Decisão:** ___

---

## Depois de preencher

Eu consolido as dez decisões em `docs/screening/metodo-screening-etapa1.md`, em prosa, com as suas palavras. Você
lê, corrige o que não soou seu, e o método está fechado. Só então começa a busca.
