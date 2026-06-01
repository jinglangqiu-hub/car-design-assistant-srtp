from pathlib import Path
from PIL import Image
from collections import Counter
import os

# ===== 路径配置 =====
SRC_DIR = Path(r"D:\car_srtp_project\data\compcars_cleaned_v1\all")

# ===== 参数配置 =====
TARGET_SIZE = 256
PADDING_RATIO = 0.06
JPEG_QUALITY = 95
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def expand_to_square(img: Image.Image, pad_ratio: float = 0.06) -> Image.Image:
    w, h = img.size
    side = max(w, h)

    pad = int(side * pad_ratio)
    canvas_size = side + 2 * pad

    background = Image.new("RGB", (canvas_size, canvas_size), (245, 245, 245))

    x = (canvas_size - w) // 2
    y = (canvas_size - h) // 2
    background.paste(img, (x, y))
    return background


def safe_open_image(img_path: Path):
    try:
        return Image.open(img_path).convert("RGB")
    except Exception:
        return None


def process_one(img_path: Path):
    img = safe_open_image(img_path)
    if img is None:
        return False

    square_img = expand_to_square(img, pad_ratio=PADDING_RATIO)
    square_img = square_img.resize((TARGET_SIZE, TARGET_SIZE), Image.LANCZOS)

    tmp_path = img_path.with_suffix(".tmp.jpg")
    square_img.save(tmp_path, format="JPEG", quality=JPEG_QUALITY)
    os.replace(tmp_path, img_path)
    return True


def main():
    image_paths = [p for p in SRC_DIR.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS]
    print(f"[*] Found images: {len(image_paths)}")

    stats = Counter()

    for idx, img_path in enumerate(image_paths, 1):
        ok = process_one(img_path)
        if ok:
            stats["processed"] += 1
        else:
            stats["bad_image"] += 1

        if idx % 5000 == 0:
            print(f"[*] Processed {idx}/{len(image_paths)} | ok={stats['processed']}")

    print("\n===== SUMMARY =====")
    for k, v in stats.most_common():
        print(f"{k}: {v}")

    print(f"\n[*] In-place processing finished: {SRC_DIR}")


if __name__ == "__main__":
    main()