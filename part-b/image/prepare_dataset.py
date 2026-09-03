"""
=============================================================================
Samvad-Setu: Civic Innovation Platform (Part B - Dataset Preparation Engine)
Module: Part B - 8-Class Unified Civic Issue Dataset Builder
=============================================================================
Classes:
    0: pothole         (Road Safety - PWD Roads)
    1: garbage         (Sanitation - Solid Waste Dept)
    2: crack           (Structural - PWD Roads)
    3: open_manhole    (Critical Hazard - PHED Drainage)
    4: waterlogging    (Flooding - PHED Drainage / Stormwater)
    5: stray_animal    (Road Hazard - Animal Control & Safety)
    6: traffic_light   (Signals - Traffic Police & Electrical)
    7: waste_container (Sanitation - Community Bin Maintenance)
=============================================================================
"""

import sys
import shutil
import random
from pathlib import Path
# pyrefly: ignore [missing-import]
from PIL import Image
# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]
import cv2 # type: ignore

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore
    except AttributeError:
        pass

# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "dataset" / "raw"
PROCESSED_DIR = BASE_DIR / "dataset" / "processed"

IMAGE_DIRS = {
    "train": PROCESSED_DIR / "images" / "train",
    "val": PROCESSED_DIR / "images" / "val",
    "test": PROCESSED_DIR / "images" / "test",
}

LABEL_DIRS = {
    "train": PROCESSED_DIR / "labels" / "train",
    "val": PROCESSED_DIR / "labels" / "val",
    "test": PROCESSED_DIR / "labels" / "test",
}

# 8 Unified Civic Classes
CLASS_MAP = {
    "pothole": 0,
    "garbage": 1,
    "crack": 2,
    "open_manhole": 3,
    "waterlogging": 4,
    "stray_animal": 5,
    "traffic_light": 6,
    "waste_container": 7,
}

CLASS_NAMES = {v: k for k, v in CLASS_MAP.items()}


# ============================================================
# RESET AND INITIALIZE OUTPUT DIRECTORIES
# ============================================================

print("Initializing processed dataset directories...")
for folder in list(IMAGE_DIRS.values()) + list(LABEL_DIRS.values()):
    if folder.exists():
        shutil.rmtree(folder)
    folder.mkdir(parents=True, exist_ok=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def split_files(files):
    """Split files into 70% train, 15% val, 15% test."""
    files = files.copy()
    random.seed(42)
    random.shuffle(files)
    total = len(files)
    train_end = int(total * 0.70)
    val_end = int(total * 0.85)
    return files[:train_end], files[train_end:val_end], files[val_end:]


def copy_sample(image_path, label_lines, split, index, class_id):
    """Copy image and create re-indexed YOLO label file."""
    if not label_lines:
        return False

    new_name = f"{class_id}_{index:05d}_{image_path.stem}"
    dest_image = IMAGE_DIRS[split] / f"{new_name}{image_path.suffix.lower()}"
    dest_label = LABEL_DIRS[split] / f"{new_name}.txt"

    shutil.copy2(image_path, dest_image)

    with open(dest_label, "w", encoding="utf-8") as f:
        for line in label_lines:
            parts = line.strip().split()
            if len(parts) != 5:
                continue
            parts[0] = str(class_id)
            f.write(" ".join(parts) + "\n")
    return True


# ============================================================
# 1. URBAN COMMUNITY ISSUES (pothole, crack, open_manhole, animal, traffic_lights, waste_container)
# ============================================================

print("\n--- 1. Processing Urban Community Issues ---")
urban_base = RAW_DIR / "Urban Community Issues" / "Data_sets" / "Data_sets"

urban_sources = {
    "pothole": (urban_base / "pothole", 300),
    "crack": (urban_base / "cracks", 200),
    "open_manhole": (urban_base / "open_manhole", 200),
    "stray_animal": (urban_base / "animal", 400),
    "traffic_light": (urban_base / "traffic_lights", 400),
    "waste_container": (urban_base / "waste_container", 400),
}

sample_counter = 0

for category, (folder, limit) in urban_sources.items():
    image_folder = folder / "images"
    label_folder = folder / "labels"

    if not image_folder.exists() or not label_folder.exists():
        print(f"  [WARN] Skipping missing category: {category} ({folder})")
        continue

    images = [
        p for p in image_folder.iterdir()
        if p.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]
    ]
    random.seed(42)
    random.shuffle(images)
    if limit and len(images) > limit:
        images = images[:limit]

    print(f"  {category:<16}: {len(images)} images")
    train, val, test = split_files(images)

    for split, files in [("train", train), ("val", val), ("test", test)]:
        for image_path in files:
            label_path = label_folder / f"{image_path.stem}.txt"
            if not label_path.exists():
                continue

            with open(label_path, "r", encoding="utf-8") as f:
                labels = [l.strip() for l in f.readlines() if l.strip()]

            if labels:
                copy_sample(image_path, labels, split, sample_counter, CLASS_MAP[category])
                sample_counter += 1


