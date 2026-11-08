# Método de screening - Etapa 1 da especialização

## Como este documento é usado

Este documento é o método que rege o screening bibliográfico da Etapa 1 da minha especialização. Ele
foi escrito antes de qualquer busca e é lido antes de cada fase: as fases de busca e extração (níveis
3 e 2) seguem as regras daqui sem alterá-las; a fase de filtragem (nível 1) é minha, e é onde as
decisões de entrada e saída são tomadas linha a linha, com o resumo de critérios do final como folha
de consulta. Toda mudança no método é registrada como versão nova, com data; o screening em curso
segue a versão vigente no momento da fase. A fundamentação do método (de onde vêm as decisões e como
ele se relaciona com os protocolos padrão de revisão) está em `fundamentacao-metodo-screening.md`.

**Uso como prompt para agentes de busca.** Este documento é também o prompt dos agentes que executam
as fases de nível 3 (screening geral e screening do screening, cap. 10): o agente recebe o método
inteiro, o pool de termos e as strings compostas, e devolve o registro do cap. 8 preenchido com
extração, nunca com interpretação (cap. 7). Estou usando agentes de busca em vez de buscar eu mesmo
por quatro motivos. Primeiro, volume: o screening cruza dezenas de surveys e centenas de referências
(a Fase 2B é uma interseção de listas), e isso é trabalho mecânico que não me ensina nada. Segundo,
separação de papéis: o que o agente faz é extrair (transcrever taxonomia, listar referências,
listar termos assumidos), e o que eu faço é decidir e ler; o aprendizado da Etapa 1 acontece na
filtragem e na leitura em nível 1, e é lá que o meu tempo tem que estar. Terceiro,
reprodutibilidade: o mesmo método e o mesmo pool, dados a um agente, produzem o mesmo procedimento,
e qualquer pessoa pode rodar de novo e conferir. Quarto, rastreabilidade: cada linha do registro diz
como a fonte foi achada e por qual fase passou, o que é mais difícil de manter numa busca manual.

Os artigos, ferramentas e cursos citados nominalmente ao longo do documento foram citados porque já
li ou consultei cada um deles em algum momento; nenhum entrou por indicação de terceiros sem que eu
o conhecesse.

---

## 1. Objeto do screening

A unidade de busca é a **área**: eficiência de modelos para implantação. As **arquiteturas** (encoder,
decoder, encoder-decoder) entram como **pilar fixo, definido a priori**: é o que eu quero aprender
neste ciclo. Os demais pilares **não são fixados agora**: emergem conforme eu for descobrindo ao ler
os documentos. Top-down na área e no pilar de arquiteturas; bottom-up no resto.

**Tipo de busca:** screening, em contraposição à Revisão Sistemática: "encontrar artigos relevantes e
que suportem o início da Etapa 1". **O que este método cobre:** o screening (nível 3) e a passagem
para a leitura (2 -> 1). A leitura da Etapa 1 em si (como se lê um seminal, como se escreve a nota)
terá regra própria quando começar.

### 1.1 Fundamentos a priori do pilar arquiteturas (rev-2)

Top-down exige conteúdo. O pilar só fecha quando **cada item tem uma fonte em nível 1** no registro.

**O que "profundidade" significa aqui** (critério adotado): *plena* = saber onde está o custo do
componente em FLOPs e em memória, e por que as três famílias diferem nele; **não** é derivar
gradiente. *Média* = entender o componente pelo gancho de implantação nomeado. *Leve* = uma frase
certa. **Critério que separou os níveis:** o componente aparece como variável de custo ou como alvo
de algum termo do pool do cap. 2? Se sim, média ou plena.

