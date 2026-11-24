# Manual do Treino

Este manual explica, passo a passo, o código de treino que replica o método de Agrawal, Ahemad & Sembium (2025) no conjunto RTE: um classificador BERT que, durante o treino, carrega um decoder do T5 como cabeça auxiliar. O decoder escreve uma justificativa gerada por um LLM (o Qwen) e é descartado na avaliação.

## Antes de começar

Ao fim deste manual você vai ter montado:

- os dados de treino: os pares do RTE unidos às justificativas, limpos e tokenizados com dois tokenizadores;
- o modelo: BERT + cabeça de classificação + decoder do T5 opcional;
- o laço de treino com três fases (A, B e C), o otimizador em grupos, o agendamento da taxa e a avaliação no dev;
- duas medidas de gradiente que rodam durante o treino, uma por grupo de palavras e outra por palavra;
- os testes que provam que cada peça faz o que este manual diz.

O código fica em quatro arquivos de `src/radibert/`:

- `rte_dados.py`: do parquet ao lote;
- `rte_modelo.py`: as classes do modelo;
- `rte_treino.py`: o laço, a avaliação, os arquivos de resultado e a linha de comando;
- `rte_gradientes.py`: as medidas de gradiente.

Os testes ficam em `tests/test_rte_treino.py`.

Três avisos valem para o manual inteiro:

1. Os trechos de código são os que estão hoje nos arquivos. Alguns deles carregam variantes de outros experimentos (marcas de atenção, encoder do T5 no lugar do BERT, controle de calendário). Este manual não trata dessas variantes. Quando uma delas aparecer num trecho, o texto avisa e você pode pular.
2. O que vem do paper cita a seção ou a tabela. O que o paper não diz está marcado como escolha deste código ou como leitura do paper.
3. Contas de memória e de tempo são estimativas, e o texto diz quando ainda não foram medidas.

## Passo 1. Entenda a ideia em uma imagem

Você vai treinar um BERT para classificar pares (premissa, hipótese). Durante o treino, um decoder do T5 lê os vetores do BERT e tenta escrever a justificativa do rótulo. O erro do decoder volta até o BERT e o empurra.

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

Leia a figura assim:

1. Você passa o par pelo BERT e recebe `h`, um vetor de 768 números para cada token.
2. Pelo lado esquerdo, você pega só o vetor do `[CLS]` e entrega à cabeça de classificação, uma camada linear de 768 para 1. O erro dela é a `L_cls`.
3. Pelo lado direito, você entrega `h` inteiro ao decoder do T5, que lê esses vetores por cross-attention e prevê a justificativa, token a token. O erro dele é a `L_aux`.
4. Na fase C você soma as duas: `L = L_cls + 0,1 x L_aux`. Nas fases A e B só a `L_aux` treina.

Na avaliação só existe o lado esquerdo. O decoder serve apenas para empurrar o BERT durante o treino.

## Passo 2. Conheça os arquivos e instale as dependências

São quatro módulos em `src/radibert/` e um arquivo de teste. Cada módulo tem uma responsabilidade:

| Arquivo | Faz | Não faz |
|---|---|---|
| `rte_dados.py` | junta o parquet do RTE com o CSV das justificativas, aplica a limpeza da abertura, tira os 20 exemplos do prompt, tokeniza com os dois tokenizadores, monta os lotes | não sabe nada de modelo |
| `rte_modelo.py` | a classe `RationaleBert` (BERT + cabeça + decoder opcional) e a função que monta o classificador só com BERT + cabeça para avaliar | não sabe nada de fases nem de taxa |
| `rte_treino.py` | o laço com as fases A/B/C, o otimizador, o agendamento da taxa, a avaliação no dev e o CSV de resultados; linha de comando | não monta modelo nem lê arquivo de dado diretamente |
| `rte_gradientes.py` | calcula as palavras de rótulo, põe cada token do alvo num grupo (S, F, C ou N) e mede os gradientes `g_c` e os de cada grupo no lote de sonda (Passos 19 a 25) | não muda nenhum peso |
| `tests/test_rte_treino.py` | os testes do Passo 27, em modelos minúsculos com pesos aleatórios (rodam na CPU, sem baixar nada) | não mede qualidade |

Dependências que você vai instalar:

- `torch==2.14.1`. Na máquina com GPU, a roda é a `cu130`, pelo índice do PyTorch, declarada no `pyproject.toml` com `[tool.uv.sources]`.
- `transformers==5.20.2`. A versão mais nova (5.22.2) foi preterida por ter só 3 dias quando a escolha foi feita.
- O `scikit-learn`, que já está no projeto, calcula ROC-AUC e F1.

Um cuidado na instalação: o `requirements.txt` gerado pelo `uv export` lista `torch==2.14.1+cu130`, mas não o índice do PyTorch. Se você instalar com `pip`, precisa de `--extra-index-url https://download.pytorch.org/whl/cu130`. Com `uv sync` não há problema.

As configurações que este manual usa: `google-t5/t5-base` tem d_model 768, `google-bert/bert-base-uncased` tem 768 e `google/bert_uncased_L-2_H-128_A-2` tem 128.

## Passo 3. Junte os pares às justificativas (`rte_dados.py`)

### O que entra

Você vai precisar de três coisas:

- `dados/rte/rte_train.parquet` (2.490 pares) e `dados/rte/rte_validation.parquet` (277 pares);
- o CSV das justificativas geradas pelo Qwen, `racionalizacoes-FA.csv` (2.470 justificativas, uma por `idx`);
- os 20 `idx` dos exemplos que foram dentro do prompt de geração, lidos por `rte_racionalizacoes.rte_examples()`, a mesma função que montou o prompt.

### Onde entram a limpeza e os 20 exemplos

```python
def read_rte(split: str) -> pd.DataFrame:
    pairs = pd.read_parquet(RTE / f"rte_{split}.parquet")
    pairs["y"] = (pairs["label"] == ENTAILMENT).astype(int)
    return pairs


def training_pairs() -> pd.DataFrame:
    """The 2,470 train pairs with an FA rationale, cleaned by C: the same set for both arms (E4)."""
    fa = pd.read_csv(FA_CSV, usecols=["idx", "qwen"])
    pairs = read_rte("train").merge(fa, on="idx", how="inner")
    pairs["rationale"] = pairs["qwen"].map(clean_opening)
    return pairs.drop(columns="qwen").sort_values("idx").reset_index(drop=True)
```

Siga o trecho assim:

1. Em `read_rte` você lê o parquet do split e cria a coluna `y`. O GLUE codifica `entailment` como 0 (a constante `ENTAILMENT`), então `y` vale 1 quando o rótulo é `entailment`.
2. Em `training_pairs` você lê do CSV só as colunas `idx` e `qwen`.
3. Você une os 2.490 pares do treino ao CSV por `idx`, com junção interna. Os 20 exemplos do prompt não têm linha no CSV, então saem aqui.
4. Você passa o texto do Qwen por `clean_opening`, que tira a abertura repetida, e guarda o resultado em `rationale`.
5. Você descarta a coluna `qwen`, ordena por `idx` e devolve 2.470 linhas, as mesmas para os dois braços do experimento.

Três escolhas estão nesse trecho:

1. A limpeza acontece na montagem, nunca no CSV. O texto original do Qwen fica guardado. Se a limpeza mudar, basta rodar o treino de novo.
2. Os 20 exemplos saem dos dois braços. Isso é escolha deste código, não do paper. Eles não têm justificativa do Qwen, porque estavam dentro do prompt. As justificativas deles foram rascunhadas por outro modelo, cuja política de uso proíbe usar a saída como alvo de treino. Tirar os 20 só do braço com decoder faria os braços treinarem em conjuntos diferentes. Por isso o BERT sozinho também treina nos 2.470.
3. A classe positiva é `entailment` (y = 1). Como o GLUE codifica `entailment` como 0, a conversão tem teste próprio. As métricas do paper (ROC-AUC, precisão e revocação a 0,7) dependem de qual classe é a positiva. No paper a positiva é "relevante", a que a justificativa defende.

O dev sai de `dev_pairs()`, que lê o split de validação com o mesmo `read_rte`.

## Passo 4. Tokenize com os dois tokenizadores e monte os lotes

Você precisa de dois tokenizadores porque o par entra no BERT e a justificativa é alvo do T5. Os limites ficam em constantes:

```python
MAX_INPUT_TOKENS = 512  # BERT's limit; the longest RTE pair is ~320 (analise-lote-FA.md), so nothing is cut (I9)
MAX_TARGET_TOKENS = 64  # the longest rationale has 34 words
IGNORED = -100  # label value the T5 cross-entropy skips
ENTAILMENT = 0  # GLUE RTE ClassLabel
```

Os tokenizadores e a tokenização:

```python
@dataclass(frozen=True)
class Tokenizers:
    bert: object
    t5: object


def load_tokenizers(bert_name: str = BERT) -> Tokenizers:
    return Tokenizers(AutoTokenizer.from_pretrained(bert_name), AutoTokenizer.from_pretrained(T5))


def encode(pairs: pd.DataFrame, tok: Tokenizers) -> list[dict]:
    """One dict of token ids per pair; `labels` (the T5 target) only when the pairs carry a rationale."""
    enc = tok.bert(list(pairs["sentence1"]), list(pairs["sentence2"]), truncation="only_first",
                   max_length=MAX_INPUT_TOKENS)
    # the T5 tokenizer (T5-encoder arms) joins the pair with </s> and has no segment ids: zeros, never read by T5
    types = enc["token_type_ids"] if "token_type_ids" in enc else [[0] * len(ids) for ids in enc["input_ids"]]
    items = [{"idx": int(idx), "y": int(y), "input_ids": ids, "token_type_ids": tt}
             for idx, y, ids, tt in zip(pairs["idx"], pairs["y"], enc["input_ids"], types)]
    if "rationale" in pairs:
        targets = tok.t5(list(pairs["rationale"]), truncation=True, max_length=MAX_TARGET_TOKENS)["input_ids"]
        for item, target in zip(items, targets):
            item["labels"] = target
    return items
```

Siga o trecho assim:

1. Em `load_tokenizers` você carrega o tokenizador do BERT (`google-bert/bert-base-uncased`) e o do T5 (`google-t5/t5-base`) e os guarda juntos.
2. Em `encode` você tokeniza premissa e hipótese juntas com o tokenizador do BERT. O resultado tem a forma `[CLS] premissa [SEP] hipótese [SEP]`. O teto é de 512 tokens, e se fosse preciso cortar, só a premissa seria cortada (`truncation="only_first"`).
3. Você monta um dicionário por par, com `idx`, `y`, `input_ids` e `token_type_ids`. A linha que cria `types` com zeros só serve à variante com encoder do T5, que este manual não trata.
4. Se os pares têm a coluna `rationale`, você tokeniza a justificativa com o tokenizador do T5, com teto de 64 tokens. O alvo termina com `</s>` (id 1). Ele entra no dicionário como `labels`. O dev não tem justificativa, então sai sem `labels`.

O que você precisa saber sobre os tamanhos:

- A entrada mais longa do RTE tem cerca de 320 tokens (estimativa por palavras). Com o teto de 512 nada é cortado, e um teste confirma isso com o tokenizador de verdade.
- A justificativa mais longa tem 34 palavras, uns 50 tokens do T5. O teto de 64 também não corta nada.

A regra de que nada pode ser cortado é conferida toda vez que os dados são carregados. A primeira função abaixo está em `rte_dados.py` e conta quantas entradas e quantos alvos passariam do teto. A segunda está em `rte_treino.py` e recusa a rodada se alguma contagem não for zero.

```python
def overlong_counts(pairs: pd.DataFrame, tok: Tokenizers) -> dict:
    """How many inputs and targets the truncation would cut (I9: both must be 0)."""
    inputs = tok.bert(list(pairs["sentence1"]), list(pairs["sentence2"]))["input_ids"]
    counts = {"inputs_cut": sum(len(ids) > MAX_INPUT_TOKENS for ids in inputs)}
    if "rationale" in pairs:
        targets = tok.t5(list(pairs["rationale"]))["input_ids"]
        counts["targets_cut"] = sum(len(ids) > MAX_TARGET_TOKENS for ids in targets)
    return counts
```

```python
def refuse_cut_text(cut: dict):
    """I9: nothing may be truncated, in inputs or targets."""
    if any(cut.values()):
        raise ValueError(f"truncation would cut text {cut}: raise MAX_INPUT_TOKENS/MAX_TARGET_TOKENS in rte_dados.py")
```

