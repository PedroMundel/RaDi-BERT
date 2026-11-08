# Piloto Qwen3.5-9B, variante E: lado a lado (45 pares do dev do e-SNLI)

Variante E do prompt; Haiku e Sonnet são do prompt A. Humano = `Explanation_1` do e-SNLI.

## 25 · entailment

- **P:** A woman is walking with a boy who is holding a flag.
- **H:** A lady is next to a child who has a flag.

| Fonte | Justificativa |
|---|---|
| Humano | There is a lady next to a boy who is holding a flag. |
| Haiku | A woman is a lady and a boy is a child, and "walking with" implies being next to them, while "holding a flag" means the boy has a flag. So if the premise is true, every part of the hypothesis must also be true. |
| Sonnet | "Lady" and "woman" refer to the same person, and "child" covers "boy." Someone walking with another person is next to them, and holding a flag means having one. Each part of the hypothesis is therefore guaranteed by the premise. |
| **Qwen E** | A woman is a lady and a boy is a child, so walking beside someone holding a flag matches being next to a child with one. |

## 309 · entailment

- **P:** Two backpackers look at scenic mountains.
- **H:** Two guys are carrying things on their back.

| Fonte | Justificativa |
|---|---|
| Humano | Two backpackers view scenic mountains. |
| Haiku | The premise doesn't establish that the two backpackers are men or that they are wearing their packs at that moment. "Backpackers" suggests packs, but it doesn't guarantee that the hypothesis is true, so the given label is not strictly justified. |
| Sonnet | Backpackers are, by definition, people who carry packs on their backs, so the premise already implies that both are carrying things there. The hypothesis's "guys" is a reasonable reading of "two backpackers," so the hypothesis follows from the premise. |
| **Qwen E** | Backpackers are travelers who carry backpacks on their backs to transport their belongings while hiking or exploring scenic areas. |

## 73 · entailment

- **P:** A man sleeping on the ground in a subway.
- **H:** There is a man on the ground.

| Fonte | Justificativa |
|---|---|
| Humano | Sleeping on the ground implies man on the ground. |
| Haiku | A man sleeping on the ground in a subway is necessarily a man lying on the ground, so if the premise is true, the hypothesis must also be true. The hypothesis simply drops details (sleeping, subway) while keeping a claim that the premise fully guarantees. |
| Sonnet | If a man is sleeping on the ground in a subway, then a man is necessarily on the ground. The hypothesis simply restates part of the premise, leaving out the details about sleeping and the subway. |
| **Qwen E** | Since a man sleeping on the ground is necessarily located on the ground, this scenario confirms that there is a man on the ground. |

## 195 · entailment

- **P:** The baby in a blue jean hat and sunglasses looks at the camera while being held.
- **H:** A baby looks at the camera.

| Fonte | Justificativa |
|---|---|
| Humano | The baby looks at a camera. |
| Haiku | The premise describes a baby looking at the camera, and the hypothesis simply drops the extra details (the hat, the sunglasses, being held) while keeping the core event. Since any scene matching the premise necessarily includes a baby looking at the camera, the hypothesis must be true whenever the premise is. |
| Sonnet | The premise says the baby, who is wearing a blue jean hat and sunglasses, looks at the camera while being held. That directly states that a baby looks at the camera, so the hypothesis follows from it. |
| **Qwen E** | The baby described in the premise is looking at the camera while being held, which directly confirms that a baby looks at the camera without adding unrelated details. |

## 57 · entailment

- **P:** A woman wearing a white baseball cap purple coat holding a poster.
- **H:** A woman with a hat holding a poster.

