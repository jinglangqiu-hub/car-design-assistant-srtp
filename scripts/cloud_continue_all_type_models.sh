#!/usr/bin/env bash
set -euo pipefail

# Continue training from outputs/final_models/{sports,sedan,suv}.pkl.
#
# Usage:
#   cloud_continue_all_type_models.sh [sports_extra_kimg] [sedan_extra_kimg] [suv_extra_kimg] [batch]
#
# Recommended first continuation:
#   cloud_continue_all_type_models.sh 1000 1500 1500 16
#
# The script archives current final models, trains each type sequentially,
# refreshes outputs/final_models/*.pkl, regenerates final samples, and appends
# to outputs/final_models/manifest.txt.

PROJECT_ROOT="${PROJECT_ROOT:-/root/autodl-tmp/car_srtp_project}"
SPORTS_EXTRA="${1:-1000}"
SEDAN_EXTRA="${2:-1500}"
SUV_EXTRA="${3:-1500}"
BATCH="${4:-16}"

SCRIPT_DIR="$PROJECT_ROOT/scripts"
STYLEGAN_DIR="$PROJECT_ROOT/refs/stylegan2-ada-pytorch"
FINAL_MODEL_DIR="$PROJECT_ROOT/outputs/final_models"
FINAL_SAMPLE_DIR="$PROJECT_ROOT/outputs/final_samples"
ARCHIVE_ROOT="$PROJECT_ROOT/outputs/final_models_archive"
RUN_TAG="$(date +%Y%m%d_%H%M%S)"
ARCHIVE_DIR="$ARCHIVE_ROOT/$RUN_TAG"
MANIFEST="$FINAL_MODEL_DIR/manifest.txt"

timestamp() {
  date '+%Y-%m-%d %H:%M:%S'
}

latest_run_dir() {
  local car_type="$1"
  find "$PROJECT_ROOT/outputs/type_models_continue/$car_type" -mindepth 1 -maxdepth 1 -type d -printf '%T@ %p\n' \
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

archive_existing_models() {
  mkdir -p "$ARCHIVE_DIR"
  for car_type in sports sedan suv; do
    if [[ -f "$FINAL_MODEL_DIR/$car_type.pkl" ]]; then
      cp "$FINAL_MODEL_DIR/$car_type.pkl" "$ARCHIVE_DIR/$car_type.pkl"
    else
      echo "Missing existing final model: $FINAL_MODEL_DIR/$car_type.pkl" >&2
      exit 2
    fi
  done
  if [[ -f "$MANIFEST" ]]; then
    cp "$MANIFEST" "$ARCHIVE_DIR/manifest.txt"
  fi
  echo "[$(timestamp)] Archived previous final models to $ARCHIVE_DIR"
}

continue_one() {
  local car_type="$1"
  local extra_kimg="$2"
  local resume="$FINAL_MODEL_DIR/$car_type.pkl"

  echo "[$(timestamp)] ===== Continuing $car_type for +$extra_kimg kimg ====="
  "$SCRIPT_DIR/cloud_train_type_from_resume.sh" "$car_type" "$resume" "$extra_kimg" "$BATCH"

  local run_dir
  run_dir="$(latest_run_dir "$car_type")"
  if [[ -z "$run_dir" || ! -d "$run_dir" ]]; then
    echo "Could not locate continuation run directory for $car_type" >&2
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
  echo "[$(timestamp)] Refreshed final model: $dst"

  rm -rf "$FINAL_SAMPLE_DIR/$car_type"
  mkdir -p "$FINAL_SAMPLE_DIR/$car_type"
  cd "$STYLEGAN_DIR"
  python generate.py \
    --outdir="$FINAL_SAMPLE_DIR/$car_type" \
    --network="$dst" \
    --seeds=0-47 \
    --trunc=0.65

  {
    echo "[continue:$RUN_TAG:$car_type]"
    echo "extra_kimg=$extra_kimg"
    echo "batch=$BATCH"
    echo "resume=$resume"
    echo "run_dir=$run_dir"
    echo "snapshot=$snapshot"
    echo "final_model=$dst"
    echo "samples=$FINAL_SAMPLE_DIR/$car_type"
    echo "sample_seeds=0-47"
    echo "sample_trunc=0.65"
    echo
  } >> "$MANIFEST"

  echo "[$(timestamp)] ===== Finished continuation $car_type ====="
}

mkdir -p "$FINAL_MODEL_DIR" "$FINAL_SAMPLE_DIR" "$ARCHIVE_ROOT"
archive_existing_models
continue_one sports "$SPORTS_EXTRA"
continue_one sedan "$SEDAN_EXTRA"
continue_one suv "$SUV_EXTRA"

echo "[$(timestamp)] All continuation runs finished."
ls -lh "$FINAL_MODEL_DIR"

