# Geração do dataset: como não errar o prompt, e o risco da licença (19/10/2026)

**Pedido do Pedro (19/10):** a semana é do dataset. Ele tem duas preocupações:
1. só há uma chance de gerar, por causa do orçamento, e um prompt ruim não pode passar;
2. medo de a Anthropic processá-lo por destilar o Claude. Pediu para procurar quem já fez algo parecido com o Claude
   ou com o ChatGPT.

**Procedência.**
- Termos da Anthropic: lidos na fonte em 19/10 (`anthropic.com/legal/commercial-terms`, por ferramenta de resumo, com
  citações literais).
- Post da Anthropic sobre ataques de destilação: idem.
- Cartão do Tülu 3 no Hugging Face: idem.
- Notícias e artigos jurídicos: **nível 3**, só resultados de busca e resumos. Servem para saber que o caso existe,
  não para citar.
- Preços e classificadores da API: skill `claude-api` (cache de 06/10/2026).
- **Nada aqui é parecer jurídico.**

---

## Parte 1: a geração não precisa ser uma chance só

### 1.1 Onde o dinheiro vai

O piloto de 13/10 custou **US$ 0,64** por 2.000 justificativas (`resultados/piloto-professores/custo.md`). Por par,
em lote:

| Professor | Entrada | Saída | Por par | 100 mil pares |
|---|---|---|---|---|
| Haiku 5.5 | 203 tokens × US$ 0,05/M | 99 tokens × US$ 0,25/M | ~US$ 0,000035 | **~US$ 3,50** |
| Sonnet 5.5 | 203 tokens × US$ 1/M | 80 tokens × US$ 5/M | ~US$ 0,0006 | **~US$ 60** |

**Dois terços do custo do Sonnet são saída.** Justificativa mais curta é a alavanca de custo mais forte. Com ~45
tokens de saída, os 100 mil pares saem por ~US$ 43.

O risco real não é testar o prompt, porque teste é barato. **O risco real é a rodada grande sair errada.** Ela é a
única etapa que consome o orçamento, e dá para dividi-la.

### 1.2 Protocolo em quatro rodadas

Cada rodada só começa depois de o Pedro aprovar a anterior.

| Rodada | O que faz | Pares | Custo (Sonnet) | Custo (Haiku) |
|---|---|---|---|---|
| **0. Régua** | Escrever os critérios de aceite e o script de checagem automática. Rodar sobre as 2.000 justificativas que **já existem** do piloto, para ter a linha de base de falhas | 0 novos | **US$ 0** | US$ 0 |
| **1. Variantes** | 3–4 versões do prompt, **mesmos pares** para todas. Amostra estratificada, com mais neutros e mais pares de rótulo disputado. Checagem automática em tudo; avaliação às cegas do Pedro em ~20 por finalista | ~300 × 4 | ~US$ 0,80 | ~US$ 0,05 |
| **2. Confirmação** | A vencedora roda em **1.000 pares novos**, nunca vistos no ajuste, para ver se as métricas se mantêm. É a proteção contra ajustar o prompt aos 300 pares da rodada 1 | 1.000 | ~US$ 0,60 | ~US$ 0,04 |
| **3. Rodada grande, em lotes** | Primeiro um **lote canário de 5 mil**, com checagem automática. Depois o resto, em lotes independentes. O `custom_id` = `pairID`, e só as falhas são reenviadas | 5 mil + resto | ~US$ 3 + resto | ~US$ 0,20 + resto |

**Total arriscado antes da rodada grande: menos de US$ 5, mesmo com o Sonnet.** Se o canário mostrar problema, a
perda é de ~US$ 3, não de US$ 60. Prompt congelado entre a rodada 2 e a 3 = texto idêntico (guardar o hash no
`estado.json`).

### 1.3 Checagens automáticas (rodada 0)

Tudo mensurável por script, sem chamar API. As quatro primeiras já apareceram no piloto (`docs/2026-10-13-custo-racionalizacao-llm.md` §7):

