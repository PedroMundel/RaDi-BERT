# Leituras Semana 4

**Como este documento foi feito:** a extração abaixo foi preparada com apoio de LLM, seguindo o meu Método de Leitura (as cinco paradas), sobre as partes de cada obra que o método indica. A minha leitura destas três obras está em andamento; quando terminar, as minhas anotações substituem estas.

As três obras foram escolhidas porque juntas cobrem a origem da destilação, um framework conceitual para decidir onde otimizar e um framework de software para servir LLMs.

## 1. Distilling the Knowledge in a Neural Network (Hinton, Vinyals e Dean, 2015)

arXiv:1503.02531. Partes usadas: resumo, seções 1, 2, 2.1, início da 3, 6 e 8.

**Promessa.** Tipo: fundador. Problema: um conjunto (ensemble) de modelos grandes generaliza bem, mas é caro demais para implantar para muitos usuários. Solução: treinar um modelo pequeno para imitar as probabilidades que o modelo grande dá a todas as classes, e não só a resposta certa; chamam isso de destilação. Número principal: no MNIST, uma rede pequena treinada do jeito normal erra 146 exemplos de teste; a mesma rede treinada com as probabilidades suaves de uma rede grande erra 74, perto dos 67 da rede grande (p. 4).

**Origem.** Antes: Buciluă, Caruana e colaboradores já tinham mostrado que o conhecimento de um ensemble cabe num modelo único, igualando os logits (p. 1-2). O que esta obra muda: uma solução mais geral, por temperatura, e a prova de que igualar logits é um caso particular dela (p. 2-3). Como pensar: a analogia do inseto, que tem uma forma de larva para se alimentar e outra adulta para se reproduzir; o modelo de treino e o de implantação não precisam ser o mesmo, porque os requisitos são diferentes (p. 1).

**Núcleo.**

- Conhecimento não são os pesos, é o mapeamento de entrada para saída. As probabilidades pequenas que o modelo dá às classes erradas carregam informação: uma BMW tem chance pequena de ser confundida com um caminhão de lixo, mas muito maior do que com uma cenoura (p. 2);
- Temperatura: o softmax ganha um parâmetro T; com T alto, a distribuição fica mais suave e mostra essas relações. O aluno é treinado com o mesmo T alto e usa T = 1 depois de treinado (p. 2-3);
- Perda: média ponderada de duas partes, a entropia cruzada com os alvos suaves do professor (em T alto) e a entropia cruzada com os rótulos verdadeiros (em T = 1), com peso bem menor na segunda. Os gradientes da parte suave precisam ser multiplicados por T ao quadrado para as duas partes manterem o peso relativo (p. 3);
- Com poucos dados: um modelo de fala treinado com só 3% dos dados e alvos suaves chega a 57,0% de acurácia de teste, contra 44,5% sem eles e 58,9% com 100% dos dados (Tabela 5, p. 8).

Divisão: destilação (compressão). Arquitetura: redes totalmente conectadas (MNIST) e um modelo acústico de fala; a obra não discute famílias de transformer, que vieram depois.

**Frameworks.** Diretriz: para comprimir um modelo grande, (1) gere alvos suaves com temperatura alta no professor, (2) treine o aluno com a mesma temperatura, misturando com os rótulos verdadeiros com peso menor, (3) use o aluno em temperatura 1 na implantação (p. 3).

**Fecho.** A própria obra deixa em aberto destilar de volta para um modelo único o conhecimento dos modelos especialistas que ela propõe (p. 8). Vocabulário: destilação, alvo suave (soft target), alvo duro (hard target), temperatura, logit, conjunto de transferência (transfer set), modelo especialista.

## 2. LLM Inference Unveiled: Survey and Roofline Model Insights (Yuan et al., 2024)

arXiv:2402.16363. Partes usadas: resumo, introdução, Figura 2 e seção 2 (p. 1-6).

**Promessa.** Tipo: mapa, com um framework próprio. Problema: a pesquisa sobre inferência eficiente de LLMs cresceu tão rápido que faltava um jeito sistemático de analisar os métodos. Solução: um survey que analisa cada técnica pelo modelo roofline, mais uma ferramenta aberta (LLM-Viewer) que faz essa análise para qualquer LLM em qualquer hardware (p. 1-3). Número principal: no Llama-2-7b numa GPU A6000, todas as operações da fase de geração (decode) são limitadas por memória, enquanto a maior parte do processamento do prompt (prefill) é limitada por computação (Tabela 1, p. 5).

**Origem.** O campo explodiu nos últimos dois anos (p. 2). Conversa com outros surveys da mesma época, sobre compressão de LLM (Zhu et al., 2023) e sobre serving (Miao et al., 2023), e se diferencia deles pela análise roofline (p. 2-3).

**Núcleo.**

- A arquitetura dominante dos LLMs é o transformer decoder: embedding, camadas com atenção multi-cabeça (MHA) e MLP, e uma cabeça que prevê o próximo token (p. 3);
- A inferência tem duas fases: prefill, que processa o prompt inteiro e cria o KV cache de cada camada, e decode, que gera um token por vez usando e aumentando esse cache (p. 3);
- Roofline: cada operação traz dados da memória, calcula e devolve. Se calcula muito e traz pouco dado, o gargalo é a computação (compute-bound); se traz muito dado e calcula pouco, o gargalo é a memória (memory-bound). O que separa os dois é a intensidade aritmética, operações por byte (p. 4-5);
- Divisão: a Figura 2 organiza a área em quatro níveis: compressão do modelo (quantização, poda, destilação, fatoração), algoritmos de decodificação rápida (saída antecipada, MoE, decodificação especulativa e outros), otimização de sistema (fusão de operadores, gerenciamento de memória, serving paralelo) e otimização de hardware (p. 2).