| Fonte | Justificativa |
|---|---|
| Humano | a cap is a hat |
| Haiku | The premise describes a woman wearing a white baseball cap and holding a poster, so she necessarily has a hat and is holding a poster as the hypothesis states. The hypothesis simply drops details (the cap's color and type, the coat), and everything it asserts is guaranteed by the premise. |
| Sonnet | The premise describes a woman in a white baseball cap holding a poster, and a baseball cap is a type of hat. So a woman with a hat holding a poster must be true given the premise. |
| **Qwen E** | Wearing a white baseball cap means the woman has a hat, so describing her as having a hat is consistent with the premise details. |

## 296 · entailment

- **P:** An old man and lady in a white uniform is standing next to a man in black playing an instrument.
- **H:** A man in black is playing an instrument.

| Fonte | Justificativa |
|---|---|
| Humano | The man in black is playing an instrument alone. |
| Haiku | The premise explicitly describes a man in black playing an instrument, so if the premise is true, the hypothesis, which states the same thing without the extra details about the old man and lady, must also be true. |
| Sonnet | The premise directly states that there is a man in black playing an instrument, with the old man and lady standing next to him. The hypothesis restates that part of the scene, so it must be true if the premise is. |
| **Qwen E** | The premise describes a man in black playing an instrument alongside others, which directly confirms that a man in black is indeed playing an instrument. |

## 281 · entailment

- **P:** Three women, two wearing red shirts and one wearing a purple shirt, and a man, wearing a light blue shirt, jump on a basketball court with balls in their hands.
- **H:** Some people's are playing basketball in basketball court

| Fonte | Justificativa |
|---|---|
| Humano | People are playing basketball on the court. |
| Haiku | The premise describes several people on a basketball court holding balls, which strongly implies they are playing basketball, so the hypothesis that some people are playing basketball on a court must be true if the premise is. The hypothesis is a general, weaker claim that the premise fully supports, even though it omits details like the shirt colors and the jumping. |
| Sonnet | The premise describes four people jumping on a basketball court while holding balls, which strongly implies they are playing basketball, so "some people are playing basketball in a basketball court" follows naturally. The setting and the action of jumping with balls in hand are enough to support the hypothesis. |
| **Qwen E** | People jumping on a basketball court with balls are playing basketball, so the presence of these specific individuals entails that some people are playing there. |

## 180 · entailment

- **P:** A crowd of people, almost all in helmets, some in masks, face the camera while someone in a red cap looks backward.
- **H:** The camera catches the faces of a crowd of people

| Fonte | Justificativa |
|---|---|
| Humano | "The camera catches the faces" implies that the people face the camera. |
| Haiku | The premise states that a crowd of people is facing the camera, which means the camera would capture their faces, so the hypothesis necessarily follows. The details about helmets, masks, and the person in the red cap are extra information that doesn't change this core relationship. |
| Sonnet | The premise says the crowd faces the camera, so the camera captures their faces, which is what the hypothesis states. Helmets and masks may cover parts of some faces, but the crowd is still oriented toward the camera, so the hypothesis follows. |
| **Qwen E** | The premise describes a crowd facing the camera, which means their faces are directed toward it and thus captured by the camera. |

## 211 · entailment

- **P:** A dune buggy with one male passenger gets some air as it drives over a sand dune.
- **H:** A dune buggy drives over sand

| Fonte | Justificativa |
|---|---|
| Humano | A dune buggy drives over a sand dune must be over sand. |
| Haiku | The premise describes a dune buggy driving over a sand dune, and a sand dune is made of sand, so the premise necessarily means the buggy is driving over sand. The hypothesis is a more general restatement of an event the premise already guarantees, so it must be true whenever the premise is. |
| Sonnet | The premise says the dune buggy drives over a sand dune, and a sand dune is made of sand, so the buggy is driving over sand. The hypothesis restates this in more general terms, so it must be true whenever the premise is. |
| **Qwen E** | Dune buggies are specifically designed to drive over sand dunes, and getting air while doing so confirms they are actively moving across that terrain. |

## 197 · entailment

- **P:** There are a lot of people in front of a tan building with colorful squares hanging from the top.
- **H:** People stand in front of a building

| Fonte | Justificativa |
|---|---|
| Humano | If people are in front of a building they are outdoors and likely to be standing. |
| Haiku | The premise states that many people are in front of a building, so it necessarily follows that people are standing in front of a building. The hypothesis only generalizes the specific details (the tan color and hanging squares) away, so anything the premise describes must also be true of the hypothesis. |
| Sonnet | The premise says there are many people in front of a tan building, so it guarantees that people are in front of a building. The hypothesis leaves out details such as the building's color and the colorful squares, but it doesn't conflict with them. "Stand" is a natural reading of people being in front of a building. |
| **Qwen E** | The premise describes many people located in front of a tan building with decorations, which confirms that people are standing in front of a building as stated in the hypothesis. |

## 75 · entailment

- **P:** A group of uniformed men carrying a cross adorned with a white ribbon in formation walking down the street on Easter.
- **H:** Several service men are carrying a cross on Easter.

| Fonte | Justificativa |
|---|---|
| Humano | Several service men implies a group of uniformed men. |
| Haiku | Uniformed men are a kind of service men, and "a group" of them is at least several, so the premise's description of men carrying a cross on Easter necessarily covers the hypothesis. The only difference is wording ("several service men" versus "uniformed men in formation"), which doesn't add or remove any essential detail. |
| Sonnet | The premise describes a group of uniformed men carrying a cross on Easter, which matches the hypothesis's "several service men" carrying a cross on Easter, since "uniformed men" can reasonably be read as service men and "a group" as "several." The extra details about the white ribbon and the formation don't conflict with the hypothesis, so it follows from the premise. |
| **Qwen E** | Uniformed men are service members, and carrying a cross in formation on Easter matches the description of several service men doing so on that holiday. |

## 9 · entailment

- **P:** People wait in line at bus stop.
- **H:** The bus already has people waiting on it.

| Fonte | Justificativa |
|---|---|
| Humano | People have to wait for bus in the bus stop |
| Haiku | The premise places people in line at a bus stop, not on a bus, so it does not guarantee that anyone is already on the bus. The assigned label doesn't fit; the hypothesis could be true, but the premise doesn't establish it. |
| Sonnet | The label given doesn't actually fit well. The premise says people are waiting in line at a bus stop, which doesn't guarantee anyone is already on the bus, so the hypothesis could be true but isn't required to be. A more accurate judgment here would be that the premise leaves the hypothesis open rather than guaranteeing it. |
| **Qwen E** | People waiting at a bus stop implies they are waiting for an arriving bus, which means passengers must already be inside or boarding it. |

## 320 · entailment

- **P:** A woman is holding a sign that says honk to indict bush.
- **H:** The woman is touching the sign.

| Fonte | Justificativa |
|---|---|
| Humano | Because a woman is holding a sign, the woman is touching the sign. |
| Haiku | To hold a sign, a person must have physical contact with it, so if the woman is holding the sign, she is necessarily touching it. The hypothesis therefore must be true whenever the premise is true. |
| Sonnet | Holding a sign necessarily involves physical contact with it, so if the woman is holding the sign, she must be touching it. The hypothesis follows directly from the premise. |
| **Qwen E** | Holding an object requires physical contact with it, so a woman holding a sign necessarily means she is touching that specific sign. |

## 126 · entailment

- **P:** A gray-haired woman wearing tan pants, a yellow and white jacket and sunglasses is sitting on a bench.
- **H:** The woman has gray hair.

| Fonte | Justificativa |
|---|---|
| Humano | The woman on the bench has gray hair. |
| Haiku | The premise explicitly describes the woman as "gray-haired," so if the premise is true, her having gray hair must also be true. The hypothesis restates this attribute directly, with no added information that the premise fails to guarantee. |
| Sonnet | The premise describes the woman as "gray-haired," which directly states that she has gray hair. So if the premise is true, the hypothesis must also be true. |
| **Qwen E** | The premise explicitly describes a gray-haired woman, which directly confirms the hypothesis that she possesses gray hair without requiring any external assumptions. |

## 265 · entailment

- **P:** Guy playing the guitar on a bench with another man watching him.
- **H:** Someone plays a guitar.

| Fonte | Justificativa |
|---|---|
| Humano | A guy is someone and the guy is playing a guitar. |
| Haiku | A guy playing the guitar is itself a person playing a guitar, so if the premise is true, the more general claim that someone plays a guitar must also be true. The other man watching him does not affect this, since the hypothesis only requires that at least one person is playing a guitar. |
| Sonnet | The premise says a guy is playing the guitar, and a guy is a someone, so the hypothesis restates part of what the premise already states. Nothing in the premise could make it true while "someone plays a guitar" is false. |
| **Qwen E** | Playing the guitar is a specific action that inherently means someone is playing it, so the general statement follows directly from the detailed premise. |

## 359 · neutral

- **P:** A woman sits in a chair under a tree and plays an acoustic guitar.
- **H:** A woman is playing a country song on her guitar while her husband in the distance listens.

| Fonte | Justificativa |
|---|---|
| Humano | A woman playing a guitar does not imply she is playing a country song, or that she has a husband in the distance listening. |
| Haiku | The premise confirms a woman playing an acoustic guitar under a tree, but it says nothing about the style of music being a country song, nor about a husband or anyone listening in the distance. These details could be true, but the premise does not guarantee them, so the hypothesis goes beyond what is stated. |
| Sonnet | The premise says only that a woman is playing an acoustic guitar under a tree. It says nothing about the genre of the song, whether she has a husband, or whether anyone is listening in the distance. These details could be true but are not guaranteed, and nothing in the premise rules them out. |
| **Qwen E** | The premise shows a woman playing guitar but provides no information about her husband's presence or whether she is playing a country song. |

## 643 · neutral

- **P:** A man is playing with a baby on a deck.
- **H:** A man plays with his son.

| Fonte | Justificativa |
|---|---|
| Humano | Only because a man is playing with a baby doesn't necessarily mean the baby is his son. |
| Haiku | The premise shows a man playing with a baby but says nothing about whether the baby is his son or related to him at all, so the hypothesis could be true without being guaranteed. The "son" detail goes beyond what the premise states, leaving the relationship unconfirmed. |
| Sonnet | The premise says only that a man is playing with a baby, and it never says the baby is his son. The baby could be a daughter, a relative, or an unrelated child, so the hypothesis is possible but not guaranteed. |
| **Qwen E** | The man playing with a baby could be his son, but the baby might also be a niece, nephew, or neighbor's child. |

## 407 · neutral

- **P:** Four men riding in a gray, fast moving boat appear to be wearing vests.
- **H:** Four men are racing their boat for pink slips.

| Fonte | Justificativa |
|---|---|
| Humano | Riding in a boat doesn't imply racing for pink slips. |
| Haiku | The premise establishes that four men are in a fast-moving gray boat wearing vests, but it says nothing about why they are moving quickly, such as whether they are racing or what stakes are involved. The hypothesis adds a specific motive, racing for pink slips (a wager on a vehicle's title), which could be true but is not guaranteed by the description. |
| Sonnet | The premise only says four men are riding in a fast-moving boat and seem to be wearing vests, which says nothing about whether they are racing or what the stakes are. They could be racing for pink slips, but they could just as easily be traveling, fishing, or out for fun, so the hypothesis is possible but not guaranteed. |
| **Qwen E** | Boats are raced for various reasons like trophies or charity, not exclusively for pink slips, so the specific motive mentioned is not confirmed by the premise. |

## 529 · neutral

- **P:** A man and a young boy are eating on a city sidewalk next to a cardboard box and a red shopping cart.
- **H:** father is eating with his son on a city sidewalk

| Fonte | Justificativa |
|---|---|
| Humano | Not all men and boys are father and son. |
| Haiku | The premise establishes a man and a young boy eating on a city sidewalk, which matches most of the hypothesis, but it never says they are father and son; they could be relatives, friends, or strangers. Because the family relationship is an unstated assumption rather than something the premise guarantees, the hypothesis might be true without being entailed. |
| Sonnet | The premise says a man and a young boy are eating on a city sidewalk, but it never says they are related. They could be father and son, but they could also be unrelated, such as a man and a boy he is helping. The hypothesis therefore adds a family relationship that the premise doesn't guarantee. |
| **Qwen E** | A man and a boy could be strangers sharing food near a cart, as the premise does not confirm their familial relationship. |

## 391 · neutral

- **P:** People go about their daily routines- selling food, cutting hair- on the ghetto streets of Ho Chi Minh City, Vietnam.
- **H:** People are trying to go about their day as causal as possible

| Fonte | Justificativa |
|---|---|
| Humano | People can go through their daily routines without the goal of being as causal as possible. |
| Haiku | The premise describes people carrying out their everyday work, such as selling food and cutting hair, but it says nothing about their intentions or whether they are deliberately trying to be casual. The hypothesis attributes a specific motive that the premise neither confirms nor rules out, so it might be true without being guaranteed by the description. |
| Sonnet | The premise says people are carrying out ordinary routines like selling food and cutting hair, but it says nothing about whether they are deliberately trying to act as casually as possible. That intent or attitude is an added detail the premise neither confirms nor rules out. |
| **Qwen E** | People can follow daily routines like selling food or cutting hair without necessarily trying to be casual, as they might be rushing or working formally. |

## 630 · neutral

- **P:** A black dog walking through water.
- **H:** A black dog is walking through water to catch a fish.

| Fonte | Justificativa |
|---|---|
| Humano | Just because a dog is walking thru water does not mean that it is to catch a fish. |
| Haiku | The premise confirms a black dog is walking through water, but it says nothing about why the dog is doing so. The added purpose of catching a fish is a plausible guess that the premise neither states nor rules out, so the hypothesis might be true without being guaranteed. |
| Sonnet | The premise only says a black dog is walking through water, and it gives no information about why. The dog might be trying to catch a fish, but it could just as easily be playing, cooling off, or crossing to the other side, so the purpose in the hypothesis is not guaranteed. |
| **Qwen E** | A dog walking through water might be cooling off or crossing a path, which are actions that do not necessarily involve hunting fish. |

## 615 · neutral

- **P:** Two brown and white dogs, one jumping over a log while the one behind runs through the grass.
- **H:** They are playing with each other.

| Fonte | Justificativa |
|---|---|
| Humano | Dogs running around each other are not always playing with each other. |
| Haiku | The premise shows one dog jumping over a log and another running behind it, which suggests they may be playing, but it does not state their intent or any interaction between them. They could just be running independently, so the hypothesis might be true without being guaranteed. |
| Sonnet | The premise describes two dogs moving through a grassy area, one jumping a log and the other running behind it. It doesn't say whether they are interacting or playing together, since they could be chasing each other, following a person, or just running in the same direction for some other reason. So the hypothesis could be true, but the premise doesn't guarantee it. |
| **Qwen E** | Dogs running and jumping together often play, but they could also be practicing or competing without interacting as friends. |

## 514 · neutral

- **P:** a man plays his guitar on the street.
- **H:** The man is begging for money on the street.

| Fonte | Justificativa |
|---|---|
| Humano | Not all men that play guitar are begging for money. |
| Haiku | The premise only tells us a man is playing guitar on a street, which is consistent with begging for money but also with busking for fun, performing, or practicing. Since nothing in the premise rules out other purposes or guarantees that he is asking for money, the hypothesis might be true without being required by the premise. |
| Sonnet | Playing a guitar on the street doesn't tell us why the man is doing it. He could be begging or busking for money, but he could just as easily be practicing, performing for fun, or entertaining passersby, so the premise doesn't guarantee the hypothesis, and it doesn't rule it out either. |
| **Qwen E** | Playing guitar on the street does not guarantee begging, as musicians often perform just for tips or appreciation without asking for money. |

## 545 · neutral

- **P:** A small child playing in a dusty square.
- **H:** A child is playing with a doll.

| Fonte | Justificativa |
|---|---|
| Humano | Children play with many things besides a doll. |
| Haiku | The premise tells us a small child is playing in a dusty square, but says nothing about what the child is playing with. The child could be playing with a doll, but also with a ball, sand, or nothing in particular, so the hypothesis might be true without being guaranteed by the premise. |
| Sonnet | The premise says only that a small child is playing in a dusty square, without saying what the child is playing with. The child could be playing with a doll, but could just as easily be playing with a ball, in the dirt, or with nothing, so the premise doesn't guarantee the hypothesis and doesn't rule it out. |
| **Qwen E** | Playing in a dusty square does not specify the toy being used, as children could be playing with balls or other items instead of dolls. |

## 531 · neutral

- **P:** A baby in an indoor pool is using an inflatable tube on it's on
- **H:** The baby is swimming

| Fonte | Justificativa |
|---|---|
| Humano | Just because the baby is in a pool does not mean it is swimming. |
| Haiku | The premise says the baby is in a pool using an inflatable tube, which suggests it is in the water, but it doesn't establish that the baby is actually swimming, since it could be floating passively, sitting, or just playing in shallow water. Because "swimming" requires a specific motion that the premise doesn't guarantee, the hypothesis might be true without being implied. |
| Sonnet | The premise says the baby is in an indoor pool using an inflatable tube, but it doesn't say the baby is actually swimming. The baby could be floating, sitting in the tube, or just playing, so swimming is possible but not guaranteed. |
| **Qwen E** | Babies can float or play on inflatable tubes in pools without necessarily performing the active strokes required to be considered swimming. |

## 409 · neutral

- **P:** A man wearing a white shirt and an orange shirt jumped into the air.
- **H:** A man leaps as he takes a shot with the basketball.

| Fonte | Justificativa |
|---|---|
| Humano | A man jumps into the air doesn't imply that he takes a shot with the basketball. |
| Haiku | The premise says a man jumped into the air in two-tone shirts, but it says nothing about a basketball or a shot being taken. The hypothesis adds specifics (a basketball, a shot) that the premise neither confirms nor rules out, so it could be true without being guaranteed by the premise. |
| Sonnet | The premise says only that a man jumped into the air, and it doesn't mention a basketball or a shot. He could be jumping for many other reasons, so the hypothesis could be true but isn't guaranteed, and nothing in the premise rules it out either. |
| **Qwen E** | Jumping into the air could occur during various activities like parkour or martial arts, not exclusively when taking a basketball shot. |

## 343 · neutral

- **P:** Asian man giving thumbs up on street.
- **H:** An Asian man is congratulating someone for a job well done.

| Fonte | Justificativa |
|---|---|
| Humano | You can give a thumbs up without congratulating someone. |
| Haiku | A thumbs-up gesture can signal approval or encouragement, but it does not by itself establish that the man is congratulating someone or that anything was accomplished. The premise leaves out who he is addressing and why, so the more specific hypothesis about a job well done might be true without being guaranteed. |
| Sonnet | The premise only says an Asian man is giving a thumbs up on the street, and that gesture could mean many things, such as approval, agreement, or posing for a photo. Nothing in it indicates he is congratulating anyone or that a job was well done, so the hypothesis could be true but isn't guaranteed. |
| **Qwen E** | Thumbs up gestures can signal approval or a greeting, but they do not necessarily indicate that someone is congratulating another person for a specific success. |

## 653 · neutral

- **P:** A young boy is dumping a bag of Lego's onto a glass table.
- **H:** A boy is excited to build a castle out of legos.

| Fonte | Justificativa |
|---|---|
| Humano | Just because a boy is dumping out Legos doesn't mean he is excited to build a castle. |
| Haiku | The premise only describes a boy dumping a bag of Legos onto a table, which doesn't reveal his emotional state or what he plans to build. Being excited and building a castle are plausible but unstated, so the premise neither guarantees nor rules them out. |
| Sonnet | The premise only shows a boy dumping Legos onto a table, and says nothing about his emotions or what he plans to build. He could be excited and building a castle, but he could just as easily be building something else, or not be excited at all, so the hypothesis isn't guaranteed. |
| **Qwen E** | Dumping a bag of Legos does not guarantee excitement or building intent, as the boy might be cleaning up, playing messily, or simply testing the table's weight. |

## 460 · neutral

- **P:** One man wearing a blue shirt, white shorts, and sandals, and another man wearing cargo pants and a gray jacket shop at a farmer's market.
- **H:** Two men but some local fruit

| Fonte | Justificativa |
|---|---|
| Humano | Being at a farmers market does not imply one is buying local fruit. |
| Haiku | The premise confirms that two men are shopping at a farmer's market, which makes "two men" plausible, but it never mentions fruit or anything about the men buying local produce. Since the men could be buying vegetables, crafts, or nothing specific at all, the claim about local fruit is neither guaranteed nor ruled out by the premise. |
| Sonnet | The premise confirms two men are shopping at a farmer's market, which fits "two men" and is consistent with buying something there. It never says what they buy, so we can't tell whether they purchase local fruit, and the hypothesis could be true but isn't guaranteed. |
| **Qwen E** | Shoppping at a farmer's market does not guarantee that specific local fruit is present, as vendors might sell vegetables or other goods instead. |

## 599 · neutral

- **P:** A boy in a blue shirt is sitting on a couch with other people.
- **H:** A boy hanging with his friends

| Fonte | Justificativa |
|---|---|
| Humano | A boy sitting on a couch with other people must not be hanging out with them because they might not be his friend. |
| Haiku | The premise places a boy on a couch with other people, but it says nothing about how they know each other or what they are doing together, so "hanging with his friends" is plausible yet not guaranteed. The other people could be strangers, relatives, or classmates, so the hypothesis might be true without being required by the premise. |
| Sonnet | The premise only says the boy is on a couch with "other people," who could be family, strangers, or anyone else, so it doesn't establish that they are his friends. The hypothesis could be true, but the premise doesn't guarantee it. |
| **Qwen E** | People sitting together on a couch may be strangers or family members, so we cannot confirm they are friends based solely on their presence. |

## 692 · contradiction

- **P:** A young male child, wearing khaki pants and a red striped polo shirt, sitting on a steel slide in a public playground.
- **H:** A young child jumping on trampoline.

| Fonte | Justificativa |
|---|---|
| Humano | The child cannot be sitting on a steel slide and jumping on a trampoline simultaneously. |
| Haiku | The premise places the child sitting on a steel slide in a playground, while the hypothesis describes the child jumping on a trampoline. These are incompatible activities and settings, so both cannot be true of the same scene at once. |
| Sonnet | The premise describes a child sitting on a steel slide in a playground, while the hypothesis describes a child jumping on a trampoline. Sitting on a slide and jumping on a trampoline are different activities in different places, so both can't describe the same scene at once. |
| **Qwen E** | Sitting on a slide requires remaining stationary, whereas jumping on a trampoline involves continuous bouncing and movement. |

## 976 · contradiction

- **P:** Musicians are performing on stage.
- **H:** A clown is juggling balls at a circus.

| Fonte | Justificativa |
|---|---|
| Humano | Musicians make music, they don't juggle. |
| Haiku | Musicians performing on stage and a clown juggling balls at a circus describe different activities and different scenes, and nothing in the premise makes the hypothesis true. The premise doesn't say whether there's a clown or juggling at all, so this pair is better described as neutral rather than contradictory under the standard definition, since both could in principle occur at the same time. |
| Sonnet | The premise describes musicians performing on stage, while the hypothesis describes a clown juggling at a circus, which are different people doing different activities. Under the assumption that both describe the same scene, the hypothesis can't also be true, because the scene's performers are musicians rather than a clown juggling. |
| **Qwen E** | Musicians performing on stage describes a specific event that does not inherently include a clown juggling balls at a circus, making the hypothesis an unrelated alternative rather than a necessary outcome or direct conflict. |

## 740 · contradiction

- **P:** A boy in jeans, black t-shirt, and blue cap on a bike, leaps over steps.
- **H:** A boy is playing on a skateboard.

| Fonte | Justificativa |
|---|---|
| Humano | A boy that leaps over steps cannot be on a skateboard. |
| Haiku | The premise places the boy on a bike, not a skateboard, so the hypothesis's specific claim about the vehicle conflicts with the described scene. Since both describe the same action of leaping over steps, a boy cannot be on a bike and on a skateboard at the same time. |
| Sonnet | The premise describes the boy as riding a bike while leaping over steps, so the hypothesis, which puts him on a skateboard, describes a different activity and object for the same scene. He can't be on a bike and on a skateboard at once, so both can't be true. |
| **Qwen E** | Leaping over steps on a bike requires riding a bicycle, whereas playing on a skateboard involves standing on a board without pedals or handlebars. |

## 862 · contradiction

- **P:** Groups of people walking different directions, mostly dressed in dark blues and dressed to stay warm.
- **H:** A prisoner stands in place.

| Fonte | Justificativa |
|---|---|
| Humano | People can't be walking in different directions and standing in place at once. |
| Haiku | The premise describes groups of people actively walking in various directions, so it depicts a busy, moving scene. A prisoner standing in place cannot be true of that same scene, since the premise portrays people in motion and says nothing about anyone being confined or stationary, making the two descriptions incompatible. |
| Sonnet | The premise describes groups of people walking in different directions, so they are in motion rather than standing still. The hypothesis describes someone standing in place, which can't hold in the same scene, and nothing in the premise suggests anyone is a prisoner. |
| **Qwen E** | Walking in different directions implies movement across a space, which contradicts standing in place and being confined as a prisoner would be. |

## 724 · contradiction

- **P:** man grilling fish on barbecue
- **H:** The man is sailing a boat.

| Fonte | Justificativa |
|---|---|
| Humano | The man cannot be sailing a boat and grilling fish. |
| Haiku | A man grilling fish on a barbecue is engaged in cooking, which cannot happen at the same time as sailing a boat, so the two descriptions of the scene are mutually exclusive. If he is grilling, he is not sailing. |
| Sonnet | The premise describes a man standing at a barbecue cooking fish, while the hypothesis has him sailing a boat. A person can't plausibly be grilling at a barbecue and sailing at the same time in the same scene, so the two statements can't both be true. |
| **Qwen E** | Grilling fish on a barbecue requires standing on solid ground, while sailing a boat takes place on water where one steers a vessel. |

## 963 · contradiction

- **P:** Bald man in white and black shorts, punching man with black hair, and red, orange and blue shorts.
- **H:** Two men sit peacefully on a park bench.

| Fonte | Justificativa |
|---|---|
| Humano | Punching is a violent act, and cannot be done peacefully |
| Haiku | The premise describes two men in a physical fight, with one actively punching the other, while the hypothesis describes two men sitting calmly on a park bench. Both cannot describe the same scene at the same time, so the hypothesis cannot be true if the premise is. |
| Sonnet | The premise describes one man punching another, which is a violent, active scene, while the hypothesis describes two men sitting peacefully on a park bench. Punching and sitting peacefully can't happen at the same time in the same scene, so the hypothesis can't be true if the premise is. |
| **Qwen E** | Punching is an aggressive physical action that directly conflicts with the peaceful sitting described in the hypothesis. |

## 948 · contradiction

- **P:** A woman is walking down the street with a brown bookbag on her back.
- **H:** she has black book bag

| Fonte | Justificativa |
|---|---|
| Humano | Black and brown are different colors. |
| Haiku | The premise explicitly describes the woman's bookbag as brown, so the claim that she has a black book bag cannot be true if the premise is true. Both sentences describe the same bag, and its color is stated in a way that directly conflicts with the hypothesis. |
| Sonnet | The premise says the woman's bookbag is brown, so it can't also be black. Since both statements describe the same bag, the hypothesis conflicts directly with the premise. |
| **Qwen E** | A book bag cannot be brown and black at the same time, so describing it as brown contradicts the claim that it is black. |

## 847 · contradiction

- **P:** Several people, including a boy in a striped shirt walk on a concrete path away from a body of water.
- **H:** People are walking on a dirt path.

| Fonte | Justificativa |
|---|---|
| Humano | The path is either concrete or dirt. It can not be both. |
| Haiku | The premise specifies that the people are walking on a concrete path, while the hypothesis says they are on a dirt path. Both describe the same scene with the same people and surface, so the surface types cannot both be true at once. |
| Sonnet | The premise says the people are walking on a concrete path, while the hypothesis says the path is dirt. A path described as concrete is not dirt, so both statements cannot be true of the same scene. |
| **Qwen E** | Walking on a concrete path and walking on a dirt path describe mutually exclusive ground surfaces that cannot exist simultaneously in the same location. |

## 878 · contradiction

- **P:** a dog carries a large stick through the field.
- **H:** The dog is indoors

| Fonte | Justificativa |
|---|---|
| Humano | fields  is different from indoors. |
| Haiku | The premise places the dog outdoors, in a field, so it cannot also be indoors at the same time. The two descriptions of the scene are incompatible, which is what makes the hypothesis contradict the premise. |
| Sonnet | The premise places the dog in a field, which is an outdoor setting, so it can't also be indoors. The two statements describe the same scene but give incompatible locations. |
| **Qwen E** | Carrying a large stick through a field requires being outdoors, which contradicts the dog being indoors where such an environment does not exist. |

## 864 · contradiction

- **P:** A standing man in a suit finishes his turn in a chess game as his seated opponent begins his in a crowded park.
- **H:** A business man is fishing alone in the middle of the Pacific ocean.

| Fonte | Justificativa |
|---|---|
| Humano | Opponent implies the man is not alone. |
| Haiku | The premise places a man in a suit in a crowded park playing chess with a seated opponent, while the hypothesis describes a businessman fishing alone in the middle of the Pacific Ocean. These two scenes cannot both be true at once: one is a busy urban park with another person present, and the other is a solitary open-ocean setting with no chess game. |
| Sonnet | The premise puts the man in a crowded park playing chess against an opponent, while the hypothesis puts a man fishing alone in the middle of the Pacific Ocean. These settings and activities cannot both describe the same scene. |
| **Qwen E** | Finishing a chess game in a crowded park contradicts fishing alone in the middle of the Pacific ocean because the locations and activities are mutually exclusive. |

## 742 · contradiction

- **P:** A man doing maintenance on the railroad tracks
- **H:** There is a woman doing work on the railroad tracks.

| Fonte | Justificativa |
|---|---|
| Humano | The worker is either a man or a woman, not both. |
| Haiku | The premise specifies that the person doing maintenance on the tracks is a man, so the same scene cannot also feature a woman performing that work in the way the hypothesis describes. Because both sentences describe the same activity on the same tracks but assign it to different people, the hypothesis cannot be true if the premise is. |
| Sonnet | The premise describes a man doing the work on the tracks, while the hypothesis says a woman is doing it. Assuming both describe the same scene, the worker can't be both a man and a woman, so the hypothesis can't be true if the premise is. |
| **Qwen E** | The premise specifies a man performing maintenance, which contradicts the hypothesis claiming it is a woman doing the work on those tracks. |

## 676 · contradiction

- **P:** Three people each lead one camel with riders in a silhouetted line across sand dunes and a gray sky.
- **H:** A group of people getting ready to go for a swim in a lake.

| Fonte | Justificativa |
|---|---|
| Humano | The people can not be going across sand dunes if they are swimming in a lake |
| Haiku | The premise describes people leading camels across desert dunes, a dry, land-based scene, while the hypothesis describes people preparing to swim in a lake, an entirely different setting and activity. If the premise is true, the people are walking camels over sand, so they cannot simultaneously be getting ready to swim in a lake. |
| Sonnet | The premise describes people leading camels across sand dunes under a gray sky, which is a desert setting. The hypothesis puts people at a lake preparing to swim, and these two scenes cannot be the same one. |
| **Qwen E** | Leading camels across sand dunes requires a desert setting, whereas preparing to swim in a lake requires being near water. |

## 986 · contradiction

- **P:** A person wearing a robe and a pointed hat is holding a basket of bananas.
- **H:** A person is wearing a flat hat.

| Fonte | Justificativa |
|---|---|
| Humano | If someone is wearing a pointed hat, it would not be a flat hat. |
| Haiku | The premise specifies that the person's hat is pointed, so it cannot also be flat; a single hat cannot be both at the same time. The hypothesis therefore describes an incompatible version of the same scene. |
| Sonnet | The premise says the person's hat is pointed, while the hypothesis says it is flat. Since a single hat can't be both pointed and flat, and both sentences describe the same person, the hypothesis can't be true if the premise is. |
| **Qwen E** | Wearing a pointed hat and wearing a flat hat describe mutually exclusive headwear styles that cannot be true for the same person simultaneously. |

## 793 · contradiction

- **P:** Elderly woman with green sweater picking out produce in outdoor market.
- **H:** The elderly lady is dead in a coffin

| Fonte | Justificativa |
|---|---|
| Humano | elderly lady cannot be dead and picking out produce at the same time |
| Haiku | The premise describes an elderly woman actively shopping for produce at a market, which means she is alive and moving about. The hypothesis claims she is dead in a coffin, so both cannot be true of the same scene at the same time. |
| Sonnet | The premise describes the woman as actively picking out produce at an outdoor market, which means she is alive and engaged in a task. The hypothesis says she is dead in a coffin, and she cannot be both at once in the same scene. |
| **Qwen E** | Picking out produce requires a living person to be active in a market, which is impossible if she were already dead inside a coffin. |

## 932 · contradiction

- **P:** A white dog is chasing a stuffed animal being pulled on a string.
- **H:** the animal is sleeping

| Fonte | Justificativa |
|---|---|
| Humano | the animal is either sleeping or chasing a stuffed animal being pulled on a string. |
| Haiku | The premise describes the stuffed animal being pulled on a string and chased, which means it is moving and active, so it cannot simultaneously be sleeping. The two descriptions of the animal's state are incompatible within the same scene. |
| Sonnet | The premise describes a dog actively chasing a stuffed animal that is being pulled on a string, so the toy is in motion. The hypothesis says the animal is sleeping, which can't be true of the same scene, since a toy being pulled and chased is not sleeping. (And if "the animal" meant the dog, it couldn't be sleeping while chasing.) |
| **Qwen E** | A dog actively chasing a toy requires it to be moving, whereas sleeping animals are stationary and unaware. |
