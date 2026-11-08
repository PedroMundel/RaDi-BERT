# Candidatos a exemplo para a variante E (escolha 6: 2 por rótulo)

12 pares do dev do e-SNLI, só pares em que a hipótese acrescenta
ao menos duas palavras de conteúdo (pedem ponte de conhecimento). Para cada um: as 3 humanas e o Qwen
com os prompts A e D. Marque os 6 e escreva a versão final na linha **Sua versão**. Ela pode ser uma
das de cima, editada ou nova. Forma de referência (Wiegreffe 2022, Tab. 2): 1–2 frases, ~10–25
palavras, a ponte de conhecimento, sem nomear o rótulo.

**Linha "Claude (rascunho v2)" (21/10, a pedido do Pedro)** regras pra explicação, escrita com a régua que saiu da discussão de teoria da informação (`docs/2026-10-20-perdas-o-que-e-I-gradiente.md`):

1. **Só o que o rótulo não diz:** o fato de mundo que liga a premissa à hipótese. É a parte com I(R; X | Y) alto.
2. **Sem oração que reafirma a relação** ("so it is not raining", "which contradicts"). Pela conta, ela repete o rótulo e não ensina nada novo. O rótulo também não é nomeado: não porque prejudique, mas porque é redundante.
3. **Pouca cópia:** das frases do par, só as palavras que a ponte liga. Cópia também sobe o I, mas ensina a reconstruir a entrada, não o porquê.
4. **A mesma forma em todos:** uma frase declarativa de conhecimento geral, de 9 a 16 palavras, para reduzir a variação de estilo (H(R | X, Y)) e o custo.
5. **Por rótulo:** na implicação, cobrir o que a hipótese acrescenta (Camburu 2018); no neutro, uma alternativa concreta compatível com a premissa; na contradição, o fato que torna as duas incompatíveis -> trocado por: choque de lugar e ação no mesmo momento.

## 1. entailment · `373001890.jpg#1r1e`

- **P:** A man with a blue shirt and a woman with a red shirt, the woman smiles.
- **H:** Two people wearing shirts, one of them smiling.

| Fonte | Justificativa |
|---|---|
| Humano 1 | Man with woman implies two people. |
| Humano 2 | One man in a shirt plus one woman in a shirt equals two people wearing shirts. The woman is smiling so one person is smiling. |
| Humano 3 | Smiling woman is wearing red shirt. |
| Qwen A | The premise describes a specific scene involving two individuals wearing shirts where at least one is smiling, which directly satisfies the general conditions stated in the hypothesis. Therefore, if the detailed description in the premise is true, the broader summary in the hypothesis must also be true. |
| Qwen D | The premise confirms two people wearing shirts and states that the woman is smiling, which supports the hypothesis. |

- [ ] escolher
- **Sua versão:** A man and a woman make two people, and the smiling woman is one of them.

## 2. entailment · `2370481277.jpg#0r1e`

- **P:** A little boy in green is kicking a soccer ball and 6 boys in referee shirts are following him.
- **H:** There are many children around.

| Fonte | Justificativa |
|---|---|
| Humano 1 | There are many children around which is part of a little boy in green and 6 boys in referee shirts. |
| Humano 2 | Saying there are many children is a more general identifier of the group of 6 boys. |
| Humano 3 | There are many children because there is a boy in green as well as 6 boys following him. |
| Qwen A | The premise explicitly states there is one boy kicking a ball and six others in referee shirts following him, which confirms that multiple children are present as described in the hypothesis. Since the specific count of seven boys satisfies the general condition of "many children," the truth of the premise guarantees the truth of the hypothesis. |
| Qwen D | The presence of a boy and six other boys confirms there are many children. |

- [ ] escolher
- **Sua versão:** Boys are children, and seven of them together make a large group.

## 3. entailment · `2723024306.jpg#3r1e`

- **P:** Man builds detailed sand castle on the beach.
- **H:** An adult is working with sand.

| Fonte | Justificativa |
|---|---|
| Humano 1 | A man is an adult, and a sand castle is made of sand. |
| Humano 2 | A man who builds a sand castle is an adult working with sand. |
| Humano 3 | If a man builds a sand castle, logically the man is working with sand, as that's what you make sand castles out of. |
| Qwen A | Building a detailed sand castle inherently requires an adult to manipulate and work with sand, making the hypothesis a necessary consequence of the premise. Since the action described in the premise guarantees that the condition in the hypothesis is occurring, the relationship holds true. |
| Qwen D | The premise states a man is building a sand castle, which implies an adult is working with sand. |

