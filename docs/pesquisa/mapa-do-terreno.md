# Mapa do terreno — como julgar pesquisa em IA

Escrito em 09/09/2026, depois que Pedro identificou o problema real: não é indecisão, é falta de
referencial. Sem o mapa, escolher entre vinte temas é escolher entre vinte nomes.

Este arquivo não propõe tema. Ele entrega a régua para você julgar qualquer tema — inclusive os
que eu propus, inclusive os que a banca vai questionar.

---

## 1. A unidade da pesquisa é a ALEGAÇÃO, não o artefato

O erro mais comum de quem vem de uma formação orientada a entrega: achar que pesquisa é construir
algo impressionante. Não é. Pesquisa é produzir **uma afirmação sobre o mundo que sobrevive ao
escrutínio de gente tentando derrubá-la**.

O sistema que você constrói é instrumento. A alegação é o produto.

Teste rápido: se você não consegue escrever a sua contribuição como uma frase declarativa que
alguém poderia contestar com evidência, você ainda não tem pesquisa — tem projeto.

- "Construí um pipeline que estrutura documentos" → não é alegação. Ninguém pode contestar.
- "Verificação aprendida detecta 78% dos erros de extração a 5% de falso positivo" → é alegação.
  Alguém pode replicar e discordar.

---

## 2. Os cinco tipos de alegação (e o que cada um custa)

Toda pesquisa empírica em IA faz uma dessas cinco. Elas não têm o mesmo preço nem o mesmo risco.

| Tipo | Forma da alegação | Custo típico | Risco principal |
|---|---|---|---|
| **Método novo** | "X funciona" | Alto — precisa implementar e vencer baselines | Não vencer; ou vencer por motivo errado |
| **Comparação** | "X supera Y sob condição Z" | Médio — precisa rodar todos com rigor igual | Baseline fraco invalida tudo |
| **Caracterização** | "X se comporta assim quando varia W" | Médio-alto — precisa de muitos pontos | Efeito sumir no ruído |
| **Crítica de medição** | "o que se acredita sobre X está mal medido" | **Baixo** — pode ser só reanálise | Estar errado publicamente |
| **Recurso** | "existe agora um dataset/benchmark que não existia" | Médio — trabalho braçal | Ninguém usar |

Duas coisas contraintuitivas aqui, e as duas importam para você:

**O tipo mais barato não é o menos valioso.** "Are Emergent Abilities a Mirage?" não treinou
nenhum modelo, reanalisou resultados publicados, e levou Outstanding Paper no NeurIPS. Custo
computacional ~zero.

**O tipo mais caro não é o mais valorizado.** Relatórios técnicos de modelos treinados em cluster
consomem meses de GPU e frequentemente valem como documentação, não como descoberta.

---

## 3. O que torna uma pergunta DIFÍCIL de verdade

Aqui está a distinção que quase ninguém explicita, e que é a que te falta.

**Parece difícil, é fácil:**
- Nome grande, dataset grande, tema da moda. A dificuldade é de acesso a recurso, não de pensamento.
- "Aplicar X em Y", quando X e Y existem e o encanamento é conhecido.
- Qualquer pergunta cuja resposta você já sabe antes de rodar. ("Mais dado ajuda?" Ajuda.)

**É difícil de verdade:**
- Você não consegue prever o resultado antes de medir.
- A própria medição é contestável — não está claro *como* medir aquilo.
- Um resultado negativo seria tão interessante quanto um positivo.
- **Existe um confundidor não óbvio**: algo além da sua variável poderia explicar a diferença.

Esse último é o coração. **A dificuldade da pesquisa está em isolar o efeito, não em rodar o
código.** Escrever o script é a parte fácil e sempre foi.

Exemplo real, do nosso próprio levantamento: o Gervásio comparou um modelo adaptado ao português
contra o LLaMA-2 base e achou ganho enorme. Só que o LLaMA-2 base não segue instrução — boa parte
do ganho é efeito do *instruction-tuning*, não da adaptação ao idioma. Os dois efeitos estão
grudados. Perceber isso é a habilidade; rodar o experimento não é.

---

## 4. O que a área chama de contribuição

A moeda é **redução de incerteza para outra pessoa**.

