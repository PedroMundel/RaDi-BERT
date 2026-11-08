# Geracao do Primeiro Lote

## 1. O pedido virou pergunta (versao F)

Na versao E, a da semana anterior, o modelo recebia premissa, hipotese e rotulo e tinha de explicar por que o rotulo
estava certo. Defendendo um rotulo, ele falava do texto ("the premise shows...", "this confirms...") em vez de trazer o
conhecimento que liga as duas frases.

Na versao F, o par vira uma pergunta "por que" sobre a cena. Sai o enquadramento de anotacao, saem os campos premissa,
hipotese e rotulo, e o rotulo so escolhe o formato da pergunta. Os 12 exemplos sao os mesmos da versao E, reescritos
no formato pergunta e resposta.

**Versao E, para o par 25 (so o fim do prompt):**

```
Premise: A woman is walking with a boy who is holding a flag.
Hypothesis: A lady is next to a child who has a flag.
Label: entailment

Explain in one sentence (about 30 words at most) why this label is correct, stating the world
knowledge that links the premise to the hypothesis. For entailment, cover what the hypothesis adds;
for neutral, give an alternative the premise allows; for contradiction, say why both cannot happen
in the same scene. Follow the style of the examples. Do not name the label. Write only the
explanation.
```

**Versao F, para o mesmo par (so o fim do prompt):**

```
Question: If a woman is walking with a boy who is holding a flag, why does that mean a lady is next
to a child who has a flag?

Answer in one sentence (about 30 words at most) with the world knowledge behind the answer.
Follow the style of the examples. Write only the answer.
```

**Os tres formatos de pergunta (o rotulo escolhe um):**

```
implicacao:  If {premissa}, why does that mean {hipotese}?
neutro:      If {premissa}, why does that not necessarily mean {hipotese}?
contradicao: If {premissa}, why can't it also be that {hipotese}, in the same place and moment?
```

**Um dos 12 exemplos, no formato da F:**

```
Question: If a biker wearing a white t-shirt is jumping over dirt hills, why can't it also be that a
biker climbs a tree in a shirt, in the same place and moment?
Answer: Jumping over dirt hills requires being on the ground, while climbing a tree means being up
in it.
```

### Resultado nos 45 pares (Qwen3.5-9B)

Mesmos 45 pares da semana anterior. Contagens por lista de expressoes; a copia e a fracao de palavras de conteudo da
justificativa que ja estao no par. Rodando a mesma versao duas vezes, as contagens variam em ate cerca de 6 casos,
entao so diferencas maiores que isso contam.

| Medida | Humano | E | F |
|---|---|---|---|
| Palavras (mediana / maxima) | 11 / 24 | 24 / 34 | 23 / 30 |
| Nomeia o rotulo | 0 | 6 | 1 |
| Palavra de relacao (contradicts, confirms, implies...) | 8 | 25 | 12 |
| Fala de "premise" ou "hypothesis" | 0 | 13 | 0 |
| Texto sobre o texto ("describes", "stated", "mentions") | 0 | 12 | 5 |
| Copia do par (mediana) | 0,86 | 0,36 | 0,36 |

### Os mesmos pares nas duas versoes

| Par | E (defende o rotulo) | F (responde a pergunta) |
|---|---|---|
| 359, neutro. P: A woman sits in a chair under a tree and plays an acoustic guitar. H: A woman is playing a country song on her guitar while her husband in the distance listens. | The premise shows a woman playing guitar but provides no information about her husband's presence or whether she is playing a country song. | Women play many music genres besides country, and they often perform solo without an audience or a husband present nearby. |
| 407, neutro. P: Four men riding in a gray, fast moving boat appear to be wearing vests. H: Four men are racing their boat for pink slips. | Boats are raced for various reasons like trophies or charity, not exclusively for pink slips, so the specific motive mentioned is not confirmed by the premise. | Men riding in a fast boat wearing vests could simply be safety-equipped participants enjoying a ride, not necessarily competitors racing for money. |
| 73, implicacao (eco). P: A man sleeping on the ground in a subway. H: There is a man on the ground. | Since a man sleeping on the ground is necessarily located on the ground, this scenario confirms that there is a man on the ground. | A man sleeping on the ground implies his body rests directly on it, making him physically located on the ground within the subway. |
| 976, contradicao. P: Musicians are performing on stage. H: A clown is juggling balls at a circus. | (...) making the hypothesis an unrelated alternative rather than a necessary outcome or direct conflict. | Performing on stage refers to musicians playing music, while juggling balls describes a specific circus act that does not require musical performance. |

Nos neutros, a F traz o conhecimento que abre a alternativa, e a E diz so que a premissa nao informa. No eco (par 73) as
duas quase repetem o par, porque nao ha o que explicar. No par 976 as duas leem a cena como neutra: a cena permite as
duas coisas, entao o problema e o par, nao o pedido.

## 2. Velocidade e escolha do modelo

Medi quantos segundos cada par leva quando o servidor recebe varios pedidos ao mesmo tempo. O ajuste que mais ajudou
foi diminuir o pedaco do prompt que o servidor reprocessa a cada pedido (os 12 exemplos sao fixos e se repetem).

**Qwen3.5-9B (90 pares, segundos por par):**

| Configuracao do servidor | 1 pedido | 2 | 4 | 8 |
|---|---|---|---|---|
| padrao | 0,63 | 0,50 | 0,42 | 0,41 |
| ajustada (-cms 0 -ub 128) | 0,52 | 0,38 | 0,31 | 0,28 |

