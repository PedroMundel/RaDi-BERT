# Por que o decoder auxiliar é descartado e não usado para gerar justificativas (20/10/2026)

**Preocupação do Pedro (20/10):** não conseguir explicar, com prova, por que não usa o decoder da cabeça auxiliar
para criar as justificativas.

**Procedência.** Os itens 1 e 4 vêm de obras que o **Pedro leu (nível 1)**, com citação literal conferida pelo Claude
nas notas de nível 2 (`docs/artigos/notas-distilling-step-by-step.md`, `notas-agrawal-coling2025.md`,
`docs/pesquisa/secao-dsbs-cabeca-auxiliar.md`). O item 3 mistura uma obra de nível 3 com inferência do Claude, marcada no texto. O
item 2 é uma medição que **ainda não foi feita**.

---

## A resposta em três frases (para a arguição)

> "A justificativa é sinal de **treino**, não saída do modelo. É assim no método que eu sigo: o Distilling
> Step-by-Step diz que ela não é necessária na hora do teste, e o Agrawal implanta só o encoder. Minha área é
> eficiência para implantação, e gerar texto custa uma passada do decoder por token; além disso, o texto que essa
> cabeça gera imita o professor e não explica a decisão do classificador, o que exigiria outra pesquisa."

## 1. É o desenho do método, não uma escolha minha (nível 1)

| Obra | O que diz | Onde |
|---|---|---|
| Hsieh et al. (2023), DSbS | *"the rationale r̂i is not required in the test time, which removes the need for an LLM at test-time"* | §3.2, logo após a Eq. 4 |
| Hsieh et al. (2023), DSbS | treinar com justificativa custa só no treino; no teste o desenho multitarefa prevê só o rótulo | *Limitations* |
| Hsieh et al. (2023), DSbS | rejeitam a alternativa de usar a justificativa como **entrada** (PINTO) porque ela exige o LLM na hora de responder e *"does not fully solve deployment challenges"* | §3.2 |
| Agrawal et al. (2025) | *"For inference, we streamline the process by deploying only the cross-encoder model, removing the need for the LLM-based rationale generator or decoder module"* | §4.3 |
| Xu et al. (2025), DHRD | a cabeça de justificativa é desligada no teste e o ganho se mantém | notas `notas-dhrd-xu2025.md` |
| Wadhwa et al. (2024) | o aluno não precisa produzir a justificativa para ganhar com ela (justificativa depois do rótulo) | lido na Semana 5 |

**Leitura:** as quatro obras tratam a justificativa como sinal de treino. Descartar a cabeça não é inventado; é a
propriedade que os próprios autores declaram. O tema v3 vai um passo além, porque descarta a cabeça inteira em vez
de só não usar a saída (`docs/pesquisa/secao-dsbs-cabeca-auxiliar.md` §2).

## 2. O motivo é custo, e esse custo dá para medir (prova própria, a fazer)

O DSbS põe o custo de implantação como eixo do paper, e ele é a sua especialização ("eficiência de modelos para
implantação"). **A prova mais forte é uma medição sua, não uma citação:**

| Medir | Encoder sozinho | Encoder + decoder gerando a justificativa |
|---|---|---|
| Parâmetros na implantação | BERT-base | BERT-base + decoder (T5-small ou T5-base) |
| Passadas por exemplo | 1 | 1 do encoder + **1 do decoder por token gerado** (~45–50 tokens, se imitar o tamanho do Sonnet no piloto) |
| Latência por exemplo e vazão (exemplos/s) na RTX 5060 | medir | medir |
| Pico de VRAM | medir | medir |

- **Pode ser feita antes de qualquer treino.** Latência e memória não dependem dos pesos estarem treinados; bastam
  os modelos pré-treinados e entradas do e-SNLI.
- Vira uma tabela de nível 1 que responde "por que não gerar?" com número, e ainda mostra a especialização na
  prática.
- Os números não estão aqui de propósito: **não foram medidos**.

## 3. O texto da cabeça não explica a decisão do classificador (nível 3 + inferência)

- **Estrutura (inferência do Claude):** as duas cabeças compartilham o encoder, mas decidem separadas. A de
  classificação dá o rótulo; o decoder é treinado para **imitar a justificativa do professor**. Nada no treino
  obriga o texto gerado a corresponder ao motivo da decisão do classificador. Ele pode gerar uma justificativa de
  "contradição" enquanto a cabeça de classificação diz "neutro".
- **Vocabulário da literatura:** isso é a diferença entre explicação **plausível** (convence quem lê) e **fiel**
  (reflete o que o modelo fez). Jacovi & Goldberg (2020), *Towards Faithfully Interpretable NLP Systems*, ACL 2020,
  pp. 4198–4205 (existência conferida; a distinção plausível × fiel está no corpo do paper, **não conferida** pelo
  Claude). Wiegreffe, Marasović & Smith (2021, EMNLP) propõem testes de associação entre rótulo e justificativa em
  modelos que fazem as duas coisas (nível 3, só abstract).
- **Consequência:** usar o decoder como explicador seria afirmar fidelidade sem medir. Medir é outra pergunta de
  pesquisa, fora do escopo do tema, que é "a justificativa melhora o classificador?".

## 4. O treino não otimiza a qualidade do texto gerado (nível 1 + inferência)

- No Agrawal, a perda é `L_cls + 0,1·L_aux`, e o decoder entra com aquecimento próprio. O peso 0,1 mostra que a
  geração é **sinal auxiliar**, não objetivo.
- **Inferência do Claude:** um decoder pequeno, treinado com peso baixo e em ~100 mil pares, deve gerar texto pior
  que o do professor. Para quem precisa da justificativa, o melhor texto já existe: o do professor, guardado.

## 5. O que não é verdade (para não exagerar na defesa)

- **Descartar não é obrigatório.** O decoder pode ficar guardado como modo "explicar sob demanda" (paga o custo só
  quando alguém pede). Isso é escolha de implantação, não limite do método.
- **Opção que transforma o medo em resultado (decisão do Pedro):** depois do treino, gerar com o decoder numa
  amostra e passar pelas mesmas checagens da rodada 0, comparando com o professor e com o humano. Se o texto for
  ruim ou desligado do rótulo previsto, isso vira **evidência** para o item 3, em vez de argumento.

## Fontes

- Hsieh et al. (2023), arXiv:2305.02301; notas `docs/artigos/notas-distilling-step-by-step.md`
- Agrawal, Ahemad & Sembium (2025), https://aclanthology.org/2025.coling-industry.12/; notas `docs/artigos/notas-agrawal-coling2025.md`
- Xu et al. (2025), DHRD; notas `docs/artigos/notas-dhrd-xu2025.md`
- Wadhwa, Amir & Wallace (2024), arXiv:2406.14511
- Jacovi & Goldberg (2020), https://aclanthology.org/2020.acl-main.386/
- Wiegreffe, Marasović & Smith (2021), https://aclanthology.org/2021.emnlp-main.804