| Nível | Itens | Gancho de implantação |
|---|---|---|
| **plena** | self-attention | centro de custo: O(n^2) no comprimento; é o que o KV cache guarda, o que FlashAttention otimiza, o que atenção linear tenta substituir |
| **plena** | máscara causal - cross-attention | **são a diferença entre as três famílias**: encoder sem máscara, decoder com, encoder-decoder com cross-attention. É onde mora "o que cada família absorve" |
| **plena** | FFN/MLP | ~2/3 dos parâmetros; alvo de poda, MoE e quantização |
| **média** | multi-head | via MQA/GQA, redução de KV cache presente em todo modelo servido hoje |
| **média** | tokenização por subpalavras | define quantos tokens um texto custa (pt-BR gasta ~1,5 a 2x em tokenizador centrado em inglês); vocabulário = matriz de embedding, ~23M dos 110M do BERT-base, 30%+ em SLMs |
| **média** | codificação posicional | RoPE é o que permite estender contexto sem retreinar; comprimento de contexto é custo de KV cache |
| **leve, com gancho** | normalização de camada | outliers de ativação que dificultam quantização (o problema de LLM.int8 / SmoothQuant) aparecem associados a ela |
| **leve, com gancho** | conexões residuais | é o que faz early exiting e poda de camadas funcionarem: o fluxo residual mantém representações intermediárias legíveis |
| **leve** | linhagem atenção Bahdanau/Luong -> scaled dot-product | base, não mecanismo em uso |

- **As três famílias e seus objetivos de pré-treino - tudo:** encoder-only (MLM - BERT) -
  decoder-only (CLM - GPT) - encoder-decoder (span corruption / seq2seq - T5, BART). O que cada
  objetivo faz a representação aprender, e por que encoder rotula e decoder gera.
- **Inferência - mantido:** decodificação autorregressiva - KV cache - prefill x decode -
  memory-bound x compute-bound - precisão numérica (FP32/FP16/BF16/INT8/INT4) - custo em FLOPs e
  bytes por token. Motivo: gestão de memória, continuous batching, early exiting e a quantização
  inteira são ilegíveis sem este bloco; sem ele o pilar seria "arquitetura de transformer" em geral,
  não "arquitetura para implantação".
- **Escala - curto:** leis de escala, só o suficiente para ler um survey de compressão.
- **Base pré-transformer - plena, pelo cap. 1.3:** RNN - LSTM - seq2seq - atenção neural (Bahdanau
  2014). Entra como fundamento, não só como história.

### 1.2 Critério de pertencimento à área (rev-5)

Uma divisão candidata **pertence à área** se reduz custo de implantação em pelo menos um de três
eixos: **(i) inferência** - latência ou throughput; **(ii) memória/hardware** - cabe onde não cabia;
**(iii) dado rotulado** - mesma capacidade com menos rótulo. Os três são os da minha proposta de
tema. **PEFT/LoRA entram**, pelo eixo de implantação: serving de múltiplos adaptadores sobre uma base.
Consequência: a fronteira é o **efeito na implantação**, não o momento em que a técnica age;
eficiência de treino pura (sem efeito no modelo servido) fica fora.

### 1.3 Escopo de "modelos" (rev-6)

**Transformers e a base dos transformers** (RNN, LSTM, seq2seq, atenção neural) para fundamentos e
ferramentas. A base pré-transformer entra como **fundamento** (é de onde o transformer vem), não só
como história. CNNs continuam só em **história** (poda e quantização nasceram nelas; ver cap. 2.4).

## 2. Divisões da área - bottom-up, com pool de termos

A minha lista inicial de termos não é rascunho de taxonomia: seria o mapa confirmando a ignorância
de partida em vez de corrigi-la. O híbrido é: **top-down no contorno, bottom-up no conteúdo.**

- **Top-down (fixado antes da busca):** o que é a área e o que pertence a ela (cap. 1.2); o pilar de
  arquiteturas e seus fundamentos (cap. 1.1); o escopo de modelos (cap. 1.3).
- **Bottom-up (vem dos surveys):** as divisões, subdivisões e nomes da área, construídos por união
  com consolidação (cap. 9). Nenhuma divisão existe no mapa antes de um survey aprovado a trazer.

### 2.1 O pool de termos - vocabulário versionado

O vocabulário do screening vive em **`docs/screening/pool-termos-etapa1.md`**: uma tabela, uma linha por termo, com
variantes, grupo, **origem** (`pedro` - `claude 15/09` - `survey:<id>`), status e retorno.
**As strings de busca são composições do pool**: string-mãe (grupo `área` + `filtro-tipo`) e uma
string-filha por grupo, traduzidas por base, com os filtros dos caps. 3.2 e 10 embutidos onde a base
permite. Nenhuma string é decretada à parte do pool; mudou o pool, regeneram-se as strings. A seção
de string de busca de `docs/pesquisa/metodo-busca-artigos.md`, arquivada em 09/09 para a busca de fronteira, é
reaproveitada aqui para outro propósito (mapa da área, não fronteira).

