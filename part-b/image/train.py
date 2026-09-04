"""
=============================================================================
Samvad-Setu: Civic Innovation Platform (Part B - Model Training Pipeline)
Module: Part B - YOLO11 Training Engine (8 Civic Issue Classes)
=============================================================================
Description:
    Trains the YOLO11 model on the 8-class processed civic issue dataset:
    (pothole, garbage, crack, open_manhole, waterlogging, stray_animal,
     traffic_light, waste_container).
    Automatically saves and exports best weights to 'part-b/models/vision_model.pt'.

Usage:
    python train.py --epochs 5 --batch 8 --imgsz 640
=============================================================================
"""

import sys
import shutil
import argparse
from pathlib import Path
from ultralytics import YOLO  # type: ignore

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore
    except AttributeError:
        pass

BASE_DIR = Path(__file__).resolve().parent
DATA_YAML = BASE_DIR / "dataset" / "processed" / "data.yaml"
BASE_MODEL = BASE_DIR / "yolo11n.pt"
OUTPUT_MODEL_DIR = BASE_DIR.parent / "models"
OUTPUT_MODEL_PATH = OUTPUT_MODEL_DIR / "vision_model.pt"


def train_yolo(epochs: int = 5, batch: int = 8, imgsz: int = 640, device: str = ""):
    """Trains YOLO model on the 8-class civic dataset."""
    if not DATA_YAML.exists():
        print(f"[ERROR] Processed data.yaml not found at {DATA_YAML}")
        print("Please run 'python prepare_dataset.py' first!")
        sys.exit(1)

    print("=" * 70)
    print(" SAMVAD-SETU : PART B COMPUTER VISION TRAINING PIPELINE (8 CLASSES)")
    print("=" * 70)
    print(f"Data config   : {DATA_YAML}")
    print(f"Base weights  : {BASE_MODEL}")
    print(f"Epochs        : {epochs}")
    print(f"Batch size    : {batch}")
    print(f"Image size    : {imgsz}")
    print("=" * 70 + "\n")

    # Initialize model
    model = YOLO(str(BASE_MODEL))

    # Start training
    results = model.train(
        data=str(DATA_YAML),
        epochs=epochs,
        batch=batch,
        imgsz=imgsz,
        device=device if device else ("0" if model.device.type == "cuda" else "cpu"),
        project=str(BASE_DIR / "runs" / "detect"),
        name="train_8class",
        exist_ok=True,
        verbose=True
    )

    # Export best model
    best_weights = BASE_DIR / "runs" / "detect" / "train_8class" / "weights" / "best.pt"
    if best_weights.exists():
        OUTPUT_MODEL_DIR.mkdir(exist_ok=True)
        shutil.copy2(best_weights, OUTPUT_MODEL_PATH)
        print("\n" + "=" * 70)
        print(" TRAINING COMPLETE & MODEL EXPORTED")
        print("=" * 70)
        print(f" Best Weights Saved To : {best_weights}")
        print(f" Exported Production Model : {OUTPUT_MODEL_PATH}")
        print("=" * 70 + "\n")
    else:
        print("[WARNING] Could not locate best.pt in training directory.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Samvad-Setu 8-Class Civic Issue Vision Model")
    parser.add_argument("--epochs", type=int, default=5, help="Number of training epochs (default: 5)")
    parser.add_argument("--batch", type=int, default=8, help="Batch size (default: 8)")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size (default: 640)")
    parser.add_argument("--device", type=str, default="", help="Device: '0' for CUDA GPU, 'cpu' for CPU")

    args = parser.parse_args()
    train_yolo(epochs=args.epochs, batch=args.batch, imgsz=args.imgsz, device=args.device)
