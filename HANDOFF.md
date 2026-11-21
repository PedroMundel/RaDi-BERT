# HANDOFF — 19/11/2026, 11:40 (Semana 10; **termo entregue**; o que falta agora é o Pedro conseguir explicar o que foi feito)

## Status

**O termo da Semana 10 foi entregue pelo Pedro em 19/11, por volta das 11:35** ("Show, entreguei o termo"), antes do
fechamento do gate às 12h. Nada no ar em nenhuma máquina. Código e documentos **sem commit** desde `59278b8` (10/11):
tudo de 10 a 19/11 existe só no SSD do notebook.

**O pedido aberto, com as palavras dele:** "Agora o mais importante (e preocupante): Não sei explicar nada do que
foi feito kkkk". Ele vai tratar disso na sessão nova. **Não sei quando ele precisa explicar em voz alta (hoje na
reunião do gate ou depois) nem quanto tempo há; foi a pergunta que ficou sem resposta.** Na sessão anterior ele
recebeu um primeiro resumo em linguagem simples (a história em seis frases, cinco termos, três números, cinco
perguntas prováveis com resposta curta); não disse se entendeu.

**O que foi entregue (tudo em `entrega/`, com a fonte `.md` ao lado):**

| Documento | Fonte | Quem leu |
|---|---|---|
| `Trilha das Semanas 9 e 10.docx` (história única da replicação, 9 seções) | `controles-do-decoder-e-destilacao.md` | reescrito em outra sessão; o Claude desta sessão leu só trechos; não sei se o Pedro leu |
| `Figuras e Evidencias.docx` (11 figuras, tabela de onde sai cada afirmação, seção 6 com a hipótese das justificativas) | `figuras-e-evidencias.md` | escrito pelo Claude; o Pedro não disse ter lido |
| `Criterios Escritos Antes dos Testes - Semana 10.docx` | `criterios-da-semana-10.md` | escrito pelo Claude, sem segunda conferência de números |
| `Marcas de Atencao e Destaque v2.docx` (seção 6 corrigida) | `marcas-de-atencao-e-destaque.md` | o `.docx` de 11/11 ficou intacto |

O rascunho do termo está em `docs/residencia/termo-de-entrega-Semana-10.md`; **o que o Pedro colou no formulário eu
não vi** (não sei se declarou o uso de LLM, como ficou o Planejamento, quais links pôs). Título do tema decidido por
ele: **"Destilação de Racionalização de LLM para Encoders: controles e limites"**, subtítulo "A supervisão por
justificativas vale o custo em encoders para implantação?".

**O que a pesquisa mostrou, em uma tabela (critérios em `docs/2026-11-18-gaps-da-argumentacao.md`, Gaps 1 a 9;
leituras no fim de `resultados/esnli-treino-16k/leitura-grade.md`, itens 1 a 44):**

| Pergunta | Resposta medida |
|---|---|
| O ganho do artigo se repete? | Não; o baseline 0,4754 não sai de nenhuma condição tentada |
| O decoder ajuda nos 16 mil pares? | Não: o +0,003 era do calendário; com o mesmo calendário, −0,9 ponto de acurácia |
| O conteúdo da justificativa conta? | Sim: a trocada custa 3,0 pontos, a certa 0,9 |
| O decoder dá algo ao encoder? | No começo (+15 pontos em 25 passos); o encoder alcança sozinho em cerca de 100 passos |
| Fora de domínio? | MNLI −1,5 ponto (−2,3 a −0,7), 0 de 5: atrapalha |
| Outras medidas (painel do Pedro)? | calibração e pior classe do lado ruim, predição seletiva nula |
| O peso da perda do decoder? | 0, 0,05 e 0,5 (3 sementes): nenhum passa; com peso 0 a perda é a mesma |
| O que sobe a nota? | destilação comum entre BERTs (+1,6; a sequência +0,93 e +0,45 no dev), sem LLM |
| Hipótese do Pedro, não testada | as justificativas dele trazem pouca informação nova (21,8% das palavras) e quase só o rótulo (BERT que lê só a justificativa: 96,9%); não explica o ganho do artigo no RTE |