**O que o pool é, e o que não é:**
- É **vocabulário e registro do ponto de partida**. Os meus termos estão nele com origem marcada;
  o confronto antes/depois (abaixo) filtra por origem.
- **Não** é divisão, pilar nem taxonomia. Termo do pool não entra no mapa por si; só um survey
  aprovado cria divisão (cap. 9).

**Regras de entrada e saída** (detalhadas no arquivo do pool): entra como semente no v0, ou como
nome de divisão/seção na taxonomia de um survey aprovado do v1 em diante; aposenta com retorno zero
*e* nenhum survey usando, riscado com motivo, nunca apagado; **v0** = sementes, **v1** = após
saturação do mapa, com os termos que os surveys trouxeram e as strings regeneradas.

**Confronto antes/depois (entregável):** no mapa v1, cada termo de origem `pedro` recebe um veredito
(**encontrou divisão / virou subdivisão / ficou fora da área (cap. 1.2) / não existe com esse nome**),
e o mesmo para os de origem `claude`, separados. É o que o screening ensinou, visível.

### 2.2 Sementes do Claude - mesmo status, origem separada

O pool v0 tem 8 termos de origem `claude 15/09` (os que eu desconhecia ou não lembrei de listar) ao
lado dos 34 meus. Status idêntico: termo de busca, não divisão. São conhecimento prévio do Claude,
**não verificados** contra survey nenhum (nível 3 por definição) e serão julgados pelo mesmo
confronto. "Prompt engineering" está no grupo `uso?`, a testar contra o cap. 1.2 no confronto;
"prompt compression" pode ser a variante que pertence.

### 2.3 Ciclo de vida do mapa

- **v0** = não existe mapa. Existem o pool v0 (caps. 2.1, 2.2) e o contorno (cap. 1).
- **Fases 1 e 2** (cap. 10): surveys da área entram; cada taxonomia é extraída (cap. 7) e vai para a
  união (cap. 9).
- **v1** = mapa após **saturação do mapa** (cap. 5.1): divisões consolidadas (>= 2 surveys ou minha
  decisão com motivo), singulares marcadas, confronto do pool (cap. 2.1) feito.
- **v2+** = revisões durante o screening por divisão (cap. 5.2), quando um survey de divisão traz
  subdivisão nova. Toda versão fica no arquivo `mapa-divisoes-etapa1.md`, com data e o que mudou.

### 2.4 Regra do pilar história (rev-3)

História de cada divisão = **o paper que a abriu** (primeiro seminal, sem janela temporal) + **a
narrativa de um survey** (introdução/seção de background). Pré-transformer e CNN entram **só no
pilar história**: LeCun 1990 (Optimal Brain Damage) e Han 2015 (Deep Compression) para poda e
quantização. **Exceção pelo cap. 1.3:** a linhagem RNN/LSTM/atenção neural (Bahdanau 2014) é base do
transformer e entra também em fundamentos.

## 3. Tipos de fonte

Aceitos, para todos os pilares, sem mapeamento fixo pilar x tipo:
**survey - livro ou capítulo - paper seminal - artigo científico.**

**Documentação de ferramenta** entra **só no pilar ferramentas**, com precedência: se a ferramenta
tem paper, o paper é a fonte e a documentação é apoio; se não tem (llama.cpp, TensorRT-LLM, Optimum,
ONNX Runtime), a documentação é a fonte, e só a página de visão geral. Tutorial e API ficam para a
Etapa 2. Motivo: a Etapa 1 inclui "ferramentas" explicitamente, e várias ferramentas centrais de
implantação não têm artigo.

Fora: tutorial de conferência, curso de referência (como fonte; ver cap. 4).

### 3.1 Ferramenta x técnica (rev-7)

**Ferramenta** = software que se instala e usa. **Técnica** = método, vai para a divisão. Um paper de
sistema (vLLM/PagedAttention, FlashAttention) gera **duas linhas** no registro: a técnica na divisão
correspondente; a ferramenta no pilar ferramentas.

### 3.2 Filtro de qualidade para survey (rev-13) - gerado com auxílio do Claude

