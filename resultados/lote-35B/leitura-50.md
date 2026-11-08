# Leitura de 50 justificativas do lote 35B, variante F (27/10)

**Como saiu:** de `racionalizacoes-F-35B.csv`, que já está na ordem da semente 42 (o treino inteiro embaralhado). Os
primeiros 17 pares de implicação, 17 de neutro e 16 de contradição, nessa ordem do arquivo (50 não divide por 3; a
contradição ficou com 16). Linhas do arquivo de origem: 0–70.

**Rubrica (29/10, escolha do Pedro):** as quatro perguntas da Parte 2 da avaliação humana de Wiegreffe et al. (2022),
*Reframing Human-AI Collaboration for Generating Free-Text Explanations*, NAACL 2022, App. B.3. Lá, o anotador vê o
par, o rótulo-ouro e uma justificativa por vez, e julga considerando o rótulo correto, mesmo que discorde dele. A Parte 1
(gramática, generalidade, factualidade) ficou de fora, porque no SNLI ficou perto do teto. **Procedência:** a rubrica
veio da extração de um agente (`docs/leituras/2026-10-20-frameworks-extracao.md` §7, nível 3); conferir no §2.3 e no
App. B.3 do paper antes de citar.

1. **Nova** (s/n): a justificativa traz fato, informação ou raciocínio que não está no par nem no rótulo? (pega o eco)
2. **Sustenta** (s/n): o que ela diz é relevante para justificar o rótulo dado?
3. **Quantidade** (p/s/d): pouca, suficiente ou demais para justificar o rótulo? O ideal é s.
4. **Aceitável** (s/n): no geral, você aceitaria essa justificativa?

**Como responder (dá pelo celular):** uma linha por par, nessa ordem, com motivo opcional no fim. Exemplo:
`2: s s s s` · `7: n s p n eco` · `12: s n s n defende neutro`.

A justificativa humana do e-SNLI saiu desta folha para não ancorar o julgamento (no paper o anotador vê uma
justificativa por vez). Ela continua no CSV.

## 1. implicação · `1932161768.jpg#3r3e`

- **Premissa:** A small white dog climbs over a log.
- **Hipótese:** An animal is near a log.
- **Qwen 35B:** A dog is an animal, and climbing over a log implies it is positioned adjacent to or on top of the log.

Nova · Sustenta · Quantidade · Aceitável: 

## 2. contradição · `11610969.jpg#4r2c`

- **Premissa:** A big outdoor market along a fence.
- **Hipótese:** An empty field.
- **Qwen 35B:** A market involves many people and stalls, while an empty field lacks such presence, making them mutually exclusive states for the same location.

Nova · Sustenta · Quantidade · Aceitável: 

## 3. neutro · `4709167742.jpg#4r1n`

- **Premissa:** A man in a white shirt is walking across the street.
- **Hipótese:** A guy crosses the street to enter the bar.
- **Qwen 35B:** A man and a guy are synonyms, but walking across the street does not specify the destination is a bar; he could be going anywhere.

Nova · Sustenta · Quantidade · Aceitável: 

## 4. contradição · `5279140646.jpg#2r1c`

- **Premissa:** A man is watching a woman bowl while another woman smiles.
- **Hipótese:** A man watches a women play basketball while a women smiles.
- **Qwen 35B:** Bowling requires a lane and ball, whereas basketball is played on a court with a hoop; these are distinct activities that cannot occur simultaneously for the same people.

Nova · Sustenta · Quantidade · Aceitável: 

## 5. neutro · `2446932233.jpg#0r5n`

- **Premissa:** Four men and a woman sit at a conference table covered in a white sheet, with beverages in front of them and one has a microphone.
- **Hipótese:** Some people are drinking.
- **Qwen 35B:** Beverages are present but may be untouched or for others; sitting and speaking do not guarantee consumption is occurring simultaneously.

Nova · Sustenta · Quantidade · Aceitável: 

## 6. implicação · `4444863942.jpg#3r1e`

- **Premissa:** A female politician is wearing a green jacket and holding hands with a man.
- **Hipótese:** There are two people in this picture
- **Qwen 35B:** A female politician and a man constitute two distinct individuals, confirming that two people are present in the scene.

Nova · Sustenta · Quantidade · Aceitável: 

