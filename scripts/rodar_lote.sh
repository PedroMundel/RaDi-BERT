#!/usr/bin/env bash
# Overnight batch: start the 35B server, run radibert.lote until the target or the deadline, restart the server if
# it dies (up to 3 tries), and always shut the server down at the end.
# Usage: bash scripts/rodar_lote.sh <alvo> <HH:MM>   (machine paths in config/maquina.env)
set -u
ALVO="$1"; ATE="$2"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CONFIG="$ROOT/config/maquina.env"
[ -f "$CONFIG" ] || { echo "falta $CONFIG: copie config/maquina.example.env e ajuste os caminhos"; exit 2; }
# shellcheck source=/dev/null
source "$CONFIG"
OUT="$ROOT/resultados/lote-35B"

for try in 1 2 3; do
  # shellcheck disable=SC2086  # LLAMA_ARGS is a list of flags
  "$LLAMA_SERVER" -m "$MODELO_35B" $LLAMA_ARGS \
    --host 127.0.0.1 --port 8080 > "$OUT/servidor-$try.log" 2>&1 &
  pid=$!
  for i in $(seq 1 90); do curl -s http://127.0.0.1:8080/health | grep -q ok && break; sleep 2; done
  echo "tentativa $try: servidor no ar, $(nvidia-smi --query-gpu=memory.used --format=csv,noheader) de VRAM"
  (cd "$ROOT" && uv run --frozen python -m radibert.lote gerar --alvo "$ALVO" --ate "$ATE") 2> "$OUT/tentativa-$try.err"
  code=$?
  kill "$pid" 2>/dev/null; sleep 5
  [ "$code" = 0 ] && { echo "lote terminou: $(cat "$OUT/progresso.txt")"; exit 0; }
  echo "tentativa $try falhou (código $code); erro em tentativa-$try.err"
done
exit 1