- [ ] escolher
- **Sua versão:** A man is an adult, and sand castles are built out of sand.

## 4. entailment · `232501417.jpg#0r1e`

- **P:** A band is playing on stage at a concert and the attendants are dancing to the music.
- **H:** A band is playing while people dance.

| Fonte | Justificativa |
|---|---|
| Humano 1 | Attendants are people, so if they are dancing while a band is playing then that is the same as saying people dance while a band is playing. |
| Humano 2 | The band is playing while people are dancing to their music. |
| Humano 3 | A band is playing for people in a concert. |
| Qwen A | The hypothesis accurately summarizes the premise by stating that a band is playing and people are dancing, which directly corresponds to the specific details of attendants dancing to the music at a concert. Since the presence of "attendants" confirms that "people" are present and dancing while the band plays, the truth of the premise guarantees the truth of the hypothesis. |
| Qwen D | The premise confirms a band plays while attendants dance, which supports the hypothesis that people are dancing to the music. |

- [ ] escolher
- **Sua versão:** Concert attendants are people, and dancing to a band’s music happens while it plays.

## 5. neutral · `189521182.jpg#4r1n`

- **P:** girl sitting in fire for a show
- **H:** The girl is an employee of the circus.

| Fonte | Justificativa |
|---|---|
| Humano 1 | she could have been a daredevil and not working for the circus. |
| Humano 2 | Sitting in fire does not necessarily mean she is an employee of the circus. |
| Humano 3 | Just because sitting in fire does not mean an employee of the circus. |
| Qwen A | The premise states that a girl is sitting in fire for a show, which could be part of a circus performance but could also belong to a theater production, street act, or other entertainment venue. Therefore, while she might be a circus employee, the information provided does not guarantee her specific employment role. |
| Qwen D | The premise describes a girl performing but provides no information about her employment status as a circus employee. |

- [ ] escolher
- **Sua versão:** Fire acts also happen at street shows and festivals, not only in circuses.

## 6. neutral · `4584266249.jpg#1r1e`

- **P:** Two Asian women wear sandals, long silk robes and hold umbrellas.
- **H:** Two women stand in the rain

| Fonte | Justificativa |
|---|---|
| Humano 1 | There doesn't need to be rain to hold an umbrella. |
| Humano 2 | Just because the women have umbrellas doesn't mean they're in the rain. |
| Humano 3 | Two women wear sandals, long silk robes and hold umbrellas don't necessarily imply that the women are standing in the rain. |
| Qwen A | Although holding umbrellas and wearing sandals suggests it might be raining, the premise does not explicitly state that it is currently raining, as these items could be used for sun protection or fashion. Therefore, while the hypothesis is plausible, it cannot be confirmed solely based on the provided information. |
| Qwen D | Wearing umbrellas does not prove it is raining, as they could simply be carrying them for sun protection or convenience. |

- [ ] escolher
- **Sua versão:** Umbrellas are also carried for shade on sunny days.

## 7. neutral · `3021780428.jpg#0r1n`

- **P:** A young boy is pushing someone with a broken foot into the hospital.
- **H:** The person got hurt playing basketball.

| Fonte | Justificativa |
|---|---|
| Humano 1 | pushing someone with a broken foot into the hospital  got hurt playing basketball. |
| Humano 2 | Just because someone has a broken foot does not mean it was from playing basketball. |
| Humano 3 | Just because a young boy is pushing someone with a broken foot into the hospital does not mean the person got hurt. |
| Qwen A | The premise states that the boy is pushing someone with a broken foot to the hospital, but it does not specify how the injury occurred. Therefore, we cannot determine from the given information whether the person was hurt while playing basketball or through some other means. |
| Qwen D | The premise does not specify how the broken foot occurred, so the cause cannot be confirmed as playing basketball. |

- [ ] escolher
- **Sua versão:** Feet get broken in falls, car accidents and many other sports.

## 8. neutral · `2587625325.jpg#0r1n`

- **P:** A group of men in fatigues eat at a fast food restaurant.
- **H:** There is a group of men who are all friends.

