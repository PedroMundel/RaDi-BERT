# HANDOFF — 09/11/2026 (PC pronto via SSH; próxima: decidir a replicação e escrever o treino)

## Status

**Contexto (herdado de 08/11, sem mudança):** ~3 semanas para as explorações (contado em 31/10), 2 semanas de
atraso; base da replicação = Agrawal 2025; IA liberada para acelerar; notebook (`WKST-001`, GTX 1650) = contexto,
PC (`DESKTOP-2VBC5EC`, RTX 5060 8 GB, SSD SATA) = GPU. HANDOFF anterior em `docs/handoffs/2026-11-08-2251.md`.

**Feito nesta sessão (09/11): ponte notebook -> PC, PC pronto para o projeto.** Nada do treino foi escrito.
- **SSH do notebook para o PC:**
  - Chave `~/.ssh/radibert_pc` (ed25519, sem senha) no notebook; atalhos no `~/.ssh/config`:
    `ssh pc` (LAN, `192.168.1.14`, DHCP, pode mudar) e `ssh pc-h` (Hamachi, `25.11.204.231`, fixo, fora de casa).
  - No PC: OpenSSH Server pelo winget (`Microsoft.OpenSSH.Preview` 10.0; o `Add-WindowsCapability` falhou calado),
    serviço `sshd` automático, regra de firewall porta 22, chave em
    `C:\ProgramData\ssh\administrators_authorized_keys` (a conta Pedro é admin) com ACL só Administradores + SYSTEM,
    shell remoto = PowerShell 5.1. Há também um `~\.ssh\authorized_keys` de 104 bytes no PC (do primeiro bloco
    colado; sem efeito para conta admin).
- **PC preparado pelo SSH:**
  - git 2.56 e uv 0.13.7 pelo winget (o winget funciona por SSH).
  - GitHub por **deploy key read-write só do `RaDi-BERT`** (`~/.ssh/github_radibert` no PC, id 169286767,
    "PC DESKTOP-2VBC5EC (RTX 5060)"); identidade git global igual à do notebook.
  - Repo em **`D:\RaDi-BERT`** (`main` em `6497a80`), `uv sync --frozen`, ganchos pre-commit + commit-msg.
  - e-SNLI (dev, train_1, train_2) copiado do notebook, md5 iguais.
  - 46 testes passam; invariantes I1–I5 todas ok no PC (com o e-SNLI, I2 e I5 deixam de pular).
  - llama.cpp b11770 (CUDA 13) e `Qwen3.6-35B-A3B-UD-IQ4_XS.gguf` em `D:\tools`, SHA-256 do GGUF igual ao do
    notebook (`649d7508…`); `config/maquina.env` do PC aponta para `/d/tools` com os `LLAMA_ARGS` de 27/10.
  - llama-server testado na 5060: pronto em 6 s, 1 pedido a ~30 tok/s, `stop`, 7,1 GB de VRAM; parado depois.
- **Não verificado:** `git push` a partir do PC (só autenticação e clone); o lote completo (`rodar_lote.sh`) no PC.
- **Uncommitted no notebook** (branch `docs/checkpoint-08-11`, o do PR #5): `CLAUDE.md` (linha da ponte entre as
  máquinas), este `HANDOFF.md` e `docs/handoffs/2026-11-08-2251.md` (cópia do handoff anterior).

## Decisions

- **Pedro (09/11):** deploy key (escopo só deste repo) em vez de clonar no PC com login do navegador; Hamachi para
  o IP dinâmico (os dois PCs já estão na mesma rede dele).
- **Claude, declarado:** chave do notebook sem senha (para comandos remotos sem interação; trocar por chave com
  senha + `ssh-agent` se o Pedro quiser); repo e ferramentas no `D:` (SSD SATA 1 TB, 694 GB livres; o `C:` tem
  256 GB); só o 35B copiado (decisão de 27/10: 35B + F).
