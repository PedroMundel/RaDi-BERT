# Roteiro do agente 1: triagem do óbvio (v1, 26/09)

**Tarefa única:** marcar como `claramente fora` só a obra que **obviamente** não tem relação com a área.
Qualquer outra obra `passa`. Você não julga relevância fina; isso é do agente 3.

**A área:** eficiência de modelos de aprendizado de máquina para implantação. Isso inclui compressão
(quantização, poda, destilação, fatoração), inferência e serving, fine-tuning eficiente (LoRA/PEFT), modelos
de linguagem (LLMs, transformers) do treino à inferência, IA em dispositivo/borda/nuvem e hardware para IA.

## `claramente fora`: só estes casos

1. O assunto **não é aprendizado de máquina nem sistemas de IA**. Exemplos: ciências sociais, gestão,
   economia, medicina clínica sem modelo de IA no centro, química, educação, direito, redes de computadores
   sem IA.
2. É IA, mas o **assunto central não tem nenhuma ligação com custo, eficiência, implantação ou modelos
   de linguagem/transformers**, e isso fica evidente no título e no abstract. Exemplo: uma revisão de
   aplicações de IA na agricultura que não fala de modelo, custo nem implantação.

## Tudo o mais `passa`, inclusive

- Obra que menciona eficiência, compressão, inferência, implantação, borda, LLM ou transformer em qualquer parte.
- Obra sobre CNN, GNN ou difusão que trata de eficiência (quem decide essas é o agente 3).
- Obra que não se declara survey (quem decide é o agente 3).
- **Na dúvida, passa.** Eliminar uma obra relevante é o erro caro. Deixar passar lixo é barato.

## Obra sem abstract

Se o campo `acesso` for `sem acesso`, **não decida**: devolva `sem acesso`.

## Saída

Grave um arquivo JSON (uma lista) no caminho indicado na tarefa, um objeto por obra:

```json
{"id": "C01", "decisao": "passa" | "claramente fora" | "sem acesso", "motivo": "uma frase curta, só se claramente fora"}
```

Não escreva mais nada no arquivo. Todas as obras recebidas precisam aparecer na saída.
