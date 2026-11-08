# Racionalizações Humanas x LLM

O código da geração e da medida foi feito com apoio de LLM. Os critérios de qualidade, a avaliação das justificativas e as decisões são meus.

## 1. O que é racionalização no meu trabalho

Racionalização é a justificativa, em texto, de por que a resposta é aquela. No meu trabalho, ela é escrita por um LLM e usada só no treino: o modelo aluno aprende com ela, mas não precisa produzi-la na hora de responder.

Ela não é a mesma coisa que o CoT. O CoT é o modelo escrever o raciocínio na hora de responder, antes da resposta. A racionalização é o texto em si, e pode vir antes da resposta, guiando-a, ou depois, justificando-a. No e-SNLI e no meu piloto, ela vem depois: quem escreve já conhece o rótulo.

Exemplo:

- Pergunta: qual membro serve para chutar uma bola?
- Resposta: pé.
- Racionalização: "para chutar se usa o pé".

## 2. Tarefa e dataset

Escolhi inferência textual (NLI): dado um par de frases, premissa e hipótese, classificar se a hipótese decorre da premissa, é neutra ou a contradiz. O dataset é o e-SNLI.

| Rótulo | Significa | Exemplo |
|---|---|---|
| Implicação | se a premissa é verdade, a hipótese com certeza é | "Two women are embracing while holding to go packages." -> "Two woman are holding packages." |
| Neutro | pode ser verdade, mas a premissa não garante | a mesma premissa -> "The sisters are hugging goodbye..." |
| Contradição | se a premissa é verdade, a hipótese não pode ser | "...boys play football..." -> "dog eats out of bowl" |

Escolhi o e-SNLI porque:

- já tem justificativa humana escrita, uma por par no treino e três na validação e no teste;
- tem a classe de contradição;
- muitas vezes o rótulo depende de uma informação que não está escrita no par, e é essa informação que a justificativa pode ensinar ("floresta verde" -> "a floresta não está morta").

Limitações: é em inglês, e as premissas são legendas de fotos, com frases simples.

## 3. Gerar justificativa de LLM é barato

Gerei justificativas para 1.000 pares da validação do e-SNLI (334 de implicação, 333 neutros e 333 de contradição) com dois modelos, o Claude Haiku 5.5 e o Claude Sonnet 5.5, pela API em lote. O prompt dá premissa, hipótese e rótulo, como foi dado aos anotadores do e-SNLI, e pede uma explicação de uma ou duas frases sem citar o nome do rótulo.

Resultado: 2.000 de 2.000 pedidos com sucesso, em cerca de 11 minutos, por US$ 0,64.

| Pares | Haiku 5.5 | Sonnet 5.5 |
|---|---|---|
| 100 mil | cerca de US$ 3,50 | cerca de US$ 60 |
| Treino inteiro (549 mil) | cerca de US$ 19 | cerca de US$ 330 |

O treino inteiro com Haiku cabe no meu orçamento de API, e um subconjunto com Sonnet também.

## 4. As justificativas humanas são inconsistentes

Comparei, em 20 pares, a justificativa humana e as dos dois LLMs. Os LLMs apareceram em ordem sorteada e sem nome, e eu só soube quem era quem no fim. Os critérios foram três:

- está correta (justifica o rótulo pelo motivo certo), ou é pobre;
- se sustenta sozinha (fora do par, continua verdadeira e com sentido);
- é circular (só repete a conclusão, petição de princípio).

| | Correta | Pobre | Se sustenta sozinha | Circular |
|---|---|---|---|---|
| Humano | 13 | 7 | 15 | 0 |
| Haiku 5.5 | 17 | 1 | 18 | 1 |
| Sonnet 5.5 | 19 | 1 | 19 | 1 |

A melhor justificativa do par foi a do Sonnet em 14 de 20 pares, a do Haiku em 3, a humana em 1, com 2 empates.

Exemplo do que considerei pobre:

- Par: "A dirt bike rider riding through the woods over logs." -> "The dirt bike rider is riding a dirt bike." (implicação)
- Humano: "A rider riding through the woods must be riding a dirt bike."
- Sonnet: "a dirt bike rider is by definition someone riding a dirt bike. So the hypothesis restates what the premise already implies and must be true..."

A humana tira a conclusão da coisa errada: andar pelo mato não implica moto de trilha, pode ser cavalo ou mountain bike. Fora do contexto, ela perde o sentido. A do Sonnet se sustenta fora do contexto, mesmo sendo uma petição de princípio.

Algumas justificativas humanas de implicação parecem cometer petição de princípio, e outras são espantalho ou tautologia.

## 5. Quanto da justificativa já está escrito no par

Para ver se isso vale para o conjunto todo, medi quanto das palavras de cada justificativa já está na premissa ou na hipótese. A medida é a fração das palavras de conteúdo da justificativa (sem palavras vazias como "the" e "is") que aparecem no par. Como controle, fiz a mesma conta contra o par de outro exemplo sorteado.

| Fonte | Justificativas | Copiado do par | Copiado só da hipótese | Controle | Não acrescenta nenhuma palavra | Palavras novas (mediana) |
|---|---|---|---|---|---|---|
| Humano, validação inteira | 29.521 | 76,5% | 46,8% | 3,5% | 30,6% | 1 |
| Humano, 1.000 pares do piloto | 1.000 | 77,2% | 48,1% | 3,1% | 33,1% | 1 |
| Haiku 5.5, os mesmos 1.000 | 1.000 | 42,2% | 23,5% | 1,9% | 0,1% | 8 |
| Sonnet 5.5, os mesmos 1.000 | 1.000 | 49,3% | 26,9% | 2,3% | 0,3% | 6 |

O que tirei:

- uma em cada três justificativas humanas não acrescenta nenhuma palavra ao par;
- a cópia é maior na implicação (85% no humano), onde eu tinha visto petição de princípio;
- as de LLM quase sempre acrescentam palavras;
- copiar menos não é ser melhor: o Sonnet copia mais que o Haiku e foi o melhor na avaliação do item 4;
- a cópia não é coincidência de vocabulário, porque contra outro par ela cai para 2% a 3,5%.

## 6. Licença

Antes de usar as justificativas do Claude para treinar, conferi os termos comerciais da Anthropic (vigência de 17/06/2025, seção D.4). A restrição é usar o serviço para treinar modelo concorrente. O meu aluno é um classificador encoder de NLI, que não gera texto e não substitui o Claude. Por cuidado, não vou publicar os pesos do modelo nem o dataset gerado. Se precisar de uma alternativa sem ambiguidade, há modelos de pesos abertos sob licença Apache 2.0, como o Qwen3.

## 7. O que isso permite

- Comparar o treino do encoder com justificativa humana e com justificativa de LLM;
- comparar também com a racionalização extrativa: o e-SNLI tem as palavras que o anotador destacou no par. Com três braços (destaques humanos, justificativa humana, justificativa de LLM), dá para separar o efeito de quem escreve do efeito de como escreve;
- escolher os pares pela qualidade da justificativa ao reduzir o dataset, já que a destilação permite treinar com menos dados e, com menos dados, cada exemplo pesa mais.

## 8. Limitações

- A avaliação de qualidade foi em 20 pares, feita só por mim;
- a medida de cópia conta palavras, não sentido, e não junta formas como "hug" e "hugging";
- tirei das justificativas as palavras de roteiro ("premise", "hypothesis", "true"...), para elas não contarem como informação nova, e essa escolha muda os números dos LLMs;
- as justificativas de LLM foram geradas com o rótulo no prompt.
