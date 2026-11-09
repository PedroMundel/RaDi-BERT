# RTE: FP2 x FP3, 20 pares do treino (Qwen3.6-35B-A3B)

Para a checada rápida da D1. Ordem = treino embaralhado com semente 42. Nada aqui foi lido ainda.

## 1. idx 1057 · entailment

- **Premissa:** In 2003, Yunus brought the microcredit revolution to the streets of Bangladesh to support more than 50,000 beggars, whom the Grameen Bank respectfully calls Struggling Members.
- **Hipótese:** Yunus supported more than 50,000 Struggling Members.
- **FP2:** The beggars are respectfully called Struggling Members, so supporting more than 50,000 beggars means supporting that many Struggling Members.
- **FP3:** Yunus supported beggars whom Grameen Bank calls Struggling Members, so supporting those beggars means he supported more than 50,000 Struggling Members.

## 2. idx 478 · not_entailment

- **Premissa:** India's steelmaker Tata Steel, of the Tata Group, buys Anglo-Dutch steel giant Corus Group for £6.7 billion ($12 billion), making it the world's fifth largest steel manufacturer. 70-year-old Tata group Chairman Ratan Tata, from one of India's best-known business families, won the race against Benjamin Steinbruch, 52, a famous Brazilian executive who is the chief and main owner of Companhia Siderurgica Nacional (CSN). Tata paid investors 608 pence a share, whereas the Brazilians final offer in an auction by the U.K.'s Takeover Panel was 603 pence. The deal triples Tata Steel's capacity to almost 28 million tons a year. Tata: "This is the first step in showing that Indian industry can step outside its shores into an international market place as a global player." Corus, which was created from the merger of British Steel and Hoogovens, currently employs 47,300 people worldwide. Last year the company was the ninth-largest steel maker worldwide. The takeover may start a round of consolidation in the fragmented steel sector.
- **Hipótese:** Tata group was founded 70 years ago.
- **FP2:** The text states Ratan Tata is 70 years old, not the company, so his age does not determine the group's founding date.
- **FP3:** Ratan Tata’s age is 70, not the group's founding date, so his age does not determine when the company was established.

## 3. idx 976 · entailment

- **Premissa:** Late Tuesday, authorities in the U.S. state of Texas carried out the execution of José Medellín, a Mexican national convicted of raping and murdering two teenage girls in 1993. The execution was carried out despite being at the center of an international legal dispute with objections from the International Court of Justice (ICJ) and UN Secretary-General Ban Ki-moon. José Ernesto Medellín, 33, was born in Mexico but moved to the U.S. as a child. He was sentenced to death for the 1993 rape and murder of two girls aged 14 and 16 in Houston, Texas. On Tuesday at 9:57 p.m. CDT, he was given a lethal injection at the Huntsville Unit in Huntsville, according to the Texas Department of Criminal Justice.
- **Hipótese:** José Medellín was executed in Huntsville prison.
- **FP2:** The text states he was given a lethal injection at the Huntsville Unit, and execution implies death by lethal injection occurs at the prison where this procedure takes place.
- **FP3:** The text states he was given a lethal injection at the Huntsville Unit, which is a prison in Huntsville.

## 4. idx 422 · not_entailment

- **Premissa:** Prosecutors were still expected to unseal an 11-count manslaughter indictment against the ferry's captain, Michael Gansas.
- **Hipótese:** Gansas' attorneys have said that rule was not communicated to ferry staff.
- **FP2:** The passage mentions the indictment but provides no information about Gansas' attorneys' statements regarding communication rules to ferry staff.
- **FP3:** The indictment details charges against Gansas but provides no information about statements made by his attorneys regarding communication rules to ferry staff.

## 5. idx 1399 · entailment

- **Premissa:** According to tradition, they founded Tenochtitlan ( "Place of the High Priest Tenoch" ) after much wandering when they saw on an island in Lake Texcoco the sign that their god Huitzilopochtli had indicated -- an eagle perched on a cactus, eating a serpent .
- **Hipótese:** They saw an eagle perched on a cactus eating a serpent.
- **FP2:** The text explicitly states they saw the sign their god indicated, which was defined as an eagle perched on a cactus eating a serpent.
- **FP3:** The text states they saw the sign their god indicated, which is explicitly described as an eagle perched on a cactus eating a serpent.

## 6. idx 1447 · entailment

- **Premissa:** iTunes software has seen strong sales in Europe.
- **Hipótese:** Strong sales for iTunes in Europe.
- **FP2:** Strong sales for iTunes in Europe is a direct rephrasing of the phrase "iTunes software has seen strong sales in Europe," confirming the statement.
- **FP3:** The premise explicitly states that iTunes software has seen strong sales in Europe, so this confirms the statement about strong sales in that region.

