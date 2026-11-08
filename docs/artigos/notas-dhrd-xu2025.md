# Notas de leitura — DHRD (Xu et al., 2025)

**Referência:** Xu, J.; Zhou, D.; Shukla, V.; Yang, Y.; Ruan, J.; Lin, S.; Zou, W.; Liu, Y.;
Lakshmanan, K. **"Dual-Head Reasoning Distillation: Improving Classifier Accuracy with
Train-Time-Only Reasoning"**. arXiv:2509.21487v2, 29/09/2025. https://arxiv.org/abs/2509.21487
Jillian Xu (University of Waterloo, trabalho feito no Google) + equipe Google / Google DeepMind.

⚠ **Procedência:** Claude leu o PDF (seções 1–5, ablações, limitações e trabalho futuro) em
10/09/2026, e **reconferiu número por número contra o PDF baixado em 10/09/2026** (v2, 12 páginas,
`2509.21487v2-dhrd.pdf` nesta pasta). **Pedro leu e escreveu resumo próprio**
(`Downloads/DHRD Resumo.pdf`, cobre resumo, introdução, trabalho relacionado, método, avaliação,
eficiência, ablação e conclusão) — **nível 1**. Estas notas são nível 2 e não substituem o dele.

**Seção de entregável derivada:** `docs/pesquisa/secao-dhrd-transferencia-encoder.md` (raiz) — o que o DHRD
autoriza e o que não autoriza na transferência para encoder, com nível 1 e nível 2 marcados item por
item, e três correções ao resumo do Pedro.

✅ **Venue RESOLVIDO (10/09/2026):** é **workshop**, não conferência principal. O campo *Comments*
do arXiv (preenchido pelos autores) diz literalmente *"39th Conference on Neural Information
Processing Systems (NeurIPS 2025) Efficient Reasoning Workshop"*. A linha do rodapé do PDF é apenas
o texto padrão do `neurips_2025.sty`, que sai em qualquer submissão — **não é evidência de venue**.
Citar como **NeurIPS 2025 Efficient Reasoning Workshop**.

### Conferência de números (10/09/2026) — tudo confere

Reconferidos contra o PDF: ganho relativo 0,65–5,47% (resumo) · vazão 96–142× (resumo e Tab. 5) ·
toda a Tabela 2 de ablação (87,52 / −1,75% / −5,70% / −48,48% e 81,57 / −3,84% / −20,24% / −45,27%)
· os dois 8B (87,52 e 87,23) acima da média do professor Gemini 2.5 Flash (86,40) · rodada única por
configuração declarada por restrição de computação.

Duas imprecisões corrigidas nestas notas:
- **CB "+8,7%" é ganho RELATIVO, não pontos.** Em pontos: Llama-3.1-8B 81,9 → 89,0 (+7,1);
  Qwen-3-8B 83,5 → 90,8 (+7,3). Os relativos dão 8,7% nos dois. (COPA no Llama-3.2-3B: 72,2 → 89,2,
  +17 pontos = +23,5% relativo — este estava certo.)
- **Pesos ótimos:** α=β=1 para **Llama-3.1-8B, Llama-3.2-3B e Qwen-3-8B**; α=1, β=0,5 só para o
  **Qwen-3-4B**. As notas diziam "os 8B", deixando o 3B de fora.

## Mecanismo

Duas cabeças leves sobre um decoder-only com **atenção causal**:

- Sequência de treino: `sᵢ = [xᵢ, <REASON>, rᵢ, <ANS>, yᵢ]`
- **Cabeça de classificação:** pooling do estado oculto do **último token real da entrada** (antes do
  `<REASON>`) → MLP de 2 camadas → K logits. **Única cabeça usada no teste.**
- **Cabeça de raciocínio:** reaproveita a **cabeça de LM do próprio modelo base**; perda causal
  padrão sobre a sequência inteira. **Só no treino.**
- Objetivo conjunto: `L_total = α·L_cls + β·L_reason`
- Professor: **Gemini 2.5 Flash** com CoT zero-shot ("Let's think step by step")

## Resultados

