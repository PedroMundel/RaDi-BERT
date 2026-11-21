# RaDi-BERT

Residência em IA (UFG, 2026/2): justificativas geradas por LLM destiladas num classificador encoder-only de NLI, por
uma cabeça decodificadora auxiliar que sai na inferência. Base: Agrawal, Ahemad & Sembium 2025 (COLING Industry).
Estado e decisões em `CLAUDE.md` e `HANDOFF.md`.

## Estrutura

| Pasta | O que tem |
|---|---|
| `src/radibert/` | o pacote. Geração das justificativas (`piloto_qwen`, `lote`, `rte_racionalizacoes`), medidas sobre elas (`copia`, `eco`, `medir_variantes`), avaliação humana (`leitura_cega`, `forms`), treino (`rte_dados`, `esnli_dados`, `rte_modelo`, `rte_treino`), variações do treino (`rte_marcas`, `rte_destilacao`, `rte_intervencao`), medidas do treino (`rte_gradientes`, `painel`, `fora_dados`), `invariantes` e os caminhos em `paths.py` |
| `tests/` | testes do pacote e dos ganchos |
| `scripts/` | entradas de linha de comando (`rodar_lote.sh`), `hooks/` (ganchos do git) e `screening/` (scripts do screening encerrado, como rodaram) |
| `config/` | `maquina.example.env`: caminhos e ajustes de cada máquina |
| `resultados/` | uma pasta por experimento, com as saídas (CSV), a leitura (`leitura-grade.md`) e os scripts de medida que só servem àquele experimento (`medir_*.py`, `ler_*.py`). Em cada uma, `pc/` e `amigo/` separam a máquina que rodou; `figuras/` tem os gráficos e os scripts que os geram |
| `dados/` | dados de entrada, todos fora do git; como baixar em `dados/README.md` |
| `docs/` | `pesquisa/`, `residencia/` (termos, gates), `screening/`, `leituras/`, `artigos/`, `handoffs/`, `claude/` (ledgers) e, soltos, os planos e critérios de cada experimento, com a data no nome |
| `entrega/` | os .docx entregues nos gates, cada um com o .md de origem |

Os experimentos em `resultados/`:

| Pastas | Experimento |
|---|---|
| `piloto-professores`, `piloto-qwen`, `s6-copia-esnli` | pilotos de geração e de cópia das justificativas |
| `lote-35B`, `rte-35B` | justificativas geradas para o e-SNLI (16 mil pares) e para o RTE |
| `rte-treino`, `rte-calendario`, `rte-small`, `rte-tiny`, `rte-t5enc` | replicação do Agrawal no RTE, por encoder |
| `rte-msmarco`, `rte-capreolus` | o baseline MS-MARCO do artigo, em dois checkpoints |
| `rte-marcas*` | marcas de atenção no `[CLS]` |
| `rte-pequenos` | BERT small: destaque, atenção por camada, destilação entre BERTs e grupos no `[CLS]` |
| `esnli-treino`, `esnli-treino-calendario` | decoder no e-SNLI com 4 mil pares |
| `esnli-treino-16k*` | decoder nos 16 mil pares: calendário, justificativa embaralhada, curva, o que o decoder gera, fora de domínio (`-fora-pesos`) e peso da perda (`-aux-<peso>`) |

## Rodar

Python 3.11 com [uv](https://docs.astral.sh/uv/):

```bash
uv sync --frozen
```

```bash
uv run python -m radibert.eco dev
```

Testes e lint:

```bash
uv run --frozen pytest -q
```

```bash
uv run --frozen ruff check .
```

Treino (opções em `--help`; `--fumaca` roda um treino mínimo para conferir que tudo liga):

```bash
uv run python -m radibert.rte_treino --help
```

Invariantes dos resultados (I2 e I5 precisam do e-SNLI; sem ele saem como PULOU):

```bash
uv run python -m radibert.invariantes
```

Ganchos do git, uma vez por clone (lint, segredos, arquivos grandes, Conventional Commits, sem linha de autoria
do Claude):

```bash
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg
```

Trabalho em branch `tipo/descricao` com PR para `main`; nada de `--no-verify`. Com o Claude Code, o hook
`.claude/hooks/guardrails.py` barra commit e push no `main`, push forçado, `--no-verify`, desligar os ganchos e
escrever em `.env` ou na configuração do próprio hook.

Cada máquina tem `config/maquina.env` (fora do git), copiado de `config/maquina.example.env` com os caminhos do
`llama-server` e do GGUF. O lote noturno roda com:

```bash
bash scripts/rodar_lote.sh 16000 07:50
```

## Máquinas e o que fica fora do git

- **PC (RTX 5060 8 GB):** geração com o Qwen e treino.
- **Notebook:** contexto, leitura, escrita, análise leve.

Fora do git: os dados (`dados/README.md`), `resultados/lote-35B/amostra-treino.csv` (regenera com
`uv run python -m radibert.lote amostra`), o GGUF do Qwen, os pesos salvos dos classificadores
(`resultados/**/pesos/*.pt`), as pastas `run/` e `fumaca/` de cada experimento e dois arquivos acima do limite de
2 MB do gancho (`entrega/Manual do Treino.docx` e `resultados/rte-treino/pc/palavras.csv`).
