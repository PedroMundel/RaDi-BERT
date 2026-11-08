# Plano: do funil de ~11,5 mil obras até o registro, com classificador (27/09)

**Status: plano. Nada rodou.** Pedido do Pedro (27/09): *"preciso de todo o processo bem definido e descritivo pra
gente não passar pelo mesmo erro novamente"*. Cada decisão aberta está em §8, marcada como **decisão do Pedro**.

## 1. O erro da F2 e a regra que nasce dele

**O que aconteceu.** A F2 decidia **grupos inteiros**: um grupo só descia se a amostra tivesse **zero** relevantes.
Com relevância de 7% num grupo, a chance de 50 sorteadas não trazerem nenhuma é 0,93^50 = 2,6%. Qualquer grupo
com relevância perto de 10% passaria inteiro, quase com certeza. E o maior grupo (o 2, com 3.988 obras) **é a
própria área**: 21 das 28 obras de ajuste do gabarito estão nele. A F2 não tinha como reduzir, e isso **dava para
calcular antes de rodar** com números que já existiam (tamanho dos grupos, taxa esperada). Não calculamos.

**Regra nova: contrato de funil.** Nenhuma etapa roda sem declarar, **por escrito e antes**:

| Campo | O que é |
|---|---|
| Entrada | quantas obras entram |
| Saída prevista | quantas devem sair, **com a conta** que leva a esse número |
| Custo | tokens, tempo, e quantas janelas de limite de uso |
| Critério de sucesso | número medido que diz se a etapa funcionou, fixado antes de rodar |
| Parada | o que faz a etapa parar no meio, e o que acontece se a previsão falhar |

Se a saída prevista não aproxima o funil do alvo, a etapa **não roda**; volta para o desenho.

## 2. O funil inteiro, com números previstos

Números de hoje, medidos na F2 (nível 3, agentes):

| Etapa | Entra | Sai (previsto) | Conta |
|---|---|---|---|
| Hoje | 11.505 não lidas + 797 já lidas com acesso | — | — |
| **C1. Classificador** (§3) | 11.505 | ordem por nota (ninguém sai) | — |
| **C2. Agentes leem por ordem de nota, até a parada** (§4) | topo da ordem | **~1.300 relevantes** (+ ~1.000 dúvidas (c)) | ~1.400 estimadas × recall 95% |
| **§3.2 do método (registro)** | ~1.300 | **~1.100** | 47 de 55 relevantes da F2 passam (85%): quase todas estão em venue revisado |
| **C3. ??? — ETAPA QUE NÃO EXISTE** | ~1.100 | **~50** | **nenhum critério desenhado corta 95%** |

**A conclusão mais importante deste plano:** o classificador resolve o **custo de achar** as relevantes, mas **não
leva a ~50**. Mesmo com classificador perfeito, sobram ~1.100 surveys relevantes e com qualidade. O alvo de ~50
(⟨rev-31⟩, provisório) exige um critério que ainda não existe: a etapa C3 (§5). Ela precisa ser escolhida
**antes** de rodar a C2, porque pode mudar a ordem do funil e baratear tudo (§5.2).

Um dado muda a cara do problema: **62% das relevantes da F2 são de 2025–26** (22 de 2025 e 12 de 2026, entre 55). A
área está explodindo, e a maior parte do que existe tem menos de dois anos.

## 3. Etapa C1 — classificador de relevância

### 3.1 O quê e por quê

Um modelo simples aprende, com os vereditos dos agentes, a separar relevante de fora a partir do vetor SPECTER2 de
cada obra, e dá uma **nota** às 11.505 não lidas. Os agentes passam a ler **por ordem de nota** em vez de por sorteio.
É destilação: o julgamento caro (cadeia Haiku -> Sonnet) ensina um classificador barato.

**Custo:** zero token; minutos de CPU na sua máquina.

### 3.1.1 Como a nota é dada, passo a passo

**Passo 1: a obra vira 768 números.** O SPECTER2 lê título e abstract e devolve um vetor de 768 números. Ele foi
treinado para uma coisa só: **artigos que se citam devem ficar perto**. Por isso a posição do vetor codifica o
**assunto** da obra. Dois surveys de quantização de LLM ficam perto um do outro; um survey de segurança de IoT
fica longe dos dois, mesmo que use a palavra "lightweight". Esse passo já foi feito na camada B, em 23/09.

