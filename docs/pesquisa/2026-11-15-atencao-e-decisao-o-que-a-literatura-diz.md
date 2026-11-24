# Atenção e decisão: o que a literatura diz (15/11/2026)

## Procedência

Pesquisa **nível 3** (agente leu resumos e páginas, não os artigos inteiros). Serve para triagem, **nunca para citação**. Números abaixo vieram de um leitor automático sobre o texto; confira na fonte antes de usar em texto assinado.

| Como foi aberto | Itens |
|---|---|
| Texto integral em HTML (ar5iv), lido por modelo resumidor | Vashishth 2019; Jain & Wallace 2019; Stacey 2022; Pruthi 2020 (Deceive); Zhong 2019; Bao 2018; Carton 2022; Pruthi 2022 (TACL); FRESH; PoWER-BERT; LTP; Bastings 2019 (só uma pergunta) |
| Só resumo / página de metadados | Wiegreffe & Pinter 2019; Serrano & Smith 2019; Bastings & Filippova 2020; Bibal 2022; Abnar & Zuidema 2020; Zhang 2016; Brunner 2020; Michel 2019; Voita 2019; Kobayashi 2020; Kovaleva 2019; Clark 2019; ERASER; Kamath 2020; Desai & Durrett 2020; Lei 2016; Kostenok 2023; Ostmeier 2026; Amini & Kosseim 2022; Mohebbi 2023; Hassid 2022; Hao 2021 |
| **Não consegui abrir o texto** | **Herrewijnen et al. EACL 2026**: PDF binário ilegível para a ferramenta, sem versão HTML/arXiv; só resumo (página da ACL) e snippets de busca. Os detalhes de modelo, camadas e números **não foram conferidos**. |

Os PDFs diretos do arXiv não eram legíveis pela ferramenta; por isso o HTML do ar5iv. Onde a pergunta pedia algo que só o texto integral daria (por exemplo "qual camada") e o leitor não trouxe, escrevo "não conferido".

Itens **não conferidos / não listados como fonte**: ver seção final.

---

## Q1. O debate "atenção é / não é explicação"

### O que cada obra afirma e achou

