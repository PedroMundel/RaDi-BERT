# Brute-test: cabeça de grupos no `[CLS]` (plano, seção 11.8, etapa 2)

17/11/2026, noite. Pedido do Pedro ("roda o brute test antes tbm"), antes de qualquer braço com a cabeça ir para o PC.

**Alvo:** `rte_destilacao.label_rate_logits` e `GroupTargets`; `RationaleBert.with_group_head` e `group_logits`;
`medir_grupos_cls.py` (`group_rows`, `gradient_cosines`, `train_head_student`, retomada); `comparisons` do
`medir_recorte.py`. **Efeitos:** só escrita de CSV; a bateria rodou na CPU, numa pasta temporária do scratchpad, com
uma cópia de `grupos-alvos-treino.csv`. **Não atacado:** o caminho na GPU (bf16, memória do lote de 256 pares do
cosseno), o tempo por aluno no tamanho real e a queda no meio da rodada. A auditoria de treino leu esses três pontos
sem rodar.

## Antes do brute-test: achado da auditoria de treino, já corrigido

| Sev | Achado | Correção |
|---|---|---|
| S1 | O viés por rótulo começava em zero e, na taxa de aprendizado das cabeças (5e-5, 1.000 passos), não conseguiria andar mais que 0,025; o que ele precisa guardar vai de −1,4 a −5,4. O efeito do rótulo passaria todo pelo `[CLS]`, o contrário do desenho | O viés nasce no logit da taxa de cada grupo em cada rótulo (`label_rate_logits`), calculado nos alvos do próprio braço. Teste novo na suíte |

## Bateria: 25 casos, 23 OK, 2 marcados

| Sev | Linha do ledger | Achado | Como repetir |
|---|---|---|---|
| nota | 9 | No controle trocado do alvo restrito, 51% dos pares ficam com a linha de alvos igual à original. Não é defeito: 69% dos pares não têm nenhum dos sete grupos, e trocar uma linha vazia por outra vazia não muda nada. Entre os pares que têm algum grupo, só 5,6% ficam iguais. Consequência para a leitura: no alvo restrito a troca só mexe de fato em cerca de 1.250 dos 4.000 pares | caso "swap (cut)" do harness |
| nota | 9 | O caso "o braço trocado treina um aluno diferente" passou e só foi marcado como lento (9 s) | caso "control" do harness |

Nenhum S1 a S4 novo. O que passou, por grupo:

- **Viés por rótulo:** rótulo sem nenhum par, grupo presente em todos os pares e tabela vazia dão números finitos;
  nos alvos reais do recorte o viés reproduz a taxa de cada rótulo (erro máximo 0,0004).
- **Cabeça:** com a camada linear em zero, a perda é exatamente a de um modelo que só vê o rótulo (diferença 1e-8).
- **Alvos:** o recorte são as mesmas colunas do alvo completo; a ordem segue a dos pares dados e não a do arquivo;
  par fora do arquivo e arquivo ausente falham com erro, sem valor inventado.
- **Troca:** mantém as somas por rótulo; o mesmo sorteio a cada chamada.
- **Perda:** lote de um par funciona; par sem linha de alvo falha com `KeyError`.
- **Avaliação:** a cópia avaliada não tem parâmetro da cabeça e não muda quando a cabeça muda.
- **Início:** com a mesma semente, encoder e classificador nascem iguais aos de um aluno do baseline.
- **Cosseno:** duas chamadas dão o mesmo valor; não sobra gradiente guardado; o modo de treino volta; grupo ausente
  do lote e lote de um par não dão NaN.
- **Repetição:** mesma semente na CPU dá o mesmo aluno e os mesmos cossenos.
- **Script:** rodar de novo não acrescenta linha (9 e 73 linhas antes e depois); braço desconhecido é recusado com
  a lista dos que existem.
- **Leitor:** cada braço com a cabeça é comparado com a sua referência e com o seu próprio controle trocado.

**Sabido e não corrigido:** uma queda entre a gravação dos cossenos e a dos acertos duplica os cossenos de um aluno
na retomada (os acertos, que decidem, não duplicam).

Harness: `brute_grupos.py`, no scratchpad da sessão (não está no repositório).