Teste prático, e é o único que importa: **quem muda de comportamento por causa do seu resultado, e
o que faz de diferente?** Se ninguém muda nada, não é contribuição — não importa quanto trabalho deu.

E daí decorre a regra que mais destoa de quem vem de entrega:

> **Esforço não é contribuição.** Os dois são independentes.

Você pode queimar três meses de GPU e não reduzir incerteza nenhuma. Você pode passar duas semanas
reanalisando tabelas dos outros e mudar como um campo inteiro reporta resultado. Na sua formação
até aqui, entregar mais = valer mais. Aqui essa relação simplesmente não existe.

---

## 5. Os seis instrumentos de julgamento

Com estes seis conceitos você consegue interrogar qualquer proposta de pesquisa — a minha, a de um
paper, a sua. São as ferramentas, não jargão.

**1. Baseline.** Contra o que você compara. Um baseline fraco invalida qualquer resultado: vencer
alguém que não estava tentando não prova nada. Pergunta a fazer sempre: *o baseline foi ajustado
com o mesmo cuidado que o método proposto?*

**2. Confundidor.** O que mais, além da sua variável, poderia explicar a diferença observada.
Pergunta: *se eu tirasse a minha contribuição e mantivesse o resto, o resultado sumiria?*

**3. Ablação.** Remover uma peça por vez para ver se ela importava. É a resposta ao confundidor. Um
trabalho com três componentes e sem ablação não sabe qual dos três funcionou — e provavelmente só
um funcionou.

**4. Tamanho do efeito versus ruído.** Rodar o mesmo experimento duas vezes com sementes diferentes
já dá resultados diferentes. Se a sua melhoria for menor que essa variação, você não mediu nada.
Pergunta: *quantas sementes? qual o desvio?* Muito paper não responde.

**5. Teto e piso.** Toda medida precisa de referência nos dois extremos. O piso é o resultado sem
nada (modelo base, chute aleatório). O teto é o melhor possível no seu setup (oráculo, especialista
humano, modelo separado por tarefa). Sem os dois, "0,84 de F1" não significa nada.

**6. Validade externa.** Se vale fora do seu setup. Um resultado em um dataset, um idioma, um
tamanho de modelo, é um ponto — não uma lei. Honestidade aqui separa trabalho sério de propaganda.

---

## 6. O seu regime: o que as restrições excluem e o que liberam

Restrições: RTX 5060 8GB, sem verba, 16 semanas, sozinho, primeiro artigo, venue de aceitação
~40–50%.

**O que isso EXCLUI:**
- Alegações de escala ("X funciona em 70B") — sem hardware.
- Método novo que precisa vencer estado da arte — sem compute para competir.
- Relatório técnico de treino grande — sem cluster.

**O que isso LIBERA — e não é prêmio de consolação:**
- Comparação rigorosa, se os artefatos comparados já existem abertos.
- Caracterização em escala pequena (curvas com modelos pequenos).
- Crítica de medição (a mais barata e a de maior teto).
- Recurso, quando o trabalho é braçal e não computacional.

Repare no padrão: **as suas restrições cortam exatamente os tipos que dependem de recurso, e deixam
intactos os que dependem de pensar.** Esses são justamente os tipos em que uma pessoa sozinha ainda
compete — e é por isso que eles não são o plano B.

Uma consequência prática que vale ouro: **quando o artefato caro já foi produzido e publicado
aberto por outra pessoa, a pergunta cara vira barata.** Você não precisa pré-treinar para estudar
o efeito de um pré-treino, se os modelos pré-treinados estão no Hugging Face.

---

## 7. Onde cai a direção escolhida

### Destilação de racionalização de LLM para encoder