**Passo 2: o modelo aprende uma direção.** A regressão logística procura, nesse espaço de 768 dimensões, **uma
direção** (768 pesos, `w`) e um deslocamento (`b`). Ao longo dessa direção, as obras que os agentes chamaram de
relevantes ficam de um lado, e as de fora ficam do outro. O treino ajusta os pesos para errar o mínimo sobre os
~825 rótulos. Uma penalidade (L2) impede pesos exagerados, que decorariam os exemplos em vez de generalizar.

**Passo 3: a nota é a posição da obra nessa direção.** Para cada obra não lida:

```
z    = w1*x1 + w2*x2 + ... + w768*x768 + b      (soma ponderada dos 768 números)
nota = 1 / (1 + e^(-z))                          (espreme z entre 0 e 1)
```

Obra muito do lado das relevantes tem `z` alto e nota perto de 1; do lado das de fora, nota perto de 0.

**Como ler a nota: é uma ordem, não uma probabilidade.**
- Ela responde a uma pergunta só: **"quanto esta obra se parece, em assunto, com as que a cadeia de agentes
  chamou de relevantes?"**
- Não mede qualidade, citação nem se é survey (a menos que isso esteja no texto e tenha separado os rótulos).
- Com peso por classe, os 55 positivos pesam tanto quanto os ~740 negativos. Isso infla as notas: 0,7 **não**
  quer dizer "70% de chance". Por isso a nota só serve para **ordenar**. O corte sai da validação (K95), não de um
  valor da nota.

**O que ela herda e o que ela não sabe:**
- Herda os acertos **e os erros** dos agentes. Se o agente 3 errou sistematicamente um tipo de obra, o
  classificador aprende o mesmo erro (daí a D2).
- Não conhece as regras do método (§1.2.1, §3.4). Aprende **aproximações** delas pelo assunto: "compressão para
  YOLO" fica perto de CNN, e CNN foi rotulada fora. Uma regra que não se reflete no assunto, como "é survey ou é
  paper primário", o vetor capta mal: um survey e um paper primário sobre o mesmo tema ficam perto.
- Obra sem abstract tem vetor feito **só do título**, que é mais pobre. A nota dela é menos confiável, e o
  relatório separa esse grupo.

**Cada nota vem com justificativa.** Ao lado da nota, o arquivo traz as **3 obras rotuladas mais próximas**
(pelo cosseno entre vetores), com o veredito e o título de cada uma: "nota 0,91; parece com: *A Survey on Model
Compression for LLMs* (relevante), *Efficient Inference of Transformers* (relevante), *…* (dúvida)". Assim dá para
conferir **por que** uma obra subiu, sem precisar abrir 768 pesos. Se uma obra tem nota alta e vizinhas de fora,
é sinal de problema, e o relatório lista esses casos.

### 3.2 Dados

| Item | Origem | Número |
|---|---|---|
| Vetores | SPECTER2 base sobre título + abstract (título só, quando não há abstract), calculados na camada B em 23/09 | 74.791 × 768, `float16` |
| Rótulos | vereditos finais da F2 com acesso | 797: 55 relevante · 157 dúvida · 335 fora · 250 claramente fora |
| Rótulos extras | metade de **ajuste** do gabarito (28 surveys da área) | positivos |
| **Nunca no treino** | metade de **teste** do gabarito (29) | reservada para o teste final (§3.6) |

**Passo 0 (antes de tudo):** copiar os vetores do scratchpad temporário (`63bb19b2…/camadaB_emb_specter2.npy`, 115 MB)
para `docs/screening/fase1/emb/`. Hoje eles vivem numa pasta que o Windows pode limpar. A linha *i* do arquivo é a
*i*-ésima obra da floresta com `camada_A` começando por "mantida", na ordem do CSV; o script confere isso pela
contagem (74.791) antes de usar.

**Limite dos rótulos:** são nível 3, de agentes. A dupla leitura concordou em 87% sobre seguir ou sair; o
classificador não pode ser mais confiável que isso, e aprende também os erros dos agentes. A sua auditoria dos 30
(`F2/auditoria.md`) é o que estima a taxa de erro dos rótulos (decisão D2).

### 3.3 O alvo do classificador (decisão D1)

