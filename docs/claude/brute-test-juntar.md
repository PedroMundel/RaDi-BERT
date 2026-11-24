# Brute-test — destilação conjunta (seção 11.5 do plano), 17/11/2026

Pedido do Pedro (17/11: "roda um brute-test e auditoria de codigo antes"), antes de lançar a rodada no PC.

**Alvo:** `src/radibert/rte_destilacao.py` (`hidden_mse`, `value_relation`, `Distillation.terms`),
`rte_modelo.py` (`with_projections`, `distill_terms`), `rte_treino.py` (`internal_only`, `loss_of`) e
`resultados/rte-pequenos/medir_juntar.py`. **Isolamento:** o script rodou com a pasta de saída trocada para o
scratchpad; nada foi gravado no repositório nem no PC. 22 casos numa execução, CPU e a GTX 1650 do notebook.
O harness é descartável e ficou no scratchpad da sessão.

## Achados

| Sev | Linha do ledger | Achado | Estado |
|---|---|---|---|
| S1 (anterior a hoje) | - | A atenção que o BERT devolve em modo de treino já passou pelo dropout (10% das entradas zeradas, linhas que não somam 1; medido: somas de 0,25 a 1,11). A perda de atenção (`attention_kl`) e a das marcas (`mark_loss`) são calculadas sobre ela desde 10/11. Uma entrada zerada onde o professor tem 0,5 custa ~4,9 de perda sozinha. O treino funciona (o gradiente passa pelas entradas vivas), mas com ruído, e o valor da perda em treino não é a distância real. Vale para todas as rodadas de atenção e de marcas já feitas | **Aberto: decisão do Pedro** |
| S2 | 6, 7 | CSV com a última linha cortada (rodada morta no meio da escrita): a retomada morria com `ParserError` do pandas, sem dizer o que fazer | Corrigido: sai com mensagem dizendo para tirar a última linha. Os scripts antigos (`medir_respostas.py`, `medir_destilacao.py`) têm o mesmo comportamento e não foram mexidos |
| S4 | - | `Distillation` sem nenhuma perda ligada: `AttributeError` dentro do treino | Corrigido: `ValueError` com a causa |
| S4 | - | `hidden_map` sem `with_projections`: `TypeError: 'NoneType' object is not subscriptable` | Corrigido: `ValueError` com a causa |
| risco (auditoria) | - | `value_relation` dizia rodar em fp32, mas dentro do autocast o produto voltava para bf16 | Corrigido antes da bateria; caso "CUDA bf16 contra fp32": maior diferença relativa 0,15% |

## O que passou (19 de 22)

- Conta à mão da relação entre valores (0,6698) e do erro quadrático.
- Todas as perdas finitas: 5 pares com preenchimento, 1 par, sem preenchimento, modo de treino, valores x 10.000.
- Gradiente: finito em modo de treino; chega às projeções; não chega ao professor; a perda dos valores chega à
  camada `value` e não à `query` da última camada.
- Pares de treino, do professor, de escolha e do dev não têm par em comum (por texto).
- Script: primeira rodada, repetição sem escrever nada, mesmos números em outra pasta (CPU), retomada só dos braços
  que faltam (9 linhas, sem duplicata), nome de braço errado recusado com mensagem.
- Modelos reais (small e base), um passo do braço mais pesado nos 32 pares mais longos (83 tokens): pico de 1,0 GB
  na GTX 1650. Cabe com folga nos 8 GB do PC.

## Não atacado

- Curva de escala: o tamanho real é a própria rodada (4.000 pares, tempo por aluno medido em 16/11).
- Duas rodadas ao mesmo tempo na mesma pasta: não acontece no uso.
- Reprodução na GPU entre rodadas: sabida como inexata (até 0,026 de ROC-AUC no RTE, medido em 10/11).
