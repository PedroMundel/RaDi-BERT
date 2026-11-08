# Racionalização pós-hoc, filtro por similaridade com o humano e gerar mais de 100 mil (20/10/2026)

**Preocupações do Pedro (20/10):**
1. a racionalização pós-hoc (rótulo dado no prompt) pode ser um problema?
2. ideia: filtrar com TF-IDF ou similaridade de cosseno entre a justificativa humana e a do LLM. O medo é encolher
   o dataset;
3. seria bom gerar mais de 100 mil justificativas.

**Procedência.**
- Números do SNLI: paper de Bowman et al. (2015), via resultado de busca (nível 3).
- Custos: preços da skill `claude-api` (cache de 06/10/2026) e tokens reais do piloto. São **estimativas**, não
  medições.
- O resto é análise do Claude, marcada como tal. **Nenhuma decisão aqui é do Claude.**

---

## 1. A racionalização pós-hoc é um problema?

### 1.1 O que não é problema

- **O humano também é pós-hoc.** Os anotadores do e-SNLI recebiam o rótulo e explicavam por que ele valia (Camburu
  2018, §3). Gerar com o rótulo no prompt mantém o LLM no **mesmo protocolo** do humano, e é isso que deixa a
  comparação humano × LLM justa.
- **É a prática dos trabalhos mais próximos:** Wiegreffe 2022 (no próprio e-SNLI, "controle metodológico"), Agrawal
  2025, Wadhwa 2024 e Dhaini 2025 dão o rótulo-ouro ao professor (`docs/2026-10-19-pesquisa-prompt-racionalizacao.md`
  §2.1).
- **Fidelidade do professor não importa aqui.** "Pós-hoc" costuma ser crítica quando a explicação diz representar o
  raciocínio de quem decidiu. O professor não decide nada no seu desenho: só justifica um rótulo já dado. O que
  importa é a justificativa estar **certa sobre o par**.

### 1.2 O que é problema de verdade: rótulo ruidoso gera justificativa forçada

- Com o rótulo dado, o LLM **sempre** acha uma justificativa, inclusive para um rótulo errado ou discutível. Foi o
  caso nº 4 do teste de 13/10 (`docs/2026-10-13-custo-racionalizacao-llm.md` §1): o par nasceu neutro, a maioria
  marcou contradição, e o LLM justificou mesmo assim.
- **O tamanho do ruído no SNLI** (Bowman 2015, nível 3): nos 56.941 pares validados por 5 pessoas, 98% chegaram a
  consenso de 3, mas só **58% foram unânimes**. Há uma fatia real de pares discutíveis. Esses 56.941 incluem
  validação e teste inteiros, então no treino são só alguns dezenas de milhares (conta do Claude, **conferir**).
- **O dano para o aluno:** o rótulo errado já atrapalha a cabeça de classificação. A justificativa forçada acrescenta
  um **motivo falso coerente** com esse rótulo. Se isso pesa no treino, ninguém mediu.

### 1.3 Opções (decisão do Pedro)

| Opção | Como funciona | Perde pares? | Custo extra | De onde vem |
|---|---|---|---|---|
| **P0. Pós-hoc puro** | Como no piloto | Não | 0 | Wiegreffe 2022, Agrawal 2025 |
| **P1. Prever e explicar, só os que acertam** | O professor não recebe o rótulo; fica só o que bate com o ouro | **Sim** (quanto, só medindo) e enviesa para os fáceis | 0 | Li 2022 (COTE), Ho 2023 |
| **P2. Prever e explicar, com reserva pós-hoc** | Igual ao P1; quando o professor discorda, gera pós-hoc e **marca** o par | Não | só as discordâncias | Li 2022 (CROP) |
| **P3. Pós-hoc + sinalizador separado** | Gera pós-hoc. Uma chamada barata à parte (Haiku, saída de ~1 palavra) prevê o rótulo sem ver o ouro. Discordância vira coluna `professor_concorda` | Não | ~US$ 3–5 no treino inteiro (estimativa) | combinação do Claude |

- **Recomendação do Claude: P3 (ou P2).** Pela mesma regra do screening, **marcar, não apagar.** A coluna permite,
  depois, treinar com e sem os pares marcados e responder com dado se a justificativa forçada atrapalha. Esse
  resultado é seu e não está na literatura.
- O subconjunto validado por 5 pessoas serve para **conferir o sinalizador**: os pares que o professor marca como
  discordantes deveriam ser os não unânimes. Falta confirmar se o CSV do SNLI original traz os 5 rótulos por par;
  o do e-SNLI só tem `gold_label`.
- P1 e P2 entram na rodada 1 como variante a custo de centavos, e a rodada 1 mede quantos pares o professor erra.

