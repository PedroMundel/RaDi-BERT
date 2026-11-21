# Avaliação da pesquisa (18/11/2026, noite)

**Procedência:** pedido do Pedro em 18/11 ("faz uma avaliação completa da pesquisa, acho que tá muito bom no rigor,
mas muito mal na contribuição, acho que seria legal melhorar isso antes de entregar algo"). Escrita pelo Claude. As
notas são opinião, sem rubrica. O Pedro não leu este arquivo.

**Conferido nesta sessão, no arquivo:** `resultados/esnli-treino-16k/leitura-grade.md` (inteiro);
`docs/2026-11-18-gaps-da-argumentacao.md` (inteiro); `docs/2026-11-18-o-que-o-decoder-gera.md` (inteiro);
`resultados/figuras/tabelas-artigo.md` e `INDICE.md`; em `resultados/rte-pequenos/leitura-grade.md`, as seções do
destaque (linhas 152 a 241), da destilação (458 a 676) e do professor que lê a justificativa (1069 a 1194);
`docs/pesquisa/2026-11-18-justificativa-em-encoder-o-que-deu-certo.md`; o termo da Semana 9; as linhas 258 a 281 e
354 a 391 de `docs/pesquisa/tema-v3-racionalizacao-encoder.md`; por busca de texto, que nenhum `.md` de `entrega/`
fala de destilação, calendário, justificativa embaralhada ou 16.000 pares do treino.

**Não conferido:** nenhum CSV foi recalculado (os números vêm das leituras); as seções de `rte-pequenos` fora das
linhas acima (marcas por camada, palavras novas, cabeça de grupos) entram pelo resumo do `CLAUDE.md`; a literatura
continua nível 3, salvo Agrawal (nível 1 do Pedro), MiniLM, TinyBERT e EIDRR (nível 2 do Claude); como a Residência
vai dar nota (o critério "processo, não produto" é de 11/09; a exigência de resultado positivo é leitura do Pedro,
a conferir com o coordenador); se as respostas do formulário de 29/10 existem.

## 1. Em uma frase

A pesquisa respondeu a uma das duas perguntas que o próprio tema tinha deixado de pé, com um controle que o artigo
de base não fez, e essa resposta não está em nenhum documento de entrega nem dita em uma frase em lugar nenhum.
Parte da nota baixa em contribuição é do que foi achado; outra parte é de como está contado.

## 2. O que o tema perguntava e o que foi respondido

O `tema-v3` (10/09, linhas 264 a 278 e 358 a 360) dizia que, depois do Agrawal, Ahemad & Sembium (2025), sobravam
duas perguntas: o controle (justificativa embaralhada no canal de saída de um encoder, que "ninguém rodou") e a
avaliação fora de domínio ("obrigatória": "sem teste fora de domínio, o trabalho não consegue responder a própria
pergunta").

**Como ler:** cada linha é uma pergunta que o projeto se fez; "estado" diz se há medida com critério escrito antes.

| Pergunta | Estado | Onde |
|---|---|---|
| O ganho do Agrawal se repete? | Não, em 9 condições; o +0,112 do RTE ficaria visível. O baseline 0,4754 não sai de nenhuma condição tentada, em dois checkpoints. "O artigo está errado" não se sustenta com isso | `tabelas-artigo.md` tabela 3; gaps 1 a 3 |
| **Controle: a justificativa embaralhada dá o mesmo que a certa?** | **Respondida, 16.000 pares, 5 sementes:** não dá. A certa fica 2,1 pontos acima da embaralhada; e as duas ficam abaixo do BERT sem decoder com o mesmo calendário (−0,9 e −3,0) | `esnli-treino-16k/leitura-grade.md`, itens 9 e 12 a 14 |
| O que parecia ganho do decoder era o quê? | O calendário de treino: sozinho vale +0,007 de ROC-AUC, 5 de 5. Caso não previsto no critério | idem, itens 8 a 10 |
| O decoder dá alguma coisa ao encoder? | Sim, no começo: +15 pontos nos primeiros 25 passos de classificação, só com a justificativa do par (3 sementes no embaralhado); some em cerca de 100 passos | idem, itens 16 a 23 |
| **Fora de domínio, o decoder ajuda?** | **Não rodou.** Só as marcas de atenção foram testadas fora (nulo, BERT small) | busca nas leituras do decoder: nenhuma menção |
| A justificativa carrega o rótulo? | Um BERT base que lê só a justificativa acerta 96,9% (o par sozinho dá 78,4%) | `rte-pequenos/leitura-grade.md`, linha 1085 |
| Outro canal (atenção) funciona? | Para nota, não (dentro e fora). Para apontar as palavras que o LLM copia, AP 0,724 contra 0,555 da melhor regra; utilidade para pessoa não testada | idem, linhas 152 a 241 |
| Algo sobe a nota do modelo pequeno? | Destilação comum (+1,6) e a sequência do TinyBERT (+0,93 no conjunto de escolha, +0,45 no dev, 15 sementes). Sem LLM e sem justificativa | idem, linhas 458 a 676 |

## 3. Nota por dimensão (opinião do Claude)

| Dimensão | Nota | Por quê |
|---|---|---|
| Rigor | 8,5 | Critério antes de rodar, controles pareados, ruído medido, nulos declarados, auditoria antes de cada treino. Tira ponto: 5 sementes na maioria; um professor e uma semente de professor; um LLM e um prompt; vários cortes escolhidos pelo Claude, um deles ambíguo; a avaliação humana das justificativas nunca foi tabulada |
| Contribuição como está escrita hoje | 4 a 5 | O que foi entregue (Semana 9) conta a versão mais fraca: "não repetiu no RTE" e o destaque. O material de 12 a 18/11 não existe para quem lê a entrega |
| Contribuição que os resultados já sustentam | 6 a 6,5 | O controle embaralhado no encoder com o confundidor de calendário separado é resultado de artigo curto ou de workshop; falta escopo (um conjunto, um LLM) e falta o teste fora de domínio que o próprio tema exigia |
| Clareza da história | 4 | Seis linhas de trabalho, nenhuma frase que as amarre |
| Domínio do autor sobre o material | não sei avaliar | Os resultados de 10 a 18/11 foram lidos pelo Claude; o `CLAUDE.md` registra que o Pedro não leu os exemplos do destaque, o MiniLM, o TinyBERT nem o EIDRR. Num programa que diz avaliar a pessoa, isso pesa, e só ele sabe quanto |

## 4. Por que a contribuição está baixa

1. **Nenhum resultado positivo usa o objeto do tema.** Os dois ganhos de nota são destilação entre BERTs, já
   publicada. Os positivos com justificativa de LLM são o destaque (sem uso demonstrado) e o arranque (que o Pedro
   descartou como objetivo em 18/11).
2. **O resultado mais forte está fora da entrega.** O controle embaralhado, o calendário, a curva e o professor que
   lê a justificativa estão em leituras internas. As figuras 25 a 29 e as tabelas "para o artigo" existem, sem texto.
3. **Não há tese.** Os fatos medidos permitem uma: "no encoder, gerar a justificativa do LLM como tarefa auxiliar
   não melhora a nota final; o que parecia ganho era o calendário; o conteúdo da justificativa importa (a errada
   custa 3,0 pontos, a certa 0,9); e o que a certa dá, o encoder aprende sozinho em cerca de 100 passos". Cada
   pedaço tem medida; a frase inteira não está escrita em nenhum arquivo.
4. **O porquê do nulo é hipótese.** "A justificativa repete o rótulo" combina com os 96,9% do professor que lê só a
   justificativa e com a curva de arranque, mas nenhum teste foi desenhado para derrubá-la. Também não está
   separado "a certa ensina o motivo" de "a errada atrapalha como ruído" (limite já escrito no gap 5).
5. **Falta a pergunta de fora de domínio para o decoder.** O tema a chamou de obrigatória; a pesquisa de 10/11 e a
   de 18/11 (nível 3) dizem que é fora da distribuição que justificativa costuma mostrar ganho.
6. **Escopo estreito:** um LLM (Qwen 35B), um prompt (F), um conjunto em escala (16.000 de 549 mil pares), BERT base.
7. **A replicação não fecha.** "Nenhuma condição tentada dá o número" é o teto sem a resposta dos autores, e a
   exigência do professor ("sem conseguir repetir, nem seu nulo eu considero") não foi cumprida ao pé da letra. O
   que existe no lugar: o mesmo caminho de gradiente move a nota em pontos inteiros quando o alvo muda (embaralhado
   −3,0), então o nulo não é de instrumento cego. Isso é argumento meu, não aceite do professor.
8. **Qualidade das justificativas sem medida humana:** a avaliação cega de 29/10 não tem resultado registrado.

## 5. O que pode mexer na contribuição até quinta

Sem ordem e sem recomendação (regra de 15/11). Os tempos de GPU são contas a partir de rodadas medidas em 18/11
(5 sementes do braço com decoder embaralhado: 2h50; 5 do calendário: 24 min), não medidos para estas rodadas.

**Como ler:** "o que acrescenta" é o que passaria a poder ser dito; "risco" é o que pode sair.

| Opção | O que acrescenta | Custo | Risco e limite |
|---|---|---|---|
| A. Documento de síntese com a tese do item 3, as tabelas 1 a 3 e as figuras 07, 10 e 29 | Leva o material de 12 a 18/11 para a entrega e dá uma frase à pesquisa. Ataca os itens 2 e 3 | Só escrita; nenhuma GPU | Não muda o que foi achado; continua sendo um negativo controlado. Você precisa ler antes de assinar |
| B. Teste fora de domínio do decoder: os braços calendário, decoder e, se couber, embaralhado, treinados nos 16.000 pares do e-SNLI e avaliados no RTE (2.767 pares, no disco; `esnli_dados.with_rte_labels` já existe) | Fecha a segunda pergunta que o tema deixou de pé (item 5). Qualquer resultado entra: ganho fora seria o primeiro positivo com justificativa; nulo fecha a pergunta | Mudança pequena no treino (avaliar um segundo conjunto no fim; os pesos não são salvos) e cerca de 3h15 de GPU para dois braços, 6 h com o embaralhado, dividindo entre as máquinas menos | O teste fora das marcas deu nulo; RTE tem 2 classes e é notícia, não legenda; critério teria de ser escrito antes |
| C. Tabular a avaliação humana de 29/10 | Uma medida humana da qualidade das justificativas do Qwen contra as do GPT-3 já julgadas (item 8) | Você exporta a planilha do Forms; a conta é de minutos | Não sei quantas respostas há; não mexe no resultado central |
| D. Braço sem as expressões de rótulo na perda do decoder (sua ideia de 28/10, nunca rodada) | Um teste desenhado para a hipótese do item 4: se a justificativa só repete o rótulo, tirar as palavras de rótulo do alvo muda o efeito | Máscara na perda auxiliar e cerca de 2h50 de GPU (5 sementes) | Pode dar nulo sem decidir nada; a tabela de expressões (202) foi montada pelo Claude |
| E. Corrigir a seção 6 de `entrega/marcas-de-atencao-e-destaque.md` ("a atenção muda, a decisão não") | Tira da entrega uma frase já derrubada | Minutos | Mexe em documento já entregue (decisão pendente desde o handoff) |

O que nenhuma opção resolve: repetir o Agrawal; ter mais de um LLM ou mais de um conjunto em escala; mostrar ganho
de nota final dentro da distribuição com justificativa (a busca de 18/11, nível 3, não achou ninguém que mostre
isso com controle e variância).
