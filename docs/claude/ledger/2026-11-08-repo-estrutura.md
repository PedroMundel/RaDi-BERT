# Ledger - Repo RaDi-BERT, passo 1 (estrutura)

Sources: mensagem do Pedro 08/11 ("NUNCA co-commitar com Claude"; guia Medium de Tosin Akinosho, 04/04/2024: src/
docs/ tests/ config/ scripts/; gates como ULTIMATUM e ABIGS_IA; "vamos por passos"); proposta de 5 passos aceita
("Sim, seguir": uv + uv.lock, pytest + CLI de invariantes, main + tipo/descricao); mapeamento dos dois repos (agente,
08/11); CLAUDE.md global (NO-DELETE, NO-GIT); memória `nunca-co-assinar-commit`.

Caminhos antigos citados aqui de propósito (este arquivo fica fora da reescrita automática).

| # | Item | Source | Done when | Status | Evidence |
|---|---|---|---|---|---|
| 1 | Histórico antigo guardado em `main-antigo`; `main` novo é órfão | msg (regra 1) + NO-DELETE | `git branch` lista os dois; `git log main` não alcança `da08e9c` | done | `git branch -a` -> `main-antigo`, `remotes/origin/main`; `git log main` -> "unknown revision" (órfão sem commit) |
| 2 | Retrato das saídas determinísticas antes de mover | convenção: prova de refatoração | arquivo de hashes em scratchpad com eco, leitura cega, forms en/pt, cópia, medir F, amostra | done | `sha256sum -c antes-arquivos.sha` -> 7/7 OK após rodar os scripts; stdout em `antes-*.out` (scratchpad); `git diff --name-only` vazio |
| 3 | Pacote `src/radibert/` com os 9 módulos vindos de `experimentos/` | proposta passo 1 | `python -c "import radibert.<m>"` passa para cada módulo | done | `uv run python -c "import radibert.piloto_qwen, candidatos_exemplos, piloto_professores, lote"` ok (12 exemplos); eco, leitura_cega, forms, copia, medir_variantes rodados com `-m` |
| 4 | Caminhos centralizados em `radibert/paths.py` | proposta passo 1 | `grep -rn "parents\[" src/radibert` sem acerto fora de `paths.py` | done | único acerto `src/radibert/paths.py:4`; `grep HERE\|sys.path\|experimentos src/radibert` vazio |
| 5 | Saídas dos pilotos e do lote em `resultados/` | proposta passo 1 | `git ls-files resultados` (sem ignorados) = 145 (155 rastreados em `experimentos/` menos 10 de código) | done | 145 = 145; a conta inicial de 155 incluía o código (corrigida aqui) |
| 6 | `scripts/rodar_lote.sh` lê caminhos da máquina de `config/maquina.env` | msg regra 3 (duas máquinas) | `config/maquina.example.env` rastreado; `maquina.env` no `.gitignore`; `bash -n scripts/rodar_lote.sh` ok | done | `git ls-files config` -> `maquina.example.env`; `git check-ignore config/maquina.env` -> `.gitignore:25`; `bash -n` ok |
| 7 | Markdown da raiz em `docs/residencia/`, `docs/pesquisa/` e `docs/screening/`; `leituras/`, `semana-1-topicos/` e `Screening/` dentro de `docs/` | guia Medium (docs/) | `git ls-files \| grep -v /` = só CLAUDE.md, HANDOFF.md, README.md, pyproject, lock, requirements, .gitignore (.gitattributes entra no passo 2) | done | raiz: `.gitignore CLAUDE.md HANDOFF.md README.md pyproject.toml requirements.txt uv.lock` |
| 8 | Scripts do screening em `scripts/screening/`, fora do lint com motivo | guia (scripts/) | `ruff check` passa; `pyproject` exclui `scripts/screening` com comentário | done | `uv run ruff check` -> "All checks passed!"; `extend-exclude` com comentário; B905 ignorado com motivo; B023 anotado na linha (falso positivo) |
| 9 | Referências a caminhos antigos atualizadas (CLAUDE.md, HANDOFF, links .md, skill termogate) | convenção | `grep` dos prefixos antigos (`experimentos/`, `Screening/`, `semana-1-topicos/`, `leituras/` sem `docs/`) = 0 fora deste ledger | done | grep -> 0 acertos; 44 arquivos reescritos; skill termogate com 2 refs novas; links relativos: 0 quebrados (6 acertos do verificador são fórmulas `](y)`, não links) |
| 10 | Pastas ignoradas (raw, emb) mudaram junto | convenção | `ls docs/screening/fase1/raw docs/screening/fase1/emb` existe; pasta `Screening/` não existe | done | `ls` lista os JSON em `docs/screening/fase1/raw`; `ls Screening` -> "No such file"; `resultados/lote-35B/amostra-treino.csv` existe |
| 11 | `pyproject.toml` + `uv.lock`, Python 3.11; `requirements.txt` gerado do lock | escolha do Pedro (uv) | `uv sync --frozen` ok; `requirements.txt` começa com o cabeçalho do `uv export` | done | `uv sync --frozen` ok; `uv lock --check` ok; `requirements.txt:1-2` = cabeçalho do `uv export`; versões fixadas nas que geraram os resultados (pandas 3.0.2, scikit-learn 1.8.0, anthropic 1.13.0) |
| 12 | [P] Saídas idênticas depois da mudança | item 2 | os mesmos hashes do item 2 reproduzidos pelos módulos novos | done | `sha256sum -c` -> 7/7 OK (duas vezes, antes e depois do ruff --fix); stdout igual em eco dev, leitura cega, cópia, medir F; eco e amostra diferem só na linha que imprime o caminho do arquivo (mudou de propósito) |
| 13 | README.md na raiz: estrutura e como rodar em cada máquina | guia Medium | `README.md` existe e cita `uv sync`, `dados/README.md`, `config/maquina.env` | done | `grep -c` -> 4 acertos |
| 14 | Commit do passo 1 sem trailer do Claude | msg regra 1 | `git log main --format=%B \| grep -ci claude` = 0 | done | `chore: estrutura inicial do repositório` (emendado com este ledger); grep -> 0 |
| 15 | Repo remoto novo criado e `main` enviado | msg | `gh repo view` privado e `git status -sb` sincronizado | done | OK do Pedro (08/11); `gh repo view` -> PRIVATE, branch `main`; 705 arquivos no remoto; só `main` enviado (`git ls-remote --heads`); 0 trailer nos commits remotos |
| 16 | 33 arquivos ignorados fora do índice (27 raw, 1 emb, amostra, 4 de `run/`) | achado: `git add -A` rodou antes do `.gitignore` novo | `git ls-files -ci --exclude-standard \| wc -l` = 0 | done | Pedro tirou do índice no terminal dele (08/11); `git ls-files -ci --exclude-standard \| wc -l` -> 0; arquivos seguem no disco |
| 18 | [P] Gancho `commit-msg` recusa trailer de autoria do Claude e aceita menção ao Claude no texto | msg regra 1 + passo 2 | `uv run pytest tests/test_sem_trailer_claude.py` vermelho antes do script, verde depois | done | vermelho: 9 failed (script ausente); verde: 9 passed |
| 19 | `.pre-commit-config.yaml` com hooks genéricos, ruff, gitleaks, Conventional Commits e o gancho do item 18 | passo 2 (padrão ABIGS) | `uv run pre-commit run --all-files` passa | done | `pre-commit run --all-files` -> todos Passed na 2ª rodada (1ª corrigiu espaço em branco em 4 arquivos de docs/) |
| 20 | Ganchos instalados no clone (pre-commit e commit-msg) | passo 2 | `.git/hooks/pre-commit` e `.git/hooks/commit-msg` existem | done | `pre-commit install` -> `.git/hooks/pre-commit` e `.git/hooks/commit-msg` |
| 21 | Commit com trailer do Claude é barrado de verdade | passo 2 (controle positivo) | `git commit` com trailer termina com erro do gancho; sem trailer passa | done | commit com trailer -> `sem-trailer-claude ... Failed`, exit 1, HEAD seguiu `10ad58f`; commit sem trailer passou (`75a729e`) |
| 22 | `.gitattributes` com LF e binários marcados | passo 2 (padrão ULTIMATUM) | `git add --renormalize .` não muda conteúdo versionado, ou a mudança é declarada | done | `git add --renormalize .` -> nenhum arquivo versionado mudou |
| 23 | Template de PR com checklist (sem co-autoria, pre-commit verde, sem `--no-verify`) | passo 2 | `.github/pull_request_template.md` existe | done | `.github/pull_request_template.md` criado |
| 24 | README explica a instalação dos ganchos | convenção | `grep "pre-commit install" README.md` acha | done | README cita `pre-commit install` |
| 25 | PR do passo 2 aberto para `main`, sem trailer | proposta (branch + PR) | `gh pr view` mostra o PR; corpo sem atribuição | done | PedroMundel/RaDi-BERT#1 aberto; corpo sem linha de autoria (grep -> 0) |
| 27 | Teste de links relativos dos .md, que ignora fórmula `](y)` e acusa link quebrado | passo 3 | `uv run pytest tests/test_links.py` -> 2 passed, um deles o caso de controle | done | 2 passed; controle acha `pasta/nao-existe.md` e ignora `](y)` |
| 28 | Workflow `gates` (ruff, pytest, pre-commit no diff, sem autoria do Claude em commits e no corpo do PR, controle positivo de link, gitleaks no histórico) | passo 3 | `.github/workflows/gates.yml` existe; os passos rodados localmente passam | done | local: ruff ok, 11 passed, pre-commit no diff Passed (gitleaks no job próprio), trailer ok no commit do branch; o controle positivo não rodou local (sistema negou escrever no README) |
| 29 | CI verde no PR #2 | passo 3 | `gh pr checks 2` -> `gates` e `segredos` passam | done | `gh pr checks 2` -> gates pass (34 s), segredos pass (47 s); no log, o controle positivo reprovou `docs/arquivo-que-nao-existe.md` como esperado |
| 30 | [P] Invariantes I1–I5 com controle positivo; saída 0/1/2 e PULOU sem dado | passo 4 | `uv run python -m radibert.invariantes` -> 5 ok, exit 0; esperados ancorados nas fontes (16.000 e 1.252 do HANDOFF 31/10; 25,4% de `docs/2026-10-21-pesquisa-eco-justificativa.md:19`) | done | 5 ok, exit 0; em memória: carga ausente -> PULOU/0, controle identidade -> CONTROLE MORTO/2 |
| 31 | `lote.py` com `read_train`/`shuffle_usable` (I2 usa o mesmo embaralhamento) sem mudar a saída | passo 4 | `lote amostra` regenera `amostra-treino.csv` com o hash de antes | done | `sha256sum -c` -> OK |
| 32 | I1, I3 e I4 no CI | passo 4 | passo `Invariantes I1 I3 I4` no `gates.yml`; CI verde no PR | todo | |
| 17 | `tabulate` declarado como dependência | achado: `copia` e `medir` falharam no venv novo (pandas `to_markdown`) | `grep tabulate pyproject.toml requirements.txt` | done | `pyproject.toml:13`, `requirements.txt:61`, versão 0.10.0 do ambiente antigo |
| 26 | `src/radibert.egg-info/` fora do índice (artefato do build que entrou no passo 1) | achado do passo 2 | `git ls-files src/radibert.egg-info \| wc -l` = 0 | done | Pedro tirou do índice no terminal dele; commit `chore: tira o egg-info do índice`; `git ls-files src/radibert.egg-info` -> 0; pasta segue no disco (5 arquivos) |

## Expectations

### #12 [P] Saídas idênticas
- `marcas.csv` gerado de novo = hash do arquivo rastreado hoje (1.252 marcas de eco)
- `leitura-50-cega.md` e `leitura-50-gabarito.csv` = hashes rastreados (semente 42)
- `criar_formulario.gs` e `criar_formulario_pt.gs` = hashes rastreados
- `copia-numeros.md` = hash rastreado
- stdout de `medir F`, `marcar_eco`, `marcar_eco dev`, `copia` = stdout capturado antes
- `amostra-treino.csv` = hash do arquivo atual (112 MB, semente 42)
- Teste: comparação dos hashes antes e depois (script em scratchpad); depois vira invariante no passo 4
- Desvio registrado: o stdout de `eco` e `amostra` imprime o caminho de saída, que mudou de `experimentos/` para
  `resultados/` por desenho; o conteúdo dos arquivos é idêntico.
