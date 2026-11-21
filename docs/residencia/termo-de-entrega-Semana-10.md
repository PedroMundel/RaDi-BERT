# Termo de Aceite de Entrega — Semana 10

- **Data da Reunião ("Gate") de aprovação:** `[preencher]`
- **Participante:** Pedro Mundel — `[matrícula]`

> Rascunho do Claude (19/11, 10:50), para o Pedro adaptar. Itens na ordem da história do documento linkado, sem o
> Resumo das Semanas. Ver "Escolhas abertas" no fim.

---

**Título / Tema:** Destilação de Racionalização de LLM para Encoders: controles e limites. A supervisão por
justificativas vale o custo em encoders para implantação? Tema dentro de eficiência de modelos para implantação.

**Pergunta:** a justificativa escrita por um LLM ajuda um modelo encoder, que não gera texto, a classificar melhor?
Parti da receita de Agrawal, Ahemad & Sembium (2025): um BERT com um decoder T5 auxiliar que escreve a justificativa
no treino e é descartado na entrega.

**O que fiz nesta décima Semana** (os itens marcados com "Semana 9" já foram entregues e entram só para a história
ficar inteira):

**1. Parti de repetir o artigo no RTE, e o número dele não saiu**

- (Semana 9) Treinei a receita no RTE, com BERT comum e com o BERT MS-MARCO que o artigo usa. O baseline deu 0,736 e
  0,767 de ROC-AUC, contra 0,4754 no artigo, e o decoder ficou abaixo do baseline nos dois (-0,028 e -0,049);
- Tentei mais condições para chegar ao 0,4754: encoder congelado (0,590), uma época só (0,635 e 0,741) e um segundo
  checkpoint MS-MARCO (0,743, com o decoder em -0,022). Nenhuma dá o número do artigo;
- Conferi a Tabela 2 do artigo no PDF. O ganho de +0,112 que ele relata no RTE apareceria nas minhas rodadas e não
  aparece. Nas tarefas em que o baseline dele é forte (QNLI, QQP e SST-2), os intervalos do próprio artigo se
  sobrepõem.

Como o resultado positivo não aparecia, resolvi medir o que o artigo não mediu.

**2. Medi de onde vem o ganho aparente do decoder e se o conteúdo da justificativa conta**

- Treinei o BERT com o decoder nos 16 mil pares do e-SNLI, onde a receita cabe inteira. A perda do decoder cai, ele
  aprende a escrever, e a classificação não ganha (+0,003 de ROC-AUC, cruzando o zero);
- Separei o calendário de treino do decoder. O calendário sozinho já ajuda (+0,007 de ROC-AUC, nas 5 sementes), e o
  que parecia ganho do decoder era dele: com o mesmo calendário dos dois lados, o decoder tira 0,9 ponto de acurácia;
- Troquei a justificativa de cada par pela de outro par do mesmo rótulo. A trocada custa 2,1 pontos a mais que a
  certa, então o conteúdo da justificativa importa, mas a certa também não passa do treino sem decoder;
- Medi se o decoder faz o treino arrancar mais rápido. Ele começa 15 pontos na frente, e o encoder alcança sozinho em
  cerca de 100 passos;
- Testei fora do domínio de treino e em mais três medidas que escolhi (calibração, predição seletiva e pior classe).
  Nenhuma melhora com o decoder, e no MNLI ele fica 1,5 ponto abaixo;
- Variei o peso da perda do decoder (0, 0,05 e 0,5), que estava fixo no valor do artigo. Com 3 sementes, nenhum valor
  passa, e com peso 0 a perda é a mesma: o custo parece estar na fase em que só o decoder treina o encoder;
- Pedi a um LLM que lesse 50 justificativas que o decoder gera depois do treino: 22 são usáveis.

**3. Medi por que outros três caminhos da justificativa ao encoder não sobem a nota**

- (Semana 9) Marquei, na atenção do `[CLS]`, as palavras que a justificativa copia do par. A atenção vai para as
  palavras marcadas (de 0,285 para 0,805) e a nota não muda. Um ganho de +0,017 que apareceu com 5 sementes sumiu com
  mais 10, e fora da distribuição deu -0,004;
- Tentei levar ao `[CLS]` as palavras novas da justificativa, agrupadas por assunto. Deu nulo, e a sonda mostrou o
  motivo: o BERT pré-treinado já tinha essa informação (0,765 antes contra 0,760 depois);
- Treinei um professor que lê o par junto com a justificativa. Ele acerta 96,7% sem precisar do par, e imitar o
  interior dele atrapalha o aluno (2,7 pontos abaixo).

**4. Medi o que funciona no mesmo cenário**

- (Semana 9) As palavras em que o modelo com marcas mais presta atenção coincidem com as que o LLM copia (AP 0,724
  contra 0,555 da melhor regra sem treino). Serve para apontar as palavras que o LLM usaria para justificar, não para
  subir a nota; não testei se isso ajuda uma pessoa nem se explica a decisão do modelo;
- Testei a destilação comum entre BERTs como referência. Imitar as respostas de um BERT maior dá +1,6 ponto no modelo
  pequeno, e imitar antes o interior dele dá mais 0,9 (0,45 no dev, com 15 sementes). É o único ganho de nota do projeto, e ele não usa LLM nem
  justificativa: é destilação padrão (Hinton, Vinyals & Dean, 2015).

**5. O que fica de entendimento**

- O ganho aparente do decoder vem do calendário de treino. O conteúdo da justificativa conta, mas, nos jeitos que
  testei, não melhora a classificação do encoder; o que melhora é a destilação comum;
