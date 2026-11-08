# As perdas do H2, peça por peça: I, ∇θ L e ΔL (20/10/2026)

Material de estudo para ler a álgebra de `L = L_cls + λ·L_aux` que o Pedro trouxe da conversa de 20/10.
Procedência: explicação do Claude (definições padrão de livro-texto: teoria da informação e cálculo). Os exemplos
numéricos são inventados para ensinar. Dois papers citados no fim foram conferidos só em existência (título e
autores no arXiv), **nível 3, não lidos**.

O que já está claro para você, e é a base de tudo:
- **L_cls = −log p(y | h)**: a cabeça de classificação dá probabilidade ao rótulo certo; quanto menor essa
  probabilidade, maior a perda.
- **L_aux = −Σₜ log q(rₜ | r_<t, h)**: a mesma ideia, palavra a palavra. O decoder dá probabilidade a cada token da
  justificativa, sabendo os anteriores (teacher forcing).

As três coisas novas são **I** (seção 1), **∇θ L** (seção 2) e **ΔL** (seção 3).

---

## 1. Informação: H e I

### 1.1 Entropia H: quanta incerteza existe

**H(Y)** mede quanta incerteza existe sobre Y antes de olhar qualquer coisa, em **bits**. Leitura prática: é o
número médio de perguntas de sim/não necessárias para descobrir o valor.

- O rótulo do e-SNLI tem 3 classes de frequência parecida. Logo H(Y) = log₂3 ≈ **1,58 bits**: uma pergunta não
  basta, duas sobram às vezes.
- Uma moeda honesta tem H = 1 bit. Uma moeda viciada que sempre dá cara tem H = 0, porque não há o que perguntar.

**H(Y | X)**, a entropia condicional, é a incerteza que **sobra** sobre Y depois de ver X. Um anotador perfeito que
lê o par sabe o rótulo, então H(Y | X) ≈ 0. Na prática não é zero: o SNLI tem só 58% de pares unânimes.

**Ligação com a perda.** A perda de entropia cruzada, −log p(certo), é exatamente essa incerteza medida pelo
modelo. Se o modelo fosse perfeito e os dados infinitos, a média de L_cls no ótimo seria H(Y | X) (em nats com
ln, em bits com log₂). Um modelo real fica acima. Por isso **a perda de um modelo treinado é uma estimativa
(por cima) de uma entropia condicional**. É o que permite medir as coisas da seção 1.4 com um LM pequeno.

### 1.2 Informação mútua I: quanto ver X ajuda a prever R

```
I(R; X) = H(R) − H(R | X)
```

Em palavras: a incerteza sobre a justificativa **antes** de ver o par, menos a incerteza **depois**. É o quanto o
par "conta" sobre a justificativa, e vice-versa (I é simétrica).

Dois exemplos para um par de contradição ("Um homem dorme no sofá" / "Um homem corre na praia"):

| Justificativa | Ver o par ajuda a prever o texto? | I(R; X) |
|---|---|---|
| "The premise contradicts the hypothesis." | Pouco: o mesmo molde serve para qualquer par de contradição | **pequena** |
| "A man cannot be sleeping on a couch and running on a beach at the same time." | Muito: as palavras "sleeping", "couch", "running", "beach" só aparecem porque o par as tem | **grande** |

**Por que I(R; X) e não H(R) no denominador** (o erro corrigido na conversa): H(R) conta toda a incerteza do texto,
inclusive escolha de palavras, estilo e sintaxe, que não dependem do par. Essa parte o encoder não tem como
aprender, porque não está em x. O que a tarefa auxiliar pode ensinar ao encoder é só a parte de R que dá para
prever olhando x, e essa parte é I(R; X).

### 1.3 A regra da cadeia: separar o redundante do novo

Suponha que o rótulo dá para ler na justificativa (vazamento total: Y = g(R)). Então saber R já inclui saber Y, e a
informação de R sobre o par se divide em duas parcelas:

```
I(R; X) = I(Y; X) + I(R; X | Y)
          redundante   novo
```

- **I(Y; X)**: a parte de R que é só o rótulo. A L_cls já ensina isso. No máximo 1,58 bits, porque I(Y; X) ≤ H(Y).
- **I(R; X | Y)**: o que a justificativa diz sobre o par **além do rótulo**. Que fato da premissa decide, que
  palavra contradiz. É o único sinal que a L_aux traz e a L_cls não traz.

Analogia: uma nota fiscal tem o total (o rótulo) e os itens (o porquê). Se você já sabe o total, a nota só te ensina
algo pelos itens. Uma justificativa de molde é uma nota só com o total.

