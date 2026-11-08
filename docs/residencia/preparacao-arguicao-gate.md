# Preparação para a arguição do gate — Semana 1

> **ENCERRADO (15/09).** O gate da Semana 1 já passou. Este documento não é mais preparação de nada;
> fica como registro. As respostas prontas (Partes 1–3) continuam sendo material reutilizável para a
> próxima arguição, quando houver — mas o contexto (o que foi entregue, o que o professor perguntou)
> será outro.

> **Parte 0 refeita em 15/09** sob o critério do programa (processo e especialização, não novidade —
> ver `CLAUDE.md`). A versão de 10/09, que abria por "o Agrawal ocupa o mecanismo", está arquivada no
> handoff `docs/handoffs/2026-09-15-1733.md`; os fatos dela continuam válidos e foram redistribuídos
> nas respostas abaixo. **As respostas 3–10 valem como estavam.** A 2 muda de moldura (ver lá).

**Contexto:** arguição direta, sem slides, com professores que leem paper. Se você ler só uma seção,
leia a Parte 0.

---

## PARTE 0 — A jogada de abertura

O professor já disse o que ele quer ouvir primeiro: **"você vai ser o quê?"**. Ele viu o tema e achou
"muito produto" — não conseguiu enxergar a pessoa atrás dele. Então a abertura não é sobre o tema. É
sobre você, e o tema entra como a coisa que você escolheu para virar isso.

**Não espere que perguntem. Abra com isso.** Sua resposta, com as suas palavras de 15/09:

- Especialização: **eficiência de modelos para implantação**.
- O que este ciclo ensina: **arquitetura de encoder, decoder e encoder-decoder, em profundidade.**
- O tema v3 é **uma análise dentro dessa área**, não a área.

**Fala de abertura (decore a estrutura, não as palavras):**

> "Antes do tema, o que eu estou construindo. Eu quero me especializar em eficiência de modelos para
> implantação — fazer capacidade de modelo grande caber onde ela não cabe: em custo de inferência,
> em dado rotulado, em hardware comum. O que eu quero saber fazer no fim deste ciclo, e hoje não sei,
> é entender de verdade como as três famílias de arquitetura — encoder, decoder, encoder-decoder —
> aprendem, e o que cada uma consegue ou não absorver.
>
> O tema é uma análise dentro disso. Eu escolhi ele porque a pergunta atravessa as três famílias na
> ordem em que a literatura as percorreu. O Distilling Step-by-Step faz o mecanismo num
> encoder-decoder, o T5. O DHRD porta para um decoder-only e mostra, com controle, que o ganho é
> conteúdo e não regularização. E a minha pergunta é o que sobra disso num encoder-only, que é a
> arquitetura que se usa de verdade para rotular em volume.
>
> Esse mecanismo já foi aplicado em BERT — o Agrawal, da Amazon, COLING 2025. Isso não me preocupa;
> é o oposto. É o método publicado que eu vou estudar, reproduzir e controlar. O que eles não
> fizeram — racionalização embaralhada, avaliação fora do domínio — é exatamente a parte que ensina,
> porque é onde eu descubro se o encoder absorveu conteúdo ou só ruído."

Uns 90 segundos. Ele responde diretamente à pergunta do professor, mostra que você já leu dois
papers em nível de detalhe, e coloca o Agrawal na mesa antes de qualquer um — como evidência de que
você faz o trabalho do especialista (achou o método publicado, sabe o que ele fez e o que faltou),
não como ameaça.

**Regra de procedência que vale aqui:** você leu o DSbS e o DHRD. **Não leu o Agrawal.** A fala acima
diz "já foi aplicado" e "o que eles não fizeram" — isso você sabe do levantamento (nível 3 → nível 2
do Claude), e é honesto dizer assim. **Não diga "eu li" sobre o Agrawal.** Se perguntarem "você leu?":
*"Ainda não; está no topo da lista, e é a primeira coisa que eu faço depois deste gate. O que eu sei
dele veio do levantamento: mecanismo, dataset e o que a seção de ablação contém."* Melhor ainda: ler
a §4.3 e a tabela de resultados antes da arguição — são 3 páginas, e aí "eu li a seção do método"
passa a ser verdade.