# ============================================================
# 2. GARBAGE DETECTION (garbage)
# ============================================================

print("\n--- 2. Processing Garbage Detection ---")
garbage_base = RAW_DIR / "garbage_detection" / "GARBAGE CLASSIFICATION"
garbage_train = garbage_base / "train"

garbage_images = [
    p for p in (garbage_train / "images").iterdir()
    if p.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp"]
]
random.seed(42)
random.shuffle(garbage_images)
garbage_images = garbage_images[:500]  # Balanced count

print(f"  garbage         : {len(garbage_images)} images")
train, val, test = split_files(garbage_images)

for split, files in [("train", train), ("val", val), ("test", test)]:
    for image_path in files:
        label_path = garbage_train / "labels" / f"{image_path.stem}.txt"
        if not label_path.exists():
            continue

        with open(label_path, "r", encoding="utf-8") as f:
            labels = [l.strip() for l in f.readlines() if l.strip()]

        if labels:
            copy_sample(image_path, labels, split, sample_counter, CLASS_MAP["garbage"])
            sample_counter += 1


# ============================================================
# 3. ROADWAY FLOODING (waterlogging: Mask to YOLO Bounding Box)
# ============================================================

print("\n--- 3. Processing Roadway Flooding (Waterlogging) ---")
flood_base = RAW_DIR / "Roadway Flooding" / "Dataset"
flood_img_dir = flood_base / "images"
flood_lbl_dir = flood_base / "labels"

flood_images = sorted([
    p for p in flood_img_dir.iterdir()
    if p.suffix.lower() in [".jpg", ".jpeg", ".png"]
])
print(f"  waterlogging    : {len(flood_images)} images")
train, val, test = split_files(flood_images)

for split, files in [("train", train), ("val", val), ("test", test)]:
    for image_path in files:
        # Match image_X.jpg with label_X.png
        index_str = image_path.stem.replace("image_", "")
        mask_path = flood_lbl_dir / f"label_{index_str}.png"
        if not mask_path.exists():
            continue

        try:
            mask = np.array(Image.open(mask_path), dtype=np.uint8)
            h, w = mask.shape[:2]
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            yolo_boxes = []
            for cnt in contours:
                x, y, bw, bh = cv2.boundingRect(cnt)
                # Filter out minor noise specks (minimum 150 square pixels)
                if bw * bh < 150:
                    continue

                x_center = (x + bw / 2.0) / w
                y_center = (y + bh / 2.0) / h
                norm_w = bw / float(w)
                norm_h = bh / float(h)

                yolo_boxes.append(f"{CLASS_MAP['waterlogging']} {x_center:.6f} {y_center:.6f} {norm_w:.6f} {norm_h:.6f}")

            if yolo_boxes:
                copy_sample(image_path, yolo_boxes, split, sample_counter, CLASS_MAP["waterlogging"])
                sample_counter += 1
        except Exception:
            continue


# ============================================================
# 4. GENERATE data.yaml
# ============================================================

data_yaml_path = PROCESSED_DIR / "data.yaml"
names_yaml = "\n".join([f"  {v}: {k}" for v, k in sorted(CLASS_NAMES.items())])

yaml_content = f"""path: {PROCESSED_DIR.as_posix()}

train: images/train
val: images/val
test: images/test

names:
{names_yaml}
"""

with open(data_yaml_path, "w", encoding="utf-8") as f:
    f.write(yaml_content)

print(f"\nGenerated updated: {data_yaml_path}")


# ============================================================
# DATASET SUMMARY
# ============================================================

print("\n" + "=" * 60)
print(" 8-CLASS CIVIC DATASET PREPARATION COMPLETE")
print("=" * 60)

for split in ["train", "val", "test"]:
    img_cnt = len(list(IMAGE_DIRS[split].glob("*")))
    lbl_cnt = len(list(LABEL_DIRS[split].glob("*.txt")))
    print(f" {split.upper():<5} -> {img_cnt} images, {lbl_cnt} label files")

print("\nClass Index Mapping:")
for v, k in sorted(CLASS_NAMES.items()):
    print(f"  {v}: {k}")
print("=" * 60 + "\n")