// Gerado por montar_google_forms.py: cria o formulario da leitura cega na sua conta Google.
// Como usar: script.google.com > Novo projeto > colar este arquivo > Executar criarFormulario > permitir acesso.
const DADOS = {
 "title": "Avaliação de justificativas de inferência textual (em português)",
 "description": "Obrigado por ajudar! São 50 itens, uns 40 minutos no total.\n\nCada item tem duas frases, uma PREMISSA (uma cena, sempre tomada como verdade) e uma HIPÓTESE, o RÓTULO que diz como elas se relacionam e uma JUSTIFICATIVA que explica esse rótulo. Sua tarefa é julgar a justificativa, não o rótulo.\n\nOs três rótulos:\n• implicação: a hipótese decorre da premissa.\n• contradição: a hipótese não pode ser verdade se a premissa for.\n• neutro: a hipótese é possível, mas a premissa não garante nem nega.\n\nImportante: você pode discordar do rótulo, mas finja que ele está certo ao julgar a justificativa. Algumas frases vêm em minúscula por erro; ignore isso.\n\nA rubrica é a de Wiegreffe et al. (2022), NAACL. Os exemplos da próxima página são os das instruções originais deles, traduzidos.\n\nVersão em português: as frases foram traduzidas do inglês, mantendo os erros e as frases estranhas do original de propósito.",
 "examples": [
  [
   "Exemplo principal (todas as respostas)",
   "Premissa: Uma pessoa a cavalo salta por cima de um avião abandonado.\nHipótese: Uma pessoa está numa lanchonete, pedindo uma omelete.\nRótulo: contradição\nJustificativa: não dá para estar num cavalo saltando enquanto se está numa lanchonete pedindo comida.\n\n• Informação nova? Sim: diz que estar num cavalo saltando torna impossível estar, ao mesmo tempo, numa lanchonete.\n• Relevante para o rótulo? Sim: sustenta a contradição.\n• Quantidade? Suficiente: explica a relação sem nada a mais ou fora do assunto."
  ],
  [
   "Mais exemplos (mesmo par, outras justificativas)",
   "Premissa: Uma pessoa a cavalo salta por cima de um avião abandonado.\nHipótese: Uma pessoa está treinando o cavalo para uma competição.\nRótulo: neutro\n\nInformação nova?\n• \"Uma pessoa está treinando por cima de um avião abandonado.\" → Não: só repete partes da premissa e da hipótese.\n• \"as pessoas andam a cavalo por muitos motivos, inclusive para treiná-los, mas também por diversão e como meio de transporte.\" → Sim: traz o fato de que se monta a cavalo por vários motivos, com exemplos.\n\nRelevante para o rótulo?\n• A mesma frase dos vários motivos → Sim: explica o neutro.\n• \"uma pessoa saltando a cavalo está treinando o cavalo.\" → Não: explica a implicação, que não é o rótulo dado.\n\nQuantidade?\n• \"a pessoa não está necessariamente treinando o cavalo.\" → Pouca: falta dizer por que saltar a cavalo pode ser outra coisa além de treinar.\n• A frase dos vários motivos → Suficiente.\n• A frase dos vários motivos seguida de um parágrafo sobre cavalos na colonização do Oeste americano → Demais: frases desnecessárias, informação sobrando."
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
   "text": "Premissa: Um bartender despeja uma bebida espumosa em um copo alto.\nHipótese: O bartender é um homem.\nRótulo: neutro\n\nJustificativa: Bartenders podem ser homens ou mulheres, então o gênero não é indicado pela ação de despejar uma bebida em um copo."
  },
  {
   "title": "Item 2 de 50",
   "text": "Premissa: Um homem de capacete de obra parece intimidado.\nHipótese: Ele exclama que cansou desse trabalho, cria asas e sai voando.\nRótulo: contradição\n\nJustificativa: Embora um capacete de obra o intimide, ele não dá asas ao homem por mágica."
  },
  {
   "title": "Item 3 de 50",
   "text": "Premissa: Dois homens estão de pé numa escada, com várias cadeiras e um cesto trançado em primeiro plano.\nHipótese: O cesto é trançado.\nRótulo: implicação\n\nJustificativa: Só tecelões são vistos trançando um cesto."
  },
  {
   "title": "Item 4 de 50",
   "text": "Premissa: Três homens estão sentados ao ar livre em cadeiras de assento vermelho.\nHipótese: Os homens estão conversando ao ar livre.\nRótulo: neutro\n\nJustificativa: Homens sentados ao ar livre não significa necessariamente que estejam conversando."
  },
  {
   "title": "Item 5 de 50",
   "text": "Premissa: Um homem de camisa laranja e capacete de obra amarelo anda por uma estrada.\nHipótese: Um trabalhador está sentado numa baia de escritório.\nRótulo: contradição\n\nJustificativa: Andar por uma estrada exige estar ao ar livre e em movimento, enquanto sentar numa baia de escritório implica estar num lugar fechado e parado."
  },
  {
   "title": "Item 6 de 50",
   "text": "Premissa: Um homem com o braço em volta de uma mulher.\nHipótese: Um homem está com uma mulher.\nRótulo: implicação\n\nJustificativa: As duas pessoas estão de mãos dadas, ou pelo menos em algum tipo de contato físico, que é uma definição simples da palavra \"com\"."
  },
  {
   "title": "Item 7 de 50",
   "text": "Premissa: três homens do exército com armas.\nHipótese: Três homens de uniforme.\nRótulo: implicação\n\nJustificativa: Homens do exército são soldados que usam uniforme como parte da vestimenta oficial, então vê-los implica que estão vestidos com essas roupas militares padrão."
  },
  {
   "title": "Item 8 de 50",
   "text": "Premissa: Uma multidão assistindo a balões à noite.\nHipótese: Pessoas estão assistindo a aviões às 10h da manhã.\nRótulo: contradição\n\nJustificativa: A noite vem depois do pôr do sol, enquanto 10h da manhã é durante o dia; esses momentos distintos não podem existir simultaneamente no mesmo instante."
  },
  {
   "title": "Item 9 de 50",
   "text": "Premissa: Um menininho brincando com duas galinhas de borracha.\nHipótese: O menino está ao ar livre.\nRótulo: neutro\n\nJustificativa: Não dá para estar brincando com galinhas de borracha ao ar livre ao mesmo tempo."
  },
  {
   "title": "Item 10 de 50",
   "text": "Premissa: quatro cães husky puxam um trenó numa corrida pela neve, guiados por um homem com o número onze.\nHipótese: quatro cães husky não estão puxando um trenó\nRótulo: contradição\n\nJustificativa: Puxar um trenó é uma tarefa física ativa que exige empenho, enquanto não puxar implica inatividade ou ausência de força, o que torna os dois estados impossíveis ao mesmo tempo."
  },
  {
   "title": "Item 11 de 50",
   "text": "Premissa: Um homem toca tambor enquanto uma multidão passa.\nHipótese: As pessoas dão gorjeta ao homem que toca tambor\nRótulo: neutro\n\nJustificativa: As pessoas passam sem parar para ouvir ou dar dinheiro, então podem não perceber a apresentação ou escolher não apoiá-la financeiramente."
  },
  {
   "title": "Item 12 de 50",
   "text": "Premissa: Quatro homens e uma mulher estão sentados a uma mesa de reunião coberta com um pano branco, com bebidas à frente, e um deles tem um microfone.\nHipótese: Algumas pessoas estão bebendo.\nRótulo: neutro\n\nJustificativa: As bebidas estão lá, mas podem estar intocadas ou ser para outros; estar sentado e falar não garante que alguém esteja bebendo ao mesmo tempo."
  },
  {
   "title": "Item 13 de 50",
   "text": "Premissa: Três trabalhadores, com coletes salva-vidas e capacetes, num barco pendurado por cabos sobre a água.\nHipótese: Três salva-vidas estão pendurados no barco, tentando salvar o cachorro de se afogar.\nRótulo: neutro\n\nJustificativa: Os trabalhadores não são salva-vidas, e não estão tentando salvar o cachorro."
  },
  {
   "title": "Item 14 de 50",
   "text": "Premissa: Quatro líderes de torcida de um grupo andam ao longo de um campo de futebol americano.\nHipótese: São duas meninas e dois meninos.\nRótulo: neutro\n\nJustificativa: Grupos de líderes de torcida podem ser formados só por meninas ou só por meninos, então quatro líderes de torcida não incluem necessariamente os dois gêneros."
  },
  {
   "title": "Item 15 de 50",
   "text": "Premissa: Um homem assiste a uma mulher jogar boliche enquanto outra mulher sorri.\nHipótese: Um homem assiste a uma mulher jogar basquete enquanto uma mulher sorri.\nRótulo: contradição\n\nJustificativa: Boliche exige uma pista e uma bola, enquanto basquete se joga numa quadra com cesta; são atividades distintas que não podem acontecer ao mesmo tempo para as mesmas pessoas."
  },
  {
   "title": "Item 16 de 50",
   "text": "Premissa: Um menininho está sentado diante de uma lareira, ao lado de uma casinha de gengibre.\nHipótese: O menino é pequeno o bastante para caber dentro da casinha de gengibre\nRótulo: contradição\n\nJustificativa: Estar sentado diante de uma lareira implica estar fora da estrutura da casa, enquanto caber dentro exige estar dentro dos limites dela, o que torna as duas posições mutuamente exclusivas ao mesmo tempo."
  },
  {
   "title": "Item 17 de 50",
   "text": "Premissa: Dois homens estão jogando durante uma partida de basquete.\nHipótese: Dois homens estão jogando.\nRótulo: implicação\n\nJustificativa: Só dois homens estão jogando numa partida de basquete. Os dois homens precisam estar jogando para que isso aconteça."
  },
  {
   "title": "Item 18 de 50",
   "text": "Premissa: Várias mulheres de vestido dançam na floresta.\nHipótese: As mulheres são mais velhas\nRótulo: neutro\n\nJustificativa: Vestidos são usados por uma variedade de pessoas de várias idades."
  },
  {
   "title": "Item 19 de 50",
   "text": "Premissa: Uma pessoa de cabelo trançado e moletom cinza cobre a boca e está sentada numa cadeira roxa.\nHipótese: Um homem está sentado numa cadeira roxa.\nRótulo: implicação\n\nJustificativa: Se um homem tem cabelo trançado e está sentado numa cadeira roxa, então ele está sentado numa cadeira roxa."
  },
  {
   "title": "Item 20 de 50",
   "text": "Premissa: Menina vestida de preto faz compras num supermercado.\nHipótese: A menina vestida de preto às vezes faz compras num supermercado.\nRótulo: neutro\n\nJustificativa: Estar vestida de preto é um estado temporário, enquanto \"às vezes\" implica um hábito recorrente ou uma característica geral que não pode ser inferida com certeza de uma única observação."
  },
  {
   "title": "Item 21 de 50",
   "text": "Premissa: Dois homens trabalham num caminhão que leva carga.\nHipótese: Dois homens estão trabalhando num caminhão e o caminhão sai da marcha.\nRótulo: neutro\n\nJustificativa: Um caminhão pode ter carga sem ter problemas mecânicos, já que trabalhar nele não implica um defeito específico como sair da marcha."
  },
  {
   "title": "Item 22 de 50",
   "text": "Premissa: Um homem de boné observa um homem de óculos pintar relógios.\nHipótese: Um homem está segurando um pincel.\nRótulo: neutro\n\nJustificativa: Pintar pode ser feito com spray ou rolo, então segurar um pincel não é necessário para o ato de pintar."
  },
  {
   "title": "Item 23 de 50",
   "text": "Premissa: Uma banda toca sob uma tenda enquanto pessoas a assistem de cadeiras a vários metros de distância.\nHipótese: A banda está tocando numa cerimônia de casamento.\nRótulo: neutro\n\nJustificativa: Bandas tocam sob tendas em festivais, festas e eventos comunitários, então esse cenário não indica exclusivamente uma cerimônia de casamento."
  },
  {
   "title": "Item 24 de 50",
   "text": "Premissa: Um menino observa um homem que toca violão na rua, sentado num banco.\nHipótese: O menino está assistindo a um jogo de hóquei.\nRótulo: contradição\n\nJustificativa: Não faz sentido um menino estar assistindo a um jogo de hóquei."
  },
  {
   "title": "Item 25 de 50",
   "text": "Premissa: Uma jovem de suéter amarelo e calça preta patina no gelo ao ar livre.\nHipótese: a mulher está cozinhando na cozinha\nRótulo: contradição\n\nJustificativa: Embora uma mulher (ou homem) pudesse estar na cozinha enquanto patina no gelo, a maioria das pessoas não passa muito tempo na cozinha usando roupas de frio assim, principalmente ao ar livre. Do contrário, isso atrapalharia muito a capacidade delas de aproveitar o"
  },
  {
   "title": "Item 26 de 50",
   "text": "Premissa: Um cachorrinho branco passa por cima de um tronco.\nHipótese: Um animal está perto de um tronco.\nRótulo: implicação\n\nJustificativa: Um cachorro é um animal, e passar por cima de um tronco implica que ele está ao lado ou em cima do tronco."
  },
  {
   "title": "Item 27 de 50",
   "text": "Premissa: Dois lutadores numa luta intensa.\nHipótese: Dois lutadores estão competindo e são irmãos.\nRótulo: neutro\n\nJustificativa: Homens podem ser amigos e/ou parceiros de luta sem ter nenhuma relação fora da luta."
  },
  {
   "title": "Item 28 de 50",
   "text": "Premissa: Uma mulher anda em direção a um faxineiro que usa capa de chuva e empurra um carrinho de limpeza.\nHipótese: Uma mulher está andando e se aproximando de um faxineiro.\nRótulo: implicação\n\nJustificativa: Andar em direção a alguém significa ficar mais perto dessa pessoa, que é a definição de se aproximar, então a mulher está se aproximando do faxineiro."
  },
  {
   "title": "Item 29 de 50",
   "text": "Premissa: Argolas coloridas jogando água numa menininha de maiô.\nHipótese: A criança está brincando.\nRótulo: implicação\n\nJustificativa: A menina está brincando com as argolas e com a água que sai delas, a água."
  },
  {
   "title": "Item 30 de 50",
   "text": "Premissa: Uma política está de jaqueta verde e de mãos dadas com um homem.\nHipótese: Há duas pessoas nesta foto\nRótulo: implicação\n\nJustificativa: Uma política e um homem são dois indivíduos distintos, o que confirma que há duas pessoas na cena."
  },
  {
   "title": "Item 31 de 50",
   "text": "Premissa: Algumas crianças andam de patins numa pista, parecendo correr umas atrás das outras.\nHipótese: Há garotos ao ar livre.\nRótulo: implicação\n\nJustificativa: Crianças são garotos, e andar de patins numa pista costuma acontecer ao ar livre, e não num lugar fechado, o que implica que elas estão ao ar livre."
  },
  {
   "title": "Item 32 de 50",
   "text": "Premissa: Um homem numa prancha de surfe amarela e verde perto da praia.\nHipótese: Um homem numa prancha de surfe perto da praia.\nRótulo: implicação\n\nJustificativa: A prancha amarela e verde é um tipo específico de prancha de surfe, então um homem nela é necessariamente um homem numa prancha de surfe perto da praia."
  },
  {
   "title": "Item 33 de 50",
   "text": "Premissa: Uma mulher asiática com uma roupa colorida rindo.\nHipótese: A mulher não está rindo.\nRótulo: implicação\n\nJustificativa: Se uma mulher está com uma roupa colorida, ela provavelmente não está rindo."
  },
  {
   "title": "Item 34 de 50",
   "text": "Premissa: Um grande mercado ao ar livre junto a uma cerca.\nHipótese: Um campo vazio.\nRótulo: contradição\n\nJustificativa: Um mercado envolve muitas pessoas e barracas, enquanto um campo vazio não tem essa presença, o que os torna estados mutuamente exclusivos para o mesmo lugar."
  },
  {
   "title": "Item 35 de 50",
   "text": "Premissa: Um menino joga videogame num restaurante McDonald's.\nHipótese: Um menino está sentado dentro de um prédio jogando um jogo.\nRótulo: implicação\n\nJustificativa: O McDonald's é um estabelecimento fechado, e jogar videogame costuma envolver sentar-se para usar o console ou o aparelho com conforto."
  },
  {
   "title": "Item 36 de 50",
   "text": "Premissa: Um homem de camisa branca está atravessando a rua.\nHipótese: Um cara atravessa a rua para entrar no bar.\nRótulo: neutro\n\nJustificativa: Homem e cara são sinônimos, mas atravessar a rua não especifica que o destino é um bar; ele poderia estar indo a qualquer lugar."
  },
  {
   "title": "Item 37 de 50",
   "text": "Premissa: Um grupo de quatro crianças cutuca duas tartaruguinhas na grama.\nHipótese: Um grupo de crianças cutucou as duas tartaruguinhas.\nRótulo: implicação\n\nJustificativa: Se um grupo de crianças cutucou as tartarugas, então as crianças devem ter cutucado as tartarugas."
  },
  {
   "title": "Item 38 de 50",
   "text": "Premissa: Um grande grupo de pessoas ocupa uma sala pouco iluminada.\nHipótese: Um grupo de pessoas está numa sala.\nRótulo: implicação\n\nJustificativa: O padrão é que grupos de pessoas provavelmente ocupem uma sala, então prever que o grupo de pessoas está na sala está correto."
  },
  {
   "title": "Item 39 de 50",
   "text": "Premissa: Pessoas olham para um estacionamento cheio de motos.\nHipótese: As pessoas estão olhando para motos.\nRótulo: implicação\n\nJustificativa: Olhar para um estacionamento cheio de motos significa voltar a atenção para o que há nele, que são motos."
  },
  {
   "title": "Item 40 de 50",
   "text": "Premissa: O jogador de futebol americano se prepara para chutar a bola.\nHipótese: O quarterback está lançando a bola.\nRótulo: contradição\n\nJustificativa: Quando você \"lança a bola\", você não chuta a bola (com ênfase em lançar a bola)! Esta pergunta foi mal construída. Uma pergunta melhor seria algo como \"O quarterback está executando uma técnica de passe..."
  },
  {
   "title": "Item 41 de 50",
   "text": "Premissa: duas meninas de camiseta amarela, uma de camiseta verde e a última de rosa estão olhando para o lado\nHipótese: Três meninos estão olhando para algo ao lado deles.\nRótulo: contradição\n\nJustificativa: Meninas são crianças do sexo feminino, não meninos; portanto, as pessoas descritas como meninas não podem ser ao mesmo tempo três meninos no mesmo instante."
  },
  {
   "title": "Item 42 de 50",
   "text": "Premissa: Um homem de capacete de obra está de camisa azul e macacão jeans.\nHipótese: Um homem de capacete de obra está sem camisa e de macacão jeans.\nRótulo: contradição\n\nJustificativa: Estar de camisa azul significa ter roupa no tronco, enquanto estar sem camisa significa estar de peito nu, que são estados mutuamente exclusivos."
  },
  {
   "title": "Item 43 de 50",
   "text": "Premissa: Uma multidão está reunida com as mãos para o alto.\nHipótese: uma multidão está num show\nRótulo: neutro\n\nJustificativa: Multidões levantam as mãos para torcer em jogos, protestos e cerimônias religiosas, não só em shows."
  },
  {
   "title": "Item 44 de 50",
   "text": "Premissa: Uma mulher tatuada clicando num mouse sobre uma mesa.\nHipótese: Um homem tatuado clicando num mouse sobre uma mesa.\nRótulo: contradição\n\nJustificativa: Uma mulher e um homem tatuados não podem ser a mesma pessoa ao mesmo tempo."
  },
  {
   "title": "Item 45 de 50",
   "text": "Premissa: Mulheres idosas estão sentadas a uma mesa.\nHipótese: senhora idosa sentada numa mesa.\nRótulo: implicação\n\nJustificativa: Mulheres idosas são senhoras idosas, e estar sentada a uma mesa implica que uma senhora idosa está sentada ali."
  },
  {
   "title": "Item 46 de 50",
   "text": "Premissa: Um patinador de patins em linha para no alto de uma rampa de skate.\nHipótese: O skatista parou no alto da piscina para pensar no próximo movimento.\nRótulo: contradição\n\nJustificativa: Um patinador usa patins em linha, enquanto um skatista usa skate; são equipamentos distintos que não podem ser usados ao mesmo tempo pela mesma pessoa no mesmo instante."
  },
  {
   "title": "Item 47 de 50",
   "text": "Premissa: Um homem de faixa vermelha na cabeça e camisa está de pé diante de uma vitrine.\nHipótese: homem é uma menina\nRótulo: contradição\n\nJustificativa: Um homem de faixa vermelha na cabeça e camisa não é necessariamente uma menina."
  },
  {
   "title": "Item 48 de 50",
   "text": "Premissa: Alguns jogadores exibem suas habilidades de justa num ginásio.\nHipótese: Os jogadores estão do lado de fora tomando limonada.\nRótulo: contradição\n\nJustificativa: A justa exige um grande espaço fechado, como um ginásio, enquanto tomar limonada do lado de fora implica estar ao ar livre, o que torna esses lugares mutuamente exclusivos no mesmo instante."
  },
  {
   "title": "Item 49 de 50",
   "text": "Premissa: Duas menininhas, uma com chocolate no rosto, fazem caretas.\nHipótese: Duas meninas pequenas estão fazendo caretas.\nRótulo: implicação\n\nJustificativa: Meninas são jovens do sexo feminino, e o chocolate no rosto é um detalhe secundário que não muda quem elas são nem a ação de fazer caretas."
  },
  {
   "title": "Item 50 de 50",
   "text": "Premissa: Pessoas de pé diante de um prédio cinza com uma placa que diz 'Ingressos à venda aqui'.\nHipótese: As pessoas querem comprar ingressos para um show.\nRótulo: neutro\n\nJustificativa: Pessoas de pé diante de um prédio não necessariamente significa querer comprar ingressos para um show. É preciso mais informação."
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
