from pathlib import Path
import random
import shutil

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

# Our final common classes
CLASS_MAP = {
    "pothole": 0,
    "garbage": 1,
    "crack": 2,
    "open_manhole": 3,
}


# ============================================================
# CREATE OUTPUT DIRECTORIES
# ============================================================

for folder in IMAGE_DIRS.values():
    folder.mkdir(parents=True, exist_ok=True)

for folder in LABEL_DIRS.values():
    folder.mkdir(parents=True, exist_ok=True)


# ============================================================
# HELPER FUNCTION
# ============================================================

def split_files(files):
    """Split files into 70% train, 15% validation, 15% test."""
    files = files.copy()
    random.shuffle(files)

    total = len(files)

    train_end = int(total * 0.70)
    val_end = int(total * 0.85)

    return (
        files[:train_end],
        files[train_end:val_end],
        files[val_end:]
    )


def copy_sample(image_path, label_lines, split, index, class_id):
    """Copy image and create converted YOLO label."""

    new_name = f"{class_id}_{index}_{image_path.stem}"

    destination_image = IMAGE_DIRS[split] / f"{new_name}{image_path.suffix}"
    destination_label = LABEL_DIRS[split] / f"{new_name}.txt"

    shutil.copy2(image_path, destination_image)

    with open(destination_label, "w", encoding="utf-8") as f:
        for line in label_lines:
            parts = line.strip().split()

            if len(parts) != 5:
                continue

            # Replace original class ID
            parts[0] = str(class_id)

            f.write(" ".join(parts) + "\n")


# ============================================================
# URBAN COMMUNITY ISSUES
# ============================================================

print("\nProcessing Urban Community Issues...")

urban_base = (
    RAW_DIR
    / "Urban Community Issues"
    / "Data_sets"
    / "Data_sets"
)

urban_sources = {
    "pothole": urban_base / "pothole",
    "crack": urban_base / "cracks",
    "open_manhole": urban_base / "open_manhole",
}

counter = 0

for category, folder in urban_sources.items():

    image_folder = folder / "images"
    label_folder = folder / "labels"

    if not image_folder.exists():
        print(f"WARNING: Missing {image_folder}")
        continue

    images = [
        p for p in image_folder.iterdir()
        if p.suffix.lower() in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]
    ]

    print(f"{category}: {len(images)} images")

    train, val, test = split_files(images)

    for split, files in [
        ("train", train),
        ("val", val),
        ("test", test)
    ]:

        for image_path in files:

            label_path = label_folder / f"{image_path.stem}.txt"

            if not label_path.exists():
                continue

            with open(label_path, "r", encoding="utf-8") as f:
                labels = f.readlines()

            copy_sample(
                image_path,
                labels,
                split,
                counter,
                CLASS_MAP[category]
            )

            counter += 1


# ============================================================
# GARBAGE DETECTION
# ============================================================

print("\nProcessing Garbage Detection...")

garbage_base = (
    RAW_DIR
    / "garbage_detection"
    / "GARBAGE CLASSIFICATION"
)

garbage_train = garbage_base / "train"

garbage_image_folder = garbage_train / "images"
garbage_label_folder = garbage_train / "labels"

if garbage_image_folder.exists():

    garbage_images = [
        p for p in garbage_image_folder.iterdir()
        if p.suffix.lower() in [".jpg", ".jpeg", ".png", ".bmp", ".webp"]
    ]

    # Limit the number for a fast prototype
    random.shuffle(garbage_images)
    garbage_images = garbage_images[:600]

    print(f"Using {len(garbage_images)} garbage images")

    train, val, test = split_files(garbage_images)

    for split, files in [
        ("train", train),
        ("val", val),
        ("test", test)
    ]:

        for image_path in files:

            label_path = garbage_label_folder / f"{image_path.stem}.txt"

            if not label_path.exists():
                continue

            with open(label_path, "r", encoding="utf-8") as f:
                labels = f.readlines()

            # All six garbage categories become ONE class: garbage
            copy_sample(
                image_path,
                labels,
                split,
                counter,
                CLASS_MAP["garbage"]
            )

            counter += 1

else:
    print("WARNING: Garbage dataset folder not found!")


# ============================================================
# SUMMARY
# ============================================================

print("\n======================================")
print("DATASET PREPARATION COMPLETE")
print("======================================")

for split in ["train", "val", "test"]:

    image_count = len(list(IMAGE_DIRS[split].glob("*")))
    label_count = len(list(LABEL_DIRS[split].glob("*.txt")))

    print(
        f"{split.upper():5} -> "
        f"{image_count} images, "
        f"{label_count} labels"
    )

print("\nClasses:")
print("0 = pothole")
print("1 = garbage")
print("2 = crack")
print("3 = open_manhole")

print("\nProcessed dataset:")
print(PROCESSED_DIR)