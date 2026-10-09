"""
Recreates the MiniPep PDB comparison figure programmatically.

Usage:   python generate_comparison.py
Output:  /mnt/user-data/outputs/MiniPep-PDB-Best-2GL1_comparison.png

Strategy:
  - Take the full-height structure image from each panel of the source PNG
  - Erase the baked-in text by painting a white rectangle over the bottom strip
  - Re-draw all metric labels and model name with Pillow

To use your OWN structure images: set panel["image"] to an absolute file path.
"""

from PIL import Image, ImageDraw, ImageFont
import os

# ─────────────────────────────────────────────────────────────────
# Panel data — edit values and/or image paths here
# ─────────────────────────────────────────────────────────────────

############################
# CHANGE THESE
SOURCE_PATH = r"C:\Users\Arnab\Downloads\5NDA_renders_overlay_align"
PDB_ID = "5NDA"
CLASS = "ALPHA-BEST"
HFLIP = True
VFLIP = False
############################

MODELS = [
    ("AF2", "AlphaFold2", 1, "af2-9"),
    ("RF2", "RoseTTAFold2", 2, "rf2-7"),
    ("ESM", "ESMFold", 3, "esm-4"),
    ("OMF", "OmegaFold", 4, "omf-6"),
    ("DMP", "DMPfold2", 5, "dmp-5")
]

PANELS = []


for i, model in enumerate(MODELS):
    image = f"{SOURCE_PATH}/{PDB_ID}-{model[0]}_aligned.png"
    name = model[1]

    metrics = []

    with open(f"../Metrics Generated/per-residue-rmsd-job-{model[3]}.csv", 'r') as f:
        for line in f.readlines():
            pdb_id, nmr_model_index, n_selected_residues, ca_rmsd_A, per_res_ca_rmsd_A = line.split(
                ',')
            if pdb_id == PDB_ID:
                metrics.append(('RMSD', f"{per_res_ca_rmsd_A[:4]} Å"))
                break

    with open(f"../Metrics Generated/metrics-metjob-v2-{model[2]}.csv", 'r') as f:
        for line in f.readlines():
            serial, nmr_frame, pdb_id, gdt_ts, lddt, lddt_coverage, native_contract, pred_dope, pred_molpdf, rmsd, tm_score = line.split(
                ',')
            if pdb_id == PDB_ID:
                metrics.append(('TM-score', tm_score[:4]))
                metrics.append(('GDT-TS', gdt_ts[:5]))
                metrics.append(('lDDT', lddt[:4]))
                metrics.append(('Q', native_contract[:4]))
                break

    panel = {
        "image": image,
        "source_crop_index": i,
        "model": name,
        "text_start_row": 240,   # row where text begins in THIS panel's source crop
        "metrics": metrics,
    }

    PANELS.append(panel)


# PANELS = [
#     {
#         # None = crop from SOURCE_IMAGE
#         "image": f"{SOURCE_PATH}/{PDB_ID}-AF2_aligned.png",
#         "source_crop_index": 0,
#         "model": "AlphaFold2",
#         "text_start_row": 240,   # row where text begins in THIS panel's source crop
#         "metrics": [
#             ("RMSD",     "0.05 Å"),
#             ("TM-score", "0.95"),
#             ("GDT TS",   "100"),
#             ("IDDT",     "0.84"),
#             ("Q",        "0.98"),
#         ],
#     },
#     {
#         "image": f"{SOURCE_PATH}/{PDB_ID}-RF2_aligned.png",
#         "source_crop_index": 1,
#         "model": "RoseTTAFold2",
#         "text_start_row": 240,
#         "metrics": [
#             ("RMSD",     "0.05 Å"),
#             ("TM-score", "0.95"),
#             ("GDT TS",   "99.47"),
#             ("IDDT",     "0.85"),
#             ("Q",        "0.99"),
#         ],
#     },
#     {
#         "image": f"{SOURCE_PATH}/{PDB_ID}-ESM_aligned.png",
#         "source_crop_index": 2,
#         "model": "ESMFold",
#         "text_start_row": 240,
#         "metrics": [
#             ("RMSD",     "0.05 Å"),
#             ("TM-score", "0.95"),
#             ("GDT TS",   "98.9"),
#             ("IDDT",     "0.86"),
#             ("Q",        "0.99"),
#         ],
#     },
#     {
#         "image": f"{SOURCE_PATH}/{PDB_ID}-OMF_aligned.png",
#         "source_crop_index": 3,
#         "model": "OmegaFold",
#         "text_start_row": 240,
#         "metrics": [
#             ("RMSD",     "0.04 Å"),
#             ("TM-score", "0.96"),
#             ("GDT TS",   "100"),
#             ("IDDT",     "0.85"),
#             ("Q",        "0.99"),
#         ],
#     },
#     {
#         "image": f"{SOURCE_PATH}/{PDB_ID}-DMP_aligned.png",
#         "source_crop_index": 4,
#         "model": "DMPfold2",
#         "text_start_row": 240,
#         "metrics": [
#             ("RMSD",     "0.11 Å"),
#             ("TM-score", "0.83"),
#             ("GDT TS",   "90.9"),
#             ("IDDT",     "0.67"),
#             ("Q",        "0.94"),
#         ],
#     },
# ]