**Qwen3.6-35B-A3B (30 pares, parte dos experts na RAM, segundos por par):**

| Configuracao do servidor | 1 pedido | 2 | 4 |
|---|---|---|---|
| padrao | 2,22 | 1,82 | 1,83 |
| ajustada (-np 4 -kvu -cms 0 -ub 128) | 1,89 | 1,74 | 1,66 |

O 35B ganha pouco com pedidos simultaneos porque parte dele roda na CPU. Com a mesma configuracao, a rodada se repete
palavra por palavra; mudar o numero de pedidos muda o texto, mas nao o tamanho nem as contagens da tabela da secao 1.

**Conta, nao medida: horas de geracao**

| Modelo | s/par | 10 mil pares | 100 mil pares |
|---|---|---|---|
| 9B, 8 pedidos | 0,28 | cerca de 47 min | cerca de 7,8 h |
| 35B, 4 pedidos | 1,66 | cerca de 4,6 h | cerca de 46 h |

**Escolhi o 35B mesmo sendo cerca de 6 vezes mais lento**, porque erra menos nos casos dificeis. Nos mesmos 90 pares,
na contagem feita com apoio de LLM, a versao F do 35B teve de 3 a 4 justificativas erradas, e a do 9B, cerca de 10. A
avaliacao humana em andamento e que vai medir isso com mais gente.

## 3. O primeiro lote

- **Pares:** o treino inteiro do e-SNLI (549.339 pares com texto completo) embaralhado com semente 42. O lote segue
  essa ordem, entao qualquer comeco do arquivo e uma amostra aleatoria do treino e da para testar o treino com
  quantidades diferentes de dados sem gerar de novo;
- **Modelo e pedido:** Qwen3.6-35B-A3B, versao F, mesma amostragem da semana anterior;
- **Resultado:** 16.000 pares em 5h20, a 1,20 s/par, numa noite, sem queda do servidor;
- **Rotulos:** 5.406 neutro, 5.320 implicacao, 5.274 contradicao;
- **Tamanho:** 22 palavras na mediana e 37 no maximo. Todas as respostas terminaram sozinhas, nenhuma foi cortada.

**Comando do servidor:**

```
llama-server -m Qwen3.6-35B-A3B-UD-IQ4_XS.gguf -ngl 999 --n-cpu-moe 30 -c 8192 -np 4 -kvu -cms 0
             -ub 128 --jinja --host 127.0.0.1 --port 8080
```

## 4. Marca de eco

Eco e o par em que a hipotese so repete um pedaco da premissa: nao ha o que explicar alem de repetir. Marquei esses
pares em vez de apagar, para depois testar se a cabeca auxiliar aprende algo neles.

**Regra:** implicacao em que a hipotese nao tem nenhuma palavra de conteudo fora da premissa. Palavras de conteudo sao
as palavras sem as mais comuns do ingles (artigos, preposicoes, verbos auxiliares). Sem juntar singular e plural, entao
"boy" e "boys" contam como palavras diferentes e o eco real e um pouco maior que o contado.

**Conferencia no conjunto de validacao do e-SNLI (9.842 pares):** a regra repete a contagem da semana anterior, casa por
casa.

| Rotulo | 0 palavras novas | 1 | 2 | 3 ou mais |
|---|---|---|---|---|
| implicacao | 25,4% | 38,3% | 22,2% | 14,0% |
| neutro | 0,7% | 23,3% | 32,3% | 43,7% |
| contradicao | 3,6% | 19,4% | 31,2% | 45,8% |

**No lote (16.000 pares):**

| Rotulo | 0 palavras novas | 1 | 2 | 3 ou mais |
|---|---|---|---|---|
| implicacao | 23,5% | 38,8% | 23,4% | 14,2% |
| neutro | 1,9% | 26,2% | 32,0% | 39,9% |
| contradicao | 3,3% | 21,0% | 31,6% | 44,2% |

**1.252 pares de eco, 7,8% do lote e 23,5% das implicacoes.** Contando as implicacoes com ate 1 palavra nova, o teto
sobe para 62,3% delas: com uma palavra nova muitas vezes ainda ha ponte (man -> human), entao esse e o limite, nao a taxa.

**Tres pares de eco do lote, com a justificativa do Qwen:**

| Premissa | Hipotese | Justificativa |
|---|---|---|
| A man in a striped shirt tugging something away from a dog. | The man and dog is tugging. | The man actively tugs the object, and since the dog holds it too, their combined action constitutes a game of tug-of-war between them. |
| Five children are playing on a large round swinging net. | Some children are on a large net. | Playing on the net requires being physically located on it, so the five children are indeed situated on the large net. |
| Three young boys are swimming in a body of water near a boat. | Three boys swimming near a boat | Three young boys are explicitly stated to be swimming in water near a boat, so the description directly confirms they are three boys swimming near a boat. |

Nos pares de eco, o Qwen copia menos do par que a justificativa humana (mediana de 0,38 das palavras de conteudo,
contra 0,83) e traz cerca de 6 palavras novas, contra 1. Parte delas e enchimento, como "explicitly stated" e "directly
confirms" no terceiro par, e a contagem de palavras nao separa enchimento de ponte. Quem separa e a leitura.

Os pares em que o modelo discorda do rotulo do e-SNLI ainda nao foram marcados.
