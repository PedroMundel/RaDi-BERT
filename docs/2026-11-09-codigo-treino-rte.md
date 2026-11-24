# O código do treino do RTE, antes de existir (09/11/2026, noite)

Continua `docs/2026-11-09-treino-agrawal-rte-explicado.md`, que explica **o método** e as decisões D0–D6. Este
documento explica **o código**: que arquivos, que classes, o que cada laço faz e que testes provam que ele faz isso.
**Atualização (09/11, noite): o código foi escrito** (branch `feat/treino-rte`, sem commit) em
`src/radibert/rte_dados.py`, `rte_modelo.py`, `rte_gradientes.py`, `rte_treino.py` e `tests/test_rte_treino.py`. Os
trechos abaixo continuam sendo o esboço aprovado. **Onde o código difere do esboço:**

- **Quatro grupos, não três:** o Pedro pediu as palavras gramaticais à parte (grupo **F**, junto com pontuação e o
  `</s>`). C ficou só com palavra de conteúdo copiada do par. Os grupos são um `IntEnum` (`Group.S/F/C/N`).
- O `collate` **não** carrega os grupos: o lote de sonda monta os seus em `build_probe`. A perda do treino nunca vê
  grupo.
- A medida por grupo se chama `measure_groups`. As palavras são `Unit` (palavra, grupo, posições) montadas por
  `token_units`, e todo token do alvo pertence a exatamente uma.
- **I1 compara só o texto do par.** O `idx` do GLUE recomeça em cada split (o dev vai de 0 a 276), então coincidir
  `idx` entre treino e dev não quer dizer nada.
- O BERT é carregado **sem o pooler** (`add_pooling_layer=False`): a cabeça lê o `[CLS]` direto, e um pooler sem uso
  deixaria pesos sem gradiente na medida.
- `--fumaca` usa sondas de 8 e 4 pares; a rodada de verdade usa 64 e 128.
- O `backward` roda fora do `autocast` (recomendação do PyTorch); o bf16 só vale na passada para frente, e só em GPU.
- Depois da auditoria (code-auditor, 09/11): `resultados.csv` é gravado **por último** (é a linha que marca a rodada
  como feita); uma rodada avulsa exige `--arm`, `--warmup` e `--seed`; o commit do código é lido **antes** do treino
  (git ausente falha na hora); os gradientes da medida saem fora do `autocast`; treino e avaliação usam a mesma
  função `classify`; número de um dígito conta como palavra, não como F.
- **Segunda auditoria (09/11), só sobre o caminho da GPU, que nunca rodou:**
  - As duas medidas estourariam os 8 GB. A por grupo segurava o grafo dos 64 pares e 6 gradientes do BERT ao mesmo
    tempo (~11 GB pela conta do auditor); a por palavra segurava o grafo dos 128 pares durante o laço inteiro. Agora a
    sonda passa em **blocos de 16 pares** (`CHUNK_PAIRS`) e os gradientes são **somados em fp32 na CPU**. A soma é
    exata porque cada bloco divide pelo denominador da sonda inteira; o teste confere bloco de 2 contra sonda inteira.
  - A **cabeça roda em fp32** mesmo sob bf16: com 8 bits de mantissa, as 277 probabilidades do dev empatariam e o
    ROC-AUC ficaria grosso.
  - O `--grade` começa por uma **checagem de memória**: um passo da fase C com os 32 pares mais longos (289 tokens),
    mais uma medida por grupo, e imprime o pico. Se não couber, o erro aparece em segundos, não horas depois.
  - `append_csv` recusa linha com colunas diferentes do cabeçalho do arquivo.
  - Mesma semente reproduz os pesos **só na CPU**. Na GPU, o backward do embedding usa somas atômicas e as rodadas
    variam um pouco.
  - **A memória na 5060 continua sem medida.** O notebook (GTX 1650, 4 GB) não comporta o modelo, e o código ainda
    não está no PC. A checagem do `--grade` é a primeira medida de verdade.
- O campo do plano virou `warmup_steps`: como `warmup`, ele sobrescrevia o "prop"/"500" da rodada no CSV (achado
  pela fumaça, com teste).
- O `requirements.txt` gerado pelo `uv export` lista `torch==2.14.1+cu130`, mas não o índice do PyTorch. Quem instalar
  com `pip` precisa de `--extra-index-url https://download.pytorch.org/whl/cu130`. Com `uv sync` não há problema.

**Procedência.** As APIs foram conferidas na fonte em 09/11: `transformers` 5.20.2 (PyPI, 19/10/2026;
`modeling_t5.py` da tag v5.20.2, linhas 1009–1052), `torch` 2.14.1 (PyPI, 30/09/2026, com roda `+cu130` para Windows
e Python 3.11 no índice do PyTorch), configs no HF Hub (`google-t5/t5-base`: d_model 768, `google-bert/bert-base-uncased`:
768, `google/bert_uncased_L-2_H-128_A-2`: 128). Driver do PC: 610.88 (`nvidia-smi`, 09/11). O que vem do paper do Agrawal
cita a seção. O resto é proposta do Claude e está marcado assim.

---

## A ideia em uma imagem

```
            premissa + hipótese (tokens do BERT)
                          │
                    ┌─────▼─────┐
                    │   BERT    │  h = um vetor de 768 por token
                    └─────┬─────┘
             ┌────────────┴─────────────┐
     h do [CLS]                    h inteiro (todos os tokens)
             │                          │
     ┌───────▼──────┐          ┌────────▼─────────┐
     │ Linear 768→1 │          │ decoder do T5    │  lê h por cross-attention
     └───────┬──────┘          │ (12 camadas)     │  e prevê a justificativa
             │                 └────────┬─────────┘  (tokens do T5)
          L_cls                        L_aux
             └──────────┬───────────────┘
              L = L_cls + 0,1 · L_aux        (fase C; nas fases A e B só L_aux)
```

Na avaliação só existe o lado esquerdo. O decoder serve apenas para empurrar o BERT durante o treino.

---

## Os arquivos

Quatro módulos novos em `src/radibert/` e um arquivo de teste. Cada módulo tem uma responsabilidade:

