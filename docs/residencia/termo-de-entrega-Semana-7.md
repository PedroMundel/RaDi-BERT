# Termo de Aceite de Entrega — Semana 7

- **Data da Reunião ("Gate") de aprovação:** `[preencher]`
- **Participante:** Pedro Mundel — `[matrícula]`

---

**Resumo das Semanas 1 a 6:**

Defini o tema, destilação de racionalização de LLM para encoders, dentro da área em que quero me especializar,
eficiência de modelos para implantação. Fiz o screening da área até chegar a uma lista de obras atuais e a um
método de leitura. Na sexta semana escolhi a tarefa, inferência textual no e-SNLI, e comparei as justificativas humanas
com as de LLM.

**O que fiz nessa sétima Semana:**

- Passei a gerar as justificativas com um modelo aberto rodando no meu notebook, o Qwen3.5-9B. Fiz isso porque a
  política de uso da Anthropic não permite treinar modelos com as saídas do Claude sem autorização. A geração custa
  zero e leva menos de 1 segundo por par;
- Encontrei problemas também nas justificativas de LLM, como verbosidade e frases que só repetem o molde. Testei
  sete versões do prompt nos mesmos 45 pares e descobri que quem decide a forma da justificativa são o pedido e os
  exemplos, não as definições dos rótulos. A versão com os meus exemplos trouxe o conhecimento que liga a premissa à
  hipótese, com cerca de 24 palavras: o pedido original dava 45 e o mais curto, 16;
- Escrevi os 12 exemplos que definem o tom do dataset, com uma regra por rótulo:
  - implicação: cobrir o que a hipótese acrescenta;
  - neutro: dar uma alternativa que a premissa permite;
  - contradição: o choque de lugar e ação no mesmo momento.

  Parti de rascunhos gerados por LLM, e a revisão e a versão final são minhas **Exemplos da Justificativa**;
- Fechei por que o decoder auxiliar é descartado na entrega, e não usado para gerar justificativas: ela é sinal de
  treino, não saída. É assim no Distilling Step-by-Step (Hsieh et al., 2023) e no Agrawal et al. (2025), e gerar
  texto custaria uma passada do decoder por token na hora de responder;
- Estudei como a justificativa ensina o aluno e vi que só a parte que não repete o rótulo traz sinal novo. Por isso,
  a checagem que importa deixou de ser "cita o rótulo?" e passou a ser "acrescenta informação sobre o par?";
- Descobri que parte das justificativas é eco: quando a hipótese é um pedaço da premissa, não há o que explicar além
  de repetir. Isso vale para cerca de 8,5% do e-SNLI e nenhuma versão do prompt removeu. Isso permite marcar esses
  pares e testar se a cabeça auxiliar aprende algo neles;
- Testei um modelo maior, o Qwen3.6-35B-A3B: a forma ficou igual e o raciocínio melhorou nos casos difíceis, mas é
  3,7 vezes mais lento. Ficou como reserva;
- O código e as rodadas foram feitos com apoio de LLM. A escolha das versões e os exemplos finais são meus
  **Geracao com Modelo Local**.

**Planejamento:**

Fechar a geração do dataset para:

- Medir quantos pares o gerador produz por hora e decidir quantos gerar;
- Gerar um primeiro lote do treino do e-SNLI com a versão final do prompt;
- Marcar nesse lote os pares de eco e os rótulos com que o modelo discorda.

---

## Documentos a linkar

| No termo | Arquivo |
|---|---|
| Exemplos da Justificativa | `entrega/Exemplos da Justificativa.docx` (fonte: `entrega/exemplos-da-justificativa.md`) |
| Geracao com Modelo Local | `entrega/Geracao com Modelo Local.docx` (fonte: `entrega/geracao-modelo-local.md`) |

---

## Escolhas abertas (só o Pedro decide)

1. **Os documentos linkados.** Nenhum .docx novo existe em `entrega/` nesta semana. Gero os dois a partir das fontes
   acima, ou você linka o `candidatos-exemplos.md` que já editou? O relatório tem tudo, mas é de trabalho: tem
   números de par e leitura minha marcada.
2. **A troca do Claude pelo Qwen.** Escrevi como decisão com motivo, não como mudança de plano. Se preferir não citar
   a Anthropic, a primeira linha pode ficar só com "modelo aberto, rodando local, custo zero".
3. **"Sete versões do prompt."** Foram A, B, D, E, E2, E3 e E4 no 9B. Se quiser contar só as que você leu, ajuste o
   número.
4. **"Escrevi os 12 exemplos."** Sete ficaram iguais ao rascunho do LLM, aprovados por você, e cinco (5, 9, 10, 11 e
   12) foram reescritos na nossa discussão. Se "escrevi" soar forte, troque por "revisei e reescrevi".
5. **O item do estudo das perdas** vem da conversa sobre I(R; X | Y). Só entra se você souber explicar na arguição.
   O doc é `docs/2026-10-20-perdas-o-que-e-I-gradiente.md`.
6. **"8,5% do e-SNLI"** é uma contagem lexical no dev (implicação sem nenhuma palavra nova na hipótese). O teto é
   21,6%. A literatura confirma o fenômeno: Camburu et al. (2018) dizem que os anotadores "just repeat" nesses pares.
   Essa fonte você não leu, então não entra no termo como lida.
7. **"Raciocínio melhorou nos casos difíceis"** são 2 casos em 45. Na arguição, diga que é preliminar.
8. **Ficaram de fora:**
   - a pesquisa de vagas (destilação aparece dentro de "compressão e otimização de inferência"), que serve à pergunta
     "você vai ser o quê?". Cabe uma linha se você quiser;
   - a pesquisa sobre como mitigar o eco, que é nível 3;
   - o protocolo de 4 rodadas contra prompt ruim e o e-mail ao suporte da Anthropic (19/10). Os dois perderam peso
     com o professor local;
   - o rótulo ruidoso: no #9 o rótulo-ouro está errado, e a regra é marcar a discordância do professor numa coluna,
     não apagar. O número "58% unânimes" do SNLI veio de leitura de agente, não sua;
   - o esqueleto de framework para a geração (Long et al., 2024, em `docs/2026-10-20-frameworks-geracao.md`). Você leu
     por resumo, então, se entrar, entra como "lido por resumo".
9. **O item do decoder** só usa obras que você leu (DSbS e Agrawal). A medida de latência que provaria o custo não
   foi feita. Se perguntarem, ela está no plano.
