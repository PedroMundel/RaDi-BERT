# 100 títulos alternativos (28/08/2026) — descargo de consciência

Gerados APÓS o tema provisório ser adotado (`tema-escolhido.md`), a pedido do Pedro, para
conferir se algo melhor ficou de fora. Todos passados na régua vigente: dor legível por
empregador + professional improvement + solucionável em 3–4 meses.

Legenda: ⭐ = melhor encaixe na régua · 〜 = vizinho do tema já escolhido (mesma família)

## F1 — Confiabilidade da extração

1. Quando o extrator mente: detecção aprendida de campos alucinados em extração estruturada por LLMs 〜
2. Orçamento de revisão humana: quanto conferir de uma extração automática para garantir uma taxa de erro alvo ⭐
3. Consenso entre modelos abertos como sinal de erro em extração de documentos 〜
4. Extração verificável: contratos de esquema, restrições e reparo automático de registros inválidos
5. O erro que não aparece: taxonomia e frequência de falhas silenciosas em pipelines de extração documental
6. Erros sintéticos treinam verificadores reais? Transferência entre perturbações injetadas e falhas observadas 〜
7. Confiança calibrada por campo: incerteza em nível de célula para extração generativa
8. Reparo assistido: modelos que corrigem registros extraídos em vez de descartá-los ⭐
9. Quanto custa a certeza: curvas de custo × erro residual em estruturação de acervos com modelos locais 〜
10. Auditoria amostral de datasets extraídos: estimativa de qualidade com garantia estatística a custo fixo ⭐

## F2 — Anotação, rótulos e economia

11. Quantos rótulos bastam? Previsão de orçamento de anotação a partir de pilotos pequenos ⭐
12. O preço do rótulo ruim: estimando ganho de desempenho por real investido em re-anotação ⭐
13. Anotação em cascata: quando o humano deve entrar e quando o modelo já basta
14. Discordância como sinal: usar desacordo entre anotadores para priorizar revisão e medir dificuldade
15. Active learning com orçamento realista: seleção de exemplos sob restrição de custo por hora de anotador
16. Pré-anotação automática muda o anotador? Efeitos de ancoragem em corpora anotados com apoio de IA ⭐
17. Guias de anotação como artefato testável: medir ambiguidade de esquema antes de anotar
18. Rótulos que envelhecem: detecção de anotações que deixaram de valer com mudança de domínio
19. Do especialista ao esquema: elicitação de conhecimento de domínio para esquemas de anotação em pt-BR
20. Quanto vale cada exemplo? Valoração de dados aplicada à decisão de coletar, comprar ou descartar

## F3 — Dados sintéticos

21. Portão para o sintético: critérios aprendidos de admissão de exemplos gerados em datasets de treino 〜
22. Diversidade ou fidelidade? O que determina a utilidade de corpora sintéticos em tarefas de extração
23. Sintético para as bordas: geração dirigida a fatias raras em vez de aumento indiscriminado ⭐
24. Proveniência de dado sintético: registrar prompt, modelo e versão como linhagem auditável
25. O gerador conhece o gabarito: vazamento entre geração e avaliação em datasets sintéticos
26. Contaminação silenciosa: detectar e medir conteúdo gerado por IA em acervos coletados da web
27. Dados sintéticos como substituto de dado sensível: utilidade preservada e risco de reidentificação
28. Aumento de dados que não paga: quando geração sintética degrada o modelo em vez de ajudar
29. Sintético local: geração com modelos abertos como alternativa viável a APIs em domínios restritos
30. Curadoria automática de corpora de treino: filtros aprendidos de qualidade em escala 〜

## F4 — Avaliação

31. Métrica que engana: diagnóstico de conjuntos de avaliação que não representam o uso real
32. Fatias que importam: descoberta automática de subgrupos onde o modelo falha ⭐
33. Contaminação entre treino e teste em benchmarks pt-BR: medição e correção
34. Juiz de máquina sob suspeita: limites de LLM-as-judge em avaliação de extração estruturada
35. Avaliação sem gabarito: sinais substitutos para monitorar qualidade quando não há rótulo ⭐
36. Benchmarks vivos: protocolo de atualização contínua de conjuntos de teste em domínios que mudam
37. Do F1 ao impacto: traduzir métricas de modelo em métricas de processo para decisão de negócio ⭐
38. Testes de comportamento para pipelines de dados: verificação por invariantes em vez de acurácia agregada
39. Quanto vale um ponto de F1? Análise de sensibilidade de decisões operacionais à qualidade do modelo
40. Reprodutibilidade em pipelines com LLM: variabilidade de resultados e como reportá-la

## F5 — Local, custo e soberania

