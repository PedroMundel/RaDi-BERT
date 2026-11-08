# Temas candidatos — 20 propostas (19/08/2026)

Gerados a partir de: config C2×C1×C6, gostos declarados do Pedro (jurídico/Ultimatum, games, voz/áudio, estruturação, bronze/silver/gold), mapa de lacunas da autoavaliação, precedentes das turmas anteriores e regra **R1** (todo tema termina treinando ou avaliando um modelo de verdade). Todos pensados para caber no ICDATA'26.

Três pares espelhados (A1↔B2, A7↔B7/B8, A2↔B5) mostram na prática o que a escolha de âncora muda: **qual lado é a pergunta de pesquisa e qual é o instrumento.**

---

## Conjunto A — âncora C2 (dados), ML como satélite

**A1. O gap sintético→real** ⭐ candidato natural
Datasets sintéticos de LLM passam nos gates de qualidade e falham no dado real (Ultimatum: F1 0,918→0,655). Construir métricas de qualidade que *prevejam* o gap antes do treino; validar no Ultimatum + 1 dataset público. — C2×C1, G06; continuação direta do que você já tem.

**A2. Anotação assistida por LLM vs humana vs híbrida**
Mesmo corpus pt-BR anotado por 3 vias; medir custo × qualidade × concordância × F1 do modelo final. — M14, I17, C1; responde "quando o LLM substitui o anotador?".

**A3. Active learning com LLM no circuito**
Quanto rótulo humano dá para economizar mantendo o F1, com o modelo escolhendo o que rotular e o LLM pré-rotulando? Pipeline com orçamento de anotação explícito. — I17, C1, G06; sua maior lacuna de interesse alto.

**A4. Estruturação por LLM: schema induction de documentos pt-BR** ⭐ ênfase declarada
LLM transforma documentos não-estruturados (jurídicos, notas, laudos) em dados estruturados com esquema induzido; avaliar a qualidade da estrutura e treinar modelo sobre ela. Variação: gerar datasheets/proveniência automaticamente no processo (M09/F05). — A02, M08, F05, C1.

**A5. Caça a erro de rótulo em datasets pt-BR públicos**
Outlier detection + LLM-judge para achar anotações erradas em benchmarks pt-BR usados por todo mundo; corrigir e medir quanto o modelo melhora. — D04, G01; resultado com impacto público imediato.

**A6. Drift e janelas de retreinamento**
Quando um dataset de treino "vence"? Detecção de drift no dado e política de retreinamento para NLP pt-BR. — Q09, G06; dois TCCs anteriores de drift = precedente sem saturação.

**A7. Anonimização LGPD com NER: privacidade × utilidade** ⭐ sequência do Ultimatum
Pipeline de pseudonimização de corpus jurídico usando o NER do Ultimatum; medir o trade-off entre grau de anonimização e desempenho do modelo treinado no corpus anonimizado. — C6×C2×C1 completo.

**A8. Benchmark de qualidade de dados pt-BR (DataPerf-like)**
Perturbar datasets (ruído, desbalanceio, rótulos errados) e medir sensibilidade de modelos; ranquear operações de limpeza por ganho real. — G01, G06, K02; não existe para pt-BR.

**A9. Lakehouse bronze/silver/gold como gate de qualidade para ML**
Formalizar as camadas como controles de qualidade de features; medir o impacto de cada camada no desempenho do modelo final. — F03, I14, I27; parte da sua única experiência prática de estruturação.

**A10. Datasets para geração procedural de conteúdo em jogos**
Estruturar conteúdo de jogo (níveis, assets, metadados) em dataset de qualidade controlada + treinar gerador condicionado. — gosto: games; precedente direto na turma 2025 (PCG guiado por prompt).

---

## Conjunto B — âncora ML, satélites de dados e segurança/privacidade

**B1. Fine-tuning eficiente de LLM pequeno para extração jurídica pt-BR**
LoRA/QLoRA em modelo aberto; a curadoria do dado de treino como variável experimental. — ML core; dado como satélite; Ultimatum como base.

**B2. Quanto sintético o treino aguenta?** (espelho de A1)
Misturas sintético/real em proporções controladas; onde o desempenho degrada e por quê. A pergunta vira de *treino*, o dataset vira instrumento. — ML×C1.

**B3. Distilação e quantização de NER pt-BR para produção**
Modelo pequeno rodando em CPU/borda com F1 aceitável; robustez sob drift como critério. — ML core, MLOps-adjacente.

**B4. Robustez adversarial em NLP pt-BR** (segurança)
Ataques textuais gerados por LLM contra classificadores/NER pt-BR; defesas e custo. — ML + segurança; precedente (phishing adversarial, 2025).

**B5. Preference tuning de assistente de domínio** (espelho de A2)
DPO/afins sobre dataset de preferências construído com anotação assistida; avaliar contra baseline. — ML core; dado como satélite.

**B6. Medir o medidor: LLM-as-judge calibrado para pt-BR**
Quando o juiz-LLM concorda com humanos? Calibração, vieses e limites em tarefa específica. — avaliação de modelos (G06 pelo lado do modelo).

**B7. Memorização e membership inference em modelos treinados com dado sensível** (privacidade)
Quanto um modelo treinado no corpus jurídico vaza? Ataques de inferência de pertencimento + mitigações. — ML×C6; espelho da A7.

**B8. Machine unlearning: o direito de ser esquecido** (privacidade)
Remover a contribuição de um titular do modelo sem retreinar do zero (LGPD art. 18); medir custo × esquecimento real. — ML×C6; tema quente e raro.

**B9. Curadoria de dados de voz: fine-tuning de TTS/conversão de voz pt-BR**
Quanto a qualidade/diversidade do dado de áudio importa vs arquitetura, com avaliação objetiva + MOS. — gosto: seus projetos de voz; ML core com dado como variável.

**B10. Treino com privacidade diferencial (DP-SGD) em NLP pt-BR** (privacidade)
O custo em F1 de garantias formais de privacidade num dataset sensível; onde o trade-off compensa. — ML×C6.

---

## Como escolher

1. **Teste da vontade:** qual lista te dá vontade de começar amanhã? Essa é a âncora real.
2. Todos cumprem R1 por construção; todos têm modelo treinado/avaliado no fim.
3. A1, A4 e A7 são os de menor risco (base já existe no Ultimatum); B7/B8 são os de maior originalidade no conjunto B.
4. O tema estacionado original (datasets anotados pt-BR jurídico com anotação assistida) é aproximadamente A2∩A4∩A7 — ele não morreu, se decompôs.
