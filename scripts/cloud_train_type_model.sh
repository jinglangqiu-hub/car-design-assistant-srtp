#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/root/autodl-tmp/car_srtp_project}"
CAR_TYPE="${1:?Usage: cloud_train_type_model.sh sports|sedan|suv [kimg] [batch]}"
KIMG="${2:-300}"
BATCH="${3:-16}"

STYLEGAN_DIR="$PROJECT_ROOT/refs/stylegan2-ada-pytorch"
DATA_ZIP="$PROJECT_ROOT/data/type_datasets/compcars_${CAR_TYPE}_256_square.zip"
RESUME_PKL="$PROJECT_ROOT/outputs/stylegan2ada_runs/baseline_240/network-snapshot-000240.pkl"
OUTDIR="$PROJECT_ROOT/outputs/type_models/${CAR_TYPE}"

if [[ ! "$CAR_TYPE" =~ ^(sports|sedan|suv)$ ]]; then
  echo "Unknown car type: $CAR_TYPE" >&2
  exit 2
fi

if [[ ! -f "$DATA_ZIP" ]]; then
  echo "Missing dataset: $DATA_ZIP" >&2
  exit 2
fi

mkdir -p "$OUTDIR"
cd "$STYLEGAN_DIR"

python train.py \
  --outdir="$OUTDIR" \
  --data="$DATA_ZIP" \
  --gpus=1 \
  --cfg=auto \
  --mirror=1 \
  --aug=ada \
  --batch="$BATCH" \
  --workers=4 \
  --snap=10 \
  --metrics=none \
  --kimg="$KIMG" \
  --resume="$RESUME_PKL"

