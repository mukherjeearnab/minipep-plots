#!/usr/bin/env python3

import os
import re
from pathlib import Path

# ==========================================================
# Configuration
# ==========================================================

# Root of LaTeX project
PROJECT_DIR = Path("../../../Downloads/MiniPep_Draft_ArXiV(2)")
MAIN_TEX = PROJECT_DIR / "main.tex"

IMAGE_EXTENSIONS = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".eps",
    ".svg",
}

# ==========================================================
# Read main.tex
# ==========================================================

if not MAIN_TEX.exists():
    raise FileNotFoundError(f"{MAIN_TEX} not found.")

tex = MAIN_TEX.read_text(encoding="utf-8")

# Remove LaTeX comments
tex = re.sub(r"(?<!\\)%.*", "", tex)

# ==========================================================
# Extract includegraphics filenames
# ==========================================================

pattern = re.compile(
    r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}"
)

used = set()

for match in pattern.findall(tex):
    path = Path(match)

    # Store both full path and filename stem
    used.add(path.as_posix())
    used.add(path.stem)

# ==========================================================
# Scan all images
# ==========================================================

all_images = []

for ext in IMAGE_EXTENSIONS:
    all_images.extend(PROJECT_DIR.rglob(f"*{ext}"))

unused = []

for img in sorted(all_images):

    rel = img.relative_to(PROJECT_DIR)

    rel_no_ext = rel.with_suffix("").as_posix()

    stem = img.stem

    rel_with_ext = rel.as_posix()

    if (
        rel_no_ext not in used
        and stem not in used
        and rel_with_ext not in used
    ):
        unused.append(rel)

# ==========================================================
# Output
# ==========================================================

print("=" * 60)
print(f"Total figures found : {len(all_images)}")
print(f"Unused figures      : {len(unused)}")
print("=" * 60)

for img in unused:
    print(img)

if not unused:
    print("No unused figures found.")