## 7. contradição · `3153720471.jpg#2r1c`

- **Premissa:** A little boy is sitting in front of a fireplace next to a Ginger bread house.
- **Hipótese:** The boy is small enough to fit inside the gingerbread house
- **Qwen 35B:** Sitting in front of a fireplace implies being outside the house structure, while fitting inside requires being within its boundaries, making both positions mutually exclusive simultaneously.

Nova · Sustenta · Quantidade · Aceitável: 

## 8. contradição · `3690159129.jpg#3r1c`

- **Premissa:** A rollerblader pauses at the top of a skate ramp.
- **Hipótese:** The skateboarder paused at the top of the pool to think of his next move.
- **Qwen 35B:** A rollerblader wears rollerblades, while a skateboarder uses a skateboard; these are distinct pieces of equipment that cannot be used simultaneously by the same person in the same moment.

Nova · Sustenta · Quantidade · Aceitável: 

## 9. neutro · `2871989067.jpg#1r1n`

- **Premissa:** Four cheerleaders in a squad walk along a football field.
- **Hipótese:** There are two girls and two boys.
- **Qwen 35B:** Cheerleading squads can consist entirely of girls or boys, so four cheerleaders do not necessarily include both genders.

Nova · Sustenta · Quantidade · Aceitável: 

## 10. neutro · `2619932923.jpg#3r1n`

- **Premissa:** Two men work on a truck carrying cargo.
- **Hipótese:** Two men are working on a truck and the truck goes out of gear.
- **Qwen 35B:** A truck can have cargo without having mechanical issues, as working on it doesn't imply a specific malfunction like going out of gear.

Nova · Sustenta · Quantidade · Aceitável: 

## 11. contradição · `3564322601.jpg#0r1c`

- **Premissa:** two girls wearing a yellow shirt, one wearing a green shirt, and the last wearing a pink are each looking to the side
- **Hipótese:** Three boys are looking at something to the side of them.
- **Qwen 35B:** Girls are female children, not boys; therefore, the subjects described as girls cannot simultaneously be three boys in the same moment.

Nova · Sustenta · Quantidade · Aceitável: 

## 12. implicação · `6441444261.jpg#2r1e`

- **Premissa:** A man on a yellow and green surfboard near shore.
- **Hipótese:** A man on a surfboard near shore.
- **Qwen 35B:** The yellow and green surfboard is a specific type of surfboard, so a man on it is necessarily a man on a surfboard near shore.

Nova · Sustenta · Quantidade · Aceitável: 

## 13. neutro · `3179448577.jpg#1r1n`

- **Premissa:** A man is playing a drum as a crowd of people are walking by.
- **Hipótese:** People tip the man playing drums
- **Qwen 35B:** People walk by without stopping to listen or give money, so they may not notice the performance or choose not to support it financially.

Nova · Sustenta · Quantidade · Aceitável: 

## 14. neutro · `6848902929.jpg#2r1n`

- **Premissa:** A bartender pours a frothy drink into a tall glass.
- **Hipótese:** The bartender is a man.
- **Qwen 35B:** Bartenders can be men or women, so the gender is not specified by the action of pouring a drink into a glass.

Nova · Sustenta · Quantidade · Aceitável: 

## 15. contradição · `3262386960.jpg#1r1c`

- **Premissa:** A few players show off their jousting skills in a gym.
- **Hipótese:** The players are outside drinking lemonade.
- **Qwen 35B:** Jousting requires a large indoor space like a gym, whereas drinking lemonade outside implies being outdoors, making these locations mutually exclusive at the same moment.

Nova · Sustenta · Quantidade · Aceitável: 

## 16. neutro · `327762135.jpg#4r1n`

- **Premissa:** Girl wearing black shops in a supermarket.
- **Hipótese:** The girl wearing black sometimes shops in a supermarket.
- **Qwen 35B:** Wearing black is a temporary state, while "sometimes" implies a recurring habit or general characteristic that cannot be definitively inferred from a single instance of observation.

Nova · Sustenta · Quantidade · Aceitável: 

## 17. neutro · `214597976.jpg#1r1n`

- **Premissa:** One man in a baseball cap is watching a man in glasses paint watches.
- **Hipótese:** A man is holding a paintbrush.
- **Qwen 35B:** Painting can be done with spray cans or rollers, so holding a brush is not required for the act of painting.

