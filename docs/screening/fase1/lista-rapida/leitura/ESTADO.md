# Leitura das 56 obras por agentes — checkpoint

**Se o limite estourar:** rodar `scripts/screening/lista/l6_faltantes.py` (lista quem ainda não tem ficha válida) e
relançar o workflow SÓ com esses ids (`args`). Nunca retomar o workflow inteiro. A ficha em `fichas/NN.json` é o
checkpoint: existe e é JSON válido = pronta.

- [x] Passo 1: textos completos — 49 de 56 (sem: 02, 14, 20, 39, 40, 50, 53; agentes tentam a web) (`l5_textos.py`, idempotente) -> `textos/NN.txt`, `manifesto.json`
- [x] Passo 2: 56 fichas válidas (27/09; ~6,7 M tokens; 5 rodadas, 1 relançada após o limite)
- [x] Passo 3: relatório `docs/screening/fase1/2026-09-27-lista-v2-fichas.md`

**Script do workflow (relançar com `args` = saída de `l6_faltantes.py`, e SEM `resumeFromRunId`):**
`C:\Users\Pedro\.claude\projects\C--Users-Pedro-Documents-Projects-UFG-2026-2-Residencia-Bacharelado-em-Inteligencia-Artificial-Screening-fase1-lista-rapida-leitura\17c8c756-a1f2-4fc2-aa89-12e105502308\workflows\scripts\leitura-lista-v2-wf_73763609-c54.js`
(cópia em `scripts/screening/lista/wf_leitura.js`)

Registro de rodadas:
- 27/09 rodada 1: ids 01–12 (textos já baixados); download do resto em paralelo (`l5_textos.py`, em segundo plano).
- 27/09 rodada 1 concluída: fichas 01–12 válidas (1,5 M tokens; 12 × manter; qualidade conferida em 02 e 06). Rodada 2: ids 13–17.
- Rodada 2 concluída (13–17, 0,6 M tokens). Rodada 3: 18–22.
- Rodada 3 concluída (18–22). Rodada 4 (23–25) caiu no limite de uso (0 fichas); download trocado por versão com metadado em lote.
- Rodada 5: ids 23–56 (34 obras) lançados depois do reinício do limite.
