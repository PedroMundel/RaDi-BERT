# Quanto da racionalização humana do e-SNLI já está no input? (Semana 6, 13/10/2026)

**Pergunta:** quanto de uma racionalização humana do e-SNLI já está escrito na premissa e na hipótese?

**Dados:** `dados/esnli/esnli_dev.csv`: 9.842 pares (3.329 implicações, 3.278 contradições, 3.235 neutros), 3
explicações por par, nenhuma vazia, nenhum par sem rótulo.

## Leitura à mão (2.3), anotações do Pedro

Leitura de 15 pares sorteados (`random_state=1`).

- "Achei boas explicações, mas algumas de implicação parecem cometer a falácia de petição de princípio."

### Humano × LLM (piloto de 13/10), observação do Pedro

Sobre o par *"A dirt bike rider riding through the woods over logs" → "The dirt bike rider is riding a dirt bike"*:

- Humano: *A rider riding through the woods must be riding a dirt bike.*
- Sonnet: *a dirt bike rider is by definition someone riding a dirt bike. So the hypothesis restates what the premise
  already implies and must be true...*

> "A segunda está bem mais correta. [...] Se a gente retirar essa frase do contexto, ela perde o significado, pode ser
> horse rider, mountain bike rider, dirt motorbike rider, etc. Já a segunda não, ela se sustenta mesmo retirando do
> contexto. 'a dirt bike rider is by definition someone riding a dirt bike' é petitio principii? Sim. Mas o meu ponto
> não é esse no momento."

## Achado

- **Uma em cada três justificativas humanas do e-SNLI não acrescenta nenhuma palavra ao par** (30,6% de 29.521).
  Em média, 76,5% das palavras de uma justificativa humana já estão na premissa ou na hipótese, e a mediana de
  palavras novas é **1**. A maior cópia aparece na implicação (85%), onde o Pedro tinha visto petição de princípio.
- **As de LLM quase nunca são cópia pura** (Haiku 0,1%, Sonnet 0,3%). Copiam 42–49% e trazem 6–8 palavras novas.
- **Mas as palavras novas do LLM são de relação, não de conhecimento:** "incompatible", "details", "restates",
  "directly", "necessarily". O LLM explicita a relação entre as frases, e os humanos fazem isso pouco.
- **Copiar menos não é ser melhor:** o Sonnet copia mais que o Haiku (49% × 42%) e venceu a avaliação manual por 14
  a 3. A medida de cópia não substitui o julgamento de qualidade. Ela mede outra coisa.
- **A cópia é real, não acaso de vocabulário:** contra o par de outro exemplo sorteado, a "cópia" cai para 2–3,5%.

Números completos: `copia-numeros.md` (gerado por `copia.py`).

## Decisões de medida (2.4)

- Palavra = letras minúsculas; sem stopwords do sklearn, sem tokens de 1 letra, sem pedaços de contração
  ("doesn", "isn").
- Palavras de "metalinguagem" (premise, hypothesis, true, guarantee, implies, scene, describes...) retiradas das
  explicações, para o vocabulário de roteiro do LLM não contar como informação nova.
- Sem lematização (hug ≠ hugging), o que subestima a cópia.
- Conjunto de palavras, sem contar repetição.
- Entrada = premissa + hipótese; medida extra só contra a hipótese (pela observação de petição de princípio).
- Controle: o mesmo cálculo contra o par de outro exemplo, sorteado (semente 0).
- Código escrito pelo Claude a pedido do Pedro (14/10).

## Cortes de leitura (2.8)

Nenhum corte foi fixado antes de rodar. Os números são descritivos. O único ponto natural usado é **100%** (a
explicação não acrescenta nenhuma palavra de conteúdo).

## Limitações

- Só a validação; cópia lexical, não de sentido.
- A lista de metalinguagem foi escolhida à mão e muda os números dos LLMs.
- As palavras novas não distinguem conhecimento de mundo ("mural = parede pintada") de retórica ("incompatible").
- As justificativas de LLM foram geradas com o rótulo no prompt.
