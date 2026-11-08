# Custo de gerar racionalização de LLM para o e-SNLI: teste cru (13/10/2026)

**Pedido do Pedro:** estimar quanto custa gerar racionalizações de LLM, comparando com a API gratuita do Gemini, a
partir de 5 racionalizações geradas como teste.

**Procedência:** os preços do Claude vêm da tabela da skill `claude-api` (cache de 06/10/2026). Os do Gemini vêm de
`ai.google.dev/gemini-api/docs/pricing` (página atualizada em 13/10/2026, lida por ferramenta de resumo). A contagem
de tokens é **aproximada** (palavras × 1,3), não é a do tokenizador.

## 1. As 5 racionalizações

Pares das primeiras linhas do `esnli_dev.csv` (72 linhas baixadas, só o começo do arquivo). As racionalizações do
LLM foram geradas pelo Claude Opus 5.5 nesta sessão, no **mesmo protocolo dos anotadores do e-SNLI**: o modelo recebe
premissa, hipótese e **o rótulo**, e explica por que o rótulo vale. Portanto, são **pós-fixadas**.

| # | Rótulo | Premissa → hipótese | Humana (e-SNLI) | LLM |
|---|---|---|---|---|
| 1 | implicação | Dois meninos de times opostos jogam futebol americano, de uniforme e capacete → "meninos jogam futebol" | *If the boys of opposing teams play football then the boys play football.* | *The premise says two boys are playing football; the hypothesis only drops the details, so it must be true.* |
| 2 | neutro | (mesma) → "meninos marcando um touchdown" | *Boys can refer to more individuals than two young boys. Playing football does not imply they are scoring a touchdown.* | *The boys are playing football, but nothing says anyone is scoring; a touchdown may or may not be happening.* |
| 3 | contradição | (mesma) → "cachorro come numa tigela" | *Boys are not dogs.* | *The premise describes boys playing football, while the hypothesis describes a dog eating; both cannot describe the same scene.* |
| 4 | contradição ⚠️ | Mulher de biquíni dá uma estrela na areia → "dá uma estrela e cai de cabeça" | *A woman doing a cartwheel as opposed to a woman falling while doing a cartwheel.* | *Doing a cartwheel means completing the move, while falling on her head means it failed; the same moment cannot be both.* **(forçada)** |
| 5 | neutro | Homem de terno preto tocando com a orquestra → "uma pessoa alta de terno" | *Not all tall people are men.* | *A man in a suit is a person in a suit, but the premise says nothing about his height.* |

### O que o teste já mostra

- **Válidas:** 5 de 5 são coerentes com o rótulo. A nº 4 é **forçada**: o `pairID` termina em `n`, o que indica que a
  hipótese foi escrita como neutra e o voto da maioria a tornou contradição. O rótulo é discutível, e o LLM
  racionalizou mesmo assim. **É o sentido psicológico da palavra, ao vivo:** com o rótulo dado, o LLM sempre acha
  uma justificativa, inclusive para rótulo ruim.
- **Humana × LLM:**
  - as humanas são curtas, moldadas ("not all X are Y", "X are not Y") e às vezes erram o alvo (nº 5: o problema é
    a altura, não o "homem");
  - as do LLM são mais longas, explícitas e uniformes.
  - Isso é o que o passo 2 da trilha mede do lado humano.
- **A nº 3** mostra uma regra do SNLI que nem a humana nem a do LLM explicitam: contradição pressupõe **a mesma
  cena** (a mesma foto).

## 2. Tamanho por exemplo

| Parte | Tokens (aprox.) |
|---|---|
| Entrada: instrução (~60) + premissa e hipótese (~40) + rótulo | ~120 |
| Saída: racionalização de 1 a 2 frases | ~45 |

Sem raciocínio interno. No Haiku 5.5 dá para desligar (`thinking` desativado é aceito em esforço `high` ou abaixo).
No Opus 5.5 **não** dá: o raciocínio fica sempre ligado e soma tokens de saída que esta conta não inclui.

## 3. Custo estimado (USD)

| Modelo | Preço entrada / saída (por 1M) | 10 mil pares | Treino inteiro (549 mil) | Lote (−50%), treino inteiro |
|---|---|---|---|---|
| **Claude Haiku 5.5** | $0,10 / $0,50 | **~$0,35** | **~$19** | **~$10** |
| Claude Sonnet 5.5 | $2 / $10 | ~$7 | ~$380 | ~$190 |
| Claude Opus 5.5 | $4 / $20 | ~$14 + raciocínio | ~$760 + raciocínio | ~$380 + raciocínio |
| Gemini 2.5 Flash-Lite (pago) | $0,10 / $0,40 | ~$0,30 | ~$17 | ~$8 |
| **Gemini (nível gratuito)** | $0 | $0 | $0 | — |

## 4. O nível gratuito do Gemini

- **Existe** para os modelos Flash e Flash-Lite (2.5, 3.x), segundo a página de preços.
- **O limite diário de pedidos não está na documentação.** A página de limites (13/10/2026) manda consultar o AI
  Studio (`aistudio.google.com/rate-limit`). **Sem esse número não dá para estimar o tempo**, e eu não vou chutar.
