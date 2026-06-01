#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="${PROJECT_ROOT:-/root/autodl-tmp/car_srtp_project}"
STYLEGAN_DIR="$PROJECT_ROOT/refs/stylegan2-ada-pytorch"
NETWORK_PKL="${1:?Usage: cloud_generate_final_samples.sh /path/to/network-snapshot.pkl [seeds] [trunc]}"
SEEDS="${2:-0-63}"
TRUNC="${3:-0.7}"
OUTDIR="$PROJECT_ROOT/outputs/final_samples/seeds_${SEEDS//,/}_trunc_${TRUNC}"

cd "$STYLEGAN_DIR"

python generate.py \
  --outdir="$OUTDIR" \
  --network="$NETWORK_PKL" \
  --seeds="$SEEDS" \
  --trunc="$TRUNC"