7 tarefas do SuperGLUE (BoolQ, CB, COPA, MultiRC, RTE, WiC, WSC). Backbones: Llama-3.1-8B,
Llama-3.2-3B, Qwen-3-8B, Qwen-3-4B.

- Ganho relativo sobre o classificador com pooling: **0,65% a 5,47%** (macro-média)
- Maiores ganhos em **CB, RTE, COPA** — implicação e causa. CB +8,7% de acurácia nos dois 8B;
  COPA +23,5% no Llama-3B
- **WiC/WSC estáveis** — os autores dizem: tarefas "menos dependentes de verbalização de múltiplos passos"
- Vazão **96–142× maior** que decodificação CoT
- Os dois 8B com DHRD **superam a média do próprio professor** no SuperGLUE
- Pesos ótimos: α=β=1 para os 8B; β=0,5 para o Qwen-3-4B

## A ablação (o achado central para o tema v3)

| Configuração | Llama-3.1-8B | Llama-3.2-3B |
|---|---|---|
| ConsistentReasoningLabel (alinhado) | referência (87,52) | referência (81,57) |
| **OnlyLabel** (sem racionalização) | **−1,75%** | **−3,84%** |
| **ShuffleReasoning** (racionalização de outro exemplo) | **−5,70%** | **−20,24%** |
| ShuffleReasoningLabel (ambos embaralhados) | −48,48% | −45,27% |

Racionalização alinhada > nenhuma > racionalização errada. Conclusão textual deles: o ganho vem do
**alinhamento entre entrada, racionalização e rótulo**, e *"rather than generic LM regularization"*.

**→ Fecha a disputa entre os dois papers lidos:** no canal de **atenção**, Herrewijnen mostrou que é
**ruído**; no canal de **saída**, DHRD mostra que é **conteúdo**. A ponte teórica do tema v3 (os dois
canais são coisas diferentes) deixa de ser argumento e passa a ter evidência dos dois lados.

**→ Confirma a hipótese do tipo de tarefa**, que estava registrada como hipótese do Claude: ganho
concentrado em implicação/causa, estabilidade onde não há verbalização de passos. Agora é achado
publicado, não conjectura.

## O espaço que sobra para o tema v3 — melhor do que se esperava

Na seção 2 eles citam o **Gemma Encoder** (Suganthan et al.), que adapta decoder-only para encoder
ligando **atenção bidirecional** + pooling + MLP. E declaram a própria escolha:

> *"DHRD deliberately retains causal attention and last-token pooling to prevent future-token
> leakage and match autoregressive pretraining."*

**Eles consideraram a via bidirecional e recusaram, por um motivo declarado: vazamento de token
futuro.** O motivo é válido no desenho deles — racionalização e rótulo estão **dentro da mesma
sequência de entrada**, então atenção bidirecional faria os tokens da entrada enxergarem a resposta.

**No desenho do tema v3 isso não ocorre:** o encoder vê apenas a entrada; a racionalização sai por
cabeça separada via atenção cruzada e **nunca entra na sequência do encoder**. O vazamento que eles
temem não existe nessa arquitetura. Confirmado na fonte: a Eq. (1) põe `xᵢ`, `rᵢ` e `yᵢ` **na mesma
sequência**, e a cabeça de classificação faz pooling do último token real da entrada — com atenção
bidirecional os tokens de `xᵢ` enxergariam `rᵢ` e `yᵢ`. O medo deles é legítimo *no desenho deles*.

**Refinamento encontrado na reconferência:** a justificativa deles tem **duas** metades —
*"to prevent future-token leakage **and match autoregressive pretraining**"*. A segunda metade
também não se aplica: um encoder **é** pré-treinado bidirecionalmente, então não há pré-treino
autorregressivo a respeitar. **Nenhuma das duas metades da razão declarada sobrevive na
arquitetura encoder** — o argumento do tema v3 é mais forte do que estava escrito, não mais fraco.

→ Posição muito mais forte: não é preencher um buraco aleatório, é **mostrar que uma mudança de
desenho remove a razão declarada para o buraco existir.**

## Limitações declaradas = mapa de oportunidades

- *"generalization to other **languages**, modalities, domains, and **architectures** remains
  untested"* — nomeiam língua e arquitetura, que é exatamente o espaço do tema v3.