| Arquivo | Faz | Não faz |
|---|---|---|
| `rte_dados.py` | junta o parquet do RTE com o CSV da FA, aplica a limpeza C, tira os 20 exemplos, tokeniza com os **dois** tokenizadores, monta os lotes | não sabe nada de modelo |
| `rte_modelo.py` | a classe `RationaleBert` (BERT + cabeça + decoder opcional) e a função que monta o classificador só com BERT + cabeça para avaliar | não sabe nada de fases nem de taxa |
| `rte_treino.py` | o laço com as fases A/B/C, o otimizador, o agendamento da taxa, a avaliação no dev e o CSV de resultados; linha de comando | não monta modelo nem lê arquivo de dado diretamente |
| `rte_gradientes.py` | calcula as palavras de rótulo, põe cada token do alvo num grupo (S, C ou N) e mede `g_c`, `g_S`, `g_C`, `g_N` no lote de sonda (seção "Medidas de gradiente") | não muda nenhum peso |
| `tests/test_rte_treino.py` | as invariantes do fim deste documento, em modelos minúsculos com pesos aleatórios (rodam na CPU, sem baixar nada) | não mede qualidade |

Dependências novas (proposta): `torch==2.14.1` (no PC, roda `cu130` pelo índice do PyTorch, declarada no
`pyproject.toml` com `[tool.uv.sources]`) e `transformers==5.20.2`. O `scikit-learn` que já está no projeto calcula
ROC-AUC e F1. A versão mais nova do transformers (5.22.2, 06/11) foi preterida por ter só 3 dias.

---

## `rte_dados.py`: do parquet ao lote

### O que entra

- `dados/rte/rte_train.parquet` (2.490 pares) e `dados/rte/rte_validation.parquet` (277 pares).
- `resultados/rte-35B/racionalizacoes-FA.csv` (2.470 justificativas, uma por `idx`).
- Os 20 `idx` dos exemplos, lidos por `rte_racionalizacoes.rte_examples()`, a mesma função que montou o prompt.

### Onde entram a limpeza C e os 20 exemplos

```python
def training_pairs() -> pd.DataFrame:
    train = read_rte("train")                                    # 2.490 pares, label 0/1 do GLUE
    fa = pd.read_csv(FA_CSV, usecols=["idx", "qwen"])
    pairs = train.merge(fa, on="idx", how="inner")               # os 20 exemplos não têm linha na FA: saem aqui
    pairs["rationale"] = pairs["qwen"].map(clean_opening)        # limpeza C só aqui, o CSV fica intacto
    pairs["y"] = (pairs["label"] == 0).astype(int)               # GLUE: 0 = entailment -> classe positiva
    return pairs                                                 # 2.470 linhas, as MESMAS nos dois braços
```

Três escolhas estão nesse trecho:

1. **A limpeza C acontece na montagem, nunca no CSV.** O texto original do Qwen fica guardado. Se a C mudar, basta
   rodar o treino de novo.
2. **Os 20 exemplos saem dos dois braços** (proposta do Claude). Eles não têm justificativa do Qwen, porque estavam
   dentro do prompt. As deles são rascunhos do Claude, e usar saída do Claude como alvo de treino é o que a Usage
   Policy proíbe. Tirar os 20 só do braço com decoder faria os braços treinarem em conjuntos diferentes. Por isso o
   BERT sozinho também treina nos 2.470.
3. **A classe positiva é `entailment`** (y = 1). O GLUE codifica `entailment` como 0, então a conversão tem teste
   próprio. As métricas do Agrawal (ROC-AUC, precisão e revocação a 0,7) dependem de qual classe é a positiva. No
   paper a positiva é "relevante", a que a justificativa defende.

### Os dois tokenizadores

```python
bert_tok = AutoTokenizer.from_pretrained("google-bert/bert-base-uncased")
t5_tok   = AutoTokenizer.from_pretrained("google-t5/t5-base")

enc = bert_tok(premise, hypothesis, truncation="only_first", max_length=512)   # [CLS] p [SEP] h [SEP]
tgt = t5_tok(rationale, max_length=64, truncation=True).input_ids              # termina com </s> (id 1)
```

- A entrada mais longa do RTE tem cerca de 320 tokens (estimativa por palavras em `analise-lote-FA.md`). Com
  `max_length=512` **nada é cortado**, e a invariante I9 confirma isso com o tokenizador de verdade.
- A justificativa mais longa tem 34 palavras, uns 50 tokens do T5. O teto de 64 também não corta nada (I9).
- **Preenchimento por lote** (*dynamic padding*): cada lote é completado até o par mais longo **daquele lote**, não até 512.
  A mediana é ~56 tokens, então os lotes ficam curtos e rápidos.
- No alvo, as posições de preenchimento viram `-100`. É o valor que o `CrossEntropyLoss` do T5 ignora (conferido na
  linha 1051 do `modeling_t5.py`).

O `collate` devolve um dicionário: `input_ids`, `attention_mask`, `token_type_ids` (do BERT), `y` e `labels` (do T5).

---

## `rte_modelo.py`: as classes

### `RationaleBert`

```python
class RationaleBert(nn.Module):
    def __init__(self, bert_name, with_decoder: bool, t5_name="google-t5/t5-base"):
        self.bert = AutoModel.from_pretrained(bert_name)                         # BertModel
        self.head = nn.Sequential(nn.Dropout(0.1), nn.Linear(hidden, 1))         # 1 logit: entailment
        self.t5 = T5ForConditionalGeneration.from_pretrained(t5_name) if with_decoder else None
        needs_bridge = with_decoder and hidden != self.t5.config.d_model
        self.bridge = nn.Linear(hidden, self.t5.config.d_model) if needs_bridge else None   # só no teste (D6)

    def forward(self, batch):
        h = self.bert(batch["input_ids"], batch["attention_mask"], batch["token_type_ids"]).last_hidden_state
        logit = self.head(h[:, 0]).squeeze(-1)                                    # vetor do [CLS]
        if self.t5 is None:
            return logit, None
        enc = self.bridge(h) if self.bridge is not None else h
        out = self.t5(encoder_outputs=(enc,), attention_mask=batch["attention_mask"], labels=batch["labels"])
        return logit, out.loss                                                    # out.loss = L_aux
```

