# Notas — MiniLM (Wang et al., 2020)

**Obra:** Wang, Wei, Dong, Bao, Yang & Zhou. *MiniLM: Deep Self-Attention Distillation for Task-Agnostic Compression
of Pre-Trained Transformers.* arXiv:2002.10957v2, 6 abr. 2020. PDF em `minilm-wang-2020.pdf`, texto extraído em
`minilm-wang-2020.txt` (as páginas citadas abaixo são as do PDF).

**Procedência:** **nível 2** — o Claude leu em 17/11/2026, a pedido do Pedro ("Lê o MiniLM"), o texto extraído do
PDF. Lidas por inteiro as seções 1 a 5.1 (introdução, método, experimentos, ablações); as seções 5.2 a 7 (geração de
texto, multilíngue, trabalhos relacionados) só passadas por cima. As equações 6 a 10 foram lidas no texto extraído,
sem ver o PDF renderizado. **O Pedro não leu.** Venue não conferido (o arXiv é a única fonte usada).

## O que o artigo faz

1. **É destilação sem tarefa** (p. 1–2): o aluno imita o professor em texto geral (Wikipedia e BookCorpus, 400 mil
   passos, p. 5) e **depois** é ajustado em cada tarefa do jeito comum. Não há rótulo, não há respostas do professor
   na tarefa, não há etapa de destilação na tarefa. A comparação com os outros métodos é feita "sem destilação na
   tarefa e sem dados aumentados" (legenda da tabela 2, p. 5).
2. **Só a última camada** (seção 3.1, p. 3–4): o aluno imita a atenção da última camada do professor, não camada a
   camada. Motivo dado: não precisar escolher qual camada do professor ensina qual do aluno.
3. **Duas perdas, somadas com peso igual** (eq. 10, p. 4):
   - atenção (eq. 6): KL entre a distribuição de atenção do professor e a do aluno, por cabeça, todas as linhas;
   - relação entre valores (eq. 7 a 9): para cada cabeça, o produto escalar entre os vetores de valor de todos os
     pares de tokens, dividido pela raiz do tamanho do vetor e passado por softmax; KL entre a do professor e a do
     aluno. O resultado é uma matriz token x token, então não depende do tamanho dos vetores.
4. **Cabeças:** "o número de cabeças das distribuições de atenção e da relação entre valores é 12 nos alunos" (seção
   4.1, p. 5). O aluno de 384 dimensões foi **montado com 12 cabeças**, igual ao professor. O artigo não trata de
   aluno com outro número de cabeças.
5. **Professor assistente** (seção 3.3): para alunos pequenos, destila primeiro num modelo intermediário. Ganho de
   0,2 a 0,3 no MNLI (tabela 3).

## Números (dev, média de 4 rodadas de ajuste; MNLI-m em acurácia)

| Comparação, aluno de 4 camadas e 384 dimensões | MNLI-m | SQuAD 2.0 | Onde |
|---|---|---|---|
| MiniLM completo | 80,3 | 69,4 | tabela 3 |
| Sem a relação entre valores (só atenção) | 79,0 | 67,5 | tabela 5 |
| Erro quadrático sobre os valores, com matriz de projeção, no lugar da relação | 80,1 | 68,3 | tabela 6 |
| Camada a camada (casamento uniforme) no lugar de só a última | 79,9 | 67,6 | tabela 7 |
| TinyBERT refeito por eles, mesmos dados | 79,2 | 66,7 | tabela 3 |
| Imitar só as probabilidades de palavra mascarada | 77,7 | 65,3 | tabela 3 |

Como ler: cada linha troca uma peça do método e mostra a nota do aluno depois de ajustado na tarefa; a primeira
linha é a referência. Nos alunos de 6 e de 3 camadas as diferenças têm o mesmo sinal (tabelas 5 a 7).

Outras frases que importam: "também tentamos transferir a relação entre estados internos, mas o desempenho dos
alunos é instável para professores diferentes" (seção 4.4, p. 7). Professor BERT base: 84,5 no MNLI (tabela 2).

## O que o artigo NÃO cobre, e é o nosso caso

- Destilar **na tarefa**, com poucos pares (4.000) e poucos passos (1.000), num aluno já pré-treinado.
- Juntar a imitação interna com as **respostas** do professor na tarefa, em qualquer ordem.
- Aluno com número de cabeças diferente do professor (8 contra 12 no nosso). O MiniLMv2 (arXiv:2012.15828) diz no
  resumo que tira essa restrição; **não lido**.
- Estados internos com projeção (a peça do TinyBERT): não é testada isolada; só o TinyBERT inteiro.

## Correções ao que estava escrito no projeto

- Seção 11.5 do plano (versão de 16/11) dizia que a relação entre valores pede "mais código, ler os vetores de valor
  de dentro da atenção". Errado: o valor é a camada linear `value` aplicada ao estado da camada anterior, que o BERT
  já devolve (`modeling_bert.py`, transformers 5.20.2). Conferido também: no small e no base cada cabeça tem 64
  dimensões (512/8 e 768/12).
- Os números citados no plano (seção 11) e no handoff de 16/11 sobre o MiniLM (82,2 contra 84,5; −1,0 a −1,3 sem a
  relação entre valores; alunos com 12 cabeças) **batem** com o artigo.
