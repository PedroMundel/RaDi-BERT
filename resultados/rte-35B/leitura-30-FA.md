# Leitura de 30 pares do lote FA (15 por rótulo, semente 2026)

Sorteio de `analise_lote_fa.py`. Texto = justificativa depois da limpeza C. Leitura do Claude em `analise-lote-FA.md`.

## 1. idx 2375 · entailment

- **P:** The Israeli army forces carried out, on Saturday, a widespread military operation into the West Bank town of Jenin and its refugee camp, local Palestinian sources said.
- **H:** The Israeli army carried out a widespread operation in Jenin.
- **FA:** Israeli army forces carried out a widespread military operation into Jenin, confirming the event occurred.

## 2. idx 1067 · entailment

- **P:** Medieval Christians said the rosary as Catholics still do today: by praying five decades of Ave Marias (Hail Marys), each introduced by a Pater Noster (Our Father), while meditating on three series of five mysteries each.
- **H:** Christians pray the rosary.
- **FA:** Christians said the rosary by praying Ave Marias and Pater Nosters, which constitutes the act of praying the rosary.

## 3. idx 1286 · not_entailment

- **P:** After trial, Family Court found defendant guilty of willfully violating the order of protection and sentenced him to six months incarceration.
- **H:** Family Court cannot punish the guilty.
- **FA:** The court sentenced him to incarceration, which is a punishment, proving it can punish the guilty.

## 4. idx 2302 · not_entailment

- **P:** Seal hunting has been a tradition in Norway for thousands of years, but has dwindled recently with only about half the annual 1,200 quota being killed each year.
- **H:** Seal-hunting endangers species.
- **FA:** The text notes a decline in hunting numbers but never claims this reduction threatens seal species with endangerment.

## 5. idx 1517 · not_entailment

- **P:** Earlier this year reporter Judith Miller was jailed for refusing to name the US-government source who identified a member of the US Central Intelligence Agency (CIA), Valerie Plame.
- **H:** Judith Miller works for the US Government.
- **FA:** Miller was a reporter who refused to name her US-government source; being a source's contact does not make her an employee of the government she investigated.

## 6. idx 2384 · entailment

- **P:** Bowles will take the title HRH Duchess of Cornwall, changing it to the Princess Consort, when Charles becomes King.
- **H:** Bowles will be known as HRH Duchess of Cornwall.
- **FA:** Bowles will take the title HRH Duchess of Cornwall when Charles becomes King, establishing her future status as Duchess of Cornwall.

## 7. idx 1743 · entailment

- **P:** Parviz Davudi was representing Iran at a meeting of the Shanghai Co-operation Organisation (SCO), the fledgling association that binds Russia, China and four former Soviet republics of central Asia together to fight terrorism.
- **H:** China is a member of SCO.
- **FA:** China is listed among the countries bound together by the SCO to fight terrorism, indicating its membership in the association.

## 8. idx 2193 · entailment

- **P:** Nicholas Cage's wife, Alice Kim Cage, gave birth Monday, to Kal-el Coppola Cage, in New York City, said the actor's Los Angeles-based publicist, Annett Wolf.
- **H:** Kal-el Coppola Cage is the son of Nicholas Cage.
- **FA:** Alice Kim Cage is Nicholas Cage's wife and gave birth to Kal-el, implying he is their son.

## 9. idx 989 · not_entailment

- **P:** Worldwide, child labor is most prevalent in the agricultural sector, where children are widely used as day laborers. Working long hours, children working in agriculture are often exposed to harmful pesticides, dangerous machinery, backbreaking loads, and many other hazardous conditions.
- **H:** Child labor is widely used in Asia.
- **FA:** The text discusses child labor globally without specifying Asia, so its prevalence there remains unconfirmed by the provided information.

## 10. idx 120 · entailment

- **P:** The Kinston Indians are a minor league baseball team in Kinston, North Carolina. The team, a Class A affiliate of the Cleveland Indians, plays in the Carolina League.
- **H:** Kinston Indians participate in the Carolina League.
- **FA:** The team plays in the Carolina League, which means they participate in it.

## 11. idx 1975 · not_entailment

- **P:** Victor Emmanuel III yielded most of his powers to his son Umberto II in 1944, when Umberto was appointed as Lieutenant General of the Realm, and finally abdicated in 1946.
- **H:** Victor Emmanuel III was king of Italy from 1900 to 1946.
- **FA:** The text states he abdicated in 1946 but does not mention when he became king, so his start date remains unknown.

## 12. idx 1125 · not_entailment