Agora monte os lotes:

```python
def pad(rows: list[list[int]], value: int) -> torch.Tensor:
    width = max(map(len, rows))
    return torch.tensor([row + [value] * (width - len(row)) for row in rows])


def collate(items: list[dict]) -> dict:
    """Pads each batch to its own longest pair (BERT pad id is 0) and the targets with IGNORED."""
    batch = {"idx": torch.tensor([it["idx"] for it in items]),
             "y": torch.tensor([it["y"] for it in items], dtype=torch.float),
             "input_ids": pad([it["input_ids"] for it in items], 0),
             "token_type_ids": pad([it["token_type_ids"] for it in items], 0),
             "attention_mask": pad([[1] * len(it["input_ids"]) for it in items], 0)}
    if "labels" in items[0]:
        batch["labels"] = pad([it["labels"] for it in items], IGNORED)
    if "marks" in items[0]:  # rte_marcas: 1 on the input positions the [CLS] attention is pulled to
        batch["marks"] = pad([it["marks"] for it in items], 0)
    return batch
```

1. Você completa cada lote até o par mais longo daquele lote, não até 512. É o preenchimento por lote (dynamic padding). A mediana é de cerca de 56 tokens, então os lotes ficam curtos e rápidos.
2. Nas entradas, o preenchimento é 0 (o id de preenchimento do BERT), e a `attention_mask` marca com 1 só os tokens de verdade.
3. No alvo, as posições de preenchimento viram `-100`. É o valor que a entropia cruzada do T5 ignora (conferido na linha 1051 do `modeling_t5.py`, na versão 5.20.2 do `transformers`).
4. O `collate` devolve um dicionário com `idx`, `y`, `input_ids`, `token_type_ids`, `attention_mask` e, quando há justificativa, `labels`. A chave `marks` pertence a outro experimento e não aparece aqui.

O `collate` não carrega os grupos de palavras das medidas de gradiente. O lote de sonda monta os seus em `build_probe` (Passo 24). A perda do treino nunca vê grupo.

## Passo 5. Monte o modelo (`rte_modelo.py`)

### Como o encoder e a cabeça são lidos

Antes da classe, veja as funções que passam o par pelo encoder e leem a cabeça. O treino e a avaliação chamam a mesma função `classify`, então o classificador avaliado é o mesmo que treinou.

```python
HEAD_DROPOUT = 0.1  # E7: BERT's own default; the paper does not say


def is_t5(encoder: nn.Module) -> bool:
    return encoder.config.model_type == "t5"


def run_encoder(bert: nn.Module, batch: dict, output_attentions: bool = False):
    extra = {} if is_t5(bert) else {"token_type_ids": batch["token_type_ids"]}
    return bert(input_ids=batch["input_ids"], attention_mask=batch["attention_mask"],
                output_attentions=output_attentions, **extra)


def classify(bert: nn.Module, head: nn.Module, batch: dict) -> tuple[torch.Tensor, torch.Tensor]:
    """Encoder vectors of every token, and the logits from the [CLS] vector (BERT) or the mean of the real tokens
    (T5): one logit per pair for two labels, one per label otherwise. Training and evaluation both call this, so the
    classifier evaluated is the one trained."""
    h = run_encoder(bert, batch).last_hidden_state
    return h, logits_of(bert, head, h, batch["attention_mask"])


def logits_of(bert: nn.Module, head: nn.Module, h: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    """The head runs in fp32 even under bf16 autocast: with 8 mantissa bits, 277 dev probabilities would tie and
    coarsen ROC-AUC (audit 09/11)."""
    with torch.autocast(h.device.type, enabled=False):
        if is_t5(bert):
            m = mask.unsqueeze(-1).float()
            pooled = (h.float() * m).sum(1) / m.sum(1)
        else:
            pooled = h[:, 0].float()
        logits = head(pooled)
        return logits.squeeze(-1) if logits.shape[-1] == 1 else logits
```

1. Em `run_encoder` você passa `input_ids`, `attention_mask` e `token_type_ids` pelo BERT.
2. Em `classify` você pega `last_hidden_state`, que é `h`, um vetor por token, e chama `logits_of`.
3. Em `logits_of` você pega o vetor do `[CLS]` (`h[:, 0]`), passa pela cabeça e recebe um logit por par: o logit de `entailment`.
4. A cabeça roda em fp32 mesmo quando o resto roda em bf16. Com 8 bits de mantissa, as 277 probabilidades do dev empatariam e o ROC-AUC ficaria grosso.
5. Os ramos com `is_t5` servem à variante com encoder do T5, fora deste manual.

### A classe `RationaleBert`

```python
class RationaleBert(nn.Module):
    def __init__(self, bert: nn.Module, t5: T5ForConditionalGeneration | None, n_labels: int = 2):
        super().__init__()
        hidden = bert.config.d_model if is_t5(bert) else bert.config.hidden_size
        self.bert = bert
        self.head = nn.Sequential(nn.Dropout(HEAD_DROPOUT), nn.Linear(hidden, 1 if n_labels == 2 else n_labels))
        self.t5 = t5
        self.mark_attention = False
        self.token_head = None  # with_token_head: one logit per input position, trained on the marks
        self.decoder_calendar = False  # no decoder, but the decoder arm's schedule (rte_treino, arm bert_calendar)
        self.bridge = None
        if t5 is not None:
            if not self.shares_t5_encoder:
                freeze_t5_encoder(t5)
            if hidden != t5.config.d_model:  # smaller encoders (small 512, tiny 128) and the CPU smoke test
                self.bridge = nn.Linear(hidden, t5.config.d_model)

    @property
    def shares_t5_encoder(self) -> bool:
        """True in the T5-encoder arm with decoder: the classifier's encoder is the T5's own, and it trains."""
        return self.t5 is not None and self.bert is self.t5.encoder

    @classmethod
    def from_pretrained(cls, bert_name: str, t5_name: str | None, n_labels: int = 2) -> "RationaleBert":
        bert = AutoModel.from_pretrained(bert_name, add_pooling_layer=False)  # the head reads [CLS] directly
        t5 = T5ForConditionalGeneration.from_pretrained(t5_name) if t5_name else None
        return cls(bert, t5, n_labels)

    @classmethod
    def with_mark_attention(cls, bert_name: str, n_labels: int = 2) -> "RationaleBert":
        """No decoder; the auxiliary loss is mark_loss on the last layer's [CLS] attention when the batch carries
        `marks` (rte_marcas). Eager attention: the default implementation does not return the probabilities."""
        model = cls(AutoModel.from_pretrained(bert_name, add_pooling_layer=False, attn_implementation="eager"), None,
                    n_labels)
        model.mark_attention = True
        return model

    @classmethod
    def with_token_head(cls, bert_name: str, n_labels: int = 2) -> "RationaleBert":
        """No decoder and no attention loss; a linear layer on each token's last vector learns the marks directly
        (token_mark_loss). The reference for the highlight read off the [CLS] attention (10/11)."""
        model = cls(AutoModel.from_pretrained(bert_name, add_pooling_layer=False), None, n_labels)
        model.token_head = nn.Linear(model.bert.config.hidden_size, 1)
        return model

    def token_logits(self, h: torch.Tensor) -> torch.Tensor:
        with torch.autocast(h.device.type, enabled=False):
            return self.token_head(h.float()).squeeze(-1)

    @classmethod
    def from_t5(cls, t5_name: str, with_decoder: bool, n_labels: int = 2) -> "RationaleBert":
        """T5 encoder as the classifier's encoder; with the decoder, both from the same checkpoint."""
        if with_decoder:
            t5 = T5ForConditionalGeneration.from_pretrained(t5_name)
            return cls(t5.encoder, t5, n_labels)
        return cls(T5EncoderModel.from_pretrained(t5_name), None, n_labels)

    def encode(self, batch: dict) -> tuple[torch.Tensor, torch.Tensor]:
        return classify(self.bert, self.head, batch)

    def decode(self, h: torch.Tensor, batch: dict):
        """T5 decoder over the encoder vectors, teacher-forced on the rationale; `.loss` is L_aux."""
        memory = self.bridge(h) if self.bridge is not None else h
        return self.t5(encoder_outputs=(memory,), attention_mask=batch["attention_mask"], labels=batch["labels"])

    def forward(self, batch: dict) -> tuple[torch.Tensor, torch.Tensor | None]:
        """Logits and the auxiliary loss: L_aux of the decoder, the mark loss (attention or token head), or None."""
        if self.token_head is not None:
            h, logit = self.encode(batch)
            if "marks" not in batch:
                return logit, None
            return logit, token_mark_loss(self.token_logits(h), batch["marks"], batch["attention_mask"])
        if self.mark_attention:
            out = run_encoder(self.bert, batch, output_attentions="marks" in batch)
            logit = logits_of(self.bert, self.head, out.last_hidden_state, batch["attention_mask"])
            return logit, (mark_loss(out.attentions[-1], batch["marks"]) if "marks" in batch else None)
        h, logit = self.encode(batch)
        return logit, (self.decode(h, batch).loss if self.t5 is not None else None)


def freeze_t5_encoder(t5: T5ForConditionalGeneration):
    """Freezes the encoder blocks only: its embedding is the `shared` matrix the decoder and lm_head also use."""
    t5.encoder.block.requires_grad_(False)
    t5.encoder.final_layer_norm.requires_grad_(False)
```

Para este manual, siga quatro partes da classe: o construtor, `from_pretrained`, `encode`/`decode` e as duas últimas linhas do `forward`. Os métodos `with_mark_attention`, `with_token_head`, `token_logits` e `from_t5`, e os atributos `mark_attention`, `token_head` e `decoder_calendar`, pertencem a outros experimentos.

1. Em `from_pretrained` você carrega o BERT sem o pooler (`add_pooling_layer=False`). A cabeça lê o `[CLS]` direto, e um pooler sem uso deixaria pesos sem gradiente nas medidas. Se o braço tem decoder, você carrega também o `T5ForConditionalGeneration`.
2. No construtor você cria a cabeça: dropout de 0,1 seguido de uma camada linear que devolve 1 logit. O paper não diz o dropout da cabeça; 0,1 é o padrão do BERT e fica declarado.
3. Ainda no construtor, se há decoder, você congela os blocos do encoder do T5 com `freeze_t5_encoder`. Só os blocos são congelados: o embedding do encoder é a matriz `shared`, que o decoder e o `lm_head` também usam.
4. Em `encode` você chama `classify` e recebe `h` e o logit.
5. Em `decode` você entrega `h` ao T5 e recebe a saída dele, cujo `.loss` é a `L_aux`.
6. No `forward`, as duas últimas linhas fazem o caminho deste manual: `encode`, depois `decode` se existe decoder. O resultado é o logit e a `L_aux`, ou o logit e `None` no braço sem decoder.

O que cada parte de `decode` faz, e por que funciona:

- `encoder_outputs=(memory,)` é o ponto central. O `T5ForConditionalGeneration` só roda o encoder do próprio T5 quando `encoder_outputs` vem vazio (linha 1009 do `modeling_t5.py`). Passando os vetores do BERT ali, o decoder do T5 lê o BERT como se ele fosse o encoder do T5. Você não precisa reescrever o decoder.
- `attention_mask=batch["attention_mask"]` vira a máscara da cross-attention (linha 1037, `encoder_attention_mask=attention_mask`). Assim o decoder não lê as posições de preenchimento do BERT.
- `labels=...`: o T5 desloca o alvo uma posição para a direita sozinho (`_shift_right`, com o token inicial 0). Isso é o teacher forcing: em cada posição o decoder recebe os tokens certos anteriores e prevê o seguinte. O T5 também calcula a entropia cruzada média por token ignorando os `-100`. Esse número é a `L_aux`.
- O gradiente da `L_aux` chega ao BERT porque `h` sai do BERT sem `detach`. É o mecanismo inteiro do método, e por isso há um teste exatamente para isso (Passo 27).
- O encoder do T5 continua carregado mas nunca roda: são cerca de 85M de pesos parados, cerca de 340 MB. Ele fica congelado e fora do otimizador. Arrancar o encoder do objeto pouparia esses 340 MB, mas a geração e outros métodos da biblioteca contam com ele. No código de hoje, a função `place` de `rte_treino.py` deixa esses blocos na CPU.
- `bridge` é um adaptador linear que leva o vetor do encoder ao tamanho que o T5 espera (por exemplo, 128 -> 768). Ele só existe quando o encoder não tem vetor de 768, como no teste de fumaça com o BERT minúsculo. Um teste garante que ele não existe na rodada com o BERT base.
- "Ignore CLS" (seção 4.4 de Agrawal, Ahemad & Sembium (2025)): este código passa todos os vetores ao decoder, inclusive o do `[CLS]`. Na Tabela 3 do paper as duas formas trocam de lugar, então nenhuma tem vantagem clara.