**O que essa abertura NÃO faz mais:** não defende novidade. Se alguém perguntar "mas isso é novo?", a
resposta é a régua do programa, dita com naturalidade: *"A pergunta de controle ninguém rodou nesse
canal, então tem espaço. Mas eu não escolhi o tema por ser inédito — escolhi porque é o que me ensina
o que eu quero aprender, e um nulo bem controlado me ensina o mesmo."*

---

## PARTE 1 — As perguntas, por ordem de perigo

### 1. "Isso já não foi feito? (Agrawal / Amazon)" — **quase certa**

Coberta pela Parte 0. Se vier depois da sua abertura, a resposta é curta: *"É o paper que eu abri
citando. Ocupa o mecanismo; deixa o controle aberto."*

**A pergunta de acompanhamento que vem em seguida, e é a de verdade:**

### 2. "Então o que exatamente sobra para você?" — **certa**

**Moldura nova (15/09):** a resposta não é "o que sobra de inédito", é **"o que eu aprendo fazendo o
que eles não fizeram"**. A tabela abaixo continua sendo o núcleo, mas o que ela mostra agora é onde
está a *lição*, não onde está a *lacuna*:

| Trabalho | Arquitetura | Canal | Rodou controle? | Conclusão |
|---|---|---|---|---|
| Herrewijnen (EACL 2026) | encoder | atenção | **sim**, tokens aleatórios | **é ruído** |
| Li et al. (2508.16777) | encoder | atenção | não | sem ganho de acurácia |
| DHRD (Xu 2025) | **decoder** | **saída** | **sim**, embaralhamento | **é conteúdo** |
| Agrawal (COLING 2025) | **encoder** | **saída** | **não** | afirma conteúdo, sem evidência |

> "A célula vazia não é mais a do mecanismo. É a do controle. No canal de atenção de um encoder,
> alguém rodou e deu ruído. No canal de saída de um decoder, alguém rodou e deu conteúdo. No canal
> de saída de um encoder — que é o caso que interessa para produção — ninguém rodou."

**Se perguntarem "e isso é contribuição suficiente?":** a pergunta pressupõe a régua errada. Responda
com a do programa: *"Suficiente para me ensinar o que eu quero aprender — sim. Se além disso virar
resultado publicável, é bônus."* Se insistirem: o Herrewijnen é um paper inteiro de EACL construído
sobre exatamente esse movimento — testar um baseline que ninguém tinha testado. Você não está
inventando um gênero.

**O que NÃO dizer aqui:** "eu vou fazer em português, então é novo". É fraco, e o Agrawal tem 9
datasets multilíngues de e-commerce.

### 3. "Resultado negativo não fecha questão nenhuma. Só mostra que VOCÊ não conseguiu." — **a mais afiada**

Sua proposta entregue **convida** essa pergunta, porque ela diz "resultado negativo também responde a
pergunta". Um professor bom vai puxar esse fio. Resposta:

> "Concordo, e é por isso que o desenho não é só 'com cabeça versus sem cabeça'. Um resultado nulo só
> vale se eu puder mostrar que a montagem conseguiria detectar o efeito se ele existisse. É o papel
> do controle positivo: se a condição com racionalização alinhada não bate a condição sem
> racionalização nenhuma, eu não tenho um achado sobre racionalização — eu tenho uma implementação
> que não funciona, e reporto isso como tal. O achado só existe no cenário em que o alinhado ganha do
> nada **e** o embaralhado não ganha. Sementes múltiplas e intervalo de confiança são obrigatórios
> pelo mesmo motivo."

Isso é a resposta que separa quem entendeu método de quem decorou o desenho. Vale ensaiar em voz alta.

### 4. "Isso não é só multi-task learning com outro nome?" — **provável**

