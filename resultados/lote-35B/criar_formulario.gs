// Gerado por montar_google_forms.py: cria o formulario da leitura cega na sua conta Google.
// Como usar: script.google.com > Novo projeto > colar este arquivo > Executar criarFormulario > permitir acesso.
const DADOS = {
 "title": "Avaliação de justificativas de inferência textual",
 "description": "Obrigado por ajudar! São 50 itens, uns 40 minutos no total.\n\nCada item tem duas frases em inglês, uma PREMISSA (uma cena, sempre tomada como verdade) e uma HIPÓTESE, o RÓTULO que diz como elas se relacionam e uma JUSTIFICATIVA que explica esse rótulo. Sua tarefa é julgar a justificativa, não o rótulo.\n\nOs três rótulos:\n• implicação: a hipótese decorre da premissa.\n• contradição: a hipótese não pode ser verdade se a premissa for.\n• neutro: a hipótese é possível, mas a premissa não garante nem nega.\n\nImportante: você pode discordar do rótulo, mas finja que ele está certo ao julgar a justificativa. Algumas frases vêm em minúscula por erro; ignore isso.\n\nA rubrica é a de Wiegreffe et al. (2022), NAACL. Os exemplos da próxima página são os das instruções originais deles, traduzidos.",
 "examples": [
  [
   "Exemplo principal (todas as respostas)",
   "Premissa: A person on a horse jumps over a broken down airplane.\nHipótese: A person is at a diner, ordering an omelette.\nRótulo: contradição\nJustificativa: one cannot be on a jumping horse while at a diner ordering food.\n\n• Informação nova? Sim: diz que estar num cavalo saltando torna impossível estar, ao mesmo tempo, num restaurante.\n• Relevante para o rótulo? Sim: sustenta a contradição.\n• Quantidade? Suficiente: explica a relação sem nada a mais ou fora do assunto."
  ],
  [
   "Mais exemplos (mesmo par, outras justificativas)",
   "Premissa: A person on a horse jumps over a broken down airplane.\nHipótese: A person is training his horse for a competition.\nRótulo: neutro\n\nInformação nova?\n• \"A person is training over a broken down airplane.\" → Não: só repete partes da premissa e da hipótese.\n• \"people ride horses for many reasons, including to train them, but also for fun and for transportation.\" → Sim: traz o fato de que se monta a cavalo por vários motivos, com exemplos.\n\nRelevante para o rótulo?\n• A mesma frase dos vários motivos → Sim: explica o neutro.\n• \"a person jumping on a horse is training the horse.\" → Não: explica a implicação, que não é o rótulo dado.\n\nQuantidade?\n• \"the person is not necessarily training his horse.\" → Pouca: falta dizer por que saltar a cavalo pode ser outra coisa além de treinar.\n• A frase dos vários motivos → Suficiente.\n• A frase dos vários motivos seguida de um parágrafo sobre cavalos na colonização do Oeste americano → Demais: frases desnecessárias, informação sobrando."
  ]
 ],
 "questions": [
  [
   "Traz informação nova?",
   "Fatos, informação ou raciocínio que não estão na premissa nem na hipótese.",
   [
    "Sim",
    "Não"
   ]
  ],
  [
   "A informação é relevante para justificar o rótulo dado?",
   "",
   [
    "Sim",
    "Não"
   ]
  ],
  [
   "Quanta informação ela traz para justificar o rótulo?",
   "",
   [
    "Pouca",
    "Suficiente",
    "Demais"
   ]
  ],
  [
   "No geral, você aceitaria essa justificativa?",
   "",
   [
    "Sim",
    "Não"
   ]
  ]
 ],
 "items": [
  {
   "title": "Item 1 de 50",
   "text": "Premissa: A bartender pours a frothy drink into a tall glass.\nHipótese: The bartender is a man.\nRótulo: neutro\n\nJustificativa: Bartenders can be men or women, so the gender is not specified by the action of pouring a drink into a glass."
  },
  {
   "title": "Item 2 de 50",
   "text": "Premissa: A man in a hard hat looks intimidated.\nHipótese: He exclaims that he's done with this work, sprouts wings, and flies away.\nRótulo: contradição\n\nJustificativa: While a hard hat intimidates him, it does not magically give the man wings."
  },
  {
   "title": "Item 3 de 50",
   "text": "Premissa: Two men stand on stairs with an assortment of chairs and a woven basket in the foreground.\nHipótese: The basket is woven.\nRótulo: implicação\n\nJustificativa: Only weavers are seen weaving a basket."
  },
  {
   "title": "Item 4 de 50",
   "text": "Premissa: Three men are sitting outside on chairs with red seats.\nHipótese: Men are having a conversation outside.\nRótulo: neutro\n\nJustificativa: Men sitting outside does not necessarily mean they are having a conversation."
  },
  {
   "title": "Item 5 de 50",
   "text": "Premissa: A man in an orange shirt and yellow hard hat walks on a road.\nHipótese: A worker sits in a cubicle.\nRótulo: contradição\n\nJustificativa: Walking on a road requires being outdoors and moving, while sitting in a cubicle implies being indoors and stationary."
  },
  {
   "title": "Item 6 de 50",
   "text": "Premissa: A man with his arm around a woman.\nHipótese: A man is with a woman.\nRótulo: implicação\n\nJustificativa: The two people are holding hands, or are at least in physical contact in some way, which is one simple definition of the word \"with\"."
  },
  {
   "title": "Item 7 de 50",
   "text": "Premissa: three army men with guns.\nHipótese: Three men in uniform.\nRótulo: implicação\n\nJustificativa: Army men are soldiers who wear uniforms as part of their official attire, so seeing them implies they are dressed in these standard military garments."
  },
  {
   "title": "Item 8 de 50",
   "text": "Premissa: A crowd watching air balloons at night.\nHipótese: People are watching airplanes at 10:00 a.m.\nRótulo: contradição\n\nJustificativa: Night occurs after sunset, while 10:00 a.m. is during daylight hours; these distinct times cannot exist simultaneously in the same moment."
  },
  {
   "title": "Item 9 de 50",
   "text": "Premissa: A little boy playing with two rubber chickens.\nHipótese: The boy is outdoors.\nRótulo: neutro\n\nJustificativa: One cannot be playing with rubber chickens outdoors at the same time."
  },
  {
   "title": "Item 10 de 50",
   "text": "Premissa: four husky dogs are pulling a sled in a race through the snow guided by a man wearing number eleven.\nHipótese: four husky dogs are not pulling a sled\nRótulo: contradição\n\nJustificativa: Pulling a sled is an active physical task that requires engagement, whereas not pulling implies inactivity or absence of force, making both states impossible simultaneously."
  },
  {
   "title": "Item 11 de 50",
   "text": "Premissa: A man is playing a drum as a crowd of people are walking by.\nHipótese: People tip the man playing drums\nRótulo: neutro\n\nJustificativa: People walk by without stopping to listen or give money, so they may not notice the performance or choose not to support it financially."
  },
  {
   "title": "Item 12 de 50",
   "text": "Premissa: Four men and a woman sit at a conference table covered in a white sheet, with beverages in front of them and one has a microphone.\nHipótese: Some people are drinking.\nRótulo: neutro\n\nJustificativa: Beverages are present but may be untouched or for others; sitting and speaking do not guarantee consumption is occurring simultaneously."
  },
  {
   "title": "Item 13 de 50",
   "text": "Premissa: Three workers, with life vests and hard hats, on a boat hanging from cables over water.\nHipótese: Three lifeguards are haning from the boar, trying to save the dog from drowning.\nRótulo: neutro\n\nJustificativa: The workers are not lifeguards, and they are not trying to save the dog."
  },
  {
   "title": "Item 14 de 50",
   "text": "Premissa: Four cheerleaders in a squad walk along a football field.\nHipótese: There are two girls and two boys.\nRótulo: neutro\n\nJustificativa: Cheerleading squads can consist entirely of girls or boys, so four cheerleaders do not necessarily include both genders."
  },
  {
   "title": "Item 15 de 50",
   "text": "Premissa: A man is watching a woman bowl while another woman smiles.\nHipótese: A man watches a women play basketball while a women smiles.\nRótulo: contradição\n\nJustificativa: Bowling requires a lane and ball, whereas basketball is played on a court with a hoop; these are distinct activities that cannot occur simultaneously for the same people."
  },
  {
   "title": "Item 16 de 50",
   "text": "Premissa: A little boy is sitting in front of a fireplace next to a Ginger bread house.\nHipótese: The boy is small enough to fit inside the gingerbread house\nRótulo: contradição\n\nJustificativa: Sitting in front of a fireplace implies being outside the house structure, while fitting inside requires being within its boundaries, making both positions mutually exclusive simultaneously."
  },
  {
   "title": "Item 17 de 50",
   "text": "Premissa: Two men are playing during a basketball game.\nHipótese: Two men are playing.\nRótulo: implicação\n\nJustificativa: Only two men are playing in a basketball game. The two men must both be playing for that occur."
  },
  {
   "title": "Item 18 de 50",
   "text": "Premissa: Several women wearing dresses dance in the forest.\nHipótese: The women are older\nRótulo: neutro\n\nJustificativa: Dresses are worn by a variety of people of various ages."
  },
  {
   "title": "Item 19 de 50",
   "text": "Premissa: A person with braided hair and a gray sweatshirt covers his mouth and sits in a purple chair.\nHipótese: A man sits in a purple chair.\nRótulo: implicação\n\nJustificativa: If a man has braided hair and is sitting in a purple chair, then he is sitting in a purple chair."
  },
  {
   "title": "Item 20 de 50",
   "text": "Premissa: Girl wearing black shops in a supermarket.\nHipótese: The girl wearing black sometimes shops in a supermarket.\nRótulo: neutro\n\nJustificativa: Wearing black is a temporary state, while \"sometimes\" implies a recurring habit or general characteristic that cannot be definitively inferred from a single instance of observation."
  },
  {
   "title": "Item 21 de 50",
   "text": "Premissa: Two men work on a truck carrying cargo.\nHipótese: Two men are working on a truck and the truck goes out of gear.\nRótulo: neutro\n\nJustificativa: A truck can have cargo without having mechanical issues, as working on it doesn't imply a specific malfunction like going out of gear."
  },
  {
   "title": "Item 22 de 50",
   "text": "Premissa: One man in a baseball cap is watching a man in glasses paint watches.\nHipótese: A man is holding a paintbrush.\nRótulo: neutro\n\nJustificativa: Painting can be done with spray cans or rollers, so holding a brush is not required for the act of painting."
  },
  {
   "title": "Item 23 de 50",
   "text": "Premissa: A band is playing under a tent while people watch them play from chairs several yards away.\nHipótese: The band is playing at a wedding ceremony.\nRótulo: neutro\n\nJustificativa: Bands perform under tents at festivals, parties, and community events, so this setting does not exclusively indicate a wedding ceremony."
  },
  {
   "title": "Item 24 de 50",
   "text": "Premissa: A young boy looks on as a man performs the guitar on the street while sitting on a bench.\nHipótese: The young boy is watching a hockey game.\nRótulo: contradição\n\nJustificativa: It doesn't make sense for a young boy to be watching a hockey game."
  },
  {
   "title": "Item 25 de 50",
   "text": "Premissa: A young woman wearing a yellow sweater and black pants is ice skating outdoors.\nHipótese: the woman is cooking in the kitchen\nRótulo: contradição\n\nJustificativa: While a woman (or man) could be in the kitchen while ice skating, most people do not spend significant amounts of time in the kitchen while wearing such cold weather clothing, especially outdoors. Otherwise, it would severely hamper their ability to enjoy the"
  },
  {
   "title": "Item 26 de 50",
   "text": "Premissa: A small white dog climbs over a log.\nHipótese: An animal is near a log.\nRótulo: implicação\n\nJustificativa: A dog is an animal, and climbing over a log implies it is positioned adjacent to or on top of the log."
  },
  {
   "title": "Item 27 de 50",
   "text": "Premissa: Two wrestlers in an intense match.\nHipótese: Two wrestlers are competing and are brothers.\nRótulo: neutro\n\nJustificativa: Men can be friends and/or wrestling partners without having any relationship outside of wrestling."
  },
  {
   "title": "Item 28 de 50",
   "text": "Premissa: A woman walks toward a janitor that's wearing a raincoat and pushing a cleaning cart.\nHipótese: A woman is walking approaching a janitor.\nRótulo: implicação\n\nJustificativa: Walking toward someone means getting closer to them, which is the definition of approaching, so the woman is approaching the janitor."
  },
  {
   "title": "Item 29 de 50",
   "text": "Premissa: Colorful rings spraying water at little girl wearing swimsuit.\nHipótese: The child is playing.\nRótulo: implicação\n\nJustificativa: The girl is playing with the rings and the water spraying out of them, the water."
  },
  {
   "title": "Item 30 de 50",
   "text": "Premissa: A female politician is wearing a green jacket and holding hands with a man.\nHipótese: There are two people in this picture\nRótulo: implicação\n\nJustificativa: A female politician and a man constitute two distinct individuals, confirming that two people are present in the scene."
  },
  {
   "title": "Item 31 de 50",
   "text": "Premissa: A few children are rollerblading across a track, seemingly chasing each other.\nHipótese: There are kids outside.\nRótulo: implicação\n\nJustificativa: Children are kids, and rollerblading on a track typically happens outdoors rather than indoors, implying they are outside."
  },
  {
   "title": "Item 32 de 50",
   "text": "Premissa: A man on a yellow and green surfboard near shore.\nHipótese: A man on a surfboard near shore.\nRótulo: implicação\n\nJustificativa: The yellow and green surfboard is a specific type of surfboard, so a man on it is necessarily a man on a surfboard near shore."
  },
  {
   "title": "Item 33 de 50",
   "text": "Premissa: An Asian woman dressed in a colorful outfit laughing.\nHipótese: The woman is not laughing.\nRótulo: implicação\n\nJustificativa: If a woman is dressed in a colorful outfit, she is likely not laughing."
  },
  {
   "title": "Item 34 de 50",
   "text": "Premissa: A big outdoor market along a fence.\nHipótese: An empty field.\nRótulo: contradição\n\nJustificativa: A market involves many people and stalls, while an empty field lacks such presence, making them mutually exclusive states for the same location."
  },
  {
   "title": "Item 35 de 50",
   "text": "Premissa: A young boy plays a video game in a McDonald's restaurant.\nHipótese: A boy is sitting inside a building playing a game.\nRótulo: implicação\n\nJustificativa: McDonald’s is an indoor establishment, and playing video games typically involves sitting down to use the console or device comfortably."
  },
  {
   "title": "Item 36 de 50",
   "text": "Premissa: A man in a white shirt is walking across the street.\nHipótese: A guy crosses the street to enter the bar.\nRótulo: neutro\n\nJustificativa: A man and a guy are synonyms, but walking across the street does not specify the destination is a bar; he could be going anywhere."
  },
  {
   "title": "Item 37 de 50",
   "text": "Premissa: A group of four children poke at two small turtles in the grass.\nHipótese: A group of kids poked at the two small turtles.\nRótulo: implicação\n\nJustificativa: If a group of kids poked at the turtles, then the kids must have poked at the turtles."
  },
  {
   "title": "Item 38 de 50",
   "text": "Premissa: A large group of people populate a dimly lit room.\nHipótese: A group of people are in a room.\nRótulo: implicação\n\nJustificativa: The default is that groups of people are likely to occupy a room, and so predicting that the group of people are in the room is correct."
  },
  {
   "title": "Item 39 de 50",
   "text": "Premissa: People look on to a parking lot full of motorcycles.\nHipótese: People are looking at motorcycles.\nRótulo: implicação\n\nJustificativa: Looking at a parking lot full of motorcycles means directing attention to its contents, which are motorcycles."
  },
  {
   "title": "Item 40 de 50",
   "text": "Premissa: The football player prepares to kick the ball.\nHipótese: The quarterback is throwing the football.\nRótulo: contradição\n\nJustificativa: When you \"throw the football,\" you don't kick the ball (emphasizing throwing the ball)! This question was poorly constructed. A better question would be something along the lines of \"The quarterback is performing a passing technique..."
  },
  {
   "title": "Item 41 de 50",
   "text": "Premissa: two girls wearing a yellow shirt, one wearing a green shirt, and the last wearing a pink are each looking to the side\nHipótese: Three boys are looking at something to the side of them.\nRótulo: contradição\n\nJustificativa: Girls are female children, not boys; therefore, the subjects described as girls cannot simultaneously be three boys in the same moment."
  },
  {
   "title": "Item 42 de 50",
   "text": "Premissa: A man in a hard hat is wearing a blue shirt and blue jean overalls.\nHipótese: A man in a hard hat is wearing no shirt and blue jeans overalls.\nRótulo: contradição\n\nJustificativa: Wearing a blue shirt means having clothing on the upper body, while wearing no shirt means being bare-chested, which are mutually exclusive states."
  },
  {
   "title": "Item 43 de 50",
   "text": "Premissa: A crowd of people are gathered with their hands up in the air.\nHipótese: a crowd is at a concert\nRótulo: neutro\n\nJustificativa: Crowds raise hands to cheer at sports games, protests, and religious ceremonies, not exclusively at concerts."
  },
  {
   "title": "Item 44 de 50",
   "text": "Premissa: A tattooed woman clicking on a mouse on a desk.\nHipótese: A tattooed man clicking on a mouse on a desk.\nRótulo: contradição\n\nJustificativa: A tattooed woman and man cannot be the same person at the same time."
  },
  {
   "title": "Item 45 de 50",
   "text": "Premissa: Elderly women are sitting at a table.\nHipótese: old lady sitting in a table.\nRótulo: implicação\n\nJustificativa: Elderly women are old ladies, and sitting at a table implies an old lady is sitting there."
  },
  {
   "title": "Item 46 de 50",
   "text": "Premissa: A rollerblader pauses at the top of a skate ramp.\nHipótese: The skateboarder paused at the top of the pool to think of his next move.\nRótulo: contradição\n\nJustificativa: A rollerblader wears rollerblades, while a skateboarder uses a skateboard; these are distinct pieces of equipment that cannot be used simultaneously by the same person in the same moment."
  },
  {
   "title": "Item 47 de 50",
   "text": "Premissa: A man in a red headband an shirt is standing in front of a display case.\nHipótese: man is a girl\nRótulo: contradição\n\nJustificativa: A man in a red headband and shirt is not necessarily a girl."
  },
  {
   "title": "Item 48 de 50",
   "text": "Premissa: A few players show off their jousting skills in a gym.\nHipótese: The players are outside drinking lemonade.\nRótulo: contradição\n\nJustificativa: Jousting requires a large indoor space like a gym, whereas drinking lemonade outside implies being outdoors, making these locations mutually exclusive at the same moment."
  },
  {
   "title": "Item 49 de 50",
   "text": "Premissa: Two little girls, one with chocolate on her face, make faces.\nHipótese: Two young girls are making faces.\nRótulo: implicação\n\nJustificativa: Girls are young females, and the chocolate on her face is incidental detail that does not change their identity or action of making faces."
  },
  {
   "title": "Item 50 de 50",
   "text": "Premissa: People standing in front of a gray building with a sign that reads' Tickets Available Here'.\nHipótese: The people are wanting to buy concert tickets.\nRótulo: neutro\n\nJustificativa: People standing in front of a building do not necessarily mean wanted to buy concert tickets. More information is needed."
  }
 ]
};

function criarFormulario() {
  const form = FormApp.create(DADOS.title);
  form.setDescription(DADOS.description).setProgressBar(true).setCollectEmail(false);
  form.addTextItem().setTitle('Seu nome ou apelido').setRequired(true);
  form.addPageBreakItem().setTitle('Exemplos').setHelpText('Leia antes de começar.');
  DADOS.examples.forEach(e => form.addSectionHeaderItem().setTitle(e[0]).setHelpText(e[1]));
  DADOS.items.forEach(it => {
    form.addPageBreakItem().setTitle(it.title).setHelpText(it.text);
    DADOS.questions.forEach(q => {
      form.addMultipleChoiceItem().setTitle(q[0]).setHelpText(q[1]).setChoiceValues(q[2]).setRequired(true);
    });
    form.addTextItem().setTitle('Motivo (opcional)');
  });
  Logger.log('Editar: ' + form.getEditUrl());
  Logger.log('Responder (mande este aos amigos): ' + form.getPublishedUrl());
}
