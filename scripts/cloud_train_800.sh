#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/root/autodl-tmp/car_srtp_project}"
STYLEGAN_DIR="$PROJECT_ROOT/refs/stylegan2-ada-pytorch"
DATA_ZIP="$PROJECT_ROOT/data/compcars_cleaned_v1_256_square.zip"
RESUME_PKL="$PROJECT_ROOT/outputs/stylegan2ada_runs/baseline_240/network-snapshot-000240.pkl"
OUTDIR="$PROJECT_ROOT/outputs/stylegan2ada_runs"

cd "$STYLEGAN_DIR"

python train.py \
  --outdir="$OUTDIR" \
  --data="$DATA_ZIP" \
  --gpus=1 \
  --cfg=auto \
  --mirror=1 \
  --aug=ada \
  --batch=16 \
  --workers=4 \
  --snap=10 \
  --metrics=fid50k_full \
  --kimg=800 \
  --resume="$RESUME_PKL"