Como ler: diferenças pareadas por semente, 5 sementes salvo indicação, intervalo de 95%.

## Decisions

- **Pedro (19/11, depois do gate):** apresentou; o professor criticou a escolha do artigo e não comentou o método.
  **Rumo: tudo daqui para frente modelado pelo custo** ("essa técnica compensa o custo 7x maior?"), com a destilação
  comum como régua; experimentação encerrada, só pontuais (a nomeada: decoder e destilação no mesmo cenário, BERT
  base e small, sem desenho ainda). Detalhe e limites no bloco "19/11, GATE 10" do `CLAUDE.md`. O passo 1 dos Next
  steps (explicar o trabalho) foi feito nesta sessão, de forma assíncrona. Pesos do Marcelo: tentativa falhou
  (`ssh amigo` sem resposta).

- **Pedro (19/11, manhã):** título e subtítulo do tema (acima); o documento principal chama-se "Trilha das Semanas 9
  e 10"; custo e hipótese das justificativas entram no termo; quis os critérios da semana em `.docx`; **"esses docs n
  são só pro termo, mas pra mim tbm, pra hora que eu for escrever o TCC"** (memória `docs-de-entrega-servem-ao-tcc`).
- **Pedro (madrugada):** painel = calibração, robustez fora de domínio, predição seletiva e pior classe; pesos 0,
  0,05 e 0,5; embaralhado no PC do Marcelo; "Usa o Opus pra coisa que n precisa do Fable" (limite de Fable acabando).
- **Rejeitado / derrubado (no `## Rejected` do `CLAUDE.md`):** decoder ajudar fora de domínio ou em outra medida; o
  peso 0,1 como causa; atalho da hipótese e compressão como medidas; lançar teste sem piso, poder e pesos salvos;
  script avulso a partir de `%TEMP%`.
- **Escolhas do Claude declaradas nos docs:** MNLI como conjunto principal; cortes do painel; limite de 0,6 ponto que
  barrou o embaralhado fora de domínio por 0,03; 3 sementes na varredura; redação dos três documentos novos.
- **Abertos:** quando e para quem o Pedro explica o trabalho; commit e push; regra de leitura do gap 4 (nunca
  confirmada); o `.docx` antigo `Controles que o Artigo Nao Rodou.docx` e `Controles do Decoder e Destilacao.docx`
  continuam em `entrega/`, sem uso.

## Files touched

- **Entrega:** `entrega/controles-do-decoder-e-destilacao.md` (título, hipótese e custo nos limites),
  `entrega/figuras-e-evidencias.md`, `entrega/criterios-da-semana-10.md` (novos), `entrega/marcas-de-atencao-e-destaque.md`;
  os quatro `.docx` da tabela acima; `docs/residencia/termo-de-entrega-Semana-10.md`.
- **Figura nova:** `resultados/figuras/figura_fora_painel.py` e `30-fora-de-dominio-painel-e-peso.png` (o `INDICE.md`
  das figuras não foi atualizado com ela).
- **Código (suíte 209 verdes às 07:53; não rodou depois do script de figura):** `src/radibert/rte_treino.py`
  (`--fora`, `--salvar-pesos`, `--peso-aux`), `rte_dados.py`, `esnli_dados.py`, `paths.py`, `fora_dados.py`,
  `painel.py`; testes novos; `resultados/esnli-treino-16k/avaliar_fora.py`, `painel_pesos.py`, `ler_fora.py`,
  `ler_peso.py`; lançadores em `resultados/rte-treino/run/`.