## Passo 6. Separe o classificador para avaliar (`classifier_only`)

```python
class Classifier(nn.Module):
    """What evaluation sees: a copy of the encoder and the head, with no decoder in the object (I8)."""

    def __init__(self, bert: nn.Module, head: nn.Module):
        super().__init__()
        self.bert, self.head = bert, head

    def forward(self, batch: dict) -> torch.Tensor:
        return classify(self.bert, self.head, batch)[1]


def classifier_only(model: RationaleBert) -> Classifier:
    return Classifier(copy.deepcopy(model.bert), copy.deepcopy(model.head))
```

1. Quando o treino termina, você chama `classifier_only(model)`.
2. Ela copia o encoder e a cabeça para um objeto `Classifier`. O decoder não existe nesse objeto.
3. A avaliação recebe esse objeto, nunca o `RationaleBert`. Assim é impossível o decoder ajudar na nota do dev.

Um teste confere que nenhuma chave do `state_dict` dele começa com `t5.` ou `bridge.`.

## Passo 7. Confira o tamanho e a memória

As contas abaixo são estimativas feitas antes de rodar.

| Parte | Parâmetros treináveis |
|---|---|
| BERT base | 110M |
| Decoder do T5 base (12 blocos x ~9,4M) | ~113M |
| Embeddings do T5 (`shared`, 32.128 x 768, também usados pelo `lm_head`) | ~25M |
| Cabeça | 769 |
| Total | ~248M |

1. Com AdamW em fp32 você gasta cerca de 16 bytes por parâmetro: cerca de 4,0 GB, mais cerca de 0,3 GB do encoder parado.
2. As sequências do RTE são curtas (mediana de cerca de 56 tokens), então a estimativa era que o lote de 32 em bf16 coubesse nos 8 GB sem acumulação.
3. A saída prevista, se estourasse, era lote 16 x 2. É o que o código faz hoje: o comentário da constante `MICRO_BATCH` registra que o lote de 32 de uma vez transbordou a memória da placa para a memória compartilhada do sistema. O Passo 10 mostra a divisão.

## Passo 8. Faça as contas de passo (`rte_treino.py`)

Os hiperparâmetros ficam em constantes no topo de `rte_treino.py`:

```python
# Table 4 of the paper
LR = 5e-5
BATCH_SIZE, EPOCHS = 32, 8
COPY_WARMUP_STEPS = 500
DECODER_WEIGHT_DECAY = 0.001  # 0 on the encoder; 0 on the head (the paper does not say)
ADAM_EPS, ADAM_BETAS = 1e-8, (0.9, 0.999)
CLIP_NORM = 1.0
# §4.3-4.4 of the paper and the decisions D2/D3
AUX_WEIGHT = 0.1
PHASE_B_SHARE = 0.3
PROPORTIONAL_WARMUP_SHARE = 0.1
# Evaluation (D4)
PRECISION_RECALL_THRESHOLD = 0.7
# Gradient measures
MEASURE_EVERY = 25
# Memory and logging (09/11: batch 32 at once spilled the 5060's VRAM into shared system memory)
MICRO_BATCH = 16
PROGRESS_EVERY = 100
```

Com os 2.470 pares, as contas são estas:

| Quantidade | Conta | Valor |
|---|---|---|
| Passos por época | teto de 2.470 / 32 | 78 (o último lote tem 6 pares) |
| Treino total (8 épocas, Tabela 4) | 78 x 8 | 624 |
| Fase A (uma passada por metade dos pares) | teto de 1.235 / 32 | 39, fora dos 624 |
| Fase B (30% do treino) | piso de 0,3 x 624 | passos 1 a 187 |
| Fase C | o resto | passos 188 a 624 |
| Aquecimento da taxa, cópia fiel | Tabela 4 | 500 passos |
| Aquecimento da taxa, proporcional | piso de 0,1 x 624 | 62 passos |

Com os 2.490 pares a conta daria 623 passos. Com os 20 exemplos fora são 624.

No código, quem faz essas contas é `make_plan`:

```python
@dataclass(frozen=True)
class Plan:
    per_epoch: int
    total: int
    phase_a: int
    phase_b: int
    warmup_steps: int  # not "warmup": the results row already has the run's warmup kind ("500"/"prop")


def make_plan(n_pairs: int, warmup: str, batch_size: int = BATCH_SIZE, epochs: int = EPOCHS) -> Plan:
    per_epoch = math.ceil(n_pairs / batch_size)
    total = per_epoch * epochs
    warmup_steps = COPY_WARMUP_STEPS if warmup == "500" else int(PROPORTIONAL_WARMUP_SHARE * total)
    return Plan(per_epoch, total, math.ceil((n_pairs // 2) / batch_size), int(PHASE_B_SHARE * total), warmup_steps)
```

1. Você chama `make_plan` com o número de pares e o tipo de aquecimento (`"500"` ou `"prop"`).
2. Ela devolve um `Plan` com os passos por época, o total, os passos da fase A, o último passo da fase B e os passos de aquecimento.
3. O campo se chama `warmup_steps`, e não `warmup`, porque a linha de resultados já tem uma coluna `warmup` com o tipo de aquecimento da rodada ("500" ou "prop"). Com o mesmo nome, um sobrescrevia o outro no CSV. Isso foi achado pelo teste de fumaça e ganhou teste.

## Passo 9. Escreva o laço de treino

### A perda de cada fase

```python
def cls_loss(logits: torch.Tensor, y: torch.Tensor, reduction: str = "mean") -> torch.Tensor:
    """L_cls: binary cross-entropy on the single logit (RTE), cross-entropy over the labels otherwise (e-SNLI)."""
    if logits.dim() == 1:
        return F.binary_cross_entropy_with_logits(logits, y.float(), reduction=reduction)
    return F.cross_entropy(logits, y.long(), reduction=reduction)
```

```python
def training_loss(step: int, plan: Plan, l_cls: torch.Tensor, l_aux: torch.Tensor | None) -> torch.Tensor:
    if l_aux is None:
        return l_cls
    if step <= plan.phase_b:
        return l_aux  # phase B: the head learns nothing here
    return l_cls + AUX_WEIGHT * l_aux  # phase C (§4.3)
```

1. A `L_cls` é a entropia cruzada binária sobre o logit único. O ramo com mais de um logit serve a outra tarefa, fora deste manual.
2. No braço BERT sozinho não existe `L_aux`, então a perda é a `L_cls`.
3. No braço com decoder, até o passo 187 (fase B) a perda é só a `L_aux`. A cabeça não aprende nada aqui.
4. Do passo 188 em diante (fase C) a perda é `L_cls + 0,1 x L_aux` (seção 4.3 do paper).

### As peças pequenas

```python
def autocast(device: torch.device):
    if device.type == "cuda":
        return torch.autocast("cuda", dtype=torch.bfloat16)
    return contextlib.nullcontext()


def to_device(batch: dict, device: torch.device) -> dict:
    return {k: v.to(device) for k, v in batch.items()}


def place(model: RationaleBert, device: torch.device) -> RationaleBert:
    """Moves the model to the device but keeps the T5 encoder blocks, frozen and never run, on the CPU (~340 MB);
    in the T5-encoder arm they are the classifier's encoder and stay on the device."""
    model.to(device)
    if model.t5 is not None and not model.shares_t5_encoder:
        model.t5.encoder.block.to("cpu")
        model.t5.encoder.final_layer_norm.to("cpu")
    return model


def make_optimizer(model: RationaleBert) -> torch.optim.Optimizer:
    return torch.optim.AdamW(param_groups(model), lr=LR, eps=ADAM_EPS, betas=ADAM_BETAS)


def finish_step(model: RationaleBert, opt: torch.optim.Optimizer):
    torch.nn.utils.clip_grad_norm_(model.parameters(), CLIP_NORM)
    opt.step()
    opt.zero_grad()
```

1. `autocast` liga o bf16 só em GPU. Na CPU não faz nada.
2. `place` leva o modelo para o dispositivo e deixa na CPU os blocos do encoder do T5, que estão congelados e nunca rodam.
3. `make_optimizer` cria o AdamW com taxa 5e-5, eps 1e-8 e betas (0.9, 0.999), sobre os grupos do Passo 11.
4. `finish_step` fecha um passo: corta a norma do gradiente em 1,0, dá o passo do otimizador e zera os gradientes.

### O laço

```python
def train(model: RationaleBert, plan: Plan, items: list[dict], seed: int, device: torch.device,
          batch_size: int = BATCH_SIZE, probes: Probes | None = None, micro: int = MICRO_BATCH) -> TrainLog:
    """Trains in place. `micro` splits each batch (and each probe) without changing the gradient (I16). Same seed, same batch order in both arms (the loader has its own generator). Same seed, same
    weights on CPU (I10); on CUDA the embedding backward uses atomic adds, so reruns differ slightly."""
    place(model, device).train()
    opt = make_optimizer(model)
    log = TrainLog()
    start = time.perf_counter()
    if model.t5 is not None:
        log.phase_a_steps = run_phase_a(model, opt, items, seed, batch_size, device, micro)
        if log.phase_a_steps != plan.phase_a:
            raise RuntimeError(f"phase A ran {log.phase_a_steps} steps, the plan says {plan.phase_a}")
    sched = LambdaLR(opt, lr_factors(model, plan))  # created after phase A: its constant 5e-5 is the base rate
    loader = DataLoader(items, batch_size=batch_size, shuffle=True, collate_fn=dados.collate,
                        generator=torch.Generator().manual_seed(seed))
    step = 0
    for epoch in range(plan.total // plan.per_epoch):
        for batch in loader:
            step += 1
            if model.decoder_calendar and step <= plan.phase_b:
                sched.step()  # calendar control: the classifier gets no step in phase B, as in the decoder arm
                continue
            batch = to_device(batch, device)
            combine = marked_loss if uses_marks(model) else functools.partial(training_loss, step, plan)
            _, l_aux = accumulated_backward(model, batch, combine, micro)
            finish_step(model, opt)
            sched.step()
            if l_aux is not None and epoch == plan.total // plan.per_epoch - 1:
                log.last_epoch_aux.append(l_aux)
            if model.t5 is not None:
                measure(model, probes, plan, step, log, device, micro)
            if step % PROGRESS_EVERY == 0:  # so the watchdog can tell slow from stuck
                print(f"  passo {step}/{plan.total} ({time.perf_counter() - start:.0f} s)", flush=True)
    return log
```

Siga o laço assim:

1. Você leva o modelo ao dispositivo, põe em modo de treino e cria o otimizador.
2. Se o modelo tem decoder, você roda a fase A (Passo 12). São 39 passos. Se o número de passos não bater com o plano, o código para com erro.
3. Só depois da fase A você cria o agendamento da taxa (Passo 13). A fase A usa a taxa constante de 5e-5 e fica fora do relógio dos 624 passos.
4. Você cria o carregador de lotes com embaralhamento e um gerador próprio com a semente da rodada. Assim a mesma semente dá a mesma ordem de lotes nos dois braços.
5. Para cada lote das 8 épocas, você soma 1 ao passo, leva o lote ao dispositivo e escolhe a perda da fase com `training_loss`.
6. Você chama `accumulated_backward` (Passo 10), que faz a passada para frente e o `backward` do lote e devolve a `L_cls` e a `L_aux` dele.
7. Você fecha o passo com `finish_step` e avança o agendamento com `sched.step()`.
8. Na última época, você guarda a `L_aux` de cada lote. A média delas vai para a linha de resultados como a `L_aux` final.
9. Se há decoder, você chama `measure`, que roda as medidas de gradiente nos passos certos (Passos 19 a 26).
10. A cada 100 passos você imprime o progresso, para dar para distinguir lento de travado.

O trecho com `decoder_calendar` e a escolha `marked_loss` pertencem a outros experimentos.

A mesma semente reproduz os mesmos pesos só na CPU. Na GPU, o `backward` do embedding usa somas atômicas e as rodadas variam um pouco.

## Passo 10. Divida cada lote em micro-lotes

O lote de 32 pares de uma vez não coube com folga na memória da placa de 8 GB. Por isso você faz o `backward` do lote em duas metades de 16.

