# Tema v2 — PROPOSTA (28/08/2026, aguardando OK do Pedro)

Substitui `tema-escolhido.md` (v1, entregue provisoriamente e invalidado no mesmo dia pela
dinâmica de preferências — ver `dinamica-preferencias.md`).

## Título (escolhido pelo Pedro em 04/09/2026)

**Especialistas fundidos para o português: curadoria, síntese de dados e reparo de adaptadores em modelos compactos**

Versão original do Pedro, com a cauda redundante cortada ("na composição de modelos compactos de
linguagem" → "em modelos compactos": "fundidos" já significa composição). Mantida a separação
"síntese **de dados**" vs. "reparo **de adaptadores**" — sem ela o leitor entende que a curadoria
e a síntese são de adaptadores.

Alternativas descartadas: "Especialistas fundidos: dado como alavanca em modelos de linguagem
pequenos para português" · "Especialistas fundidos e reparados: recuperando capacidade perdida
com dado mínimo"

## De onde veio

Escolhas do Pedro na dinâmica (36/42): âncora ML ("melhorar o modelo"), medir > construir,
extrair > verificar, texto pt-BR, dado público, sem depender de terceiros, demo + portfólio +
publicar, ineditismo em pt-BR basta. Restrição dura declarada depois: **sem dinheiro para API,
sem GPU potente** — RTX 5060 8GB. Dessa restrição saiu a abertura para SLMs; ele escolheu as
direções S2 (especialista pequeno vs. generalista grande) e S3 (fusão de modelos), e pediu
para incorporar tratamento/QA/síntese de dados.

## Espinha

Uma pergunta medida em três lugares: **quantos exemplos custa cada ponto de qualidade, e o que
reduz essa conta.**

| Parte | Conteúdo | Papel |
|---|---|---|
| 1. Curadoria como alavanca | LoRA por tarefa; curva de dados; alavancas de dedup, filtro de ruído/rótulo errado, seleção por diversidade | Núcleo (S2 + tratamento/QA) |
| 2. Fusão | Fundir adaptadores sem retreinar; medir interferência e o que sobrevive | Núcleo (S3) |
| 3. Reparo com dado mínimo | Quão pouco dado conserta a fusão; real vs. sintético gerado localmente, com gate de admissão | Diferencial — amputável se o cronograma apertar |

Baselines honestos: especialistas separados (teto) · modelo único treinado em tudo junto
(concorrente direto da fusão) · modelo maior por prompt (o que se quer substituir).

## Viabilidade em 8GB (RTX 5060, Blackwell)

- LoRA/QLoRA em 1–3B: confortável.
- QLoRA em 7–8B: apertado (seq curta, batch 1, acumulação) — bônus, não plano.
- Fusão de adaptadores: aritmética de pesos, custo desprezível.
- Inferência 4-bit até ~8B: cabe.

**Risco nº 1 — suporte a Blackwell (sm_120):** builds antigos de PyTorch/bitsandbytes não
reconhecem RTX 50xx. PRIMEIRA tarefa do cronograma: instalar, carregar modelo em 4-bit e rodar
um passo de treino. Sem isso, o resto é fantasia.

**Risco nº 2 — explosão combinatória.** Disciplina obrigatória: 3 tarefas, ~5 pontos de tamanho
de dado, 2 alavancas de curadoria. Nada além.

## Simplificação adotada

A âncora agora é o modelo, então o dado é instrumento: usar **datasets públicos pt-BR já
existentes** para as tarefas, eliminando o gargalo de anotação manual que quase estourou o
cronograma da v1. DJEN (ver `corpus-djen-verificacao.md`) fica como tarefa "do mundo real"
opcional, não como alicerce.

## Cronograma (16 semanas)

- S1–2: preflight de ambiente (Blackwell) · escolha de modelo base e das 3 tarefas · baseline zero-shot
- S3–5: especialistas base por tarefa + curva de dados sem curadoria
- S5–7: alavancas de curadoria → nova curva
- S7–10: fusão + medição de interferência
- S10–12: reparo da fusão com dado mínimo (real vs. sintético + gate)
- S12–14: baselines honestos
- S14–16: escrita + buffer

## Pendências antes de começar

1. **Modelo base**: tabela comparativa verificada (1–3B, licença, suporte a português) — ONE-TABLE, Pedro escolhe.
2. **3 tarefas pt-BR** com dataset público pronto, preferindo extração.
3. Teste de ambiente na 5060 (risco nº 1).
