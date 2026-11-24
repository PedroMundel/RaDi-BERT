# Exemplos de RTE para o prompt (caminho A, 09/11)

**O que é:** os 12 exemplos de hoje são do e-SNLI (legendas de foto, conhecimento de mundo). Puxam a explicação por
plausibilidade e não mostram como se prender a um parágrafo sem dizer "The text states". Aqui vão **20 pares do treino
do RTE** (10 por rótulo), fora dos 20 da checada, para substituir os exemplos. **Os 20 saem de qualquer lote**, para o
aluno nunca ver um exemplo como alvo (`cmd_gerar` pula os idx deste arquivo).

**Como o código lê este arquivo** (`rte_examples()` em `src/radibert/rte_racionalizacoes.py`):
- usa a linha **Sua versão** quando ela está preenchida; senão, o **Rascunho do Claude**;
- se algum par estiver marcado `- [x] usar`, usa **só os marcados**; se nenhum estiver, usa os 20;
- intercala os rótulos (implicação, não implicação, ...).

**Regras dos rascunhos** (as mesmas para a sua versão): começar pelo conteúdo, nunca por "The text / The passage /
The sentence"; aberturas todas diferentes entre os 20; implicação = o que no texto garante a hipótese; não implicação =
o que falta ou o que bate de frente, não "é improvável no mundo"; uma frase, ~12–25 palavras, sem nomear o rótulo.

Os 6 primeiros de cada rótulo incluem os 6 da primeira versão (que o Pedro achou bons), sem mudança. **Rascunho do
Claude** = proposta, nível 2.

## 1. entailment · idx 888 · palavra explícita decide

- **P:** The black Muslim activist said that he had relieved Muhammad of his duties "until he demonstrates that he is willing to conform to the manner of representing Allah and the honorable Elijah Muhammad (founder of the Nation of Islam)".
- **H:** Elijah Muhammad founded the Nation of Islam.
- **Rascunho do Claude:** Elijah Muhammad is introduced, in passing, as the founder of the Nation of Islam.
- **Sua versão:**
- [ ] usar

## 2. entailment · idx 1820 · ponte de mundo pequena

- **P:** A Belgian policeman posing as an art dealer in Brussels arrested three Swedes.
- **H:** Three Swedes were arrested in a Belgian police sting operation.
- **Rascunho do Claude:** A policeman posing as an art dealer to catch suspects is running a sting, and he was Belgian.
- **Sua versão:**
- [ ] usar

## 3. entailment · idx 1437 · juntar duas partes da frase

- **P:** In 1869 Sumner resigned his see, but continued to live at the official residence at Farnham until his death on the 15th of August 1874.
- **H:** Sumner died at Farnham.
- **Rascunho do Claude:** Living at Farnham until his death in 1874 places his death at Farnham.
- **Sua versão:**
- [ ] usar

## 4. entailment · idx 1302 · eco quase literal

- **P:** The U.S. space shuttle Atlantis, its lights flashing like a beacon, smoothly docked with Russia's space station Mir Wednesday on its mission to pick up U.S. astronaut Shannon Lucid, who has spent a record-breaking six months in orbit.
- **H:** US shuttle Atlantis docks with the Mir space station.
- **Rascunho do Claude:** Same event with fewer details: Atlantis docked with Russia's space station Mir.
- **Sua versão:**
- [ ] usar

## 5. entailment · idx 927 · paráfrase de duas partes

- **P:** Aziz confirmed that Iraq's demands include "the lifting of the blockade and the restructuring of the espionage commission, including its Chairman, (Richard) Butler.
- **H:** Iraq demands the lifting of the embargo and changes in the committee.
- **Rascunho do Claude:** Lifting the blockade is lifting the embargo, and restructuring the commission and its chairman is changing the committee.
- **Sua versão:**
- [ ] usar

## 6. entailment · idx 1805 · inferir o estado atual por datas

- **P:** Olson, 62, previously worked as a partner at Ernst & Young LLP, as a Minnesota bank president and as a congressional aide, before joining the Fed board in 2001, to serve a term ending in 2010.
- **H:** Olson is a member of the Fed board.
- **Rascunho do Claude:** Olson joined the Fed board in 2001 for a term running to 2010, which makes him a member.
- **Sua versão:**
- [ ] usar

## 7. entailment · idx 729 · cargo implica vínculo

- **P:** "The capacity people have to adjust and make peace with a new situation, even if they feel vulnerable, is really remarkable," said Randy Quevillon, chair of the psychology department and the Disaster Mental Health Institute at the University of South Dakota.
- **H:** Randy Quevillon is employed at the University of South Dakota.
- **Rascunho do Claude:** As chair of the university's psychology department, Quevillon works for the University of South Dakota.
- **Sua versão:**
- [ ] usar

## 8. entailment · idx 239 · sinônimo (factory = plant)

- **P:** Up to 150 workers were believed to have been inside the factory, which produces syringes and other plastic medical supplies, at the time of the explosion.
- **H:** Workers were inside the plant at the time of the explosion.
- **Rascunho do Claude:** A factory making syringes is a plant, and up to 150 workers were in it when it exploded.
- **Sua versão:**
- [ ] usar

## 9. entailment · idx 56 · ponte de mundo com a mesma modalidade (may)

