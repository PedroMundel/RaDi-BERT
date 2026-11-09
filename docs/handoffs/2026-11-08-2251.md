# HANDOFF — 08/11/2026 (repo RaDi-BERT montado; próxima: decidir a replicação e voltar ao treino)

## Status

**Contexto novo (Pedro):**
- Semana 9 dura 2 semanas; a Residência vai até a Semana 10 e depois vira escrita do TCC: **~3 semanas para as
  explorações** (contado em 31/10).
- Aula de 31/10 (professor, para a turma): escolher uma obra-base, refazer os experimentos dela e depois explorar.
  "Treinar sobre dados diferentes não é replicar." **A base do Pedro é o Agrawal 2025** (DSbS no `## Rejected`).
- 08/11: **2 semanas de atraso**. O PC (RTX 5060) perdeu o slot NVMe e roda com outro SSD (SATA); o SSD do projeto
  está no notebook (`WKST-001`, GTX 1650). Regras novas (CLAUDE.md, bloco MODO DE TRABALHO): IA liberada para
  acelerar; notebook = contexto, PC = GPU; tudo compartilhável (GitHub, HF Hub, Drive).

**Feito nesta sessão (31/10 a 08/11):**
- **Replicação (só conversa, nada rodou):**
  - Do Agrawal são replicáveis GLUE, QADSM e ESCI (apêndice A do paper). Não há código, o baseline (BERT +
    MS-MARCO) não tem nome, o prompt para o GLUE não existe e o professor é contraditório (Mixtral no §4,
    LLaMA2/Mistral-7B no apêndice B).
  - Tamanhos conferidos no HF: QNLI com 104.743 de treino (é relevância de frase, não NLI; ganho deles de só +0,6),
    RTE com 2.490 de treino e 277 no dev (NLI de 2 classes; ganho deles de +11 sobre um baseline quebrado).
  - **Recomendação do Claude:** mini-replicação no RTE (10 sementes, barata) e depois os três braços no e-SNLI.
    **Pedro não decidiu** entre RTE, QNLI e pular a replicação.
- **Avaliação humana:** o Claude respondeu o Forms como "Junior", sem gabarito. Aceitou 28/30 do Qwen e 4/20 do
  GPT-3; com os votos do Wiegreffe, 14/20 (κ = 0,40), sempre mais rigoroso.
  - **Pedro (03/11):** Junior conta como avaliador, declarado como LLM e não cego, com números com e sem ele
    (no HANDOFF antigo).
  - Proposta pendente: excluir avaliador com κ < 0,2 nos 20 itens do Wiegreffe, fixado antes de olhar a taxa do
    Qwen. Espera a planilha exportada.
- **Anthropic (resposta de 05/11):** o caso "parece permitido", mas sugere permissão escrita, lista "Outputs as
  training targets" como proibido e não cita o decoder. **Não é autorização; o Claude segue arquivado como
  gerador.** Oferecida uma pergunta sim/não citando o decoder; sem resposta.
