# Roteiro do agente 3: julgamento (v1, 26/09)

**Tarefa:** julgar cada obra **só com as frases transcritas pelo agente 2**. Você não vê o abstract inteiro.
Se as frases não bastarem para decidir, a resposta certa é `dúvida`; a obra sobe um degrau e será lida na introdução.

## A área e as regras (copiadas do método de screening, `docs/screening/metodo-screening-etapa1.md`)

**§1.2, pertencimento.** Pertence à área o que **reduz custo de implantação** de modelos em pelo menos um eixo:
**(i) inferência**: latência ou throughput; **(ii) memória/hardware**: o modelo cabe onde não cabia;
**(iii) dado rotulado**: mesma capacidade com menos rótulo. PEFT/LoRA entram (serving de vários adaptadores).
A fronteira é o **efeito na implantação**. **Eficiência de treino pura**, sem efeito no modelo servido, fica fora.

**§1.3, modelos.** Transformers e a base dos transformers (RNN, LSTM, seq2seq, atenção). LLMs estão dentro.

**§1.2.1, survey.** Quando a obra é survey:

| Caso | Regra |
|---|---|
| (a) cobre a área **em parte** (ex.: survey de LLM com seção de inferência; treino + inferência; fine-tuning com PEFT) | **relevante**, como base de conhecimento |
| (b) técnica da área aplicada **só** a CNN, GNN ou difusão | **fora** |
| (c) aplicação específica (ex.: compressão para YOLO, biometria, imagem médica) | **dúvida**, com motivo "aplicação específica (c)": só entra se nenhum survey geral cobrir a divisão |
| (d) infraestrutura de implantação (borda, nuvem, serverless, serving de agentes) | **relevante** |
| (e) hardware para IA (aceleradores, FPGA) | **relevante** (presença no mapa) |
| sem nenhum eixo de §1.2 (ex.: survey só de treino) | **fora** |

**§3.4, não é survey.** Conta como survey a obra que **se declara** survey, review, overview ou taxonomy
**ou** que **funciona** como survey (revisa e organiza literatura). Obra que não é survey é **fora**, com
motivo `não é survey` e um subtipo: `primário da área` · `sistema/ferramenta` · `fora da área`.

## O campo `objetivo` (só para `relevante`; ele ordena, não muda o veredito)

As obras servem a objetivos de aprendizado:
- `saber`: conhecimento e compreensão (taxonomias, conceitos, história, comparações);
- `saber fazer`: prática; as frases mostram código, ferramenta, benchmark reproduzível, tutorial, guia,
  estudo de caso de implantação ou lições práticas;
- `saber + saber fazer`: os dois;
- `não dá para dizer`: as frases não mostram.

Não invente sinal prático: sem frase que o mostre, não é `saber fazer`.

## Obra sem acesso

Se a obra chegar com `acesso: "sem acesso"`, devolva `veredito: "sem acesso"` e nada mais.

## Saída

Grave um arquivo JSON (uma lista) no caminho indicado na tarefa, um objeto por obra:

```json
{"id": "C01", "veredito": "relevante" | "fora" | "dúvida" | "sem acesso",
 "regra": "ex.: §1.2 (ii) · §1.2.1 (a) · §1.2.1 (b) · §3.4 primário da área · treino puro",
 "frase": "a frase transcrita que sustenta o veredito, cópia exata",
 "objetivo": "saber" | "saber fazer" | "saber + saber fazer" | "não dá para dizer" | null,
 "motivo": "uma frase curta"}
```

Não escreva mais nada no arquivo. Todas as obras recebidas precisam aparecer na saída.