Nova · Sustenta · Quantidade · Aceitável: 

## 18. contradição · `24187497.jpg#3r1c`

- **Premissa:** A man in an orange shirt and yellow hard hat walks on a road.
- **Hipótese:** A worker sits in a cubicle.
- **Qwen 35B:** Walking on a road requires being outdoors and moving, while sitting in a cubicle implies being indoors and stationary.

Nova · Sustenta · Quantidade · Aceitável: 

## 19. neutro · `2987439273.jpg#3r1n`

- **Premissa:** A crowd of people are gathered with their hands up in the air.
- **Hipótese:** a crowd is at a concert
- **Qwen 35B:** Crowds raise hands to cheer at sports games, protests, and religious ceremonies, not exclusively at concerts.

Nova · Sustenta · Quantidade · Aceitável: 

## 20. contradição · `3207676216.jpg#0r1c`

- **Premissa:** four husky dogs are pulling a sled in a race through the snow guided by a man wearing number eleven.
- **Hipótese:** four husky dogs are not pulling a sled
- **Qwen 35B:** Pulling a sled is an active physical task that requires engagement, whereas not pulling implies inactivity or absence of force, making both states impossible simultaneously.

Nova · Sustenta · Quantidade · Aceitável: 

## 21. implicação · `20971288.jpg#3r1e`

- **Premissa:** Elderly women are sitting at a table.
- **Hipótese:** old lady sitting in a table.
- **Qwen 35B:** Elderly women are old ladies, and sitting at a table implies an old lady is sitting there.

Nova · Sustenta · Quantidade · Aceitável: 

## 22. implicação · `1012150929.jpg#1r4e`

- **Premissa:** A young boy plays a video game in a McDonald's restaurant.
- **Hipótese:** A boy is sitting inside a building playing a game.
- **Qwen 35B:** McDonald’s is an indoor establishment, and playing video games typically involves sitting down to use the console or device comfortably.

Nova · Sustenta · Quantidade · Aceitável: 

## 23. contradição · `10637120.jpg#3r1c`

- **Premissa:** A man in a hard hat is wearing a blue shirt and blue jean overalls.
- **Hipótese:** A man in a hard hat is wearing no shirt and blue jeans overalls.
- **Qwen 35B:** Wearing a blue shirt means having clothing on the upper body, while wearing no shirt means being bare-chested, which are mutually exclusive states.

Nova · Sustenta · Quantidade · Aceitável: 

## 24. implicação · `149231190.jpg#3r1e`

- **Premissa:** People look on to a parking lot full of motorcycles.
- **Hipótese:** People are looking at motorcycles.
- **Qwen 35B:** Looking at a parking lot full of motorcycles means directing attention to its contents, which are motorcycles.

Nova · Sustenta · Quantidade · Aceitável: 

## 25. neutro · `3824938721.jpg#1r1n`

- **Premissa:** A band is playing under a tent while people watch them play from chairs several yards away.
- **Hipótese:** The band is playing at a wedding ceremony.
- **Qwen 35B:** Bands perform under tents at festivals, parties, and community events, so this setting does not exclusively indicate a wedding ceremony.

Nova · Sustenta · Quantidade · Aceitável: 

## 26. contradição · `107318069.jpg#3r3c`

- **Premissa:** A crowd watching air balloons at night.
- **Hipótese:** People are watching airplanes at 10:00 a.m.
- **Qwen 35B:** Night occurs after sunset, while 10:00 a.m. is during daylight hours; these distinct times cannot exist simultaneously in the same moment.

Nova · Sustenta · Quantidade · Aceitável: 

## 27. contradição · `4715755037.jpg#3r1c`

- **Premissa:** Two man on stallions perform lassoing a small black calf.
- **Hipótese:** Women at the beauty shop
- **Qwen 35B:** Lassoing calves on stallions requires being outdoors on a ranch, whereas women at a beauty shop are indoors performing hair services.

Nova · Sustenta · Quantidade · Aceitável: 

## 28. neutro · `7638876050.jpg#1r1n`

- **Premissa:** A rock and roll concert ensues as a guitarist steals the spotlight.
- **Hipótese:** a guitarist is the most important in the band
- **Qwen 35B:** Guitarists often steal the spotlight through solos or stage presence without being the primary creative force or leader of the band.