# ─────────────────────────────────────────────────────────────────
# Layout constants
# ─────────────────────────────────────────────────────────────────

PANEL_W = 640
PANEL_H = 480
LINE_HEIGHT = 36
FONT_SIZE = 36
TITLE_SIZE = 36
TEXT_X = 18
TEXT_COLOR = (0, 0, 0)
WHITE = (255, 255, 255, 128)
OUTPUT_PATH = f"./gen/{CLASS}_{PDB_ID}.png"

# ─────────────────────────────────────────────────────────────────
# Font helpers
# ─────────────────────────────────────────────────────────────────


def load_font(size, bold=False):
    suffix = "-Bold" if bold else ""
    candidates = [
        # f"./OpenSans-VariableFont_wdth,wght.ttf",
        f"./OpenSans_Condensed-{'Bold' if bold else 'Regular'}.ttf",
        # f"/usr/share/fonts/truetype/freefont/FreeSans{'Bold' if bold else ''}.ttf",
    ]
    for p in candidates:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


font_reg = load_font(FONT_SIZE,  bold=False)
font_bold = load_font(TITLE_SIZE, bold=True)

# ─────────────────────────────────────────────────────────────────
# Load source image
# ─────────────────────────────────────────────────────────────────

# source = Image.open(SOURCE_IMAGE).convert("RGBA")
# src_w, _ = source.size
# src_pw = src_w // len(PANELS)


def get_struct(panel) -> Image.Image:
    """Return full-height structure crop (or external image)."""
    if panel["image"] and os.path.exists(panel["image"]):
        img = Image.open(panel["image"]).convert("RGBA")

        if HFLIP:
            img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

        if VFLIP:
            img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

        return img.resize((PANEL_W, PANEL_H), Image.LANCZOS)
    # idx = panel["source_crop_index"]
    # left = idx * src_pw
    # cropped = source.crop((left, 0, left + src_pw, PANEL_H))
    # return cropped.resize((PANEL_W, PANEL_H), Image.LANCZOS)

# ─────────────────────────────────────────────────────────────────
# Compose final canvas
# ─────────────────────────────────────────────────────────────────


canvas = Image.new("RGBA", (PANEL_W * len(PANELS),
                   PANEL_H), (255, 255, 255, 255))

for col, panel in enumerate(PANELS):
    x0 = col * PANEL_W
    # print(x0)
    tsr = 240   # text start row in source (pre-resize)

    # Paste full-height structure panel
    struct = get_struct(panel)

    overlay = Image.new("RGBA", struct.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Erase the baked-in text region with a white rectangle
    draw.rectangle([0, tsr, 0 + 210, PANEL_H], fill=WHITE)

    # Draw metric lines
    y = tsr
    for key, val in panel["metrics"]:
        label = f"RMSD: {val}" if key == "RMSD" else f"{key}: {val}"
        draw.text((0 + TEXT_X, y), label, font=font_reg, fill=TEXT_COLOR)
        y += LINE_HEIGHT

    # Draw bold model name
    draw.text((0 + TEXT_X, y), panel["model"],
              font=font_bold, fill=TEXT_COLOR)

    composite = Image.alpha_composite(struct, overlay)
    canvas.paste(composite, (x0, 0), composite)

    # if col == 1:
    #     canvas.convert("RGB").save(OUTPUT_PATH, "PNG", dpi=(150, 150))
    #     exit()


# ─────────────────────────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────────────────────────

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
canvas.convert("RGB").save(OUTPUT_PATH, "PNG", dpi=(150, 150))
print(f"✓ Saved → {OUTPUT_PATH}  ({PANEL_W * len(PANELS)}×{PANEL_H} px)")
