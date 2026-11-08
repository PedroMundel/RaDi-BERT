# Guia detalhado do método de leitura (30/09)

Complemento de `docs/metodo-de-leitura.md`: **como fazer cada parte**, passo a passo. Os exemplos usam o **Distilling
Step-by-Step** (Hsieh et al. 2023), que você já leu, para você conferir cada exemplo com o que lembra. Os fatos dos
exemplos vêm de `docs/artigos/notas-distilling-step-by-step.md` (nível 1 seu e nível 2 do Claude). Onde a página
exata não está nas notas, o exemplo cita a **seção** (§).

---

## 0. Antes de abrir o PDF (2 minutos)

1. Copie `docs/leituras/modelo-ficha.md` para `docs/leituras/fichas/<ano>-<primeiro-autor>.md` (ex.: `2023-hsieh.md`).
2. Preencha a linha de procedência: data, link do arXiv.
3. Deixe abertos, lado a lado: o PDF, a sua ficha e o `glossario.md`. Você vai escrever **durante** a leitura, não
   depois.
4. **Não leia a ficha do agente** (regra 6): ela vem só no fim.
5. Ligue um cronômetro: 10 minutos para a passada 1.

---

## 1. Passada 1: reconhecimento (5 a 10 minutos)

### 1.1 O que ler, na ordem, e o que procurar em cada parte

| Parte | Como ler | O que você procura |
|---|---|---|
| **Título** | uma vez, devagar | a promessa: que coisa a obra diz que faz |
| **Abstract** | inteiro, com atenção | o problema, a solução e o número principal. Quase todo abstract segue essa ordem |
| **Introdução** | inteira | o **último parágrafo** costuma listar as contribuições ("our contributions are…"); o primeiro e o segundo dizem de onde vem o problema |
| **Títulos das seções e subseções** | só os títulos, sem o texto | o esqueleto da obra; num survey, os títulos **são** a taxonomia |
| **Figuras e tabelas** | de relance: a Figura 1 e a tabela principal | a Figura 1 costuma resumir a ideia inteira; a tabela principal mostra contra quem a obra se compara |
| **Conclusão** | inteira | o que os autores acham que provaram e o que ficou faltando |
| **Referências** | de relance | nomes que se repetem e obras que você já conhece |

### 1.2 Como responder às cinco perguntas

**Pergunta 1, Tipo.** Use esta regra de decisão:
- **mapa:** o título ou o abstract tem *survey*, *review*, *overview* ou *tutorial*, e as seções organizam trabalhos
  dos outros;
- **fundador:** propõe um método que outros depois adotaram (é citado como "a origem de…"), e as seções são método →
  experimentos;
- **conceito:** propõe uma arquitetura ou ideia que os outros **assumem** sem explicar (Transformer, BERT);
- **sistema:** propõe e **libera** uma ferramenta, biblioteca ou motor (a palavra *system*, *framework*, *engine* ou
  *library* no título, e um link para o código).

> **Exemplo (DSbS):** **fundador**. Propõe um método (treinar o aluno com rótulo e racionalização como duas tarefas) e
> se compara com fine-tuning padrão e com destilação padrão. Também libera código, mas o centro é o método, não a
> ferramenta.

**Pergunta 2, Contexto.** Duas frases: (a) qual problema existia, nas palavras da introdução; (b) com quem a obra
conversa (os 2 ou 3 trabalhos que ela mais cita como próximos).
> **Exemplo:** (a) LLMs grandes são caros para implantar, e modelos pequenos precisam de muito dado rotulado; (b)
> conversa com PINTO (que usa um LLM no teste), Ho et al. 2022 e Magister et al. 2022.

**Pergunta 3, Contribuição.** Uma frase, **verbo + o quê + resultado**. Se não couber em uma frase, você ainda não
entendeu: volte à introdução.
> **Exemplo:** "Treina um modelo pequeno com as racionalizações de um LLM como tarefa extra, e ele supera o fine-tuning
> padrão usando menos dados."

**Pergunta 4, Lugar no mapa.** A divisão da área (destilação, quantização, poda, serving…). Se não souber ainda,
escreva "?" e deixe para a passada 2.
> **Exemplo:** destilação (mais precisamente, destilação de raciocínio de LLM para modelo pequeno).