| Checagem | Por quê | No piloto |
|---|---|---|
| Cita o nome do rótulo | Vazamento direto | Haiku 6,1% · Sonnet 1,7% |
| Repete a definição do rótulo que estava no prompt ("must also be true", "neither guarantees nor rules out") | Vazamento por paráfrase; parecido com a circularidade que o Pedro marcou | frequente, não contado |
| Tamanho em palavras | Custo, e diferença de 4× para o humano (12 × 45–50) | mediana 45–50 |
| Taxa de cópia do par (`copia.py`, já existe) | Mesma régua usada nas humanas | 42–49% |
| `stop_reason` ≠ `end_turn`, texto vazio, recusa | Falha de geração. Ver o classificador `frontier_llm` na Parte 2 | 0 de 2.000 |
| Palavras de hesitação ("might", "may") em implicação, ou certeza em neutro | Justificativa que contradiz o próprio rótulo | não medido |

**Opcional, centavos:** pedir ao Haiku que adivinhe o rótulo **só pela justificativa, sem o par**. Se acertar quase
sempre, a justificativa carrega o rótulo, e a cabeça auxiliar aprende o rótulo de novo em vez de aprender o porquê. A
ideia tem nome na literatura: *leakage-adjusted simulatability* (Hase et al., 2020, Findings of EMNLP). **Citado de
memória, conferir antes de usar.**

### 1.4 O que as variantes testam (decisões do Pedro, não do Claude)

As perguntas que já estavam abertas no HANDOFF viram variantes **medidas**, em vez de escolha no escuro:

| Variante | Muda | Hipótese que testa |
|---|---|---|
| A | prompt do piloto, igual | linha de base |
| B | **sem as definições de rótulo** | a paráfrase da definição some? a correção cai? |
| C | B + **exemplos escolhidos pelo Pedro** (por exemplo, os que ele marcou `ssn` e "melhor" na avaliação) | exemplo bom ensina o tom e o tamanho melhor que instrução |
| D | C + limite explícito ("uma frase, até ~25 palavras; diga o fato da premissa que decide") | mais curta e menos circular, a menor custo |

- **Exemplos quase não custam.** No Haiku 5.5 e no Sonnet 5.5, o prefixo mínimo cacheável é de **512 tokens**.
  Um bloco fixo de exemplos acima disso é cobrado a ~0,1× na leitura de cache. No lote, o cache funciona por melhor
  esforço.
- Wiegreffe et al. (2022, NAACL), que geraram explicações do GPT-3 **para o próprio e-SNLI**, relatam que a qualidade
  dos exemplos no prompt muda a qualidade da explicação (nível 3, só resultado de busca; ler antes de citar).
- **Com ou sem rótulo no prompt** e **qual professor** podem entrar como eixo extra da rodada 1 (custa o dobro, ainda
  centavos no Haiku).
- **Não mudar o raciocínio em silêncio.** O piloto usou esforço `low` com o raciocínio adaptativo ligado. Desligar
  (`between_tools` no Sonnet) muda a qualidade; se for testado, entra como variante.

---

## Parte 2: licença e precedentes

### 2.1 O que o contrato diz (Commercial Terms, vigência 17/06/2025, lidos em 19/10)

- **§D.4:** proíbe usar os serviços "to build a competing product or service, including to train competing AI
  models", **"except as expressly approved by Anthropic"**. Proíbe também "reverse engineer or duplicate the Services".
- **§B:** o cliente **é dono das saídas** ("owns its Outputs"), e a Anthropic cede a ele os direitos que tiver
  sobre elas, condicionado ao cumprimento dos termos.
- **Consequência prevista no próprio contrato:** **suspensão** do acesso por violação do §D.4 (§I.3.a) ou rescisão
  com aviso de 30 dias e prazo para corrigir (§I.2.b). Lei aplicável: Califórnia (fora da UE/Reino Unido).
- **Não há cláusula sobre uso acadêmico.** Nem permite, nem proíbe.
- **⚠️ CORREÇÃO (20/10): faltou a Usage Policy.** O §D.2 dos Commercial Terms incorpora a Usage Policy por
  referência. A versão em vigor (desde 15/09/2025; conferida no snapshot do Wayback Machine de 31/08/2026), na seção
  "Do Not Abuse our Platform", proíbe: *"Utilization of inputs and outputs to train an AI model (e.g., "model
  scraping" or "model distillation") without prior authorization from Anthropic"*. A versão nova, que entra em vigor
  em **12/11/2026**, mantém a regra: *"Use outputs to train an AI model (...) without prior authorization from
  Anthropic"*. **A regra vale para qualquer modelo de IA, não só para concorrente.** O argumento "o classificador NLI
  não concorre com o Claude" responde ao §D.4, mas não a esta cláusula. A violação da Usage Policy também permite
  suspensão (§I.3.a cita o §D.2). A saída é a mesma do §D.4: autorização prévia. O e-mail de 19/10 ao suporte cita
  só o §D.4, então precisa de complemento.
