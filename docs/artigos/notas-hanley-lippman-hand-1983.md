# Notas — Hanley & Lippman-Hand (1983), "If Nothing Goes Wrong, Is Everything All Right? Interpreting Zero Numerators"

*JAMA* 249(13):1743–1745. DOI 10.1001/jama.1983.03330370053031.

**Procedência: nível 2 — Claude leu o texto completo (23/09/2026).** Fonte lida: transcrição do artigo
hospedada na página de curso do primeiro autor (`jhanley.biostat.mcgill.ca/c607/ch08/zero_numerator.pdf`,
4 páginas) — não é o PDF diagramado do JAMA (paywall). Pedro não leu: **não citável em texto assinado
por ele** sem a leitura dele. Motivo da leitura: decidir a fase F2 do desenho dos agentes
(`docs/screening/fase1/2026-09-23-desenho-agentes.md`).

## O que o artigo diz

- **A regra:** se nenhum de *n* casos mostra o evento, pode-se dizer com 95% de confiança que a chance
  do evento é **no máximo ~3/n**. É o limite superior do intervalo de confiança de 95% de uma taxa 0/n.
- **Derivação:** resolver (1 − risco máximo)^n = 0,05; para n >= 30, 0,05^(1/n) ≈ 1 − 3/n, porque
  ln 0,05 ≈ −3. Pela Poisson, exp(−n × risco) = 0,05 dá o mesmo 3/n.
- **Precisão:** para n > 30, a regra bate com o cálculo exato até o ponto percentual; abaixo de 30,
  superestima um pouco (0/10: exato 26%, regra 30%).
- **Outras confianças:** 99% -> "regra de 4,6"; 99,9% -> "regra de 6,9".
- **Tabela 2 (o que 0/n exclui, 95%):** 0/10 -> 26% · 0/20 -> 14% · **0/30 -> 10%** · 0/50 -> 6% ·
  0/100 -> 3% · 0/1.000 -> 0,3%.
- **Uso em triagem, citado pelos autores:** a "regra das 14 falhas consecutivas" em pesquisa de câncer,
  para **descartar** agentes que provavelmente não mostram atividade em pelo menos 1 de cada 5
  pacientes (3/14 ≈ 21%). É o mesmo formato de decisão da nossa F2.
- **Mensagem central:** zero no numerador **não quer dizer risco zero**; quer dizer um intervalo de
  0 até ~3/n.

## O que o artigo NÃO diz (importa para a F2)

- **Não trata de população finita nem do tamanho da população.** O modelo é o de uma **taxa de longo
  prazo** (cada caso com a mesma chance, independente — binomial/Poisson). A única ressalva é
  "confinar as inferências às populações de onde os pacientes vêm".
- Consequência para nós (raciocínio do Claude, não do artigo): num grupo finito amostrado **sem
  reposição**, o limite binomial é **conservador** (o limite real é um pouco menor), então "< 3/n do
  grupo" continua valendo. Mas o que ele limita é a **proporção**; o **número** de cajuzeiros que
  pode sobrar é essa proporção vezes o tamanho do grupo.
- **Não trata de erro na detecção do evento.** Nos exemplos, "ter o evento" é observado sem erro. Na
  nossa F2 o "evento" é o agente marcar a obra como relevante — se o agente deixa passar um cajuzeiro,
  o zero é falso. A validação (M4) mede isso.
- A amostra precisa representar o grupo; nos exemplos isso é suposto. Para nós: **sorteio aleatório**.