| Obra | Ambiente | O que achou | Ressalvas |
|---|---|---|---|
| Jain & Wallace 2019, "Attention is not Explanation", NAACL 2019 ([arXiv 1902.10186](https://arxiv.org/abs/1902.10186)) | BiLSTM (principal), Average, CNN; SST, IMDB, MIMIC, 20News, AG News, CNN-QA, bAbI, SNLI | Pesos de atenção só se correlacionam de forma fraca com gradiente/leave-one-out; **permutar a atenção muitas vezes muda pouco a saída**; é "muito frequente" achar atenções adversariais bem diferentes com a mesma predição | Só RNN/CNN, **nenhum Transformer**; sem arquiteturas bi-atentivas típicas de pares; a exceção é MIMIC-diabetes, onde perturbar a atenção da classe positiva muda a saída. Nas tarefas de par (QA/NLI) o padrão é o mesmo, sem conclusão separada |
| Wiegreffe & Pinter 2019, "Attention is not not Explanation", EMNLP 2019 ([arXiv 1908.04626](https://arxiv.org/abs/1908.04626)) | RNN | Depende do que se chama "explicação". Propõe 4 testes (linha de base uniforme, variância entre sementes, diagnóstico com pesos congelados, treino adversarial ponta a ponta). Atenções adversariais existem, mas vão mal no teste diagnóstico | Resumo apenas. Link correto: arXiv 1908.04626 |
| Serrano & Smith 2019, "Is Attention Interpretable?", ACL 2019 ([arXiv 1906.03731](https://arxiv.org/abs/1906.03731)) | Classificadores de texto treinados; zera/mexe pesos | Peso alto às vezes tem mais influência, muitas vezes não; gradiente previu o efeito melhor que a magnitude da atenção. "Indicador ruidoso, nunca infalível" | Resumo apenas |
| Vashishth et al. 2019, "Attention Interpretability Across NLP Tasks" ([arXiv 1909.11218](https://arxiv.org/abs/1909.11218), preprint, sem venue na página) | Classificação de uma sequência, NLI, QA, NMT | **Sequência única (sentimento, tópico):** trocar a atenção por uniforme/aleatória quase não muda a acurácia (queda média ~0,5 a 0,9 ponto; permutar na inferência ~4,2). **Pares e geração:** atenção uniforme derruba muito (queda relativa média 49,5% em pares; SNLI com Bahdanau cai ~43 pontos na inferência). Conclui: atenção é interpretável quando é calculada sobre duas entradas e é essencial à predição | Modelos com atenção tipo Bahdanau (RNN), não BERT |
| Pruthi et al. 2020, "Learning to Deceive...", ACL 2020 ([arXiv 1909.07913](https://arxiv.org/abs/1909.07913)) | Embedding+Atenção, BiLSTM+Atenção, **BERT-base** (média e máximo entre cabeças), enc-dec GRU; 4 classificações e 4 seq2seq | Dá para treinar o modelo a pôr **quase zero de atenção** nos tokens "proibidos" com custo mínimo de acurácia (BERT, ocupação: 97,2% mantidos, massa de atenção em gênero 13,9 para 0,01) e **o modelo continua usando esses tokens**, por outros caminhos (RNN passa informação aos vizinhos; no modelo de embeddings sem contexto, aumenta a norma do embedding) | Quais camadas do BERT foram restritas: não conferido. Prova que **mexer na atenção sem mexer na decisão é possível**, no sentido "tirar" atenção |
| Bastings & Filippova 2020, BlackboxNLP 2020 ([arXiv 2010.05607](https://arxiv.org/abs/2010.05607)) | Artigo de posição | Para o objetivo "quais tokens importam" (público: desenvolvedor), métodos de saliência servem melhor que atenção | Sem experimentos novos |
| Bibal et al. 2022, "Is Attention Explanation? An Introduction to the Debate", ACL 2022 ([ACL Anthology](https://aclanthology.org/2022.acl-long.269/)) | Levantamento | Revisa e compara a discussão; áreas se comunicam mal | Resumo apenas |
| Abnar & Zuidema 2020, "Quantifying Attention Flow in Transformers" ([arXiv 2005.00928](https://arxiv.org/abs/2005.00928), preprint, sem venue na página) | Transformers | Atenção bruta é sonda de explicação pouco confiável porque a informação se mistura entre camadas; rollout e flow correlacionam mais com ablação e gradiente que a atenção bruta | Resumo apenas |

### Trabalhos de 2022 a 2026 sobre Transformers

| Obra | Achado (da página) |
|---|---|
| Amini & Kosseim 2022, "How (Un)Faithful is Attention?", BlackboxNLP 2022 ([ACL Anthology](https://aclanthology.org/2022.blackboxnlp-1.10/)) | Métrica AtteFa de fidelidade; testa efeito da frequência de elementos informativos e de codificadores contextuais vs. não contextuais |
| Hassid et al. 2022, "How Much Does Attention Actually Attend?", Findings EMNLP 2022 ([arXiv 2211.03495](https://arxiv.org/abs/2211.03495)) | Em Transformers pré-treinados, trocar as matrizes de atenção por matrizes constantes (média de muitas entradas) custa em média ~8% relativo em seis tarefas; trocar metade quase não custa. Modelos mais fortes perdem mais |
| Mohebbi et al. 2023, "Quantifying Context Mixing in Transformers", EACL 2023 ([arXiv 2301.12971](https://arxiv.org/abs/2301.12971)) | Atenção sozinha dá quadro infiel da mistura de contexto; propõe Value Zeroing sobre o bloco inteiro |
| Herrewijnen et al. 2026, EACL 2026 ([ACL Anthology](https://aclanthology.org/2026.eacl-long.31/)) | Ver Q2. Snippets de busca dizem que mudanças na atenção "não se refletem" nas explicações SHAP (não conferido na página) |

### Ponto-chave: dá para mudar muito os pesos de atenção SEM mudar a predição?

**Resposta curta: sim, é resultado estabelecido em parte dos ambientes, e falso em outros. Não é um resultado geral.**

| Condição | Mudar atenção sem mudar saída? | Fonte |
|---|---|---|
| Classificação de **sequência única**, RNN | **Sim**: permutar/uniformizar quase não muda a saída | Jain & Wallace 2019; Vashishth 2019 (atenção vira "porta") |
| **Pares** (NLI, QA) com atenção sobre uma sequência condicionada na outra | **Não**: uniforme derruba a acurácia em dezenas de pontos | Vashishth 2019 |
| **Treinar** o modelo para tirar atenção de certos tokens (RNN, embeddings, BERT) | **Sim**, e o modelo segue usando os tokens por outros caminhos | Pruthi 2020 |
| Transformer pré-treinado, atenção trocada por constante | Queda pequena em média (~8% relativo), maior em modelos mais fortes | Hassid 2022 |
| Supervisionar a atenção do `[CLS]` na última camada em NLI (BERT) | **Muda a decisão**: ganho pequeno com marcas reais, **piora** com marcas embaralhadas | Stacey 2022 (Q2) |

Limites do consenso (todos do que as fontes dizem, mais inferência marcada):

- Os resultados "atenção não importa" são sobretudo de RNN e de sequência única. Vashishth 2019 usa isso para explicar a divergência entre Jain & Wallace e outros.
- Quase nada na lista acima testa a intervenção "supervisionar só a última camada, média entre cabeças" em Transformer pequeno.
- **Inferência do agente:** a frase "mudar a atenção não muda a decisão" é verdadeira como observação deste experimento (a nota não mudou), mas **não é um fato geral** da literatura, e o próprio experimento do aluno a contradiz em parte: as marcas aleatórias derrubaram a acurácia em ~0,04 a 0,05. Se a atenção supervisionada não tivesse influência na decisão, marcas aleatórias não deveriam custar nada.

### Contradição com a frase do assistente ("mudar a atenção não muda a decisão")

- **Contra:** Stacey et al. 2022 supervisionam exatamente `[CLS]`, última camada, em BERT, em NLI, e o controle com a distribuição embaralhada "performs worse than the baseline" (SNLI test 89,50 contra 89,77; SNLI-hard 78,84 contra 79,36). Atenção supervisionada, portanto, muda a saída. Vashishth 2019 mostra que, em pares, alterar a atenção muda muito a saída. Pruthi 2022 e Herrewijnen também (Q2).
- **A favor, só sob condições:** sequência única + RNN (Jain & Wallace; Vashishth); "tirar" atenção de tokens (Pruthi 2020); Transformer pré-treinado com atenção constante (Hassid 2022). Em todos, a medida é "a saída não muda quando a atenção muda", e isso não equivale a "a atenção não tem papel".
- **Inferência do agente:** a redação defensável é "neste setup, levar a atenção do `[CLS]` da última camada para as marcas (0,29 para 0,80) não alterou o ROC-AUC", sem generalizar.

---

## Q2. Supervisionar atenção com justificativas ajuda?

| Obra | Modelo | Atenção supervisionada | Dados | Ganho sobre baseline | Controle aleatório/embaralhado |
|---|---|---|---|---|---|
| Zhang, Marshall & Wallace 2016, EMNLP 2016 ([arXiv 1605.04469](https://arxiv.org/abs/1605.04469)) | CNN por sentença | Peso de cada sentença no documento, com supervisão de justificativas | 5 conjuntos | "Supera linhas de base fortes" (resumo; números não conferidos) | Não conferido |
| Bao et al. 2018, EMNLP 2018 ([arXiv 1808.09367](https://arxiv.org/abs/1808.09367)) | Classificador com atenção + R2A | Atenção-alvo gerada por mapa justificativa para atenção, transferido de domínios ricos | Alvo: 200 exemplos com justificativas por aspecto | Domínio hotel: 84,52 contra 82,10 (location), 90,66 contra 89,01, 89,93 contra 87,91; "15,08% de redução média de erro" | Linhas de base sem justificativa e com supervisão direta (Ra-Trans); sem controle aleatório |
| Zhong, Shao & McKeown 2019 ([arXiv 1908.04626](https://arxiv.org/abs/1908.04626)) | AttnLSTM (Bi-LSTM) | Atenção com perda KL contra distribuição uniforme sobre as justificativas humanas | MPQA 100 a 800 justificativas; GFBF 50 a 400 | +4,9 a +8,3 pontos (MPQA incl. 32,7 para 37,6; GFBF excl. 80,4 para 88,7); 100 justificativas rendem ~metade do ganho do MPQA | Atenção sem treino, multitarefa; sem controle aleatório |
| **Stacey, Belinkov & Rei 2022**, AAAI 2022 ([arXiv 2104.08142](https://arxiv.org/abs/2104.08142)) | **BERT-base**, DeBERTa | **`[CLS]`, última camada, top-K cabeças (K em {1,3,6,9,12}; melhor K=3)**; MSE com λ=1,0 | e-SNLI 550 mil pares; 25 sementes | SNLI +0,40; SNLI-hard +0,79; MNLI +0,84/+0,91; HANS +1,59; **ANLI −0,40**; DeBERTa +0,1 | **Sim**: distribuição embaralhada separadamente em premissa e hipótese **piora** (SNLI-test 89,50 contra 89,77; hard 78,84 contra 79,36; MNLI ~71,2 a 71,5 contra 72,4) |
| Pruthi et al. 2022, TACL ([arXiv 2012.00893](https://arxiv.org/abs/2012.00893)) | Aluno BERT-base/large, BiLSTM | Regularização KL da atenção do aluno para os tokens do professor | IMDb 600 a 4.000; NQ 250 a 500 | Humano, 600 exemplos: 75,5 para 81,5; professor automático, 1.000: 91,5 para 93,9 (+1,4 a +2,6 nos transformers); ganho **encolhe com mais dados** | **Sim**: explicações aleatórias não ajudam de forma confiável (BERT-base 90,6 contra 91,5; mas BiLSTM 4.000: 75,8 contra 71,1, misto) |
| Carton, Kanoria & Tan 2022, Findings ACL 2022 ([arXiv 2112.00071](https://arxiv.org/abs/2112.00071)) | BERT-base, modelo extrator+preditor | **Não supervisiona atenção**: supervisiona a máscara por token do extrator | MultiRC, FEVER, e-SNLI | Melhor modelo: MultiRC 71,2 contra 68,1; FEVER 91,5 contra 90,2; e-SNLI 90,1 contra 89,7 (p=0,1, não significativo); o modelo supervisionado ingênuo piorou em e-SNLI (87,8) | Sem controle aleatório. Achado: maximizar a acurácia na justificativa não é o melhor caminho |
| Herrewijnen, Nguyen, Bex & Gatt 2026, EACL 2026 ([ACL Anthology](https://aclanthology.org/2026.eacl-long.31/)) | Modelos tipo BERT | Regularização da atenção com justificativas humanas | **Não conferido** | Pelo resumo: justificativas aleatórias "frequentemente" dão ganhos parecidos; humanas ganham ao reduzir sensibilidade a correlações espúrias fortes | **Sim, é o desenho central** (aleatório contra humano) |
| Atenção supervisionada por justificativa de LLM | (nenhuma obra encontrada) | | | | A busca não achou perda direta na atenção do encoder com justificativa gerada por LLM. O COLING 2025 (Agrawal et al.) usa justificativa de LLM como tarefa auxiliar em decoder, sem perda na atenção |

### Consenso

- **Inferência do agente:** "ajuda pouco e de forma condicional". Ganhos grandes (4 a 8 pontos, 15% de erro) aparecem em **poucos dados** (50 a 800 justificativas, 200 exemplos, 600 a 1.000 exemplos), RNN/CNN. Em BERT com dados cheios: +0,4 em dentro da distribuição, +0,8 a +1,6 fora (e −0,4 em ANLI). Pruthi 2022 diz que o ganho encolhe com mais dados.
- Herrewijnen 2026 sugere que parte do ganho vem da **regularização**, não do conteúdo da justificativa (aleatório dá resultado parecido); o conteúdo só se paga em espúrios.
- Resultado do aluno (ROC-AUC sem mudança; aleatório pior em ~0,04 a 0,05) é **compatível** com "sem ganho consistente" mas **difere** de Herrewijnen (aleatório não piora ali, segundo o resumo) e de Stacey (aleatório embaralhado piora só ~0,3 a 1,2).

### O que as obras com ganho fizeram de diferente do setup do aluno

| Escolha | Obras com ganho | Setup do aluno |
|---|---|---|
| **Só algumas cabeças** (Stacey: top-3 de 12, melhor que as 12) | Stacey 2022 | **Média entre todas as cabeças**, sem seleção (a média inclui cabeças que a tarefa não usa) |
| Dados | e-SNLI 550 mil (Stacey); ou poucos dados + transferência (Bao, Zhong, Pruthi 2022) | ~2.500 pares |
| Modelo | BERT-base 12 camadas; LSTM | BERT pequeno, 4 camadas, 512 |
| Alvo | Explicações humanas curtas (e-SNLI: palavras destacadas) | Cópia de justificativa de LLM |
| Pesos da perda | λ=1,0 (BERT) com MSE | 1,0 com perda não conferida |
| Variante com camada extra sobre o modelo | Stacey: camada extra supervisionada ganhou **menos** | Não aplicável |
| Controle | Embaralhado, aleatório, multitarefa | Aleatório (mesmo método) |

**Inferência do agente:** a maior diferença visível é a média entre todas as cabeças contra top-3; segunda, o tamanho do modelo/dados. Não é possível dizer qual explica o nulo sem testar.

---

## Q3. O nulo pode ser artefato?

### Razões, com fonte

| Razão | Fonte (verificada em resumo) | Como se aplica |
|---|---|---|
| **Informação já agregada em camadas anteriores** e mistura de contexto por todo o bloco: atenção sozinha dá quadro infiel | Brunner et al. 2020, ICLR ([arXiv 1908.04211](https://arxiv.org/abs/1908.04211)): identidade do token se preserva no ângulo do embedding e some com a profundidade; informação "fortemente misturada". Mohebbi 2023; Abnar & Zuidema 2020 | No BERT de 4 camadas, a camada 3 já mostra ~0,4 de atenção nas marcas em todos os modelos, o que sugere que a informação das marcas já chegou ao `[CLS]` antes da camada 4 (**inferência do agente**) |
| **Pesos de atenção superestimam a contribuição**: o que conta é peso x norma do vetor de valor | Kobayashi et al. 2020, EMNLP ([arXiv 2004.10102](https://arxiv.org/abs/2004.10102)) | Subir o peso de uma palavra não garante que ela contribua mais; o modelo pode encolher a norma dos valores dessas palavras |
| **Redundância de cabeças** | Michel et al. 2019, NeurIPS ([arXiv 1905.10650](https://arxiv.org/abs/1905.10650)); Voita et al. 2019, ACL ([arXiv 1905.09418](https://arxiv.org/abs/1905.09418)); Kovaleva 2019, EMNLP ([arXiv 1908.08593](https://arxiv.org/abs/1908.08593)): cabeças reusam poucos padrões e desligar algumas pode melhorar | A média entre cabeças dilui; só poucas cabeças especializadas carregam a decisão, e Stacey usa top-3 |
| **Atenção do `[CLS]` / tokens especiais**: BERT concentra atenção em delimitadores e deslocamentos posicionais | Clark et al. 2019, BlackboxNLP ([arXiv 1906.04341](https://arxiv.org/abs/1906.04341)); Kobayashi 2020 diz que BERT atende **menos** aos tokens especiais do que se pensava | Pode haver um piso de atenção fixo, e a medida "0,29 para 0,80" depender de como os tokens especiais entram na soma |
| **Atenção bruta tolerada**: Transformers pré-treinados toleram atenção constante | Hassid et al. 2022 | A decisão pode depender pouco da atenção do `[CLS]` na última camada |
| **Treino não impede caminho alternativo** | Pruthi 2020 | O modelo pode usar a informação das marcas por vizinhos, que a perda de atenção não toca |
| **Que camada Kovaleva diz ser "task-agnostic"** | Não conferido: o resumo cita só padrões reutilizados e desligar cabeças; **a afirmação sobre a última camada do `[CLS]` não está no resumo** | Não usar como fonte sem ler o artigo |

### O que as obras supervisionadas fazem

- Stacey: `[CLS]`, última camada, top-K cabeças, com K ajustado; camada extra supervisionada teve ganho menor. Atenção de **todos os tokens** sobre premissa e hipótese **não** é o que ela supervisiona; ela supervisiona o `[CLS]`.
- Zhong, Pruthi 2022, Bao: atenção do modelo de classificação sobre palavras (RNN) ou atenção de aluno por KL.
- Não conferido: se alguma obra supervisiona várias camadas.

### Verificações sugeridas pela literatura para separar "atenção não importa" de "intervi no lugar errado"

| # | Verificação | Distingue | Fonte de apoio |
|---|---|---|---|
| 1 | **Substituir a atenção na inferência** (uniforme, permutada, constante) em cada camada e cada cabeça, medir a mudança na saída | "A atenção do `[CLS]` não é usada" contra "é usada mas a mudança não altera a decisão" | Jain & Wallace; Serrano & Smith; Vashishth; Hassid |
| 2 | **Ablação das palavras marcadas** (suficiência/abrangência) no modelo com e sem a perda | Se as marcas carregam a decisão no modelo treinado | DeYoung et al. 2020 (ERASER, ACL 2020, [arXiv 1911.03429](https://arxiv.org/abs/1911.03429)) |
| 3 | **Concordância com atribuição** (gradiente, rollout, Value Zeroing) em vez de só atenção | Se a mudança na atenção se reflete na contribuição real | Abnar & Zuidema; Mohebbi 2023; Bastings & Filippova 2020 |
| 4 | **Supervisionar outras camadas** e **só top-K cabeças** (copiar Stacey), incluindo a camada 3 | "Lugar errado" contra "não importa" | Stacey 2022 |
| 5 | **Análise por norma** (peso x norma de valor) das palavras marcadas | Se o peso subiu mas a contribuição não | Kobayashi 2020 |
| 6 | **Controle de caminho alternativo**: zerar a atenção do `[CLS]` às marcas na inferência e ver se a nota cai | Se o modelo usa as marcas por outro caminho | Pruthi 2020 |
| 7 | **Mais sementes** (o aluno já mediu variação de até 0,026 entre rodadas) | Efeito pequeno contra ruído | Registro do projeto (não é da literatura) |

---

## Q4. Atenção como sinal de incerteza ou adiamento

| Obra | Achado |
|---|---|
| Kamath, Jia & Liang 2020, ACL 2020 ([arXiv 2006.09462](https://arxiv.org/abs/2006.09462)) | Abster-se pela probabilidade softmax vai mal sob mudança de domínio (modelo superconfiante). Um calibrador treinado para prever erro responde 56% das perguntas a 80% de acurácia contra 48% do softmax (QA, não classificação) |
| Desai & Durrett 2020, EMNLP 2020 ([arXiv 2003.07892](https://arxiv.org/abs/2003.07892)) | BERT e RoBERTa em NLI/paráfrase/senso comum: bem calibrados dentro do domínio; fora, erro de calibração até 3,5x menor que linhas de base sem pré-treino; temperature scaling e label smoothing ajudam |
| Kostenok, Cherniavskii & Zaytsev 2023 ([arXiv 2308.11295](https://arxiv.org/abs/2308.11295), preprint) | Atributos topológicos das matrizes de atenção superam métodos existentes em aceitabilidade gramatical e detecção de texto artificial; os métodos clássicos ficam perto de heurísticas simples (resumo) |
| Ostmeier et al. 2026 ([arXiv 2602.13699](https://arxiv.org/abs/2602.13699), "EMNLP 2026 Findings" segundo a página) | HeadEntropy (entropia de Rényi por cabeça) prevê correção da resposta de **LLMs**, AUROC 0,736, 5 LLMs e 5 conjuntos; não é classificador encoder |

**Resposta em uma linha:** há evidência de que features de atenção (topológicas, entropia por cabeça) preveem erro, mas **não encontrei comparação direta, em classificador BERT, de entropia/concentração da atenção contra a confiança softmax**; as linhas de base de confiança (Kamath, Desai & Durrett) são calibração/abstenção por softmax. Evidência existente é de classificação de aceitabilidade (Kostenok) e de LLMs generativos (Ostmeier), então **a transferência para NLI com BERT pequeno é inferência do agente, não resultado**.

---

## Q5. Destaque de um modelo pequeno para podar a entrada de um maior

| Obra | Tarefa(s) | Fração de tokens | Acurácia mantida | Contra aleatório / regra |
|---|---|---|---|---|
| Lei, Barzilay & Jaakkola 2016, EMNLP 2016 ([arXiv 1606.04155](https://arxiv.org/abs/1606.04155)) | Sentimento multi-aspecto, recuperação de perguntas | Não conferido | Supera linha de base com atenção "por margem significativa" (resumo) | Não conferido |
| Bastings, Aziz & Titov 2019 ([arXiv 1905.08160](https://arxiv.org/abs/1905.08160), preprint) | Sentimento; **SNLI** | SNLI: alvo de 10% de atenção não nula (8,5% efetivo) | **SNLI 85,5% teste (86,0% dev)** | Não conferido contra aleatório |
| FRESH, Jain et al. 2020, ACL 2020 ([arXiv 2005.00115](https://arxiv.org/abs/2005.00115)) | SST, AgNews, Evidence Inference, Movies, MultiRC (**sem NLI**) | 10% a 30% | F1 macro: SST .81 contra .90 integral; AgNews .91 contra .94; EI .68 contra .73; Movies .94 contra .95; MultiRC .67 contra .68 | Aleatório só no estudo humano (Movies: aleatório contíguo 0,84, FRESH 0,92) |
| PoWER-BERT, Goyal et al. 2020, ICML 2020 ([arXiv 2001.08950](https://arxiv.org/abs/2001.08950)) | GLUE: RTE, MNLI, QQP, QNLI etc. | RTE: 868 de 3.072 vetores (~28%) | Queda <1 ponto: RTE 68,1 para 67,4; MNLI-m 84,6 para 83,8; QQP 71,2 para 70,2 (aceleração 2,0 a 4,5x) | SST-2 dev: primeiros-k 85,4%, aleatório 85,7%, por atenção 88,3% |
| LTP, Kim et al. 2022, KDD 2022 ([arXiv 2107.00910](https://arxiv.org/abs/2107.00910)) | GLUE, RoBERTa-base | Não reporta tokens mantidos; FLOPs ~45 a 52% menores | MNLI-m 87,53 para 86,53; QQP 90,39 para 89,69; RTE 77,98 para 77,98 | Sem baseline aleatório; compara com SpAtten e LAT |

**Resposta em uma linha:** poda por atenção/aprendida mantém dentro de ~1 ponto no GLUE (inclusive RTE e MNLI) com cerca de metade dos FLOPs ou ~28% dos vetores no RTE, e supera seleção aleatória/primeiros-k no que foi medido (SST-2, +2,6 a +2,9); **a obra com NLI (SNLI) e seleção por modelo separado é Bastings 2019 (85,5%), sem comparação com aleatório**. Nenhuma das obras acima usa um modelo *pequeno* como seletor para um maior (PoWER-BERT e LTP podam dentro do mesmo modelo).

---

## Não conferido (não usar como fonte)

- **Herrewijnen et al. 2026**: existência verificada (página da ACL), mas **detalhes (modelo, camada, números) não conferidos**; a afirmação sobre SHAP veio só de snippet de busca.
- Kovaleva 2019: a tese "atenção do `[CLS]` na última camada é agnóstica à tarefa após o ajuste fino" **não está no resumo** e não foi conferida.
- Detalhes de camadas restringidas em Pruthi 2020 com BERT.
- Zhang 2016, Wiegreffe & Pinter, Serrano & Smith, Brunner, Michel, Voita, Kobayashi, Clark, Lei: **só resumo**.
- Vistos só em snippets de busca, **não abertos**: UAT-Lite (arXiv 2602.02952), Ensembling Pruned Attention Heads (arXiv 2510.18358), "attention divergence" LLM (arXiv 2605.05025). Não entram como fonte.
- Jayaram & Allaway 2021 (justificativas humanas como prioridade de atribuição): citado por snippet, **não encontrado**, não listado como fonte.
- Um ID tentado por engano (arXiv 1909.00031) correspondia a outro artigo e foi descartado; o Zhong 2019 correto é arXiv 1908.04626.

---

## O que isto muda para a decisão

- Não escrever "mudar a atenção não muda a decisão". Escrever o que foi medido: nesta configuração, subir a atenção do `[CLS]` da última camada para as marcas (0,29 para 0,80) não mudou o ROC-AUC.
- O próprio resultado do aluno (marcas aleatórias custam ~0,04 a 0,05) mostra que a perda de atenção **afeta** a decisão, ao menos quando é prejudicial. Isso é inferência do agente, mas é coerente com Stacey (embaralhado piora).
- A literatura que diz "atenção pode mudar sem mudar a saída" é de RNN e sequência única (Jain & Wallace, Vashishth) ou de "tirar" atenção (Pruthi 2020); em pares, alterar a atenção costuma mudar muito a saída.
- O estudo mais próximo (Stacey 2022) usa o mesmo alvo (`[CLS]`, última camada, BERT, NLI) e obtém ganho pequeno (+0,4 dentro, +0,8 a +1,6 fora, −0,4 em ANLI) **com top-3 cabeças e 550 mil pares**. O nulo do aluno é plausível mesmo se a técnica funcionar em geral.
- Antes de concluir "a atenção não importa", fazer as checagens 1, 2, 4 e 6 da Q3 (trocar a atenção na inferência, ablação das marcas, outras camadas e top-K cabeças, zerar atenção às marcas).
- Herrewijnen 2026 sugere que o ganho típico vem da regularização e não do conteúdo; o controle aleatório do aluno é o desenho certo, mas o resultado depende de ler esse artigo (não conferido aqui).
- Para usar atenção como sinal de adiamento (Q4), não há evidência direta em BERT; seria teste novo contra a confiança softmax (Kamath; Desai & Durrett).
- Para poda guiada por destaque (Q5), a literatura existente mostra que seleção por atenção bate aleatório e regras simples e mantém ~1 ponto no GLUE; não há obra com seletor pequeno e leitor maior em NLI.

## Limites desta pesquisa

- Nível 3: resumos e leitura automática de HTML; números podem ter erro de sumarização.
- Herrewijnen 2026, a obra mais próxima do desenho do aluno em controle aleatório, não foi aberta em texto.
- Busca limitada a poucas consultas; trabalhos de 2022 a 2026 sobre intervenção em atenção de Transformers estão **subamostrados**.
- Nenhuma obra achada reproduz o setup exato (BERT de 4 camadas, média entre cabeças, justificativa de LLM, ~2.500 pares).
- As comparações numéricas entre obras misturam métricas (F1, acurácia, erro) e conjuntos diferentes.
