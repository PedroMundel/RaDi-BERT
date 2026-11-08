# Relatório de Pesquisa para Definição de Tema
Residência em IA — Pedro Mundel

Extraí os tópicos de interesse das CfPs de três conferências do CSCE'26 (ICAI, ICDATA e ACC),
chegando a 289 itens. Pontuei todos, um a um, num funil de 16 macro-temas, e agrupei o resultado em
9 clusters temáticos. Como sobraram notas altas demais para escolher, apliquei duas podas de
critério e consolidei 29 conceitos de interesse máximo.

Antes de transformar isso em tema, verifiquei o contexto. Levantei os 80 TCCs das turmas anteriores
(cerca de 8 têm dados como núcleo; perto de 25% se concentram em LLM e agentes) e reli as próprias
CfPs, que são listas recicladas de anos anteriores e quase não mencionam LLM ou IA generativa.

Para calibrar a escolha dentro dos 29 conceitos, respondi uma dinâmica de preferência revelada — 36
escolhas entre pares de atividades concretas, em vez de entre nomes de área. O resultado mostrou que
minha âncora é **aprendizado de máquina**, e que prefiro extrair a verificar e medir a construir.

Uma lista de tópicos não seleciona um tema sozinha, então escrevi um referencial próprio de
julgamento: os cinco tipos de alegação que uma pesquisa empírica pode fazer e o que cada um custa, o
que torna uma pergunta difícil de verdade, os seis instrumentos de avaliação (baseline, confundidor,
ablação, ruído, teto e piso, validade externa) e o que meu regime de recursos exclui e libera. A ele
somei dois critérios meus: o tema precisa comunicar a um empregador que eu resolvo um problema dele,
e precisa sobreviver à alternativa mais simples que já existe no mercado.

O tema veio de uma leitura. O *Distilling Step-by-Step* treina um modelo texto-para-texto a prever o
rótulo **e** gerar a justificativa produzida por um LLM, obtendo mais desempenho com menos dado. Daí
a pergunta: **como injetar esse conhecimento de racionalização num modelo encoder-only, que não gera
texto?** É a arquitetura que existe pronta e adaptada ao português, e a que de fato se implanta em
tarefas de rotulagem em volume — onde chamar um LLM por item não fecha a conta.

Formulei duas hipóteses de mecanismo e verifiquei a novidade das duas na fonte. A primeira — prever
o vetor da racionalização — já está ocupada por trabalho publicado. A segunda — uma cabeça geradora
acoplada apenas no treino e descartada na entrega — tem lacuna arquitetural aberta: o mecanismo foi
validado sobre modelos decoder-only, e o trabalho que o validou declara ter recusado a via
bidirecional por um motivo que não se aplica a um encoder. Fechei o desenho de estudo com as duas
hipóteses no mesmo modelo, o que transforma a ablação no próprio desenho, e com controle aleatório
obrigatório.

**Tema:** *Destilação de racionalização de LLM para modelos encoder-only.*

**Ainda em aberto:** a tarefa e o conjunto de dados, que dependem de uma escolha entre português e
inglês com custo dos dois lados; e o modelo base.

---

Detalhamento em: `docs/pesquisa/mapa-do-terreno.md` (referencial de julgamento) · `docs/pesquisa/tema-v3-racionalizacao-encoder.md`
(proposta) · `docs/pesquisa/artigos-verificados.md` (triagem) · `docs/pesquisa/bibliografia-base.md`