- **Repo `PedroMundel/RaDi-BERT` (privado), em 5 passos, todos no `main`:**
  1. Estrutura `src/radibert`, `docs/`, `scripts/`, `config/`, `resultados/`, `tests/`; uv com versões travadas
     (pandas 3.0.2, scikit-learn 1.8.0, anthropic 1.13.0, tabulate 0.10.0); saídas idênticas byte a byte.
  2. Ganchos do pre-commit e gancho `commit-msg` contra autoria do Claude (PR #1).
  3. CI `gates`: ruff, pytest, ganchos no diff, regra de autoria, controle positivo de link, gitleaks (PR #2).
  4. Invariantes I1–I5 com controle positivo; I1, I3 e I4 no CI (PR #3).
  5. Hook do Claude Code `.claude/hooks/guardrails.py`, com falha fechada (PR #4). **Vale a partir de uma sessão
     nova**, e bloqueia também o Claude.
  - `main` em `6497a80`; 46 testes; invariantes 5/5 no notebook.
  - Ledger: `docs/claude/ledger/2026-11-08-repo-estrutura.md`.

**Em aberto quando parou:** este checkpoint está no branch `docs/checkpoint-08-11` (PR a mergear pelo Pedro).

## Decisions

- **Pedro:**
  - Base da replicação = Agrawal (31/10).
  - Junior/Claude como avaliador (03/11).
  - IA liberada; notebook e PC; tudo compartilhável (08/11).
  - Repo `RaDi-BERT` privado.
  - **Nunca co-assinar commit com o Claude** (memória `nunca-co-assinar-commit`; o gancho e o CI barram).
  - Guia do Medium (src/docs/tests/config/scripts).
  - Gates como no ULTIMATUM e no ABIGS_IA, por passos.
  - uv + `uv.lock`; pytest para unitários + CLI de invariantes; `main` + branch `tipo/descricao` com PR.
  - **Dizer o plano antes de agir e nunca exagerar** (memória `dizer-antes-e-nao-exagerar`, a partir das notas do
    Karpathy).
- **Rejeitados (no CLAUDE.md):**
  - DSbS como base.
  - Git Flow com `develop`.
  - mypy, `ruff format`, Docker, dependabot e cobertura mínima (escala do ABIGS).
- **Recomendações do Claude sem decisão do Pedro:**
  - Replicação no RTE em vez do QNLI.
  - Corte κ < 0,2.
  - Limite de 2 MB por arquivo (resultado grande vai para o HF Hub privado).
- **Becos técnicos:**
  - O hook do Pedro barra `git rm --cached`: tirar do índice é comando dele.
  - O sistema negou um comando que escrevia no README e o desfazia com `git checkout --`.
  - O llama-server não reproduz entre rodadas (antigo).

## Files touched

- Repo inteiro reorganizado no passo 1 (mapa em `README.md`). Novos:
  - `src/radibert/paths.py` e `src/radibert/invariantes.py`;
  - `scripts/rodar_lote.sh` e `scripts/hooks/sem_trailer_claude.py`;
  - `config/maquina.example.env`;
  - `tests/test_sem_trailer_claude.py`, `tests/test_links.py` e `tests/test_guardrails.py`;
  - `.pre-commit-config.yaml`, `.gitattributes`, `.github/pull_request_template.md` e `.github/workflows/gates.yml`;
  - `.claude/hooks/guardrails.py` e `.claude/settings.json`;
  - `pyproject.toml`, `uv.lock`, `requirements.txt` (gerado) e `dados/README.md`;
  - `docs/claude/ledger/2026-11-08-repo-estrutura.md`.
- `CLAUDE.md`: bloco MODO DE TRABALHO, repositório, caminhos novos e `## Rejected`.
- `docs/handoffs/2026-10-31-2359.md`: o HANDOFF anterior, arquivado.
- Memória: `nunca-co-assinar-commit.md`, `dizer-antes-e-nao-exagerar.md` e
  `professor-sem-llm-no-processo.md` (veto revogado).
- **Branches que sobraram** (apagar é decisão do Pedro):
  - `main-antigo`, só no notebook, com os 2 commits co-assinados;
  - `chore/guardrails-locais`, `ci/gates`, `test/invariantes` e `chore/guardrails-claude`, no notebook e no
    GitHub.

## Next steps

1. **(Pedro: GitHub)** Mergear o PR do branch `docs/checkpoint-08-11` (este handoff + linha 35 do ledger +
   rejeitados).
2. **(Pedro: decisão)** Replicação: RTE (recomendado), QNLI inteiro ou pular. Ela define a primeira semana.
3. **(Pedro: dado)** Exportar a planilha do Forms e confirmar o corte κ < 0,2. Depois (Claude): taxa de aceitáveis
   do Qwen por avaliador (Wilson 95%), α de Krippendorff e concordância com os votos do Wiegreffe, com e sem o
   Junior; seção nova em `entrega/geracao-primeiro-lote.md` e .docx regerado.
4. **(Pedro: PC)** SSH do notebook para o PC: OpenSSH Server no PC, `whoami` e o IP; o Claude gera a chave e o
   comando do `administrators_authorized_keys`. Depois, no PC:
   - `git clone`, `uv sync --frozen` e `uv run pre-commit install --hook-type pre-commit --hook-type commit-msg`;
   - `config/maquina.env` copiado do exemplo;
   - e-SNLI pelo `dados/README.md`;
   - GGUF por pendrive.
5. **(Claude, num branch)** Código do treino seguindo o Agrawal (BERT base + decoder T5 base,
   L = L_cls + 0,1·L_aux, aquecimento em 2 fases, hiperparâmetros da Tabela 4), testado na CPU com
   `google/bert_uncased_L-2_H-128_A-2`. Invariantes do treino: braço trocado é permutação, treino e dev sem
   sobreposição, reprodução com a semente.
6. **(Pedro: decisão)** Pendências antigas:
   - folha extra com +50 do Qwen (sim/não);
   - nome do aluno (o repositório já se chama RaDi-BERT: confirmar);
   - pergunta à Anthropic citando o decoder (enviar ou não);
   - baixar `esnli_test.csv`.
7. **(Claude, quando houver GPU)** Marca de discordância (passada do Qwen pedindo só o rótulo; retomável).

## Resume commands

```bash
cd "C:/Users/Pedro/Documents/Projects/UFG/2026-2/Residencia Bacharelado em Inteligencia Artificial"
git checkout main && git pull --ff-only
uv sync --frozen
uv run pytest -q                         # 46 testes
uv run python -m radibert.invariantes    # I1-I5; sem e-SNLI, I2 e I5 saem como PULOU
gh pr list --repo PedroMundel/RaDi-BERT  # PR do checkpoint aberto
bash scripts/rodar_lote.sh <alvo> <HH:MM>  # lote no PC (precisa de config/maquina.env)
```

Python: `uv run` (3.11, versões do `uv.lock`). Trabalho sempre em branch `tipo/descricao` com PR. O hook do Claude
Code barra commit no `main`, push forçado, `--no-verify` e escrita no `.env` e na configuração do hook.
