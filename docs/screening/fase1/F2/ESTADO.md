# Estado da F2 — checkpoint (atualizado a cada passo)

**Se o limite de uso estourar:** retomar pelo primeiro item não marcado. Tudo é idempotente: cada script só
refaz o que falta ou está inválido. **Nunca relançar o workflow inteiro** (o resume de 27/09 não reaproveitou o
cache e reescreveu arquivos).

- [x] Amostra sorteada: `entrada.json` (962), `mapa.json`, lotes `a1/` (25) e `dupla/a1/` (3)
- [x] Agente 1: 25 + 3 lotes válidos
- [x] Agente 2: 25 + 3 lotes; "inválido" era BOM/LaTeX — lido por `f2_consolida.py::le`, arquivos intactos
- [x] Agente 3: 25 + 3 lotes completos (lote 20 rodado sozinho em 27/09)
- [x] Consolidação, artefatos (`f2_artefatos.py`) e relatório `../2026-09-27-F2-relatorio.md` (27/09). Próximo: decisões do Pedro (§6 do relatório). Tabela-mestra NÃO foi tocada.
