# Cópia: números (gerado por `copia.py`)

## A. Todas as explicações humanas da validação

| fonte | n | sem_conteudo | copia_entrada | copia_hipotese | controle | 100%_copiada | palavras_novas_mediana |
|---|---|---|---|---|---|---|---|
| humano (9.842 pares × 3) | 29521 | 5 | 76.5% | 46.8% | 3.5% | 30.6% | 1 |

## B. Os mesmos 1.000 pares do piloto: humano × Haiku × Sonnet

| fonte | n | sem_conteudo | copia_entrada | copia_hipotese | controle | 100%_copiada | palavras_novas_mediana |
|---|---|---|---|---|---|---|---|
| humano | 1000 | 0 | 77.2% | 48.1% | 3.1% | 33.1% | 1 |
| haiku | 1000 | 0 | 42.2% | 23.5% | 1.9% | 0.1% | 8 |
| sonnet | 1000 | 0 | 49.3% | 26.9% | 2.3% | 0.3% | 6 |

### Cópia da entrada por rótulo

| gold_label    | humano   | haiku   | sonnet   |
|:--------------|:---------|:--------|:---------|
| contradiction | 78.4%    | 41.0%   | 50.7%    |
| entailment    | 85.0%    | 44.1%   | 50.0%    |
| neutral       | 68.2%    | 41.6%   | 47.1%    |

### Cópia só da hipótese por rótulo

| gold_label    | humano   | haiku   | sonnet   |
|:--------------|:---------|:--------|:---------|
| contradiction | 43.5%    | 21.6%   | 26.7%    |
| entailment    | 51.8%    | 24.5%   | 27.1%    |
| neutral       | 49.0%    | 24.3%   | 27.0%    |

### Palavras novas mais frequentes (não estão no par)

- **humano:** mean (89), just (80), necessarily (44), simultaneously (36), infer (34), time (33), different (24), means (19), rephrasing (17), person (14), type (13), doing (12)
- **haiku:** incompatible (136), details (128), places (124), necessarily (120), claim (108), directly (101), different (100), setting (96), confirms (94), adds (92), specific (86), simply (85)
- **sonnet:** restates (141), means (116), just (113), directly (110), details (96), different (92), incompatible (90), rules (79), possible (74), general (71), easily (70), doing (67)