**Frameworks.**

- Diretriz (roofline, p. 4-5): (1) desenhe o roofline do hardware com o pico de computação e o pico de largura de banda de memória; (2) calcule a intensidade aritmética de cada camada; (3) se a camada está limitada por memória, use quantização, fusão de kernels ou lote maior; se está limitada por computação, use computação em menos bits;
- Consequência prática (p. 5): como o decode roda uma vez para cada token gerado e é limitado por memória, otimizar a memória da fase de decode é o que mais pesa no desempenho;
- Software: LLM-Viewer, ferramenta aberta que recebe o LLM, o hardware e a configuração de inferência e devolve o gargalo de cada camada e o uso de memória (p. 5-6).

**Fecho.** Vocabulário: prefill, decode, KV cache, roofline, intensidade aritmética, memory-bound, compute-bound, ponto de virada (turning point), operator fusion.

## 3. Efficient Memory Management for Large Language Model Serving with PagedAttention (Kwon et al., 2023)

SOSP 2023, arXiv:2309.06180. Partes usadas: resumo, seções 1, 3, 4, 4.1, 4.2 e 10.

**Promessa.** Tipo: sistema. Problema: para servir LLMs com vazão alta é preciso juntar muitas requisições num lote, mas o KV cache de cada requisição é grande e cresce e diminui durante a geração; mal gerenciado, desperdiça memória e limita o tamanho do lote. Solução: PagedAttention, um algoritmo de atenção inspirado na memória virtual com paginação dos sistemas operacionais, e vLLM, o sistema de serving construído sobre ele. Número principal: vazão de 2 a 4 vezes maior que FasterTransformer e Orca, com a mesma latência (p. 1).

**Origem.** Antes: os sistemas guardavam o KV cache de cada requisição num bloco contínuo de memória, reservado para o tamanho máximo possível da resposta; só 20,4% a 38,2% dessa memória guardava de fato os tokens (Figura 2, p. 2). Como pensar: a solução vem de outra área, sistemas operacionais; os autores reconhecem que o KV cache se comporta como a memória de um processo e reaproveitam uma ideia antiga e testada (p. 2, p. 14).

**Núcleo.**

- Onde a memória vai: num modelo de 13B numa A100 de 40 GB, cerca de 65% é dos pesos e perto de 30% é do KV cache (Figura 1, p. 1);
- O tamanho do problema: no OPT-13B, o KV cache de um único token ocupa 800 KB, e o de uma requisição de 2.048 tokens chega a 1,6 GB (p. 4);
- Três desperdícios dos sistemas anteriores: espaço reservado para tokens futuros, fragmentação interna (reservou para 2.048 e usou menos) e fragmentação externa (p. 4);
- PagedAttention: divide o KV cache de cada sequência em blocos de tamanho fixo, que podem ficar em lugares não contínuos da memória; a atenção é calculada bloco a bloco (p. 5);
- Gerenciador do KV cache: como numa memória virtual, blocos lógicos de cada requisição são mapeados para blocos físicos na GPU por uma tabela de blocos, e a memória é alocada sob demanda, sem reservar tudo antes (p. 5-6). Isso também permite compartilhar blocos entre sequências da mesma requisição (p. 2).

Divisão: inferência e serving. Arquitetura: transformer autorregressivo (decoder); o KV cache é um problema de quem gera token a token.

**Frameworks.** Software: vLLM, sistema de serving de LLMs de código aberto (github.com/vllm-project/vllm). Diretriz: quando um recurso cresce e diminui de forma imprevisível, aloque em blocos pequenos sob demanda, em vez de reservar o máximo de uma vez (p. 2, p. 5-6).

**Fecho.** Vocabulário: serving, vazão (throughput), lote (batch), KV cache, fragmentação interna e externa, paginação, bloco de KV, tabela de blocos.

## 4. O que estas três leituras somam

**Linha do tempo:**

| Ano | Marco | Fonte |
|---|---|---|
| 2006 | Buciluă, Caruana e colaboradores: conhecimento de um ensemble cabe num modelo único | citado por Hinton et al. (2015), p. 1 |
| 2015 | Hinton et al.: destilação com temperatura e alvos suaves | Hinton et al. (2015) |
| 2023 | Kwon et al.: PagedAttention e vLLM, memória paginada para o KV cache | Kwon et al. (2023) |
| 2024 | Yuan et al.: o roofline como forma de analisar a inferência de LLMs | Yuan et al. (2024) |

**Frameworks:**

| Framework | Tipo | Atividade | Fonte |
|---|---|---|---|
| Destilação com temperatura | diretriz | comprimir um modelo para implantar | Hinton et al. (2015), p. 3 |
| Roofline | diretriz | decidir o que otimizar num hardware | Yuan et al. (2024), p. 4-5 |
| LLM-Viewer | software | analisar gargalos de um LLM num hardware | Yuan et al. (2024), p. 5-6 |
| vLLM | software | servir LLMs com vazão alta | Kwon et al. (2023), p. 1 |

**Uma ligação entre as três:** o roofline (Yuan) explica por que a geração de tokens é limitada por memória; o vLLM (Kwon) ataca exatamente a memória do KV cache dessa fase; e a destilação (Hinton) reduz o modelo inteiro, o que diminui pesos e cache ao mesmo tempo.