Um survey entra no screening se satisfaz **pelo menos um**: (a) venue com revisão por pares
(periódico, conferência, workshop com anais); (b) **>= 100 citações** no Semantic Scholar; (c) citado
por **>= 2** surveys já registrados. Survey de arXiv sem nenhum dos três é registrado como "não
entra: sem filtro de qualidade", não descartado silenciosamente.
Regra adotada: os três em OU, com 100 e 2. Motivação da recomendação (do Claude) para cada perna:
revisão por pares sozinha exclui surveys bons que só existem no arXiv (comuns nesta área); citação
sozinha exclui os recentes; a citação cruzada entre surveys é o que resgata os recentes bons. Os
números são calibráveis: se a Fase 1 devolver < 3 surveys por divisão, baixar para 50; se devolver
> 10, subir para 200.

## 4. Identificação do seminal de cada divisão

Seminal é o que **os surveys da divisão citam em comum** e/ou o que **cursos de referência usam**.
O curso não é lido: a ementa aponta o paper. A Fase 2B de `docs/pesquisa/metodo-busca-artigos.md` (estudo de
população da área), arquivada em 09/09, **volta** como esse critério.

(rev-10) **Limiar de (b):** citado por **>= 2 dos >= 3 surveys** da divisão que passaram no cap. 3.2.
Recomendação ao analisar o meu limiar com LLMs: 2 de 3. Motivo: com 1 de 3 tudo vira seminal; com 3
de 3 um survey ruim veta. Se uma divisão tiver >= 5 surveys, subir para "metade ou mais".

**Cláusula de inclusão forçada:** se um paper é, para a divisão, tão relevante quanto o "Attention
is All You Need" (citação massiva), ele entra também, mesmo que não saia pelos dois critérios.
Contagem de citação não é critério de busca; é só esse gatilho.
(rev-11) **Gatilho operacional:** está entre os **3 mais citados da divisão** (Semantic Scholar,
busca pelo nome da divisão) e não saiu por (b)/(c). Recomendação adotada: 3. Um paper nessa posição
que não foi citado por 2 surveys é raro, e a raridade é o sinal.

### 4.1 Cursos de referência (rev-14)

Lista inicial de cursos que achei interessantes, verificada em 15/09 (página existe e título
confere; nível 3; ementas ainda não lidas). Somente eu adiciono ou removo; os agentes da pesquisa não
podem alterar, apenas recomendar.

| Curso | Instituição / responsável | Cobre | URL |
|---|---|---|---|
| 6.5940 TinyML and Efficient Deep Learning Computing | MIT, Song Han | compressão, quantização, poda, destilação, inferência eficiente | hanlab.mit.edu/courses/2024-fall-65940 |
| CS336 Language Modeling from Scratch | Stanford | arquitetura transformer, treino e inferência de LM, escala | cs336.stanford.edu/spring2025 |
| 11-868 Large Language Model Systems | CMU | serving, batching, memória, kernels | llmsystem.github.io/llmsystem2025spring |

## 5. Regra de parada - saturação em dois níveis (rev-8) (rev-9)

Saturação, em dois níveis, em ordem:

1. **Saturação do mapa** (nível da área): um survey *da área* novo não traz **divisão nova**. Satura
   primeiro; produz o mapa v1 (cap. 2.3) por união (cap. 9).
2. **Saturação da divisão:** um survey *da divisão* novo não traz **seminal novo** (critério do cap.
   4) nem **fundamento assumido novo** (cap. 6, regra transversal).

**Mínimo:** **3 surveys** lidos (em nível de screening) antes de declarar saturação em qualquer
nível; com um só, "o próximo não trouxe nada" é indistinguível de "não li o suficiente". Sem teto de
tempo por divisão.

## 6. Profundidade de leitura no screening - por tipo de fonte

Definida com o objetivo da Etapa 1 e as regras anteriores em mente (os surveys corrigem o mapa; a
saturação precisa detectar "novo"; a Fase 2B precisa das referências).

