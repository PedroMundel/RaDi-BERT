# Banco de fontes preliminares — Triagem Bibliográfica
Pedro Mundel · atualizada: 10 de set. de 2026

**Procedência.** Cada fonte carrega o nível de leitura, e eles não são equivalentes:
**[L]** eu li · **[LA]** leitura assistida do texto completo · **[T]** título, venue e resumo
verificados na fonte, corpo não lido. **[T] serve para triar, não para citar.**

---

## Frente 1 — Racionalização em modelos encoder

| Artigo | Fonte da racionalização | Mecanismo | Nível |
|---|---|---|---|
| **Zaidan, Eisner & Piatko**, NAACL-HLT 2007 | humana extrativa | features de contraste (origem do termo) | [T] |
| **Bao, Chang, Yu & Barzilay**, EMNLP 2018, arXiv:1808.09367 | humana extrativa | mapeia racionalização para pesos de atenção | [T] |
| **Huang, Zhu, Feng & Zhao**, ACL 2021, arXiv:2106.01809 | **ruidosa / distante** | duas perdas auxiliares para racionalização imperfeita | [T] |
| **REFER** — Ghasemi Madani & Minervini, CoNLL 2023, arXiv:2310.14418 | humana | extrator diferenciável fim-a-fim | [T] |
| **Herrewijnen, Nguyen, Bex & Gatt**, EACL 2026 | humana extrativa | regularização de atenção; **encoder confirmado** | [LA] |
| **Kamp, Beinborn & Fokkens**, AACL 2025 | humana | classificação de token vs. atenção regularizada | [T] |
| **SRA** — Eilertsen et al., AAAI 2026, arXiv:2511.07065 | humana | perda conjunta atenção↔racionalização; avalia em pt-BR | [T] |
| **CAGE** — Rajani et al., ACL 2019, arXiv:1906.02361 | humana, texto livre | gera explicação e concatena; alvo é **gerador** | [T] |
| **Li, Schlegel et al.**, arXiv:2508.16777 | **LLM, reduzida a spans** | atenção supervisionada por máscara · formulação NER | [LA] |
| **ERASER** — DeYoung et al., ACL 2020, arXiv:1911.03429 | — | benchmark: *plausibility* e *faithfulness* | [T] |
| **Wiegreffe & Marasović**, NeurIPS D&B 2021 | — | taxonomia: *highlights* / texto livre / estruturada | [T] |
| **Pruthi et al.**, TACL 2022, arXiv:2012.00893 | — | mede utilidade da explicação pelo ganho do aluno | [T] |
| **Hase & Bansal**, arXiv:2102.02201 | — | quando explicação ajuda: framework formal | [T] |

**Leitura da frente:** a supervisão de racionalização em encoders usa racionalização **humana e
extrativa**; racionalização de **texto livre de LLM** alimenta modelos **geradores**. A célula que
cruza as duas aparece vazia.

## Frente 2 — Verificação dos dois mecanismos candidatos

| Artigo | Relevância | Nível |
|---|---|---|
| **LRKD** — Qiu et al., WWW'26, arXiv:2601.21611 (Alibaba) | **Ocupa o primeiro mecanismo:** regressão do vetor latente de um cross-encoder BERT contra embedding congelado da racionalização | [T] |
| arXiv:2609.05363 — GenAIECommerce @ RecSys 2026 | Muito próximo: projeção descartada na inferência | [T] |
| **Agrawal, Ahemd & Sembium** (Amazon), COLING 2025 Industry | **Mecanismo não confirmado** — exige leitura manual. Última incógnita de novidade | [T] |
| **DHRD** — Xu et al., NeurIPS 2025 Efficient Reasoning Workshop, arXiv:2509.21487 | **Vizinho do segundo mecanismo:** cabeça de raciocínio só no treino, mas backbone decoder-only | **[L]** |
| **Distilling Step-by-Step** — Hsieh et al., ACL 2023 Findings, arXiv:2305.02301 | Origem da ideia e mecanismo a transportar | **[L]** |
| **ExpBERT** — Murty, Koh & Liang, ACL 2020, arXiv:2005.01932 | Canal diferente: explicação como texto de entrada | [T] |
| **KEPLER** — arXiv:1911.06136 | Precedente distante: conhecimento por perda latente | [T] |
| **Deeply-Supervised Nets** — Lee et al., AISTATS 2015, arXiv:1409.5185 | Precedente do padrão "cabeça descartada na inferência" | [T] |
| **WT5** — arXiv:2004.14546 · **SCOTT** — ACL 2023, arXiv:2305.01879 | Contraste: auto-explicação **mantém** o gerador | [T] |
| **Chronopoulou et al.**, NAACL 2019, arXiv:1902.10547 | Perda auxiliar de LM genérico no ajuste fino | [T] |

## Frente 3 — Recursos em português

| Recurso | Nota | Nível |
|---|---|---|
| **HateBRXplain** — Salles, Vargas & Benevenuto, COLING 2025 | 7 mil comentários com racionalização humana; código aberto | [T] |
| **HateBRMoralXplain / SMRA** — Vargas et al., Findings ACL 2026, arXiv:2601.03481 | racionalização moral anotada | [T] |
| **ASSIN 2** — Real, Fonseca & Gonçalo Oliveira, STIL 2019 | inferência textual e similaridade; ~7 mil pares | [T] |

**Nenhum destila racionalização de LLM para encoder em português.**

---

## Ordem de leitura

**Antes de comprometer as 16 semanas**
1. ~~Distilling Step-by-Step~~ **[L]** · 2. ~~DHRD~~ **[L]** · 3. **Agrawal (2025)** — única
incógnita restante de novidade · 4. **LRKD** · 5. **Herrewijnen (2026)**

**Para desenhar o estudo**
6. Huang et al. (2021), racionalização ruidosa — que é o que racionalização de LLM é ·
7. Wiegreffe & Marasović, para o vocabulário de posicionamento · 8. ERASER, para *plausibility* e
*faithfulness* · 9. HateBRXplain, se entrar como teto humano

**Para escrever e citar**
Deeply-Supervised Nets · SCOTT · Bao et al. (2018)

---

Além destas frentes, foram triados artigos de eficiência em escala pequena, medição em português e
fronteira dados↔modelo durante a exploração inicial; o registro completo está em
`docs/pesquisa/artigos-verificados.md`.