```python
def target_tokens(batch: dict) -> int:
    return int((batch["labels"] != dados.IGNORED).sum())


def aux_units(batch: dict) -> int:
    """What the auxiliary loss averages over: marked pairs (mark arms) or target tokens (decoder)."""
    return marcas.marked_pairs(batch) if "marks" in batch else target_tokens(batch)


def accumulated_backward(model: RationaleBert, batch: dict, combine, micro: int = MICRO_BATCH) -> tuple:
    """Backward of one batch in micro-batches, each loss weighted by its share of the batch's pairs (L_cls) and
    auxiliary units (L_aux), so the summed gradient is the full batch's (I16) with about half the activation memory
    (09/11: batch 32 spilled the 5060's VRAM into shared memory). `combine(l_cls, l_aux)` is the phase's loss.
    Returns the batch's L_cls and L_aux (None without one). Backward runs outside autocast."""
    device = batch["input_ids"].device
    n_pairs, n_tokens = len(batch["y"]), aux_units(batch)
    l_cls_total, l_aux_total = 0.0, None
    for start in range(0, n_pairs, micro):
        part = grads.rows_of(batch, start, start + micro)
        with autocast(device):
            logit, l_aux = model(part)
            l_cls = cls_loss(logit, part["y"]) * (len(part["y"]) / n_pairs)
            if l_aux is not None:
                l_aux = l_aux * (aux_units(part) / n_tokens)
            loss = combine(l_cls, l_aux)
        loss.backward()
        l_cls_total += l_cls.item()
        if l_aux is not None:
            l_aux_total = (l_aux_total or 0.0) + l_aux.item()
    return l_cls_total, l_aux_total
```

1. Você conta os pares do lote e as unidades da perda auxiliar. No braço com decoder a unidade é o token do alvo (`target_tokens`). O ramo com `marks` é de outro experimento.
2. Você percorre o lote de 16 em 16 pares. `rows_of` (em `rte_gradientes.py`, Passo 25) recorta as linhas e apara o preenchimento até o par mais longo do pedaço.
3. Para cada pedaço, você passa pelo modelo e pesa as perdas: a `L_cls` pela fração dos pares do lote que está no pedaço, a `L_aux` pela fração dos tokens de alvo que está no pedaço.
4. Você combina as duas com a perda da fase e chama `backward`. Os gradientes dos pedaços se somam.
5. Como cada pedaço entra com o seu peso, o gradiente somado é o do lote inteiro. A memória de ativações cai mais ou menos pela metade.
6. O `backward` roda fora do `autocast`, que é a recomendação do PyTorch. O bf16 só vale na passada para frente, e só em GPU.

O tamanho do micro-lote muda com `--micro` na linha de comando. O padrão é 16. O texto de ajuda da opção registra o uso de 8 quando outros programas seguram memória da placa.

## Passo 11. Monte o otimizador em grupos

| Grupo | O que tem | Weight decay | Fonte |
|---|---|---|---|
| `encoder` | BERT | 0 | Tabela 4 |
| `head` | a cabeça linear | 0 | escolha deste código (o paper não diz) |
| `decoder` | decoder do T5 + `shared` (+ `bridge` quando existe) | 0,001 | Tabela 4 |

O encoder do T5 fica fora de todos os grupos.

```python
def param_groups(model: RationaleBert) -> list[dict]:
    """Encoder, head and decoder (+ bridge) as separate groups; the frozen T5 encoder is in none."""
    encoder = list(model.bert.parameters())
    heads = list(model.head.parameters()) + (list(model.token_head.parameters()) if model.token_head is not None
                                             else [])
    groups = [{"params": encoder, "weight_decay": 0.0}, {"params": heads, "weight_decay": 0.0}]
    if model.t5 is not None:
        # T5-encoder arm: the encoder (and the `shared` embedding it reads) is already in the first group
        in_encoder = {id(p) for p in encoder}
        decoder = [p for p in model.t5.parameters() if p.requires_grad and id(p) not in in_encoder]
        decoder += list(model.bridge.parameters()) if model.bridge is not None else []
        groups.append({"params": decoder, "weight_decay": DECODER_WEIGHT_DECAY})
    return groups
```

1. Você põe os pesos do BERT no primeiro grupo, sem weight decay.
2. Você põe os pesos da cabeça no segundo grupo, sem weight decay. O trecho com `token_head` é de outro experimento.
3. Se há decoder, você põe no terceiro grupo todos os pesos do T5 que pedem gradiente (o encoder do T5 está congelado, então não entra) e os do `bridge`, quando existe. Esse grupo tem weight decay de 0,001.

## Passo 12. Rode a fase A

Na fase A o BERT fica congelado e só o decoder aprende, usando só a `L_aux`. É uma passada por metade dos pares: 39 lotes.

```python
def run_phase_a(model: RationaleBert, opt: torch.optim.Optimizer, items: list[dict], seed: int, batch_size: int,
                device: torch.device, micro: int = MICRO_BATCH) -> int:
    """One pass over a random half of the pairs: BERT frozen (no graph through it), decoder learns to read it."""
    half = torch.randperm(len(items), generator=torch.Generator().manual_seed(seed))[: len(items) // 2]
    loader = DataLoader([items[i] for i in half], batch_size=batch_size, collate_fn=dados.collate)
    for batch in loader:
        batch = to_device(batch, device)
        n_tokens = target_tokens(batch)
        for start in range(0, len(batch["y"]), micro):
            part = grads.rows_of(batch, start, start + micro)
            with autocast(device):
                with torch.no_grad():
                    h, _ = model.encode(part)
                l_aux = model.decode(h, part).loss * (target_tokens(part) / n_tokens)
            l_aux.backward()
        if model.shares_t5_encoder:  # `shared` is also the encoder's input: frozen with it here (audit 10/11)
            model.t5.shared.weight.grad = None
        finish_step(model, opt)
    return len(loader)
```

1. Você sorteia metade dos pares com a semente da rodada.
2. Para cada lote, você conta os tokens de alvo e percorre o lote em micro-lotes, como no Passo 10.
3. Você passa o pedaço pelo BERT dentro de `torch.no_grad()`. É a forma mais simples de "congelado": nenhum gradiente é calculado ali, então o BERT não muda e a fase gasta menos memória.
4. Você entrega `h` ao decoder, pega a `L_aux` do pedaço, pesa pela fração dos tokens e chama `backward`.
5. Você fecha o passo com `finish_step`. A linha com `shares_t5_encoder` só serve à variante com encoder do T5.
6. A função devolve o número de lotes, que o laço compara com o plano.

A taxa do decoder na fase A é constante, 5e-5. O decoder já é pré-treinado, e a fase tem só 39 passos.

Um teste compara os pesos do BERT antes e depois da fase A: têm de ser idênticos, e os do decoder, diferentes.

## Passo 13. Agende a taxa de aprendizado

O paper tem dois aquecimentos, e o código tem de dizer como eles convivem:

- o da Tabela 4 (500 passos, ou 62 na versão proporcional), que vale para o treino;
- o da fase B (seção 4.4: o encoder é liberado com "aquecimento linear nos primeiros 30%"), que vale para o BERT.

A leitura adotada é que cada grupo do otimizador tem o próprio fator, multiplicado pela taxa de 5e-5:

```
fator(passo) do decoder e da cabeça:  sobe de 0 a 1 em W passos (W = 500 ou 62) e cai linearmente até 0 no passo 624
fator(passo) do BERT:                 sobe de 0 a 1 nos passos 1–187 (fase B) e cai linearmente até 0 no passo 624
fase A:                               taxa constante de 5e-5 no decoder (fora do relógio dos 624 passos)
braço BERT sozinho:                   um fator só para tudo, o da Tabela 4 (W = 500 ou 62)
```

No código:

```python
def linear_schedule(warmup: int, total: int):
    """Hugging Face's get_linear_schedule_with_warmup factor: 0 -> 1 over `warmup` steps, then 1 -> 0 at `total`."""
    def factor(step: int) -> float:
        if step < warmup:
            return step / max(1, warmup)
        return max(0.0, (total - step) / max(1, total - warmup))
    return factor


def lr_factors(model: RationaleBert, plan: Plan) -> list:
    """E1: BERT warms up over phase B when there is a decoder; head and decoder over the Table 4 warmup."""
    table4 = linear_schedule(plan.warmup_steps, plan.total)
    if model.t5 is None and not model.decoder_calendar:
        return [table4, table4]
    return [linear_schedule(plan.phase_b, plan.total), table4] + ([table4] if model.t5 is not None else [])
```

1. `linear_schedule` devolve o fator de um passo: sobe de 0 a 1 durante o aquecimento e depois cai em linha reta até 0 no último passo.
2. Em `lr_factors`, se o modelo não tem decoder, você usa o fator da Tabela 4 para o BERT e para a cabeça.
3. Se o modelo tem decoder, o BERT usa o fator que aquece durante a fase B (187 passos), e a cabeça e o decoder usam o da Tabela 4.
4. A condição com `decoder_calendar` é de outro experimento.

A queda linear até zero depois do aquecimento é o padrão do `get_linear_schedule_with_warmup` da Hugging Face, e a Tabela 4 fala em "warmup steps" do jeito dela. O paper não descreve a queda, então isso é uma leitura do paper, não está escrito nele.

Duas consequências que você precisa declarar ao relatar qualquer resultado:

1. Na cópia fiel, a cabeça só começa a aprender no passo 188 e já está com taxa reduzida. Ela aprende em 437 passos, contra 624 do BERT sozinho. Isso é o desenho do paper, não um erro do código, mas é diferença entre os braços que um resultado nulo pode esconder.
2. O aquecimento do BERT também muda de braço para braço. No braço com decoder ele aquece nos 187 passos da fase B. No BERT sozinho, nos 500 ou 62 passos da Tabela 4.

Fora o decoder, os braços diferem em duas coisas: o atraso da cabeça e a rampa do BERT. Um resultado nulo (ou um ganho) tem de nomear as duas.

## Passo 14. Avalie no dev

```python
@torch.no_grad()
def predict(classifier, items: list[dict], device: torch.device) -> np.ndarray:
    classifier.to(device).eval()
    out = []
    for batch in DataLoader(items, batch_size=BATCH_SIZE, collate_fn=dados.collate):
        with autocast(device):
            logits = classifier(to_device(batch, device)).float()
        out.append((torch.sigmoid(logits) if logits.dim() == 1 else torch.softmax(logits, -1)).cpu())
    return torch.cat(out).numpy()


def metrics(y: np.ndarray, p: np.ndarray, labels: dict[int, str] = grads.RTE_LABELS) -> dict:
    """D4: the paper's ROC-AUC and precision/recall at 0.7, plus accuracy and F1 at 0.5. With more than two labels
    (e-SNLI): accuracy and F1 of the most probable label, ROC-AUC one-vs-rest averaged over the labels."""
    if p.ndim == 2:
        guess = p.argmax(1)
        f1_each = f1_score(y, guess, average=None, labels=list(labels), zero_division=0)
        return {"roc_auc": roc_auc_score(y, p, multi_class="ovr", average="macro", labels=list(labels)),
                "accuracy": accuracy_score(y, guess), "f1_macro": f1_score(y, guess, average="macro", zero_division=0)
                } | {f"f1_{name}": f for name, f in zip(labels.values(), f1_each)}
    at_half, at_cut = p >= 0.5, p >= PRECISION_RECALL_THRESHOLD
    f1_each = f1_score(y, at_half, average=None, labels=[1, 0], zero_division=0)
    return {"roc_auc": roc_auc_score(y, p), "accuracy": accuracy_score(y, at_half),
            "f1_macro": f1_score(y, at_half, average="macro", zero_division=0),
            "f1_entailment": f1_each[0], "f1_not_entailment": f1_each[1],
            "precision_at_0_7": precision_score(y, at_cut, zero_division=0),
            "recall_at_0_7": recall_score(y, at_cut, zero_division=0)}
```

1. Em `predict` você passa os 277 pares do dev pelo classificador do Passo 6, em modo de avaliação e sem gradiente, e aplica a sigmoide ao logit. O resultado é a probabilidade de `entailment` de cada par.
2. Em `metrics` você calcula as métricas do paper, ROC-AUC e precisão e revocação com corte em 0,7, e mais acurácia, F1 macro e F1 de cada classe com corte em 0,5.
3. O ramo `p.ndim == 2` serve a uma tarefa com mais de dois rótulos, fora deste manual.

