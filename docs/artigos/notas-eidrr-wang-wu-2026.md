# Notas de leitura: EIDRR (Wang e Wu, 2026)

**Obra:** Heng Wang e Changxing Wu, "Improving Implicit Discourse Relation Recognition with Natural Language
Explanations from LLMs", AAAI 2026 (rodapé de copyright da AAAI no PDF), arXiv:2602.21763v1, 25/02/2026.
PDF em `eidrr-wang-wu-2026.pdf`, texto extraído em `eidrr-wang-wu-2026.txt` (as páginas citadas abaixo são as do PDF).

**Procedência: nível 2.** O Claude leu o texto principal inteiro (páginas 1 a 7; 8 e 9 são referências) em
18/11/2026. **Não lidos:** os apêndices A a G (ficam no GitHub, não no PDF) e o código. O Pedro não leu. Não citar
em texto assinado por ele antes de ele ler.

## O que o artigo faz

- **Tarefa principal:** dizer qual relação de discurso liga dois trechos (4 classes, corpus PDTB), sem conectivo
  explícito (p. 1).
- **Justificativas:** um LLM (Qwen-long) escreve uma para cada exemplo de treino, **recebendo o rótulo certo**. Cada
  uma tem duas partes: reconta os dois trechos e depois explica a relação (p. 2 e 3, Figura 2). Em 1.000 sorteadas,
  nota humana média 4,53 de 5; correção manual em menos de 100 casos de 15.004 (p. 3).
- **Modelo (p. 3 e 4, Figura 3, equações 1 a 3):**
  - encoder do tipo RoBERTa, compartilhado (o tamanho não está no texto principal);
  - **classificação por prompt:** a entrada termina em "The conjunction between Arg1 and Arg2 is `<mask>`", o modelo
    prevê o conectivo na máscara e uma regra o converte em relação;
  - **geração:** o encoder roda **de novo**, numa segunda entrada que já traz o rótulo previsto ("... is [rótulo], the
    main reason is that"); a saída passa por **uma camada Transformer nova, iniciada ao acaso**, e vai para o
    decoder de um T5, que gera a justificativa;
  - perda total = α x classificação + β x geração.
- **Treino em duas etapas (p. 4):** primeiro 30 épocas com α = 0,4 e β = 0,6 (ênfase em gerar), taxa 5e-6 no
  RoBERTa e 5e-5 no resto; depois α = 0,8 e β = 0,2, taxa 3e-5 no resto, e o melhor ponto na validação aparece em
  até 6 épocas. Dropout 0,3, AdamW, média de 3 sementes, uma RTX 3090.
- **Na inferência** o rótulo sai do caminho de classificação, que não lê justificativa nenhuma. A justificativa é
  gerada depois, a partir do rótulo previsto.

## Números (Tabela 1, p. 5; Tabela 3, p. 7)

Como ler: acurácia e F1 macro em %, média de 3 sementes, conjunto de teste. "Sem geração" é o mesmo modelo sem a
tarefa de gerar a justificativa.

| Conjunto (tamanho do teste) | Sem geração | Com geração | Diferença em acurácia |
|---|---|---|---|
| PDTB (1.046) | 71,80 / F1 66,87 | 73,14 / F1 68,01 | +1,34 |
| NLI, amostra de 1.499 de treino (600) | 74,83 / F1 74,79 | 75,83 / F1 75,73 | +1,00 |
| Sentimento por aspecto, Restaurant15 (576) | 85,59 / F1 70,18 | 87,44 / F1 71,30 | +1,85 |

Outras linhas da Tabela 1: T5 com cabeça de classificação no encoder e decoder gerando a justificativa, 63,67 para
64,91; os melhores métodos anteriores no PDTB ficam entre 70,84 e 72,52.

**Linha que importa para nós (Figura 4a, p. 5 e 6):** a versão **sem a camada de ponte**, com o RoBERTa ligado
direto ao decoder do T5 (eles chamam de e-INFERSENT), dá **73,04 de acurácia e 65,79 de F1**. Em acurácia é
praticamente o EIDRR (73,14); em F1 fica abaixo até do modelo sem geração (66,87). Segundo o texto, a ponte muda
sobretudo a qualidade da justificativa gerada (nota humana 1,71 sem ponte, 4,20 com).

## O que o artigo não tem

- **Sem desvio, intervalo ou teste estatístico.** O texto diz "significantly" (p. 5) sem teste.
- **Sem justificativa embaralhada ou aleatória.** O único controle é tirar a tarefa de geração.
- **Sem controle de calendário.** O texto não diz se o modelo "sem geração" passou pelas mesmas 30 + 6 épocas e
  pelas mesmas taxas. Se não passou, a diferença mistura a justificativa com o calendário (foi o que aconteceu
  aqui: nos 16.000 pares o calendário sozinho valia +0,007 de ROC-AUC).
- **O ponto é escolhido na validação** (p. 4), e não há número de quantas épocas o modelo sem geração treinou.
- **NLI:** o corpus não é nomeado, só "o usado em Chen et al. 2017"; não há linha de base de fora.
- As ablações estão no Apêndice C, não lido.

## Tamanho do efeito contra o tamanho do teste (conta do Claude, não do artigo)

- No PDTB, 1,34 ponto em 1.046 exemplos são cerca de **14 exemplos**. No NLI, 1,00 ponto em 600 são **6 exemplos**.
  No conjunto de sentimento, 1,85 em 576 são cerca de 11.
- O erro padrão de uma acurácia de 72% medida em 1.046 exemplos é cerca de 1,4 ponto; em 600 exemplos a 75%, cerca
  de 1,8. A comparação pareada no mesmo teste é mais apertada que isso, mas o artigo não dá o que seria preciso
  para calcular.

## Diferenças para o que foi rodado neste projeto (braço `bert_decoder`, receita do Agrawal)

| | EIDRR | O nosso braço com decoder |
|---|---|---|
| O que o decoder recebe | uma segunda passada do encoder, com o **rótulo previsto escrito na entrada** | os estados do encoder lendo só o par |
| Ponte encoder para decoder | uma camada Transformer nova | direto |
| Classificação durante a fase de gerar | sempre ligada (α = 0,4) | desligada na fase B |
| Taxa do encoder | 5e-6, 30 épocas e depois até 6 | 5e-5, 5 épocas |
| Justificativa | longa: reconta os dois trechos e explica | uma frase curta |
| Escolha do ponto | melhor época na validação | fim do treino, sem escolha |
| Medida | 3 sementes, teste de 600 a 1.046 exemplos | 5 sementes, dev de 9.842 pares, controle de calendário e embaralhado |

## Leitura do Claude

O ganho relatado é de 1 a 2 pontos, em testes pequenos, com 3 sementes e sem os dois controles (calendário e
justificativa trocada) que aqui mudaram a leitura do decoder. Não dá para dizer pelo artigo se o ganho vem da
justificativa. O que o artigo mostra com mais força é outra coisa: o modelo gera justificativas bem avaliadas por
pessoas (4,20 de 5) sem perder acurácia.
