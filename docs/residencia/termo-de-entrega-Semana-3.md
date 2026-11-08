# Termo de Aceite de Entrega — Semana 3

- **Data da Reunião ("Gate") de aprovação:** `[preencher]`
- **Participante:** Pedro Mundel — `[matrícula]`

---

**O que fiz nessa terceira Semana:**

Executei a Fase 1 do screening nas bases Semantic Scholar e arXiv. A primeira execução mostrou que
cerca de 94% do retorno era ruído vindo de dois termos meus (`resource-constrained` e `on-device`).
Em vez de apagar esses termos, movi eles para uma string própria (`edge`), para que continuem sendo
buscados sem contaminar a busca principal. A segunda execução devolveu 154 obras, e separei 58 delas
como referência do que é da área **Execucao da Fase 1**;

Terminei a leitura de Petersen et al. (2008) e, com ela e com o retorno da busca na mão, finalizei
os ajustes no método em pontos que eu não tinha como decidir antes de ver dados:

- A população passou a ser surveys sem piso de citação, porque o piso escondia idade: os 8 surveys
  mais citados da referência são todos de 2020-21;
- Ferramentas são buscadas fora de survey, porque a área documenta as ferramentas mas não faz survey
  delas;
- Adotei os termos do professor: fundamentos é o que forma a área hoje, e divisões, vocabulário,
  conceitos, ferramentas e história são as partes dele;
- A leitura para classificar virou uma escada (resumo, depois introdução, depois conclusão), e só
  sobe quando o degrau anterior não basta;
- Defini o que pertence à área survey a survey (treino puro, CNN, GNN e difusão ficam fora;
  infraestrutura de implantação e hardware ficam dentro);
- O screening passou a rodar em voltas, e cada volta termina com uma decisão minha **Ajustes do Metodo**;

A execução final, com o pool corrigido, trouxe 118.659 obras. Escolhi limpar esse volume em camadas,
cada uma com critério declarado antes de rodar e perda medida contra a referência:

- Camada A, campo de estudo: cada obra vem da base com os campos em que foi classificada (Física,
  Medicina, Educação...). Os campos candidatos a sair foram os 17 em que não caiu nenhum survey de
  referência. Sozinho, isso é evidência fraca, porque a referência é pequena e outro survey da área
  poderia estar nesses campos. Por isso o corte teve travas:
  - obra com termo central do meu pool no título nunca sai (salvou 1.142);
  - conferi a olho uma amostra sorteada de 30 excluídas (todas de fora da área);
  - medi a perda na metade de teste (1 de 29);
  - nada foi apagado: obra excluída volta se a bola de neve trouxer ela.

  Medicina, Educação e Matemática ficaram, porque têm surveys da área (sobraram 74.791);
- Camada B, assunto: transformei título e resumo de cada obra num vetor com o SPECTER2, um encoder
  BERT treinado em artigos científicos, e agrupei os vetores parecidos com o BERTopic, que nomeia
  cada grupo pelas palavras típicas dos títulos. Saíram 66 grupos; revisei um a um e marquei os de
  outra área (segurança de IoT, redes 5G, imagem médica...), com a mesma salvaguarda do título
  (sobraram 14.901) **Limpeza em Camadas**;
- Árvore de citação: montei quem cita quem dentro das obras que sobraram. Obra sem nenhuma ligação
  com o bloco onde estão os surveys de referência vai para o fim da fila, exceto as de 2025-26, que
  ainda não tiveram tempo de ser citadas (seguem 11.420, nenhuma apagada);

Separei a referência em duas metades antes de começar: uma para ajustar os critérios e outra só
para testar. Na metade de teste, as três etapas juntas mantiveram 28 de 29 surveys (97%). Fiz isso
porque hoje eu não sei reconhecer sozinho um survey importante da área, então preciso de uma medida
que me diga quando um corte está jogando fora o que eu procuro;

Na árvore de citação, a base principal escondia as referências de 63% das obras. Em vez de aceitar
obras isoladas por falta de dado, juntei uma segunda base (OpenAlex), e obra sem dado de citação não
desce da fila **Arvore de Citacao**;

Desenhei a próxima etapa, de leitura com agentes de LLM, e decidi cada parte dela: amostragem por
grupo com a regra do três (Hanley & Lippman-Hand, 1983), keywording (Petersen et al., 2008) e por
fim leitura completa com a minha decisão sobre cada obra. Separei a leitura em três agentes, um por
tarefa (eliminar o óbvio, transcrever as frases, julgar), para que nenhum deles se perca misturando
tarefas. Nenhum agente elimina obra que não conseguiu acessar: ela entra numa lista que eu reviso ao
fim de cada volta **Desenho da Leitura por Agentes**.

**Planejamento:**

Executar a leitura por agentes para:

- Calibrar os agentes na metade de ajuste da referência antes de usar no conjunto inteiro;
- Chegar à lista de surveys que entram, com a decisão final minha;
- Produzir o registro de screening e a primeira versão do mapa de divisões da área.

---

## Documentos a linkar

| No termo | Arquivo |
|---|---|
| Execucao da Fase 1 | `entrega/Execucao da Fase 1.docx` |
| Ajustes do Metodo | `entrega/Ajustes do Metodo.docx` |
| Limpeza em Camadas | `entrega/Limpeza em Camadas.docx` |
| Arvore de Citacao | `entrega/Arvore de Citacao.docx` (fonte: `entrega/arvore-citacao.md`) |
| Desenho da Leitura por Agentes | `entrega/Desenho da Leitura por Agentes.docx` (fonte: `entrega/desenho-leitura-agentes.md`) |

A página interativa da árvore (https://claude.ai/artifact/NtZpXxsQPWczatLpA9Nbir) serve para mostrar ao
vivo; o link do termo é o .docx.

---

## Escolhas abertas (só o Pedro decide)

1. **"seguem 11.420"** = 11.292 para a F2 + 128 com bilhete. Se preferir, "11.292 seguem, 3.481
   descem".
2. **Uso de LLM em números**, como no gate 2: limpeza, agrupamento e scripts pelo Claude, revisados
   por você.
3. **Hanley & Lippman-Hand (1983)** foi lido só pelo Claude (nível 2) — o docx do desenho declara isso.
