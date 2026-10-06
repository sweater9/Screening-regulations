#!/usr/bin/env bash
# Run ON the VM. Runs each engine for DURATION seconds while you talk to the avatar from the browser,
# capturing app log + GPU stats. FPS parsing is a heuristic: check the raw log if numbers look wrong.
set -euo pipefail
DURATION="${DURATION:-120}"; OUT="$HOME/bench_results/$(date +%Y%m%d-%H%M%S)"; mkdir -p "$OUT"
for spec in "wav2lip wav2lip256_avatar1" "musetalk ${MUSETALK_AVATAR:-musetalk_avatar1}"; do
  set -- $spec; model=$1
  echo "== $model: open the page and keep talking for ${DURATION}s =="
  nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv -l 2 > "$OUT/$model.gpu.csv" & G=$!
  timeout "$DURATION" "$(dirname "$0")/run.sh" "$1" "$2" > "$OUT/$model.log" 2>&1 || true
  kill $G 2>/dev/null || true
  echo "-- $model fps lines (last 5):"; grep -iE 'fps' "$OUT/$model.log" | tail -5 || echo "no fps lines found"
done
echo "Per-stage latency (STT/LLM/TTS): python3 $(dirname "$0")/../integrations/stage_latency.py"
echo "Results in $OUT. Acceptance: FPS >= 25."