**Fração redundante:** ρ = I(Y; X) / I(R; X) ≤ 1,58 / I(R; X).
- Justificativa de molde: I(R; X | Y) ≈ 0, então ρ ≈ 1. Tudo é redundante.
- Justificativa que cita o fato decisivo: I(R; X | Y) grande, então ρ → 0.

**O que isso decide:** vazar o rótulo não é o problema. O problema é **I(R; X | Y) pequeno**, ou seja, justificativa
vazia. Um texto pode vazar o rótulo e ainda carregar muita informação nova. É o eixo informativa × vazia.

### 1.4 Como medir, sem API

Pela ligação da seção 1.1 (perda de um LM ≈ entropia condicional), treine um LM pequeno (por exemplo, T5-small)
de dois jeitos, sobre as justificativas de um braço:

| LM | Entrada | Perda média estima |
|---|---|---|
| A | só o rótulo | H(R \| Y) |
| B | par + rótulo | H(R \| X, Y) |

```
I(R; X | Y) = H(R | Y) − H(R | X, Y)  ≈  perda(A) − perda(B)
```

Em bits por justificativa, um número por braço (humano, Haiku, Sonnet, Qwen). Ressalva: cada perda é uma
estimativa por cima; a diferença de duas estimativas não é um limite garantido. Serve para **comparar braços entre
si** com o mesmo LM e o mesmo treino, não como valor absoluto.

### 1.5 Ressalva do Xu et al. (2020): o que vale para o número medido

Tudo de 1.2 e 1.3 é teoria de Shannon, com um observador que pode usar **qualquer** modelo. O número de 1.4 é outra
coisa: a informação que **um LM específico** consegue usar. Isso tem nome: **V-informação** (Xu et al., 2020, ICLR;
notas em `docs/artigos/notas-xu-2020-v-information.md`, nível 3). Três propriedades de Shannon **não valem** para
ela:

- **Simetria:** I_V(X→R) ≠ I_V(R→X) em geral (§3.3 do paper). O "e vice-versa" de 1.2 só vale na teoria. A direção
  X→R é a que a cabeça auxiliar faz, então é a que se mede.
- **Regra da cadeia:** o paper diz no Apêndice F que a decomposição aditiva de Shannon não vale para a V-informação
  em geral. A partição "redundante + novo" de 1.3 é argumento teórico; o número medido **não** se decompõe sozinho.
  Por isso se mede I(R; X | Y) **direto**, como a diferença de 1.4, e não como diferença entre totais.
- **Desigualdade de processamento de dados:** computação pode **criar** informação usável (§3.2). Para um decodificador
  fixo, a representação do encoder h = f(x) pode render mais que o x cru.

A versão **condicional** (o "| Y") não está definida no Xu 2020. Ela vem de Hewitt et al. (2021, EMNLP), e é a que
o REV (Chen et al., 2023) usa.

---

## 2. Gradiente: ∇θ L

### 2.1 Com um parâmetro só

θ (theta) é o conjunto dos pesos do modelo. Comece com um peso só e uma perda L(θ) = (θ − 3)², mínima em θ = 3.

- A **derivada** dL/dθ = 2(θ − 3) diz quanto L sobe se θ subir um pouquinho. Em θ = 5, vale 4: subir θ piora a
  perda, e rápido.
- **Descida de gradiente:** andar no sentido contrário, com passo η (eta, a taxa de aprendizado):
  θ ← θ − η · dL/dθ. Com η = 0,1: θ = 5 − 0,1·4 = **4,6**. Mais perto de 3.

### 2.2 Com muitos parâmetros

O encoder tem ~110 milhões de pesos. **∇θ L** (lê-se "gradiente de L em relação a θ") é a lista com uma derivada
por peso: um vetor de 110 milhões de números. Cada número diz quanto a perda sobe se aquele peso subir um pouco. O
passo é o mesmo, só que vetorial: θ ← θ − η · ∇θ L. É o que `loss.backward()` + `optimizer.step()` fazem no PyTorch.

Na notação da conversa:
- **g_c = ∇θ L_cls**: para onde a classificação quer mover os pesos do encoder.
- **g_a = ∇θ L_aux**: para onde a tarefa auxiliar quer movê-los.

Como L = L_cls + λ·L_aux, o gradiente total é **g_c + λ·g_a** (a derivada de uma soma é a soma das derivadas).

**Detalhe que importa:** só os pesos **compartilhados** (o encoder) recebem os dois gradientes. Os pesos da cabeça de
classificação só recebem g_c, e os do decoder só recebem g_a. Conflito só pode acontecer no encoder.

---

## 3. ΔL_cls: o passo ajudou ou atrapalhou a classificação?

### 3.1 O que é