O dev é o teste, porque o teste do GLUE não tem rótulo. Por isso você lê o dev uma vez, no fim: sem parada antecipada, sem escolher época pelo dev. Vale o modelo do passo 624.

## Passo 15. Grave os resultados de cada rodada

```python
def run_one(cfg: RunConfig, data: Data, device: torch.device, out_dir: Path):
    torch.manual_seed(cfg.seed)  # head (and bridge) initialization; from_pretrained draws nothing else
    model, t5_name = build_model(cfg.arm, cfg.bert_name, len(data.labels))
    plan = make_plan(len(data.train), cfg.warmup, cfg.batch_size, cfg.epochs)
    probes = Probes(data.probes.groups.to(device), data.probes.words.to(device) if cfg.measure_words else None)
    start = time.perf_counter()
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)
    log = train(model, plan, training_items(cfg.arm, data), cfg.seed, device, cfg.batch_size, probes,
                cfg.micro_batch)
    seconds = time.perf_counter() - start
    peak = f", pico {torch.cuda.max_memory_allocated(device) / 2**30:.1f} GB" if device.type == "cuda" else ""
    keys = {"arm": cfg.arm, "warmup": cfg.warmup, "seed": cfg.seed}
    classifier = classifier_only(model)
    scores = metrics(data.dev_y, predict(classifier, data.dev, device), data.labels)
    if data.held is not None:
        held = metrics(data.held_y, predict(classifier, data.held, device), data.labels)
        scores |= {"held_roc_auc": held["roc_auc"], "held_accuracy": held["accuracy"],
                   "n_train": len(data.train), "n_held": len(data.held)}
    if data.outside is not None:
        scores |= outside_scores(data.outside_y, predict(classifier, data.outside, device))
    row = keys | scores | asdict(plan) | {
        "phase_a_steps": log.phase_a_steps, "l_aux_last_epoch": np.mean(log.last_epoch_aux) if log.last_epoch_aux
        else None, "seconds": round(seconds, 1), "device": str(device), "bert": cfg.bert_name,
        "t5": t5_name, "code": code_version()}
    append_csv(out_dir / "gradientes.csv", [keys | r for r in log.group_rows])
    append_csv(out_dir / "palavras.csv", [keys | r for r in log.word_rows])
    append_csv(out_dir / "resultados.csv", [row])  # last: this row is what marks the run as done for --grade
    print(f"{cfg.arm} {cfg.warmup} seed {cfg.seed}: roc_auc {row['roc_auc']:.4f} acc {row['accuracy']:.4f} "
          f"({seconds:.0f} s{peak})", flush=True)
```

Siga uma rodada do começo ao fim:

1. Você fixa a semente do PyTorch. Ela decide a inicialização da cabeça (e do `bridge`), a ordem dos lotes, a metade da fase A e o dropout.
2. Você monta o modelo do braço e o plano de passos.
3. Você leva as sondas das medidas ao dispositivo. A sonda por palavra só entra se a rodada pede essa medida.
4. Você treina e mede o tempo e, em GPU, o pico de memória.
5. Você separa o classificador com `classifier_only` e calcula as métricas no dev.
6. Você monta a linha de resultados: braço, aquecimento, semente, as métricas, os campos do plano, os passos da fase A, a `L_aux` média da última época, o tempo, o dispositivo, os nomes dos modelos e o commit do código.
7. Você grava as linhas das medidas em `gradientes.csv` e `palavras.csv`, e por último a linha em `resultados.csv`.

Os trechos com `data.held` e `data.outside` são de outros experimentos.

Você não salva pesos. O resultado é o CSV.

O `resultados.csv` é gravado por último de propósito: é essa linha que marca a rodada como feita. Se a rodada cair antes, ela é refeita.

As funções de apoio:

```python
@functools.cache
def code_version() -> str:
    """Commit of the code, '-dirty' if src/ has uncommitted changes. main() calls it before any training, so a
    missing git fails at once instead of after an hour of runs (weights are not saved, E8)."""
    def git(*args):
        return subprocess.run(["git", *args], capture_output=True, text=True, check=True,
                              cwd=RTE_TREINO.parents[1]).stdout.strip()
    return git("rev-parse", "--short", "HEAD") + ("-dirty" if git("status", "--porcelain", "src") else "")


def append_csv(path: Path, rows: list[dict]):
    """Appends rows; refuses columns that differ from the file's header, which would land values under wrong names."""
    if not rows:
        return
    frame = pd.DataFrame(rows)
    if path.exists():
        header = list(pd.read_csv(path, nrows=0).columns)
        if header != list(frame.columns):
            raise ValueError(f"{path}: columns {list(frame.columns)} differ from the file's {header}; "
                             "write to a new file instead of mixing schemas")
    path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(path, mode="a", header=not path.exists(), index=False)
```

1. `code_version` lê o commit do código e acrescenta `-dirty` se há mudança sem commit em `src/`. Ela é chamada antes de qualquer treino. Se o git faltar, o erro aparece na hora, não depois de uma hora de rodadas.
2. `append_csv` acrescenta linhas ao arquivo. Ela recusa linha com colunas diferentes do cabeçalho do arquivo, porque os valores cairiam sob nomes errados.

## Passo 16. Rode a grade de rodadas

| Braço | Aquecimento | Sementes | Rodadas |
|---|---|---|---|
| BERT sozinho | 500 e 62 | 5 (10 se for barato) | 10 (20) |
| BERT + decoder | 500 e 62 | 5 (10) | 10 (20) |

São 20 rodadas, ou 40 com 10 sementes. Com sequências curtas, cada rodada deve levar poucos minutos na RTX 5060 (estimativa grossa, a medir na primeira). As sementes são as mesmas nos dois braços, então a mesma semente dá a mesma ordem de lotes nos dois.

A grade pula o que já foi feito:

```python
def done_runs(out_dir: Path) -> set:
    path = out_dir / "resultados.csv"
    if not path.exists():
        return set()
    done = pd.read_csv(path, dtype={"warmup": str})
    return set(zip(done["arm"], done["warmup"], done["seed"]))
```

1. Você lê o `resultados.csv` da pasta de saída.
2. Você monta o conjunto das combinações (braço, aquecimento, semente) que já têm linha.
3. A grade só roda as que faltam. Se a máquina cair, você roda o mesmo comando de novo e ele continua de onde parou.

## Passo 17. Use a linha de comando

As três formas de uso estão no cabeçalho de `rte_treino.py`:

```python
    uv run python -m radibert.rte_treino --fumaca                # D6 smoke test on CPU: tiny BERT + bridge + T5 base
    uv run python -m radibert.rte_treino --grade --seeds 5       # both arms x both warmups; skips runs in the CSV
    uv run python -m radibert.rte_treino --arm bert_decoder --warmup prop --seed 1
```

1. `--fumaca` é o teste de fumaça na CPU: BERT minúsculo de verdade + `bridge` + T5 base de verdade. No código de hoje ele usa 48 pares, lotes de 16, 2 épocas e sondas de 8 e 4 pares. A rodada de verdade usa sondas de 64 e 128.
2. `--grade` roda a tabela do Passo 16, pulando o que já está no CSV. `--seeds` diz quantas sementes.
3. A terceira forma é uma rodada avulsa. Ela exige `--arm`, `--warmup` e `--seed`. Em `--warmup`, `prop` quer dizer 10% dos passos, e `500` é a cópia da Tabela 4.
4. `--medir-palavras` liga a medida por palavra numa rodada avulsa (Passo 21).

## Passo 18. Cheque a memória antes da grade

Quando há braço com decoder a rodar em GPU, o comando começa por uma checagem de memória.

```python
def memory_check(model: RationaleBert, items: list[dict], probe: grads.Probe, device: torch.device,
                 batch_size: int = BATCH_SIZE, micro: int = MICRO_BATCH) -> float:
    """One phase-C step on the longest pairs, then one group measure: the peak GPU memory in GB (0 on CPU). --grade
    runs it first, so an out-of-memory error shows up in seconds instead of hours into the grid (audit 09/11)."""
    place(model, device).train()
    if device.type == "cuda":
        torch.cuda.reset_peak_memory_stats(device)
    longest = sorted(items, key=lambda it: len(it["input_ids"]), reverse=True)[:batch_size]
    accumulated_backward(model, to_device(dados.collate(longest), device), lambda c, a: c + AUX_WEIGHT * a, micro)
    finish_step(model, make_optimizer(model))
    grads.measure_groups(model, probe.to(device), step=0, amp=lambda: autocast(device), chunk=micro)
    return torch.cuda.max_memory_allocated(device) / 2**30 if device.type == "cuda" else 0.0
```

1. Você pega os 32 pares mais longos do treino (o mais longo tem 289 tokens).
2. Você faz um passo da fase C com eles, com a perda `L_cls + 0,1 x L_aux`.
3. Você roda uma medida de gradiente por grupo.
4. Você lê o pico de memória da GPU e imprime, ao lado do total da placa.

Se não couber, o erro aparece em segundos, não horas depois, no meio da grade.

Quando este código foi escrito, a memória na RTX 5060 ainda não tinha sido medida. Essa checagem é a primeira medida de verdade.

## Passo 19. Entenda por que medir o gradiente

Duas medidas entram no laço: a parcela do gradiente auxiliar que vem de cada grupo de palavras da justificativa (uma ideia que parte de Wadhwa et al. (2024)) e o cosseno entre `g_c`, o gradiente da `L_cls`, e `g_a`, o gradiente da `L_aux`.

Elas importam no RTE porque o rótulo está escrito na justificativa. Uma contagem sobre as 2.470 justificativas mostra:

- "not / never / no" aparece em 90% das justificativas de not_entailment e em 4% das de entailment. Só por essas palavras já se adivinha o rótulo quase sempre.
- 90 expressões de 1 a 3 palavras aparecem 30 vezes ou mais e caem em 90% ou mais das vezes num só rótulo.
  - Do lado de not_entailment: "does not" 381/398, "never" 167/168, "does not mention" 76/76, "not necessarily", "no information", "is not established", "unknown".
  - Do lado de entailment: "confirming" 203/205, "directly" 173/184, "is explicitly" 127/134, "which means" 44/45, "constitutes" 47/47.

É o equivalente no RTE de "mutually exclusive / cannot" no e-SNLI. Para o decoder acertar essas palavras, o BERT precisa saber o rótulo, que já é o que a `L_cls` pede.

A pergunta que a medida responde é: quanto do empurrão do decoder no BERT vem dessas palavras, e quanto vem do conteúdo (o fato que decide)? Se quase tudo vier delas, a cabeça auxiliar é uma segunda cabeça de classificação, e o método não está ensinando o "porquê".

## Passo 20. Ponha cada token da justificativa num grupo

Todo token da justificativa cai em exatamente um grupo. Você testa as regras nesta ordem:

| Grupo | Regra | Exemplo em "Titan has an atmosphere but the text never mentions its orbit" (premissa fala de Titã e da atmosfera) |
|---|---|---|
| S, palavras de rótulo | o token está dentro de uma expressão de 1 a 3 palavras com 30 ocorrências ou mais e 90% ou mais num só rótulo (calculada só no treino) | "but", "never mentions" |
| F, gramatical | stop word, palavra de enunciado de `copia.py` ("states", "premise"), "text", "passage", letra solta, ou token que não é palavra (pontuação, `</s>`) | "has", "an", "the", "text", "its", "." |
| N, palavra nova | palavra de conteúdo que não aparece na premissa nem na hipótese (números contam como palavra) | "orbit" |
| C, copiada do par | palavra de conteúdo que está no par | "Titan", "atmosphere" |

O que você precisa saber sobre as regras:

- A regra de N é a mesma de `copia.new_words`, já usada no e-SNLI e na análise do lote de justificativas (mediana de 4 palavras novas por justificativa).
- Não há lematização, então "moons" é nova se o par diz "moon".
- S vem primeiro: uma palavra de rótulo fica em S mesmo que esteja no par.
- Número de um dígito conta como palavra, não como F.

### O que cada grupo contém de verdade

Uma primeira contagem por palavra, feita com três grupos (S, C e N, com a gramática dentro de C), deu S 12%, C 71% e N 17% das 49.767 palavras:

- S: "not", "but", "does", "confirming", "no", "never".
- C: dominado por palavras gramaticais ("the", "a", "in", "to").
- N: mais conectivo de raciocínio do que conhecimento de mundo. As mais comuns são "implying", "specific", "identified", "meaning", "explicitly" e "claim". As de conteúdo vêm logo atrás: "location", "role", "date", "year", "event".