| Fonte | Justificativa |
|---|---|
| Humano 1 | Not all those who dress alike are friends. |
| Humano 2 | We have no idea if they are friends, they could be anyone. |
| Humano 3 | Not all group of men are friends.. |
| Qwen A | The premise states that a group of men are eating together, but it does not provide any information about their personal relationships. Therefore, we cannot determine if they are all friends based solely on the fact that they are sharing a meal. |
| Qwen D | Eating at a restaurant does not prove the men are friends. |

- [ ] escolher
- **Sua versão:** Soldiers from the same unit eat together on duty whether or not they are friends.

## 9. contradiction · `2998185688.jpg#0r1c`

- **P:** Several horsemen are riding past each other carrying flags.
- **H:** The horses are in their stables.

| Fonte | Justificativa |
|---|---|
| Humano 1 | Horse in stables cannot be riding. |
| Humano 2 | Horses are not horsemen.  If horsemen are riding past horses are not in their stables. |
| Humano 3 | The horses cannot be riding past each other and in their stables. |
| Qwen A | The premise describes horsemen actively riding horses past each other, which implies the animals are moving outdoors, whereas the hypothesis claims they are stationary inside stables; these two scenarios cannot both be true at the same time. |
| Qwen D | Horsemen riding past each other contradicts horses being inside stables because they are actively moving outdoors. |

- [ ] escolher
- **Sua versão:** Riding past each other requires the horses to be out and moving, while being in their stables means being confined in them.

## 10. contradiction · `4573958272.jpg#2r1n`

- **P:** A rather tall man and a woman wearing a red top and blue jeans waiting at on the sidewalk.
- **H:** The man and woman are walking to the pharmacy.

| Fonte | Justificativa |
|---|---|
| Humano 1 | The man and the woman may either be walking or waiting. |
| Humano 2 | One cannot walk  while waiting on the sidewalk. |
| Humano 3 | The subjects are either walking to the pharmacy or are waiting on the sidewalk. |
| Qwen A | The premise states that the individuals are waiting on the sidewalk, which contradicts the hypothesis claiming they are actively walking. Since one cannot be simultaneously stationary while waiting and moving to a specific destination like a pharmacy, the two statements describe incompatible actions. |
| Qwen D | The premise states they are waiting on the sidewalk, which contradicts the hypothesis that they are walking to a pharmacy. |

- [ ] escolher
- **Sua versão:** Waiting on the sidewalk requires staying in one spot, while walking to the pharmacy means moving away from it.

## 11. contradiction · `372559387.jpg#0r1c`

- **P:** A crowd standing in a room with their backs to the camera.
- **H:** The crowd in the room is smiling at the camera man.

| Fonte | Justificativa |
|---|---|
| Humano 1 | It is assumed the camera man is pointing the camera away from him. In this case the crowd cannot have their back to the camera and smile at the camera man operating it |
| Humano 2 | The crowd either smiling at the camera man or have their backs to the camera.. |
| Humano 3 | If they are smiling at the camera man that implies facing the camera and therefore cannot have their backs are to the camera. |
| Qwen A | The premise states that the crowd has their backs to the camera, which physically prevents them from looking at or smiling at the camera man as claimed in the hypothesis. Therefore, the two statements describe mutually exclusive situations regarding the direction of the crowd's attention. |
| Qwen D | Since the crowd has their backs to the camera, they cannot be smiling at the camera man. |

- [ ] escolher
- **Sua versão:** A crowd smiling at the cameraman requires facing the camera he stands behind, while having their backs to the camera means facing away from him.

## 12. contradiction · `2932519416.jpg#3r1c`

- **P:** A biker wearing a white t-shirt is jumping over dirt hills.
- **H:** A biker climbs a tree in a shirt.

| Fonte | Justificativa |
|---|---|
| Humano 1 | Jumping is not the same as climbing. |
| Humano 2 | The biker can't climb a tree and jump over dirt hills at the same time. |
| Humano 3 | If the biker is jumping he cannot be climbing at the same time. |
| Qwen A | The premise describes a biker performing an action on the ground (jumping over dirt hills), which directly conflicts with the hypothesis stating that the same biker is climbing a tree. Since a person cannot simultaneously be jumping over hills and climbing a tree, the two statements describe mutually exclusive scenarios. |
| Qwen D | The premise states the biker is jumping over dirt hills, which contradicts the hypothesis that they are climbing a tree. |

- [ ] escolher
- **Sua versão:** Jumping over dirt hills requires being on the ground, while climbing a tree means being up in it.
