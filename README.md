# RaDi-BERT

Residência em IA (UFG, 2026/2): justificativas geradas por LLM destiladas num classificador encoder-only de NLI, por
uma cabeça decodificadora auxiliar que sai na inferência. Base: Agrawal, Ahemad & Sembium 2025 (COLING Industry).
Estado e decisões em `CLAUDE.md` e `HANDOFF.md`.

## Estrutura

| Pasta | O que tem |
|---|---|
| `src/radibert/` | código: geração das justificativas (`piloto_qwen`, `lote`), medidas (`copia`, `eco`, `medir_variantes`), avaliação humana (`leitura_cega`, `forms`); caminhos em `paths.py` |
| `scripts/` | entradas de linha de comando (`rodar_lote.sh`); `screening/` guarda os scripts do screening encerrado, como rodaram |
| `config/` | `maquina.example.env`: caminhos e ajustes de cada máquina |
| `resultados/` | saídas dos pilotos e do lote (CSV, relatórios) |
| `dados/` | dados de entrada; o e-SNLI fica fora do git (ver `dados/README.md`) |
| `docs/` | `pesquisa/`, `residencia/` (termos, gates), `screening/`, `leituras/`, `artigos/`, `handoffs/` |
| `entrega/` | os .docx entregues nos gates |

## Rodar

Python 3.11 com [uv](https://docs.astral.sh/uv/):

```bash
uv sync --frozen
```

```bash
uv run python -m radibert.eco dev
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

## Duas máquinas

- **Notebook:** contexto, leitura, escrita, análise leve.
- **PC (RTX 5060 8 GB):** tudo que precisa de GPU (geração com o Qwen, treino).

O que não está no git: e-SNLI (`dados/README.md`), `resultados/lote-35B/amostra-treino.csv` (regenera com
`uv run python -m radibert.lote amostra`), GGUF e checkpoints (HF Hub privado).
