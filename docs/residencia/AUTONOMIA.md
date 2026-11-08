
# Rodada autônoma — 27/09/2026 (F2 do screening)

Pedido do Pedro: terminar a F2, criar checkpoints para o limite de uso não fazer perder trabalho, e "se corrigir
os erros for mais barato que relançar a pesquisa, corrigimos o erro". TaskCreate não está disponível nesta
sessão: a fila vive aqui.

## Fila

1. Checkpoint de estado da F2 (`docs/screening/fase1/F2/ESTADO.md`), atualizado a cada passo.
2. Reparar por script as saídas inválidas do agente 2 (sem relançar agentes).
3. Completar o que falta (agente 3 do lote 20, e qualquer id sem veredito), com execução idempotente: só o que falta.
4. Conferência de cópia exata + consolidação da F2 (proposta por grupo, SEM gravar na tabela-mestra).
5. Lista `sem acesso` da volta + amostra de 30 vereditos para a auditoria do Pedro.
6. Relatório descritivo da F2.
7. Relatório final desta rodada.

## Decisões (registro corrido)

- **D1 (27/09) — "JSON inválido" era BOM, não conteúdo.** 12 saídas do agente 2 e 2 da dupla começavam com BOM
  (UTF-8 com assinatura). Um arquivo tinha barra invertida de LaTeX sem escape. Correção **na leitura**
  (`utf-8-sig` + escape tolerante em `f2_consolida.py::le`), sem alterar arquivo nem relançar agente — custo zero,
  contra ~40 chamadas de agente. Rejeitado: relançar agentes 2/3 nesses lotes.
- **D2 — o resume do workflow não usou o cache** (27/09): rodou de novo agentes que já tinham terminado e
  sobrescreveu saídas. Por isso algumas saídas do agente 3 foram julgadas sobre versões anteriores das frases do
  agente 2 (conteúdo equivalente: mesma entrada, mesmo roteiro). Aceito como está e registrado; relançar custaria
  ~50 chamadas para ganho nulo. Regra nova no ESTADO.md: nunca relançar o workflow inteiro, só o que falta.
- **D3 — precedência do veredito:** "claramente fora" do agente 1 prevalece sobre qualquer veredito posterior (o
  agente 2 às vezes processou obras que o agente 1 tirou); obra sem abstract é `sem acesso` independentemente do
  que um agente tenha escrito (M6: nenhum agente decide sobre ela).
- **D4 — só o agente 3 do lote 20 roda** (32 obras, 1 chamada Sonnet).
- **D5 — grupo 43 e grupos 1/14 não decididos por mim.** A regra da F2 os mantém ("segue"), mas são casos de
  borda (32/40 sem acesso; 0 relevante e só dúvidas (c)). Apresentados como decisão do Pedro no relatório, §6.
- **D6 — nada gravado na tabela-mestra.** Regra de 23/09: proposta por grupo antes de qualquer marcação.
- **D7 — medi dois cortes baratos para informar a decisão da F3** (piso de citação 60 e situação na F1), sem aplicar
  nenhum: o piso não concentra relevância (6% × 7%); a F1 concentra (11% × 0,9%).
- **D8 — não lancei a F3.** Custaria ~87 milhões de tokens e o desenho dela (keywording sobre 11,5 mil obras) não
  cabe no alvo de ~50; é decisão do Pedro, com quatro caminhos numerados no relatório.

## Feito

1. **Checkpoint** — `docs/screening/fase1/F2/ESTADO.md`, atualizado a cada passo. Verificado: reflete os arquivos em disco.
2. **Saídas do agente 2** — "inválido" era BOM/LaTeX; corrigido na leitura (`f2_consolida.py::le`). Verificado:
   25 + 3 lotes carregam; 726 obras com frases.
3. **Faltantes** — só o agente 3 do lote 20 (32 obras) rodou. Verificado: 0 obras com acesso sem veredito.
4. **Consolidação** — 962 vereditos; verbatim 4,1% não bate; dupla leitura 87% de concordância entre seguir e sair.
5. **Sem acesso + auditoria** — `F2/sem-acesso.md` (165, 92 prioritárias) e `F2/auditoria.md` (30 sorteadas).
   Verificado: arquivos gerados; `vereditos.csv` com 962 linhas.
6. **Relatório** — `docs/screening/fase1/2026-09-27-F2-relatorio.md`. CLAUDE.md e memória atualizados.

## Bloqueado

Nada. Nenhuma ação destrutiva, git ou externa foi necessária.

## Próximos passos

1. Pedro lê o §6 do relatório da F2 e decide: grupos 1/14, grupo 43, e o caminho de ~11,5 mil para ~50 (a–d).
2. Pedro confere `F2/auditoria.md` (30 vereditos).
3. Depois da decisão: gravar a coluna `F2` na tabela-mestra e seguir pelo caminho escolhido, com ESTADO.md e lotes
   idempotentes.
4. Pendente de antes: escolha do Pedro sobre a lista de destilação (§9 de `2026-09-24-kd-lista-leitura.md`).
