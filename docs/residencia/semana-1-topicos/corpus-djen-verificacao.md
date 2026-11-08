# Verificação de acesso — DJEN (28/08/2026)

Feita depois que Pedro apontou o DJEN como fonte pública viável (o dataset do Ultimatum veio de
scraping dessa fonte; ver memória `ultimatum-nao-e-base-garantida`). Fonte: agente de pesquisa
com fetch em páginas oficiais. **O que não foi confirmado está marcado — não tratar como fato.**

## Confirmado

- **DJEN existe e é sistema novo e unificado** (substitui os diários eletrônicos de cada
  tribunal). Portal de consulta: https://comunica.pje.jus.br/ · hub: https://www.jus.br/servico/diario-de-justica-eletronico-nacional-djen/
- Base normativa: Resolução CNJ 234/2016, regulamentado pela **Res. 455/2022**
  (https://atos.cnj.jus.br/atos/detalhar/4509), alterada pela **569/2024**
  (https://atos.cnj.jus.br/atos/detalhar/5691).
- **Adesão gradual por tribunal, 2022–2025** — não há data única de início nacional. Ex.: TJMG
  obrigatório a partir de 27/01/2025. Implicação: cobertura temporal varia por tribunal.
- **Existe API de comunicações**: `GET https://comunicaapi.pje.jus.br/api/v1/comunicacao`.
  Swagger em https://comunicaapi.pje.jus.br/ (a ferramenta levou 403; **abrir no navegador**).
- **DataJud é outra coisa** (metadados processuais/movimentações, não o texto do diário), exige
  chave cadastrada. https://www.cnj.jus.br/sistemas/datajud/api-publica/
- **Não existe dataset público derivado do DJEN** em Hugging Face, Zenodo ou Kaggle. Os corpora
  jurídicos pt-BR existentes são de decisões/jurisprudência de tribunais específicos (STJ, TJAL,
  STF), não da publicação nacional. → **ineditismo em pt-BR sai de graça.**

## NÃO confirmado (checar antes de fechar o método)

- **Estrutura de campos da API** — terceiros citam `id`, `hash`, `dataDisponibilizacao`, `text`,
  e filtros por `numeroProcesso`, `siglaTribunal`, `numeroOab`, `ufOab`, `tipoComunicacao`. Não
  há dicionário oficial confirmado. **Crítico**: saber quais campos vêm estruturados e quais
  estão embutidos no texto livre define a tarefa de extração e o gabarito barato.
- **Autenticação**: terceiros dizem que a consulta é sem credencial. Não confirmado na doc oficial.
- **Limite de requisições**: não há SLA publicado. Recomendação informal de terceiros: ~500ms
  entre chamadas.
- **Bulk**: não foi encontrado download de cadernos em PDF/XML com URL previsível. O caminho
  parece ser a API.
- **Licença / termos de uso do DJEN**: não localizados (só o DataJud tem termo formal).
  robots.txt de comunica.pje.jus.br e comunicaapi.pje.jus.br deram 403 para a ferramenta —
  **verificar manualmente**.
- **Volume** (publicações/dia, nº de tribunais publicando): não localizado.

## Alternativa de menor atrito (backup)

**Querido Diário** (Open Knowledge Brasil) — https://queridodiario.ok.org.br ·
https://github.com/okfn-brasil/querido-diario · docs https://docs.queridodiario.ok.org.br/
Entrega **texto já extraído** de diários oficiais municipais, API documentada, código MIT e
conteúdo **CC-BY 4.0**. Custo: é diário oficial municipal (atos administrativos), não judicial —
muda o domínio, não o método. É o item 91 da lista de domínios.

Outras: STJ Dados Abertos (https://dadosabertos.web.stj.jus.br/dataset/) · DOU/Imprensa Nacional
(https://www.in.gov.br/acesso-a-informacao/dados-abertos).

## Checagens manuais pendentes (10 min no navegador)

1. Abrir https://comunicaapi.pje.jus.br/ e ler o Swagger: quais campos vêm estruturados.
2. `comunica.pje.jus.br/robots.txt` e procurar termos de uso do portal.
3. Fazer uma chamada real à API com um intervalo de datas pequeno e ver o JSON de verdade.

## Nota de dado pessoal

Publicações judiciais são públicas por princípio de publicidade, mas o texto contém nomes de
partes e advogados. Isso não impede pesquisa de extração, mas precisa de uma linha no método
(e conversa com o orientador) sobre o que será redistribuído — publicar o pipeline é mais seguro
que publicar o corpus.