O que cada linha faz, e por que funciona:

- **`encoder_outputs=(enc,)`** é o ponto central. O `T5ForConditionalGeneration` só roda o encoder do próprio T5 quando
  `encoder_outputs` vem vazio (linha 1009). Passando os vetores do BERT ali, o decoder do T5 lê o BERT **como se ele
  fosse o encoder do T5**. Não é preciso reescrever o decoder.
- **`attention_mask=batch["attention_mask"]`** vira a máscara da *cross-attention* (linha 1037,
  `encoder_attention_mask=attention_mask`). Assim o decoder não lê as posições de preenchimento do BERT.
- **`labels=...`**: o T5 desloca o alvo uma posição para a direita sozinho (`_shift_right`, com o token inicial 0).
  Isso é o *teacher forcing* do passo 3 do outro documento. Ele também calcula a entropia cruzada média por token
  ignorando os `-100`. Esse número é o `L_aux`.
- **O gradiente de `L_aux` chega ao BERT** porque `h` sai do BERT sem `detach`. É o mecanismo inteiro do método, e
  por isso a invariante I7 testa exatamente isso.
- O encoder do T5 continua carregado mas nunca roda: são ~85M de pesos parados, ~340 MB de VRAM. Ele fica congelado
  e **fora do otimizador**. Arrancar o encoder do objeto pouparia esses 340 MB, mas a geração e outros métodos da
  biblioteca contam com ele. Na 5060 sobra memória (conta abaixo), então fica.
- **`bridge`** é o adaptador 128 → 768 da D6. Ele só existe quando o BERT não tem vetor de 768, ou seja, no teste de
  fumaça com o BERT minúsculo. A invariante I4 garante que ele **não existe** na rodada de verdade.
- **"Ignore CLS"** (§4.4 do Agrawal): o esboço passa **todos** os vetores ao decoder, inclusive o do `[CLS]`. Na
  Tabela 3 as duas formas trocam de lugar, então nenhuma tem vantagem clara. Ver E3.

### `classifier_only(model)`

```python
def classifier_only(model: RationaleBert) -> nn.Module:
    """BERT + cabeça, copiados; o decoder não existe neste objeto."""
```

A avaliação recebe **este** objeto, nunca o `RationaleBert`. Assim é impossível o decoder ajudar na nota do dev. A
invariante I8 confere que nenhuma chave do `state_dict` dele começa com `t5.` ou `bridge.`.

### Tamanho e memória (conta do Claude, a medir)

| Parte | Parâmetros treináveis |
|---|---|
| BERT base | 110M |
| Decoder do T5 base (12 blocos × ~9,4M) | ~113M |
| Embeddings do T5 (`shared`, 32.128 × 768, também usados pelo `lm_head`) | ~25M |
| Cabeça | 769 |
| **Total** | **~248M** (o outro documento dizia ~230M; faltava o embedding do T5) |

Com AdamW em fp32 são ~16 bytes por parâmetro, **~4,0 GB**, mais ~0,3 GB do encoder parado. As sequências do RTE
são curtas (mediana ~56 tokens), então lote 32 em bf16 deve caber nos 8 GB **sem acumulação**. Se estourar, a saída
é lote 16 × 2. A primeira rodada mede.

---

## `rte_treino.py`: o laço

### As contas de passo, com os 2.470 pares

| Quantidade | Conta | Valor |
|---|---|---|
| Passos por época | ⌈2.470 / 32⌉ | 78 (o último lote tem 6 pares) |
| Treino total (8 épocas, Tabela 4) | 78 × 8 | **624** |
| Fase A (uma passada por metade dos pares, D3) | ⌈1.235 / 32⌉ | **39**, fora dos 624 |
| Fase B (30% do treino, D3) | ⌊0,3 × 624⌋ | passos **1–187** |
| Fase C | o resto | passos **188–624** |
| Aquecimento da taxa, cópia fiel (D2) | Tabela 4 | **500** passos |
| Aquecimento da taxa, proporcional (D2) | ⌊0,1 × 624⌋ | **62** passos |

(O outro documento usava 2.490 pares e dava 623. Com os 20 exemplos fora são 624.)

### O esqueleto

```python
def train(arm, warmup, seed, bert_name):
    set_seed(seed)                                          # ordem dos lotes, metade da fase A, cabeça, dropout
    model = RationaleBert(bert_name, with_decoder=(arm == "bert_decoder"))
    opt = AdamW(param_groups(model), lr=5e-5, eps=1e-8, betas=(0.9, 0.999))
    sched = LambdaLR(opt, lr_factors(warmup, total=624, phase_b=187))     # um fator por grupo, ver abaixo

    if arm == "bert_decoder":
        phase_a(model, opt, half_of_train(seed))            # 39 passos, BERT congelado, só L_aux

    for step, batch in enumerate(eight_epochs(seed), start=1):            # 624 passos
        logit, l_aux = model(batch)
        l_cls = binary_cross_entropy_with_logits(logit, batch["y"])
        if arm == "bert":
            loss = l_cls
        elif step <= 187:
            loss = l_aux                                    # fase B: a cabeça não aprende nada aqui
        else:
            loss = l_cls + 0.1 * l_aux                      # fase C (§4.3)
        loss.backward()
        clip_grad_norm_(model.parameters(), 1.0)
        opt.step(); sched.step(); opt.zero_grad()

    return evaluate(classifier_only(model), dev_loader())
```

### O otimizador em grupos

| Grupo | O que tem | Weight decay | Fonte |
|---|---|---|---|
| `encoder` | BERT | 0 | Tabela 4 |
| `head` | a cabeça linear | 0 | **proposta do Claude** (o paper não diz) |
| `decoder` | decoder do T5 + `shared` (+ `bridge` no teste) | 0,001 | Tabela 4 |

O encoder do T5 fica fora de todos os grupos.

### Fase A, em detalhe

```python
def phase_a(model, opt, pairs):
    for batch in batches(pairs):                            # 39 lotes
        with torch.no_grad():
            h = model.bert(...).last_hidden_state           # sem gradiente: o BERT não muda
        l_aux = model.t5(encoder_outputs=(h,), ...).loss
        l_aux.backward(); clip; opt.step(); opt.zero_grad()
```

