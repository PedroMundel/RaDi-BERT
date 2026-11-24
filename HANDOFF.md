# HANDOFF — 24/11/2026, 12:40 (Residência encerrada no gate 10; tudo commitado e enviado; próximo trabalho: transformar a obra num estudo de custo)

## Status

**O gate 10 passou em 19/11.** O Pedro entregou o termo, apresentou e "não apanhou muito". O professor criticou a
**escolha do artigo** (Agrawal: "pouco descritivo, sem código, com baselines quebrados, poucas sementes"). **Ele não
elogiou o método:** isso é inferência do Pedro, dita por ele; não registrar como fala do professor. A nota não saiu;
o Pedro estima 7.

**Rumo decidido pelo Pedro (19/11): "modelar tudo daqui pra frente baseado nesse cerne de custo".** A pergunta do
trabalho passa a ser "essa técnica compensa o custo 7x maior?", com a destilação comum entre BERTs como régua.
**"As experimentações acabaram, só pode fazer pontuais."** Próximo passo anunciado por ele (21/11): "fechar as pontas
do que precisa pra transformar 100% a obra em um estudo de custo"; depois, infográficos, a narrativa do processo e o
README de vitrine. **Nada disso foi desenhado nem começado.**

**Feito nesta sessão (19 a 24/11):**

- **Documento de entrega reescrito como história única** (`entrega/controles-do-decoder-e-destilacao.md`, 9 seções;
  entregue como `Trilha das Semanas 9 e 10.docx`) e **termo da Semana 10 reordenado** na mesma ordem, sem o Resumo
  das Semanas, no formato dos termos finais dos colegas. Narrativa: "o positivo não aparecia, então medi o que o
  artigo não mediu". Uma segunda sessão (a de contexto cheio) acrescentou título, custo e hipótese das justificativas
  e gerou os outros três `.docx`.
- **Explicação do trabalho ao Pedro, assíncrona,** antes da apresentação: arquitetura, fases A/B/C, calendário,
  por que os nulos valem, contribuição, destilação, perguntas prováveis. Está só no chat, não em arquivo.
- **Conferência dos documentos entregues:** cerca de 93 de 100 números batem. **Quatro imprecisões em texto já
  entregue, não corrigidas** (decisão do Pedro: "posso deixar assim mesmo"; corrigir na versão do TCC, com pedido):
  1. "21,8% das palavras são novas" vem da sonda de **63 pares**, não dos 16 mil; e "quase só o rótulo" é mais forte
     que a fonte (os 76,4% são de outro conjunto, de 4.000 pares; sem o grupo de argumentar ainda dá 70,4%). Está em
     Figuras e Evidências (seção 6), na Trilha (seção 9) e no bloco 5 do termo.
  2. Critérios da Semana 10, linha 5: "lado bom conta como ganho"; nos Gaps 7 a 9 lado bom com 5 sementes é só
     **candidato**.
  3. Critérios da Semana 10, linha 13: a regra do Gap 4 aparece como fixada; era "proposta, a confirmar" e o Pedro
     nunca confirmou.
  4. Figuras e Evidências: figura 4 sem dizer que o embaralhado tem 3 sementes; "209 testes em 19/11" vale para as
     07:53; a composição das justificativas do RTE vem da sonda (contagem nas 2.470: novas 16,5%, não 13,5%).
- **Pesos do PC do Marcelo copiados** (13 arquivos, 5,3 GB, SHA-256 igual) para `resultados/<pasta>/amigo/pesos/`.
- **Tudo de 10 a 19/11 commitado e enviado** no `feat/treino-rte`: 16 commits, de `0c72bda` a `7a2544d`; 209 testes
  e lint passando depois do último. **Nenhum PR para `main`.**
- **README com a estrutura atualizada** (módulos do treino, tabela de experimentos, o que fica fora do git). A parte
  de narrativa do README foi adiada por decisão do Pedro.
- **SSD de volta ao PC (Pedro, 21/11):** esta instalação (`WKST-001`) roda agora com a RTX 5060 de 8 GB. Projeto e
  GPU na mesma máquina. A cópia antiga do PC é `E:\RaDi-BERT` (21 pesos em `resultados/*/pesos/`), ferramentas em
  `E:\tools`; o `config/maquina.env` daqui aponta para `C:\Users\Pedro\Documents\Projects\tools`.

**Régua de custo levantada nesta sessão (raciocínio sobre números de cenários diferentes, não limiar medido):**