## 7. idx 2329 · not_entailment

- **Premissa:** Two portraits, one by Reynolds, the other by Gainsborough, since 1990 among the most looked-after works in the Art Loss Register database, were recovered this week when they were brought into Sotheby's for evaluation. Also a lithograph by Norwegian artist Edvard Munch, stolen from an Oslo art gallery in April, has been recovered, news reports said today.
- **Hipótese:** These two portraits and a lithography by Edvard Munch were recovered using the Art Loss Register database.
- **FP2:** The text states the portraits were in the database and later recovered, but does not specify that the database was used as the method for their recovery.
- **FP3:** The text says they were in the database, not that the database was used to find them.

## 8. idx 1937 · entailment

- **Premissa:** Rose made his first start since joining the Knicks 10 games ago, replacing Thomas, who has an infected elbow.
- **Hipótese:** Rose joined the Knicks 10 games ago.
- **FP2:** The phrase "since joining" establishes a starting point for his tenure, directly implying he became a member of the Knicks ten games prior to this event.
- **FP3:** The phrase "since joining" indicates the starting point of his absence, which directly implies he joined the team ten games prior to this event.

## 9. idx 2064 · entailment

- **Premissa:** With its headquarters in Madrid, Spain, WTO is an inter-governmental body entrusted by the United Nations to promote and develop tourism.
- **Hipótese:** The WTO headquarters is located in Madrid, Spain.
- **FP2:** The text explicitly states the WTO has its headquarters in Madrid, Spain, so this location is a direct fact provided by the passage.
- **FP3:** The premise explicitly states the WTO's headquarters are in Madrid, which directly confirms its location there.

## 10. idx 2476 · not_entailment

- **Premissa:** In the United States Senate on Tuesday, Senators Byron Dorgan, a Democrat from North Dakota, and Mike Enzi, a Republican from Wyoming, introduced the "Freedom to Travel to Cuba Act" (S.428), a bill that would lift the travel restrictions that have prevented U.S. citizens from visiting Cuba since the early 1960s. The bill is co-sponsored by 20 senators, and the House of Representatives is considering a companion measure, H.R. 874, introduced by Representatives Bill Delahunt and Jeff Flake. The house measure has 121 cosponsors.
- **Hipótese:** Byron Dorgan was born in Wyoming.
- **FP2:** Dorgan is identified as a Democrat from North Dakota, while Enzi is the Republican from Wyoming, indicating they represent different states, not necessarily that Dorgan was born in Wyoming.
- **FP3:** Byron Dorgan is identified as a Democrat from North Dakota, while Mike Enzi is the Republican from Wyoming.

## 11. idx 2020 · not_entailment

- **Premissa:** BEA Arthur seemed the very definition of a tough showbiz broad. Tall, astringent, imperious -- she looked like someone who didn't suffer fools and could cut them down with a withering look or a well-aimed barb, delivered in that famous contralto. And it was, for the most part, all an act, says her close friend of more than 40 years, Angela Lansbury. "Bea was absolutely the antithesis of the characters she portrayed," Lansbury says. "She was sensitive -- really, really sensitive -- and self-conscious. But she covered it up by becoming this deep-voiced comic.
- **Hipótese:** Angela Lansbury is an actress.
- **FP2:** The text states Angela Lansbury is a close friend, not that she is an actress, so her profession is unspecified in the passage.
- **FP3:** The text states Angela Lansbury is a close friend, not her profession; being a friend does not necessarily mean she is an actress.

## 12. idx 654 · entailment

- **Premissa:** On Wednesday night people in the Bahçelievler district of Yenibosna in Istanbul, Turkey, claimed that they had seen a UFO flying in the sky, the Turkish newspaper Sabah reports. They said that the UFO was glowing with white lights and that it revolved around itself. Istanbul has had previous UFO incidents in the past, and in 2002, the Istanbul UFO Museum was opened to the public.
- **Hipótese:** A UFO might have been seen in Turkey.
- **FP2:** Istanbul is a city in Turkey, and since people there claimed to see a UFO, it means a UFO might have been seen in Turkey.
- **FP3:** People reported seeing a UFO in Istanbul, which is located in Turkey, meaning a UFO was potentially sighted within the country.

## 13. idx 509 · not_entailment

