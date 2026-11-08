# Proposta de Tema
**Destilação de racionalização de LLM para modelos encoder-only**
Residência em IA — Pedro Mundel · 15 de set. de 2026 (rev. 2)

## O que estou construindo

Minha especialização é **eficiência de modelos para implantação**: fazer a capacidade de um modelo
grande caber onde ele não cabe — em custo de inferência, em quantidade de dado rotulado, em hardware
comum. O que eu quero saber fazer ao fim deste ciclo, e hoje não sei, é entender **em profundidade
como as três famílias de arquitetura — encoder, decoder e encoder-decoder — aprendem e o que cada
uma consegue ou não absorver.**

Este tema é uma análise dentro dessa área, não a área. Escolhi ele porque a pergunta atravessa as
três famílias na ordem em que a literatura as percorreu: o mecanismo nasce num encoder-decoder, é
portado para um decoder-only, e o que eu quero saber é o que sobra dele num encoder-only.

## De onde veio

O *Distilling Step-by-Step* (Hsieh et al., ACL 2023 Findings) treina um modelo texto-para-texto
(T5, encoder-decoder) a fazer duas coisas: prever o rótulo e gerar a justificativa que um LLM
produziu para aquele exemplo. O modelo aprende mais com menos dado. A justificativa **não é gerada
na inferência** — serve só como sinal de treino.

Lendo isso, me ocorreu a pergunta que virou o tema:

> **Como injetar esse conhecimento num modelo encoder-only, que não gera texto?**

A pergunta importa porque encoder é o que se usa de verdade para rotular em volume: uma passagem,
uns 110 milhões de parâmetros, contra um modelo generativo que produz um token por vez com bilhões.
Em aplicações como triagem de documentos ou verificação de consistência entre uma afirmação e sua
fonte, chamar um LLM para cada item não fecha a conta.

## O que já se sabe

O **DHRD** (Xu et al., NeurIPS 2025 Efficient Reasoning Workshop) faz algo próximo: acopla ao modelo
uma cabeça de raciocínio supervisionada pela justificativa do professor, **usada só no treino e
desligada no teste**. A acurácia sobe e o custo de inferência não muda. A ablação deles mostra que o
ganho vem do conteúdo da justificativa, não de um efeito genérico de regularização — justificativa
trocada por outra piora o resultado bem mais do que justificativa nenhuma.

Mas o DHRD usa um modelo **decoder-only**. E eles declaram no artigo que consideraram a via
bidirecional e a recusaram, por dois motivos: evitar que o modelo enxergue tokens futuros, e manter
coerência com o pré-treino autorregressivo.

**Nenhum dos dois motivos vale para a arquitetura que eu proponho.** No desenho deles, o texto, a
justificativa e o rótulo estão todos na mesma sequência de entrada — por isso o vazamento seria
real. Numa cabeça separada, a justificativa nunca entra na sequência do encoder. E encoder já é
pré-treinado bidirecionalmente, então não há coerência a preservar.

## O que eu proponho

Acoplar a um encoder uma cabeça auxiliar treinada a produzir a justificativa do professor, e
**descartá-la antes de entregar o modelo**. O que sobra é um classificador comum, com custo de
classificador comum.

O ponto que torna isso interessante além de barato: se a cabeça é descartada, qualquer ganho que
sobreviva **tem** que estar na representação do encoder, porque não sobrou outro lugar. Num modelo
texto-para-texto não dá para separar essas duas coisas.

## Como testar

Comparação controlada, variando só o que interessa:

| Condição | O que mede |
|---|---|
| Encoder sozinho | piso |
| Encoder + cabeça auxiliar | o efeito proposto |
| Encoder + cabeça auxiliar com texto aleatório | separa **conteúdo** de **ruído** |

Com várias sementes, e avaliando **dentro e fora do domínio de treino** — se o ganho só aparece em
dados parecidos com os de treino, o método vale menos do que parece.

**Resultado negativo também responde a pergunta.** Se a cabeça auxiliar não render nada, a conclusão
é que racionalização não transfere para encoders — e eu terei aprendido, com o objeto na mão, onde
está o limite entre o que um encoder e um decoder conseguem absorver. É esse aprendizado que eu
estou buscando; o resultado é o veículo.

## Viabilidade

Um encoder desse tamanho treina em minutos numa RTX 5060 de 8GB, então dá para rodar a grade inteira
várias vezes. O professor gera as justificativas uma vez, offline, e o arquivo é reaproveitado em
todos os experimentos.

## Em aberto

- **Tarefa e conjunto de dados.** O critério já está claro — precisa ser classificação e precisa
  exigir raciocínio, porque o próprio DHRD mostra que o ganho some em tarefas resolvidas por
  reconhecimento de padrão. Falta escolher entre português e inglês, e cada opção tem um custo.
- **Modelo base.**
- **Uma leitura obrigatória** (Agrawal et al., COLING 2025 Industry, Amazon), que aplica um
  mecanismo próximo sobre BERT. Ainda não li. Não é ameaça ao tema: é o método publicado que eu
  vou estudar, reproduzir e controlar — o que eles não fizeram (justificativa embaralhada, avaliação
  fora do domínio) é exatamente a parte que ensina.

## Principal risco

O DHRD parte do princípio de que o modelo **já tem** capacidade de raciocínio adquirida no
pré-treino, e que o treino apenas a traz à tona. Isso vale para modelos de bilhões de parâmetros. Um
encoder pequeno pode não ter nada a revelar — e aí a justificativa teria que **ensinar**, o que é
bem mais difícil. É o risco que questiona a premissa, e é o que o estudo vai descobrir.