> "Estruturalmente é, sim — é uma perda auxiliar somada. Eu não estou alegando um regime de treino
> novo. O que está em disputa é outra coisa: **o que aquele sinal auxiliar carrega.** E aí tem um dado
> do Distilling Step-by-Step que eu li: na Tabela 2, concatenar racionalização e rótulo na mesma
> sequência de saída fica **abaixo** do fine-tuning padrão em ANLI e CQA, enquanto separar as saídas
> ganha em tudo. Mesma informação, mesmos dados, resultado oposto dependendo de onde a saída sai.
> Então 'onde a cabeça está' não é detalhe de implementação."

Números, se pedirem (T5 220M, 100% dos dados): fine-tuning padrão e-SNLI 88,38 / ANLI 43,58 / CQA
62,19. Tarefa única concatenada: 88,88 / 43,50 / 61,37. Multi-tarefa separada: 89,51 / 49,58 / 63,29.

### 5. "Por que encoder? Por que não usar um T5 pequeno e pronto?" — **provável**

Dois níveis, dê o segundo:

> "O primeiro motivo é custo: uma passagem, 110 milhões, contra geração token a token. É o argumento
> do Agrawal — 50 vezes mais rápido por amostra, empatando com um LLM de 7B.
>
> O segundo motivo é o que me interessa mais. Num T5, quando você descarta a saída de racionalização,
> o decoder continua lá, e o caminho do rótulo passa por ele. Então não dá para saber se o
> conhecimento ficou na representação ou no decoder. Num encoder com cabeça separada, você joga a
> cabeça **inteira** fora. Se sobrar efeito, ele só pode estar na representação, porque não sobrou
> outro lugar. A arquitetura vira instrumento de medição, não só alvo barato de implantação."

### 6. "Qual é o dataset?" — **certa, e você não tem resposta decidida**

Não improvise e não diga "ASSIN2" solto. Você tem coisa melhor: mostre que a indecisão é um critério
sendo aplicado, não uma lacuna.

> "Não decidi, e a razão é um achado desta semana. O ASSIN2 era meu candidato óbvio em português. Fui
> ler o overview do shared task e ele é **binário** — tiraram paráfrase e excluíram contradição de
> propósito. E ele foi construído a partir do SICK-BR, que vem de legenda de imagem; os organizadores
> escrevem que escolheram essa base justamente por ter menos fenômenos linguísticos complexos e só
> fatos simples. Isso é o oposto do meu critério de tarefa, que é precisar de um passo de inferência
> que não esteja na superfície do texto.
>
> Pior: o SICK-BR não serve como conjunto fora de domínio, porque é a fonte do ASSIN2. O único par
> fora de domínio viável em português é ASSIN2 para ASSIN 1, e exige colapsar paráfrase em
> entailment.
>
> Em inglês, o e-SNLI resolve os dois problemas: três classes, contradição inclusa, racionalização
> humana como teto, e o protocolo fora de domínio é consagrado. O custo é que eu perco o argumento
> de português. Estou decidindo entre os dois com esse trade-off explícito."

Números na ponta da língua: ASSIN2 = 6.500 / 500 / 2.448, 2 classes, melhor do shared task 0,883 F1.
e-SNLI = 549.367 / 9.842 / 9.824, 3 classes, 1 racionalização humana no treino e 3 em validação e
teste.

**Detalhe que vale ouro se perguntarem se você conferiu:** o Agrawal avalia em GLUE, e as tarefas de
inferência que ele usa são **RTE e QNLI** — MNLI e SNLI ficaram de fora.

### 7. "Quantos dos ~50 artigos você leu de verdade?" — **provável, e é oportunidade**

Não peça desculpa. Esta é a melhor coisa no seu processo.

> "Dois em nível de leitura integral com resumo meu: Distilling Step-by-Step e DHRD. Um terceiro
> agora, o Agrawal. Os outros estão registrados em três níveis de procedência, e eu marco cada um:
> se eu li, se a leitura foi assistida, ou se eu só verifiquei título, venue e resumo na fonte. **Só
> o primeiro nível entra em texto assinado por mim.**
>
> E hoje eu tenho um caso que mostra por que a regra existe: o Agrawal estava no nível 3, classificado
> pela triagem como incógnita de novidade. A triagem não pegou o mecanismo. A leitura pegou — e o
> mecanismo era o meu. Se eu tivesse tratado triagem como leitura, eu teria defendido hoje um tema
> que já está publicado."

