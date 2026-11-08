# Roteiro do agente 2: extração (v2, 26/09)

**Mudança da v1:** na calibração, 6% das frases saíram alteradas (sigla expandida, trechos colados, lista
editada). A v2 proíbe isso de forma explícita, e um script confere cada frase contra o texto original.

**Tarefa única:** transcrever, **palavra por palavra**, as frases do título e do abstract que dizem do que a
obra trata. **Você não julga.** Não diga se a obra é boa, relevante ou da área. Não resuma nem parafraseie.

## Transcreva (até 6 frases por obra, cópia exata do texto, no idioma original)

1. **O objeto:** a frase que diz do que a obra trata (ex.: "This paper surveys ...", "We review ...", "We propose ...").
2. **O tipo:** a frase que mostra se a obra revisa literatura (survey, review, overview, taxonomy) ou propõe
   método, sistema ou experimento próprio.
3. **Os modelos:** a frase que diz sobre quais modelos a obra trata (ex.: LLMs, transformers, CNNs, GNNs,
   modelos de difusão), se houver.
4. **A técnica ou o problema:** a frase que diz qual técnica ou problema é coberto (ex.: quantização, poda,
   destilação, serving, borda, fine-tuning, treino).
5. **Sinais práticos:** a frase que menciona código, ferramenta, biblioteca, benchmark, tutorial, guia,
   estudo de caso ou lições práticas, se houver.

## Cópia exata: o que é proibido

- **Expandir ou trocar sigla.** Se o texto diz "KD plays a crucial role", copie "KD plays a crucial role", não
  "Knowledge Distillation (KD) plays…".
- **Colar trechos.** Cada frase é um trecho **contínuo** do texto. Se precisar de dois trechos, faça duas frases.
- **Editar listas, conjugar ou corrigir.** Não tire itens, não troque "provide" por "provides", não corrija erro
  do autor.
- **Começar ou terminar no meio de uma palavra.** Pode começar no meio da frase do autor, desde que o trecho
  seja contínuo e idêntico.

Um script compara cada frase com o título e o abstract. A frase que não bater é marcada `não verbatim` e
aparece na auditoria.

Se o título já diz algo que o abstract não diz, transcreva o título como uma das frases, marcado `[título]`.
Se nenhuma frase cobre um item, não invente: deixe o item de fora.

## Obra sem abstract

Se o campo `acesso` for `sem acesso`, devolva `frases: []` e `acesso: "sem acesso"`.

## Saída

Grave um arquivo JSON (uma lista) no caminho indicado na tarefa, um objeto por obra:

```json
{"id": "C01", "acesso": "ok", "frases": [{"item": "objeto" | "tipo" | "modelos" | "tecnica" | "pratica", "texto": "cópia exata"}]}
```

Não escreva mais nada no arquivo. Todas as obras recebidas precisam aparecer na saída.
