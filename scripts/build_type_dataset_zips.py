#!/usr/bin/env python3
"""Build per-type StyleGAN2-ADA datasets for the car SRTP project.

The cleaned images are expected to be named like:

    make_id__model_id__year__image_id.jpg

The script reads a CompCars-style attributes file, maps model_id to vehicle
type, filters the cleaned images into sports/sedan/suv groups, and writes
three zip datasets that StyleGAN2-ADA can read directly.

Because CompCars mirrors sometimes differ in how they store the type field, the
script is intentionally conservative:

1. It first prints a type summary and a sample of parsed attributes.
2. It uses a configurable default mapping for common numeric/string labels.
3. You can override the mapping with --mapping-json if the summary shows a
   different convention.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple


IMAGE_EXTS = {".jpg", ".jpeg", ".png"}


# Default mapping covers the common CompCars attribute conventions seen in
# public mirrors: either string type names or numeric ids where sedan/SUV/sports
# car are stored as separate classes. Numeric ids can be overridden after
# running --dry-run and checking the summary.
DEFAULT_TYPE_MAP = {
    "sedan": "sedan",
    "saloon": "sedan",
    "轿车": "sedan",
    "suv": "suv",
    "sport utility vehicle": "suv",
    "sports": "sports",
    "sport": "sports",
    "sports car": "sports",
    "sportscar": "sports",
    "跑车": "sports",
    # Common CompCars numeric convention used by many preprocessed copies.
    # If your attributes summary disagrees, pass --mapping-json.
    "1": "mpv",
    "2": "suv",
    "3": "hatchback",
    "4": "sedan",
    "5": "minibus",
    "6": "fastback",
    "7": "estate",
    "8": "pickup",
    "9": "sports",
    "10": "crossover",
}


def normalize_token(value: str) -> str:
    value = value.strip().lower()
    value = value.replace("_", " ").replace("-", " ")
    value = re.sub(r"\s+", " ", value)
    return value


def load_mapping(path: Optional[Path]) -> Dict[str, str]:
    mapping = dict(DEFAULT_TYPE_MAP)
    if path is None:
        return mapping
    with path.open("r", encoding="utf-8") as f:
        user_map = json.load(f)
    for key, value in user_map.items():
        mapping[normalize_token(str(key))] = normalize_token(str(value))
    return mapping


def parse_attributes(path: Path) -> Tuple[Dict[str, str], Counter, List[Tuple[str, str, str]]]:
    """Return model_id -> raw type token.

    The parser accepts lines where the first token is model_id and the final
    token is the type. Header/comment/blank lines are skipped.
    """
    model_to_raw_type: Dict[str, str] = {}
    raw_counts: Counter = Counter()
    samples: List[Tuple[str, str, str]] = []

    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            parts = re.split(r"[\s,;]+", stripped)
            if len(parts) < 2:
                continue
            model_id = parts[0]
            if not re.fullmatch(r"\d+", model_id):
                continue
            raw_type = normalize_token(parts[-1])
            model_to_raw_type[model_id] = raw_type
            raw_counts[raw_type] += 1
            if len(samples) < 12:
                samples.append((model_id, raw_type, stripped))

    return model_to_raw_type, raw_counts, samples


def image_model_id(path: Path) -> Optional[str]:
    parts = path.stem.split("__")
    if len(parts) < 2:
        return None
    model_id = parts[1]
    return model_id if model_id.isdigit() else None


def iter_images(cleaned_dir: Path) -> Iterable[Path]:
    for path in cleaned_dir.iterdir():
        if path.is_file() and path.suffix.lower() in IMAGE_EXTS:
            yield path


def build_groups(
    cleaned_dir: Path,
    model_to_raw_type: Dict[str, str],
    mapping: Dict[str, str],
) -> Tuple[Dict[str, List[Path]], Counter, Counter]:
    groups: Dict[str, List[Path]] = defaultdict(list)
    raw_image_counts: Counter = Counter()
    skipped: Counter = Counter()

    for image in iter_images(cleaned_dir):
        model_id = image_model_id(image)
        if model_id is None:
            skipped["bad_filename"] += 1
            continue
        raw_type = model_to_raw_type.get(model_id)
        if raw_type is None:
            skipped["missing_model_type"] += 1
            continue
        raw_image_counts[raw_type] += 1
        target = mapping.get(raw_type)
        if target in {"sports", "sedan", "suv"}:
            groups[target].append(image)
        else:
            skipped[f"unmapped:{raw_type}"] += 1

    for target in ("sports", "sedan", "suv"):
        groups[target].sort()
    return groups, raw_image_counts, skipped


def write_zip(images: List[Path], out_zip: Path) -> None:
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    if out_zip.exists():
        out_zip.unlink()
    with zipfile.ZipFile(out_zip, "w", compression=zipfile.ZIP_STORED) as zf:
        for image in images:
            zf.write(image, arcname=image.name)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleaned-dir", type=Path, default=Path("data/compcars_cleaned_v1/all"))
    parser.add_argument("--attributes", type=Path, default=Path("data/raw_compcars/misc/attributes.txt"))
    parser.add_argument("--outdir", type=Path, default=Path("data/type_datasets"))
    parser.add_argument("--mapping-json", type=Path, default=None)
    parser.add_argument("--dry-run", action="store_true", help="Print counts without writing zip files.")
    parser.add_argument("--min-count", type=int, default=500, help="Fail if any target class has fewer images.")
    args = parser.parse_args()

    mapping = load_mapping(args.mapping_json)
    model_to_raw_type, raw_model_counts, samples = parse_attributes(args.attributes)
    groups, raw_image_counts, skipped = build_groups(args.cleaned_dir, model_to_raw_type, mapping)

    print("Parsed model type samples:")
    for model_id, raw_type, line in samples:
        print(f"  model_id={model_id:<6} raw_type={raw_type:<12} line={line}")
    print()

    print("Raw type counts by model:")
    for key, count in raw_model_counts.most_common():
        print(f"  {key}: {count}")
    print()

    print("Raw type counts by cleaned image:")
    for key, count in raw_image_counts.most_common():
        print(f"  {key}: {count}")
    print()

    print("Target dataset counts:")
    for target in ("sports", "sedan", "suv"):
        print(f"  {target}: {len(groups[target])}")
    print()

    if skipped:
        print("Skipped image counts:")
        for key, count in skipped.most_common(20):
            print(f"  {key}: {count}")
        print()

    too_small = [target for target in ("sports", "sedan", "suv") if len(groups[target]) < args.min_count]
    if too_small:
        print(f"ERROR: target class too small with --min-count={args.min_count}: {', '.join(too_small)}")
        print("Run with --dry-run first and inspect raw type counts. If numeric labels differ, pass --mapping-json.")
        return 2

    if args.dry_run:
        print("Dry run only; no zip files written.")
        return 0

    for target in ("sports", "sedan", "suv"):
        out_zip = args.outdir / f"compcars_{target}_256_square.zip"
        print(f"Writing {out_zip} ({len(groups[target])} images)...")
        write_zip(groups[target], out_zip)

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