- **No nível gratuito, os dados são usados para melhorar os produtos do Google**, segundo a coluna "Used to improve
  our products" da mesma página. Para o e-SNLI, que é público, isso não é problema.
- **Reprodutibilidade:** modelo "preview" e limites que mudam são ruins para experimento. Ao usar, é preciso
  registrar o nome exato do modelo e a data.

## 5. Leitura

- "Sem verba para API" precisa ser revisto à luz dos números. Com o **Haiku 5.5 em lote, o treino inteiro sai por
  ~$10**, e um subconjunto de 10 mil sai por centavos. Decisão do Pedro.
- O gargalo **não é o custo**. É a decisão de desenho: qual professor, com ou sem rótulo no prompt (pós × pré), e
  quantos pares.
- **Isto não é o experimento.** Cinco exemplos servem para estimar custo e enxergar o formato, não para concluir
  nada sobre qualidade.

## 6. Orçamento real (Pedro, 13/10)

- **US$ 100 de crédito de API da Anthropic.** Isso cobre o treino inteiro com Haiku 5.5 em lote (~US$ 10) com folga
  para repetir, testar prompts e comparar com e sem rótulo. Um subconjunto com Sonnet 5.5 também cabe.
- **US$ 250 de sessões na nuvem do Claude Code.** Não é crédito de API. Pode servir para um piloto ou para treino,
  se a sessão tiver GPU (não confirmado).
- A premissa "sem verba para API" caiu. **Qual modelo, quantos pares e com ou sem rótulo no prompt continuam sendo
  decisão do Pedro.**

## 7. Piloto rodado (13/10, 21h31 → 21h42)

Lote `msgbatch_013JKrdwE7T122imLFDRJETk`: 1.000 pares da validação × {Haiku 5.5, Sonnet 5.5}, prompt pós-fixado,
esforço `low`. **2.000 de 2.000 com sucesso, 0 falhas, ~11 min, US$ 0,64.** Arquivos em
`resultados/piloto-professores/` (`resultados.csv`, `custo.md`, `gerar.py`).

**Tokens reais por par:** ~203 de entrada (a estimativa era 120, porque o prompt com as definições é maior); saída
de ~99 no Haiku e ~80 no Sonnet (a estimativa era 45).

**Estimativa refeita (lote):**

| Pares | Haiku 5.5 | Sonnet 5.5 |
|---|---|---|
| 100 mil | ~US$ 3,50 | ~US$ 60 |
| 549 mil (treino inteiro) | ~US$ 19 | ~US$ 330 (não cabe nos US$ 100) |

**Primeiras observações (Claude, sobre `resultados.csv`):**

- Tamanho mediano: humano 12 palavras · Haiku 50 · Sonnet 45. As do LLM são ~4× maiores.
- Citam o nome do rótulo, mesmo com instrução para não citar: humano 0,3% · Haiku 6,1% · Sonnet 1,7%.
- **As do LLM repetem as definições dos rótulos que estavam no prompt** ("must also be true", "neither guarantees
  nor rules out"). É vazamento do rótulo por paráfrase, e é o mesmo padrão de petição de princípio que o Pedro
  observou nas humanas, só que vindo do prompt. **Decisão de desenho para o experimento real:** tirar as
  definições do prompt, ou aceitar e medir.
- Há explicação humana errada no meio (par 400: *"You can not infer the child is playing with a container"*, quando a
  premissa diz que ele brinca com potes plásticos).

## 8. Licença: pode treinar com saída do Claude? (levantado pelo Pedro, 14/10)

**Commercial Terms da Anthropic** (vigência 17/06/2025, §D.4, lidos em 14/10/2026):

> "Customer may not and must not attempt to (a) access the Services to build a competing product or service,
> including to train competing AI models or resell the Services except as expressly approved by Anthropic; (b)
> reverse engineer or duplicate the Services"

- A cláusula não fala em "destilação". Ela proíbe treinar **modelos concorrentes**.
- Um classificador encoder de NLI, pequeno e acadêmico, é "concorrente" do Claude? **É questão de interpretação
  jurídica**, e não cabe ao Claude decidir. Há uma saída prevista no próprio texto: "except as expressly approved
  by Anthropic".
- **Alternativa sem ambiguidade:** professor de pesos abertos com licença permissiva. `Qwen/Qwen3-8B` e
  `Qwen/Qwen3-4B` estão sob Apache 2.0 (tag de licença no HF, conferida em 14/10). Podem rodar localmente (8 GB, com
  quantização) ou num provedor.
- O Gemini tem termos próprios. Conferir antes de usar (não lido).
- **Decisão do Pedro.** O piloto (avaliação e cópia) não treina modelo nenhum.

**Decisão do Pedro (14/10):** manter o Claude como professor, sem publicar os pesos do modelo nem o dataset gerado.
**Nota do Claude:** a cláusula restringe o *treino* de modelo concorrente, não a publicação. Não publicar reduz a
exposição, mas não muda a leitura da cláusula. O argumento que sustenta o uso é outro: o classificador de NLI não
concorre com o Claude. Não é parecer jurídico. A alternativa de pesos abertos (Qwen3, Apache 2.0) continua
disponível.