| Tipo | O que se lê no screening | Por quê |
|---|---|---|
| **Survey** | resumo - introdução - **seção/figura de taxonomia** - títulos de todas as seções - conclusão / future directions - **referências extraídas em forma estruturada** (rev-16) | a taxonomia corrige o cap. 2 e dispara o cap. 5; introdução e conclusão carregam história e problemas abertos; as referências alimentam a Fase 2B |
| **Livro / capítulo** | sumário - prefácio - introdução do capítulo | decide se cobre a divisão; prefácio costuma ser a melhor fonte de história |
| **Paper seminal** | resumo - introdução (contribuições declaradas) - figura principal do método - tabela principal | o bastante para posicioná-lo e extrair o vocabulário que ele introduziu; **leitura integral é Etapa 1** |
| **Artigo científico** (não seminal; inclui paper de sistema) | título - resumo - figura 1 - conclusão | se não decidir em 5 minutos, não entra |
| **Documentação** (só ferramentas) | página de visão geral | cap. 3 |

Regras transversais:
- Nada lido em nível de screening pelos agentes deve contar como fundamento aprendido por mim.
- Fonte que pede mais leitura para decidir vira **"dúvida"** dentro do registro (resolução no cap.
  8.1).
- (rev-1) **Conceitos assumidos:** toda fonte screenada produz a lista dos termos que ela **usa sem
  definir**. Cada termo vira candidato a fundamento. Um fundamento está **coberto** quando tem fonte
  própria (seminal ou livro/capítulo) no registro; **descoberto** enquanto não tiver. É o teste
  "self-attention": se o alvo é transformer e self-attention aparece assumido em toda fonte, ele
  precisa de linha própria. A lista do cap. 1.1 é o ponto de partida; esta regra é o que a completa.

## 7. Procedência - 3 -> 2 -> 1, sem degrau novo

- **Nível 3 = o screening.** Um agente faz a leitura do cap. 6 e devolve o registro. É triagem:
  decide o que entra, não ensina nada, nunca cita.
- **Nível 2 = Claude lê o texto completo** do que os agentes produziram e produz notas.
- **Nível 1 = Eu leio o original e realizo a poda inicial.** Só isso conta como fundamento aprendido
  e só isso é citável em texto assinado por mim.

O screening inteiro roda em nível 3 e é delegável. A subida 3 -> 2 -> 1 é a Etapa 1 propriamente
dita.

(rev-15) **O que "versão simples" do nível 3 significa: extração, não interpretação.** O agente
devolve, para cada fonte: seção de taxonomia **transcrita**; títulos de seções; contribuições
declaradas **verbatim** (o parágrafo "our contributions are..."); lista de referências estruturada
(cap. 8, identificador); conceitos assumidos (cap. 6). **O agente não julga relevância** e não resume
o método com as próprias palavras: foi assim que o Agrawal passou como "incógnita" no nível 3 e o
mecanismo dele só apareceu no nível 2. A filtragem (cap. 10) é minha, sobre extração.
**Falha de extração:** se `pdftotext` falhar ou sair ilegível, tentar outra rota (URL do publisher,
versão HTML, arXiv) **antes** de registrar "ilegível"; "ilegível" nunca vira registro permanente sem
uma segunda tentativa documentada.

## 8. Registro

Um **arquivo único com tabela** (o screening) **+ um arquivo de notas por fonte lida em nível 1**.

- Tabela: `screening-etapa1_v1.2.md`. Colunas: as minhas originais e as adicionadas pela revisão
  (rev-4) (rev-16) (rev-19):

| Coluna | Origem | Conteúdo |
|---|---|---|
| divisão | original | conforme mapa do cap. 9 (ou "mapa" para surveys da área) |
| pilar | original | história - divisões - fundamentos - vocabulário - ferramentas |
| tipo de fonte | original | cap. 3 |
| referência | original | autores, título, ano |
| **identificador** | rev-16 | DOI ou arXiv id; sem identificador não entra na Fase 2B |
| **venue** | rev-19 | campo Comments do arXiv ou página do publisher; rodapé de PDF não é venue |
| como foi achada | original | busca por título - ementa de curso - interseção de surveys (Fase 2B) - inclusão forçada - bola de neve |
| **fonte de origem** | rev-19 | qual survey/curso levou até ela: a bola de neve visível |
| nível de procedência | original | 3 / 2 / 1 |
| decisão | original | entra / não entra / dúvida |
| motivo | original | uma linha |
| **termos** | rev-4 | introduzidos pela fonte + assumidos por ela (alimenta o glossário) |
| **data** | rev-19 | quando foi screenada |
| **origem** | rev-20 | `etapa-1` ou `etapa-3` (ver cap. 11) |