`torch.no_grad()` no BERT é a forma mais simples de "congelado". Nenhum gradiente é calculado ali, então o BERT não
muda e a fase gasta menos memória. A invariante I5 compara os pesos do BERT antes e depois.

### O agendamento da taxa

São dois aquecimentos no paper, e o código tem de dizer como eles convivem:

- o da **Tabela 4** (500 passos, ou 62 na versão proporcional), que vale para o treino;
- o da **Fase B** (§4.4: o encoder é liberado com "aquecimento linear nos primeiros 30%"), que vale para o BERT.

**Leitura proposta (E1):** cada grupo tem o próprio fator, multiplicado pela taxa de 5e-5.

```
fator(passo) do decoder e da cabeça:  sobe de 0 a 1 em W passos (W = 500 ou 62) e cai linearmente até 0 no passo 624
fator(passo) do BERT:                 sobe de 0 a 1 nos passos 1–187 (fase B) e cai linearmente até 0 no passo 624
fase A:                               taxa constante de 5e-5 no decoder (fora do relógio dos 624 passos)
braço BERT sozinho:                   um fator só para tudo, o da Tabela 4 (W = 500 ou 62)
```

A queda linear até zero depois do aquecimento é o padrão do `get_linear_schedule_with_warmup` da Hugging Face, e a
Tabela 4 fala em "warmup steps" do jeito dela. O paper não descreve a queda, então isto é **interpretação declarada**.

Uma consequência que o termo precisa dizer: **na cópia fiel, a cabeça só começa a aprender no passo 188 e já está com
taxa reduzida**. Ela aprende em 437 passos, contra 624 do BERT sozinho. Isso é o desenho do paper, não um erro do código,
mas é diferença entre os braços que um nulo pode esconder.

**Segunda diferença, apontada pelo training-auditor (09/11):** o aquecimento do **BERT** também muda de braço para
braço. No braço com decoder ele aquece nos 187 passos da fase B (E1); no BERT sozinho, nos 500 ou 62 passos da Tabela 4.
Fora o decoder, os braços diferem em duas coisas: o atraso da cabeça e a rampa do BERT. Um resultado nulo (ou um
ganho) tem de nomear as duas.

### Avaliação

```python
def evaluate(clf, dev):
    p = sigmoid(clf(dev))                                   # probabilidade de entailment, 277 pares
    return {"roc_auc": roc_auc_score(y, p),
            "precision@0.7": precision_score(y, p >= 0.7), "recall@0.7": recall_score(y, p >= 0.7),
            "accuracy": accuracy_score(y, p >= 0.5), "f1_macro": f1_score(y, p >= 0.5, average="macro"),
            "f1_entailment": ..., "f1_not_entailment": ...}            # D4
```

- **O dev é o teste** (o teste do GLUE não tem rótulo). Por isso ele é lido **uma vez, no fim**: sem parada antecipada,
  sem escolher época pelo dev. Vale o modelo do passo 624.
- Cada rodada acrescenta uma linha a `resultados/rte-treino/resultados.csv` com braço, aquecimento, semente, as
  métricas, o `L_aux` final, o tempo e o commit do código. Não se salvam pesos (proposta: E8). O CSV é o resultado.

### A grade de rodadas

| Braço | Aquecimento | Sementes | Rodadas |
|---|---|---|---|
| BERT sozinho | 500 · 62 | 5 (10 se barato, D5) | 10 (20) |
| BERT + decoder | 500 · 62 | 5 (10) | 10 (20) |

São 20 rodadas, ou 40 com 10 sementes. Com sequências curtas, cada rodada deve levar poucos minutos na 5060 (conta
grossa do Claude, a medir na primeira). As sementes são as mesmas nos dois braços, então a mesma semente dá a mesma
ordem de lotes nos dois.

### Linha de comando

```
uv run python -m radibert.rte_treino --arm bert_decoder --warmup prop --seed 1   # prop = 10% dos passos; ou 500
uv run python -m radibert.rte_treino --grade            # a tabela acima, pulando o que já está no CSV
uv run python -m radibert.rte_treino --fumaca           # D6: BERT minúsculo + bridge + T5 base, 3 passos, CPU
```

O `--grade` pula combinações que já estão no CSV, como os lotes do Qwen. Se o PC cair, roda-se de novo e ele continua de
onde parou.

---

## Medidas de gradiente durante o treino

Duas medidas combinadas antes entram no laço: a **ideia do Pedro de 28/10** (`docs/ideias-de-desenho.md`, a partir de
Wadhwa et al. 2024) e o **cosseno g_c·g_a** de `docs/2026-10-20-perdas-o-que-e-I-gradiente.md` §3.5.

### Por que importa no RTE: o rótulo está escrito na justificativa

Contagem sobre os 2.470 da FA (09/11, script avulso do Claude com a regra do item 1 abaixo, que o código vai recalcular
e salvar):

- **"not / never / no" aparece em 90% das justificativas de not_entailment e em 4% das de entailment.** Só por essas
  palavras já se adivinha o rótulo quase sempre.
- 90 expressões de 1 a 3 palavras aparecem 30 vezes ou mais e caem em 90% ou mais das vezes num só rótulo.
  - Do lado de not_entailment: "does not" 381/398, "never" 167/168, "does not mention" 76/76, "not necessarily",
    "no information", "is not established", "unknown".
  - Do lado de entailment: "confirming" 203/205, "directly" 173/184, "is explicitly" 127/134, "which means" 44/45,
    "constitutes" 47/47.

É o equivalente no RTE de "mutually exclusive / cannot" no e-SNLI. Para o decoder acertar essas palavras, o BERT
precisa saber o rótulo, que já é o que a `L_cls` pede. A pergunta de 28/10 continua a mesma: **quanto do empurrão do
decoder no BERT vem dessas palavras, e quanto vem do conteúdo (o fato que decide)?** Se quase tudo vier delas, a
cabeça auxiliar é uma segunda cabeça de classificação, e o método não está ensinando o "porquê".

### Como medir: três grupos de tokens (Pedro, 09/11: "os três")

