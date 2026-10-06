#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
[ -f "$ROOT/config.env" ] || { echo "Missing $ROOT/config.env (copy config.env.example)"; exit 1; }
# shellcheck disable=SC1091
source "$ROOT/config.env"
GC=(gcloud --project "$PROJECT_ID")