- **Artigo de suporte "Can I use my Outputs to train an AI model?"** (16/03/2026, trazido pelo Pedro em 20/10 e
  conferido na fonte). O artigo:
  - abre repetindo a regra geral: treinar ou "develop" modelo exige permissão escrita;
  - **permite** treinar modelos não concorrentes, como "specialized classifiers" (cita análise de sentimento e
    "content categorization"). O classificador NLI de 3 classes cabe aqui;
  - **proíbe**, numa lista sob "models that are competitive", entre outros, "Using Outputs as training targets for
    models".

  O ponto ambíguo é exatamente o nosso: o modelo final é um classificador permitido, mas a cabeça decoder auxiliar,
  descartada, usa as saídas como alvo de treino. O artigo não fala de avaliação, uso como referência, dados
  sintéticos nem uso acadêmico.
- **Contorno por outro LLM guiado pelas saídas do Claude: descartado (20/10).** Gerar o dataset com outro modelo
  usando as saídas do Claude como guia continua sendo "develop" com o sinal do Claude. Um desenho feito para tirar a
  letra da regra e manter o sinal é o que o §D.4(c) e a Usage Policy ("intentionally bypass") punem. Também fere a
  regra do projeto de não disfarçar o uso de LLM. Usar as saídas **só** para avaliar ou comparar, sem selecionar nem
  filtrar dado de treino, é análise. Isso continua livre.

### 2.2 Quem já fez algo parecido

| Quem | Professor | O que fez | Publicou? | O que aconteceu |
|---|---|---|---|---|
| **Tülu 3** (Allen Institute for AI, 2024) | **Claude 3.5 Sonnet**, GPT-4o, GPT-4 Turbo e outros | Dados de preferência para treinar um **modelo de linguagem aberto**, concorrente direto | Sim. Dataset sob ODC-BY, com a nota *"Outputs produced by Claude are subject to Anthropic terms of service and usage policy"* (lido no cartão, 19/10) | Não encontrei notícia de ação |
| **Alpaca** (Stanford, 2023) | text-davinci-003 (OpenAI) | 52 mil demonstrações para treinar o LLaMA 7B | Sim, para uso não comercial; a demonstração saiu do ar uma semana depois (nível 3; o motivo não foi verificado) | Não encontrei notícia de ação |
| **Ho, Schmid & Yun** (2023, ACL) | GPT-3 175B | Justificativas do professor para ajustar alunos pequenos (Fine-tune-CoT) | Sim, código e dados no GitHub | Nenhuma conhecida |
| **Wiegreffe et al.** (2022, NAACL) | GPT-3 | Explicações em texto livre **para o e-SNLI** e o CommonsenseQA, avaliadas contra as humanas | Sim | Nenhuma conhecida |
| **DHRD** (Xu et al., 2025; Pedro leu) | Gemini 2.5 Flash | Justificativas do Gemini para treinar **Llama e Qwen**, que são decoders gerativos | Sim, workshop do NeurIPS | Nenhuma conhecida |
| Agrawal et al. (2025; Pedro leu) | **Mixtral**, aberto | Mesma ideia sobre BERT. A Amazon escolheu professor aberto | — | — |

**Leitura:** destilar justificativa de LLM comercial para modelo pequeno é prática comum em artigo publicado. Vários
casos concorrem muito mais com o professor do que um classificador de NLI: o Tülu 3 e o DHRD treinam modelos que
geram texto. Não ter achado notícia de ação não prova que ela não existiu. Mas os casos abaixo, que são públicos, têm
outro perfil.

### 2.3 Quando a Anthropic agiu

| Quando | Contra | O que motivou | O que a Anthropic fez |
|---|---|---|---|
| ago/2025 | **OpenAI** | Usar o Claude em ferramentas internas para comparar com os próprios modelos antes do GPT-5 | **Cortou o acesso à API**, mas manteve o acesso para benchmark e avaliação de segurança. Sem processo |
| fev/2026 | **DeepSeek, Moonshot, MiniMax** | >16 milhões de trocas por ~24 mil **contas fraudulentas** e proxies, contornando a restrição regional, inclusive extraindo cadeia de raciocínio | Banimento de contas, detecção, compartilhamento de indicadores com outros laboratórios e autoridades. **O post não menciona processo** |

