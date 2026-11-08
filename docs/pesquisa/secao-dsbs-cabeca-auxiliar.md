# Seção para o entregável — o que o Distilling Step-by-Step autoriza no desenho da cabeça auxiliar

Destino: seção nova do resumo `Distilling Step-by-Step.pdf`. Reúne as extrações do paper que
**licenciam** treinar uma cabeça auxiliar de racionalização e **removê-la depois**, que é o mecanismo
do tema v3 (H2).

## ⚠ Procedência desta seção

| Item | Quem leu | Nível |
|---|---|---|
| Toda a base do resumo, incluindo a frase "Comparado com a destilação padrão, r̂ᵢ não é necessário durante a inferência" | **Pedro**, lendo o paper | **1 — citável** |
| Números da Tabela 2, localização das seções e trechos em inglês acrescentados abaixo | Claude, extraindo o PDF v2 (arXiv:2305.02301v2) em 10/09/2026 | **2 — conferir na fonte antes de assinar** |

Tudo marcado **[C]** abaixo é acréscimo do Claude e precisa da sua conferência na página indicada
antes de entrar em texto assinado. O resto já é seu.

---

## 1. A racionalização é sinal de treino, não de inferência

Esta é a licença central, e é a frase que você já tinha extraído:

> Comparado com a destilação padrão, **r̂ᵢ não é necessário durante a inferência**.

**[C] Localização e original:** §3.2, imediatamente após a Eq. 4 — *"the rationale r̂ᵢ is not required
in the test time, which removes the need for an LLM at test-time"* (Hsieh et al., 2023).

**O que autoriza:** se a racionalização não é produzida na hora de responder, o ganho não vem de
computação em tempo de inferência — vem de **sinal de treino**. E sinal de treino não está preso à
arquitetura que o consumiu. É o que permite perguntar se um encoder pode receber o mesmo sinal.

## 2. Os próprios autores declaram o desenho como "só no treino"

**[C]** Na seção *Limitations* (última página), a segunda limitação diz que treinar com
racionalização traz *"slight training-time computation overhead"*, e completa que, no teste, o
desenho multi-tarefa evita esse custo porque permite prever só os rótulos, sem gerar as
racionalizações.

**O que autoriza:** a remoção da racionalização na entrega **não é uma adaptação nossa** — é
propriedade declarada do método original. O tema v3 leva isso um passo adiante: em vez de deixar de
usar a saída de racionalização, **descarta a cabeça inteira**.

## 3. A ablação de design de treino — a licença mais forte, e a que estava solta no resumo

