# Notas: Xu, Zhao, Song, Stewart & Ermon (2020), *A Theory of Usable Information under Computational Constraints*

- **Venue:** ICLR 2020 (Talk), pelo campo *Comments* do arXiv 2002.10689.
- **Código:** GitHub Newbeeer/V-information (citado pela busca, não aberto).
- **Procedência: nível 3.** O texto completo (ar5iv) foi lido em 21/10/2026 por extração via WebFetch: um modelo
  pequeno respondeu perguntas sobre o texto. As fórmulas abaixo vêm dessa extração. **Não é leitura do Claude
  (nível 2), nem do Pedro.** Conferir no PDF antes de citar.

## O que o paper propõe

A informação de Shannon supõe um observador sem limite de computação. A **V-informação** mede a informação que um
observador **com uma família de modelos V** consegue usar.

| Item | Onde | Conteúdo |
|---|---|---|
| Família preditiva | Def. 1, §2 | V ⊆ Ω = {f : 𝒳 ∪ {∅} → 𝒫(𝒴)}, com a condição de **ignorância opcional**: o modelo pode ignorar a entrada lateral (entrada nula ∅) |
| V-entropia condicional | Def. 2 | H_V(Y \| X) = inf_{f∈V} E[−log f[x](y)]; H_V(Y) = H_V(Y \| ∅) = inf_{f∈V} E[−log f[∅](y)] |
| V-informação | Def. 3, Eq. 3 | I_V(X→Y) = H_V(Y \| ∅) − H_V(Y \| X) |
| Casos especiais | Prop. 1 | V = Ω recupera Shannon; família gaussiana linear recupera R² · tr(Cov(Y)); outras recuperam desvio absoluto médio e traço da covariância |
| Propriedades | Prop. 2, §3.1 | monotonicidade (família maior dá entropia menor), não negatividade, independência ⇒ I = 0 |
| Assimetria | §3.3 | I_V(X→h(X)) ≫ I_V(h(X)→X) para função de mão única |
| Viola a desigualdade de processamento de dados | §3.2 | computação pode criar informação usável: I_V(t(X)→Y) > I_V(X→Y) |
| Sem regra da cadeia | Apênd. F | a regra aditiva de Shannon "does not hold true for general 𝒱-Information" |
| Estimação | Def. 4, Teo. 1 | erro de estimação ≤ 4·(complexidade de Rademacher da família) + termo O(\|D\|^−1/2), com probabilidade ≥ 1−2δ, supondo log-verossimilhança limitada |

Experimentos: árvores de Chow-Liu (estrutura), rede gênica DREAM5, ordem de quadros em Moving-MNIST (PixelCNN++) e
justiça (*fairness*) em Adult, German e Heritage. Segundo a extração, a V-informação vence os estimadores de
informação mútua (CPC, NWJ, MINE, KSG) na recuperação da estrutura. Os números exatos não foram extraídos.

## O que licencia no projeto (leitura do Claude)

1. **A medida de I(R; X | Y) com um LM pequeno é uma V-informação**, não a de Shannon. O número depende do
   estimador por definição, e não por defeito. Comparar braços exige a **mesma família** de estimador.
2. **A direção importa:** medir X→R, que é a direção da cabeça auxiliar. As duas escritas são iguais só na teoria
   de Shannon.
3. **A partição redundante + novo é só teórica:** sem regra da cadeia, o termo condicional se mede direto.
4. **A ignorância opcional vira receita prática:** H_V(R | Y) se estima com **a mesma arquitetura**, com o par
   substituído por entrada nula. Não com outro modelo.
5. **Teorema 1:** um estimador grande demais sobreajusta (Rademacher alto). Estimar em dados separados do ajuste é
   inferência do Claude: o paper define a medida sobre o conjunto empírico.
6. **A versão condicional não está neste paper:** ela vem de Hewitt et al. (2021, EMNLP, *Conditional probing*), e é
   a que o REV (Chen et al., 2023, ACL) usa.
