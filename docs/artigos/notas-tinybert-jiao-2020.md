# Notas — TinyBERT (Jiao et al., 2020)

**Obra:** Jiao, Yin, Shang, Jiang, Chen, Li, Wang & Liu. *TinyBERT: Distilling BERT for Natural Language
Understanding.* arXiv:1909.10351v5, 16 out. 2020. PDF em `tinybert-jiao-2020.pdf`, texto extraído em
`tinybert-jiao-2020.txt` (as páginas citadas são as do PDF).

**Procedência:** **nível 2** — o Claude leu em 17/11/2026, a pedido do Pedro ("Ler o TinyBERT antes"), o texto
extraído do PDF. Lidas por inteiro as seções 1 a 4.6 e os apêndices A, B e C; trabalhos relacionados, conclusão e
apêndice D (descrição do GLUE) só passados por cima. Equações 6 a 11 lidas no texto extraído, sem ver o PDF
renderizado. **O Pedro não leu.** Venue não conferido (o arXiv é a única fonte usada).

## O que o artigo faz

1. **Duas etapas** (seção 3.2, p. 4–5):
   - **geral:** o aluno imita o BERT base **sem ajuste** em texto geral (Wikipedia, 3 épocas), só as partes internas;
   - **na tarefa:** o aluno imita o BERT base **ajustado na tarefa**, em dados da tarefa **aumentados** (cada exemplo
     vira 20 novos, por troca de palavras; algoritmo 1).
2. **A etapa da tarefa tem duas fases seguidas** (seção 4.2, p. 6):
   - fase interna: embeddings + atenção + estados internos de todas as camadas, **20 épocas** nos dados aumentados,
     lote 32, taxa 5e-5 (10 épocas nas tarefas grandes MNLI, QQP e QNLI; 50 no CoLA);
   - fase das respostas: só as respostas do professor, **3 épocas**, taxa escolhida entre 1e-5, 2e-5 e 3e-5.
3. **As quatro perdas** (seção 3.1, p. 4):
   - atenção (eq. 7): erro quadrático entre as notas de atenção **antes do softmax**, por cabeça. Dizem que antes
     do softmax converge mais rápido e dá nota melhor;
   - estados internos (eq. 8): erro quadrático entre o estado do professor e o do aluno passado por uma matriz
     treinada junto, que leva o tamanho do aluno ao do professor;
   - embeddings (eq. 9): o mesmo, na saída da camada de embeddings;
   - respostas (eq. 10): entropia cruzada contra as probabilidades do professor, temperatura 1. **Sem o rótulo
     certo:** a variante "sem respostas" é a que treina no rótulo certo (nota 10, p. 8).
4. **Casamento de camadas:** uniforme, camada m do aluno aprende da 3m do professor; peso 1 em todas (seção 4.2).
5. **Aluno:** 4 camadas, 312 dimensões, **12 cabeças** (seção 4.2). Como no MiniLM, igual ao professor.

## Números (dev; aluno de 4 camadas; MNLI-m em acurácia)

| Versão | MNLI-m | MRPC | CoLA | Onde |
|---|---|---|---|---|
| TinyBERT completo | 82,8 | 85,8 | 50,8 | tabelas 2 e 3 |
| Sem a etapa geral | 82,5 | 84,1 | 40,8 | tabela 2 |
| Sem a etapa da tarefa | 80,6 | 83,8 | 28,5 | tabela 2 |
| Sem dados aumentados | 80,5 | 82,4 | 29,8 | tabela 2 |
| Sem a perda de atenção | 79,9 | 82,3 | 41,1 | tabela 3 |
| Sem a perda de estados internos | 81,7 | 84,1 | 43,7 | tabela 3 |
| Sem as respostas (treina no rótulo certo) | 80,5 | 84,3 | 48,2 | tabela 3 |
| Sem embeddings | 82,3 | 85,0 | 46,7 | tabela 3 |
| Casamento pelo topo / pela base, no lugar do uniforme | 81,7 / 80,6 | 83,6 / 84,6 | 35,9 / 38,5 | tabela 4 |

Como ler: cada linha tira ou troca uma peça; a primeira é a referência; maior é melhor.

**Apêndice C, o caso mais perto do nosso** (aluno pequeno pré-treinado direto, sem a etapa geral, e sem dados
aumentados; tabela 7):

| Aluno | MNLI-m (392 mil pares) | MRPC (3,5 mil) | CoLA (8,5 mil) |
|---|---|---|---|
| BERT pequeno pré-treinado direto, ajustado na tarefa | 75,9 | 83,2 | 19,5 |
| O mesmo, com a destilação na tarefa | 79,2 | 82,9 | 12,4 |
| Aluno da etapa geral, com a destilação na tarefa | 80,5 | 82,4 | 29,8 |

Como ler: a segunda linha é a destilação na tarefa aplicada a um aluno pré-treinado do jeito comum. Ajuda na
tarefa grande (+3,3) e **não ajuda nas pequenas** (−0,3 e −7,1). Explicação deles, dada como conjectura: sem ter
imitado o BERT base no pré-treino, as partes internas do aluno não casam com as do professor, e imitá-las na
tarefa bagunça o que o aluno já sabia; com muito dado a tarefa compensa.

## O que isso diz sobre o nosso desenho

- O nosso aluno (`google/bert_uncased_L-4_H-512_A-8`) é um BERT pequeno pré-treinado direto, e o conjunto é de
  4.000 pares, sem aumento: é a condição da segunda linha do apêndice C em tarefa pequena, a que **não ajudou**.
  (O aluno deles tem 312 dimensões; o nosso, 512. Não é a mesma condição.)
- No TinyBERT, a fase interna imita **atenção e estados internos juntos**, antes das respostas. O "jeito 1" (só
  atenção, depois respostas) e o "pacote TinyBERT do jeito 2" (tudo junto num treino só) são, cada um, metade do
  que o artigo faz.
- A fase interna é bem mais longa que a das respostas: 20 épocas contra 3 (10 contra 3 nas tarefas grandes), e em
  dados 21 vezes maiores.
- A nossa perda de atenção (KL depois do softmax, média das cabeças) não é a deles (erro quadrático antes do
  softmax, por cabeça). 8 contra 12 cabeças segue sem fonte.

## Conferência do que já estava escrito no projeto

- Handoff de 16/11: "10–20 épocas de interior e 3 de respostas" e "sem atenção cai de 82,8 para 79,9 no MNLI, sem
  respostas para 80,5 (tabela 3)": **batem**.
- Plano, seção 11: "erro quadrático entre as notas de atenção antes do softmax (eq. 7)", "camada m aprende da 3m",
  "aluno com 12 cabeças": **batem**.
