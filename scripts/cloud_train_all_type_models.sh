#!/usr/bin/env bash
set -euo pipefail

# Sequential formal training script for the SRTP three-type car generator.
#
# Usage:
#   cloud_train_all_type_models.sh [sports_kimg] [sedan_kimg] [suv_kimg] [batch]
#
# Example:
#   cloud_train_all_type_models.sh 800 1000 1000 16
#
# Outputs:
#   outputs/final_models/sports.pkl
#   outputs/final_models/sedan.pkl
#   outputs/final_models/suv.pkl
#   outputs/final_samples/<type>/
#   outputs/final_models/manifest.txt

PROJECT_ROOT="${PROJECT_ROOT:-/root/autodl-tmp/car_srtp_project}"
SPORTS_KIMG="${1:-800}"
SEDAN_KIMG="${2:-1000}"
SUV_KIMG="${3:-1000}"
BATCH="${4:-16}"

SCRIPT_DIR="$PROJECT_ROOT/scripts"
STYLEGAN_DIR="$PROJECT_ROOT/refs/stylegan2-ada-pytorch"
FINAL_MODEL_DIR="$PROJECT_ROOT/outputs/final_models"
FINAL_SAMPLE_DIR="$PROJECT_ROOT/outputs/final_samples"
MANIFEST="$FINAL_MODEL_DIR/manifest.txt"

mkdir -p "$FINAL_MODEL_DIR" "$FINAL_SAMPLE_DIR"

timestamp() {
  date '+%Y-%m-%d %H:%M:%S'
}

latest_run_dir() {
  local car_type="$1"
  find "$PROJECT_ROOT/outputs/type_models/$car_type" -mindepth 1 -maxdepth 1 -type d -printf '%T@ %p\n' \
    | sort -n \
    | tail -n 1 \
    | cut -d' ' -f2-
}

latest_snapshot() {
  local run_dir="$1"
  find "$run_dir" -maxdepth 1 -name 'network-snapshot-*.pkl' -printf '%f\n' \
    | sort \
    | tail -n 1
}

record_manifest_header() {
  {
    echo "SRTP car type model training manifest"
    echo "Generated at: $(timestamp)"
    echo "Project root: $PROJECT_ROOT"
    echo "Batch: $BATCH"
    echo "Targets: sports=$SPORTS_KIMG kimg, sedan=$SEDAN_KIMG kimg, suv=$SUV_KIMG kimg"
    echo
  } > "$MANIFEST"
}

train_one() {
  local car_type="$1"
  local kimg="$2"

  echo "[$(timestamp)] ===== Training $car_type for $kimg kimg ====="
  "$SCRIPT_DIR/cloud_train_type_model.sh" "$car_type" "$kimg" "$BATCH"

  local run_dir
  run_dir="$(latest_run_dir "$car_type")"
  if [[ -z "$run_dir" || ! -d "$run_dir" ]]; then
    echo "Could not locate run directory for $car_type" >&2
    exit 3
  fi

  local snapshot
  snapshot="$(latest_snapshot "$run_dir")"
  if [[ -z "$snapshot" ]]; then
    echo "Could not locate snapshot in $run_dir" >&2
    exit 3
  fi

  local src="$run_dir/$snapshot"
  local dst="$FINAL_MODEL_DIR/$car_type.pkl"
  cp "$src" "$dst"

  echo "[$(timestamp)] Copied final model: $dst"

  mkdir -p "$FINAL_SAMPLE_DIR/$car_type"
  cd "$STYLEGAN_DIR"
  python generate.py \
    --outdir="$FINAL_SAMPLE_DIR/$car_type" \
    --network="$dst" \
    --seeds=0-31 \
    --trunc=0.7

  {
    echo "[$car_type]"
    echo "target_kimg=$kimg"
    echo "run_dir=$run_dir"
    echo "snapshot=$snapshot"
    echo "final_model=$dst"
    echo "samples=$FINAL_SAMPLE_DIR/$car_type"
    echo
  } >> "$MANIFEST"

  echo "[$(timestamp)] ===== Finished $car_type ====="
}

record_manifest_header
train_one sports "$SPORTS_KIMG"
train_one sedan "$SEDAN_KIMG"
train_one suv "$SUV_KIMG"

echo "[$(timestamp)] All type models finished."
echo "Final models:"
ls -lh "$FINAL_MODEL_DIR"
echo
echo "Manifest:"
cat "$MANIFEST"

