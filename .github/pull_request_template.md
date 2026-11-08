## O que muda

<!-- 2 a 3 linhas: o que este PR faz e por quê. -->

## Como verificar

<!-- Comandos para reproduzir o resultado. -->

## Checklist

- [ ] Pre-commit verde (`uv run pre-commit install --hook-type pre-commit --hook-type commit-msg`, uma vez por clone); nada de `--no-verify`
- [ ] Mexeu em `src/radibert/`: as saídas determinísticas continuam se reproduzindo (invariantes)
- [ ] Nada de `dados/esnli/`, `.env` ou arquivo acima de 2 MB no diff (dado grande vai para o HF Hub privado)
- [ ] Número citado no texto vem de um arquivo em `resultados/` gerado pelo código deste PR
- [ ] Regra nova ou rejeição registrada no `CLAUDE.md`
- [ ] Sem linha de co-autoria em commit, PR ou comentário