41. Modelo aberto local ou API? Protocolo de decisão por tarefa a partir de sondas baratas ⭐
42. O custo real da inferência local: energia, tempo e qualidade em pipelines de dados sem nuvem
43. Quantização e qualidade de extração: até onde comprimir sem perder o registro
44. Cascatas econômicas: roteamento de documentos entre modelos pequenos e grandes por dificuldade estimada ⭐
45. Fine-tuning barato para estruturação: LoRA em modelos abertos vs. prompting em modelos maiores
46. Soberania de dado como requisito de projeto: arquitetura de pipelines de IA sem tráfego externo
47. Um modelo por domínio ou um modelo para todos? Especialização vs. generalidade em extração documental
48. Latência importa? Requisitos de tempo real em pipelines de estruturação de documentos
49. Do notebook ao servidor da empresa: viabilidade de pipelines de IA em hardware modesto
50. Destilação de capacidade de extração: transferindo competência de modelos grandes para pequenos locais ⭐

## F6 — Privacidade e LGPD

51. Minimização de dados sem perder o modelo: o que descartar sob a LGPD mantendo desempenho ⭐
52. Mapa de risco de acervo: identificação automática de dado pessoal e sensível antes do processamento ⭐
53. Anonimização que preserva utilidade: pseudonimização de corpora e seu custo em desempenho
54. O modelo lembra? Memorização de dados sensíveis em modelos ajustados com corpora institucionais
55. Direito ao esquecimento aplicado: custo e verificação da remoção de dados de um titular
56. Dados sintéticos protegem mesmo? Auditoria de reidentificação em corpora textuais gerados
57. Privacidade diferencial em extração de documentos: o preço em qualidade de garantias formais
58. Compartilhar sem expor: protocolos de publicação de datasets institucionais em pt-BR
59. Conformidade mensurável: traduzir exigências da LGPD em métricas técnicas verificáveis
60. Governança de acesso a dados de treino: rastrear quem usou o quê, e para qual modelo

## F7 — Manutenção e ciclo de vida

61. Quando o dataset vence: previsão de validade de dados de treino por domínio ⭐
62. Custo total de manter um modelo vivo: cronograma e orçamento de retreinamento por taxa de deriva ⭐
63. Monitorar sem rótulo: sinais de degradação de pipelines de extração em produção
64. Versionamento de datasets que importa: o que registrar para reproduzir um modelo dois anos depois
65. Esquemas que mudam: evolução de estrutura de dados sem quebrar modelos treinados
66. Reprocessar ou remendar? Decisão econômica de reconstruir datasets após melhoria do extrator ⭐
67. Deriva de fonte: quando o produtor do documento muda o formato e ninguém percebe
68. Pipelines que se explicam: instrumentação de proveniência para diagnóstico de falhas de dados
69. Modelos aposentados: critérios de descontinuação de sistemas de IA em produção
70. Dívida técnica de dados: identificação e priorização de passivos em pipelines de ML

## F8 — Estruturação e modelagem

71. Esquema induzido ou esquema imposto? Estratégias de modelagem para acervos documentais heterogêneos
72. Da tabela ao grafo: modelos de dados alternativos para conhecimento extraído de documentos
73. Integração de fontes heterogêneas com apoio de LLMs: correspondência de esquemas e resolução de entidades ⭐
74. Camadas bronze/prata/ouro como controles de qualidade: formalização e medição do ganho por camada
75. Documentos longos, contexto curto: estratégias de segmentação para extração estruturada confiável
76. Extração multimodal de documentos: quando o layout carrega a informação que o texto perde ⭐
77. Normalização de entidades brasileiras: CPF, CNPJ, endereços e nomes em corpora institucionais
78. Ontologias leves para domínios específicos: quanto de estrutura formal compensa na prática
79. Estruturar o suficiente: granularidade de esquema como variável de projeto em pipelines de dados
80. Consultas sobre acervos estruturados por IA: da extração ao uso analítico real

## F9 — Documentação, proveniência e reuso

81. Documentação que se gera sozinha: datasheets automáticos como subproduto do pipeline ⭐
82. Datasets brasileiros abandonados: levantamento de reusabilidade de corpora públicos em pt-BR
83. O que impede o reuso? Barreiras práticas à reutilização de datasets institucionais
84. Ficha técnica de dataset como contrato: documentação mínima para transferir dado entre times
85. Linhagem de dados em pipelines com IA: rastrear a origem de cada registro estruturado
86. Publicar o dado ou o pipeline? Estratégias de compartilhamento sob restrição legal
87. Metadados que sobrevivem: padrões de descrição para acervos documentais públicos
88. Curadoria colaborativa de corpora: modelos de contribuição e controle de qualidade distribuído
89. Do PDF ao dado aberto: protocolo de abertura de acervos públicos brasileiros ⭐
90. Custo de entrada: quanto trabalho é preciso para tornar um acervo público realmente utilizável