- **Resultados copiados:** `resultados/esnli-treino-16k*-fora-pesos*/{pc,amigo}/` (não estão no `.gitignore`).
- **Registro:** `docs/2026-11-18-avaliacao-da-pesquisa.md`, `docs/2026-11-18-gaps-da-argumentacao.md` (Gaps 7 a 9),
  `resultados/esnli-treino-16k/leitura-grade.md`, `docs/claude/ledger/2026-11-18-fora-de-dominio-decoder.md`,
  `CLAUDE.md`, `dados/README.md`, memória `docs-de-entrega-servem-ao-tcc`.
- **Fora do git:** `dados/mnli/`, `dados/hans/`; pesos em `resultados/esnli-treino-16k*-fora-pesos*/pesos/` no PC do
  Pedro (21 arquivos) e no do Marcelo (13), cerca de 0,44 GB cada.
- **Lixo, nada apagado:** fumaças novas nas três máquinas; `resultados/esnli-treino-16k-calendario-fora/` no PC do
  Pedro; `%TEMP%\h2.py` e scripts avulsos; `.docx` dos colegas em `~/.claude/uploads/`; scratchpad da sessão
  48e33852; os dois `.docx` antigos em `entrega/`; tudo em `C:\RaDi-BERT` no PC do Marcelo.

## Next steps

1. **(Claude, com o Pedro, já)** Fazê-lo conseguir explicar o trabalho. Antes de tudo perguntar: quando ele explica,
   para quem e quanto tempo há. Depois, com o objeto na mão (memória `pedro-nivel-de-experiencia`): partir do termo
   que ele entregou, bloco por bloco; ele explica com as palavras dele e o Claude corrige só o que estiver errado;
   usar as figuras de `entrega/Figuras e Evidencias.docx` (a 3, dos quatro braços, e a 5, de fora de domínio e peso,
   carregam a história). Não despejar texto novo: ele já tem documentos demais sem ler.
2. **(Pedro)** Ler a Trilha e os Critérios, que são texto assinado por ele.
3. **(Pedro: git)** Commit e push no `feat/treino-rte`; é a única cópia do trabalho de 10 a 19/11. Antes, decidir se
   as pastas `resultados/esnli-treino-16k*-fora-pesos*/` entram.
4. **(Claude, se ele pedir)** Atualizar `resultados/figuras/INDICE.md` com a figura 30; guardar o termo entregue em
   `entrega/termos-entregues/` (faltam os das Semanas 9 e 10); copiar os pesos do PC do Marcelo antes de ele apagar.
5. **(depois, só com pedido do Pedro)** O que nunca foi testado: duração da fase só do decoder, outro LLM ou prompt,
   um domínio em que a justificativa traga informação nova, poucos rótulos, perguntar aos autores.

## Resume commands

```bash
cd "C:/Users/Pedro/Documents/Projects/UFG/2026-2/Residencia Bacharelado em Inteligencia Artificial"
uv run --frozen pytest -q && uv run --frozen ruff check .
uv run --frozen python resultados/esnli-treino-16k/ler_fora.py pc amigo    # fora de domínio, painel, embaralhado
uv run --frozen python resultados/esnli-treino-16k/ler_peso.py             # varredura do peso
uv run --frozen --with matplotlib python resultados/figuras/figura_fora_painel.py
# regerar um .docx de entrega (o terceiro argumento é uma pasta de imagens temporárias, no scratchpad):
uv run --frozen --with pillow --with python-docx python scripts/screening/scripts/f1/md2docx_plain.py entrega/<fonte>.md "entrega/<Nome>.docx" <pasta>
```

- Para explicar ao Pedro: `docs/residencia/termo-de-entrega-Semana-10.md` (o rascunho do que ele entregou),
  `entrega/figuras-e-evidencias.md` e `entrega/controles-do-decoder-e-destilacao.md`.
- Repositório: https://github.com/PedroMundel/RaDi-BERT (privado pelo registro de 08/11; ramo publicado parado em 10/11).
