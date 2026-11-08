# O método reconstruído de baixo para cima: dos critérios à regressão (27/09)

**Status: camada 1 em proposta para a correção do Pedro; camadas 2 a 5 esboçadas. Nada rodou.**
Pedido do Pedro (27/09): *"podemos ir fazendo o bottom-up do método que está sendo construído até chegar de volta
na regressão"*. Cada camada só é construída quando a de baixo estiver fechada. Toda camada que roda tem **contrato de
funil** (entrada, saída prevista com a conta, custo, sucesso, parada; regra de 27/09).

**De onde vem cada peça:** perguntas do Pedro (27/09, P1–P6), perguntas do professor (vocabulário e "atualmente",
15/09 e 22/09), meta do Pedro de 15/09 (arquitetura), regra de saturação do método (acréscimo), critérios de
pertencimento já decididos (§1.2, §1.2.1, §1.3, §3.4). A base na literatura está em `docs/criterios-de-relevancia.md`.

## Visão geral: as camadas

```
Camada 5  REGRESSÃO (classificador) ....... ordena o pool pelo nível A; aprendizado ativo por cota
   ^
Camada 4  RÓTULOS ......................... nível A + nível B para as obras já lidas e as novas
   ^
Camada 3  INSTRUMENTO ..................... roteiros dos agentes que respondem as perguntas, com frase transcrita
   ^
Camada 2  PILOTO .......................... Pedro e agente nas mesmas 30 obras; Kappa por pergunta
   ^
Camada 1  CRITÉRIOS ....................... o que é relevante: nível A (tópico) + nível B (perguntas)
```

Acima da camada 5 ficam a seleção final de ~50 (C3, pela cobertura) e a bola de neve (seminais e ferramentas). Elas
entram depois; este documento termina na regressão, como pedido.

---

## Camada 1 — Critérios (PROPOSTA: cada linha "conta como sim" é para você corrigir)

### 1.1 Nível A — tópico: a obra pertence à área? (já decidido; não muda)

§1.2 (reduz custo de implantação: inferência, memória/hardware, dado rotulado) · §1.2.1 (casos a–e para survey) ·
§1.3 (transformers e a base deles) · §3.4 (não é survey: fica no bruto; primário volta como seminal; sistema vai
para ferramentas). **É porta:** só a obra que passa no nível A é avaliada no nível B.

### 1.2 Nível B — situacional: para que a obra serve?

| Código | Pergunta | Conta como **sim** se… | Não conta se… | Evidência que o agente transcreve | Onde se responde |
|---|---|---|---|---|---|
| **P1** | Mapa: me mostra como a área (ou uma divisão) se organiza? | a obra **organiza** trabalhos em categorias explícitas: taxonomia, classificação, tabela ou figura de categorias, ou declara que categoriza ("we categorize", "taxonomy", "we classify") | só lista trabalhos, um após o outro, sem agrupar; ou propõe método próprio | a frase que declara a organização | abstract (quase sempre declara); confirmação no sumário |
| **P2** | Conteúdo: me ensina como as coisas funcionam? | explica **mecanismo ou princípio** (como a técnica age, por que funciona), por exemplo com seção de fundamentos, *background* ou *preliminaries* | só cita e compara resultados | a frase que promete explicar, ou o título da seção | sumário (abstract às vezes) |
| **P3** | Conta a história: narra como a área ou divisão nasceu e evoluiu? | narra **evolução no tempo**: origem, marcos, "from X to Y", linha do tempo, gerações de técnicas | só menciona datas de passagem | a frase da evolução | abstract ou introdução |
| **P4a** | Como fazer, na área: me ensina a executar algo da implantação? | traz **prática**: ferramentas ou frameworks nomeados, benchmark reproduzível, guia, tutorial, estudo de caso de implantação, código, "lessons learned", em **qualquer** divisão | só discute em teoria | a frase com o sinal prático | abstract (piso) + corpo |
| **P4b** | Como fazer, na trilha: o mesmo, para **destilação** | como P4a, restrito a destilação de conhecimento (professor-aluno, racionalização, destilação de LLM) | como P4a | idem | idem |
| **V** | Vocabulário (professor): me dá os nomes da área? | **define** termos: glossário, tabela de siglas ou notação, definições explícitas ("we define", "terminology") | usa os termos sem definir | a frase ou o título da seção | corpo (o abstract quase nunca mostra) |
| **A** | Atualidade (professor, "atualmente"): mostra a área como é hoje? | **ver decisão D-A abaixo**; proposta: cobre a era LLM (trata de LLM, ou de transformer grande, ou de trabalhos de 2023 em diante) | cobre só técnicas anteriores à virada de 2022–23 | a frase que situa a cobertura, ou o ano | metadado + abstract |
| **R** | Arquitetura (sua meta de 15/09): me ensina como a família de arquitetura muda o problema? | discute como **encoder-only, decoder-only ou encoder-decoder** (ou transformer × outras) mudam a técnica ou a implantação; por exemplo, KV cache é coisa de decoder | trata "o modelo" sem distinguir família | a frase que distingue | corpo; abstract às vezes |

**Fora da triagem por obra:**

| Código | O quê | Por onde entra |
|---|---|---|
| **P6** | É seminal: é o trabalho que abriu a divisão | não se lê: sai das referências (§4: citado por >= 2 surveys da divisão) na bola de neve |
| **C** | Acréscimo: o que ela traz que as já escolhidas não trazem | é regra sobre o **conjunto**, aplicada na seleção final (C3): uma obra entra se preenche uma célula (pergunta × divisão) ainda com menos de N obras, ou traz divisão, termo ou ferramenta nova |
| **P5** | Como pensar | nas suas notas de leitura, com o saber ser (decisão de 27/09) |