Isso pesa na leitura:

- N não é "conhecimento do professor" puro. É "o que o professor escreveu além do par", com muito conectivo misturado.
- Com três grupos, C misturava cópia do par com gramática. As palavras gramaticais são fáceis e devem ter perda baixa cedo, mas enquanto não tiverem, entrariam na parcela de C.

Por isso as palavras gramaticais ficam num grupo à parte, o F. Com as regras finais do código (`word_groups`, 90 expressões de rótulo nas 2.470 justificativas), as 50.800 palavras ficam em S 12,0%, F 40,3%, C 31,2% e N 16,5%. Quase metade do C de três grupos era gramática.

A cada carga de dados, o código salva `grupos-palavras.csv` com as 50 palavras mais comuns de cada grupo, e `expressoes-rotulo.csv` com as expressões de rótulo e as contagens por rótulo. Assim você lê o que cada número significa, sem confiar no nome do grupo.

## Passo 21. Meça a parcela de cada grupo no gradiente

Faça a medida nesta ordem:

1. Marcação. Em cada justificativa, você acha as palavras e o grupo de cada uma, em posições de caractere. O tokenizador rápido do T5 devolve a posição de cada token (`return_offsets_mapping`), então cada token do alvo recebe S, F, C ou N.
2. Lote de sonda fixo. Você separa 64 pares do treino (32 por rótulo), os mesmos em todas as rodadas, sorteados uma vez com semente própria. A medida roda com o modelo em `eval()` (sem dropout) e volta para `train()` depois.
3. A cada 25 passos, e também no passo 1, nas fases B e C, você tira cinco gradientes só nos pesos do BERT: `g_c` (da `L_cls`) e `g_S`, `g_F`, `g_C`, `g_N` (das partes da `L_aux` que vêm de cada grupo). Na fase A o BERT está congelado e não recebe gradiente, então não há medida.
4. A `L_aux` é a média por token. Dividindo cada parte pelo mesmo denominador, `L_aux = L_S + L_F + L_C + L_N`, e `g_a = g_S + g_F + g_C + g_N` exatamente.
5. Você grava uma linha em `gradientes.csv`, por braço, aquecimento, semente e passo, com as colunas abaixo.

| Coluna | O que diz |
|---|---|
| `frac_tokens_S`, `_F`, `_C`, `_N` | fração dos tokens do alvo em cada grupo. É a régua: se S tem 12% dos tokens e 60% do gradiente, domina |
| `share_S`, `_F`, `_C`, `_N` = `dot(g_X, g_a) / dot(g_a, g_a)` | quanto do gradiente auxiliar vem de cada grupo; as parcelas somam 1 |
| `cos_c_a` | o cosseno entre `g_c` e `g_a`: a auxiliar ajuda (maior que 0), é neutra (perto de 0) ou briga (menor que 0) |
| `cos_c_S`, `_F`, `_C`, `_N` | o cosseno entre `g_c` e o gradiente de cada grupo. S deve concordar com a classificação; se houver briga, mostra de que grupo ela vem |
| `l_S`, `l_F`, `l_C`, `l_N` | perda média por token de cada grupo, para ver qual o decoder já aprendeu |
| `norm_c`, `norm_a` | o tamanho de `g_c` e de `g_a`. É a escala, para ler o peso 0,1 da `L_aux` |

A linha tem ainda o passo, a fase, a `L_cls` e a `L_aux` da sonda.

São 25 medidas por rodada: os passos 1, 25, 50, e assim por diante até 600. O braço BERT sozinho fica de fora, porque não tem `L_aux`.

Custo: a estimativa, feita quando eram três grupos, era de 25 medidas por rodada x 4 `backward` em 64 pares, segundos por rodada. É uma estimativa, a medir.

## Passo 22. Meça a influência de cada palavra no encoder

São três números diferentes, que não convém misturar:

| Pergunta | Número | Onde |
|---|---|---|
| A palavra é difícil para o decoder? | `l` = perda do decoder naquela palavra | `l_S`, `l_F`, `l_C`, `l_N` nos grupos; `l_t` por palavra |
| Quanto a palavra mexe no encoder? | o tamanho do gradiente dela nos pesos do BERT | `share_*` nos grupos; `norm_t` por palavra |
| Esse empurrão no encoder ajuda a classificar? | `dot(g_c, g) / norm_c` = quanto do empurrão aponta na direção da `L_cls` | `cos_c_*` nos grupos; `align_t` por palavra |

As medidas por grupo já são do encoder: os gradientes de cada grupo são tirados nos pesos do BERT, não no decoder. O que a medida por palavra acrescenta é a resolução.

### Como ler o `align_t`

O `align_t` tem leitura direta pela aproximação de primeira ordem: a mudança na perda é aproximadamente o gradiente vezes o deslocamento. Se o BERT desse um passo de tamanho eta empurrado só pela palavra t, a `L_cls` mudaria em aproximadamente `-eta * 0,1 * dot(g_c, g_t)`.

- Positivo quer dizer que a palavra ensina ao encoder algo que serve para classificar.
- Negativo, que ela puxa contra.

É a mesma ideia de medir influência por produto de gradientes do TracIn (arXiv:2002.08484, "Estimating Training Data Influence by Tracing Gradient Descent"). Dessa obra só o título foi conferido, e lá a unidade é o exemplo de treino, não a palavra.

### Como medir

1. A unidade é a ocorrência de palavra, não o tipo. Numa sonda de 128 pares, só 48 palavras aparecem 8 vezes ou mais, e elas cobrem 44% do texto, quase todas gramaticais ou de rótulo. As palavras de conteúdo ("Titan", "orbit") aparecem uma vez cada. Por isso cada ocorrência vira uma linha, e a agregação vem depois: por tipo para as frequentes, por grupo e por par para as raras.
2. Uma palavra é a soma das perdas dos tokens do T5 que a formam ("Saturn's" pode virar 3 tokens). Você faz um `backward` por ocorrência, só nos pesos do BERT, com o `g_c` da sonda inteira guardado. Cada `g_t` vira números e é descartado na hora, então a memória fica em cerca de 2 gradientes.
3. Os tokens que não são palavra (pontuação e o `</s>` do fim de cada alvo) entram como unidades próprias, no grupo F, para que a soma feche.
4. A sonda por palavra tem 128 pares (64 por rótulo), os mesmos em todas as rodadas.
5. Custo (estimativa, a medir): 128 pares x ~20 palavras, cerca de 2.600 `backward` de um par só, cerca de 1 minuto por medida na RTX 5060. Por isso a medida roda em 3 pontos (passo 1, passo 187 no fim da fase B e passo 624 no fim) e só em uma semente por aquecimento no braço com decoder. Na grade, é a semente 1. Numa rodada avulsa, você liga com `--medir-palavras`. A medida por grupo continua a cada 25 passos em todas as rodadas.
6. A saída vai para `palavras.csv`, uma linha por ocorrência de palavra em cada rodada e passo: `idx` do par, palavra, grupo, número de tokens, `l_t`, `norm_t`, `align_t` e `cos_t`.

```python
def measure_words(model, probe: Probe, step: int, amp=contextlib.nullcontext, chunk: int = CHUNK_PAIRS) -> list[dict]:
    """One row per word occurrence: loss in the decoder, size of its push on BERT, and how much of it helps L_cls.
    g_c is summed in chunks; then one pair's graph at a time, one backward per word, reduced to numbers at once."""
    n_pairs, n_tokens = probe_sizes(probe)
    device = next(model.bert.parameters()).device
    rows = []
    with evaluating(model):
        ([g_c], _) = summed_grads(model, probe, cls_term(n_pairs), amp, chunk)
        g_c = [g.to(device) for g in g_c]
        norm_c = dot(g_c, g_c) ** 0.5
        for i, units in enumerate(probe.units):
            pair = rows_of(probe.batch, i, i + 1)
            with amp():
                h, _ = model.encode(pair)
                nll = token_nll(model.decode(h, pair).logits, pair["labels"])[0] / n_tokens
            for j, unit in enumerate(units):
                part = nll[list(unit.positions)].sum()
                g_t = bert_grad(part, model, retain_graph=j < len(units) - 1)
                ct, tt = dot(g_c, g_t), dot(g_t, g_t)
                rows.append({"step": step, "idx": int(pair["idx"]), "word": unit.word, "group": unit.group.name,
                             "n_tokens": len(unit.positions), "l_t": part.item() * n_tokens / len(unit.positions),
                             "norm_t": tt ** 0.5, "align_t": ct / norm_c,
                             "cos_t": ct / (norm_c * tt ** 0.5) if tt else 0.0})
    return rows
```

Siga a função assim:

1. Você lê o tamanho da sonda: número de pares e número de tokens de alvo.
2. Com o modelo em modo de avaliação, você calcula `g_c`, o gradiente da `L_cls` da sonda inteira, somado em blocos (a função `summed_grads` está no Passo 25), e guarda a norma dele.
3. Você percorre a sonda um par por vez. Para cada par, passa pelo BERT e pelo decoder e calcula a perda de cada posição do alvo, dividida pelo número de tokens da sonda inteira. É o mesmo denominador da `L_aux`.
4. Para cada palavra do par, você soma as perdas das posições dela e tira o gradiente dessa soma nos pesos do BERT: é o `g_t`.
5. Você reduz o `g_t` a números e o descarta: `l_t` (perda média por token da palavra), `norm_t` (tamanho do empurrão no encoder), `align_t` (quanto dele aponta na direção da `L_cls`) e `cos_t` (o cosseno com `g_c`).

Rodar um par por vez (passada para frente de um par, um `backward` por palavra dele) é o que torna o custo cerca de 1 minuto.

A soma dos `align_t` de todas as palavras da sonda é igual a `dot(g_c, g_a) / norm_c`, o alinhamento da `L_aux` inteira. As palavras dividem exatamente o empurrão total, como os grupos. Há um teste para isso.

Limite: o `align_t` é de primeira ordem (um passo pequeno, sem Adam). O AdamW normaliza o passo por parâmetro, então o passo real não é eta vezes o gradiente. A medida diz para onde cada palavra empurra o encoder, não quanto o otimizador de fato anda.

## Passo 23. Saiba o que a medida prova e o que não prova

- 25 pontos por rodada cobrem início, meio e fim. Palavra fácil tem perda perto de zero no fim e gradiente baixo, mesmo que tenha dominado o começo.
- `share_S` alto não prova dano. Quem prova é um terceiro braço com os tokens de S fora da `L_aux`. Esse braço não entra na grade: só faz sentido se o `share_S` vier alto. O mesmo vale para C (um braço sem a cópia do par).
- A medida é a parcela do gradiente por grupo de palavras. Não é o método de atribuição de Wadhwa et al. (2024). A seção abaixo explica a diferença.

### O que Wadhwa et al. (2024) fizeram, e por que a medida aqui é outra

O que segue vem da seção 2, "Experimental Design", parte "Attribution from Rationales", e da Tabela 3 do paper (arXiv:2406.14511).

- Método: Integrated Gradients (Sundararajan et al. 2017). Eles ajustam um GPT-2 para escrever a justificativa antes do rótulo e medem quanto cada token da justificativa pesa na saída do rótulo: o gradiente da saída em relação ao embedding do token, integrado do vetor de base (zero ou neutro) até o embedding real. A direção é token da justificativa -> rótulo.
- Uso: guardam os 15 tokens de maior atribuição (a justificativa média tem 36,3 tokens) e treinam os alunos (GPT-2, Phi-1.5, Gemma-2B; professor Mistral-7B-Instruct) com esses 15 depois do rótulo. O desempenho não muda de forma significativa em relação à justificativa inteira.
- O controle que interessa aqui: trocar a justificativa pelas 15 palavras mais parecidas com o rótulo (vizinhas no Word2Vec) dá resultado comparável a não usar justificativa. Na frase deles, os tokens precisam trazer sinal "além de ser simplesmente parecidos" com o rótulo.

Por que você não pode copiar o método: o Integrated Gradients deles pergunta de quais tokens da justificativa a previsão do rótulo depende. Isso só existe num modelo que lê a justificativa antes de dar o rótulo. Aqui o classificador nunca vê a justificativa: ela é só alvo do decoder. A pergunta equivalente neste desenho é a inversa, quais tokens da justificativa moldam o encoder (direção token da justificativa -> pesos do BERT), e é isso que o `share_S` mede. Por isso a medida daqui não se cita como sendo a de Wadhwa et al. (2024).