- Notas: `docs/artigos/notas-<autor>-<ano>.md`, padrão já em uso; nível 2 e nível 1 marcados item a
  item.
- (rev-4) **Glossário:** `glossario-etapa1.md`, alimentado pela coluna termos. Cada termo: definição
  em uma linha, fonte onde foi definido (não onde foi assumido), divisão. É o pilar vocabulário
  materializado.

### 8.1 Resolução de "dúvida" (rev-17)

Dúvida não fica para a Etapa 1 (que só lê o que entrou). Regra: o Claude lê **a seção em questão**
(nível 2 parcial, limitado à seção) e devolve o fato; eu decido entra/não entra. Prazo: antes de
declarar a divisão saturada.

## 9. Saída do screening

**Lista de fontes por divisão + mapa das divisões da área (uma página).** Sem trilha ordenada de
leitura: a ordem se decide no início da Etapa 1, com a lista e o mapa na mão.

(rev-18) "Às vezes um paper mais recente oferece uma abordagem não tão boa quanto o antigo, e o
cenário contrário também; e o antigo tem mais citações por ser antigo" -> nem recência nem citação
decidem. Regra: união com consolidação (proposta do Claude, aprovada e revisada por mim, avaliação
abaixo): o mapa não adota a taxonomia de nenhum survey. É construído por **união**: cada divisão que
aparece em qualquer survey aprovado entra no mapa com a lista dos surveys que a usam. Divisão que só
aparece em **1** survey é marcada *singular* e só se consolida quando um segundo a confirma (ou eu a
mantenho com motivo). Sobreposições e nomes diferentes para a mesma coisa são **mescladas por mim**,
com o motivo na linha. Os termos do pool (cap. 2.1) são confrontados com a união, item a item, por
origem: encontra divisão / vira subdivisão / fora da área pelo cap. 1.2 / não existe com esse nome.
O mapa é meu; os surveys são evidência, não autoridade.

*Por que união e não as alternativas:* (a) survey mais recente manda: descartada, pelo motivo
acima; (b) mais citado manda: envelhece pelo mesmo motivo; (c) interseção (só divisão em que >= 2
surveys concordam): perde as divisões recentes, que só um survey ainda cobre, e nesta área o recente
é o serving; (d) união com consolidação: é (c) sem perder o recente, e a única que não elege
autoridade. Fraqueza conhecida: surveys cortam em granularidades diferentes (um trata "quantização"
como divisão; outro separa PTQ e QAT), o que obriga mesclagem manual; e a mesclagem manual é o
exercício de aprender as divisões da área, que é o que a Etapa 1 pede.

## 10. Procedimento (rev-12) (rev-21)

Pipeline em quatro fases: **screening geral -> screening do screening -> filtragem -> leitura
completa.** As duas primeiras fases são nível 3 (agente, largo e depois fino sobre os candidatos); a
filtragem é a minha decisão sobre a tabela do cap. 8; a leitura completa é a subida 2 -> 1.

**Bases:** arXiv - ACL Anthology - Semantic Scholar (também para contagem de citação) - Google
Scholar (conferência) - livros via ementas dos cursos do cap. 4.1 e via referências dos surveys.
**Janela:** surveys **2020+** para mapa e divisões (a área mudou de forma com os LLMs); **sem
janela** para seminais e história. **Língua:** inglês.

**Fase 1 - screening geral** (nível 3, agente). *Entrada:* o pool v0 (`docs/screening/pool-termos-etapa1.md`) e as
strings compostas dele. *Como:* (1) **string-mãe** nas bases (mapa da área), depois **strings-filhas**
por grupo, todas geradas do pool, com os filtros dos caps. 3.2 e 10 embutidos; (2) ementas dos cursos
do cap. 4.1; (3) referências dos surveys encontrados (bola de neve, uma rodada). Aplicar o cap. 3.2.
*Saída:* lista de surveys candidatos, registrados com decisão "entra" ou "não entra: sem filtro de
qualidade".