Todo token da justificativa cai em **exatamente um** grupo, testado nesta ordem:

| Grupo | Regra | Exemplo em "Titan has an atmosphere but the text never mentions its orbit" (premissa fala de Titã e da atmosfera) |
|---|---|---|
| **S, palavras de rótulo** | o token está dentro de uma expressão de 1 a 3 palavras com 30 ocorrências ou mais e 90% ou mais num só rótulo (calculada **só no treino**) | "but", "never mentions" |
| **F, gramatical** (Pedro, 09/11: "F separado") | *stop word*, palavra de enunciado de `copia.py` ("states", "premise"), "text", "passage", letra solta, ou token que não é palavra (pontuação, `</s>`) | "has", "an", "the", "text", "its", "." |
| **N, palavra nova** | palavra de conteúdo que **não aparece** na premissa nem na hipótese (números contam como palavra) | "orbit" |
| **C, copiada do par** | palavra de conteúdo que está no par | "Titan", "atmosphere" |

A regra de N é a mesma de `copia.new_words`, já usada no e-SNLI e na análise do lote (mediana de 4 palavras novas por
justificativa). Não há lematização, então "moons" é nova se o par diz "moon". S vem primeiro: uma palavra de rótulo
fica em S mesmo que esteja no par.

**Prévia por palavra no lote FA** (09/11, script avulso do Claude; o código faz o mesmo por token do T5):
**S 12% · C 71% · N 17%** das 49.767 palavras.
- **S:** "not", "but", "does", "confirming", "no", "never".
- **C:** dominado por palavras gramaticais ("the", "a", "in", "to").
- **N:** **mais conectivo de raciocínio do que conhecimento de mundo.** As mais comuns são "implying", "specific",
  "identified", "meaning", "explicitly" e "claim". As de conteúdo vêm logo atrás: "location", "role", "date", "year",
  "event".

Isso pesa na leitura:
- **N não é "conhecimento do professor" puro.** É "o que o professor escreveu além do par", com muito conectivo
  misturado.
- **C mistura cópia do par com gramática.** As palavras gramaticais são fáceis e devem ter perda baixa cedo, mas
  enquanto não tiverem, entram na parcela de C. Ver a pergunta aberta no fim desta seção.

Para cada rodada, o código salva `resultados/rte-treino/grupos-palavras.csv` com as 50 palavras mais comuns de cada
grupo. Assim dá para ler o que cada número significa, sem confiar no nome do grupo.

**Passos da medida:**

1. **Marcação.** Em cada justificativa, os trechos que casam com S e as palavras de N viram posições de caractere. O
   tokenizador rápido do T5 devolve a posição de cada token (`return_offsets_mapping`), então cada token do alvo
   recebe S, C ou N.
2. **Lote de sonda fixo:** 64 pares do treino, os mesmos em todas as rodadas (sorteados uma vez com semente própria).
   A medida roda com o modelo em `eval()` (sem dropout) e volta para `train()` depois.
3. **A cada 25 passos, nas fases B e C** (na fase A o BERT está congelado e não recebe gradiente), são quatro
   `backward` só nos pesos do BERT: `g_c` (da `L_cls`) e `g_S`, `g_C`, `g_N` (das partes da `L_aux` que vêm de cada
   grupo). A `L_aux` é a média por token, então `L_aux = L_S + L_C + L_N` com o mesmo denominador, e
   `g_a = g_S + g_C + g_N` exatamente.
4. **O que vai para `resultados/rte-treino/gradientes.csv`**, por braço, aquecimento, semente e passo:

| Coluna | O que diz |
|---|---|
| `frac_tokens_S`, `_C`, `_N` | fração dos tokens do alvo em cada grupo. É a régua: se S tem 12% dos tokens e 60% do gradiente, domina |
| `share_S`, `_C`, `_N` = g_X·g_a / ‖g_a‖² | quanto do gradiente auxiliar vem de cada grupo; os três somam 1 |
| `cos(g_c, g_a)` | a medida de 20/10: a auxiliar ajuda (> 0), é neutra (≈ 0) ou briga (< 0) |
| `cos(g_c, g_S)`, `_C`, `_N` | o argumento do §3.4 de 20/10: S deve concordar com a classificação; se houver briga, de que grupo ela vem |
| `l_S`, `l_C`, `l_N` | perda média por token de cada grupo, para ver qual o decoder já aprendeu |
| `‖g_c‖`, `‖g_a‖` | escala, para ler o 0,1 do λ |

Custo: 25 medidas por rodada × 4 `backward` em 64 pares, segundos por rodada (conta do Claude).

**Decidido (Pedro, 09/11): F separado.** Com as regras finais do código (`word_groups`, 90 expressões de rótulo nos
2.470, depois da correção da C), as 50.800 palavras ficam em **S 12,0% · F 40,3% · C 31,2% · N 16,5%**. Quase metade
do C de três grupos era gramática.

### Influência de cada palavra no encoder (pedido do Pedro, 09/11)

**Três números diferentes, que não convém misturar:**

| Pergunta | Número | Onde |
|---|---|---|
| A palavra é difícil para o **decoder**? | `l` = perda do decoder naquela palavra | `l_S/C/N` nos grupos; `l_t` por palavra |
| Quanto a palavra **mexe no encoder**? | ‖g‖ = tamanho do gradiente dela **nos pesos do BERT** | `share_*` nos grupos; `norm_t` por palavra |
| Esse empurrão no encoder **ajuda a classificar**? | g_c·g / ‖g_c‖ = quanto do empurrão aponta na direção da `L_cls` | `cos_c_*` nos grupos; `align_t` por palavra |

As medidas por grupo já são do encoder: g_S, g_C e g_N são gradientes nos pesos do BERT, não no decoder. O que faltava
era a resolução por palavra.

