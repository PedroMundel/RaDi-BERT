# Camada A — exclusão por campo de estudo: relatório (23/09/2026)

**Status: coleta feita, critério NÃO escolhido, nada excluído.** Nível 3: os campos de estudo são
metadado atribuído pelo Semantic Scholar (em parte por um modelo automático, `s2-fos-model`), não
leitura. Bruto: `raw/2026-09-23-camadaA-campos.json` (campos das 118.659 obras).

---

## 1. O que é a camada A e por que ela existe

É o primeiro corte da limpeza A -> B -> C que você escolheu. A ideia é a mais barata e mais
tradicional de revisão sistemática: um **critério de exclusão por metadado**, declarado antes e
aplicado igual a todas as obras (Kitchenham & Charters 2007 — lido por mim, não por você). O
metadado é o **campo de estudo** que o Semantic Scholar atribui a cada paper (Computer Science,
Physics, Medicine…). Objetivo: tirar da floresta o que é de outra área — as árvores que claramente
não são cajueiro.

## 2. Um problema descoberto antes de começar

A proposta original era "excluir quem não é Ciência da Computação". Testei numa amostra de 40 obras:
**todas** tinham Ciência da Computação, porque a busca já tinha filtrado por isso. Na floresta
inteira, confirmado: **118.637 de 118.659** têm CS. Então esse critério não tira nada.

O lixo de outra área está **junto** com CS: um paper de física computacional vem marcado
"Computer Science + Physics". O critério, portanto, tem de olhar **quais outros campos** a obra tem.

## 3. Como a floresta se distribui

| campo (além de CS) | obras | % da floresta | cajuzeiros conhecidos com esse campo (metade de ajuste, 28) |
|---|---|---|---|
| Engineering | 46.208 | 38,9 | 7 |
| Medicine | 28.549 | 24,1 | **4** |
| Environmental Science | 17.296 | 14,6 | 0 |
| Education | 11.353 | 9,6 | **2** |
| Business | 8.557 | 7,2 | 0 |
| Physics | 5.334 | 4,5 | 0 |
| Linguistics | 4.663 | 3,9 | 3 |
| Psychology | 3.919 | 3,3 | 0 |
| Materials Science | 3.093 | 2,6 | 0 |
| Mathematics | 3.009 | 2,5 | **5** |
| Biology | 2.474 | 2,1 | 0 |
| Sociology · Agricultural · Economics · Political Sci. · Law · Chemistry · Art · Geography · Philosophy · Geology · History | 2.453 a 297 cada | < 2,1 cada | 0 |

Só CS, sem outro campo: 19.694 obras. Metade dos cajuzeiros conhecidos (14 de 28) é "só CS".

**Três leituras importantes:**
1. **Matemática não pode ser excluída.** Você citou química, física e matemática como lixo — mas
   5 dos 28 cajuzeiros conhecidos têm "Mathematics" (quantização e fatoração são matemática).
2. **Medicina e Educação também têm cajuzeiro** (4 e 2 de 28). O campo automático do S2 erra: um
   survey de compressão de LLM pode vir marcado "Medicine" por citar uma aplicação médica.
3. **"Zero cajuzeiros com esse campo" é evidência fraca**: são só 28 obras de amostra. Um campo com
   17 mil obras (Environmental Science) pode ter cajuzeiro que a amostra não pegou — e tem, ver §4.

## 4. O que cada critério tiraria

Para não viciar o teste, as opções abaixo mostram **só a metade de ajuste** do gabarito. A metade
de teste só é usada depois que você escolher.

**Salvaguarda pelo título** (variante de cada opção): a obra **não** é excluída se o título tiver
termo de um grupo núcleo do pool (`área`, `compressão`, `inferência/serving`, `adaptação`, `edge`).
Motivo: o campo automático erra, e o título é a evidência mais direta que temos no nível 3.

| opção | exclui obra com algum destes campos | tira | sobra | cajuzeiros de ajuste perdidos |
|---|---|---|---|---|
| **1** | Physics, Chemistry, Materials Science, Biology, Geology ("ciências duras") | 10.952 (9,2%) | 107.707 | 0/28 |
| **1 + salvaguarda** | idem, exceto se o título tiver termo núcleo | 10.630 | 108.029 | 0/28 |
| **2** | os 17 campos que tiveram 0 cajuzeiros no ajuste | 45.010 (37,9%) | 73.649 | 0/28 |
| **2 + salvaguarda** | idem, exceto se o título tiver termo núcleo | 43.868 | 74.791 | 0/28 |
| 3 | opção 2 + Medicine + Education | 74.055 (62,4%) | 44.604 | **5/28** — descartada por perder cajuzeiro |

**O que cairia sem a salvaguarda, e parecia cajueiro pelo título:**
- Opção 1: 26 obras. A maioria é lixo real — *compressão de vídeo por transformada fractal*,
  *identificação esparsa de sistemas não lineares*, *fatoração de matrizes para ômica* — mas também
  **"Sparsity in transformers: A systematic literature review"**, marcado Physics pelo S2.
- Opção 2: 128 obras. Muito lixo real — e um caso que ensina: **"LoRa" (rádio de longo alcance para
  IoT) casa com o termo "LoRA" (adaptação de baixo posto)** porque a comparação ignora maiúsculas.
  Mas também **"Data Distillation: A Survey"** (Environmental Science), que pode ser da área.

A salvaguarda existe exatamente para esses casos: mantém *Sparsity in transformers* e *Data
Distillation*, e deixa o resto sair.

## 5. Decisão sua

Escolher uma das quatro primeiras opções. Depois da escolha:
1. meço a perda na **metade de teste** (29 obras) — o número que vale;
2. sorteio uma amostra das obras excluídas para você conferir a olho;
3. cada obra ganha a coluna `camada_A` (mantida / excluída + campo que causou), e nada é apagado.

**Achado para a camada B (registrado agora):** homônimos por maiúscula — *LoRa* × *LoRA* — precisam de
casamento sensível a maiúscula nos termos-sigla.

---

## 6. Resultado — opção escolhida pelo Pedro (23/09): **2 + salvaguarda**

**Aplicada.** A coluna `camada_A` (e `campos_s2`) foi acrescentada ao `2026-09-22-floresta-obras.csv`
— nenhuma linha removida.

| | obras |
|---|---|
| excluídas | **43.868** |
| mantidas | **74.791** |
| … das quais salvas pela salvaguarda do título | 1.142 |

**Perda na metade de teste (o número que vale): 1 de 29 — recuperação 97%.**
A perdida: **"A Survey on Green Deep Learning"** — marcada *Environmental Science* pelo S2, e o título
não tem termo núcleo do pool (o pool tem `green NLP`, não "green deep learning"). É o mesmo título que
já tinha escapado do filtro de título na volta 1. Não ajustei a regra para salvá-la: ajustar depois
de ver o teste gastaria o teste (ele deixaria de medir). Rota de recuperação: bola de neve, se outros
surveys a citarem.

**Amostra de 30 excluídas, sorteada (semente 2309), para conferência a olho:** todas parecem de fora
da área — modelo de população de galáxias, energia escura, comércio social, marketing, tecnoestresse,
materiais para robótica mole, detecção de falha em linha de transmissão, doença de planta com IoT,
psicometria… Nenhuma é survey de eficiência de modelo. (Amostra completa no chat de 23/09;
reproduzível pela semente.)

**Leitura (nível 3):** a camada A tirou 37% da floresta com perda de 1 em 29 no teste. Com 29 obras,
cada perda vale ~3,4 pontos; a margem é larga.