- Sobre o custo: gerar as 16 mil justificativas levou 5h20 de GPU (1,20 s por par), e o treino com decoder leva
  cerca de 33 minutos por semente, contra 4,5 do treino sem decoder com o mesmo calendário. Na inferência o custo é
  igual, porque o decoder é descartado. Em troca, a acurácia não sobe: cai 0,9 ponto dentro do domínio e 1,5 fora.
  Nesta receita, com um LLM e um prompt, a supervisão por justificativas não vale o custo;
- Uma hipótese que não testei: a falta de ganho pode vir das justificativas que gerei, e não da receita. No
  comércio eletrônico do artigo a justificativa pode trazer informação do domínio que não está no par. Nas minhas,
  só 21,8% das palavras são novas, e essas palavras novas sozinhas já entregam o rótulo em 76,4% dos pares (acaso
  33,5%); um BERT que lê só a justificativa acerta 96,9%. Ou seja, o que elas trazem de novo é quase só o rótulo, que
  o classificador já recebe. Essa hipótese não explica o ganho que o artigo relata no RTE, que é de domínio geral;
- Toda comparação com decoder precisa do controle de calendário, senão o calendário passa por efeito do decoder;
- O mesmo treino, repetido na GPU, varia até 0,026 de ROC-AUC. Diferença menor que isso com 5 sementes não é sinal;
- Escrevi o critério de cada teste antes de rodar, e foi isso que me deixou chamar os nulos de nulos.

A história completa, com as tabelas e os limites, está em **Trilha das Semanas 9 e 10**. As figuras e a lista
de onde está cada número estão em **Figuras e Evidencias da Semana 10**. As regras escritas antes de cada teste estão
em **Criterios Escritos Antes dos Testes - Semana 10**, e a versão corrigida do documento da Semana 9 em **Marcas de
Atencao e Destaque v2**.

**Planejamento:**

- `[preencher ou deixar em branco; ver a escolha aberta 3]`

---

## Documentos a linkar

| No termo | Arquivo |
|---|---|
| Trilha das Semanas 9 e 10 | `entrega/Trilha das Semanas 9 e 10.docx` (fonte: `entrega/controles-do-decoder-e-destilacao.md`, reescrito em 19/11 como história única da replicação) |
| Criterios Escritos Antes dos Testes - Semana 10 | `entrega/Criterios Escritos Antes dos Testes - Semana 10.docx` (fonte: `entrega/criterios-da-semana-10.md`; escrito pelo Claude em 19/11 às 11:19 a partir de `docs/2026-11-18-gaps-da-argumentacao.md`; você não leu) |
| Marcas de Atencao e Destaque v2 | `entrega/Marcas de Atencao e Destaque v2.docx` (a versão com a seção 6 corrigida; o `.docx` entregue em 11/11 ficou intacto) |
| Figuras e Evidencias da Semana 10 | `entrega/Figuras e Evidencias.docx` (fonte: `entrega/figuras-e-evidencias.md`; 8 figuras de `resultados/figuras/` e a tabela de onde sai cada afirmação; gerado em 19/11 às 11:03) |

---

## Escolhas abertas (só o Pedro decide)

1. **Você não leu os resultados de 10 a 19/11.** As leituras e o documento linkado foram escritos com LLM. Pela regra
   do projeto, nada entra em texto assinado por você sem leitura sua.
2. **O bloco 5 ("O que fica de entendimento") é novo e saiu do registro, não de fala sua.** O Fernando fecha o termo
   dele com "entendimentos"; se nenhum dos quatro for seu, corte o bloco.
3. **Planejamento.** Os três colegas (David, Fernando e Anna) entregaram o Planejamento em branco no termo de 18/11.
   Nada está decidido para depois do gate.
4. **Título.** Você trocou o título do documento para "Trilha das Semanas 9 e 10" (19/11, 11:10; antes era
   "Controles que o Artigo Nao Rodou", e o `.docx` com esse nome antigo continua na pasta, sem uso); a linha "Título / Tema"
   agora traz o título e o subtítulo do tema que você ditou às 10:50 ("Destilação de Racionalização de LLM para
   Encoders: controles e limites" e a pergunta do custo). O título do documento linkado não foi trocado. O item de
   custo no bloco 5 foi acrescentado a seu pedido; os números vêm de `entrega/geracao-primeiro-lote.md` (5h20, 1,20 s
   por par) e dos tempos gravados na rodada de 19/11 (33 e 4,5 minutos por semente).
5. **Uso de LLM.** Nenhum item declara o LLM. Na Semana 9 o primeiro item declarava ("auxílio pesado de LLM"), a seu
   pedido. Decida se entra de novo.
6. **Itens da Semana 9 repetidos.** Estão marcados com "(Semana 9)" para a história ficar inteira, como a Anna fez. Se
   preferir só o que é novo, saem quatro itens.
7. **Ressalvas que ficaram só no documento:** a varredura do peso é exploratória; o braço embaralhado fora de domínio
   não passou numa conferência e não entrou no termo; MiniLM (Wang et al., 2020) e TinyBERT (Jiao et al., 2020), que
   guiaram "imitar o interior", não foram lidos por você e não são citados aqui.
8. **`.docx` das marcas** (seção 6 corrigida em 18/11): relinkar a versão corrigida ou deixar a entregue em 11/11.
9. **Números conferidos por agente (19/11)** contra as leituras em `resultados/`: os do termo batem todos; no
   documento, três frases foram corrigidas (atenção sozinha, base de sementes do 74,9%, sentido do +2,0 do juiz).