Nova · Sustenta · Quantidade · Aceitável: 

## 29. neutro · `5501939710.jpg#2r1n`

- **Premissa:** Children are laughing as they sack race against each other.
- **Hipótese:** The children are at a park.
- **Qwen 35B:** Sack races occur at school fairs, community festivals, and family reunions, not exclusively in parks.

Nova · Sustenta · Quantidade · Aceitável: 

## 30. implicação · `4977405533.jpg#4r1e`

- **Premissa:** three army men with guns.
- **Hipótese:** Three men in uniform.
- **Qwen 35B:** Army men are soldiers who wear uniforms as part of their official attire, so seeing them implies they are dressed in these standard military garments.

Nova · Sustenta · Quantidade · Aceitável: 

## 31. neutro · `892870649.jpg#2r1n`

- **Premissa:** Two young boys are having fun and jumping from a swing set.
- **Hipótese:** Friends play together at recess.
- **Qwen 35B:** Boys can be siblings or classmates playing outside school, so their activity doesn't guarantee they are friends during a recess period.

Nova · Sustenta · Quantidade · Aceitável: 

## 32. neutro · `4495716228.jpg#2r1n`

- **Premissa:** Baseball players walk as a group on the field, and some jump to celebrate.
- **Hipótese:** Baseball players are celebrating a homerun.
- **Qwen 35B:** Players might celebrate winning the game, a strikeout, or completing an inning, not just hitting a home run.

Nova · Sustenta · Quantidade · Aceitável: 

## 33. neutro · `17185253.jpg#4r1n`

- **Premissa:** Elderly people sitting at a bench.
- **Hipótese:** People are sitting on a bench to rest from their long walk.
- **Qwen 35B:** Elderly people sit on benches for various reasons, such as socializing or waiting, not exclusively to rest after walking.

Nova · Sustenta · Quantidade · Aceitável: 

## 34. implicação · `4069561894.jpg#1r1e`

- **Premissa:** A woman walks toward a janitor that's wearing a raincoat and pushing a cleaning cart.
- **Hipótese:** A woman is walking approaching a janitor.
- **Qwen 35B:** Walking toward someone means getting closer to them, which is the definition of approaching, so the woman is approaching the janitor.

Nova · Sustenta · Quantidade · Aceitável: 

## 35. neutro · `3016651969.jpg#4r1n`

- **Premissa:** People are walking on a street outside of a building.
- **Hipótese:** The people walking outside are headed to their cars.
- **Qwen 35B:** People walk on streets for many reasons, such as going to shops or visiting friends, not just to reach their vehicles.

Nova · Sustenta · Quantidade · Aceitável: 

## 36. neutro · `6254643279.jpg#3r1n`

- **Premissa:** Two athletes in a gym fencing with each other.
- **Hipótese:** The people have swords.
- **Qwen 35B:** Fencing involves using foils, épées, or sabres, which are specialized weapons distinct from traditional swords used in other contexts.

Nova · Sustenta · Quantidade · Aceitável: 

## 37. contradição · `8081646730.jpg#0r5c`

- **Premissa:** A baseball player in a white uniform with dark stripes is partially on the ground, poised to catch a ball in his left hand as the ball quickly approaches.
- **Hipótese:** Superman flies out of nowhere and intercepts the ball
- **Qwen 35B:** Superman is a fictional character who does not exist in reality, so he cannot physically intercept a ball during a baseball game.

Nova · Sustenta · Quantidade · Aceitável: 

## 38. implicação · `2490179961.jpg#3r1e`

- **Premissa:** Two little girls, one with chocolate on her face, make faces.
- **Hipótese:** Two young girls are making faces.
- **Qwen 35B:** Girls are young females, and the chocolate on her face is incidental detail that does not change their identity or action of making faces.

Nova · Sustenta · Quantidade · Aceitável: 

## 39. contradição · `4756089631.jpg#4r1c`

- **Premissa:** Man in sports jacket taking picture.
- **Hipótese:** the man is asleep
- **Qwen 35B:** Taking a picture requires being awake and operating a camera, while being asleep implies unconsciousness and inactivity.

Nova · Sustenta · Quantidade · Aceitável: 