No próprio post de 23/02/2026, a Anthropic chama a destilação de *"a widely used and legitimate training method"*. O
problema que ela aponta é o uso ilícito: fraude, contornar restrição regional, concorrente comercial e escala
industrial.

### 2.4 O que dizem os juristas (nível 3)

- **Henderson & Lemley (2024)**, *The Mirage of Artificial Intelligence Terms of Use Restrictions* (arXiv:2412.07066):
  - as saídas de modelo provavelmente não têm proteção de direito autoral, então resta o contrato;
  - fora a suspensão de contas, **nenhum criador de modelo tentou cobrar multa ou pedir liminar** com base nesses
    termos;
  - cláusulas anticoncorrência são as mais frágeis.
- Comentário de juristas sobre OpenAI × DeepSeek (Chander, Kortz, via notícia): a via plausível seria quebra de
  contrato, não propriedade intelectual.

### 2.5 Uma checagem técnica que já rodou a favor

O Haiku 5.5 e o Sonnet 5.5 têm um classificador de segurança, `frontier_llm`, que **recusa pedidos que "could assist
the development of competing AI models"** (documentação da API, via skill `claude-api`). É a própria Anthropic
filtrando destilação na entrada. **No piloto, 2.000 de 2.000 pedidos passaram, com 0 recusas.** Não é permissão
jurídica, mas mostra que o sistema dela não viu essa carga como desenvolvimento de modelo concorrente. Na rodada
grande, a taxa de recusa vira uma das checagens (§1.3). Se subir, parar e reavaliar.

**O que não fazer:** disfarçar o prompt para passar no classificador. Isso seria a conduta que os termos punem, e
contraria a regra do projeto de nunca esconder o uso de LLM.

### 2.5.1 As defesas novas de outubro de 2026 (verificado em 20/10)

O Pedro trouxe um texto (fonte não identificada) dizendo que as defesas da Anthropic podem bloquear ou banir quem
gera justificativas em lote. Conferido na fonte primária, *Strengthening our defenses against distillation attacks*
(anthropic.com/research/distillation-defenses, 12/10/2026), e em duas notícias (NeoTeo e Tech Insider, 13/10).

| Afirmação do texto | O que a fonte diz |
|---|---|
| As defesas miram a "destilação de raciocínio (rationale distillation)" | Miram o **raciocínio oculto** (os tokens de *thinking*), não a saída visível. O post diz que as defesas focam quase só em tornar o raciocínio do Claude difícil de acessar, e que a detecção funciona porque usuário comum raramente pede ao modelo para reproduzir o raciocínio inteiro |
| O *Preserved Thinking* é barreira contra o seu caso | É a proibição de **editar o contexto anterior** (os blocos de raciocínio) em conversas de várias voltas, para contas criadas a partir de 31/08/2026. O `gerar.py` faz um pedido por par, de uma volta, sem devolver bloco nenhum. Não se aplica |
| Pedido em lote de justificativas é "comportamento idêntico" ao dos banidos | Os banidos fizeram **tentativas repetidas e persistentes** de extrair raciocínio, com milhares de contas e técnicas de extração (um laboratório testou 12 mil técnicas diferentes). Uma conta pedindo uma explicação curta e visível não é o mesmo padrão. O post não fala de uso acadêmico nem de dados sintéticos |
| Os filtros podem bloquear os pedidos | **Verdade.** O classificador erra em menos de 0,1% dos pedidos benignos, segundo a própria Anthropic. Desde 24/09/2026, pedido bloqueado antes da resposta é **cobrado** nessa categoria |
| Podem banir a conta automaticamente | O banimento é para tentativas repetidas e persistentes de destilação. Não há menção a ban por bloqueio ocasional |

**O fato mais forte:** o piloto rodou em **13/10, um dia depois do post**, já com essas defesas no ar. Foram 2.000 de
2.000 pedidos sem nenhuma recusa.

**O que fazer, sem disfarçar nada:**
1. O prompt pede **só a explicação**, sem "pense passo a passo", sem pedir para mostrar o raciocínio e sem
   `display: "summarized"`. O piloto já era assim.