**Fase 2 - screening do screening** (nível 3, agente). *Entrada:* surveys que entraram. *Como:*
leitura do cap. 6 por tipo, extração do cap. 7, conceitos assumidos, referências estruturadas. Rodar
a Fase 2B (interseção) por divisão assim que houver >= 3 surveys dela. *Saída:* tabela do cap. 8
preenchida com surveys, seminais candidatos (b, c, forçados), fundamentos candidatos, ferramentas
candidatas.

**Fase 3 - filtragem** (eu). *Entrada:* a tabela. *Como:* decisão linha a linha (entra / não entra /
dúvida), com motivo; dúvidas pelo cap. 8.1; saturação pelo cap. 5, primeiro do mapa, depois por
divisão; mapa pelo cap. 9. *Saída:* screening da divisão fechado; mapa das divisões.

**Fase 4 - leitura completa** (Claude nível 2 -> eu nível 1). *Entrada:* o que entrou. *Como:* notas
em `docs/artigos/`; glossário atualizado; fundamentos dos caps. 1.1 e 6 marcados cobertos. *Saída:*
Etapa 1, o que, por regra própria, ainda será escrito.

## 11. Reaproveitamento da Etapa 3 (rev-20)

`docs/pesquisa/artigos-verificados.md` já tem ~50 artigos verificados na fonte para a divisão destilação de
raciocínio (a do meu tema), e quatro em nível 2 com notas. Eles **entram no registro novo** com o
nível de procedência que já têm e `origem: etapa-3`. Não se refaz o que já foi feito; mas a divisão
ainda passa pelo cap. 5 (saturação) como as outras, porque aquela busca foi de fronteira, não de
mapa.

## 12. Critérios de conclusão e métricas de gate (rev-21)

**Screening de uma divisão concluído:** saturação pelo cap. 5 - seminais identificados pelo cap. 4 -
nenhuma "dúvida" aberta - fundamentos assumidos listados (cobertos ou marcados descobertos).
**Screening concluído:** mapa saturado (cap. 5.1) - toda divisão do mapa com screening concluído -
pilar arquiteturas com todos os itens do cap. 1.1 com fonte no registro - mapa do cap. 9 escrito.
**Etapa 1 concluída** (fora deste método, mas o alvo): todo fundamento coberto tem fonte em nível 1;
todo seminal em nível 1; glossário fechado.

**Métricas de gate (planejado x feito, semanal):** divisões saturadas / total do mapa - fontes
registradas - fontes em nível 2 - fontes em nível 1 - fundamentos cobertos / listados.

---

## Relação com o que já existe

- `docs/screening/pool-termos-etapa1.md`: o vocabulário versionado (v0) e as strings compostas dele, como texto.
- `docs/pesquisa/metodo-busca-artigos.md` (09/09): método de busca de **fronteira** para o tema; serve à Etapa 3. A
  Fase 2B dele volta aqui como critério de seminal (cap. 4).
- `docs/pesquisa/artigos-verificados.md` e `docs/residencia/triagem-bibliografica.md`: resultado daquela busca; entram pelo cap. 11.
- Procedência (cap. 7) é a regra permanente de procedência do projeto.

---

## Resumo - critérios de aceite e de rejeição

Consolidação do que as seções acima decidem, para consulta rápida durante a filtragem (Fase 3). Cada
linha aponta a seção que a fundamenta; em conflito, vale a seção.

### Critérios de aceite

**Uma divisão entra no mapa se:**
- reduz custo de implantação em pelo menos um eixo: inferência, memória/hardware ou dado rotulado (cap. 1.2);
- foi trazida como divisão por **>= 2 surveys aprovados**, ou por 1 survey **e** minha decisão com motivo na linha (cap. 9);
- para PEFT/LoRA e casos análogos: o efeito na implantação existe, mesmo que a técnica aja no treino (cap. 1.2).

**Um survey entra no screening se satisfaz pelo menos um** (cap. 3.2):
- venue com revisão por pares; ou
- >= 100 citações no Semantic Scholar; ou
- citado por >= 2 surveys já registrados.
E, para contar no mapa e nas divisões: publicado em **2020+** (cap. 10). Para história: sem janela.

