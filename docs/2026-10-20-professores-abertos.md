# Professores de pesos abertos para racionalizações do e-SNLI (20/10/2026)

## Procedência (leia primeiro)

- **Nível 3 inteiro.** Pesquisa feita por agente (páginas lidas por ferramenta de fetch com sumarização). Serve para triagem, **nunca para citação**. Nenhum PDF foi lido por Pedro nem pelo Claude nesta rodada.
- Etiquetas: **[V]** = conferido na fonte (URL ao lado) · **[E]** = estimativa, com a conta · **[M]** = memória/sem fonte aberta · **[N2]** = já registrado em nota nível 2 do projeto · **[N3]** = fonte secundária lida por sumarizador.
- Fontes de artigo: **N3-txt** = texto da seção/tabela lido (HTML do arXiv) · **N3-abs** = só resumo/metadados.
- Nenhum benchmark mede "racionalização curta de NLI". Os números de benchmark abaixo são **proxy** de capacidade geral.

## 1. Tabela comparativa (ONE-TABLE)

Premissas do cálculo [E]: 250 tokens de entrada (~190 de prefixo fixo reaproveitável pelo cache de prompt, ~60 únicos por par), 50 tokens de saída com raciocínio desligado; o gpt-oss-20b não desliga o raciocínio, então assumi +60 tokens (não verificado). RTX 5060: 8 GB GDDR7, barramento 128 bits, **448 GB/s** [V: [guru3d](https://www.guru3d.com/review/geforce-rtx-5060-8gb-review/page-3/) e varejistas; conta 28 Gbps x 128 / 8].

| Candidato (repo HF exato) | Params total/ativo | Quantização e pegada | Vazão na 5060 8 GB: 1 fluxo / agregado em lote | Evidência de qualidade | Licença; treinar com a saída? | Maturidade |
|---|---|---|---|---|---|---|
| **RECOMENDADO: `Qwen/Qwen3.5-9B`** (GGUF: `unsloth/Qwen3.5-9B-GGUF`) | 9B denso / 9B (híbrido DeltaNet) | Q4_K_M **5,68 GB**, tudo na VRAM [V] | ~45 tok/s / ~200 tok/s (8 slots; faixa 150-300) [E] | MMLU-Pro 82,5; IFEval 91,5 [V, cartão; modo não informado] | Apache-2.0 [V]; **sim**, sem cláusula de saída | Lançado mar/2026; GGUF e llama.cpp disponíveis; sem relato de 5060 achado |
| `openai/gpt-oss-20b` (GGUF: `unsloth/gpt-oss-20b-GGUF`) | 21B / 3,6B (MoE) | GGUF Q4_K_M **11,6 GB**, F16 (MXFP4 nativo) 13,8 GB [V]; no relato da 5060: `--n-cpu-moe 18`, ~1,2 GB de VRAM livres [V] | **33-35 tok/s medido em RTX 5060 8 GB + 32 GB DDR5, `--parallel 1`** [V] / ~50-80 (lote 16; conta na §3) [E] | MMLU-Pro 73,6; GPQA 66 (raciocínio médio) [V] | Apache-2.0 [V]; **sim** | ago/2025; o único com medição em 5060 8 GB. Exige formato harmony; raciocínio não desliga |
| `Qwen/Qwen3.6-35B-A3B` (GGUF: `unsloth/Qwen3.6-35B-A3B-GGUF`) | 35B / 3B (MoE, 256 experts, 8 ativos) | UD-IQ4_XS **17,7 GB** ou UD-Q4_K_M **22,1 GB**; experts na RAM [V] | ~25-35 tok/s (anedotas em 8 GB: 25-32 em IQ4_XS, 40+ em IQ3) / ~35-45 [E] | MMLU-Pro 85,2; GPQA 86,0 [V] | Apache-2.0 [V]; **sim** | abr/2026; 22 GB em 32 GB de RAM com Windows é apertado |
| `microsoft/phi-4` | 14B denso / 14B | Q4_K_M ~9 GB [E: 14,7B x 4,85 bits / 8]; ~2-3 GB vazam para a RAM | ~12-16 tok/s / ~40-60 [E] | MMLU 84,8; GPQA 56,1; foco em inglês [V] | MIT [V, campo do cartão]; **sim** | dez/2024; antigo frente aos Qwen 2026 |

**Recomendação: `Qwen/Qwen3.5-9B`** em Q4_K_M, via `llama-server`, com `enable_thinking=false`. É o único que cabe inteiro na VRAM, o único cujo lote escala, e a licença não tem cláusula de saída. Ressalva: é também o menor da tabela em capacidade; só o piloto da §6 diz se a qualidade basta.

**Alternativas verificadas fora da tabela (limite de 4 linhas):**
- `google/gemma-4-26B-A4B-it`: 25,2B / 3,8B ativos, Apache-2.0 no cartão [V], GGUF UD-Q4_K_M 16,9 GB, UD-IQ4_XS 13,6 GB [V]; MMLU-Pro 82,6. Cabe melhor na RAM de 32 GB que o Qwen3.6-35B. Mesma limitação de lote por experts na RAM [E].
- `Qwen/Qwen3-14B` (Apache-2.0 [V], 14,8B): alternativa ao Phi-4, com pensamento ligável por `enable_thinking`.
- `Qwen/Qwen3.6-27B` (Apache-2.0 [V], denso, MMLU-Pro 86,2): não cabe em 8 GB, só em nuvem.
- **Excluídos por licença:** `google/gemma-3-12b-it` (Gemma Terms, ver §2); Llama 3.x (ver §2).

## 2. Licenças: o que a saída permite

| Modelo | Cláusula relevante | Fonte |
|---|---|---|
| Qwen3.5-9B | Apache 2.0 integral, copyright "Alibaba Cloud"; sem restrição de saída (só marcas, §6) [V] | [LICENSE](https://huggingface.co/Qwen/Qwen3.5-9B/blob/main/LICENSE) |
| Qwen3.6-35B-A3B, Qwen3-14B | campo `license: apache-2.0` no cartão [V]; texto da LICENSE não aberto | [cartão](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) |
| gpt-oss-20b | Apache 2.0 [V]. A política de uso do repo só pede "comply with all applicable law"; não menciona treino com saídas [V] | [LICENSE](https://huggingface.co/openai/gpt-oss-20b/blob/main/LICENSE), [USAGE_POLICY](https://huggingface.co/openai/gpt-oss-20b/blob/main/USAGE_POLICY) |
| Gemma 4 | Campo `apache-2.0` nos cartões 26B-A4B e E4B [V]; a página do Google liga "Gemma 4 license" a `/gemma/apache_2` [V]. Resta um link "Prohibited use" (versão de fev/2024) que não menciona treino e **não diz se vale para o Gemma 4** | [terms](https://ai.google.dev/gemma/terms), [apache_2](https://ai.google.dev/gemma/apache_2), [policy](https://ai.google.dev/gemma/prohibited_use_policy) |
| Gemma 3 (termos próprios) | §1.1(e): modelos treinados com dados sintéticos do Gemma são "Model Derivatives" (herdam restrições); "Outputs are not deemed Model Derivatives." [V] | [terms](https://ai.google.dev/gemma/terms) |
| Llama 3.3 | §1.b.i: modelo treinado com as saídas deve ter "Llama" no começo do nome; exibir "Built with Llama" ao distribuir [V] | [LICENSE (raw)](https://raw.githubusercontent.com/meta-llama/llama-models/main/models/llama3_3/LICENSE) |
| Phi-4 | campo `license: MIT` [V]; LICENSE não aberta | [cartão](https://huggingface.co/microsoft/phi-4) |

Leitura: Apache-2.0/MIT não limitam o uso de saídas para treinar outro modelo. É leitura de texto, não parecer jurídico. Gemma 3 e Llama não proíbem, mas impõem condições herdadas (nome, atribuição, termos).

## 3. Tempo de geração (conta explícita) [E]

Requisições x tokens de saída / vazão agregada. Prefill: 60 tokens únicos por par (resto em cache de prefixo) a ~2.000 tok/s para o 9B [E]; sem cache seriam 250 tokens (~4x mais prefill). Prefill dos MoE não foi medido por ninguém que eu tenha achado.

| Candidato | Saída/req | Vazão usada | 100k pares | 550k pares |
|---|---|---|---|---|
| Qwen3.5-9B (lote) | 50 | 200 tok/s | 5,0M / 200 = 25.000 s (6,9 h) + prefill 6M / 2.000 = 3.000 s -> **~7,8 h** | 27,5M / 200 = 137.500 s (38 h) + prefill 16.500 s -> **~43 h (1,8 dia)** |
| Qwen3.5-9B (pior caso, 1 fluxo 45 tok/s) | 50 | 45 | 5,0M / 45 = 111.000 s -> **~31 h** | **~170 h (7 dias)** |
| gpt-oss-20b (lote 16) | ~110 | 70 | 11M / 70 = 157.000 s -> **~44 h** | 60,5M / 70 = 864.000 s -> **~240 h (10 dias)** |
| gpt-oss-20b (1 fluxo medido 34) | ~110 | 34 | 11M / 34 -> **~90 h** | **~494 h (20 dias)** |
| Qwen3.6-35B-A3B (experts na RAM) | 50 | 40 | 5,0M / 40 = 125.000 s -> **~35 h** | 27,5M / 40 = 687.500 s -> **~191 h (8 dias)** |
| Phi-4 (14B, parcial) | 50 | 50 | 5,0M / 50 = 100.000 s -> **~28 h** | 27,5M / 50 = 550.000 s -> **~153 h (6,4 dias)** |

**Por que o lote não ajuda o MoE com experts na RAM [E]:** cada passo de decodificação lê da RAM a união dos experts escolhidos pelos tokens do lote. Fração lida = 1 - (1 - k/n)^B. gpt-oss (4 de 32 por camada): lote 8 lê ~66% dos experts contra 12,5% de 1 token (5,3x os bytes para 8x os tokens = ganho ~1,5x); lote 16 lê ~88% (ganho ~2,3x). Qwen3.6-35B (8 de 256): lote 8 lê ~22% contra 3,1% (ganho ~1,1x); lote 16 ~40% (ganho ~1,2x). O modelo denso lê os pesos uma vez por passo, então o lote escala quase linear até o cálculo limitar.

**Resposta direta à preocupação:** não existe o cenário "1 token por milênio". O pior local aqui é ~12 tok/s (Phi-4 parcial). A troca real é outra: modelo grande com experts na RAM dá 33-35 tok/s numa conversa, mas em volume são 4-10 dias de GPU ligada para 550k. O 9B denso entrega em ~2 dias (~8 h para 100k). O ponto fraco do 9B é a qualidade (§5), não a velocidade.

## 4. Nuvem barata para pesos abertos

**(a) Alugar GPU** (RunPod, preço/hora, [página de preços](https://www.runpod.io/pricing) [V]): RTX 4090 24 GB **US$ 0,34** (comunidade) / **0,89** (segura) · RTX A6000 48 GB 0,33 / 0,59 · L40S 48 GB 0,79 / 1,09 · RTX 5090 32 GB 0,69 / 1,19 · H100 PCIe 80 GB 1,99 / 2,89. Os preços da comunidade vieram de dados estruturados da página, não da tabela visível. Vast.ai: preço dinâmico, sem números (página carrega ao vivo).
Estimativa [E] para Qwen3.5-9B em BF16 (~18 GB) no vLLM, numa 4090 (1.008 GB/s): passo ~25 ms, lote 128 => teto ~5.000 tok/s, uso 2.000. 550k: 27,5M / 2.000 = 3,8 h de decodificação + 1,5-6 h de prefill = **~5-10 h, US$ 2-9** (mais ~1 h de montagem). 100k: ~1-2 h, **US$ 0,4-2**. Numa L40S/A6000 de 48 GB cabe o Qwen3.6-35B-A3B em 8 bits (~36 GB [E]), mesma ordem de custo. O e-SNLI é público, então a nuvem "comunitária" não traz risco de privacidade.

**(b) API hospedada** (preços de lista em 20/10/2026 [V]; saída com raciocínio **desligado**, senão a saída pode multiplicar por 10 ou mais). 550k pares = 137,5M tokens de entrada + 27,5M de saída [E], sem desconto de cache:

| Provedor / modelo | US$/M entrada / saída | 100k | 550k | Fonte |
|---|---|---|---|---|
| DeepInfra `Qwen3.5-9B` | 0,10 / 0,15 | ~3,3 | **~17,9** (13,75 + 4,13) | [pricing](https://deepinfra.com/pricing) |
| DeepInfra `gemma-4-26B-A4B-it` | 0,07 / 0,34 | ~3,5 | ~19,0 (9,63 + 9,35) | idem |
| DeepInfra `Qwen3.6-35B-A3B` | 0,10 / 0,95 | ~7,3 | ~39,9 (13,75 + 26,13) | idem |
| Together `Qwen3.5 9B` | 0,17 / 0,25 | ~5,5 | ~30,3 (23,4 + 6,9) | [pricing](https://www.together.ai/pricing) |

- **Lote:** a documentação da Together diz até 50% de desconto "só para modelos selecionados" e lista apenas `openai/whisper-large-v3` [V](https://docs.together.ai/docs/batch-inference); logo **sem desconto de lote** para esses modelos. A DeepInfra mostra um nível "Flex" a 0,8x, sem confirmar quais modelos [V]. Os totais acima não têm desconto.
- **Termos de uso:** Together §7.2: "you exclusively own all right, title, and interest in Your Content and Output."; sem proibição de treinar com a saída, só §4.3(c) contra produto "competitive with the Company's products"; §2.4 manda cumprir a licença do modelo, que prevalece [V](https://www.together.ai/terms-of-service). DeepInfra §11(a)(i): proíbe uso "competitive with any business of Provider"; nenhuma cláusula contra treinar com a saída e nenhuma de propriedade da saída [V](https://deepinfra.com/terms). Um BERT de NLI não concorre com nenhum dos dois. Leitura por sumarizador (N3).

## 5. Precedentes e qualidade

| Fonte | O que mostra | Nível |
|---|---|---|
| Agrawal, Ahemad & Sembium 2025, COLING Industry ([2025.coling-industry.12](https://aclanthology.org/2025.coling-industry.12)) | Professor **Mixtral 8x7B Instruct** (AWS Bedrock); prompt com o rótulo e "Explain why"; BERT base + decoder T5 [N2: `docs/artigos/notas-agrawal-coling2025.md`, linhas 35-42] | N2 do projeto; o PDF não abriu por fetch |
| Dhaini et al. 2025, [arXiv:2508.09776](https://arxiv.org/abs/2508.09776) | **Mais próximo da sua situação.** e-SNLI (840 pares com explicação humana) + HealthFC; explicadores GPT-4o mini, **Mixtral-7B, Gemma2-9B**, Llama3-70B; **rótulo-ouro no prompt**, temperatura 0, zero/few-shot (4 exemplos; ganho do few-shot "marginal"). Métricas contra a humana: BLEU, ROUGE-1, BERTScore-F1, MAUVE, G-Eval (e-SNLI GPT-4o mini: BERTScore ~0,88, BLEU 0,04-0,05; Tab. 1). BERT/DeBERTa/RoBERTa/ModernBERT treinados com explicação humana vs de LLM: no e-SNLI **as de LLM ficam abaixo** (GPT-4o few-shot ~0,119 de acurácia abaixo; Tab. 2a); no HealthFC é o contrário. A explicação ali é entrada do classificador, não alvo auxiliar: transferência indireta | N3-txt (§3.1-3.3, §4.1-4.3, Tab. 1-3; HTML) |
| [arXiv:2505.22823](https://arxiv.org/html/2505.22823v2) | e-SNLI com Falcon3-7B, Llama3.1-8B, Mistral-7B-v0.3, Qwen2.5-7B (Apêndice B, Tab. 5). ~~Explicações de ~21 palavras (Tab. 9)~~ **corrigido em 21/10: a Tab. 9 mede o tamanho da ENTRADA (contra-instâncias), não da explicação; o paper não dá o tamanho médio da explicação em número (só a Fig. 6). O título é *Self-Critique and Refinement for Faithful Natural Language Explanations*, de Wang & Atanasova, e a explicação é condicionada ao rótulo previsto pelo modelo, não ao ouro;** acurácia do rótulo quando o modelo prevê: Falcon 89,6, Qwen 88,7, **Mistral 58,1, Llama 56,9** (Tab. 7). Infidelidade inicial: Falcon 22,4%, Qwen 42,9%, Llama 59,5%, Mistral 58,9% (Tab. 1). **Não compara com explicações humanas** (Limitações) | N3-txt |
| Wiegreffe et al. 2022, [arXiv:2112.08674](https://arxiv.org/abs/2112.08674) (NAACL) | GPT-3 Davinci (não instruct), 8-24 exemplos; no NLI só **31,5%** das explicações gulosas aceitas por 3/3 anotadores (§3); cabeça a cabeça no e-SNLI: humana preferida 63,6% x GPT-3 24,8% (prompt de crowd, Tab. 3) ou 49,6% x 40,7% (prompt dos autores, Tab. 5); filtro treinado (T0-3B) melhora a seleção (Tab. 8) | N3-txt (lido só até ~100k caracteres) |
| Osnabrück 2024, [arXiv:2409.12599](https://arxiv.org/html/2409.12599v1) | Racionalizações do ChatGPT-3.5-Turbo no **ANLI** (não e-SNLI) para treinar T5-Small: +1,3% e +2,3%; qualidade medida só por BLEU (§3.1, §4.3) | N3-txt |

**O que isso significa, sem eufemismo:** (1) não achei nenhuma avaliação humana de 9B/14B/MoE-3B como gerador de racionalização do e-SNLI com números diretos contra a explicação humana. A mais próxima (Dhaini) testou 7-9B só por métricas de sobreposição. (2) Mesmo GPT-4o e GPT-3 ficam abaixo da explicação humana do e-SNLI; "parecida com a humana" não é o critério alcançável, "aceitável e correta para o rótulo" é. (3) Com rótulo-ouro no prompt a competência de NLI do modelo pesa menos (só justifica), mas o risco é **racionalizar à força** pares de rótulo ruidoso ou duvidoso (neutro/contradição). (4) Nenhuma comparação entre Qwen3.5-9B, gpt-oss-20b, Qwen3.6 e Phi-4 em NLI foi encontrada: o piloto da §6 é insubstituível. (5) Não achei, em busca nenhuma, artigo que use ≤14B aberto como professor de alvo auxiliar de um BERT; isso é ausência nas minhas buscas, não prova.

## 6. Teste barato antes de comprometer (~300 pares)

Sem Claude: nem como gabarito, nem como filtro.

1. **Amostra.** 300 pares do **dev** do e-SNLI, 100 por rótulo, semente fixa, sem sobreposição com os exemplos do prompt. O dev traz **3 explicações humanas por par** [N2: `docs/datasets-nli-verificacao.md`, linha 87]. Os 4-6 exemplos do prompt saem do treino.
2. **Geração.** Mesmo prompt e mesma amostragem (temp 0,3) para cada candidato (Qwen3.5-9B, gpt-oss-20b, Qwen3.6-35B-A3B e, se quiser, Gemma 4 26B-A4B). Via API: 300 x 4 modelos < US$ 0,20 [E]. Local também serve e já mede a vazão.
3. **Vazão real** (decide mais que qualquer tabela deste arquivo): `llama-bench` e `llama-batched-bench` na própria 5060 com 1, 4, 8, 16 slots, e `--n-cpu-moe` varrido nos MoE. Anote tok/s de geração e de prefill.
4. **Checagens automáticas** (só para ordenar; o artigo do e-SNLI avisa que BLEU não serve para explicação): BERTScore-F1 e ROUGE-L contra a melhor das 3 humanas; comprimento (alvo 20-50 palavras); vazamento do rótulo ("entailment", "contradiction"); cópia literal de premissa/hipótese; vazamento de `<think>`/harmony; falhas de formato.
5. **Ida e volta sem rótulo.** Um modelo aberto **diferente do gerador** recebe premissa + hipótese + racionalização (sem o rótulo) e prevê o rótulo. Acerto do rótulo-ouro = quanto a racionalização carrega o rótulo; a explicação humana é o teto. Pares em que a racionalização não recupera o rótulo são candidatos a descarte, e é um filtro sem Claude. Como "juiz" escolha modelo forte em NLI (no 2505.22823, Mistral e Llama erram o rótulo ~42-43% das vezes; Qwen e Falcon, ~11%).
6. **Cego manual (Pedro).** 60 pares (20 por rótulo) x cada candidato + a humana, embaralhados, IDs ocultos. Três perguntas por item, escala 0/1/2: (a) sustenta o rótulo-ouro?; (b) afirma algo que a premissa não diz (alucinação)?; (c) tem 1-2 frases sem revelar o rótulo? ~300 itens x ~20 s = ~1,7 h. "Aceitável" = (a)=2 e (b)=0, formato inspirado na aceitabilidade de Wiegreffe 2022.
7. **Regra de decisão escrita antes de rodar.** Escolher o mais barato em tempo/dinheiro cujo "aceitável" cego chegue a X% (Pedro fixa X; Wiegreffe 2022 só teve 31,5% 3/3 no GPT-3 puro, então X alto exige filtro, ver passo 5). Se nenhum local passar, o próximo passo é API (§4b) com modelo maior (ex.: Gemma 4 31B a US$ 0,39/0,97 por M na Together [V]) antes de repensar o professor.

## 7. Suporte à RTX 5060 (sm_120) no Windows

| Ferramenta | Situação | Fonte |
|---|---|---|
| **llama.cpp** | Binários oficiais para Windows em CUDA 12.4 e **13.4** (release b11769) [V]. CUDA 12.8 foi o primeiro toolkit com alvo sm_120 [N3], então o build 12.4 provavelmente não usa a GPU de forma nativa; **use o 13.4** (driver recente; ~580+ para CUDA 13 [M]) ou compile com `-DCMAKE_CUDA_ARCHITECTURES=120` e toolkit >= 12.8 | [releases](https://github.com/ggml-org/llama.cpp/releases), [NVIDIA fórum](https://forums.developer.nvidia.com/t/software-migration-guide-for-nvidia-blackwell-rtx-gpus-a-guide-to-cuda-12-8-pytorch-tensorrt-and-llama-cpp/321330) |
| **Ollama** | Lista oficial: compute capability **12.0 = RTX 5060**, driver >= 550 [V]; Windows nativo. Não tem `--n-cpu-moe` nem controle de slots como o `llama-server`: prefira `llama-server` | [docs.ollama.com/gpu](https://docs.ollama.com/gpu) |
| **PyTorch estável** | 2.14.1 no PyPI (30/09/2026), Python >= 3.10 [V]. O índice `cu128` tem wheels Windows cp311 só até 2.11.0 [V]; para 2.14 os índices anunciados são cu126/cu130/cu132 e 2.14 é a última linha com CUDA 12.x [N3]. Para sm_120 use **cu130** | [PyPI](https://pypi.org/project/torch/), [índice cu128](https://download.pytorch.org/whl/cu128/torch/), [aviso](https://dev-discuss.pytorch.org/t/notice-cuda-12-6-wheels-will-no-longer-be-published-from-pytorch-2-15-drops-maxwell-pascal-volta/3432) |
| **vLLM** | **Sem Windows nativo** (só WSL2); binários CUDA 12.9 (padrão), 12.8 e 13.0 [V]. A página não menciona sm_120; há relato de RTX 5090 funcionando com torch 2.9.0 cu128 [N3]. Em 8 GB e 32 GB de RAM, o WSL2 não compensa: **vLLM só na GPU alugada (Linux)** | [docs vLLM](https://docs.vllm.ai/en/latest/getting_started/installation/gpu.html), [fórum](https://discuss.vllm.ai/t/vllm-on-rtx5090-working-gpu-setup-with-torch-2-9-0-cu128/1492) |

Comando de partida para o recomendado [E, não testado]: `llama-server -m Qwen3.5-9B-Q4_K_M.gguf -ngl 999 -c 8192 --parallel 8 -fa on --cache-reuse 256 --jinja --chat-template-kwargs '{"enable_thinking":false}'`. O `-c` é dividido entre os slots; 8 slots x ~500 tokens cabem em 8k. Para o gpt-oss: `--n-cpu-moe` entre 16 e 22 conforme o contexto ([guia do llama.cpp](https://github.com/ggml-org/llama.cpp/discussions/15396) [V]); a 5060 do relato usou 18 com 64k de contexto ([hindsight #2525](https://github.com/vectorize-io/hindsight/discussions/2525) [V]).

## 8. Becos sem saída e o que não consegui verificar

- **Sem medição direta** do Qwen3.5-9B na 5060 8 GB. Uma calculadora de terceiros dá ~29,5 tok/s, mas assume 9,4 GB e vazamento de 0,8 GB para a RAM, o que contradiz o arquivo de 5,68 GB [V]. Os ~45 tok/s são conta: 448 GB/s / 5,68 GB = teto de 79 x ~0,6 [E].
- **Vazão em lote** de qualquer candidato local: sem benchmark publicado para 8 slots em placa de 8 GB. Todos os números de lote são [E].
- **Nenhum número de NLI específico** dos quatro modelos. Os 7-9B dos artigos são Qwen2.5-7B, Llama3.1-8B, Mistral-7B, Gemma2-9B, não os candidatos atuais.
- Wiegreffe 2022: li só os primeiros ~100k caracteres do HTML. Agrawal 2025: PDF ilegível por fetch; o Mixtral 8x7B vem da nota N2 do projeto.
- Vast.ai sem preços. Preços do RunPod valem na data da consulta.
- Gemma 4: a página ainda liga uma "Prohibited use policy" de 2024 sem dizer se vale. Antes de escolher, ler a LICENSE do repositório (o caminho `blob/main/LICENSE` deu 404).
- Texto das LICENSEs de Qwen3.6, Qwen3-14B e Phi-4 não aberto (só o campo do cartão).
- O cartão do Qwen3.5-9B não diz em que modo (pensando ou não) foram obtidos os benchmarks.
- Relatos de terceiros sobre `--n-cpu-moe` em 8 GB (Medium deu 403; Reddit via espelho) são anedotas.
- Descartados no caminho: Llama 3.x e Gemma 3 (condições herdadas), `Qwen3.6-27B` (não cabe), Ollama como ferramenta de produção (sem controle de experts).
