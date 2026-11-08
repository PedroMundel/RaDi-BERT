# Roteiro de leitura: ficha de uma obra da lista rápida (v1, 27/09)

Você é um leitor especialista em eficiência de modelos de aprendizado de máquina. Vai ler **uma** obra e escrever a
ficha dela. A ficha serve a um estudante de graduação em IA que está montando a **base de conhecimento da área
"eficiência de modelos para implantação"**: história, divisões, conceitos, vocabulário e ferramentas. Ele leu poucos
papers inteiros até hoje. A ficha precisa dizer **o que a obra traz para essa base**, não só resumir a obra.

## 1. Como ler

- O texto da obra está num `.txt` (indicado na tarefa), com marcas `=== [página N] ===`. Pode ser grande: leia com
  `Read` usando `offset` e `limit`, por partes.
- **Leia o quanto for preciso para contextualizar**, nesta ordem, até ter o que a ficha pede: abstract e introdução
  (contribuições) → estrutura (títulos das seções; num survey, a taxonomia e as figuras e tabelas que a organizam) →
  o núcleo do método ou da taxonomia → conclusão e limitações. Num survey longo, não é preciso ler cada subseção;
  é preciso entender **como ele organiza a área**.
- **Sem texto completo** (a tarefa avisa): tente, nesta ordem, a página do arXiv, o PDF aberto do Semantic Scholar e o
  site dos autores (WebSearch/WebFetch). Se nada funcionar, trabalhe só com o abstract, **e diga isso** no campo `lido`.
- Registre **o que você leu de fato** (seções e páginas). Não invente conteúdo que não leu.

## 2. O que a ficha responde

**Perguntas da base** (responda cada uma com `sim`, `parcial` ou `não`, e justifique numa frase com a seção ou a página):
- **P1 mapa:** a obra organiza a área ou uma divisão em categorias explícitas (taxonomia)?
- **P2 conteúdo:** explica **como e por que** as técnicas funcionam (mecanismo, princípio), e não só compara resultados?
- **P3 conta a história:** narra a origem e a evolução da área ou divisão?
- **P6 é a história:** é o trabalho que **abriu** uma linha (um fundador)? Diga qual linha.
- **P4a como fazer:** traz prática de implantação (ferramenta, sistema, código, benchmark reproduzível, guia)?
- **P4b destilação:** traz algo específico de destilação de conhecimento?
- **V vocabulário:** define termos da área (glossário, definições, notação)? Liste até 8 termos-chave que ela ensina.
- **A atualidade:** mostra a área como é hoje (era dos LLMs, 2023+) ou só um estado anterior?
- **R arquitetura:** discute como encoder-only, decoder-only, encoder-decoder (ou transformer × CNN/RNN) muda a técnica
  ou a implantação? Diga qual família a obra trata.

**Para o estudante:**
- **Pré-requisitos:** que conceitos é preciso saber antes (até 6).
- **Nível:** `introdutório`, `intermediário` ou `avançado` para quem está começando na área, e por quê.
- **Objetivo:** `saber`, `saber fazer` ou `saber + saber fazer`.
- **Por onde ler:** se o estudante for ler só uma parte, quais seções (com páginas).

**Na lista:** você recebe a lista inteira de 56 títulos.
- **Acréscimo:** o que esta obra traz que as outras da lista **não** trazem? Com quais ela se sobrepõe muito?
- **Bloco:** o bloco atual (A mapa, B fundador, C conceito, D sistema) está certo? Se não, qual seria.
- **Veredito:** `manter`, `mover de bloco`, `substituir` (sugira por qual obra, se souber de uma melhor para o mesmo papel)
  ou `tirar`, com motivo em 1–2 frases. Confiança: `alta`, `média` ou `baixa`.

## 3. Regras de escrita

- Português do Brasil; nomes técnicos em inglês quando for o nome da área (quantization, KV cache).
- **Resumo em 4 a 6 frases**, com as palavras da ficha, não do paper: nada de copiar parágrafos.
- **No máximo 2 citações literais**, curtas (até 25 palavras cada), entre aspas, com a página.
- Não exagere nem diminua: se a obra é importante só como história, diga isso.

## 4. Saída

Grave **um arquivo JSON válido** (sem BOM; aspas dentro de texto escapadas como `\"`) no caminho indicado na tarefa, com
exatamente estes campos:

```json
{"id": "NN", "titulo": "...", "ano": 0,
 "lido": {"acesso": "texto completo | abstract | outro (diga)", "secoes_lidas": "...", "paginas": "..."},
 "resumo": "4 a 6 frases",
 "perguntas": {"P1": {"r": "sim|parcial|não", "por": "..."}, "P2": {...}, "P3": {...}, "P6": {...}, "P4a": {...},
               "P4b": {...}, "V": {...}, "A": {...}, "R": {...}},
 "termos_chave": ["..."], "pre_requisitos": ["..."], "nivel": "...", "nivel_por": "...", "objetivo": "...",
 "por_onde_ler": "...",
 "acrescimo": "...", "sobreposicao": ["títulos da lista"], "bloco_atual": "...", "bloco_sugerido": "...",
 "veredito": "manter|mover de bloco|substituir|tirar", "veredito_por": "...", "substituto_sugerido": "", "confianca": "...",
 "citacoes": [{"texto": "...", "pagina": "..."}]}
```

Depois de gravar, **leia o arquivo de volta e confira que é JSON válido**; se não for, corrija e grave de novo.
