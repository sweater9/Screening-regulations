#!/usr/bin/env bash
# Run ON the VM. Usage: run.sh [wav2lip|musetalk] [avatar_id]
set -euo pipefail
MODEL="${1:-wav2lip}"; AVATAR="${2:-wav2lip256_avatar1}"
# Keys come from Secret Manager (never from files/args). Needs the VM service account to read the secret.
if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
  ANTHROPIC_API_KEY="$(gcloud secrets versions access latest --secret "${ANTHROPIC_SECRET:-anthropic-api-key}")"
  export ANTHROPIC_API_KEY
fi
source "$(conda info --base)/etc/profile.d/conda.sh"; conda activate nerfstream
cd "$HOME/LiveTalking"
exec python app.py --transport webrtc --model "$MODEL" --avatar_id "$AVATAR"
