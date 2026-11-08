# C9 — Processamento de Sinal, Áudio e Multimídia com ML

## 1. O que a área é no dia a dia

Trabalha-se com sinais de áudio (fala, música, sensores) em duas frentes complementares: (a) **modelos generativos** — TTS, voice conversion (VC), singing voice conversion (SVC), síntese de música — que aprendem a produzir ou transformar sinal de áudio; e (b) **mineração/classificação de áudio-vídeo** — extrair features, detectar eventos, classificar locutor/emoção/idioma, ou minerar padrões em coleções multimídia (o ângulo que o ICDATA chama de "multimedia mining"). Na prática o dia a dia envolve: preparar/curar corpora de áudio (limpeza, alinhamento, rotulagem), treinar ou fazer fine-tuning de modelos neurais (encoder-decoder, diffusion, flow-matching), avaliar qualidade com métricas objetivas (MOS preditivo, WER via ASR, similaridade de locutor) porque avaliação humana é cara, e lidar com pipelines que encadeiam vários modelos (extração de features → modelo → vocoder). É uma área com fronteira clara entre pesquisa aplicada (melhorar um modelo) e engenharia de dados (curar/avaliar corpora), sendo esta segunda a mais compatível com o escopo de data science do ICDATA.

## 2. Problemas abertos quentes (2024-2026)

- **Avaliação automática de qualidade de áudio gerado** sem depender de MOS humano caro — VoiceMOS Challenge 2024/2025 e métricas tipo TTSDS2 ainda não generalizam bem para novas arquiteturas.
- **Detecção de deepfake de voz** generaliza mal para ataques "in the wild" e para novos geradores (vozes falsas fora do domínio de treino continuam driblando detectores).
- **Escassez de datasets/benchmarks de VC e SVC** — comparação entre sistemas é inconsistente entre challenges (VCC, SVCC), dificultando replicação.
- **TTS/VC low-resource para línguas como português** — corpora ricos foneticamente ainda são escassos frente a inglês/chinês; abordagens multilíngues e transfer learning tentam compensar.
- **Robustez e viés dos preditores de MOS** — modelos treinados em dados históricos não acompanham saltos de qualidade de novas gerações de sintetizadores (problema de "range-equalizing bias").
- **Ética e proveniência de dados de voz clonada** — rastreabilidade de consentimento em corpora usados para VC/TTS comerciais.

## 3. Surveys de referência (verificados)

- **"Reimagining Speech: A Scoping Review of Deep Learning-Powered Voice Conversion"** (2023, arXiv:2311.08104) — revisão de 123 estudos elegíveis entre 621 triados, cobrindo VC de 2017–2023. https://arxiv.org/abs/2311.08104
- **"Audio Deepfake Detection: What Has Been Achieved and What Lies Ahead"** (2025, ResearchGate) — survey atualizado até 2024/2025, primeiro a analisar privacidade, fairness, adaptabilidade e explicabilidade em detecção de deepfake de áudio. https://www.researchgate.net/publication/390149087_Audio_Deepfake_Detection_What_Has_Been_Achieved_and_What_Lies_Ahead
- **"An Extensive Analysis of the Singing Voice Conversion Challenge 2025 Evaluation Results"** (2025, arXiv:2509.15629) — não é survey clássico, mas consolida o estado da arte em SVC via resultados de challenge recente, útil como referência de benchmark. https://arxiv.org/pdf/2509.15629

Survey clássico anterior (2023) também localizado mas não priorizado por já estar parcialmente superado: **"Audio Deepfake Detection: A Survey"** (Yi, Wang et al., 2023) — https://www.semanticscholar.org/paper/Audio-Deepfake-Detection:-A-Survey-Yi-Wang/79ba04e381b5e6538767d74e599a08e0f048779c

## 4. Onde se publica

- **Venues naturais da área**: ICASSP (IEEE), INTERSPEECH (ISCA), ISMIR (música), IEEE/ACM Transactions on Audio, Speech and Language Processing (TASLP) — todos com peer review rigoroso e foco 100% em áudio/fala, muito mais competitivos e reconhecidos na comunidade de speech do que o CSCE.
- **Entrada via ICDATA/ICAI**: o caminho realista não é "VC/TTS puro", mas sim o ângulo de **mineração/qualidade de dados de áudio** — ex. curadoria de corpus, pipeline de anotação, avaliação de qualidade de dataset de voz, deepfake detection como classificação/mineração — que se encaixa nos tópicos explícitos "Multimedia mining (audio/video)" e "Signal Processing" do ICDATA'26 (confirmado na CfP oficial: https://icdatascience.org/cfp-topics/). Não é o venue nativo da área, mas é aceitável para um primeiro paper de graduação com foco em dados.

