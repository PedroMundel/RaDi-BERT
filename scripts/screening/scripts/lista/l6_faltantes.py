"""Lista os ids (01..56) sem ficha válida em leitura/fichas/. Saída: JSON com a lista, para passar como args ao workflow."""
import csv, json, os, re
LR = r"C:\Users\Pedro\Documents\Projects\UFG\2026-2\Residencia Bacharelado em Inteligencia Artificial\Screening\fase1\lista-rapida"
n = len(list(csv.DictReader(open(os.path.join(LR, "lista-v2.csv"), encoding="utf-8-sig"))))
def ok(i):
    p = os.path.join(LR, "leitura", "fichas", f"{i:02d}.json")
    if not os.path.exists(p): return False
    t = open(p, encoding="utf-8-sig").read()
    try: json.loads(t); return True
    except json.JSONDecodeError:
        try: json.loads(re.sub(r'\(?!["\/bfnrtu])', r'\\', t)); return True
        except json.JSONDecodeError: return False
print(json.dumps([f"{i:02d}" for i in range(1, n + 1) if not ok(i)]))