**Pergunta 5, Decisão.** Duas respostas:
- **vale a passada 2?** Sim, se a obra está no seu top 10 ou se a passada 1 mostrou que ela preenche os campos
  obrigatórios do tipo dela;
- **o que falta saber?** Os termos do abstract e da introdução que você não conseguiria explicar. Liste-os. Se for
  um ou dois, siga. Se for muitos, anote em `fila.md` e leia o pré-requisito primeiro (Keshav: é o motivo mais comum
  de uma leitura travar).
> **Exemplo:** sim; pré-requisitos: chain-of-thought, fine-tuning de T5, o que é multi-task learning.

**Ao terminar a passada 1:** pare 1 minuto e marque, na tabela da §3 do método, **quais campos este tipo de obra
preenche**. É a sua lista de busca para a passada 2.

---

## 2. Passada 2: extração (até 1 hora)

### 2.1 Como ler

1. **Siga o esqueleto, não a ordem do PDF.** Leia primeiro as seções que preenchem os campos obrigatórios do tipo:
   - **mapa:** a figura ou tabela da taxonomia → as seções que a explicam → a conclusão. Não leia cada trabalho
     citado: leia **como o autor agrupa**;
   - **fundador:** a seção do método → a figura do método → a tabela principal → as ablações → as limitações;
   - **conceito:** a seção da arquitetura e a figura dela → o porquê das escolhas (costuma estar numa seção "why…");
   - **sistema:** o problema que o sistema resolve → a arquitetura do sistema → como usar → a comparação com
     concorrentes.
2. **Pule provas, apêndices e detalhes de hiperparâmetro.** Se uma equação aparecer, leia **a frase antes e a frase
   depois**: elas dizem o que a equação faz. Reescreva a equação em palavras na ficha.
3. **Figura antes do texto.** Olhe a figura, tente entender, e só então leia o parágrafo que a explica.
4. **Escreva enquanto lê, com a página.** Uma anotação por ideia, curta, com "(p. N)" no fim. Não deixe para depois:
   depois, a página se perde.
5. **Termo desconhecido:** se ele trava a contribuição, procure agora (no máximo 10 minutos). Se não trava, anote em
   `fila.md` e siga.

### 2.2 Como preencher cada campo

Para cada campo: **como achar**, **como escrever**, **teste de qualidade** e **erro comum**.

**Campo 1, Identificação e procedência.** Já feito no passo 0. No fim, acrescente as seções que leu de fato. Teste:
alguém consegue saber exatamente o que você leu e o que não leu?

**Campo 2, Em três frases.**
- Como escrever: frase 1 = problema; frase 2 = solução; frase 3 = **número principal + contra quem + em que condição**.
- Teste: a frase 3 tem as três partes?
- Erro comum: número sem condição.
> **Exemplo:** "…no e-SNLI, o T5 de 220M com 12,5% dos dados supera o fine-tuning padrão com 100% (Fig. 4)." O 0,1%,
> que também aparece no paper, é outra comparação (contra o PaLM com chain-of-thought, Fig. 8). As notas do projeto
> registram exatamente esse tropeço: os dois números foram confundidos no primeiro resumo.

**Campo 3, História.**
- Como achar: a introdução ("prior work has…", "recently…") e a seção de trabalhos relacionados.
- Como escrever: duas linhas. **Antes:** como se fazia, segundo os autores. **Esta obra:** o que ela abriu ou mudou.
  Depois copie a linha para `linha-do-tempo.md` com o ano.
- Teste: dá para pôr num eixo de tempo?
- Erro comum: escrever a história que você acha, e não a que o paper conta. Se o paper não conta, escreva "não conta".
> **Exemplo:** antes: destilação padrão (imitar o rótulo do professor) e trabalhos que usavam a racionalização do LLM
> **na hora de responder** (PINTO). Esta obra: usa a racionalização **só no treino**, e no teste o LLM não é mais
> necessário (§3.2).

**Campo 4, Divisões.**
- **Num mapa** é o campo mais importante. Copie a árvore da taxonomia como lista aninhada, com a página da figura.
  Depois, em `mapa-divisoes.md`, junte com as árvores dos outros mapas: ramo que aparece em dois mapas consolida; ramo
  que só um mapa declara fica marcado como **singular** (regra do nosso método, §9).