## 40. implicação · `157245265.jpg#3r1e`

- **Premissa:** A few children are rollerblading across a track, seemingly chasing each other.
- **Hipótese:** There are kids outside.
- **Qwen 35B:** Children are kids, and rollerblading on a track typically happens outdoors rather than indoors, implying they are outside.

Nova · Sustenta · Quantidade · Aceitável: 

## 41. contradição · `3578318751.jpg#4r1c`

- **Premissa:** An audience watching a performance.
- **Hipótese:** Nobody is performing.
- **Qwen 35B:** A performance requires someone to perform, so if an audience is watching a performance, there must be performers present, not nobody performing.

Nova · Sustenta · Quantidade · Aceitável: 

## 42. implicação · `2561849813.jpg#1r1e`

- **Premissa:** A baby sits on an empty beach under a big, blue sky.
- **Hipótese:** A baby sits on a beach.
- **Qwen 35B:** The baby is physically located on the sand, which constitutes the beach, making the statement true regardless of the sky or emptiness.

Nova · Sustenta · Quantidade · Aceitável: 

## 43. contradição · `3353400143.jpg#0r1c`

- **Premissa:** A man in a yellow outfit riding a yellow motorcycle.
- **Hipótese:** The man is driving a bus.
- **Qwen 35B:** A motorcycle and a bus are distinct vehicles; one cannot simultaneously operate two different modes of transportation in the same location at the same time.

Nova · Sustenta · Quantidade · Aceitável: 

## 44. contradição · `5855641283.jpg#2r1c`

- **Premissa:** A freckled child in a gray shirt is stretching one arm overhead, and grasping it with the other hand.
- **Hipótese:** The child's hands are in their pockets.
- **Qwen 35B:** Stretching an arm overhead requires it to be extended and visible, while keeping hands in pockets means they are concealed and stationary.

Nova · Sustenta · Quantidade · Aceitável: 

## 45. implicação · `3644945293.jpg#3r1e`

- **Premissa:** Young Asian women are talking at a small gathering.
- **Hipótese:** there is a kitty party of young asian ladies
- **Qwen 35B:** Young Asian women are young Asian ladies, and a small gathering where they talk fits the definition of a kitty party.

Nova · Sustenta · Quantidade · Aceitável: 

## 46. implicação · `380515798.jpg#2r1e`

- **Premissa:** A street market filled with white tents, pedestrians, and vendors.
- **Hipótese:** People are attending the market.
- **Qwen 35B:** Pedestrians are people who visit places, and vendors operate markets; thus their presence confirms that people are attending the market.

Nova · Sustenta · Quantidade · Aceitável: 

## 47. implicação · `374124237.jpg#0r1e`

- **Premissa:** A woman is propping her leg up revealing cleavage, a great tatoo, and some kicking boots.
- **Hipótese:** An attractive woman with tattoos looking sexy.
- **Qwen 35B:** Cleavage is associated with sexiness and tattoos are visible body art, so revealing them implies an attractive woman with tattoos looking sexy.

Nova · Sustenta · Quantidade · Aceitável: 

## 48. implicação · `4887180035.jpg#1r4e`

- **Premissa:** A young brunette wearing purple and black floral stretch pants is attaching her bike to a finch.
- **Hipótese:** A young woman is standing on the ground.
- **Qwen 35B:** A brunette wearing pants is a young woman, and attaching a bike to a fence typically requires standing on the ground rather than flying or sitting in a car.

Nova · Sustenta · Quantidade · Aceitável: 

## 49. implicação · `4647908531.jpg#0r1e`

- **Premissa:** A man in a green shirt, holding a bike in front of him, looking towards an officer talking to several young men.
- **Hipótese:** A man watches a talking officer.
- **Qwen 35B:** The man looks toward the officer, which constitutes watching him, and the officer is described as talking to others.

Nova · Sustenta · Quantidade · Aceitável: 

## 50. implicação · `2315350560.jpg#3r1e`

- **Premissa:** Three women, one holding up a red and white dress.
- **Hipótese:** Three women holding one dress.
- **Qwen 35B:** The phrase "one holding up" distributes the action across the group, meaning all three women are collectively holding the single dress.

Nova · Sustenta · Quantidade · Aceitável: 
