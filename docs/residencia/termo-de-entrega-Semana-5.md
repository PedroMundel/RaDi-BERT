# Termo de Aceite de Entrega — Semana 5

- **Data da Reunião ("Gate") de aprovação:** `[preencher]`
- **Participante:** Pedro Mundel — `[matrícula]`

---

**Resumo das Semanas 1 a 4:**

Na primeira semana defini o tema, destilação de racionalização de LLM para encoders, a partir de leituras que me
mostraram que a racionalização de um LLM pode treinar um modelo menor só durante o treino, sem ser usada na hora de
responder, e que uma cabeça auxiliar descartada na entrega leva isso a um classificador BERT. Na segunda, defini o
método de screening da área em que quero me especializar, eficiência de modelos para implantação. Na terceira,
executei a busca, limpei em camadas as 118.659 obras que ela devolveu e li sobre mapeamento e revisão sistemática,
de onde tirei que dá para organizar uma área em categorias sem julgar cada estudo, desde que os critérios sejam
decididos antes de rodar. Na quarta, usei 91 surveys como júri para chegar a uma lista de 56 obras, montei o meu
método de leitura e li sobre a história da destilação, sobre como as fases da inferência afetam o hardware e as
ferramentas para cada tipo de gargalo, e sobre como a gestão do KV cache afeta um sistema de serving.

**O que fiz nessa quinta Semana:**

- Reduzi a lista de 56 para 39 obras, tirando 17 superadas ou fora do foco, porque quero me apoiar em métodos e
  ferramentas atuais;
- Li o DistilBERT (Sanh et al., 2019) e anotei o que ele levanta para o meu trabalho: a loss de destilação responde
  por grande parte do ganho, e eu vou destilar racionalização, não conhecimento. A leitura virou uma lista do que
  preciso estudar: surveys recentes, tipos de loss e boas práticas de treino de BERT;
- Levantei com apoio de LLM os surveys recentes de destilação de LLM e escolhi a taxonomia de Fang et al. (2025) como
  mapa, porque preciso de poucos surveys, e recentes;
- Separei a destilação tradicional da destilação de racionalização, porque elas transferem coisas diferentes: a
  primeira, como o professor distribui a confiança entre as respostas, inclusive as erradas; a segunda, como ele
  justifica a resposta certa. Isso muda que loss e que professor fazem sentido para um encoder;
- Pedi fonte para cada afirmação do LLM nessa comparação e descartei as que não tinham, porque vou tomar decisões
  com base nela;
- Li quatro obras porque precisava entender por que a racionalização ajuda **Leituras Semana 5**:
  - Wadhwa et al. (2024): o aluno não precisa raciocinar na hora de responder. A racionalização depois do rótulo
    funciona melhor, a gramática não importa, e manter só os tokens importantes mantém o ganho;
  - Chen et al. (2025): responder antes de racionalizar faz a racionalização amplificar o erro e concentrar o
    aprendizado nas amostras difíceis. Para perguntas muito complexas, racionalizar antes ainda é melhor;
  - Feng et al. (2024): os tokens de uma racionalização não têm a mesma importância, e um módulo aprende pesos para
    o aluno imitar com precisão os tokens-chave;
  - Wang et al. (2025): um framework de destilação de LLM, com síntese de dados, ajuste supervisionado, otimização de
    ranking e aprendizado por reforço.

  Concluí que o ganho não vem de o aluno raciocinar na hora de responder, e sim de tokens específicos ligados ao
  rótulo. Que sinal exatamente é transferido ainda está em aberto;
- Registrei essas leituras junto com as das semanas anteriores **Obras Lidas v4**.

**Planejamento:**

Entender que sinal a racionalização transfere para:

- Escolher as losses que vou testar no encoder;
- Definir como treinar o encoder aluno, a partir de boas práticas recentes.

---

## Documentos a linkar

| No termo | Arquivo |
|---|---|
| Leituras Semana 5 | `Downloads/Leituras Semana 5.docx` (seu documento; mover para `entrega/` se quiser manter junto) |
| Obras Lidas v4 | `entrega/Obras Lidas v4.docx` (fonte: `entrega/obras-lidas-v4.md`) |

---

## Escolhas abertas (só o Pedro decide)

1. **Fang et al. (2025):** o item diz que você escolheu a taxonomia como mapa. Se você não leu a figura com atenção,
   troque "escolhi como mapa" por "separei para ler", e ela não entra no Obras Lidas.
2. **O item do DistilBERT** não tem documento linkado. Se quiser, o seu `DistillBert (1).docx` pode entrar como
   link.
3. **"Pedi fonte para cada afirmação do LLM"**: mostra processo e uso de LLM declarado. Tire se achar que expõe
   demais.
4. **Três pontos no seu Leituras Semana 5** que valem conferir antes de entregar (ver a conversa).
5. **Ano do Chen:** usei 2025, como no seu documento. O arXiv é de 2024 e o paper está em *early access* na IEEE
   TNNLS; troque se preferir.
6. **Agrawal no Obras Lidas v4:** usei a linha que você entregou na v3a, sem a parte "é o mecanismo que eu queria
   levar para um encoder...".