- Em outros tipos, só o lugar: divisão e sub-divisão.
- Teste: daria para desenhar a árvore numa folha?
> **Exemplo:** DSbS não é mapa, então: destilação → destilação a partir de LLM → com racionalização.

**Campo 5, Conceitos.**
- Como achar: a seção de método ou de fundamentos e a figura principal.
- Como escrever: para cada mecanismo, **o que entra, o que acontece e o que sai**, com as suas palavras. Se houver
  equação, a versão em palavras.
- **Teste de qualidade:** feche o PDF e explique o mecanismo em voz alta ou num papel. Se travar, volte ao texto.
> **Exemplo:** "O aluno recebe a mesma entrada com dois prefixos diferentes, `[label]` e `[rationale]`. Com um, aprende
> a dar a resposta; com o outro, a reproduzir a explicação do LLM. A perda total é a soma das duas (L = L_label +
> L_rationale). No teste usa-se só o prefixo `[label]` (§3.2)."

**Campo 6, Vocabulário.**
- Como achar: a primeira vez que um termo aparece em itálico, entre aspas ou definido ("we call this…"); a seção de
  fundamentos; tabelas de notação.
- Como escrever: **termo, definição em uma linha com as suas palavras, página**. Depois copie para `glossario.md`. Se o
  termo já estiver lá, só acrescente a nova fonte.
- Teste: a definição se entende sem ler o paper?
- Erro comum: copiar a frase do paper. Reescreva.
> **Exemplo:** **racionalização (rationale):** explicação em linguagem natural que um LLM gera junto com a resposta,
> dizendo por que chegou a ela.

**Campo 7, Frameworks.** Dois tipos (definição de 30/09):
- **software:** procure link de código (github), nomes de bibliotecas e a frase "we implement… using X". Escreva: nome,
  para qual **atividade** serve (treinar, servir, quantizar, compilar, rodar em borda) e página;
- **conceitual:** procure **frases que prescrevem**: "first…, then…", "if…, use…", "we recommend…", listas de passos,
  fluxogramas. Escreva a diretriz no formato "se X, faça Y" ou "primeiro A, depois B";
- Copie para `frameworks.md`, com a atividade.
- Teste: a diretriz serve para decidir algo num projeto seu? Se só classifica, é mapa, não framework.
> **Exemplo (software):** código liberado no repositório do Google Research; atividade: treinar aluno com
> racionalização.
> **Exemplo (conceitual):** "para destilar raciocínio, ponha rótulo e racionalização em **tarefas separadas** (dois
> prefixos), e não na mesma sequência de saída". A ablação da Tabela 2 (p. 9) mostra que concatenar os dois fica abaixo
> do fine-tuning padrão em ANLI e CQA.

**Campo 8, Arquitetura.**
- Como achar: a seção de experimentos (que modelos usam) e qualquer frase que compare famílias.
- Como escrever: a família usada e **o que muda com ela**, se o texto disser. Se não disser, escreva "não discute".
> **Exemplo:** professor decoder-only (PaLM 540B), aluno encoder-decoder (T5). O mecanismo depende de o aluno **gerar
> texto** (a racionalização), e é exatamente isso que o seu tema v3 questiona para encoder-only.

**Campo 9, Atualidade.**
- Como achar: as limitações, os trabalhos futuros e a conclusão.
- Como escrever: o que a obra diz que falta. Só escreva "foi superada por X" se uma fonte disser isso.
> **Exemplo:** as limitações e a discussão do paper.

**Campo 10, Pré-requisitos.** Vem da passada 1 e do que travou na 2. Copie para `fila.md` com "onde aprender" (uma obra
da lista, uma aula, um capítulo).

**Campo 11, Ligações.**
- Como achar: as referências que a introdução trata como base ("following X", "building on X") e as que aparecem em
  várias seções.
- Como escrever: até 3 referências fundadoras (vão para `fila.md`) e as obras da sua lista com que esta conversa.
> **Exemplo:** fundadoras: Hinton et al. 2015 (destilação), chain-of-thought (Wei et al. 2022). Conversa com: Hinton
> 2015 e DistilBERT (lista v2).