2. O `gerar.py` passa a registrar `stop_details.category` das recusas, para saber qual classificador disparou.
3. **Regra de parada no canário:** se as recusas passarem de ~0,5% (5× o erro declarado), parar e reavaliar antes do
   resto.
4. Com 0,1% de erro, 100 mil pedidos dão ~100 bloqueios, cobrados por centavos. Os pares bloqueados ficam sem
   justificativa e são marcados, não reenviados em loop. Reenviar o mesmo pedido bloqueado repetidas vezes é o que
   se parece com "tentativa persistente".
5. Opcional, como variante da rodada 1: desligar o raciocínio no Sonnet (`thinking: {type: "between_tools"}`). Não
   há raciocínio oculto para ninguém suspeitar, mas a qualidade pode mudar, e por isso precisa ser medida.

### 2.6 Leitura do risco (Claude, não é parecer)

- **Pior caso realista:** suspensão da conta da API. É a única sanção que o contrato prevê de forma direta e a única
  que a Anthropic já aplicou, mesmo contra laboratórios com fraude em escala de milhões.
- **Processo:** não achei precedente nenhum, nem contra os casos mais graves.
- **O perfil do Pedro é o oposto do perfil sancionado:** uma conta, identidade real, ~100 mil pedidos curtos, uso
  acadêmico, sem publicar dataset nem pesos (decisão dele, 14/10). E o modelo final é um classificador de ~110M que
  **não gera texto**, então não substitui o Claude em nada.
- **O ponto que segue aberto:** "concorrente" não está definido no contrato. O argumento continua sendo o de 14/10: o
  classificador de NLI não concorre com o Claude.

### 2.7 Três atitudes que reduzem o risco sem mudar o desenho

1. **Declarar no texto:** modelo exato (`claude-sonnet-5-5` ou `claude-haiku-5-5`), data, uso via API sob os
   Commercial Terms, dataset não redistribuído. O Tülu 3 fez a mesma coisa no cartão do dataset.
2. **Pedir a aprovação expressa que o próprio §D.4 prevê** ("except as expressly approved by Anthropic"): um e-mail
   ao suporte descrevendo o projeto. Custa um e-mail e fecha a ambiguidade. Pode demorar mais que a semana; gerar sem
   resposta continua sendo decisão do Pedro.
   **Feito (Pedro, 19/10):** mensagem enviada ao suporte da Anthropic. Resposta pendente.
3. **Gerar tudo de uma vez, em poucos lotes.** Se a conta for suspensa depois, os dados já gerados continuam com ele
   (§B: ele é dono das saídas).

---

## Decisões que ficam com o Pedro

1. Rodar a rodada 0 (script de checagem sobre o piloto, sem custo de API)?
2. Quais variantes entram na rodada 1 (A–D, com ou sem rótulo, um ou dois professores)?
3. Quantos pares na rodada grande (100 mil? treino inteiro?) e qual professor. O professor pode sair da rodada 1.
4. Mandar ou não o e-mail pedindo aprovação expressa à Anthropic.

## Fontes

- [Anthropic Commercial Terms](https://www.anthropic.com/legal/commercial-terms)
- [Anthropic, *Detecting and preventing distillation attacks* (23/02/2026)](https://www.anthropic.com/news/detecting-and-preventing-distillation-attacks)
- [Tülu 3, cartão do dataset `tulu-3-sft-reused-on-policy-70b`](https://huggingface.co/datasets/allenai/tulu-3-sft-reused-on-policy-70b/blob/main/README.md)
- [TechCrunch, corte do acesso da OpenAI (02/08/2025)](https://www.techcrunch.com/2025/08/02/anthropic-cuts-off-openais-access-to-its-claude-models)
- [Henderson & Lemley, arXiv:2412.07066](https://arxiv.org/pdf/2412.07066)
- [Monash Lens, destilação e direito autoral](https://lens.monash.edu/ai-distillation-and-the-law-why-learning-from-claude-or-gpt-may-not-be-copyright-infringement/)
- [Ho, Schmid & Yun 2023, arXiv:2212.10071](https://arxiv.org/abs/2212.10071v2)
- [Wiegreffe et al. 2022, NAACL](https://aclanthology.org/2022.naacl-main.47)
- [Alpaca, verbete de wiki (nível 3)](https://aiwiki.ai/wiki/alpaca/raw)