| Jeito de treinar | Tempo de treino contra o treino comum | Custo antes do treino | Ganho de acurácia |
|---|---|---|---|
| Destilação, respostas do professor | 1,8 vez (76 s contra 43 s) | treinar um BERT base | +1,6 ponto |
| Destilação, sequência | 6,4 vezes (277 s contra 43 s) | o mesmo | +2,5 pontos no total |
| Decoder com justificativa | 7,4 vezes (33 min contra 4,5 min) | 5h20 de LLM para 16 mil pares | -0,9 ponto |

Como ler: cada linha é um jeito de treinar; a segunda coluna compara um treino com o do mesmo modelo sem nada; a
última é a diferença contra esse treino (no decoder, contra o controle de calendário). **As duas primeiras linhas são
BERT small com 4.000 pares (`resultados/rte-pequenos/juntar-esnli-4000.csv`, coluna `seconds`); a terceira é BERT
base com 16 mil pares.** Pôr os dois no mesmo cenário é a experimentação pontual que o Pedro nomeou.

## Decisions

- **Pedro:** a história cobre a replicação inteira (09 a 19/11) e substitui o documento "Controles"; termo "na mesma
  ordem, mas não exatamente enxugado", olhando os termos dos colegas, sem resumo no começo; título do documento
  "Controles que o Artigo Nao Rodou", depois trocado por ele para "Trilha das Semanas 9 e 10"; tema "Destilação de
  Racionalização de LLM para Encoders: controles e limites"; deixar as quatro imprecisões como estão no entregue;
  moldura de custo daqui para frente; commits seguindo o mapa, com as quatro recomendações do Claude (scripts de
  medida ficam em `resultados/`, `brute_test_results.json` ignorado, `AUTONOMIA.md` na raiz, arquivos acima de 2 MB
  fora do git, push sem PR); README de estrutura agora e de narrativa depois.