- **P:** Geoscience Australia said the 5.3 quake did not generate a tsunami. The 2004 Indian Ocean earthquake, which had a magnitude of 9.0, triggered a series of lethal tsunamis on December 26, 2004 that killed over 270,000 people, making it the deadliest tsunami in recorded history.
- **H:** A tsunami is a series of waves created when a body of water rapidly displaced on a massive scale.
- **FA:** The text reports on specific tsunami events but does not define what a tsunami is, so the definition cannot be inferred from the passage.

## 13. idx 1247 · not_entailment

- **P:** Mr. Balasingham will return to his London home and then move on to Sri Lanka in early October to consult with LTTE leader Vilupillai Prabhakaran, diplomats said.
- **H:** Vilupillai Prabhakaran is a diplomat.
- **FA:** Diplomats reported the plan, but Prabhakaran is identified as an LTTE leader, not a diplomat.

## 14. idx 202 · entailment

- **P:** The organizing committee said 65 countries have entered the Lillehammer Olympic Games, matching the number of nations at the 1992 Winter Games in Albertville, France.
- **H:** 65 countries take part in the Lillehammer Olympic Games.
- **FA:** The organizing committee stated that 65 countries entered the Games, which indicates their participation in the event.

## 15. idx 2335 · not_entailment

- **P:** Canada and the United States signed an agreement on January 30, 1979, to amend the treaty to allow subsistence hunting of waterfowl.
- **H:** The Israel-Egypt Peace Agreement was signed in 1979.
- **FA:** The text concerns a Canada-US agreement on waterfowl hunting; it mentions no Israel-Egypt Peace Agreement, leaving its signing date unaddressed.

## 16. idx 437 · not_entailment

- **P:** Two Belgian soldiers, part of the UN peacekeeping force in Lebanon, were wounded Friday after stepping on a cluster bomb during a mine-clearing operation in southern Lebanon. One of the two soldiers stepped on a cluster bomb while clearing a minefield near the village of Majdel Silim. Their injuries were "serious but not life-threatening", a UNIFIL spokesman said, however this was denied by the cabinet of the Belgian Minister of Defence, André Flahaut. One soldier was wounded at the neck, the second was wounded at the foot.
- **H:** UNIFIL is affiliated with the Belgian Minister of Defence.
- **FA:** A UNIFIL spokesman reported the injuries, but the Belgian Defense Minister denied them; these are separate entities with no stated affiliation.

## 17. idx 1292 · entailment

- **P:** Italian director Federico Fellini was older than his American peers at his first nomination and, like other foreigners, had not been nominated for his earlier masterworks, "La Strada" and "Nights of Cabiria", though both films had won the Best Foreign-Language Picture in 1956 and 1957, respectively. Fellini later received an Honorary Oscar in 1993, which was basically a compensatory gesture.
- **H:** An Italian director is awarded an honorary Oscar.
- **FA:** Fellini, identified as an Italian director, received an Honorary Oscar in 1993, confirming an Italian director was awarded this honor.

## 18. idx 2055 · entailment

- **P:** Nonetheless, a literacy rate of 96 percent put Cuba on a par with such highly developed countries as Japan, France, the Soviet Union, Switzerland and Italy, Campo said.
- **H:** The literacy rate in Cuba is 96%.
- **FA:** Campo explicitly states that Cuba's literacy rate is 96 percent, making this a direct factual assertion within the sentence.

## 19. idx 1020 · not_entailment

- **P:** But most Israelis, including those sympathetic to the settlers' efforts to reclaim all the territory that was part of the biblical Land of Israel, reacted with horror to the Hebron killings and the subsequent violence.
- **H:** Hebron is located 20 miles south of Jerusalem.
- **FA:** The text describes reactions to the killings but provides no geographical information regarding Hebron's location relative to Jerusalem.

## 20. idx 2008 · entailment

- **P:** Saginaw police responded to a domestic violence complaint at the wrong house and ended up shooting the owners' dog.
- **H:** Saginaw police mistakenly went to the wrong house in response to a complaint.
- **FA:** Police responded to a complaint at the wrong house, which indicates they mistakenly went to the incorrect location in response to the domestic violence report.

## 21. idx 1666 · entailment

- **P:** Capital punishment has a deterrent effect.
- **H:** Capital punishment is a deterrent to crime.
- **FA:** Deterrent effect and deterrent to crime are synonymous phrases referring to the same concept, so the statement directly confirms capital punishment's role in preventing crime.

## 22. idx 957 · entailment

- **P:** The activists had been imprisoned in relation to their protest in the main square of Krakow , Poland, against the presence of Vladimir Putin at the ceremonies for the 60th anniversary of the freeing of the Auschwitz-Birkenau concentration camp.
- **H:** Vladimir Putin participated in the ceremonies for the freeing of the Auschwitz Birkenau concentration camp.
- **FA:** Putin was present at the ceremonies for the camp's freeing, and the activists protested against his presence there.

