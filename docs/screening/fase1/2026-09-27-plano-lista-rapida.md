# Plano: lista de alta qualidade, rápida, com os surveys como júri (27/09)

**Status: plano. Nada rodou.** Pedido do Pedro (27/09): *"a gente tinha escolhido surveys pq o objetivo era, no final,
fazer um bottom-up, mas não temos mais tempo pra isso, precisamos de uma lista de muita qualidade o mais rápido
possível."*

## 1. A ideia

Os surveys deixam de ser o produto e viram o **júri**. Quem escreve survey é especialista, e o que **muitos surveys
citam em comum** é o consenso da área sobre o que importa. O método já foi testado em 24/09, na lista de
destilação: com 88 surveys votando, a linhagem inteira apareceu sozinha (Buciluă, Hinton, FitNets, DistilBERT, DSbS),
em minutos, sem agentes. Aqui ele se generaliza para a área toda.

## 2. Números de partida (medidos em 27/09)

| Item | Número |
|---|---|
| Jurados validados: 57 surveys do gabarito + 55 relevantes da F2 | **112** |
| … com lista de referências | **91** (73 pelo S2, 18 pelo OpenAlex) |
| Anos dos jurados | 2020: 13 · 2021: 9 · 2022: 6 · 2023: 14 · 2024: 27 · 2025: 30 · 2026: 13 |
| Reserva: surveys ligados na F1, ainda não julgados, com referências no S2 | 1.702 |

## 3. Composição proposta da lista (~50; decisão do Pedro)

| Bloco | Obras | Como sai | Responde a |
|---|---|---|---|
| **A. Mapas** (surveys de entrada) | ~10–12 | 1–2 por subárea: o jurado **mais citado pelos outros jurados**, mais 1 de 2025–26 por subárea, que ainda não teve tempo de ser citado | P1 mapa, V vocabulário, A atualidade |
| **B. Fundadores** (seminais) | ~20–25 | obras citadas por muitos jurados, com cota **por subárea** e **por época** (até 2017 · 2018–21 · 2022+), cortando os genéricos por especificidade, como na lista de destilação | P3/P6 história, P2 conteúdo |
| **C. Conceitos pré-requisito** | ~5–8 | os **genéricos** mais citados por todos (Attention, BERT, GPT-3, T5…): a poda de especificidade os separa em vez de jogar fora | Q4 conceitos, R arquitetura |
| **D. Sistemas e ferramentas** | ~5–8 | papers de sistema citados pelos jurados (a F1 já mostrou um núcleo de serving: Orca, PagedAttention, SGLang) | P4a como fazer |

**Subáreas:** os grupos do pool de termos (compressão, inferência/serving, adaptação, edge, hardware, dado/confiança). É
**de cima para baixo e provisório**: a troca que o prazo impõe. O mapa por divisões declaradas pelos surveys fica para
depois.

## 4. Contrato de funil

| Campo | Valor |
|---|---|
| Entrada | 91 jurados com referências (+ reserva, se uma subárea ficar fina) |
| Saída prevista | ~50 obras em 4 blocos, cada uma com votos, subárea, época e o motivo de estar ali |
| Conta | na destilação, 88 jurados deram 45 obras com 10 ou mais votos; para a área toda, com 91 jurados, espera-se algumas centenas de candidatas, e as cotas por subárea e época cortam para ~50 |
| Custo | **0 token de agente**; metadado das candidatas pelo S2 (grátis); cerca de 1–2 horas de script + leitura dos abstracts pelo Claude |
| Sucesso | toda subárea com >= 1 mapa e >= 2 fundadores; toda pergunta (P1–R) coberta por >= 1 obra; você aprova >= 80% da lista na primeira passada |
| Parada | subárea com menos de 5 jurados que a citam: é sinal de júri fino (o hardware tende a ser). Aí a reserva entra só para essa subárea, com os surveys de maior nota de tópico do classificador, e isso é marcado na lista |

## 5. Controle de qualidade

1. **Leitura do Claude** do título e do abstract de cada obra da lista (nível 3): marca as que parecerem fora do
   escopo (§1.2, §1.3) ou duplicadas.
2. **Matriz de cobertura:** linhas = obras, colunas = perguntas P1–R. Pergunta sem obra aparece na hora.
3. **Consistência:** a sub-lista de destilação tem de bater com a de 24/09; se divergir, o relatório explica.
4. **Sua revisão final**, por título, com o motivo de cada obra ao lado. Você decide.

## 6. O que fica em pausa (sem apagar nada)

A continuação da F2, o classificador como motor de triagem, o método por camadas e a extração de taxonomias para um
mapa de baixo para cima. Os critérios P1–R **continuam**, agora como checklist da lista final (a matriz de §5).

## 7. Limites declarados

- **Consenso favorece o centro:** o gabarito está concentrado em compressão e serving (21 de 28 no grupo 2). A cota por
  subárea corrige parte disso.
- **Citação favorece o antigo:** a cota por época e o mapa de 2025–26 por subárea corrigem parte disso.
- **Subáreas de cima para baixo:** podem esconder uma divisão que os surveys declaram e o pool não nomeia.
- **Os 21 jurados sem referências não votam:** a maioria é de editora fechada.

## 8. Decisões do Pedro

1. Seguir com o **júri de surveys + contagem de citações comuns**?
2. A composição **A/B/C/D** e a divisão de ~50 servem?
3. Aceitar **subáreas de cima para baixo** (pool), abrindo mão do mapa de baixo para cima por enquanto?
4. Usar a **reserva** (surveys de maior nota de tópico) só onde o júri for fino?