- **Pedro, sobre o trabalho:** "pra mim é medíocre"; o que pesa é o resultado, não quem escreveu o código ("pra mim
  código n importa"); acha que o trabalho não influencia empregador. A frase dele que virou o cerne: "meu trabalho
  não é 'quero deixar um modelo melhor com RD' e sim 'quero medir se essa técnica compensa o custo 7x maior'".
- **Limite de honestidade combinado:** os critérios escritos antes medem o **benefício** (acurácia); o custo vem dos
  tempos gravados; não escrever que os critérios nasceram da pergunta de custo.
- **Derrubado nesta sessão (no `## Rejected` do `CLAUDE.md`):** dizer que "ninguém mediu" os controles; mover os
  scripts de medida para `scripts/`.
- **Erros do Claude nesta sessão:** registrou "o método ficou bom" como fala do professor (corrigido pelo Pedro);
  supôs que a decepção dele vinha de o código ser de LLM (ele negou).
- **Abertos:** a nota; o desenho do estudo de custo; a pontual do mesmo cenário (decoder x destilação); o que há nos
  scripts que sobraram no PC do Marcelo; organização no HF Hub para os pesos (o Pedro disse que vai criar); regra de
  leitura do Gap 4 (nunca confirmada); PR do `feat/treino-rte` para `main`.

## Files touched

- **Entrega:** `entrega/controles-do-decoder-e-destilacao.md` (reescrito), `entrega/Trilha das Semanas 9 e 10.docx`;
  pela outra sessão: `entrega/figuras-e-evidencias.md`, `entrega/criterios-da-semana-10.md` e os `.docx` deles,
  `entrega/Marcas de Atencao e Destaque v2.docx`.
- **Residência:** `docs/residencia/termo-de-entrega-Semana-10.md` (rascunho; o que o Pedro colou no formulário
  ninguém viu).
- **Repositório:** `README.md`, `.gitignore` (`brute_test_results.json`), `CLAUDE.md` (bloco "19/11, GATE 10 E RUMO
  PÓS-GATE", com o SSD e os commits; `## Rejected`), `docs/handoffs/2026-11-19-0735.md` e `2026-11-19-1140.md`.
- **Fora do git:** `resultados/esnli-treino-16k-calendario-fora-pesos/amigo/pesos/` (5),
  `-embaralhado-fora-pesos/amigo/pesos/` (5), `-fora-pesos-aux-0.5/amigo/pesos/` (3).
- **Commitado em 24/11, a pedido do Pedro ("commita tudo que n ta no repo"):** este `HANDOFF.md`, o `CLAUDE.md`,
  `entrega/Manual do Treino.docx` e `resultados/rte-treino/pc/palavras.csv` (o limite do gancho de arquivos grandes
  subiu de 2 para 3 MB) e os três arquivos de lixo listados abaixo, que agora estão no repositório.
- **Lixo, nada apagado:** `entrega/Controles do Decoder e Destilacao.docx`, `entrega/Controles que o Artigo Nao
  Rodou.docx`, `docs/claude/ledger/2026-11-09-retomada.md.new`; os termos dos colegas em `~/.claude/uploads/`; o
  scratchpad desta sessão (cópia do documento antes da reescrita, scripts avulsos); tudo em `C:\RaDi-BERT` no PC do
  Marcelo; `E:\RaDi-BERT` (cópia antiga, ainda com os 21 pesos, não apagar antes de subir ao HF Hub).

## Next steps

1. **(Pedro: decisão)** Dizer por onde começa o estudo de custo. Ele anunciou "fechar as pontas"; o Claude não
   propõe o rumo, só lista se ele pedir. Insumos prontos: a tabela de custo acima; os tempos em `seconds` de cada
   `resultados.csv`; `entrega/geracao-primeiro-lote.md` (5h20, 1,20 s por par).
2. **(Claude, com pedido)** A pontual do mesmo cenário: decoder e destilação com o mesmo aluno e os mesmos pares.
   Antes de rodar: critério escrito, piso, poder, pesos salvos, fumaça em todos os braços, auditoria de treino,
   `train-watch`. Sempre com o braço `bert_calendar`.
3. **(Claude, com pedido)** Corrigir as quatro imprecisões nos `.md` de entrega para a versão do TCC, gerando `.docx`
   com outro nome, sem tocar nos entregues.
4. **(Claude, quando o PC do Marcelo ligar)** Listar o que sobrou em `C:\RaDi-BERT` e comparar por hash com o
   repositório, para dizer quais scripts são únicos. Até lá ele não apaga os scripts; os pesos pode apagar.
5. **(Pedro)** Criar a organização no HF Hub; depois o Claude sobe os 34 pesos (13 em `resultados/*/amigo/pesos/`,
   21 em `E:\RaDi-BERT\resultados\*\pesos\`).
6. **(Pedro: git)** Decidir o PR do `feat/treino-rte` para `main`; decidir se os três arquivos de lixo saem do
   repositório.
7. **(depois)** Infográficos, narrativa do processo e README de vitrine, nessa ordem que o Pedro deu. Guardar os
   termos entregues das Semanas 9 e 10 em `entrega/termos-entregues/`.

## Resume commands

```bash
cd "C:/Users/Pedro/Documents/Projects/UFG/2026-2/Residencia Bacharelado em Inteligencia Artificial"
git status -sb                                   # feat/treino-rte igual ao remoto; 5 arquivos não rastreados de propósito
uv run --frozen pytest -q                        # 209 passam
uv run --frozen ruff check .
nvidia-smi --query-gpu=name,memory.used --format=csv,noheader     # a 5060 está nesta máquina agora
ssh -o ConnectTimeout=15 amigo hostname          # PC do Marcelo; costuma estar desligado
uv run --frozen python resultados/esnli-treino-16k/ler_fora.py pc amigo
uv run --frozen --with pillow --with python-docx python scripts/screening/scripts/f1/md2docx_plain.py entrega/<fonte>.md "entrega/<Nome>.docx" <pasta-temporaria>
```

- Estado e regras: bloco "19/11, GATE 10 E RUMO PÓS-GATE" do `CLAUDE.md`. Critérios: `docs/2026-11-18-gaps-da-argumentacao.md`.
  Leituras: fim de `resultados/esnli-treino-16k/leitura-grade.md` e `resultados/rte-pequenos/leitura-grade.md`.
- História para explicar o trabalho: `entrega/controles-do-decoder-e-destilacao.md` e `entrega/figuras-e-evidencias.md`.
- Scripts avulsos: do scratchpad, com `python -I`. Comando longo com `\|` ou continuação de linha é barrado pelo
  guardrail do projeto: pôr num arquivo `.sh` no scratchpad e rodar com `bash`.
- Repositório: https://github.com/PedroMundel/RaDi-BERT (privado), ramo `feat/treino-rte`.