| Opção | Positivo = | Positivos | Efeito |
|---|---|---|---|
| **P1** | só `relevante` | 55 + 28 | alvo limpo; poucos positivos, validação ruidosa |
| **P2** | `relevante` + `dúvida` | 212 + 28 | mais positivos; puxa também aplicação específica (c), e o topo da lista fica maior |
| **P3** | dois classificadores, P1 e P2, e a ordem usa P1 | — | ordena pelo que importa e ainda mede a (c) em separado |

### 3.4 Modelo e comparação

- **Modelo:** regressão logística sobre os vetores padronizados, com peso por classe (`class_weight="balanced"`) e
  regularização escolhida por validação interna. Com 83 a 240 positivos, qualquer coisa mais complexa decora os dados.
- **Descartados, com motivo:** ajuste fino do SPECTER2 (rótulos de menos para mexer em 110 M de parâmetros); rede
  neural sobre os vetores (mesma razão). Um **kNN** entra como comparação, não como candidato.
- **Linhas de base obrigatórias** (o instrumento "baseline" do `docs/pesquisa/mapa-do-terreno.md`). O classificador só vale se
  bater todas:
  1. ordem aleatória;
  2. ordem pela F1 (ligada e sem dado primeiro, que já concentra 11% contra 0,9%);
  3. regra de palavras núcleo no título (a mesma da lista `sem acesso`);
  4. kNN sobre os mesmos vetores.

### 3.5 Validação (pré-registrada: estes números são fixados antes de treinar)

- Validação cruzada **estratificada em 5 dobras, repetida 5 vezes** (sementes 1–5), só com os rótulos da F2 e o ajuste.
- **Métrica principal: K95**, a fração da lista que é preciso ler, de cima para baixo, para achar 95% dos positivos
  de cada dobra. Projetada para as 11.505: K95 = 20% significa ler ~2.300.
- Métricas de apoio: área sob a curva precisão-recall; recall no topo de 10%, 20% e 30%.
- **Critério de sucesso (proposta, decisão D3):** K95 <= 25% **e** pelo menos 10 pontos percentuais melhor que a
  melhor linha de base. **Se falhar: parar, relatar, não rodar agentes.**

### 3.6 Teste final (uma vez só)

Depois de fixar o modelo, as 29 obras da metade de **teste** do gabarito recebem nota. Medida: quantas caem acima do
corte K. É a perda do processo inteiro (M4.4), e é usada **uma vez**. Se ficar abaixo de 90% (26/29), o relatório diz
isso antes de qualquer outra coisa.

### 3.7 Checagens de vazamento

- Nenhuma obra do teste do gabarito entre os rótulos (verificado por chave S2/arXiv/DOI).
- Nenhuma obra repetida entre as dobras.
- As obras já lidas na F2 não entram de novo na leitura da C2.

### 3.8 Saída

`docs/screening/fase1/C1/`: `notas.csv` (obra, nota, posição, grupo, situação na F1), `validacao.md` (curvas, K95 por
dobra, comparação com as linhas de base), `teste-gabarito.md`. **A tabela-mestra não é tocada** até você aprovar
(regra de 23/09).

## 4. Etapa C2 — agentes leem por ordem de nota

- Mesma cadeia calibrada (roteiros 1 v1, 2 v2, 3 v1), em lotes de 40 **na ordem da nota**.
- **Parada por rendimento (proposta, decisão D4):** a cada 200 obras lidas, conta-se a fração de relevantes nas
  últimas 200. Se cair abaixo de **2%** em duas janelas seguidas, a leitura para. O que ficar abaixo da parada
  continua no bruto (ordena, não apaga).
- **Custo previsto:** ~7,6 mil tokens por obra (medido na F2). Com K95 = 20% (~2.300 obras): **~17 milhões de
  tokens**, ou cerca de 2 a 3 janelas de limite. A parada por rendimento deve cortar parte disso.
- **Proteção contra o limite de uso** (memória de 27/09): `C2/ESTADO.md` atualizado por lote; cada lote grava a
  própria saída; o lançamento seguinte roda **só os lotes que faltam**; nada de retomar o workflow inteiro; erro de
  formato se corrige na leitura.

## 5. Etapa C3 — de ~1.100 para ~50: a etapa que falta (decisão D5)

### 5.1 Candidatos

