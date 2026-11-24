# Termo de Aceite de Entrega — Semana 9

- **Data da Reunião ("Gate") de aprovação:** `[preencher]`
- **Participante:** Pedro Mundel — `[matrícula]`

> Rascunho do Claude (11/11), para o Pedro adaptar. Ver "Escolhas abertas" no fim.

---

**Resumo das Semanas 1 a 8:**

Defini o tema, Destilação de Racionalização de LLM para Encoders, dentro da área em que quero me especializar,
eficiência de modelos para implantação. Fiz o screening da área até chegar a uma lista de obras atuais e a um
método de leitura. Na sexta semana escolhi a tarefa, inferência textual no e-SNLI, e comparei as justificativas
humanas com as de LLM. Na sétima Semana, passei a gerar as justificativas com um modelo aberto, Qwen. Testei versões
do prompt nos mesmos pares e vi que a forma da justificativa vem do pedido e dos exemplos, e não das definições dos
rótulos, então escrevi os 12 exemplos que definem o tom do dataset. Na oitava Semana, troquei o pedido por uma
pergunta sobre a cena, gerei o primeiro lote de 16 mil pares e montei uma avaliação humana das justificativas.

**O que fiz nesta nona Semana:**

- A placa-mãe do meu computador queimou e precisei trocá-la. Enquanto a nova não chegava, rodei os modelos por SSH no
  computador de um amigo, nos horários em que ele não estava usando. Isso atrasou bastante o desenvolvimento. Para
  ainda entregar um trabalho de qualidade neste gate e rodar todos os experimentos que eu queria, fiz parte do
  trabalho com auxílio pesado de LLM: o código dos treinos, as rodadas e a leitura dos resultados;
- Escolhi o Agrawal, Ahemad & Sembium (2025) como obra-base e repeti o treino deles, um BERT com um decoder auxiliar
  que escreve a justificativa, no RTE, um dos conjuntos do paper. Como o paper não traz o prompt, gerei as
  justificativas do RTE com o Qwen e tomei as decisões sobre o que o paper não diz;
- O resultado do paper não se repetiu. O baseline deles (0,4754) fica abaixo de um modelo sem treino nenhum, o meu
  deu 0,767, e com o decoder a nota caiu em vez de subir;
- Medi de onde vem a queda: um BERT treinado no mesmo calendário, sem o decoder, não cai. A queda vem da perda do
  decoder, e não de erro no código ou de menos treino;
- Testei uma ideia minha: em vez de escrever a justificativa, o modelo é cobrado a prestar atenção nas palavras do
  par que ela usa, sem decoder. Como controle, o mesmo treino com palavras sorteadas. A marca real ganha da sorteada
  em todas as rodadas, mas não ganha do treino normal, nem em um modelo menor, nem em pares de outro conjunto;
- Um ganho que apareceu em 5 sementes sumiu em 10 novas. O mesmo treino rodado duas vezes já varia mais do que esse
  ganho, então passei a escrever o critério antes de rodar cada teste;
- O que funcionou: o modelo pequeno aprende a apontar, em pares que nunca viu, as palavras que o LLM usa para
  justificar, melhor do que regras simples de palavras (0,73 contra 0,56), e sem custo a mais na inferência.

**O que Mudou em Relacao ao Agrawal**, **Replicacao do Agrawal no RTE**, **Marcas de Atencao e Destaque**,
**Criterios Escritos Antes dos Testes** & **Exemplos do Destaque**.

**Planejamento:**

- Testar o destaque em uma tarefa de texto mais longo, onde apontar a evidência tem uso;
- Comparar a justificativa com a destilação comum, como referência do que um modelo pequeno recupera.

---

## Documentos a linkar

| No termo | Arquivo |
|---|---|
| O que Mudou em Relacao ao Agrawal | `entrega/O que Mudou em Relacao ao Agrawal.docx` (fonte: `entrega/o-que-mudou-em-relacao-ao-agrawal.md`) |
| Replicacao do Agrawal no RTE | `entrega/Replicacao do Agrawal no RTE.docx` (fonte: `entrega/replicacao-do-agrawal-no-rte.md`) |
| Marcas de Atencao e Destaque | `entrega/Marcas de Atencao e Destaque.docx` (fonte: `entrega/marcas-de-atencao-e-destaque.md`) |
| Criterios Escritos Antes dos Testes | `entrega/Criterios Escritos Antes dos Testes.docx` (fonte: `entrega/criterios-escritos-antes-dos-testes.md`) |
| Exemplos do Destaque | `entrega/Exemplos do Destaque.docx` (gerado por `resultados/rte-pequenos/docx_destaque.py`) |

---

## Escolhas abertas (só o Pedro decide)

1. **Quais documentos entram.** Os cinco da tabela existem (11/11): três curtos e dois relatórios. Corte os que não
   quiser linkar. O código do treino explicado (`docs/2026-11-09-codigo-treino-rte.md`) ficou de fora.
2. **Você não leu os resultados.** Os cinco documentos saem das leituras escritas pelo Claude; o relatório da replicação foi redigido por um agente e
   conferido pelo Claude. Pela regra do projeto,
   nada entra em texto assinado por você sem leitura sua: precisa ler cada um antes de linkar. O relatório da replicação diz "Eu não li o lote" das justificativas do RTE:
   se você leu, a frase muda.
3. **Hardware e LLM (item acrescentado a seu pedido em 11/11).** O primeiro item traz a placa-mãe, o computador do
   amigo por SSH, o atraso e o auxílio pesado de LLM. Você disse "algumas coisas"; escrevi quais (o código dos
   treinos, as rodadas e a leitura dos resultados), porque é o que os documentos linkados declaram. Os registros do
   projeto falam em perda do slot NVMe e chamam a máquina de "o PC": confira que o item está como você quer assinar.
4. **Planejamento.** Os dois itens são ideias anotadas em `docs/ideias-de-desenho.md`, nenhuma decidida. Você disse
   que as tarefas "vão entrar depois do gate" e achou a destilação comum "muito óbvia". Troque pelo que for decidir
   com o professor.
5. **Saíram sem comentário** dois itens do Planejamento da Semana 8: juntar as respostas da avaliação humana (a
   planilha do Forms não foi exportada) e marcar os pares em que o modelo discorda do rótulo. O terceiro (definir
   encoder, decoder e as primeiras versões do treino) está entregue no primeiro item.
6. **Números no texto.** Deixei quatro: 0,4754 e 0,767 (são o achado da replicação) e 0,73 contra 0,56 (o destaque).
   O "0,73" é a precisão média com 2.000 pares de treino; se preferir sem número, a frase aguenta.
7. **"Semana 9"** cobre de 29/10 a 11/11 (o handoff de 08/11 diz que ela dura duas semanas). Confirme o número.
8. **O T5 como encoder, o e-SNLI com 4 mil pares, o BERT tiny e a cabeça por token** ficaram fora do termo; entram
   nos documentos.