## F10 — Domínios com dor de mercado

91. Diários oficiais como fonte de dados estruturados: viabilidade, qualidade e limites
92. Jurisprudência em escala: estruturação de decisões judiciais para análise quantitativa
93. Licitações e contratos públicos: extração estruturada para detecção de padrões e auditoria ⭐
94. Prontuários e laudos: estruturação de texto clínico em pt-BR sob restrições de privacidade
95. Documentos financeiros e regulatórios: extração confiável em contexto de alta consequência ⭐
96. Atas e relatórios corporativos: transformar rotina documental em base analítica
97. Voz para dado: estruturação de acervos de áudio institucional com transcrição e extração
98. Registros de suporte ao cliente como fonte de dataset: qualidade, viés e utilidade
99. Dados de telemetria de jogos: estruturação de eventos para modelagem de comportamento
100. Acervos científicos brasileiros: extração estruturada de teses e artigos para mapeamento de pesquisa

---

# Rodada 2 — só domínios (28/08/2026)

Pedro reprovou as famílias F1–F9 (método-primeiro) e aprovou SÓ a F10 (domínio-primeiro):
**o tema deve ser nomeado pelo acervo, com o método por dentro.** Acesso ao dado é o critério
que mata tema em prazo de 3–4 meses. 🟢 público · 🟡 parcial, verificar · 🔴 privado/difícil
(🟢 = acervo oficialmente público; permissão de download em massa e licença AINDA NÃO verificadas).

## Compras públicas e controle

101. Acórdãos de tribunais de contas (TCU/TCEs): o que já foi glosado, e por quê 🟢⭐
102. Autos de infração e sanções administrativas a fornecedores 🟢
103. Aditivos e medições de obras públicas: sobrepreço e atraso no texto 🟡
104. Termos de referência de contratações de TI 🟢
105. Emendas parlamentares e sua execução orçamentária 🟡
106. Convênios e transferências a entidades privadas 🟢

## Trabalho e RH

107. Convenções e acordos coletivos de trabalho: cláusulas por categoria e região 🟢⭐
108. Editais de concurso público: requisitos, prazos e conteúdo programático 🟢
109. Processos e acordos trabalhistas 🟡
110. Anúncios de vaga e descrições de cargo: mapeamento de competências do mercado 🟢
111. Normas internas e políticas de compliance 🔴
112. Laudos periciais e decisões de benefícios previdenciários 🔴

## Regulação, saúde e segurança

113. Consultas públicas de agências reguladoras: contribuições em texto livre 🟢⭐
114. Registros e bulas de medicamentos: rastrear composição, indicação e alerta 🟢
115. Autos de infração sanitária e relatórios de inspeção 🟡
116. Boletins epidemiológicos e notas técnicas de saúde 🟢
117. Manifestações de ouvidoria e denúncias: triagem de texto livre em volume 🟡
118. Boletins de ocorrência e registros de segurança pública 🟡

## Meio ambiente, energia e agro

119. Licenças ambientais e suas condicionantes 🟢⭐
120. Autos de infração ambiental 🟢
121. Estudos de impacto ambiental: extração de compromissos em documentos gigantes 🟡
122. Contratos e leilões do setor elétrico 🟡
123. Receituários e registros de defensivos agrícolas 🟡
124. Relatórios de sustentabilidade e ESG corporativos 🟢

## Financeiro e jurídico não-judicial

125. Fatos relevantes e comunicados de companhias abertas 🟢⭐
126. Prospectos e documentos de oferta pública 🟡
127. Pareceres de procuradorias públicas 🟢
128. Acórdãos do CARF: jurisprudência tributária administrativa 🟢⭐
129. Contratos de concessão e parcerias público-privadas 🟡
130. Publicações do Diário da Justiça: intimações, prazos e partes 🟢⭐

## Propriedade intelectual, ciência e cidade

131. Pedidos e cartas-patente: vigilância tecnológica 🟢
132. Projetos de lei e proposições legislativas 🟢
133. Atas de conselhos municipais de saúde e educação 🟡
134. Planos diretores e legislação urbanística 🟡
135. Editais de fomento à pesquisa 🟢
136. Matrículas e registros imobiliários 🔴

## Destaques da rodada 2

- **107 (convenções coletivas)** — dor subestimada: todo DP precisa saber que cláusula vale para
  cada categoria/região; texto livre caótico; acervo público, mercado privado grande.
- **130 (Diário da Justiça)** — único com mercado JÁ pagando por software equivalente (captura de
  publicações e prazos): dor comprovada por preço.
- **128 (CARF)** — território jurídico sem a saturação do NLP judicial; tributarista paga por dado.
