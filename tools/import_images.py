#!/usr/bin/env python3
"""Copy the Gemini masters (talassut_*.jpg/png) into assets/img at web size.

    python tools/import_images.py <folder with the masters>

talassut_p_<name>   -> assets/img/p-<name>.jpg    (packshots, 800 px wide)
talassut_cat_<name> -> assets/img/cat-<name>.jpg  (category tiles, 900 px)
talassut_hero       -> assets/img/hero.jpg        (2400 px)
talassut_<name>     -> assets/img/<name>.jpg      (scenes, 1600 px; _ becomes -)

Needs Pillow (pip install pillow).
"""
import sys
from pathlib import Path
from PIL import Image

OUT = Path(__file__).resolve().parent.parent / "assets" / "img"


def target(stem):
    name = stem[len("talassut_"):]
    if name.startswith("p_"):
        return "p-" + name[2:], 800
    if name.startswith("cat_"):
        return "cat-" + name[4:], 900
    if name == "hero":
        return "hero", 2400
    return name.replace("_", "-"), 1600


def main(src):
    OUT.mkdir(parents=True, exist_ok=True)
    for f in sorted(Path(src).glob("talassut_*")):
        if f.suffix.lower() not in (".jpg", ".jpeg", ".png"):
            continue
        name, width = target(f.stem)
        im = Image.open(f).convert("RGB")
        if im.width > width:
            im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
        im.save(OUT / (name + ".jpg"), "JPEG", quality=82, optimize=True, progressive=True)
        print(f.name, "->", name + ".jpg", im.size)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "_art")