O `align_t` tem leitura direta pelo nosso doc de 20/10 (§3, ΔL ≈ gradiente × deslocamento). Se o BERT desse um passo
de tamanho η empurrado **só** pela palavra t, a `L_cls` mudaria em ≈ −η·0,1·(g_c·g_t). Positivo quer dizer que a
palavra ensina ao encoder algo que serve para classificar. Negativo, que ela puxa contra. É a mesma ideia de medir
influência por produto de gradientes do TracIn (arXiv:2002.08484, "Estimating Training Data Influence by Tracing
Gradient Descent"). **Nível 3:** só o título foi conferido, e lá a unidade é o exemplo de treino, não a palavra.

**Como medir:**

1. **Unidade = ocorrência de palavra**, não tipo. Contei numa sonda de 128 pares: só 48 palavras aparecem 8 vezes ou
   mais, e elas cobrem 44% do texto, quase todas gramaticais ou de rótulo. As palavras de conteúdo ("Titan",
   "orbit") aparecem uma vez cada. Por isso cada ocorrência vira uma linha, e a agregação vem depois: por tipo para
   as frequentes, por grupo (S/C/N) e por par para as raras.
2. **Uma palavra = a soma das perdas dos tokens do T5 que a formam** ("Saturn's" pode virar 3 tokens). Um `backward`
   por ocorrência, só nos pesos do BERT, com o g_c da sonda inteira guardado. Cada g_t vira três números e é
   descartado na hora, então a memória fica em ~2 gradientes. O `</s>` do fim de cada alvo entra como uma "palavra"
   própria (grupo C), para que a soma feche (I15). A sonda por palavra tem 128 pares (64 por rótulo), os mesmos em
   todas as rodadas.
3. **Custo** (conta do Claude, a medir): 128 pares × ~20 palavras ≈ 2.600 `backward` de um par só, cerca de 1 minuto
   por medida na 5060. Por isso roda em **3 pontos** (passo 1, passo 187 no fim da fase B e passo 624 no fim) e só em
   **uma semente por aquecimento** no braço com decoder (`--medir-palavras`). A medida por grupo continua a cada 25
   passos em todas as rodadas.
4. **Saída:** `resultados/rte-treino/palavras.csv`, uma linha por (rodada, passo, idx, posição): palavra, grupo
   S/C/N, `l_t`, `norm_t`, `align_t`, `cos_t`.

```python
def measure_words(model, probe, step) -> list[dict]:
    """Uma linha por ocorrência de palavra do alvo: perda no decoder, empurrão no encoder e alinhamento com a L_cls."""
    model.eval()
    params = list(model.bert.parameters())
    h, logit = model.encode(probe)
    g_c = torch.autograd.grad(binary_cross_entropy_with_logits(logit, probe["y"]), params, retain_graph=True)
    norm_c = dot(g_c, g_c) ** 0.5
    nll = token_nll(model.decode(h, probe), probe["labels"]) / probe["n_target_tokens"]   # mesmo denominador da L_aux
    rows = []
    for i, pos, word, group, token_ids in probe["word_spans"]:     # (par, posição, palavra, S/C/N, tokens do T5)
        l_t = nll[i, token_ids].sum()
        g_t = torch.autograd.grad(l_t, params, retain_graph=True)
        rows.append({"step": step, "idx": probe["idx"][i], "pos": pos, "word": word, "group": group,
                     "l_t": l_t * probe["n_target_tokens"] / len(token_ids),   # perda média por token da palavra
                     "norm_t": dot(g_t, g_t) ** 0.5, "align_t": dot(g_c, g_t) / norm_c,
                     "cos_t": dot(g_c, g_t) / (norm_c * dot(g_t, g_t) ** 0.5)})
    model.train()
    return rows
```

O esboço faz o `backward` no grafo do lote inteiro. Na escrita, a versão final roda **um par por vez** (forward de um
par, `backward` por palavra dele), que é o que torna o custo ~1 minuto.

**Invariante nova, I15:** a soma dos `align_t` de todas as palavras da sonda é igual a g_c·g_a/‖g_c‖, o alinhamento da
`L_aux` inteira. As palavras dividem exatamente o empurrão total, como os grupos.

**Limite:** o `align_t` é de primeira ordem (um passo pequeno, sem Adam). O AdamW normaliza o passo por parâmetro, então
o passo real não é η·g. A medida diz **para onde** cada palavra empurra o encoder, não quanto o otimizador de fato anda.

### O que a medida prova e o que não prova

- 25 pontos por rodada cobrem início, meio e fim, como a nota de 28/10 pedia: palavra fácil tem perda perto de zero
  no fim e gradiente baixo, mesmo que tenha dominado o começo.
- **`share_S` alto não prova dano.** Quem prova é um terceiro braço com os tokens de S fora da `L_aux`. Esse braço
  **não entra na grade agora**: só faz sentido se o `share_S` vier alto. O mesmo vale para C (um braço sem a cópia do
  par, a pergunta do eco do e-SNLI).
- A medida é **parcela do gradiente por grupo de palavras**, não o método de atribuição do Wadhwa 2024 (ver abaixo).

### O que o Wadhwa et al. (2024) fez de fato, e por que a medida aqui é outra

**Procedência:** o Claude leu em 09/11 o §2 "Experimental Design", parte RQ3 "Attribution from Rationales", e a Tabela 3,
na versão HTML do arXiv (2406.14511v2). É nível 2 só nesse trecho. O Pedro leu o paper na Semana 5.

- **Método:** *Integrated Gradients* (Sundararajan et al. 2017). Eles ajustam um GPT-2 para escrever a justificativa
  **antes** do rótulo e medem quanto cada token da justificativa pesa na **saída do rótulo**: o gradiente da saída em
  relação ao embedding do token, integrado do vetor de base (zero ou neutro) até o embedding real. A direção é
  **token da justificativa → rótulo**.
- **Uso:** guardam os 15 tokens de maior atribuição (a justificativa média tem 36,3 tokens) e treinam os alunos (GPT-2,
  Phi-1.5, Gemma-2B; professor Mistral-7B-Instruct) com esses 15 depois do rótulo. O desempenho não muda de forma
  significativa em relação à justificativa inteira.
- **O controle que interessa aqui:** trocar a justificativa pelas 15 palavras mais **parecidas com o rótulo**
  (vizinhas no Word2Vec) dá resultado comparável a **não usar justificativa**. Na frase deles, os tokens precisam
  trazer sinal "além de ser simplesmente parecidos" com o rótulo.

**Por que não dá para copiar o método:** o IG deles pergunta de quais tokens da justificativa a previsão do rótulo
depende. Isso só existe num modelo que **lê** a justificativa antes de dar o rótulo. Aqui o classificador nunca vê a
justificativa: ela é só alvo do decoder. A pergunta equivalente no nosso desenho é a inversa, **quais tokens da
justificativa moldam o encoder** (direção **token da justificativa → pesos do BERT**), e é isso que o `share_S` mede.

**O que o Wadhwa empresta para a leitura do resultado** (hipótese, não prova, porque o aluno deles é decoder):
as palavras de rótulo do RTE ("not", "never", "confirming") são o caso "parecido com o rótulo". Se o `share_S` vier
alto, a previsão pelo Wadhwa é **ganho perto de zero** contra o BERT sozinho. Se vier baixo e houver ganho, o ganho
vem do conteúdo.

### Esboço do código da medida

Esboço para aprovar. Os nomes podem mudar na escrita, o desenho não.

```python
# src/radibert/rte_gradientes.py
MIN_COUNT, MIN_SHARE = 30, 0.9          # a regra das palavras de rótulo
MEASURE_EVERY = 25                      # passos; mede também o passo 1
PROBE_SIZE, PROBE_SEED = 64, 0          # 32 por rótulo, os mesmos em toda rodada

def label_expressions(train: pd.DataFrame) -> re.Pattern:
    """Expressões de 1 a 3 palavras com >= 30 ocorrências e >= 90% num rótulo. Lê só o treino.
    Salva resultados/rte-treino/expressoes-rotulo.csv (expressão, n_entailment, n_not_entailment) e devolve uma
    regex com todas, a mais longa primeiro."""

GROUPS = ("S", "C", "N")                 # rótulo, copiada do par (e gramática), nova
SOURCE_WORDS = {"text", "passage"}      # nomeiam a fonte, como "premise" e "sentence" em copia.META

def token_groups(rationale: str, premise: str, hypothesis: str, t5_tok, label_expr: re.Pattern) -> list[int]:
    """Índice do grupo (0 = S, 1 = C, 2 = N) de cada token do T5 no alvo (I13)."""
    enc = t5_tok(rationale, return_offsets_mapping=True, truncation=True, max_length=64)
    s_spans = [m.span() for m in label_expr.finditer(rationale)]
    pair = set(re.findall(r"[a-z]+", f"{premise} {hypothesis}".lower()))
    n_spans = [m.span() for m in re.finditer(r"[a-z]+", rationale.lower())
               if len(m.group()) > 1 and m.group() not in DROP | SOURCE_WORDS and m.group() not in pair]
    overlaps = lambda spans, a, b: any(x < b and a < y for x, y in spans)
    return [0 if overlaps(s_spans, a, b) else 2 if overlaps(n_spans, a, b) else 1 for a, b in enc["offset_mapping"]]
    # o </s> do fim vem com posição (0, 0): não cruza nada e cai em C

def aux_loss_split(t5_out, labels, groups) -> list:
    """L_aux dividida por grupo com o mesmo denominador: a soma é exatamente a L_aux (I12)."""
    nll = cross_entropy(t5_out.logits.transpose(1, 2), labels, ignore_index=-100, reduction="none")  # [lote, tokens]
    valid = labels != -100
    n = valid.sum()
    return [(nll * (valid & (groups == g))).sum() / n for g in range(len(GROUPS))]

def measure(model, probe, step) -> dict:
    """Quatro gradientes só nos pesos do BERT, sem tocar em peso nem no .grad do otimizador (I14)."""
    model.eval()                                            # sem dropout: número estável, sem gastar o sorteio
    params = list(model.bert.parameters())
    h, logit = model.encode(probe)                          # o mesmo caminho do forward do treino
    l_cls = binary_cross_entropy_with_logits(logit, probe["y"])
    parts = aux_loss_split(model.decode(h, probe), probe["labels"], probe["groups"])
    g_c = torch.autograd.grad(l_cls, params, retain_graph=True)     # autograd.grad devolve o gradiente
    g_x = [torch.autograd.grad(l, params, retain_graph=True) for l in parts]   # sem somar no .grad:
    model.train()                                                    # o otimizador não vê nada disso
    dot = lambda x, y: sum((a * b).sum() for a, b in zip(x, y))     # produto escalar camada a camada
    g_a = [sum(layer) for layer in zip(*g_x)]
    valid = probe["labels"] != -100
    row = {"step": step, "phase": "B" if step <= 187 else "C", "l_cls": l_cls,
           "cos_c_a": cosine(g_c, g_a, dot), "norm_c": dot(g_c, g_c) ** 0.5, "norm_a": dot(g_a, g_a) ** 0.5}
    for name, g, loss, idx in zip(GROUPS, g_x, parts, range(len(GROUPS))):
        row |= {f"frac_tokens_{name}": (probe["groups"][valid] == idx).float().mean(),
                f"share_{name}": dot(g, g_a) / dot(g_a, g_a),
                f"cos_c_{name}": cosine(g_c, g, dot),
                f"l_{name}": loss / (probe["groups"][valid] == idx).float().mean()}   # perda média por token do grupo
    return row
```

**O que muda nos outros arquivos:**

- `rte_modelo.py`: o `forward` passa a ser `encode` (BERT + cabeça, devolve `h` e o logit) seguido de `decode` (o T5
  sobre `h`). O treino e a medida chamam **as mesmas duas funções**, então não há como a medida olhar um modelo
  diferente do que treina.
- `rte_dados.py`: o `collate` passa a devolver também `groups` (0/1/2 por token do alvo), que só a medida lê. A
  perda do treino não usa os grupos.
- `rte_treino.py`, dentro do laço do braço com decoder, depois do `opt.step()`:

  ```python
  if step == 1 or step % MEASURE_EVERY == 0:
      gradient_rows.append({**run_keys, **measure(model, probe, step)})
  ...
  append_csv(RESULTADOS / "rte-treino" / "gradientes.csv", gradient_rows)   # junto com a linha de resultados.csv
  ```

  São 25 medidas por rodada: os passos 1, 25, 50, ..., 600. A fase A fica de fora porque o BERT está congelado. O
  braço BERT sozinho também fica de fora, porque não tem `L_aux`.

**Memória e tempo (conta do Claude, a medir):** os quatro gradientes do BERT ocupam juntos ~1,8 GB em fp32 enquanto a
medida roda, e são soltos logo depois. Se não couber ao lado do estado do treino, eles vão para a CPU, e a medida fica
mais lenta mas continua em segundos. Por rodada, são 100 `backward` a mais em 64 pares.

**Invariante nova:** a I14 diz que **medir não muda o treino**. Duas rodadas minúsculas com a mesma semente, uma com
medida e outra sem, terminam com a mesma perda e os mesmos pesos. Isso prova que a medida não toca no `.grad`, nos
pesos nem no sorteio.

## Invariantes

Cada linha vira um teste em `tests/test_rte_treino.py`, com BERT e T5 de configuração minúscula e pesos aleatórios
(`BertConfig(hidden_size=32, ...)`, `T5Config(d_model=32, ...)`). Roda na CPU em segundos, sem rede, e cabe no CI.

| # | Invariante | Como o teste prova |
|---|---|---|
| I1 | treino e dev não têm par em comum | nenhum par (premissa, hipótese) repetido entre os dois (o `idx` recomeça em cada split e não serve) |
| I2 | os 20 exemplos ficam fora, e os dois braços treinam nos mesmos 2.470 | `training_pairs()` sem nenhum `idx` de `rte_examples()`; mesmo conjunto nos dois braços |
| I3 | y = 1 ⇔ `entailment` | um par conhecido do treino com label 0 no GLUE sai com y = 1 |
| I4 | o braço BERT sozinho não tem decoder, e a rodada de verdade não tem `bridge` | `model.t5 is None`; com hidden 768, `model.bridge is None` |
| I5 | fase A não muda o BERT | pesos do BERT idênticos antes e depois; pesos do decoder diferentes |
| I6 | fase B não muda a cabeça | pesos da cabeça idênticos antes e depois do passo 187 |
| I7 | **o gradiente de `L_aux` chega ao BERT** | `L_aux.backward()` sozinho deixa gradiente não nulo numa camada do BERT |
| I8 | a avaliação não vê o decoder | `classifier_only` sem chave `t5.`/`bridge.`; mesma nota com o decoder zerado |
| I9 | nada é cortado | nenhuma entrada passa de 512 tokens e nenhum alvo passa de 64; a contagem é registrada no log da rodada |
| I10 | a mesma semente reproduz | duas rodadas minúsculas com a mesma semente dão a mesma perda na CPU |
| I11 | as contas de passo batem | 78 por época, 624 no total, fase A com 39, fase B até 187 |
| I12 | a divisão do gradiente fecha | `L_S + L_C + L_N` igual à `L_aux` do T5; `g_S + g_C + g_N` igual a `g_a` (tolerância numérica); os três `share` somam 1 |
| I13 | os grupos caem nos tokens certos | com premissa sobre Titã e atmosfera, em "Titan has an atmosphere but the text never mentions its orbit": "but" e "never mentions" em S, "orbit" em N, "Titan" e "atmosphere" em C, "has", "the", "text", "its" e `</s>` em F; S é calculado sem ler o dev |
| I14 | medir não muda o treino | mesma semente com e sem `measure()` e `measure_words()`: perdas e pesos finais iguais |
| I15 | as palavras dividem o empurrão total | soma dos `align_t` da sonda igual a g_c·g_a/‖g_c‖ (tolerância numérica) |

A I7 é a mais importante: se ela falhar, o braço com decoder é só um BERT com uma cabeça a mais que não toca nele, e
qualquer resultado não mede o método.

O teste de fumaça da D6 (BERT minúsculo de verdade + `bridge` + T5 base de verdade) **não entra no pytest**, porque
baixa ~900 MB do T5. Ele vira o comando `--fumaca`, rodado uma vez no notebook antes de ir para o PC.

---

## Decisões (E1–E8 aceitas pelo Pedro em 09/11, todas na recomendação)

A tabela ficou como foi proposta. O Pedro aceitou as oito recomendações em 09/11 e pediu as medidas de gradiente da
seção acima.

| # | Decisão | Opções | Recomendação do Claude |
|---|---|---|---|
| E1 | Como o aquecimento da Tabela 4 convive com a fase B | (a) um fator por grupo, como acima · (b) multiplicar os dois no BERT · (c) só o da fase B para todos | **(a)**: cada aquecimento vale para a parte de que o paper fala |
| E2 | Taxa do decoder na fase A | constante 5e-5 · com aquecimento próprio | **constante**: o decoder já é pré-treinado, e a fase A tem só 39 passos |
| E3 | Passar o `[CLS]` ao decoder ("Ignore CLS", §4.4) | passa · não passa · as duas | **passa**: a Tabela 3 não dá vantagem a nenhuma; "as duas" dobra a grade |
| E4 | Pares do braço BERT sozinho | os mesmos 2.470 · os 2.490 | **2.470**: o único jeito de os braços diferirem só no decoder |
| E5 | Limpeza C (ver `analise-lote-FA.md`: em 96 dos 450 cortes a frase fica sem sujeito) | estreitar a regra · tirar a C · deixar como está | **estreitar**: cortar só quando o resto é frase inteira; o resto fica com "The text" |
| E6 | Onde vive o teste da D6 | pytest com modelos minúsculos aleatórios + `--fumaca` manual · tudo no pytest | **o primeiro**: CI sem rede, e a D6 continua sendo feita |
| E7 | Dropout da cabeça | 0,1 (padrão do BERT) · nenhum | **0,1**, declarado (o paper não diz) |
| E8 | Salvar pesos | não salvar · salvar o melhor · salvar todos | **não salvar**: o resultado é o CSV, e o HF Hub fica para quando houver um modelo para mostrar |

Ordem de escrita: branch `feat/treino-rte`, `rte_dados.py` + testes I1–I3, I9, I11 e I13, `rte_modelo.py` + I4,
I7 e I8, `rte_treino.py` + I5, I6, I10, I12, I14 e I15 (a medida de gradiente fica num `rte_gradientes.py` próprio, chamado
pelo laço), `--fumaca` no notebook, e então a grade no PC.
