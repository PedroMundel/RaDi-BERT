# Criterios Escritos Antes dos Testes - Semana 10

Na Semana 9 passei a escrever a regra de leitura de cada teste antes de rodar, depois que um ganho de 5 sementes sumiu com mais 10. Este documento lista os critérios da Semana 10: o que ficou fixado antes de cada rodada e o que o resultado deu contra a regra. Os textos completos, com data e hora, estão em docs/2026-11-18-gaps-da-argumentacao.md, no projeto.

A forma é a mesma em todos: a diferença entre dois braços é pareada por semente, com intervalo de 95%. Intervalo inteiro do lado bom conta como ganho, inteiro do lado ruim conta como perda, e cruzando o zero é nulo. Junto com um nulo vai o tamanho que o teste conseguiria enxergar.

## 1. Os testes e o que cada regra decidiu

Como ler: cada linha é um teste; "fixado antes" é o que eu não podia mais mudar depois de ver o número; "resultado contra a regra" é o veredito pela regra escrita, e não a minha impressão.

| Teste (data) | Fixado antes | Resultado contra a regra |
|---|---|---|
| Decoder nos 16 mil pares do e-SNLI (18/11) | decoder menos sem decoder em ROC-AUC; junto, dizer se o ganho pequeno do artigo cabe no intervalo | nulo: +0,003, cruzando o zero |
| Controle de calendário (18/11) | calendário menos sem decoder; decoder menos calendário; três leituras combinadas previstas | fora do previsto: o calendário ajuda (+0,007, nas 5 sementes), caso que eu não tinha escrito; com o mesmo calendário, o decoder perde 0,9 ponto de acurácia |
| Justificativa de outro par (18/11) | real menos trocada; antes de ler a nota, conferir que a troca funcionou pela perda do decoder | a conferência passou; a real fica 2,1 pontos acima da trocada |
| Curva de arranque (18/11) | medida principal: acurácia média nos cinco primeiros passos medidos; 11 passos escolhidos antes | o decoder arranca na frente (+4,1 pontos na medida principal) e termina 0,9 atrás |
| Fora do domínio de treino (19/11) | o MNLI decide, o RTE e o HANS ficam ao lado; passar com 5 sementes vira só candidato, que precisa de mais 10; conferir antes que cada modelo repete a acurácia do treino | perda: -1,5 ponto no MNLI, nas 5 sementes; sem candidato |
| Painel de quatro medidas (19/11) | as quatro medidas fechadas de uma vez: robustez, calibração, predição seletiva e pior classe; relatar as quatro; nenhuma quinta medida depois | três do lado ruim e uma nula |
| Justificativa de outro par, fora do domínio (19/11) | rodou em outro computador; a acurácia tinha de repetir a de 18/11 dentro de 0,6 ponto; diferença entre placas medida por um braço repetido | a conferência não passou, por 0,03 ponto; pela regra a rodada não se lê e os números ficaram só descritos |
| Peso da perda do decoder: 0, 0,05 e 0,5 (19/11) | exploratório, 3 sementes; a acurácia no dev decide; um valor que passe é só candidato | nulo nos três valores, todos abaixo do calendário em todas as sementes |

## 2. O que as regras me impediram de dizer

- Que o decoder ajuda nos 16 mil pares. A diferença bruta era positiva (+0,003), e só o controle de calendário mostrou que ela não era do decoder;
- Que o conteúdo da justificativa conta mais fora do domínio. Os números apontam para isso (2,9 pontos no MNLI contra 1,6 no dev), mas a conferência dessa rodada falhou por 0,03 ponto e a regra dizia para não ler;
- Que o calendário melhora a calibração. Apareceu nos números (5 de 5 sementes), mas essa comparação não estava entre as do painel, então ficou como observação;
- Que algum peso do decoder é melhor que outro. Com 3 sementes, diferenças de até cerca de 1 ponto não se distinguem.

## 3. Onde o processo falhou e o que mudei

- A primeira versão do critério do teste fora do domínio foi escrita com pressa e a rodada foi lançada sem salvar os modelos treinados e sem conferir antes se o teste saía do acaso. Parei a rodada antes de existir qualquer número do braço com decoder, reescrevi o critério e relancei salvando os modelos. A versão 2 declara o que eu já tinha visto até ali (só o braço de calendário);
- O limite de 0,6 ponto da conferência foi escolhido sem medida que o sustentasse, e o desvio entre sementes do braço que ele barrou já era de 0,6. Mantive o veredito da regra e registrei que o limite estava apertado;
- Uma das regras de 18/11 (a que lê se a escala curta explicava o nulo) foi escrita com LLM e eu não a confirmei antes da rodada. As frases que dependem dela estão marcadas no documento principal.

## 4. O que é meu e o que foi feito com LLM

Escolhi o que medir: o controle de calendário, a justificativa trocada, a pergunta do arranque, o teste fora do domínio, as quatro medidas do painel e os três valores de peso. O desenho de cada teste, os cortes e a redação das regras foram feitos com LLM (Claude), antes de cada rodada.