### 8. "Você está citando um workshop e preprints do arXiv." — **possível**

> "O DHRD é workshop, sim — Efficient Reasoning Workshop do NeurIPS 2025, e eu digo isso na proposta.
> Descobri conferindo o campo *Comments* do arXiv. O rodapé do PDF dizia '39th Conference on NeurIPS
> 2025', que é o texto padrão do arquivo de estilo e sai em qualquer submissão. Eu uso o DHRD pela
> ablação, que é a evidência mais direta que existe de que racionalização embaralhada piora mais do
> que racionalização nenhuma — não pelo carimbo. O Herrewijnen é EACL e o Agrawal é COLING."

Números da ablação do DHRD, se pedirem (Llama-3.1-8B / Llama-3.2-3B): sem racionalização −1,75% /
−3,84%; racionalização de outro exemplo −5,70% / −20,24%.

### 9. "A premissa não é frágil? Um BERT de 110M tem capacidade de raciocínio latente para revelar?" — **provável**

Este era seu risco número um. **O Agrawal o reduz** — use isso:

> "Era meu principal risco, e o Agrawal responde parte dele: com exatamente 110 milhões de parâmetros
> eles tiram +6% de ROC-AUC em GLUE com esse sinal. Então há alguma coisa lá para mexer. O que
> continua aberto é se o que mexeu foi conteúdo ou regularização — que é a minha pergunta. O paper que
> tirou minha novidade é o mesmo que baixou meu risco de premissa."

### 10. "Cabe em três a quatro meses, nessa GPU?" — **provável**

Cuidado: sua proposta afirma "treina em minutos numa RTX 5060 de 8GB" e **você ainda não rodou nada**.

> "É estimativa, não medida — está marcada como estimativa no meu documento de tema, e testar o
> ambiente é a primeira atividade do próximo ciclo. Tem um risco concreto: a 5060 é Blackwell, sm_120,
> e builds antigos de PyTorch não reconhecem. Se o ambiente não fechar, isso muda o cronograma antes
> de mudar o desenho, e eu prefiro descobrir na semana 2 do que na semana 10."

Se pressionarem sobre o e-SNLI ser grande: subamostrar para 30–50k é coerente com a tese do próprio
Distilling Step-by-Step, que é justamente que menos dado basta quando há racionalização.

### 11. "Qual é a aplicação disso? Quem usa?" — **possível**

> "Triagem de documentos em volume e verificação de consistência entre uma afirmação e sua fonte —
> casos em que chamar um LLM por item não fecha a conta. O Agrawal é a prova industrial de que a
> conta importa: relevância de busca na Amazon, milhões de pares por dia, 110M no lugar de 7B."

---

## PARTE 2 — Perguntas que você NÃO consegue responder: o script

Você leu três papers. Vão citar coisas que você não leu. **Bluffar é o único jeito de perder feio.**

**O script, palavra por palavra:**

> "Não li esse. Está na minha triagem em nível 3 — eu verifiquei título, venue e resumo na fonte, mas
> não o mecanismo, e eu não uso nível 3 para argumentar. Se ele faz o que o senhor está descrevendo,
> é material para o próximo ciclo e pode mudar o desenho."

Três razões para isso funcionar: é verdade, é a política que você já declarou por escrito no termo de
entrega, e você tem um exemplo pronto de por que a política é boa — o Agrawal.

**Variações:**

- Se citarem algo que você nunca ouviu: *"Não conheço. Anota aí que eu levo para o próximo ciclo?"* —
  e **anote na hora**, à mão, na frente deles. Vale mais que qualquer resposta.
- Se perguntarem um número que você não lembra: *"Não vou chutar número. Está no meu documento, eu
  confiro e mando."* Nunca aproxime de cabeça.
- Se te levarem a um terreno técnico que você não domina (otimização, teoria de generalização):
  *"Aí eu não tenho base para responder. É um gap que eu sei que tenho e estou fechando."*