Você já registrou o achado ("o treinamento multitarefa é superior à predição conjunta em tarefa
única"). **[C]** Ele tem número, e o número é o argumento:

**§4.4, Tabela 2** — T5 de 220M, 100% dos dados em todos os datasets:

| Método | e-SNLI | ANLI | CQA | SVAMP |
|---|---|---|---|---|
| Fine tuning padrão | 88,38 | 43,58 | 62,19 | 62,63 |
| **Tarefa única** (concatena r̂ᵢ e ŷᵢ numa sequência só, Eq. 5) | 88,88 | **43,50** | **61,37** | 63,00 |
| **Multi-tarefa** (saídas separadas) | **89,51** | **49,58** | **63,29** | **65,50** |

**Concatenar racionalização e rótulo na mesma sequência de saída chega a ser PIOR que não usar
racionalização nenhuma** — em ANLI e CQA, abaixo do fine tuning padrão. Os autores citam
Wiegreffe et al. 2021, Magister et al. 2022 e Ho et al. 2022 como tendo observado o mesmo.

**O que autoriza — e é o ponto que faltava conectar:** o benefício da racionalização depende de
**onde a saída sai**. Misturar os dois alvos no mesmo canal de saída destrói o ganho; separá-los
recupera. No T5 a separação é feita por **prefixos de tarefa** (`[label]` / `[rationale]`
prependidos à entrada, §3.2), que é uma separação *lógica* — o mesmo decoder produz as duas coisas.

→ Uma **cabeça auxiliar fisicamente separada** é a forma mais extrema dessa separação: não há
sequência compartilhada, não há prefixo a resolver, não há como um alvo contaminar o outro. A
ablação do paper aponta na direção do desenho do tema v3, não contra ele.

→ E gera **previsão testável** para o tema: se o que importa é a separação dos canais de saída,
cabeças separadas devem ir melhor que qualquer variante que ponha racionalização e rótulo na mesma
sequência. É comparável no mesmo experimento.

## 4. Racionalização como ENTRADA foi considerada e rejeitada

**[C]** §3.2 discute a alternativa `f(xᵢ, r̂ᵢ) → ŷᵢ` (Eq. 2), e a rejeita porque exigiria um LLM
disponível na hora de responder — citam o PINTO (Wang et al. 2022a) nominalmente por depender de
geração de racionalização no teste. Você já tinha a troca registrada: `f(xᵢ, r̂ᵢ) → ŷᵢ` vira
`f(xᵢ) → (ŷᵢ, r̂ᵢ)`.

**O que autoriza:** a racionalização tem que ser **alvo**, nunca entrada. Para um encoder, que não
gera texto, isso deixa exatamente duas formas de ser alvo — prever o **vetor** da racionalização
(H1) ou prever a **sequência** dela por uma cabeça acoplada (H2). O paper fecha as outras portas,
e é por isso que o espaço de hipóteses do tema v3 tem só duas entradas.

## 5. A perda é uma soma ponderável

**[C]** §3.2, Eqs. 1 e 4: `L = L_label + L_rationale`, as duas entropia cruzada sobre tokens.

**O que autoriza:** a estrutura de soma é o que permite a grade do tema v3
(`L = α·L_classificação + β·L_embedding + γ·L_geração`), onde zerar um termo é o próprio braço de
ablação. Não é invenção nova de objetivo — é a mesma forma, com um termo a mais.

## 6. O professor não precisa ser gigante

**[C]** §4.4, Tabela 1: com racionalização extraída de um **GPT-NeoX de 20B** em vez do PaLM 540B, o
método **ainda supera** o fine tuning padrão (e-SNLI 89,12 vs. 88,38; SVAMP 63,00 vs. 62,63) — mas o
ganho é **menor**, e os autores atribuem à qualidade da racionalização do modelo maior.

**O que autoriza:** professor aberto e local é viável, o que é a diferença entre o projeto existir e
não existir sem verba de API. Com a ressalva declarada: **parte do efeito se perde**, e a qualidade
do professor é variável, não constante.

---

## O que este paper NÃO autoriza — declarar junto

Três limites, para a seção não prometer o que a fonte não sustenta:

1. **Nada aqui foi testado em encoder.** Todo o paper é T5 (encoder-decoder). A transferência para
   encoder-only é a pergunta do tema, não um resultado do paper.
2. **A ablação de design de treino é um ponto, não uma curva** — T5 de 220M, 100% dos dados, uma
   configuração por linha. Não há sementes múltiplas nem intervalo de confiança na Tabela 2.
3. **Não há controle com racionalização aleatória ou embaralhada.** O paper não separa "conteúdo da
   racionalização" de "efeito de ter um objetivo auxiliar qualquer". Quem fecha essa lacuna são o
   DHRD (ablação de embaralhamento) e o Herrewijnen (tokens aleatórios) — e é por isso que o
   controle aleatório é obrigatório no desenho do tema v3.

## Uma frase para fechar a seção

O Distilling Step-by-Step estabelece que a racionalização de um LLM funciona como **objetivo de
saída em tempo de treino** e é **dispensável na inferência**; e a própria ablação dele mostra que o
ganho depende de manter esse objetivo em um **canal de saída separado** do rótulo. As duas coisas
juntas são a licença para pendurar uma cabeça de racionalização num encoder, treinar, e removê-la
antes de entregar.