- **P:** Startling new research into mobile phones claims they may reduce a man's sperm count by up to 30%.
- **H:** Male fertility may be affected by use of a mobile phones.
- **Rascunho do Claude:** Phones that may cut a man's sperm count by up to 30% may affect his fertility.
- **Sua versão:**
- [ ] usar

## 10. entailment · idx 1855 · ligar nome e obra numa lista

- **P:** Even Homer realises the cleverness of Jan De Bont's tautly-directed action. Laser Movies , Speed , Widescreen with Keanu Reeves, Dennis Hopper, Sandra Bullock.
- **H:** The movie 'Speed' was directed by Jan De Bont.
- **Rascunho do Claude:** The tautly-directed action credited to Jan De Bont is the film listed right after it, Speed.
- **Sua versão:**
- [ ] usar

## 11. not_entailment · idx 788 · armadilha da plausibilidade

- **P:** State Police issued bulletins via teletype requesting patrols to be on the lookout for Robert Senacal, 35, of Cortlandt Manor.
- **H:** Robert Senacal was arrested by police.
- **Rascunho do Claude:** Patrols were only asked to look out for Senacal; an arrest is never reported.
- **Sua versão:**
- [ ] usar

## 12. not_entailment · idx 707 · números trocados

- **P:** Nine soldiers and two police officers were killed in the ensuing gun battle, and two police officers were wounded, the officials said.
- **H:** Six policemen and two soldiers were killed in a gunbattle, officials said.
- **Rascunho do Claude:** Nine soldiers and two police officers died, so the counts of soldiers and police are swapped and wrong.
- **Sua versão:**
- [ ] usar

## 13. not_entailment · idx 1616 · papel trocado

- **P:** Most of the life of Petko Kiryakov was not unveiled by historians but by the prominent Bulgarian writer Nikolai Haitov, who wrote a novel and a script which was turned into a TV series, which became a favourite of most Bulgarians.
- **H:** Nikolai Haitov is a historian.
- **Rascunho do Claude:** Haitov is set apart from the historians: he is the writer of a novel and a script.
- **Sua versão:**
- [ ] usar

## 14. not_entailment · idx 1681 · parentesco trocado

- **P:** A Muslim charity in the Philippines that was supported by bin Laden and run by a brother-in-law, Mohammad Jamal Khalifa, financed Shah and the other plotters.
- **H:** Mohammad Khalifa's father-in-law is Osama Bin Laden.
- **Rascunho do Claude:** Khalifa is bin Laden's brother-in-law, a different tie from bin Laden being his father-in-law.
- **Sua versão:**
- [ ] usar

## 15. not_entailment · idx 1005 · data e pessoa erradas

- **P:** The documents commented by the magazine date of April 25, 2002, epoch in which the Brazilian president was Fernando Henrique Cardoso.
- **H:** The Brazilian President is Luiz Inácio Lula da Silva.
- **Rascunho do Claude:** Cardoso was president in April 2002, the date of the documents; Lula is never mentioned.
- **Sua versão:**
- [ ] usar

## 16. not_entailment · idx 2013 · atributo preso à pessoa errada

- **P:** Although they were born on different planets, Oscar-winning actor Nicolas Cage's new son and Superman have something in common - both were named Kal-el.
- **H:** Nicolas Cage's new son was awarded an Oscar.
- **Rascunho do Claude:** Cage, the father, is the Oscar winner; his newborn son only shares the name Kal-el with Superman.
- **Sua versão:**
- [ ] usar

## 17. not_entailment · idx 1427 · aviso não é fato

- **P:** Critics said the National Certificate of Educational Achievement or NCEA, the main qualification for high school students, would be degraded by the authority allowing text-speak use in exams.
- **H:** The NCEA has been degraded by the authority.
- **Rascunho do Claude:** Critics only warned that text-speak would degrade the NCEA; whether it has been degraded is not established.
- **Sua versão:**
- [ ] usar

## 18. not_entailment · idx 632 · o texto diz que não se sabe

- **P:** Actual statistics about the deterrent value of capital punishment are not available because it is impossible to know who may have been deterred from committing a crime.
- **H:** Capital punishment is a deterrent to crime.
- **Rascunho do Claude:** Deterrence statistics are unavailable, so whether capital punishment deters crime is left open.
- **Sua versão:**
- [ ] usar

## 19. not_entailment · idx 1947 · preparo não é anúncio

- **P:** Gladys Lauture, a close Aristide friend and longtime supporter, said she and a team of carpenters, plumbers and decorators spent 18 days making Aristide's Port-au-Prince home livable again.
- **H:** Aristide is due to live at Port-au-Prince again.
- **Rascunho do Claude:** Making Aristide's home livable again prepares it, but his return to live there is never announced.
- **Sua versão:**
- [ ] usar

## 20. not_entailment · idx 2261 · acima da média não é o mais alto

- **P:** Immediately after 1990, however, Swedish fertility plummeted in another unique movement, and had fallen to 1.5 children per woman in 1998 and in 1999. This is the lowest birth rate in Sweden ever-although above the European average.
- **H:** Sweden is the European country with the highest birth rate.
- **Rascunho do Claude:** Sweden's 1998 rate was its lowest ever and only above the European average, not the highest in Europe.
- **Sua versão:**
- [ ] usar