| | Critério | O que faz | Previsão | Custo | Risco |
|---|---|---|---|---|---|
| **a** | **Centralidade na rede interna** | ordena as relevantes pelo número de **outras relevantes** que as citam (a perna (c) do §3.2, levada ao extremo); fica o topo | ~50, por construção | zero (a rede da F1 já existe) | as de 2025–26 (62%) ainda não foram citadas; precisa de exceção por ano, como na F1 |
| **b** | **N por divisão** | depois da extração (a taxonomia de cada survey), escolhem-se os N melhores surveys por divisão do mapa | ~5 × nº de divisões | a extração lê cada relevante: é o mais caro | depende do mapa, que depende da extração: circular se feito sobre as 1.100 |
| **c** | **Conjunto inicial + bola de neve** (Wohlin 2014) | um conjunto inicial pequeno e diverso (§5.3 do método) e a bola de neve só pelas referências e citações dele, até saturar | o que a saturação der | médio | é o método previsto; o conjunto inicial vira a decisão crítica |
| **d** | **Rever o alvo** | aceitar que a área tem ~1.000 surveys e trocar "~50 lidos" por "~50 lidos + o resto mapeado" | — | — | muda o critério do produto |

### 5.2 Por que a C3 precisa ser escolhida antes da C2

Se a C3 for **(a) centralidade**, ela pode rodar **antes** dos agentes. A rede e o classificador são de graça, e os
agentes leriam só as ~200 obras centrais com nota alta, em vez de ~2.300. O custo cairia de ~17 milhões para ~1,5
milhão de tokens. Se a C3 for **(b)**, a C2 inteira é necessária. **A ordem do funil depende dessa escolha.** Rodar
a C2 antes de decidir a C3 é repetir o erro da F2: gastar para descobrir depois que a etapa não aproxima do alvo.

## 6. O que este plano substitui

- **As decisões 1 e 2 do relatório da F2** (grupos 1/14 e grupo 43) perdem o objeto: o classificador dá nota a cada
  obra, e o grupo deixa de ser unidade de decisão.
- **F3 do desenho de 23/09** (keywording sobre o que sobrar da F2): não roda sobre 11,5 mil obras. O keywording pode
  voltar dentro da C3 (b), sobre as relevantes.

## 7. Ordem de execução (só depois das decisões de §8)

| Passo | O quê | Custo | Produto |
|---|---|---|---|
| 0 | Copiar os vetores para o projeto; conferir a contagem | 0 | `emb/` |
| 1 | C1: treino + validação + linhas de base | 0 token | `C1/validacao.md` |
| 2 | **Você lê a validação.** Critério D3 cumprido? | — | GO ou NO-GO |
| 3 | Teste final no gabarito (uma vez) | 0 | `C1/teste-gabarito.md` |
| 4 | C3, se for (a): rede de centralidade sobre as notas altas | 0 | ordem final |
| 5 | C2: agentes por ordem, com parada por rendimento | ~1,5 a 17 milhões de tokens | vereditos |
| 6 | Relatório descritivo + proposta de coluna na tabela-mestra | — | para a sua decisão |

## 8. Decisões do Pedro

- **D1. Alvo do classificador:** P1 (só relevante), P2 (relevante + dúvida) ou P3 (os dois; ordena por P1)?
- **D2. Auditoria antes do treino?** Os 30 vereditos em `F2/auditoria.md` estimam o erro dos rótulos. Ler antes custa
  cerca de 1 hora sua e diz se os rótulos prestam; ler depois arrisca treinar sobre rótulo ruim.
- **D3. Critério de sucesso da C1:** K95 <= 25% e 10 pontos acima da melhor linha de base, como proposto?
- **D4. Parada por rendimento da C2:** menos de 2% de relevantes em duas janelas de 200 seguidas, como proposto?
- **D5. A etapa C3:** a, b, c, d ou combinação? Ela decide a ordem do funil (§5.2).

## 9. Arquivos citados

`docs/screening/fase1/2026-09-27-F2-relatorio.md` · `F2/vereditos.csv` · `F2/auditoria.md` ·
`scripts/screening/camadaB/camadaB_topicos.py` (como os vetores foram feitos) · `docs/screening/metodo-screening-etapa1.md`
§3.2 e §5.3 · `2026-09-23-desenho-agentes.md`.