- **Rodada única, sem intervalo de confiança, por restrição de computação.** Com encoders de 110M
  (rodadas de minutos), o Pedro **pode** rodar várias sementes → melhoria metodológica real sobre o
  vizinho mais próximo.
- Dependência de racionalização de alta qualidade e consistente com o rótulo.
- Sensibilidade ao peso β: 4B regride com β alto (0,5 é mais seguro), 8B tolera β=1.
- Sem comparação controlada por orçamento contra compressão de CoT (HiddenCoT, C3oT, CCoT).

## Trabalho futuro que eles listam

Backbones maiores; busca em grade de α/β; objetivos auxiliares por tarefa (supervisão de span para
WiC/WSC); currículo que reduz gradualmente a perda de raciocínio; **rótulos suaves para a cabeça de
raciocínio** (KL com temperatura entre distribuições de professor e aluno); comparação direta contra
compressão de CoT; variantes híbridas com seleção ou sumarização de racionalização.

## ⚠ Risco novo identificado nesta leitura

A motivação declarada é que o pooling *"under-utilize the model's **latent reasoning abilities
learned in pre-training**"*. O mecanismo assume que **a capacidade já existe** e o treino apenas a
traz à tona.

**Um BERT-base de 110M provavelmente não tem essa capacidade latente.** Se não tiver, a
racionalização teria que **ensinar** em vez de **revelar** — e ensinar é muito mais difícil, com
ordens de magnitude menos parâmetros.

É o risco mais profundo do tema v3, e é de natureza diferente dos anteriores: não é sobre
arquitetura nem sobre tipo de tarefa, é sobre **haver algo lá dentro para trazer à tona**.
Mitigação a considerar: encoder maior e mais moderno (DeBERTa-v3-large, ModernBERT) em vez de
BERT-base. Nada disso foi testado.

## Referência nova a registrar (surgida desta leitura)

**Suganthan et al. (2025), "Gemma Encoder"** — citado duas vezes pelo DHRD: na §2 como o trabalho
que adapta decoder-only para encoder ligando atenção bidirecional + pooling + MLP, e na §3.1 como a
origem da própria cabeça de classificação do DHRD ("following the adaptation proposed in Suganthan
et al. (2025)"). É o vizinho que faz o movimento **oposto** ao do tema v3 (traz o decoder para o
mundo encoder, em vez de levar a racionalização para o encoder que já existe). **Ainda não está em
`docs/pesquisa/artigos-verificados.md`; ID do arXiv não verificado — verificar antes de citar.**

## Tabela 1 completa (conferida na ordem de leitura da página 4, 10/09/2026)

| Modelo | Baseline (pooled) | DHRD | Relativo |
|---|---|---|---|
| Gemini 2.5 Flash (professor, CoT zero-shot) | — | 86,40 | — |
| Llama-3.1-8B | 86,29 | 87,52 | +1,43% |
| Qwen-3-8B | 86,09 | 87,23 | +1,32% |
| Llama-3.2-3B | 77,34 | 81,57 | **+5,47%** |
| Qwen-3-4B | 84,50 | 85,05 | **+0,65%** |

**⚠ Não há tendência por tamanho.** O maior e o menor ganho são os dois de modelos pequenos. O paper
só afirma que o Llama-3.2-3B teve o maior ganho relativo.

**Explicação alternativa relevante para o tema (Claude, 10/09 — não está no paper):** o Llama-3.2-3B
tem o **baseline mais fraco** (77,34 contra 84,50–86,29). O ganho pode ser função de **espaço para
melhorar**, não de tamanho nem de capacidade latente. As duas leituras preveem coisas **opostas** para
um encoder de 110M — espaço prevê ganho grande, capacidade latente prevê ganho nulo. Quatro pontos não
separam; o tema pode.

**Precisão terminológica:** *ShuffleReasoning* é a justificativa **de outro exemplo** (texto coerente,
alinhamento errado), **não** justificativa aleatória. A ablação deles corrompe **alinhamento**, não
**informatividade** — por isso não substitui o controle de tokens aleatórios do Herrewijnen.