**ΔL_cls** é quanto a perda de classificação mudou depois de **um** passo de treino:
ΔL_cls = L_cls(θ depois) − L_cls(θ antes). Negativo = a classificação melhorou.

### 3.2 A conta (aproximação de primeira ordem)

Para um passo pequeno, a mudança da perda ≈ gradiente × deslocamento (é a reta tangente; com um parâmetro,
ΔL ≈ L'(θ)·Δθ). Com muitos parâmetros, o "×" vira **produto escalar** (multiplica peso a peso e soma).

O deslocamento do passo é Δθ = −η(g_c + λ·g_a). Então:

```
ΔL_cls ≈ g_c · Δθ = −η · g_c · (g_c + λ g_a) = −η ( ‖g_c‖² + λ · g_c·g_a )
```

- **‖g_c‖²** = g_c · g_c, sempre ≥ 0. Esse termo sozinho sempre faz a classificação melhorar.
- **g_c · g_a** é o termo que decide o efeito da tarefa auxiliar.

### 3.3 O produto escalar como "concordância"

g_c · g_a é positivo quando os dois vetores apontam para lados parecidos, zero quando são perpendiculares e negativo
quando brigam. O **cosseno**, cos = g_c·g_a / (‖g_c‖ ‖g_a‖), é a mesma coisa normalizada entre −1 e 1.

Exemplo com dois pesos, λ = 1, ‖g_c‖² = 4:

| g_c | g_a | g_c · g_a | ΔL_cls ≈ −η(4 + g_c·g_a) | Leitura |
|---|---|---|---|---|
| (2, 0) | (1, 1) | 2 | −6η | a auxiliar **ajuda**: a classificação melhora mais do que sozinha |
| (2, 0) | (0, 3) | 0 | −4η | **neutra**: mexe em outros pesos |
| (2, 0) | (−1, 1) | −2 | −2η | **atrapalha um pouco**, mas a classificação ainda melhora |
| (2, 0) | (−3, 1) | −6 | **+2η** | **prejudica**: neste passo a classificação piora |

A última linha é a condição da conversa: prejudica quando g_c·g_a < 0 **e** λ·|g_c·g_a| > ‖g_c‖². O λ é a alavanca:
se o conflito existir, diminuir λ o desarma.

### 3.4 Por que os tokens que vazam não brigam

Separe g_a pelos tokens: g_a = g_a^rót (tokens que dizem o rótulo) + g_a^resto (o conteúdo).
- Para o decoder acertar o token "contradicts", o h precisa codificar o rótulo, que é o mesmo pedido da L_cls.
  Então **em média** g_c · g_a^rót ≥ 0.
- Se houver conflito, ele vem de g_a^resto.

Isso é **argumento, não teorema**: as duas cabeças são diferentes e podem pedir codificações diferentes do mesmo
rótulo. O cosseno medido no treino é o que confirma ou derruba.

### 3.5 Como medir no treino

A cada N passos, calcule os dois gradientes separadamente **só nos pesos do encoder** e registre o cosseno:

```python
enc = [p for p in encoder.parameters() if p.requires_grad]
g_c = torch.autograd.grad(loss_cls, enc, retain_graph=True)
g_a = torch.autograd.grad(loss_aux, enc, retain_graph=True)
dot = sum((a * b).sum() for a, b in zip(g_c, g_a))
cos = dot / (torch.sqrt(sum((a * a).sum() for a in g_c)) * torch.sqrt(sum((b * b).sum() for b in g_a)))
```

Custa um backward a mais nesses passos; com N = 100, quase nada.

---

## 4. O que muda no desenho

A checagem "a justificativa nomeia o rótulo?" sai, e entram duas medidas:
1. **I(R; X | Y) por braço**, antes do treino, com um LM pequeno (seção 1.4). Diz se o braço é informativo ou vazio.
2. **O cosseno entre g_c e g_a**, durante o treino (seção 3.5). Diz se a tarefa auxiliar ajuda, é neutra ou atrapalha.

## 5. Para ir além (nível 3, só existência conferida em 20/10)

Medir o cosseno entre gradientes de tarefas é uma linha conhecida de aprendizado multitarefa:
- Du, Czarnecki, Jayakumar et al., *Adapting Auxiliary Losses Using Gradient Similarity* (arXiv:1812.02224): usa o
  cosseno entre o gradiente da tarefa principal e o da auxiliar para decidir quando usar a auxiliar.
- Yu, Kumar, Gupta et al. (2020), *Gradient Surgery for Multi-Task Learning* (PCGrad, arXiv:2001.06782): quando o
  cosseno é negativo, projeta um gradiente para tirar a parte que briga.

Os dois são candidatos à lista de leitura das perdas. O resumo de cada um vem da memória do Claude, **não foi
conferido no texto**.
