# Notas — Wohlin (EASE 2014)

**Título:** *Guidelines for Snowballing in Systematic Literature Studies and a Replication in Software
Engineering*
**Venue:** Proceedings of the 18th International Conference on Evaluation and Assessment in Software
Engineering (EASE '14), Londres, maio 2014. ACM, DOI 10.1145/2601248.2601268. 8 páginas.
**Autor:** Claes Wohlin, Blekinge Institute of Technology, Suécia.
**PDF:** `docs/artigos/wohlin-2014-ease.pdf` (baixado de `wohlin.eu/ease14.pdf`, site do autor, 19/09/2026).

## PROCEDÊNCIA

**Nível 4 — Claude leu o texto completo em 19/09/2026 (todas as 8 páginas, via `pdftotext`). Pedro NÃO
leu.** Serve para conferir a tabela §1 de `docs/metodo-de-construcao-do-metodo.md` e para orientar a
Fase 2B. **Nada daqui entra em texto assinado pelo Pedro sem leitura dele.**

---

## Veredito de uma linha

O paper é o procedimento de snowballing em passos (start set → iterações backward/forward → parada
quando uma iteração não traz paper novo → contato com autores), validado por replicação de uma RSL
publicada. **Confirma a linha P4 da tabela §1** — mas o que ele chama de *start set* não é "os
surveys" e o que ele chama de parada não é saturação de categoria; ver "O que não licencia".

## O que o paper propõe (§3, transcrito em resumo fiel)

**3.1 Start set.** Primeiro desafio do snowballing, equivalente ao de formular a string na busca por
base. Recomenda Google Scholar para evitar viés de editora. Características de um bom start set:
- cobre as **comunidades** diferentes que podem publicar sobre o assunto — crucial se houver *clusters
  independentes* (papers que não se citam entre si);
- **tamanho proporcional à largura da área** — área estreita, poucos papers; área larga, mais;
- se a busca devolve papers demais, **selecionar alguns relevantes e muito citados** é uma alternativa;
- **diversidade** de editoras, anos e autores;
- formulado a partir das **palavras-chave da pergunta de pesquisa, com sinônimos**, para não capturar só
  uma terminologia.
- "Não há bala de prata"; uma possibilidade é partir de **um paper seminal e muito citado** da área.
  Identificar bom start set é declarado **problema em aberto** (§3.1 e §5).

**3.2 Iterações.** Só entra na iteração o paper **já decidido como incluído após leitura do texto
completo** — se um paper usado para snowballing for excluído depois, tudo que veio dele tem de ser
revertido (*rollback*). Uma iteração por vez, para rastreabilidade.
- **Backward (3.2.1):** varrer a lista de referências. Ordem de exame: (1) excluir por critérios
  básicos (língua, ano, tipo de publicação); (2) remover as já examinadas; (3) para as restantes,
  **título → venue → autores**; (4) se ainda candidata, ver **onde e como o paper a cita** (lugar e
  contexto da referência); (5) só então buscar o paper e ler o resumo, depois partes, até decidir.
  "Não ler do início ao fim; folhear as partes relevantes."
- **Forward (3.2.2):** quem cita o paper incluído, via Google Scholar. Primeira triagem pela
  informação do Scholar; depois resumo; depois o trecho que cita; depois texto completo.
- **3.2.3:** o loop termina quando **backward e forward não trazem paper novo**.

**3.3 Autores.** Após o loop, contatar os autores mais ativos; se surgir paper novo, reiniciar. Também:
buscar nos venues onde os incluídos foram publicados.

**3.4 Extração.** Como os incluídos já foram lidos por inteiro para decidir inclusão, a extração pode
ser feita no mesmo momento.

## O que a replicação mostrou (§4)

Replica MacDonell et al. 2010 (RSL sobre modelos de estimativa cross-company vs. within-company,
1995–2005). Números: 13 candidatos no start set tentativo → **3 incluídos** (todos com um autor em
comum — o próprio Wohlin diz que "está longe de perfeito"). Iteração 1: 25 referências examinadas,
**7 incluídos** por backward, **0** por forward. Iteração 2: 97 referências + 126 citações, **1**
incluído (por forward). Iteração 3: 33 candidatos, 0. Total **11 papers**, os mesmos das duas RSLs
originais (9 em comum com ambas; o 11º era o que a RSL original diz que deveria ter sido excluído).
Eficiência (§4.6): backward muito mais produtivo que forward neste caso; 10 dos 11 vieram por
backward. Papers lidos em detalhe: 38, mesmo esforço das duas RSLs por base (24 e 38). A matriz de
citação (Tabela 1) mostra que **achar qualquer um dos 11 leva aos outros 10** — "não importa qual".

## Dez lições (§4.9.1, resumidas)

1. Exclusão direta na lista de referências por língua/ano/tipo é quase de graça.
2. Muitas referências repetem entre papers, sobretudo dos mesmos autores — ou a área foi capturada, ou
   é **um cluster** e outros existem. Volta ao start set.
3. Decidir *em que nível* excluir (título, resumo, texto) é o equilíbrio difícil; excluir cedo demais é
   o risco maior.
4. Backward: quando um paper entra, olhar os **outros citados de modo parecido** no mesmo trecho.
5. Forward: idem para o paper que levou ao novo.
6. A ordem de exame muda quantos candidatos cada paper gera; o total por passo deve ser estável.
7. **Rastrear a frequência de novos por passo**; com bom start set, deve cair a cada iteração.
8. Se **não cair**, buscar de novo com **sinônimos** — sinal de cluster perdido.
9. **Matriz de citação**: muitas células vazias indicam papers perdidos (não detecta cluster
   independente).
10. Linha do tempo ajuda a ler a matriz.

## O que licencia no método de screening (Pedro decide; isto é leitura do Claude)

- **§4 do método (seminal = citado em comum pelos surveys)** é backward snowballing a partir de um
  start set de surveys, com contagem. O paper licencia o backward e a ideia de que referências
  repetidas indicam captura da área (lição 2) — a **contagem/limiar "2 de 3"** é adição nossa, não
  está no Wohlin.
- **Cláusula de inclusão forçada (§4, "muito citado")**: o Wohlin cita "paper seminal e muito citado"
  como forma legítima de *compor o start set*, e "selecionar relevantes e muito citados" como
  alternativa quando a busca devolve demais. Cobre a cláusula.
- **Diversidade do start set** (comunidades, editoras, anos, autores) é o critério dele para a
  cobertura — apoia a exigência de ≥ 3 surveys (§5 do método) e sugere um check que o método não
  tem: os 3 surveys **não podem ser do mesmo grupo/venue**.
- **Lições 7–8** são um teste de parada operacional que o método pode adotar sem custo: registrar
  quantas divisões/seminais novos cada survey trouxe; se não cair, trocar termos (o pool tem
  sinônimos para isso).
- **Ordem título → venue → autores → contexto da citação** é o nível 3 do método com um passo a mais
  (o contexto da citação), útil para o agente extrator.

## O que NÃO licencia

- **Parada.** A regra de parada do Wohlin é *"uma iteração não trouxe paper novo"* — exaustividade por
  fechamento do grafo de citações, não saturação de categoria. O método §5 usa saturação (nenhuma
  divisão/seminal/fundamento **novo**), que é conceito do Glaser & Strauss 1967, não deste paper. Não
  citar o Wohlin para a parada.
- **Objetivo.** O Wohlin escreve para RSL (todos os papers relevantes de uma pergunta estreita); o
  screening quer mapa de área. A lição 2 e a matriz de citação assumem população fechada — em área
  larga com clusters independentes, o próprio paper avisa que a matriz não ajuda.
- **Google Scholar** é a ferramenta dele para forward; o método usa Semantic Scholar. Não há
  comparação no paper.
- O paper **não define** "seminal"; usa "seminal and highly cited" sem critério.

## Conferência da tabela §1 (`docs/metodo-de-construcao-do-metodo.md`)

Linha **P4** — "Wohlin 2014, *backward snowballing* a partir de um *start set*; a interseção de
referências entre surveys é snowballing com voto": **confere** na primeira metade (termos e conceito
existem no paper como descrito). A segunda metade ("com voto") é interpretação nossa, não do paper —
na tabela está correto porque a frase separa o que é dele do que é nosso, mas se for para a
Fundamentação, dizer que o limiar de votos é decisão do método.
