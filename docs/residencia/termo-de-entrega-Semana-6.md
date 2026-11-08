# Termo de Aceite de Entrega — Semana 6

- **Data da Reunião ("Gate") de aprovação:** `[preencher]`
- **Participante:** Pedro Mundel — `[matrícula]`

---

**Resumo das Semanas 1 a 5:**

Na primeira semana defini o tema, destilação de racionalização de LLM para encoders, a partir de leituras que me
mostraram que a racionalização de um LLM pode treinar um modelo menor só durante o treino, sem ser usada na hora de
responder, e que uma cabeça auxiliar descartada na entrega leva isso a um classificador BERT. Na segunda, defini o
método de screening da área em que quero me especializar, eficiência de modelos para implantação. Na terceira,
executei a busca, limpei em camadas as 118.659 obras que ela devolveu e li sobre mapeamento e revisão sistemática,
de onde tirei que dá para organizar uma área em categorias sem julgar cada estudo, desde que os critérios sejam
decididos antes de rodar. Na quarta, cheguei a uma lista de 56 obras, montei o meu método de leitura e li sobre
destilação, gargalos de inferência e serving. Na quinta, fiquei só com as obras atuais e entendi que o ganho da
racionalização vem de tokens ligados ao rótulo, não de o aluno raciocinar ao responder.

**O que fiz nessa sexta Semana:**

- Fixei a definição de racionalização que uso no trabalho: a justificativa, em texto, de por que a resposta é
  aquela. No meu caso, ela é escrita por um LLM e usada só no treino. Fiz isso porque é o conceito central do tema
  e precisa ficar separado do CoT, que gera a justificativa na hora de responder;
- Escolhi a tarefa: inferência textual com 3 classes no e-SNLI, porque ele já tem justificativa humana, inclui
  contradição e exige um passo de inferência que a justificativa pode ensinar;
- Descobri que gerar justificativa de LLM é barato: gerei 2.000 com Claude Haiku e Claude Sonnet por US$ 0,64, e
  o conjunto de treino inteiro sairia por cerca de US$ 19, o que cabe no meu orçamento;
- Encontrei inconsistências nas justificativas humanas do e-SNLI: comparadas às de LLM, as humanas foram pobres em
  um terço dos casos, e as do Sonnet foram as mais corretas e as que mais se sustentam fora do contexto. Isso
  permite comparar o treino com justificativa humana e com justificativa de LLM;
- Medi quanto da justificativa já está escrito no par: uma em cada três justificativas humanas não acrescenta
  nenhuma palavra à premissa e à hipótese, enquanto as de LLM quase sempre acrescentam. Isso dá uma primeira pista
  do sinal que a justificativa transfere;
- Conferi os termos de uso da Anthropic antes de usar as justificativas para treinar: a restrição é treinar modelo
  concorrente, e o meu aluno é um classificador que não gera texto;
- O código da geração e da medida foi feito com apoio de LLM. Os critérios de qualidade e a avaliação das
  justificativas são meus **Racionalizacoes Humanas x LLM**.

**Planejamento:**

Montar o treino do encoder aluno para:

- Comparar o treino com justificativa humana e com justificativa de LLM;
- Escolher as losses e como a cabeça auxiliar recebe a justificativa;
- Medir quanto custa treinar com menos dados.

---

## Documentos a linkar

| No termo | Arquivo |
|---|---|
| Racionalizacoes Humanas x LLM | `entrega/Racionalizacoes Humanas x LLM.docx` (fonte: `entrega/racionalizacoes-humanas-x-llm.md`) |

---

## Escolhas abertas (só o Pedro decide)

1. **O documento linkado.** Ele ainda não existe. Gero o .docx a partir dos três arquivos acima? Ou você prefere
   escrever o seu, como no Leituras Semana 5?
2. **"Uma primeira pista do sinal que a justificativa transfere."** A leitura de que as palavras novas do LLM são de
   relação ("incompatible", "restates"), e não de conhecimento, foi minha. Se não for sua, corte a frase depois do
   número.
3. **Vazamento do rótulo no prompt.** As justificativas de LLM repetem as definições de rótulo que estavam no prompt.
   A observação foi minha e ficou fora do termo. Entra se você concordar e souber explicar.
4. **Wiegreffe e Gurrapu.** Não entraram como lidos. Se você ler antes do gate, cabe uma linha: "li X para apoiar a
   definição".
5. **"Pobres em um terço dos casos"** = 7 de 20 pares. Na arguição, o tamanho da amostra é a primeira pergunta
   provável: os 20 pares são o "olhei de perto" e a medida de cópia, em 29.521 justificativas, é o "vale para o
   conjunto".
6. **Função do encoder como verificador** (checar se uma afirmação decorre de um texto) ficou de fora, porque não
   está conferida na fonte.