**O que nunca dizer:** "acho que sim", "salvo engano", "pelo que eu vi por alto". Todas convidam a
pergunta seguinte, que você também não responde — e aí a conversa vira sobre o que você não sabe.

---

## PARTE 3 — Armadilhas nos seus próprios documentos

Coisas que **você escreveu** e que convidam uma pergunta que hoje você não sustenta. Saiba a versão
precisa de cada uma antes de entrar.

| O que está escrito | O problema | A versão que se defende |
|---|---|---|
| "o próprio DHRD mostra que o ganho some em tarefas resolvidas por reconhecimento de padrão" | **"Mostra" é forte demais.** É um padrão por tarefa na tabela do SuperGLUE, não um experimento controlado sobre tipo de tarefa | "o ganho **se concentra** em implicação e causa, e fica estável onde não há passo a verbalizar. É padrão observado na tabela deles, não experimento controlado" |
| "Um encoder desse tamanho treina em minutos numa RTX 5060" | **Você não rodou.** E tem risco de Blackwell/sm_120 | "estimativa, não medida — testar o ambiente é a primeira atividade do próximo ciclo" |
| A tabela de teste da proposta tem 3 condições | Falta o braço H1 e falta a condição de cabeça com pesos aleatórios congelados | tenha na cabeça que o desenho completo tem mais braços; a proposta traz o núcleo |
| "Resultado negativo também responde a pergunta" | Convida a pergunta 3, que é a mais afiada da lista | veja a resposta da pergunta 3 — controle positivo |
| Termo de entrega ainda com `[colchetes]`, data do gate e matrícula em branco | Se abrirem o documento na reunião, é constrangimento gratuito | **preencha antes.** É trabalho de dez minutos |

---

## PARTE 4 — O que não dizer, em nenhuma hipótese

1. **Não diga que o tema é inédito.** Não é mais, no nível do mecanismo. Dizer isso na frente de
   alguém que consegue buscar o título é o pior resultado possível da reunião.
2. **Não descreva papers que você não leu como se tivesse lido.** Inclusive os do seu próprio
   `docs/pesquisa/artigos-verificados.md` — a maior parte daquele arquivo é nível 3, por escrito.
3. **Não narre a troca de temas** (v1 → v2 → v3) a menos que perguntem diretamente. Você já decidiu
   que a moldura é por critérios, não por trilha de fracassos. Se perguntarem: *"os critérios que eu
   uso hoje saíram desses descartes"* — e siga.
4. **Não prometa resultado.** Prometa desenho e controle.
5. **Não peça desculpa por ter lido pouco.** Você leu três em profundidade e registrou a procedência
   dos outros ~50. Isso é mais disciplina do que a média, e o caso Agrawal prova que a disciplina
   pagou.

---

## PARTE 5 — As três frases que você tem que conseguir dizer sem pensar

1. **O que é:** *"Racionalização de LLM injetada num encoder por uma cabeça auxiliar que é jogada
   fora antes da entrega — o que sobra é um classificador de 110 milhões com custo de classificador."*
2. **O que sobrou de aberto:** *"Existe um paper da Amazon que faz o mecanismo e alega que o ganho vem
   do conteúdo da racionalização, sem nunca ter rodado um controle. Num canal vizinho, quem rodou o
   controle descobriu que era ruído. Eu quero rodar o controle."*
3. **Por que você:** *"É uma pergunta pequena, cara em rigor e barata em GPU. É exatamente do tamanho
   que eu consigo fazer direito em três meses."*

---

## Checklist de dez minutos antes de entrar

- [ ] Preencher data do gate e matrícula no termo; trocar os `[colchetes]` por links
- [ ] Ler a Parte 0 em voz alta uma vez
- [ ] Ler as respostas 2, 3 e 6 em voz alta uma vez — são as três que decidem
- [ ] Levar papel e caneta e **usar** quando citarem algo que você não conhece
- [ ] Reler a tabela de quatro linhas da pergunta 2. É o núcleo. Se você só lembrar dela, dá conta