O que Wadhwa et al. (2024) emprestam para a leitura do resultado é uma hipótese, não uma prova, porque o aluno deles é decoder. As palavras de rótulo do RTE ("not", "never", "confirming") são o caso "parecido com o rótulo". Se o `share_S` vier alto, a previsão é ganho perto de zero contra o BERT sozinho. Se vier baixo e houver ganho, o ganho vem do conteúdo.

## Passo 24. Escreva o código dos grupos e da sonda (`rte_gradientes.py`)

### Os grupos e as constantes

```python
class Group(IntEnum):
    S = 0  # label word
    F = 1  # function word or non-word token
    C = 2  # copied from the pair
    N = 3  # new


MIN_COUNT, MIN_SHARE = 30, 0.9
SOURCE_WORDS = {"text", "passage"}  # name the source, as "premise" and "sentence" do in copia.META
WORD = re.compile(r"[a-z0-9]+", re.I)  # matched on the original text, so offsets stay those of the tokenizer
PROBE_SEED = 0
GROUP_PROBE_SIZE, WORD_PROBE_SIZE = 64, 128
TOP_WORDS_PER_GROUP = 50
CHUNK_PAIRS = 16  # probe pairs per forward pass in the measures


def words_of(text: str) -> list[str]:
    return [w.lower() for w in WORD.findall(text)]


RTE_LABELS = {1: "entailment", 0: "not_entailment"}  # y -> name, in the table's column order
```

1. Os grupos são um `IntEnum`: `Group.S`, `Group.F`, `Group.C`, `Group.N`.
2. `MIN_COUNT` e `MIN_SHARE` são a regra das palavras de rótulo: 30 ocorrências ou mais, 90% ou mais num rótulo.
3. As sondas têm 64 pares (medida por grupo) e 128 pares (medida por palavra), sorteados com a semente 0.
4. `CHUNK_PAIRS` é o número de pares da sonda por passada para frente nas medidas: 16.

### As expressões de rótulo

```python
def expression_table(pairs: pd.DataFrame, labels: dict[int, str] = RTE_LABELS) -> pd.DataFrame:
    """Expressions of 1-3 words found in >= MIN_COUNT rationales, >= MIN_SHARE of them with one label (train only)."""
    seen = {y: Counter() for y in labels}
    for y, rationale in zip(pairs["y"], pairs["rationale"]):
        tokens = words_of(rationale)
        seen[y].update({" ".join(tokens[i:i + n]) for n in (1, 2, 3) for i in range(len(tokens) - n + 1)})
    rows = []
    for expr in set().union(*seen.values()):
        counts = {y: seen[y][expr] for y in labels}
        total = sum(counts.values())
        if total >= MIN_COUNT and max(counts.values()) / total >= MIN_SHARE:
            rows.append({"expression": expr} | {f"n_{labels[y]}": n for y, n in counts.items()})
    columns = [f"n_{name}" for name in labels.values()]
    return pd.DataFrame(rows, columns=["expression", *columns]).sort_values(columns, ascending=False,
                                                                             ignore_index=True)


def expression_pattern(table: pd.DataFrame) -> re.Pattern:
    """One regex for all expressions, longest first; words may be joined by any non-word run ("doesn't")."""
    parts = sorted((r"\W+".join(map(re.escape, e.split())) for e in table["expression"]), key=len, reverse=True)
    return re.compile(r"\b(?:" + "|".join(parts) + r")\b", re.I)
```

1. Em `expression_table` você percorre as justificativas do treino e conta, por rótulo, em quantas delas aparece cada expressão de 1, 2 ou 3 palavras. Ela lê só o treino, nunca o dev.
2. Você guarda as expressões com 30 ocorrências ou mais e 90% ou mais num só rótulo.
3. Em `expression_pattern` você monta uma regex com todas elas, a mais longa primeiro.

### O grupo de cada palavra

```python
def word_groups(rationale: str, premise: str, hypothesis: str, label_expr: re.Pattern) -> list[tuple[int, int, str, int]]:
    """(start, end, word, group) for each word of the rationale."""
    label_spans = [m.span() for m in label_expr.finditer(rationale)]
    pair = set(words_of(f"{premise} {hypothesis}"))
    out = []
    for m in WORD.finditer(rationale):
        word, (start, end) = m.group().lower(), m.span()
        if any(a < end and start < b for a, b in label_spans):
            group = Group.S
        elif (len(word) == 1 and not word.isdigit()) or word in DROP or word in SOURCE_WORDS:
            group = Group.F
        else:
            group = Group.C if word in pair else Group.N
        out.append((start, end, word, group))
    return out
```

1. Você acha os trechos da justificativa que casam com alguma expressão de rótulo.
2. Você monta o conjunto das palavras do par (premissa + hipótese).
3. Para cada palavra da justificativa, você testa na ordem: se cruza um trecho de rótulo, é S; se é letra solta (que não seja dígito), stop word, palavra de enunciado ou palavra que nomeia a fonte ("text", "passage"), é F; senão, é C se está no par e N se não está.

### Dos grupos de palavra às posições do alvo

```python
@dataclass(frozen=True)
class Unit:
    """One word of a rationale (or one non-word token) and the T5 target positions it spans."""
    word: str
    group: int
    positions: tuple[int, ...]


def token_units(rationale: str, premise: str, hypothesis: str, t5_tok, label_expr: re.Pattern) -> list[Unit]:
    """Every T5 target position belongs to exactly one unit, so units split L_aux with nothing left over (I15)."""
    enc = t5_tok(rationale, return_offsets_mapping=True, truncation=True, max_length=MAX_TARGET_TOKENS)
    words = word_groups(rationale, premise, hypothesis, label_expr)
    owner = {}
    for pos, (a, b) in enumerate(enc["offset_mapping"]):
        hit = next((i for i, (start, end, _, _) in enumerate(words) if a < end and start < b), None)
        owner.setdefault(("w", hit) if hit is not None else ("t", pos), []).append(pos)
    tokens = t5_tok.convert_ids_to_tokens(enc["input_ids"])
    units = []
    for (kind, ref), positions in owner.items():
        word, group = words[ref][2:] if kind == "w" else (tokens[ref], Group.F)
        units.append(Unit(word, group, tuple(positions)))
    return units
```

1. Você tokeniza a justificativa com o T5 pedindo a posição de caractere de cada token.
2. Para cada posição do alvo, você procura a palavra que ela cruza. Se achar, a posição pertence àquela palavra. Se não achar (pontuação, `</s>`), a posição vira uma unidade própria, do grupo F.
3. Cada `Unit` guarda a palavra, o grupo e as posições do alvo que ela ocupa. Toda posição do alvo pertence a exatamente uma unidade, então as unidades dividem a `L_aux` sem sobra.

### O lote de sonda

```python
@dataclass
class Probe:
    """A fixed batch of train pairs, the group of each target position (-1 on padding) and its word units."""
    batch: dict
    groups: torch.Tensor
    units: list[list[Unit]]

    def to(self, device) -> "Probe":
        return Probe({k: v.to(device) for k, v in self.batch.items()}, self.groups.to(device), self.units)


def build_probe(pairs: pd.DataFrame, tok: Tokenizers, label_expr: re.Pattern, size: int) -> Probe:
    """size / (number of labels) pairs per label, drawn with PROBE_SEED, the same in every run."""
    per_label = size // pairs["y"].nunique()
    chosen = pd.concat([g.sample(per_label, random_state=PROBE_SEED) for _, g in pairs.groupby("y")])
    chosen = chosen.sort_values("idx")
    batch = collate(encode(chosen, tok))
    units = [token_units(r, p, h, tok.t5, label_expr)
             for p, h, r in zip(chosen["sentence1"], chosen["sentence2"], chosen["rationale"])]
    groups = torch.full_like(batch["labels"], -1)
    for i, pair_units in enumerate(units):
        for unit in pair_units:
            groups[i, list(unit.positions)] = unit.group
    if not torch.equal(groups == -1, batch["labels"] == IGNORED):
        raise ValueError("probe: target positions without a group, or a group on padding; offsets and ids disagree")
    return Probe(batch, groups, units)
```

1. Em `build_probe` você sorteia o mesmo número de pares por rótulo, com a semente fixa, e ordena por `idx`.
2. Você tokeniza e monta o lote com as mesmas funções do treino (`encode` e `collate`).
3. Você calcula as unidades de cada par e preenche a matriz `groups`: o grupo de cada posição do alvo, e -1 no preenchimento.
4. Você confere que as posições sem grupo são exatamente as de preenchimento. Se não forem, o código para com erro.

## Passo 25. Escreva o código da medida por grupo

### As peças de apoio

```python
@contextlib.contextmanager
def evaluating(model):
    was_training = model.training
    model.eval()
    try:
        yield
    finally:
        model.train(was_training)


def measured_params(model) -> list:
    """The encoder weights the measures look at. In the T5-encoder arm with decoder the `shared` embedding is left
    out: the decoder also embeds its own target tokens with it, so its gradient would mix the decoder's learning
    with the push on the encoder (audit 10/11)."""
    params = list(model.bert.parameters())
    if getattr(model, "shares_t5_encoder", False):
        params = [p for p in params if p is not model.t5.shared.weight]
    return params


def bert_grad(loss: torch.Tensor, model, retain_graph: bool = True) -> tuple[torch.Tensor, ...]:
    return torch.autograd.grad(loss, measured_params(model), retain_graph=retain_graph)


def dot(a, b) -> float:
    return float(sum((x.float() * y.float()).sum() for x, y in zip(a, b)))


def token_nll(logits: torch.Tensor, labels: torch.Tensor) -> torch.Tensor:
    """Per-position cross-entropy of the T5 target; 0 on IGNORED positions."""
    return F.cross_entropy(logits.transpose(1, 2).float(), labels, ignore_index=IGNORED, reduction="none")


def split_aux_loss(logits: torch.Tensor, labels: torch.Tensor, groups: torch.Tensor, n_tokens: int) -> list:
    """L_aux split by group over the target tokens of the whole probe (`n_tokens`), so the parts of every chunk add up
    to L_aux exactly (I12)."""
    nll = token_nll(logits, labels)
    return [(nll * (groups == g)).sum() / n_tokens for g in Group]


def rows_of(batch: dict, start: int, stop: int) -> dict:
    """Rows start..stop-1 of a batch, trimmed to their own longest input and target. Contiguous copies: a trimmed
    slice is not, and T5 calls labels.view(-1) (the PC run of 09/11 died on it)."""
    rows = slice(start, stop)
    n_in = int(batch["attention_mask"][rows].sum(1).max())
    n_out = int((batch["labels"][rows] != IGNORED).sum(1).max())
    out = {k: batch[k][rows, :n_in] for k in ("input_ids", "token_type_ids", "attention_mask", "marks") if k in batch}
    out |= {"labels": batch["labels"][rows, :n_out], "y": batch["y"][rows], "idx": batch["idx"][rows]}
    return {k: v.contiguous() for k, v in out.items()}
```

1. `evaluating` põe o modelo em modo de avaliação durante a medida e devolve ao modo anterior no fim. Sem dropout o número é estável, e a medida não gasta o sorteio do treino.
2. `measured_params` devolve os pesos do encoder que a medida olha. O ramo com `shares_t5_encoder` é da variante com encoder do T5.
3. `bert_grad` tira o gradiente de uma perda só nesses pesos, com `torch.autograd.grad`. Essa função devolve o gradiente sem somar no `.grad`, então o otimizador não vê nada disso.
4. `dot` é o produto escalar de dois gradientes, camada a camada.
5. `token_nll` é a entropia cruzada de cada posição do alvo, com 0 nas posições ignoradas.
6. `split_aux_loss` divide a `L_aux` por grupo, sempre com o mesmo denominador (os tokens de alvo da sonda inteira). Assim as partes somam exatamente a `L_aux`.
7. `rows_of` recorta linhas de um lote e apara o preenchimento. Ela devolve cópias contíguas, porque o T5 chama `labels.view(-1)` e isso falha num recorte que não é contíguo.

### A soma em blocos

