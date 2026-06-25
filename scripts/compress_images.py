"""One-time image optimization pass for assets/.

Writes NEW, web-sized copies alongside the originals (suffix "-web.jpg" /
"-web.png") instead of overwriting anything, so the source images are never
touched or deleted. Run with: python3 scripts/compress_images.py
Then point app.py at the "-web" filenames once you're happy with the result.
"""
from pathlib import Path

from PIL import Image

ASSETS_DIR = Path(__file__).parent.parent / "assets"

LOGO_FILENAME = "651fa53d-7fd1-4663-8600-aba5389a5bca.png"

JPEG_TARGETS = {
    "094c11e2-a39c-4b8e-949b-e66d416e0534.png": 1100,
    "4e101546-ebb5-4381-8d29-f7a360030067.png": 1100,
    "6cc32f61-1971-49cd-9962-55ca04232192.png": 1100,
    "bdc8f3c0-9962-4796-8b6a-ffc29437e487.png": 1100,
    "cd822b57-ac2f-40b7-ad87-d434f32afe0b.png": 1100,
    "e9b42817-9dbe-4a2d-93e4-a70823199223.png": 1100,
    "hero-background.jpg": 2400,
}


def resize_to_max_dim(image: Image.Image, max_dim: int) -> Image.Image:
    width, height = image.size
    if max(width, height) <= max_dim:
        return image
    scale = max_dim / max(width, height)
    return image.resize((round(width * scale), round(height * scale)), Image.LANCZOS)


def compress_as_jpeg(filename: str, max_dim: int) -> None:
    path = ASSETS_DIR / filename
    if not path.exists():
        print(f"skip (missing): {filename}")
        return
    before_kb = path.stat().st_size / 1024
    image = Image.open(path).convert("RGB")
    image = resize_to_max_dim(image, max_dim)
    target_path = path.with_name(path.stem + "-web.jpg")
    image.save(target_path, "JPEG", quality=82, optimize=True, progressive=True)
    after_kb = target_path.stat().st_size / 1024
    print(f"{filename}: {before_kb:.0f} KB -> {target_path.name}: {after_kb:.0f} KB (original untouched)")


def compress_logo() -> None:
    path = ASSETS_DIR / LOGO_FILENAME
    if not path.exists():
        print(f"skip (missing): {LOGO_FILENAME}")
        return
    before_kb = path.stat().st_size / 1024
    image = Image.open(path)
    image = resize_to_max_dim(image, 400)
    target_path = path.with_name(path.stem + "-web.png")
    image.save(target_path, "PNG", optimize=True)
    after_kb = target_path.stat().st_size / 1024
    print(f"{LOGO_FILENAME}: {before_kb:.0f} KB -> {target_path.name}: {after_kb:.0f} KB (original untouched)")


if __name__ == "__main__":
    for filename, max_dim in JPEG_TARGETS.items():
        compress_as_jpeg(filename, max_dim)
    compress_logo()