**Um paper é seminal da divisão se** (cap. 4):
- é citado por >= 2 dos >= 3 surveys aprovados da divisão; ou
- consta na ementa de um curso de referência da lista do cap. 4.1; ou
- está entre os 3 mais citados da divisão (inclusão forçada), mesmo sem os dois anteriores.

**Um artigo científico (não seminal) entra se** (cap. 6):
- a decisão sai de título + resumo + figura 1 + conclusão em <= 5 minutos; e
- serve de apoio a um pilar nomeado (história, divisões, fundamentos, vocabulário, ferramentas).

**Um livro/capítulo entra se** (cap. 6): o sumário + prefácio + introdução mostram que cobre uma divisão do mapa ou um fundamento do cap. 1.1.

**Uma ferramenta entra no pilar ferramentas se** (caps. 3, 3.1):
- é software instalável (não técnica); e
- tem paper de sistema (fonte primária) **ou**, na ausência, documentação com página de visão geral.

**Um fundamento está coberto se** (caps. 1.1, 6): tem fonte própria (seminal ou livro/capítulo) no registro, na profundidade definida na tabela do cap. 1.1: plena, média ou leve.

**Uma fonte sobe de nível se** (cap. 7): 3 -> 2 quando o Claude lê o texto completo e produz nota; 2 -> 1 quando eu leio o original. Só nível 1 é citável.

**Uma divisão está screenada se** (caps. 5.2, 12): >= 3 surveys lidos; survey novo não traz seminal nem fundamento assumido novo; nenhuma dúvida aberta; seminais identificados; fundamentos assumidos listados.

**O mapa está saturado se** (cap. 5.1): >= 3 surveys da área lidos e o próximo não traz divisão nova.

**O screening está concluído se** (cap. 12): mapa saturado; toda divisão screenada; todo item do cap. 1.1 com fonte no registro; mapa do cap. 9 escrito; confronto do pool (cap. 2.1) feito.

### Critérios de rejeição

**Uma divisão candidata fica fora se:**
- não reduz custo em nenhum dos três eixos do cap. 1.2 (ex.: eficiência de treino pura, sem efeito no modelo servido; "prompt engineering" será testado por esta regra);
- só aparece em 1 survey e eu não a mantive com motivo: fica *singular*, não entra (cap. 9);
- é nome alternativo de divisão já existente: mescla, com motivo, não entra em duplicata (cap. 9).

**Um survey fica fora se:**
- não satisfaz nenhuma das três pernas do cap. 3.2: registrado como "não entra: sem filtro de qualidade", nunca descartado em silêncio;
- é anterior a 2020 e o uso pretendido é mapa/divisões (cap. 10);
- cobre modelos fora do escopo do cap. 1.3 (ex.: só CNNs) e o uso pretendido não é história.

**Um paper fica fora como seminal se:** só tem contagem de citação a seu favor e não está no top-3 da divisão (cap. 4); citação não é critério de busca.

**Uma fonte fica fora do screening se:**
- é tutorial de conferência ou curso de referência usado como fonte (cap. 3); cursos só apontam seminais (cap. 4);
- é documentação de ferramenta fora do pilar ferramentas, ou é tutorial/API em vez de visão geral (cap. 3);
- está em outra língua que não inglês (cap. 10);
- não tem identificador (DOI/arXiv id) resolvível: não entra na Fase 2B até ter (cap. 8);
- a decisão de entrada exigiria leitura além da tabela do cap. 6: vira **dúvida**, resolvida pelo cap. 8.1 antes da saturação da divisão; não entra "por via das dúvidas".

**Uma extração de nível 3 é rejeitada se** (cap. 7):
- contém interpretação do agente em vez de transcrição (taxonomia parafraseada, contribuições resumidas com palavras próprias, juízo de relevância);
- registra "ilegível" sem segunda tentativa documentada por outra rota.

**Uma citação é rejeitada em texto assinado por mim se** (cap. 7): a fonte não está em nível 1.

**Um venue é rejeitado se** (cap. 8): a única evidência é o rodapé do PDF; vale o campo Comments do arXiv ou a página do publisher.

**Um termo do pool não vira divisão se** (cap. 2.1): nenhum survey aprovado o traz como divisão; fica com veredito "sem retorno" ou "não existe com esse nome" no confronto, e é aposentado se além disso nenhum survey o usa; é dado, não erro.