```python
def summed_grads(model, probe: Probe, terms, amp, chunk: int) -> tuple[list, list[float]]:
    """For each loss term that `terms(model, rows, groups)` returns on a chunk of the probe, its BERT gradient summed
    over all chunks, in fp32 on the CPU, and the term's value summed. Only one chunk's graph and one gradient are on
    the GPU at a time (audit 09/11: the whole probe's graph plus 6 BERT gradients would not fit the 5060)."""
    acc, values = None, None
    for start in range(0, len(probe.batch["y"]), chunk):
        rows = rows_of(probe.batch, start, start + chunk)
        with amp():
            losses = terms(model, rows, probe.groups[start:start + chunk, :rows["labels"].shape[1]])
        if acc is None:
            acc = [[torch.zeros(p.shape) for p in measured_params(model)] for _ in losses]
            values = [0.0] * len(losses)
        for k, loss in enumerate(losses):
            for total, g in zip(acc[k], bert_grad(loss, model, retain_graph=k < len(losses) - 1)):
                total += g.float().cpu()
            values[k] += loss.item()
    return acc, values


def cls_term(n_pairs: int):
    """L_cls of a chunk, scaled so the chunks add up to the mean over the whole probe."""
    def terms(model, rows, groups):
        _, logit = model.encode(rows)
        return [cls_loss(logit, rows["y"], reduction="sum") / n_pairs]
    return terms


def cls_and_group_terms(n_pairs: int, n_tokens: int):
    def terms(model, rows, groups):
        h, logit = model.encode(rows)
        l_cls = cls_loss(logit, rows["y"], reduction="sum") / n_pairs
        return [l_cls] + split_aux_loss(model.decode(h, rows).logits, rows["labels"], groups, n_tokens)
    return terms


def probe_sizes(probe: Probe) -> tuple[int, int]:
    return len(probe.batch["y"]), int((probe.batch["labels"] != IGNORED).sum())
```

A sonda inteira não cabe de uma vez na placa de 8 GB. A medida por grupo seguraria o grafo dos 64 pares e 6 gradientes do BERT ao mesmo tempo (cerca de 11 GB, pela conta feita na revisão do código), e a medida por palavra seguraria o grafo dos 128 pares durante o laço inteiro. Por isso:

1. Em `summed_grads` você percorre a sonda em blocos de 16 pares.
2. Para cada bloco, você calcula os termos da perda (a função `terms` diz quais) e tira o gradiente de cada termo nos pesos do BERT.
3. Você soma os gradientes em fp32 na CPU. Só o grafo de um bloco e um gradiente ficam na GPU de cada vez.
4. A soma é exata porque cada bloco divide pelo denominador da sonda inteira: `cls_term` e `cls_and_group_terms` dividem a `L_cls` pelo número de pares da sonda e a `L_aux` pelo número de tokens de alvo da sonda. Um teste confere bloco de 2 contra sonda inteira.

A estimativa anterior era de cerca de 1,8 GB para quatro gradientes do BERT em fp32 enquanto a medida roda, com a saída de mandá-los para a CPU se não coubessem. É o que o código faz.

### A medida

```python
def measure_groups(model, probe: Probe, step: int, amp=contextlib.nullcontext, chunk: int = CHUNK_PAIRS) -> dict:
    """g_c and one L_aux gradient per group, reduced to fractions, shares, cosines and per-token losses.
    `amp` builds the autocast context of the forward pass; the gradients are taken outside it, as in training."""
    with evaluating(model):
        (g_c, *g_parts), (l_cls, *parts) = summed_grads(model, probe, cls_and_group_terms(*probe_sizes(probe)), amp,
                                                        chunk)
    g_a = [sum(layer) for layer in zip(*g_parts)]
    aa, cc = dot(g_a, g_a), dot(g_c, g_c)
    valid = probe.groups[probe.groups >= 0]
    row = {"step": step, "l_cls": l_cls, "l_aux": sum(parts), "norm_c": cc ** 0.5, "norm_a": aa ** 0.5,
           "cos_c_a": dot(g_c, g_a) / (cc * aa) ** 0.5}
    for g, part, g_x in zip(Group, parts, g_parts):
        frac = float((valid == g).float().mean())
        xx = dot(g_x, g_x)
        row |= {f"frac_tokens_{g.name}": frac, f"share_{g.name}": dot(g_x, g_a) / aa,
                f"cos_c_{g.name}": dot(g_c, g_x) / (cc * xx) ** 0.5 if xx else 0.0,
                f"l_{g.name}": part / frac if frac else 0.0}
    return row
```

1. Com o modelo em modo de avaliação, você chama `summed_grads` e recebe `g_c` e um gradiente por grupo, mais os valores da `L_cls` e das partes da `L_aux`.
2. Você soma os gradientes dos grupos, camada a camada, e tem `g_a`.
3. Você calcula as normas e o cosseno entre `g_c` e `g_a`.
4. Para cada grupo, você calcula a fração dos tokens, a parcela do gradiente (`share`), o cosseno com `g_c` e a perda média por token do grupo.
5. A passada para frente usa o mesmo contexto de bf16 do treino (`amp`). Os gradientes saem fora dele, como no treino.

## Passo 26. Ligue a medida ao treino

O que a medida exige dos outros arquivos:

- Em `rte_modelo.py`, o `forward` é `encode` (BERT + cabeça, devolve `h` e o logit) seguido de `decode` (o T5 sobre `h`). O treino e a medida chamam as mesmas duas funções, então não há como a medida olhar um modelo diferente do que treina.
- Em `rte_dados.py`, nada muda: o `collate` não devolve os grupos. Só a sonda os carrega, e a perda do treino não os usa.
- Em `rte_treino.py`, dentro do laço do braço com decoder, depois do passo do otimizador, você chama esta função:

```python
def measure(model, probes: Probes | None, plan: Plan, step: int, log: TrainLog, device, chunk: int):
    """Group measure at step 1 and every MEASURE_EVERY steps; word measure at 1, end of phase B and the last step."""
    if probes is None:
        return
    amp = lambda: autocast(device)  # noqa: E731  forward under bf16 like training; gradients outside it
    if step == 1 or step % MEASURE_EVERY == 0:
        log.group_rows.append({"phase": "B" if step <= plan.phase_b else "C"}
                              | grads.measure_groups(model, probes.groups, step, amp, chunk))
    if probes.words is not None and step in {1, plan.phase_b, plan.total}:
        log.word_rows += grads.measure_words(model, probes.words, step, amp, chunk)
```

1. Se a rodada não tem sondas, a função não faz nada.
2. No passo 1 e a cada 25 passos, você roda a medida por grupo e guarda a linha, com a fase (B até o passo 187, C depois).
3. Se a rodada tem a sonda por palavra, você roda a medida por palavra nos passos 1, 187 e 624.
4. As linhas vão para `gradientes.csv` e `palavras.csv` no fim da rodada, junto com a linha de `resultados.csv` (Passo 15).

A fase A fica de fora porque o BERT está congelado. O braço BERT sozinho também fica de fora, porque não tem `L_aux`.

Medir não muda o treino. Duas rodadas minúsculas com a mesma semente, uma com medida e outra sem, terminam com a mesma perda e os mesmos pesos. Isso prova que a medida não toca no `.grad`, nos pesos nem no sorteio. Há um teste para isso.

## Passo 27. Rode os testes

Cada linha da tabela é um teste em `tests/test_rte_treino.py`, com BERT e T5 de configuração minúscula e pesos aleatórios (`BertConfig(hidden_size=32, ...)`, `T5Config(d_model=32, ...)`). Eles rodam na CPU em segundos, sem rede, e cabem no CI.

| O que tem de valer | Como o teste prova |
|---|---|
| treino e dev não têm par em comum | nenhum par (premissa, hipótese) repetido entre os dois. O teste compara só o texto: o `idx` do GLUE recomeça em cada split (o dev vai de 0 a 276), então coincidir `idx` não quer dizer nada |
| os 20 exemplos ficam fora, e os dois braços treinam nos mesmos 2.470 | `training_pairs()` sem nenhum `idx` de `rte_examples()`; mesmo conjunto nos dois braços |
| y = 1 se e somente se o rótulo é `entailment` | um par conhecido do treino com label 0 no GLUE sai com y = 1 |
| o braço BERT sozinho não tem decoder, e a rodada com BERT base não tem `bridge` | `model.t5 is None`; com hidden 768, `model.bridge is None` |
| a fase A não muda o BERT | pesos do BERT idênticos antes e depois; pesos do decoder diferentes |
| a fase B não muda a cabeça | pesos da cabeça idênticos antes e depois do passo 187 |
| o gradiente da `L_aux` chega ao BERT | `L_aux.backward()` sozinho deixa gradiente não nulo numa camada do BERT |
| a avaliação não vê o decoder | `classifier_only` sem chave `t5.`/`bridge.`; mesma nota com o decoder zerado |
| nada é cortado | nenhuma entrada passa de 512 tokens e nenhum alvo passa de 64; a contagem é conferida a cada carga de dados |
| a mesma semente reproduz | duas rodadas minúsculas com a mesma semente dão a mesma perda na CPU |
| as contas de passo batem | 78 por época, 624 no total, fase A com 39, fase B até 187 |
| a divisão do gradiente fecha | a soma das perdas dos grupos é igual à `L_aux` do T5; a soma dos gradientes dos grupos é igual a `g_a` (tolerância numérica); as parcelas `share` somam 1 |
| os grupos caem nos tokens certos | com premissa sobre Titã e atmosfera, em "Titan has an atmosphere but the text never mentions its orbit": "but" e "never mentions" em S, "orbit" em N, "Titan" e "atmosphere" em C, "has", "the", "text", "its" e `</s>` em F; S é calculado sem ler o dev |
| medir não muda o treino | mesma semente com e sem `measure_groups()` e `measure_words()`: perdas e pesos finais iguais |
| as palavras dividem o empurrão total | soma dos `align_t` da sonda igual a `dot(g_c, g_a) / norm_c` (tolerância numérica) |

O teste de que o gradiente da `L_aux` chega ao BERT é o mais importante. Se ele falhar, o braço com decoder é só um BERT com uma cabeça a mais que não toca nele, e qualquer resultado não mede o método.

O teste de fumaça (BERT minúsculo de verdade + `bridge` + T5 base de verdade) não entra no pytest, porque baixa cerca de 900 MB do T5. Ele é o comando `--fumaca`, que você roda uma vez na CPU antes de levar o código para a máquina com GPU.

## Passo 28. Confira as decisões que o código carrega

O paper deixa oito pontos em aberto. A tabela mostra as opções e a escolha que o código adota.

| Decisão | Opções | Escolha adotada |
|---|---|---|
| Como o aquecimento da Tabela 4 convive com a fase B | (a) um fator por grupo, como no Passo 13; (b) multiplicar os dois no BERT; (c) só o da fase B para todos | (a): cada aquecimento vale para a parte de que o paper fala |
| Taxa do decoder na fase A | constante 5e-5; com aquecimento próprio | constante: o decoder já é pré-treinado, e a fase A tem só 39 passos |
| Passar o `[CLS]` ao decoder ("Ignore CLS", seção 4.4) | passa; não passa; as duas | passa: a Tabela 3 não dá vantagem a nenhuma; "as duas" dobra a grade |
| Pares do braço BERT sozinho | os mesmos 2.470; os 2.490 | 2.470: o único jeito de os braços diferirem só no decoder |
| Limpeza da abertura (em 96 dos 450 cortes a frase fica sem sujeito) | estreitar a regra; tirar a limpeza; deixar como está | estreitar: cortar só quando o resto é frase inteira; o resto fica com "The text" |
| Onde vive o teste de fumaça | pytest com modelos minúsculos aleatórios + `--fumaca` manual; tudo no pytest | o primeiro: CI sem rede, e o teste de fumaça continua sendo feito |
| Dropout da cabeça | 0,1 (padrão do BERT); nenhum | 0,1, declarado (o paper não diz) |
| Salvar pesos | não salvar; salvar o melhor; salvar todos | não salvar: o resultado é o CSV |

Se você for escrever o código do zero, siga esta ordem:

1. `rte_dados.py`, com os testes de separação entre treino e dev, dos 20 exemplos, da classe positiva, de que nada é cortado, das contas de passo e dos grupos de tokens.
2. `rte_modelo.py`, com os testes de que o braço sem decoder não tem decoder, de que o gradiente da `L_aux` chega ao BERT e de que a avaliação não vê o decoder.
3. `rte_treino.py`, com os testes das fases A e B, da semente, da divisão do gradiente, de que medir não muda o treino e de que as palavras dividem o empurrão. A medida de gradiente fica num `rte_gradientes.py` próprio, chamado pelo laço.
4. O `--fumaca` na CPU.
5. A grade na máquina com GPU.

O código foi escrito com LLM (Claude) a partir das decisões descritas neste manual.
