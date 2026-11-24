# Folha do gate de 11/11: o que foi feito e por quê

**Procedência:** escrita pelo Claude em 10/11 à noite, a pedido do Pedro, para ele ler antes do gate. Não é o
termo e não é texto de entrega. Os números vêm de `resultados/rte-pequenos/leitura-grade.md`,
`resultados/rte-msmarco/leitura-grade.md` e `resultados/rte-marcas/leitura-grade.md`. O código e as medidas foram
escritos e rodados pelo Claude; as ideias e decisões marcadas abaixo são do Pedro. O Pedro leu o Agrawal, Ahemad &
Sembium (2025); as leituras de resultado ele ainda não leu.

## 1. A história em seis frases

1. Tentei repetir o Agrawal, Ahemad & Sembium (2025) no RTE, na condição que o paper descreve.
2. Não se repete: o baseline deles (0,4754) fica abaixo de um modelo sem treino (0,58 a 0,62), o meu baseline dá
   0,767 e o decoder piora a nota (−0,049).
3. Chequei que não era erro meu, com três verificações.
4. Testei uma ideia própria, as marcas de atenção, com um controle de marca aleatória. Também não melhora a nota,
   nem no modelo grande, nem no pequeno, nem fora da distribuição.
5. Um resultado que parecia positivo (+0,017 em 5 sementes) caiu quando rodei 10 sementes novas (+0,002).
6. O que ficou de positivo: o modelo pequeno aprende a apontar as palavras que o LLM usaria para justificar, sem
   custo a mais na inferência.

## 2. O que mudou em relação ao Agrawal

No Agrawal (2025), o BERT classifica e, durante o treino, um decoder do T5 tem de escrever a justificativa lendo os
vetores do BERT. A aposta: para o decoder conseguir escrever, o BERT guarda o raciocínio nos vetores. No fim o
decoder é jogado fora.

| | Decoder (Agrawal 2025) | Marcas de atenção | Cabeça por token |
|---|---|---|---|
| O que se aproveita da justificativa | o texto inteiro | só quais palavras do par ela usa | só quais palavras do par ela usa |
| O que o modelo é cobrado a fazer | escrever a justificativa | fazer o `[CLS]` olhar para essas palavras | dizer, palavra por palavra, "marcada ou não" |
| Peça a mais no treino | um decoder inteiro | nenhuma | uma camada pequena |
| Perda | classificação + 0,1 × escrita, em três fases | classificação + 1 × atenção | classificação + 1 × marcação |
| Na inferência | o decoder é descartado | nada a descartar | a camada pode ficar, para dar o destaque |

As três mudanças, em ordem:

- **De "escrever" para "apontar"** (ideia do Pedro, 10/11). Sem decoder. Da justificativa sai só a lista de palavras
  do par que ela cita.
- **De modelo grande para pequeno** (ideia do Pedro, 10/11). BERT base (12 camadas) por BERT small (4 camadas).
- **De "a nota sobe?" para "o modelo aprende a apontar?"**. A primeira pergunta deu não em tudo; a segunda deu sim.

**O controle que sustenta tudo:** a marca aleatória. Mesmo treino, mesmas contas, mas com palavras sorteadas em vez
das palavras da justificativa. Se a marca real ganha da aleatória, o efeito vem do conteúdo da justificativa.

## 3. Os números que valem a pena saber de cor

Nota = ROC-AUC (0,5 é chute, 1,0 é perfeito), no dev do RTE, salvo indicação.

| O quê | Número |
|---|---|
| Baseline do paper no RTE | 0,4754 |
| Meu baseline com o mesmo tipo de BERT (MS-MARCO) | 0,767; com decoder −0,049 |
| BERT comum: sozinho × com decoder | 0,736 × −0,028 |
| BERT small: sem marcas × marca real (15 sementes) | 0,676 × 0,683 (+0,007, empate) |
| Fora da distribuição (e-SNLI, 9.842 pares): marca real − sem marcas | −0,004 (empate) |
| Marca real − marca aleatória | cerca de +0,05, em todas as rodadas |
| Atenção do `[CLS]` nas palavras marcadas: sem marcas × com marca real | 0,29 × 0,80 |
| Destaque (AP): marca real × melhor regra sem treino × sem marcas | 0,73 × 0,56 × 0,38 |
| Destaque (AP): cabeça por token | 0,75 |
| Ruído: o mesmo treino rodado duas vezes na GPU | difere em até 0,026 |

AP (precisão média): ordeno as palavras do par pela nota que o modelo dá e vejo se as marcadas vêm no topo. 1,0 =
todas no topo; ao acaso dá 0,26.

## 4. Perguntas prováveis e o que responder

**"Por que o paper não se repete?"** Não sei, e não afirmo que eles erraram. O que medi: o baseline deles é pior que
um modelo sem treino, o que sugere um problema na avaliação ou no checkpoint deles. Usei um checkpoint MS-MARCO
público (nboost), que não é garantidamente o deles. Existe um segundo checkpoint (Capreolus) que não rodei.

**"Como sabe que não é erro seu?"** Três checagens: (1) com o peso do decoder em zero, o modelo fica idêntico ao BERT
sozinho; (2) o corte de gradiente quase não atua; (3) um BERT sozinho treinado no mesmo calendário do decoder dá
0,746, então a queda não é falta de treino, vem da perda do decoder.

**"Se não melhora a nota, para que serve?"** Para a nota, não serve; esse é o resultado. O que serve é o destaque: o
modelo pequeno classifica e aponta as palavras que um LLM citaria, na mesma passada. Limites: só medi que ele imita o
LLM, não que ajuda uma pessoa; e o destaque não explica a decisão do modelo, porque mudar a atenção de 0,29 para
0,80 não mudou a nota.

**"Como pode mexer tanto na atenção e a nota não mudar?"** A atenção da última camada é só um dos caminhos até a
decisão. Na camada anterior o `[CLS]` já recolheu a informação (lá a atenção nas palavras marcadas é cerca de 0,4 em
todos os modelos treinados, com ou sem marca). Explicação provável, não medida diretamente.

**"Usou IA?"** Sim. O código e as medidas foram escritos e rodados com o Claude. Meus: a ideia das marcas, a de
trocar por um modelo mais fraco, a de testar nos pares não treinados, e as decisões do que rodar. A regra de parada
foi escrita antes do teste e eu aceitei antes de ver o resultado.

**"O que você aprendeu?"** Que 5 sementes com diferença pequena não são resultado (o +0,017 sumiu). Que resultado
precisa de controle (marca aleatória) e de critério escrito antes. Que um paper publicado pode não se repetir.

**"E agora?"** Só a próxima semana: decidir com o professor se sigo neste tema ou mudo o veículo. Opções já
anotadas, nenhuma decidida: levar o destaque para outra tarefa (reranqueador, análise de pronunciamento) ou comparar
com destilação comum.

## 5. Antes do gate, com as próprias mãos

- Abrir `resultados/rte-pequenos/destaque-exemplos.html` e olhar 5 pares: o destaque faz sentido?
- Ler as seções "Como ler" de `resultados/rte-pequenos/leitura-grade.md`.
- Conseguir desenhar a tabela da seção 2 sem olhar.

## 6. O que não dizer

- Que a justificativa "melhora" o modelo. Não melhora a nota.
- Que o destaque "explica" o modelo. Ele imita o LLM.
- Que o paper está errado. Só que não consegui repetir, e com o quê.
