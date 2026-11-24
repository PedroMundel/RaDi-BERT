# Ledger - termo de entrega da Semana 9 e documentos

Sources: mensagem do Pedro de 11/11 ("Vamos montar o termo de entrega. Esse vai precisar de MUITA documentação");
skill `termogate`; termo entregue da Semana 8 (`entrega/termos-entregues/Termo Semana 8.docx`); `HANDOFF.md` de
10/11 22h45; `docs/handoffs/2026-11-08-2251.md`; `resultados/rte-pequenos/leitura-grade.md`.

| # | Item | Source | Done when | Status | Evidence |
|---|---|---|---|---|---|
| 1 | Rascunho do termo da Semana 9 com Resumo, 6 itens, Planejamento, tabela de documentos e escolhas abertas | msg | `docs/residencia/termo-de-entrega-Semana-9.md` existe com as seções da skill | done | escrito 11/11 08h; Resumo copiado do termo entregue da S8 mais uma frase |
| 2 | `entrega/Replicacao do Agrawal no RTE.docx` (com o .md fonte ao lado) | msg ("MUITA documentação"); proposta do Claude | arquivo existe e o Pedro leu | done | docx gerado 11/11; redigido por agente a partir das leituras, conferido por amostra pelo Claude (MS-MARCO, calendário, small, e-SNLI, T5); o Pedro ainda não leu |
| 3 | `entrega/Marcas de Atencao e Destaque.docx` (com o .md fonte ao lado) | idem | arquivo existe e o Pedro leu | done | docx gerado 11/11; números das leituras de 10/11; o Pedro ainda não leu |
| 4 | Checagens da skill no termo final (números batem com os documentos entregues, todo .docx existe) | skill `termogate` | lista de checagens rodada depois dos documentos | done | 0,4754, 0,767, 0,73 e 0,56 batem com os documentos; citação com ano; 5 docx com data de 11/11; sem caractere proibido nos 4 .md |
| 5 | `entrega/O que Mudou em Relacao ao Agrawal.docx` (curto, com o .md fonte) | Pedro 11/11 ("criar outros docs das partes mais importantes"); lista do Claude | arquivo existe; números batem com as leituras | done | docx gerado 11/11, 789 palavras |
| 6 | `entrega/Exemplos do Destaque.docx` (20 pares coloridos) | idem | arquivo existe com 20 pares | done | docx gerado 11/11: 20 pares, 193 palavras marcadas, 131 e 62 coincidências |
| 7 | `entrega/Criterios Escritos Antes dos Testes.docx` (curto, com o .md fonte) | idem | arquivo existe; cada critério bate com o plano | done | docx gerado 11/11, 657 palavras; critérios copiados do plano, seções 3, 8 e 9 |
| 8 | O Pedro lê os cinco documentos antes de linkar | regra de procedência do projeto | declaração dele | blocked | depende do Pedro |
| 9 | Item do termo sobre a placa-mãe, o computador do amigo por SSH, o atraso e o auxílio pesado de LLM | Pedro 11/11 ("adiciona no termo que minha placa-mãe queimou...") | `grep -n "placa-mãe" docs/residencia/termo-de-entrega-Semana-9.md` acha no corpo | done | primeiro item do corpo; escolha aberta 3 reescrita |
| 10 | `entrega/Manual do Treino.docx`: o documento do código do treino reescrito como manual em segunda pessoa, com os trechos de código | Pedro 11/11 ("me manda aquele documento sobre o treino... como se fosse um manual... em docx") | arquivo existe e foi enviado | done | 28 passos, 37 trechos de código tirados dos arquivos atuais, ~9.600 palavras de texto; redigido por agente, conferido por amostra e por busca de caracteres; o Pedro ainda não leu |