- **Tipo de alegação:** comparação + caracterização ("o canal de saída transfere conhecimento para
  um encoder; o canal de atenção não") — os dois tipos que o meu regime libera.
- **Dificuldade real:** média-alta, e no lugar certo. O confundidor principal é separar *conteúdo da
  racionalização* de *efeito de ter um objetivo auxiliar qualquer*, e ele é controlável com o
  controle de tokens aleatórios. Não consigo prever o resultado antes de medir.
- **Quem muda de comportamento:** quem decide entre pagar inferência de LLM por item ou ajustar um
  encoder pequeno. Decisão recorrente, com orçamento atrás — e os dois trabalhos mais próximos são
  de indústria, o que confirma que a decisão existe.
- **Custo:** baixo. Encoder de ~110M treina em minutos; o professor roda uma vez, offline.
- **Falsificável nos dois sentidos:** se o canal de saída também for ruído, a conclusão fecha uma
  pergunta aberta em vez de não produzir nada.
- **Veredito honesto:** a novidade é modesta — sustenta-se em três contribuições somadas, não numa
  alegação grande. Para um primeiro artigo, é o formato normal.

## 7b. Referência de apoio — quem faz o quê entre as arquiteturas

| | Como lê e treina | O que produz | Tarefas | Exemplos (e em pt-BR) |
|---|---|---|---|---|
| **Encoder-only** | Lê tudo de uma vez, **bidirecional**; treina prevendo tokens mascarados | Vetor por token + vetor da sequência. **Não gera texto** | Classificação, rotulagem de token (NER, POS), QA extrativa, embeddings para busca | BERT, RoBERTa, DeBERTa · BERTimbau, Albertina, BioBERTpt, DeBERTinha |
| **Decoder-only** | Esquerda para direita, **causal**; treina prevendo o próximo token | Texto, por construção | Geração, conversa, instrução, few-shot, raciocínio, código | GPT, LLaMA, Mistral, Qwen · Sabiá, Bode, TeenyTinyLlama |
| **Encoder-decoder** | Encoder lê bidirecional, decoder gera condicionado | Texto condicionado a uma entrada | Tradução, resumo, "tudo é texto→texto" | T5, BART, mT5 · PTT5 |

Regra prática: saída é **rótulo ou trecho** → encoder-only, ordens de grandeza mais barato · saída é
**texto derivado de uma entrada** → encoder-decoder foi a escolha clássica · saída é **texto e você
quer um modelo para tudo** → decoder-only, que venceu em escala.

O detalhe econômico: encoder faz **uma passagem** com ~110M parâmetros; decoder gera **um token por
vez** com bilhões. Por isso decoder-only dominou o uso geral, mas encoder-only continua sendo o que
roda em produção para rotular em volume — e é por isso que os modelos de domínio abertos em
português são todos encoders.

## 7c. Destilar sem ter um modelo de bilhões de parâmetros

O ponto que muda tudo: **o custo do professor é único e offline.** Gera-se a racionalização (ou o
rótulo suave) **uma vez** para o conjunto de treino, salva em arquivo, e todos os experimentos leem
esse arquivo. Não é custo recorrente, é um lote que roda uma noite.

Caminhos, do mais barato ao mais caro: (1) datasets que já vêm com racionalização anotada — elimina
o professor; (2) modelo aberto 7–8B em 4-bit rodando local, gerando em lote; (3) GPU gratuita na
nuvem (Kaggle, Colab) para um professor maior; (4) cota gratuita de API, verificando limites.

E o movimento que transforma a restrição em achado: **a qualidade do professor vira variável
experimental.** "Quão bom precisa ser o professor para a racionalização ainda ajudar?" é pergunta
legítima, e se um modelo aberto pequeno entregar quase o mesmo que um enorme, isso é resultado útil
para todo mundo sem verba. Ressalva: professor aberto é mais fraco em português, e gerar em inglês
para traduzir introduz confundidor.

## 8. Como usar este mapa para decidir

Ordem das perguntas, e vale para qualquer candidato a tema:

1. **Qual é a alegação?** Escreva em uma frase contestável. Se não sair, não é tema ainda.
2. **De que tipo ela é?** (dos cinco) — isso já diz o custo e o risco.
3. **Eu consigo prever a resposta?** Se sim, não vale a pena medir.
4. **Qual o confundidor principal, e eu consigo controlá-lo?** Se não existe confundidor, a pergunta
   provavelmente é fácil demais. Se existe e você não consegue controlar, é difícil demais.
5. **Quem muda de comportamento com a resposta?** Se ninguém, pare aqui.
6. **Cabe no meu regime?** (seção 6)
7. **O que eu aprendo executando isso?** — o critério que faltava, e o único que a residência
   deveria priorizar acima dos outros.

Se um tema passa nos sete, ele é seu. Se falha em um, você sabe exatamente onde, e o conserto é
local — não precisa recomeçar de duzentas opções.