**Campo 12, Como pensar.** O mais pessoal. Pergunte: **o que o autor fez que eu faria diferente, ou não pensaria em
fazer?**
> **Exemplo:** "Eles levam o **custo de implantação** a sério desde a primeira página: rejeitam a alternativa que
> precisaria de um LLM no teste. O critério de projeto vem antes do método."

**Campo 13, Dúvidas.** Tudo o que ficou sem resposta. Releia antes de começar a próxima obra: muitas dúvidas se
resolvem na leitura seguinte, e isso também é ligação.

---

## 3. Passada 3: reconstrução (só quando você decidir)

**Quando fazer:** em obras da sua trilha (destilação) e em frameworks que você vai apresentar no gate.

**Três níveis, do mais barato ao mais caro:**
1. **Reconstrução de memória (30 min):** sem o PDF, escreva o método inteiro como se fosse explicar a um colega, e
   desenhe a figura principal. Depois compare com o paper: o que você esqueceu é o que não tinha entendido.
2. **Reconstrução em papel (1 a 2 h):** refaça um exemplo pequeno à mão (ex.: calcular uma perda, um roofline de um
   modelo, um passo de quantização com números).
3. **Reconstrução em código (2 a 5 h):** rode a coisa. Use o código liberado ou um exemplo mínimo.
> **Exemplo (DSbS):** nível 3 seria treinar um T5 pequeno em poucas centenas de exemplos do e-SNLI, com os dois
> prefixos, e comparar com o fine-tuning padrão. É a sua RTX 5060 trabalhando, e o começo concreto do tema v3.

Escreva na ficha o que você reconstruiu e **o que aprendeu fazendo que não tinha aprendido lendo**.

---

## 4. Depois de ler (10 a 15 minutos)

1. **Atualize os arquivos acumulados** (a ficha já tem as linhas prontas; é copiar):
   - `linha-do-tempo.md`: uma linha por marco, **ordenada por ano**;
   - `mapa-divisoes.md`: a árvore, se for mapa, ou só o lugar da obra;
   - `glossario.md`: termos novos; termo repetido só ganha a nova fonte;
   - `frameworks.md`: nome, tipo, atividade, diretriz ou função, fonte;
   - `fila.md`: pré-requisitos e fundadoras.
2. **Compare com a ficha do agente** (`docs/screening/fase1/2026-09-27-lista-v2-fichas.md`, procure pelo título). Anote no fim
   da sua ficha: onde concordam, onde discordam e quem estava certo. Isso mostra onde o agente erra e serve de resposta
   pronta para "usou IA?" no gate: você leu primeiro e usou a IA como conferência.
3. **Releia as suas dúvidas.** Alguma virou pré-requisito? Mande para `fila.md`.

---

## 5. Depois das duas primeiras obras: revisar o modelo (20 minutos)

Olhe as duas fichas e pergunte:
- algum campo ficou vazio nas duas? Ele faz sentido para o seu objetivo?
- algo que você quis anotar não tinha lugar? Crie o campo;
- algum campo pede trabalho demais pelo que entrega? Simplifique.

Mude o `modelo-ficha.md`, escreva no topo "v2, <data>: o que mudou e por quê". É o piloto que a literatura pede
(Levac 2010), e é também processo, que é o que a Residência avalia.

---

## 6. Ritmo sugerido para o top 10

- **Por obra:** passada 1 (10 min) + passada 2 (até 1 h) + atualização (15 min) ≈ **1h30**.
- **Por dia:** duas obras, ou uma obra mais a passada 3 de uma anterior.
- **Top 10:** cerca de 15 horas de leitura, em uma semana. Depois das 2 primeiras, faça a revisão do modelo (§5).
- **Para o gate:** a linha do tempo, o mapa, o glossário e os frameworks, como estiverem, **são** o material. Não
  precisa terminar as 10 para ter o que mostrar.

## 7. Checklist de uma obra

- [ ] Ficha criada, procedência preenchida
- [ ] Passada 1: cinco respostas no topo; campos do tipo marcados
- [ ] Passada 2: campos obrigatórios do tipo preenchidos, **todos com página**
- [ ] Explicou o mecanismo principal de olhos fechados
- [ ] Linha do tempo, mapa, glossário, frameworks e fila atualizados
- [ ] Comparação com a ficha do agente anotada
- [ ] Dúvidas relidas
