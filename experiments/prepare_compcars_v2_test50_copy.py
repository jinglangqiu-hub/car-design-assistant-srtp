from pathlib import Path
from PIL import Image
from collections import Counter
import shutil

# ===== 路径配置 =====
SRC_DIR = Path(r"D:\car_srtp_project\data\compcars_cleaned_v1\all")
BEFORE_DIR = Path(r"D:\car_srtp_project\data\compcars_cleaned_v1_test50_before")
AFTER_DIR = Path(r"D:\car_srtp_project\data\compcars_cleaned_v1_test50_after")

# ===== 参数配置 =====
TARGET_SIZE = 256
PADDING_RATIO = 0.06
JPEG_QUALITY = 95
TEST_LIMIT = 50
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def expand_to_square(img: Image.Image, pad_ratio: float = 0.12) -> Image.Image:
    """把长方形图补边扩成正方形，不裁主体。"""
    w, h = img.size
    side = max(w, h)

    pad = int(side * pad_ratio)
    canvas_size = side + 2 * pad

    # 浅灰白底，适合车图 baseline
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


def main():
    BEFORE_DIR.mkdir(parents=True, exist_ok=True)
    AFTER_DIR.mkdir(parents=True, exist_ok=True)

    image_paths = sorted(
        [p for p in SRC_DIR.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS]
    )[:TEST_LIMIT]

    print(f"[*] Test mode: processing first {len(image_paths)} images")

    stats = Counter()

    for idx, img_path in enumerate(image_paths, 1):
        # 先复制原图到 before
        before_path = BEFORE_DIR / img_path.name
        shutil.copy2(img_path, before_path)

        img = safe_open_image(img_path)
        if img is None:
            stats["bad_image"] += 1
            print(f"[{idx}/{len(image_paths)}] BAD -> {img_path.name}")
            continue

        square_img = expand_to_square(img, pad_ratio=PADDING_RATIO)
        square_img = square_img.resize((TARGET_SIZE, TARGET_SIZE), Image.LANCZOS)

        after_path = AFTER_DIR / img_path.name
        square_img.save(after_path, format="JPEG", quality=JPEG_QUALITY)

        stats["processed"] += 1
        print(f"[{idx}/{len(image_paths)}] OK  -> {img_path.name}")

    print("\n===== SUMMARY =====")
    for k, v in stats.most_common():
        print(f"{k}: {v}")

    print(f"\n[*] BEFORE images: {BEFORE_DIR}")
    print(f"[*] AFTER  images: {AFTER_DIR}")


if __name__ == "__main__":
    main()