- **Premissa:** The marriage is planned to take place in the Kiev Monastery of the Caves, whose father superior, Bishop Pavel, is Yulia Timoshenko's spiritual father.
- **Hipótese:** Yulia Timoshenko is the daughter of Bishop Pavel.
- **FP2:** Spiritual father refers to a religious mentor, not a biological parent, so Yulia Timoshenko is not necessarily Bishop Pavel's daughter.
- **FP3:** Spiritual father refers to a religious mentor, not a biological parent, so Yulia Timoshenko is not necessarily Bishop Pavel's daughter.

## 14. idx 410 · entailment

- **Premissa:** From 1016 to 1030 the Normans were pure mercenaries, serving either Byzantines or Lombards, and then Sergius of Naples, by installing their leader Rainulf in the fortress of Aversa in 1030, gave them their first pied-à-terre and they began an organized conquest of the land.
- **Hipótese:** Rainulf was the leader of the Normans.
- **FP2:** The text explicitly states that Sergius installed "their leader Rainulf," using the possessive pronoun "their" to refer back to the Normans, thereby identifying him as their leader.
- **FP3:** Installing their leader Rainulf implies he held that specific role, as one cannot install a person in a position they do not already occupy.

## 15. idx 1862 · not_entailment

- **Premissa:** The dual citizenship debate has been a major distraction for the Weah campaign and many of his opponents have been secretly advocating against his presence in the race.
- **Hipótese:** Weah does business with his opponents.
- **FP2:** The text mentions a political debate and campaign opposition, but provides no information about any business relationship between Weah and his opponents.
- **FP3:** The text mentions a political debate and campaign distractions, but provides no information about any business relationship between Weah and his opponents.

## 16. idx 252 · entailment

- **Premissa:** "On Feb. 20, Dr. Hunter S. Thompson took his life with a gunshot to the head at his fortified compound in Woody Creek, Colorado. The family will shortly provide more information about memorial service and media contacts. Hunter prized his privacy and we ask that his friends and admirers respect that privacy as well as that of his family," Juan Thompson said in a statement issued to Aspen Daily News. The death was confirmed by Pitkin County Sheriff Bob Braudis. Hunter S. Thompson was best known for his 1972 book "Fear and Loathing in Las Vegas". He was recently married and had emotionally supported his friend John Kerry's candidacy.
- **Hipótese:** John Kerry was friends with Hunter S. Thompson.
- **FP2:** The text states Thompson emotionally supported Kerry’s candidacy, implying a personal connection that aligns with them being friends.
- **FP3:** Hunter emotionally supported John Kerry's candidacy, and such personal political backing implies a close friendship between them.

## 17. idx 450 · entailment

- **Premissa:** Mercedes-Benz is another German luxury-car manufacturer, but its M-Class sport-utility vehicle is assembled in Alabama and the new G-Class is from Austria.
- **Hipótese:** Mercedes-Benz is a German car manufacturer.
- **FP2:** The text explicitly calls Mercedes-Benz a German luxury-car manufacturer in the first clause, establishing its origin directly.
- **FP3:** The text explicitly states that Mercedes-Benz is a German luxury-car manufacturer, establishing its origin directly in the premise.

## 18. idx 1646 · not_entailment

- **Premissa:** English has been written using the Latin alphabet since around the ninth century. (Before that, Old English had been written using the Anglo-Saxon Futhorc.) The spelling system or orthography of English is historical, not phonological.
- **Hipótese:** A spelling reform was approved in all German speaking countries.
- **FP2:** The passage discusses English orthography and history, not German-speaking countries or spelling reforms, so it provides no information about those topics.
- **FP3:** The text discusses English orthography and history, providing no information regarding spelling reforms in German-speaking countries.

## 19. idx 1498 · not_entailment

- **Premissa:** In 1997, Tyson bit off part of one of Evander Holyfield's ears in their rematch that led to Tyson's disqualification and suspension. In 2002, at a melee at a news conference in New York, Tyson bit champion Lennox Lewis' leg.
- **Hipótese:** Tyson bit off part of one of Evander Holyfield's ears in 2002.
- **FP2:** The text specifies the ear-biting occurred in 1997 and the leg-biting in 2002, making these distinct events separated by time rather than a single repeated action.
- **FP3:** Tyson bit Holyfield's ear in 1997 and Lewis' leg in 2002, so the events are distinct occurrences in different years.

## 20. idx 1316 · not_entailment

- **Premissa:** SCI, Houston's largest funeral services company, was headed by Robert Waltrip--a close associate of the Bush family.
- **Hipótese:** Robert Waltrip works for the Bush family.
- **FP2:** Being a close associate implies a personal relationship, not necessarily an employer-employee dynamic, as associates can be independent partners or advisors.
- **FP3:** Being a close associate implies a personal relationship, not necessarily employment; he leads the funeral company, which is distinct from working for the Bush family.