---

## 2. Filtro por similaridade com a justificativa humana

**A ideia mede a coisa errada como critério de qualidade**, por três motivos:

1. **Parecido com o humano é, em boa parte, parecido com o par.** O humano copia em média 76,5% das palavras do par,
   e 30,6% das justificativas não acrescentam nenhuma (`resultados/s6-copia-esnli/resultado.md`). Um filtro por
   similaridade **premiaria a justificativa de LLM que mais copia**, o oposto do que a evidência valoriza
   (informação nova; Wadhwa 2024, Wiegreffe 2022).
2. **A referência é fraca.** Na sua avaliação, o humano saiu "pobre" em 7 de 20. Filtrar pelo humano mede o LLM
   com a régua pior.
3. **TF-IDF não vê paráfrase.** "Boys are not dogs" e "the premise describes boys, while the hypothesis is about a
   dog" dão o mesmo motivo com quase nenhuma palavra em comum. Embedding de frase resolve a paráfrase, mas não os
   problemas 1 e 2.

**Onde a similaridade serve: diagnóstico, não corte.**
- Similaridade **muito baixa** com o humano, **somada** à discordância do sinalizador (§1.3), é um bom candidato a
  "motivo diferente do humano". Vale olhar uma amostra à mão.
- Como métrica da rodada 1: "a variante X concorda mais com o motivo humano que a Y?". Serve para comparar variantes,
  não para jogar par fora.

**Filtro, se houver, que não encolhe o dataset:** gerar **mais** do que o necessário e **escolher** os melhores. Era
a sua ideia de 14/10 (cortar para ~100 mil escolhendo pela qualidade; `docs/ideias-de-desenho.md`). Gerar mais é o
que transforma o filtro em seleção, em vez de perda.

---

## 3. Gerar mais de 100 mil: quanto o orçamento compra

**Conta (estimativa).**
- Entrada ~150 tokens por par (sem as definições; com exemplos no prompt, o cache deve deixar o custo efetivo
  parecido, mas no lote o cache é por melhor esforço).
- Preço em lote: Sonnet US$ 1 / US$ 5 por milhão de tokens; Haiku US$ 0,05 / US$ 0,25.
- Disponível para a rodada grande: **~US$ 85** (US$ 100 − 0,64 do piloto − ~3 das rodadas 0–2 − ~10 de reserva para
  reenvios).

| Professor | Tamanho da saída | Custo por 100 mil | Pares com ~US$ 85 |
|---|---|---|---|
| Sonnet 5.5 | 80 tokens (como no piloto) | ~US$ 55 | ~155 mil |
| Sonnet 5.5 | **45 tokens** (~30 palavras) | ~US$ 38 | **~225 mil** |
| Sonnet 5.5 | **30 tokens** (~20 palavras, perto da variante D) | ~US$ 30 | **~280 mil** |
| Haiku 5.5 | 45–80 tokens | ~US$ 2–3 | o treino inteiro (549 mil) por ~US$ 10–15 |

**Combinação que vale considerar:** Haiku no treino inteiro (~US$ 10–15) + Sonnet em ~180 mil (~US$ 70). Isso dá
volume para seleção, cobre a curva de aprendizado (10 → 25 → 50 → 100 mil → tudo) e cria, de graça, um braço
"professor fraco × forte" na interseção. O DSbS fez a mesma pergunta com PaLM × GPT-NeoX (Tab. 1).

**Justificativa curta é o que compra volume.** A evidência (Wadhwa 2024) sugere que tamanho não é o que ensina, e
a sua placa de 8 GB agradece alvos curtos no decoder.

### 3.1 O gargalo pode ser o treino, não a API

- `docs/datasets-nli-verificacao.md` já registrava: 549 mil pares por época na RTX 5060 têm custo **alto** e
  **exigem subamostrar**.
- Braços (sem justificativa, humano, LLM, embaralhado) × 3 sementes × curva de aprendizado multiplicam isso.
- **Gerar 280 mil não obriga a treinar com 280 mil.** O excedente vira margem de seleção e de curva. Mas antes de
  decidir o volume, vale saber quantos pares por hora a placa treina. O script de benchmark que ficou para depois
  pode medir isso junto com a latência.

---

## Decisões que ficam com o Pedro

1. Pós-hoc puro (P0) ou com sinalizador (P2/P3)? P1 e P2 entram na rodada 1?
2. Similaridade com o humano: só diagnóstico (recomendado) ou corte?
3. Volume e professor: Sonnet sozinho (~225–280 mil, com saída curta) ou Haiku em tudo + Sonnet em parte?
4. Medir a vazão de treino antes de fechar o volume?
