export const meta = {
  name: 'leitura-lista-v2',
  description: 'Fichas de leitura das obras da lista rápida v2: um agente Sonnet por obra, grava fichas/NN.json',
  phases: [{ title: 'Leitura', detail: 'um agente por obra; a ficha em disco é o checkpoint' }],
}
const LR = 'C:\\Users\\Pedro\\Documents\\Projects\\UFG\\2026-2\\Residencia Bacharelado em Inteligencia Artificial\\Screening\\fase1\\lista-rapida\\leitura'
const ROT = 'C:\\Users\\Pedro\\Documents\\Projects\\UFG\\2026-2\\Residencia Bacharelado em Inteligencia Artificial\\Screening\\agentes\\roteiro-leitura-lista-v1.md'
const RES = { type: 'object', properties: { id: { type: 'string' }, gravado: { type: 'boolean' }, acesso: { type: 'string' } }, required: ['id', 'gravado'] }
const ids = Array.isArray(args) ? args : []
log(`obras nesta rodada: ${ids.length}`)
const prompt = id => `Leia o roteiro e siga-o à risca: ${ROT}

A obra desta tarefa é a de id ${id}.
- Metadado e acesso: leia a entrada "${id}" em ${LR}\\manifesto.json (título, ano, bloco, divisão, arXiv, DOI, e se há "texto completo").
- Texto completo (quando houver): ${LR}\\textos\\${id}.txt — leia por partes com Read (offset/limit).
- Lista inteira das 56 obras (para acréscimo e sobreposição): ${LR}\\lista-56-titulos.txt
- Grave a ficha JSON em: ${LR}\\fichas\\${id}.json

Não leia outros arquivos do projeto além destes. Pode usar WebSearch/WebFetch só se não houver texto completo. Ao terminar, devolva id, gravado e o tipo de acesso usado.`
const r = await parallel(ids.map(id => () => agent(prompt(id), { label: `obra ${id}`, phase: 'Leitura', model: 'sonnet', agentType: 'general-purpose', schema: RES })))
return { pedidas: ids.length, voltaram: r.filter(Boolean).map(x => x.id) }
