# Termo de Aceite de Entrega — Semana 8

- **Data da Reunião ("Gate") de aprovação:** `[preencher]`
- **Participante:** Pedro Mundel — `[matrícula]`

---

**Resumo das Semanas 1 a 7:**

Defini o tema, destilação de racionalização de LLM para encoders, dentro da área em que quero me especializar,
eficiência de modelos para implantação. Fiz o screening da área até chegar a uma lista de obras atuais e a um
método de leitura. Na sexta semana escolhi a tarefa, inferência textual no e-SNLI, e comparei as justificativas humanas
com as de LLM. Na sétima, passei a gerar as justificativas com um modelo aberto rodando no meu notebook, o Qwen,
porque a política de uso da Anthropic não permite treinar modelos com as saídas do Claude sem autorização. Testei
versões do prompt nos mesmos pares e vi que a forma da justificativa vem do pedido e dos exemplos, e não das
definições dos rótulos, então escrevi os 12 exemplos que definem o tom do dataset. Encontrei o eco: em cerca de 8,5%
do e-SNLI a hipótese é um pedaço da premissa, e a justificativa só consegue repetir. Fechei também por que o decoder
auxiliar é descartado na entrega, já que a justificativa é sinal de treino e não saída, e deixei um modelo maior, o
Qwen3.6-35B-A3B, como reserva, por raciocinar melhor nos casos difíceis.

**O que fiz nessa oitava Semana:**

- Troquei o pedido ao modelo: ao invés de pedir para ele explicar por que o rótulo está certo, o par vira uma
  pergunta ("por quê") sobre a cena, sem rótulo e sem as palavras premissa e hipótese. Com isso, o modelo parou de só
  reproduzir o texto ("a premissa não informa...") e passou a trazer conhecimento de mundo ("mulheres tocam muitos
  gêneros além de country"); **Geracao do Primeiro Lote**
- Medi quantos pares o gerador produz mandando vários pedidos ao mesmo tempo e escolhi o Qwen3.6-35B-A3B, mesmo
  sendo cerca de 6 vezes mais lento, porque erra menos nos casos difíceis; **Geracao do Primeiro Lote**
- Gerei o primeiro lote do dataset: 16 mil pares do treino do e-SNLI em uma noite (5h20), todos completos e com
  cerca de 22 palavras. Gerei em ordem aleatória para que qualquer começo do arquivo sirva de amostra, o que me
  deixa testar o treino com quantidades diferentes de dados sem gerar de novo;
- Marquei os pares que só repetem a hipótese, cerca de 8%. Resolvi manter assim, para testar se a cabeça auxiliar
  aprende algo nesses pares; **Geracao do Primeiro Lote**
- Montei a avaliação humana das justificativas com a rubrica de Wiegreffe et al. (2022), feita para justificativas
  de LLM no SNLI: traz informação nova, sustenta o rótulo, quantidade de informação e se é aceitável. Junto com as
  do meu lote, entraram justificativas que os avaliadores do paper já julgaram, o que permite comparar o meu
  julgamento com o deles. A avaliação vai ser feita por mais pessoas, e ainda não há resultado porque nem todos
  responderam;
- Estudei se as palavras que só aparecem com um rótulo, como "mutually exclusive" e "cannot" na contradição, podem
  atrapalhar o aluno, porque repetem o rótulo em vez de explicar o par. A partir da atribuição por palavra de Wadhwa
  et al. (2024), a ideia é medir no treino quanto do gradiente da cabeça auxiliar cai nessas palavras e tirá-las da
  perda se o peso for alto;
- O código e as rodadas foram feitos com apoio de LLM. A escolha do modelo, do tamanho do lote e da forma de
  avaliar são minhas.

**Planejamento:**

Fechar a avaliação do dataset e o desenho do primeiro treino para:

- Juntar as respostas e medir quantas justificativas do lote são aceitáveis;
- Medir quanto os avaliadores concordam entre si e com os do paper;
- Marcar os pares em que o modelo discorda do rótulo do e-SNLI;
- Definir o encoder, como a cabeça auxiliar recebe a justificativa e os braços de controle, a partir do resultado
  da avaliação.

---

## Documentos a linkar

| No termo | Arquivo |
|---|---|
| Geracao do Primeiro Lote | `entrega/Geracao do Primeiro Lote.docx` (fonte: `entrega/geracao-primeiro-lote.md`) |

---

## Escolhas abertas (só o Pedro decide)

1. **Documento linkado.** `Geracao do Primeiro Lote` cobre o pedido em pergunta (prompts das versões E e F,
   resultado nos 45 pares e exemplos), a velocidade (tabelas por número de pedidos), o lote e a marca de eco
   (regra, conferência no dev, tabelas e exemplos). A avaliação humana não tem documento; se quiser, entra como
   seção nova quando houver resultado.
2. **Wiegreffe et al. (2022) você não leu.** Pela regra do projeto, para citar no termo precisa ler pelo menos o
   §2.3 e o Apêndice B.3 (a parte da rubrica). Se não der tempo, troque por "com uma rubrica publicada para
   justificativas de LLM no SNLI" e cite na arguição só se perguntarem.
3. **"Erra menos nos casos difíceis"** vem da minha leitura de 90 pares (uns 3 a 4 erros do 35B contra uns 10 do
   9B), não da sua. Se perguntarem o número, diga que foi a leitura de apoio e que a avaliação humana é a que vai
   medir.
4. **O PC.** Se quiser explicar a semana mais enxuta, cabe uma linha de fato: "O PC passou a reiniciar de hora em
   hora e perdi parte da semana até achar a causa". Ficou de fora porque o termo não costuma narrar o que deu
   errado.
5. **O SCOTT (Wang et al., 2023)**, considerado e descartado como filtro de qualidade, ficou de fora: você não leu,
   e o motivo do descarte (exigiria outra passada do modelo sobre o lote) só faz sentido se perguntarem.
6. **"Mais pessoas" sem número.** Se souber quantos amigos vão responder, troque por "por N pessoas além de mim".
7. **O item das palavras de rótulo** é ideia sua (28/10), registrada em `docs/ideias-de-desenho.md`. Wadhwa et al.
   (2024) você leu na Semana 5; confira na fonte qual método de atribuição eles usam antes da arguição.
8. **"Como a cabeça auxiliar recebe a justificativa"** era do planejamento da Semana 6 e voltou para o planejamento
   desta, sem comentário. Se ele perguntar, a resposta está na conversa de 29/10 (Agrawal et al., 2025, §3 e §4.4).
