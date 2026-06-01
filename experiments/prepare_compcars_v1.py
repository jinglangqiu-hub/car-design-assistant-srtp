from pathlib import Path
from PIL import Image
from collections import Counter

# ===== 路径配置 =====
ROOT = Path(r"D:\car_srtp_project\data\raw_compcars")
IMAGE_DIR = ROOT / "image"
LABEL_DIR = ROOT / "label"

OUT_DIR = Path(r"D:\car_srtp_project\data\compcars_cleaned_v1\all")

# ===== 参数配置 =====
TARGET_VIEWPOINTS = {4}   # 4 = front-side
MIN_CROP_W = 128
MIN_CROP_H = 128
JPEG_QUALITY = 95

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def safe_open_image(img_path: Path):
    try:
        img = Image.open(img_path).convert("RGB")
        return img
    except Exception:
        return None


def parse_label_file(label_path: Path):
    """
    label 文件三行：
    1) viewpoint
    2) bbox count
    3) x1 y1 x2 y2
    """
    try:
        lines = label_path.read_text(encoding="utf-8", errors="ignore").strip().splitlines()
        if len(lines) < 3:
            return None

        viewpoint = int(lines[0].strip())
        bbox_count = int(lines[1].strip())

        parts = lines[2].strip().split()
        if len(parts) != 4:
            return None

        x1, y1, x2, y2 = map(int, parts)
        return {
            "viewpoint": viewpoint,
            "bbox_count": bbox_count,
            "bbox": (x1, y1, x2, y2),
        }
    except Exception:
        return None


def is_valid_bbox(bbox, width, height):
    x1, y1, x2, y2 = bbox
    return 1 <= x1 < x2 <= width and 1 <= y1 < y2 <= height


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if not IMAGE_DIR.exists():
        print(f"[ERROR] image dir not found: {IMAGE_DIR}")
        return
    if not LABEL_DIR.exists():
        print(f"[ERROR] label dir not found: {LABEL_DIR}")
        return

    image_paths = [p for p in IMAGE_DIR.rglob("*") if p.suffix.lower() in IMAGE_EXTS and p.is_file()]
    print(f"[*] Found image files: {len(image_paths)}")

    stats = Counter()

    for idx, img_path in enumerate(image_paths, 1):
        rel = img_path.relative_to(IMAGE_DIR)
        label_path = LABEL_DIR / rel.with_suffix(".txt")

        if not label_path.exists():
            stats["missing_label"] += 1
            continue

        label = parse_label_file(label_path)
        if label is None:
            stats["bad_label"] += 1
            continue

        viewpoint = label["viewpoint"]
        bbox = label["bbox"]

        if viewpoint not in TARGET_VIEWPOINTS:
            stats[f"skip_viewpoint_{viewpoint}"] += 1
            continue

        img = safe_open_image(img_path)
        if img is None:
            stats["bad_image"] += 1
            continue

        w, h = img.size
        if not is_valid_bbox(bbox, w, h):
            stats["bad_bbox"] += 1
            continue

        x1, y1, x2, y2 = bbox
        crop = img.crop((x1, y1, x2, y2))

        cw, ch = crop.size
        if cw < MIN_CROP_W or ch < MIN_CROP_H:
            stats["too_small_after_crop"] += 1
            continue

        flat_name = "__".join(rel.parts).replace(img_path.suffix, ".jpg")
        out_path = OUT_DIR / flat_name

        crop.save(out_path, format="JPEG", quality=JPEG_QUALITY)
        stats["saved"] += 1

        if idx % 5000 == 0:
            print(f"[*] Processed {idx}/{len(image_paths)} | saved={stats['saved']}")

    print("\n===== SUMMARY =====")
    for k, v in stats.most_common():
        print(f"{k}: {v}")

    print(f"\n[*] Cleaned images saved to: {OUT_DIR}")


if __name__ == "__main__":
    main()