## 23. idx 552 · not_entailment

- **P:** Further evidence emerged on Wednesday of the severe downturn in the aviation sector as Emirates pulled its giant Airbus A380s off the Dubai to New York route. The airline blamed the weakening global economy for the decision, an embarrassing U-turn only eight months after its A380 services were launched with the New York route. Emirates' failure to make New York work with the A380 has raised concerns about the large number of the double-decker aircraft ordered by the carrier. It is the A380's largest customer and has ordered 58 of the 500-seat aircraft. It operates two to New York, one to Heathrow and one to Sydney.
- **H:** A380 has only 58 seats.
- **FA:** Emirates ordered 58 A380s, which are each 500-seat aircraft; the number 58 refers to the quantity of planes, not the seat capacity.

## 24. idx 2129 · not_entailment

- **P:** Ahern, who was travelling to Tokyo for an EU-Japan summit yesterday, will consult with other EU leaders by telephone later this week in an effort to find an agreed candidate to presidency of the European commission.
- **H:** EU leaders found an agreement about a candidate to the post of European commission president.
- **FA:** Leaders plan to consult by telephone later this week to find a candidate, meaning no agreement has been reached yet.

## 25. idx 558 · not_entailment

- **P:** With a 38-35 victory over the New York Giants at Giants Stadium Saturday night, the New England Patriots became the second team in the modern era of the National Football League to go undefeated (16-0) in the regular season. The only other team to have achieved this feat was the Miami Dolphins in 1972, who were 14-0 due to a different regular season structure at the time.
- **H:** New England Patriots is the name of a fast food chain.
- **FA:** The Patriots are described as an NFL team that defeated the Giants in a regular season game, not as a fast food chain.

## 26. idx 1883 · entailment

- **P:** Tom Online revenues for the three months ended June 30, 2005 were US$42.78 mn, an increase of 38.5% over the same period in 2004.
- **H:** Tom Online revenues have risen by 38.5%.
- **FA:** Revenues increased by 38.5% over the prior year, confirming the reported rise in Tom Online's financial performance for that period.

## 27. idx 1108 · not_entailment

- **P:** Christopher Hitchens called him a "Bin Ladenist" and Cathy Young editorialized in The Boston Globe that he "blames the victims of terrorism" when he puts out a novel like Snowball's Chance, a biting send-up of George Orwell's Animal Farm which he was inspired to write after the terrorist attacks on September 11. "The clear references to 9/11 in the apocalyptic ending can only bring Orwell's name into disrepute in the U.S.," wrote William Hamilton, the British literary executor of the Orwell estate. That process had already begun: it was revealed Orwell gave the British Foreign Office a list of people he suspected of being "crypto-Communists and fellow travelers," labeling some of them as Jews and homosexuals. "I really wanted to explode that book," Reed told The New York Times. "I wanted to completely undermine it."
- **H:** Cathy Young is the author of "Snowball's Chance".
- **FA:** Young editorialized about the novel; Hitchens wrote it, making Young the critic rather than the author.

## 28. idx 161 · not_entailment

- **P:** Gamma ray bursts are some of the most powerful objects observed in the Universe and are thought to signal the birth of black holes. Swift is designed to detect the bursts and automatically re-orient itself to gather images and data of the phenomenon.
- **H:** Gamma rays are forms of electromagnetic radiation.
- **FA:** The text mentions gamma ray bursts but never defines them as electromagnetic radiation, leaving their physical nature unspecified.

## 29. idx 1371 · entailment

- **P:** Around 130 flights were cancelled during a strike held on 19 January, and others were cancelled in the days that followed. When the flight assistants announced a further 24-hour for 23 January, the Italian Guarantee Authority (Commissione di Garanzia) which regulates strikes in essential public services (under the terms of laws no. 194/1990 and no. 83/2000) (IT0004266F) accused the unions of breaching the legal provision that 10 days must elapse between one strike and the next.
- **H:** Italian flight assistants go on strike.
- **FA:** Flight assistants announced a strike for January 23, and flights were cancelled during a strike on January 19, confirming they went on strike.

## 30. idx 1 · entailment

- **P:** A place of sorrow, after Pope John Paul II died, became a place of celebration, as Roman Catholic faithful gathered in downtown Chicago to mark the installation of new Pope Benedict XVI.
- **H:** Pope Benedict XVI is the new leader of the Roman Catholic Church.
- **FA:** Pope Benedict XVI was installed as Pope, and since the Pope is the leader of the Roman Catholic Church, he is its new leader.