- **Sem rejeitados novos.**
- **Becos técnicos (para não repetir):**
  - PowerShell 5.1 descarta argumento vazio para exe nativo (`-N ""` do ssh-keygen quebra) e estraga aspas
    aninhadas: para script no PC, mandar bash por stdin:
    `ssh pc '& "C:\Program Files\Git\bin\bash.exe" -s' <<'EOF' ... EOF`.
  - Dentro desse bash, `ssh`/`git clone` consomem o stdin do script: usar `</dev/null`.
  - Em sessão SSH com chave, o Windows não libera o cofre de credenciais (DPAPI): login https do GitHub feito no PC
    não serviria para `pull`/`push` remoto. Por isso a deploy key.
  - O guardrail do projeto bloqueia comandos Bash com barra invertida de continuação ou escape (`\` no fim da
    linha, `D:\\tools` em sed). Escrever em uma linha e sem barras invertidas.
  - `python` no PC é o atalho da Microsoft Store: usar `uv run python`.
  - Pedro (09/11): **um comando por vez** quando ele tiver que colar algo no PowerShell; bloco inteiro falha
    linha a linha e esconde o primeiro erro.

## Files touched

- Notebook, no repo: `CLAUDE.md` (linha 22 em diante, "Ponte entre as máquinas"), `HANDOFF.md`,
  `docs/handoffs/2026-11-08-2251.md`.
- Notebook, fora do repo: `~/.ssh/radibert_pc`, `~/.ssh/radibert_pc.pub`, `~/.ssh/config` (novo), `~/.ssh/known_hosts`.
- PC: `D:\RaDi-BERT\` (clone), `D:\RaDi-BERT\config\maquina.env`, `D:\RaDi-BERT\dados\esnli\*.csv`,
  `D:\tools\llama.cpp-b11770\`, `D:\tools\models\Qwen3.6-35B-A3B-UD-IQ4_XS.gguf`, `~\.ssh\github_radibert(.pub)`,
  `~\.ssh\config`, `C:\ProgramData\ssh\administrators_authorized_keys`, registro `HKLM:\SOFTWARE\OpenSSH\DefaultShell`.
- GitHub: deploy key 169286767 no `PedroMundel/RaDi-BERT`.
- **Lixo (apagar é decisão do Pedro):** `D:\tools\teste-server.log` e `D:\tools\teste-resposta.json` no PC;
  branches antigos listados no handoff de 08/11 (`main-antigo`, `chore/guardrails-*`, `ci/gates`,
  `test/invariantes`).

## Next steps

1. **(Pedro: git)** Commitar `CLAUDE.md`, `HANDOFF.md` e `docs/handoffs/2026-11-08-2251.md` no branch
   `docs/checkpoint-08-11` e mergear o PR #5 (ou pedir ao Claude que commite).
2. **(Pedro: decisão)** Replicação: RTE (recomendado pelo Claude), QNLI inteiro ou pular. Define a primeira semana.
3. **(Claude, num branch)** Código do treino seguindo o Agrawal (BERT base + decoder T5 base,
   L = L_cls + 0,1·L_aux, aquecimento em 2 fases, hiperparâmetros da Tabela 4), testado na CPU do notebook com
   `google/bert_uncased_L-2_H-128_A-2`; invariantes do treino (braço trocado é permutação, treino e dev sem
   sobreposição, reprodução com a semente). Depois, rodar no PC por `ssh pc`.
4. **(Pedro: dado)** Exportar a planilha do Forms e confirmar o corte κ < 0,2; depois (Claude) taxa de aceitáveis
   do Qwen por avaliador (Wilson 95%), α de Krippendorff e concordância com o Wiegreffe, com e sem o Junior, em
   `entrega/geracao-primeiro-lote.md` + .docx.
5. **(Claude, quando quiser)** Testar `git push` do PC num branch descartável; rodar `rodar_lote.sh` curto no PC
   para comparar com o 1,20 s/par de 27/10.
6. **(Pedro: decisão)** Pendências antigas: folha extra com +50 do Qwen; nome do aluno (RaDi-BERT?); pergunta à
   Anthropic citando o decoder; baixar `esnli_test.csv`.
7. **(Claude, com GPU)** Marca de discordância (passada do Qwen pedindo só o rótulo; retomável) — agora possível
   no PC.

## Resume commands

```bash
cd "C:/Users/Pedro/Documents/Projects/UFG/2026-2/Residencia Bacharelado em Inteligencia Artificial"
git status -sb                               # docs/checkpoint-08-11, 3 arquivos sem commit
gh pr view 5 --repo PedroMundel/RaDi-BERT    # PR do checkpoint
ssh pc hostname                              # LAN; fora de casa: ssh pc-h hostname
ssh pc 'Set-Location D:\RaDi-BERT; git pull --ff-only; uv run pytest -q'
ssh pc '& "C:\Program Files\Git\bin\bash.exe" -s' <<'EOF'
cd /d/RaDi-BERT && bash scripts/rodar_lote.sh <alvo> <HH:MM>
EOF
```

Python: `uv run` (3.11, versões do `uv.lock`), nas duas máquinas. Trabalho em branch `tipo/descricao` com PR. O hook
do Claude Code barra commit no `main`, push forçado, `--no-verify`, escrita no `.env` e comandos com barra invertida.
