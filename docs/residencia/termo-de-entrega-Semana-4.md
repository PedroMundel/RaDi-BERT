# Termo de Aceite de Entrega — Semana 4

- **Data da Reunião ("Gate") de aprovação:** `[preencher]`
- **Participante:** Pedro Mundel — `[matrícula]`

---

**O que fiz nessa quarta Semana:**

- Calibrei os agentes de LLM na metade de ajuste da referência antes de usá-los, porque precisava saber se eles
  acertam antes de confiar neles: não eliminaram nenhum survey da área e acertaram 96% dos relevantes;
- Usei os agentes para ler uma amostra de 962 obras, porque queria medir quanto do que sobrou da limpeza é da área.
  Aprendi que cerca de metade é: o corte por assunto já estava feito, e o que faltava era escolher, entre milhares de
  obras da área, as que formam uma base;
- Escrevi as perguntas que uma obra precisa responder para entrar na base (se mostra o mapa da área, como ela nasceu,
  que conceitos e palavras ela ensina, que frameworks traz, se é atual), porque ser do assunto não diz se a obra
  serve para aprender a área. Para isso me apoiei em literatura sobre critérios de relevância levantada com LLM;
- Passei a usar os surveys como júri, e não como resultado: as obras que muitos surveys citam em comum formam a lista,
  porque quem escreve survey é especialista, e o que muitos deles citam é o consenso da área. Com 91 surveys votando,
  saiu uma lista de 56 obras em quatro grupos (mapas, fundadores, conceitos e sistemas), com peso extra para hardware,
  que considero parte importante da área **Selecao das Obras**;
- Pedi que agentes de LLM lessem as 56 obras e escrevessem uma ficha de cada uma, porque eu preciso saber o que cada
  obra traz antes de decidir a ordem de leitura. Com as fichas, escolhi as 10 primeiras;
- Montei um método de leitura em que já sei o que extrair de cada obra (de onde veio, onde fica na área, palavras
  novas e frameworks), porque assim cada leitura alimenta direto a linha do tempo, o mapa, o glossário e a lista de
  frameworks da área **Metodo de Leitura**;
- Usei a definição de framework nos dois sentidos, ferramenta e diretriz, porque os dois apoiam a
  execução de uma atividade de implantação;
- `[preencher depois de ler]` Li Hinton et al. (2015), Yuan et al. (2024) e Kwon et al. (2023), porque juntos
  mostram a origem da destilação, um framework para decidir onde otimizar (roofline) e um framework de serving (vLLM).
  Registrei essas leituras junto com as das semanas anteriores **Obras Lidas v3**.

**Planejamento:**

Ler as 10 primeiras obras pelo método para:

- Montar a linha do tempo, o mapa de divisões e o glossário da área;
- Levantar os frameworks por atividade, como base da próxima etapa.

---

## Documentos a linkar

| No termo | Arquivo |
|---|---|
| Selecao das Obras | `entrega/Selecao das Obras.docx` (fonte: `entrega/selecao-obras.md`) |
| Metodo de Leitura | `entrega/Metodo de Leitura.docx` (fonte: `entrega/metodo-leitura.md`) |
| Obras Lidas v3 | `entrega/Obras Lidas v3.docx` (fonte: `entrega/obras-lidas-v3.md`) |
| Leituras Semana 4 (reserva) | `entrega/Leituras Semana 4.docx` (fonte: `entrega/leituras-semana-4.md`) — extração com apoio de LLM; usar só se a sua não ficar pronta |

---

## Escolhas abertas (só o Pedro decide)

1. **O último item (as três leituras):** fica só se você tiver lido. Se ler só parte, cite só o que leu, com o ano.
   Se não der tempo, apague o item e deixe as três no Planejamento.
2. **A literatura de critérios de relevância** (JBI, Levac 2010, Saracevic 2007) foi lida pelo Claude, não por você. O
   termo diz "levantada com LLM". Se preferir, tire a frase.
3. **A leitura por amostragem (962 obras)** está como medição, sem falar que ela não reduziu a lista como o plano
   esperava. Se o professor perguntar pelo plano anterior: a amostragem mostrou que o problema não era assunto, e
   isso levou ao júri.
4. **A definição de framework:** se ela veio do professor, escreva "a definição de framework do professor" (fica mais
   forte). Eu não pus porque você não disse de onde veio.
5. **Keshav (2007) no Metodo de Leitura:** o documento diz que o método se baseia nele, e quem leu foi o Claude. São
   **3 páginas** (`docs/artigos/keshav-2007-how-to-read-a-paper.pdf`), cerca de 10 minutos. Leia, ou tire a frase do
   documento antes de entregar.
6. **Leituras Semana 4 (reserva):** extração das três obras preparada com apoio de LLM, e o documento diz isso no
   topo. Se usar a reserva, o item das leituras no termo fica assim: "Comecei a leitura de Hinton et al. (2015), Yuan et
   al. (2024) e Kwon et al. (2023), com uma extração preparada com apoio de LLM pelo meu método, que estou conferindo na
   fonte **Leituras Semana 4**". E as três saem do Obras Lidas v3 até você terminar.