### 1.3 Como os dois níveis se juntam

- **Nível A é porta; nível B é valor.** Uma obra do nível A que não responde nenhuma pergunta do B continua
  relevante por tópico, mas não ajuda a base; fica ordenada no bruto.
- **As perguntas não se somam em nota única.** O que importa é a **cobertura**: cada divisão precisa de obras que
  respondam P1, P2, P3, P4a, V, A e R. Isso une este critério ao "cobertura por subárea" do relatório de riscos (R-D1).
- **Previsão do tamanho final (contrato da C3, conta a conferir):** 7 perguntas respondíveis por survey × N = 2
  obras por célula = 14 "vagas" por divisão. Se um survey bom responde ~4 perguntas, bastam ~3–4 por divisão. Com
  10–15 divisões (estimativa; o mapa ainda não existe), dá **~35 a 55 obras**. É a primeira conta que fecha perto do
  alvo de ~50.

### 1.4 Decisões do Pedro (camada 1)

- **D-1.** Corrigir as linhas "conta como sim / não conta" da tabela 1.2, uma por uma.
- **D-A. Atualidade:** em 22/09 você confirmou "atualmente = janela 2020+ para o mapa". Como a floresta já é 2020+,
  a pergunta A seria "sim" para quase tudo. Proposta: **A = cobre a era LLM** (virada de 2022–23). Aceita, ou fica 2020+?
- **D-N.** Quantas obras por célula (pergunta × divisão): **N = 2** (proposta)?

---

## Camada 2 — Piloto de confiabilidade (esboço; roda depois da camada 1 fechada)

- **O quê:** você e a cadeia de agentes respondem o nível A e o nível B para as **mesmas 30 obras** de
  `F2/auditoria.md` (já sorteadas, com abstract; para P2, V e R você olha também o sumário).
- **Medida:** Kappa de Cohen **por pergunta**, entre você e o agente (Kitchenham & Charters §6.2.3, versão para
  pesquisador único). Pergunta com Kappa baixo tem critério ambíguo: reescreve-se a linha na camada 1 e pilota-se de
  novo, só aquela pergunta.
- **Contrato:** entram 30 obras · sai um Kappa por pergunta · custo: ~1 a 2 horas suas + ~0,3 M tokens do agente ·
  sucesso (proposta): Kappa >= 0,6 em cada pergunta usada na triagem · parada: pergunta que não passar em duas
  rodadas sai da triagem por agente e vai para leitura humana.
- **Efeito colateral útil:** o seu nível A nas 30 é a auditoria que já estava pedida (D2), e mede a taxa de erro dos
  rótulos da F2 (risco R3).

## Camada 3 — Instrumento (esboço)

- **Agente 2 v3:** passa a transcrever frases **por pergunta** (P1, P2, P3, P4a/b, V, A, R), além das atuais.
- **Agente 3 v2:** mantém o veredito do nível A e acrescenta, para cada pergunta do nível B, **sim / não / não dá
  para saber pelo texto**, com a frase transcrita e o código da pergunta.
- **Onde o abstract não basta** (P2, V, R): o agente sobe um degrau na escada de §6.1 (introdução e sumário), que o
  método já prevê.
- **Calibração:** a mesma de 26/09, nas 28 de ajuste do gabarito, com a meta do nível A mantida; o nível B se calibra
  no piloto da camada 2.

## Camada 4 — Rótulos (esboço)

- **Nível A:** os 797 vereditos da F2 continuam valendo (a regra não mudou), corrigidos pelo que o piloto mostrar.
- **Nível B:** só para as obras que passaram no nível A. Hoje são 55 relevantes + 157 dúvidas = **212**. As frases
  que o agente 2 extraiu na F2 não cobrem as perguntas novas, então é preciso reextrair.
- **Contrato:** entram 212 obras · saem 212 × 8 respostas · custo ~1,6 M tokens (7,6 mil por obra, medido na F2) ·
  sucesso: nenhuma obra sem resposta nem `sem acesso` escondido · parada: checkpoint em ESTADO.md, lotes idempotentes.

## Camada 5 — Regressão (volta ao classificador)

- **O que o classificador aprende:** o **nível A** (pertence à área), como antes. O nível B depende de ler o texto e
  fica com os agentes; o classificador só decide **em que ordem** os agentes leem.
- **O que muda por causa das camadas de baixo:**
  1. a leitura por ordem de nota vira leitura por **cota de cobertura**: em cada rodada de aprendizado ativo, os
     agentes leem o topo de cada subárea que ainda tem célula vazia (camada 1, §1.3);
  2. cada obra lida recebe nível A **e** nível B, e a rodada seguinte já sabe quais células encheram;
  3. a parada deixa de ser "achar 95% das relevantes" e passa a ser "**todas as células com N obras**, mais a
     amostra de controle abaixo do corte sem relevantes" (R-D1, R11).
- As correções medidas no relatório de riscos (peso por inclusão, validação agrupada, penalidade para obra sem
  palavra de tipo, fila de obras sem abstract) entram aqui. As decisões R-D1 a R-D5 continuam abertas e são
  decididas quando esta camada for construída.

---

## Próximo passo

Fechar a **camada 1** (D-1, D-A, D-N). Com ela fechada, o piloto da camada 2 é a primeira coisa que roda.