## 5. Stack necessária (verificada)

- **Seed-VC** — já usado por Pedro (conversão de voz).
- **torchaudio** — biblioteca oficial PyTorch para processamento de áudio, integra nativamente com pipelines PyTorch.
- **ESPnet** (`pip install espnet espnet-model-zoo`, disponível no PyPI: https://pypi.org/project/espnet/) — toolkit end-to-end para ASR, TTS, VC, tradução de fala, diarização; usa PyTorch e receitas estilo Kaldi.
- Métricas/avaliação: **VoiceMOS Challenge baselines**, **TTSDS2** (arXiv:2506.19441) para avaliação objetiva sem MOS humano.
- Datasets citados na literatura recente para PT-BR: CETUC, TTS-Portuguese, CML-TTS (multilíngue) — mencionados em trabalhos de 2024 sobre corpora fonéticos para português.

## 6. Sinal de mercado

Mercado de voice cloning/AI de voz em forte crescimento: US$ 3,28 bi (2025) → US$ 4,06 bi (2026), CAGR ~24%, projeção de US$ 9,56 bi até 2030 — impulsionado por audiobooks, podcasts, games, assistentes virtuais. Contratação em IA/ML cresceu 88% ano-a-ano em 2025 e 76% dos empregadores relatam dificuldade para preencher vagas de IA; especialistas em "voice engineering" (voice agents, TTS/VC em produção) tendem a ganhar prêmio salarial de 30-50% sobre um ML generalista de mesma senioridade. Sinal favorável, mas datado de fontes de mercado (relatórios comerciais), não de dados de emprego direto no Brasil — tratar com cautela.

## 7. Como seria um tema de residência

1. **Curadoria e avaliação de qualidade de corpus de voice conversion em português** — construir/expandir um dataset PT-BR anotado para VC (aproveitando pipeline Seed-VC já dominado), aplicar métricas objetivas (TTSDS2-like) e comparar com MOS humano reduzido; ângulo de "mineração/qualidade de dados" que casa bem com ICDATA. Exequível com GPU única (Seed-VC já roda em GPU modesta).
2. **Benchmark de detecção de deepfake de voz em português/sotaques brasileiros** — treinar/avaliar um classificador leve sobre amostras geradas pelo próprio pipeline de VC de Pedro + dados públicos, medindo generalização cross-domain (problema identificado como aberto nos surveys de 2024-2025). Encaixa em "Multimedia mining" e tem apelo de segurança/ética.
3. **Estudo comparativo de métricas de avaliação automática de qualidade para SVC/VC de baixo recurso** — replicar parte da metodologia do Singing Voice Conversion Challenge 2025 em um recorte menor (música/fala em português), comparando métricas objetivas vs. avaliação humana reduzida. Mais leve computacionalmente, foco em análise de dados/métricas.

Todas as três aproveitam o portfólio existente (Seed-VC, pipelines de SVC/TTS) e não exigem treinar modelos generativos do zero — o esforço fica em dados, avaliação e experimentação, compatível com GPU única de aluno de graduação.

## 8. Riscos

- **CSCE/ICDATA não é o venue natural da área** — quem realmente acompanha áudio/fala está em ICASSP/INTERSPEECH/ISMIR; um paper aqui tem menos visibilidade dentro da comunidade de speech, mesmo sendo aceitável tematicamente.
- **Custo de GPU**: treinar do zero um TTS/VC competitivo exige recursos que uma GPU única não sustenta bem; a estratégia viável é fine-tuning/avaliação sobre modelos pré-treinados (Seed-VC), não treino do zero.
- **Ética de deepfakes**: qualquer trabalho envolvendo geração ou detecção de voz clonada exige cuidado com consentimento de dados de voz e uso responsável — precisa de justificativa clara de uso ético/defensivo (ex. detecção) para evitar questionamento em revisão por pares.
