#!/usr/bin/env bash
# Run ON the VM. Installs LiveTalking in a Python 3.10 conda env and fetches weights.
set -euo pipefail
nvidia-smi >/dev/null || { echo "NVIDIA driver missing"; exit 1; }
cd "$HOME"
[ -d LiveTalking ] || git clone https://github.com/lipku/LiveTalking.git
cd LiveTalking
command -v conda >/dev/null || { echo "conda not found; install Miniconda first"; exit 1; }
conda create -y -n nerfstream python=3.10 || true
# shellcheck disable=SC1091
source "$(conda info --base)/etc/profile.d/conda.sh"; conda activate nerfstream
# Docs target PyTorch 2.5.0 + CUDA 12.4
pip install torch==2.5.0 torchvision==0.20.0 torchaudio==2.5.0 --index-url https://download.pytorch.org/whl/cu124
pip install -r requirements.txt
mkdir -p models data/avatars
cat <<MSG
Weights are NOT downloaded automatically: the README links them from Google Drive / Quark,
and I could not verify stable direct URLs. Download wav2lip256.pth, rename to models/wav2lip.pth,
and unpack the wav2lip256_avatar1 avatar into data/avatars/ (see LiveTalking README).
MuseTalk needs its own extra weights; follow the README section when you get to that step.
MSG
