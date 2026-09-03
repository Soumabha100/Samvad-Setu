import sys
from pathlib import Path

from ultralytics import YOLO   # type: ignore
from severity import calculate_severity


# ============================================================
# MODEL
# ============================================================

MODEL_PATH = "./runs/detect/train-2/weights/best.pt"

model = YOLO(MODEL_PATH)


# ============================================================
# GET IMAGE
# ============================================================

if len(sys.argv) < 2:
    print("Usage: python predict.py <image_path>")
    print("Example: python predict.py test2.jpg")
    sys.exit(1)

image_path = sys.argv[1]

if not Path(image_path).exists():
    print(f"ERROR: Image not found: {image_path}")
    sys.exit(1)


# ============================================================
# PREDICTION
# ============================================================

results = model(image_path, conf=0.25)


# ============================================================
# COLLECT DETECTIONS
# ============================================================

detections = []

for result in results:

    if result.boxes is None or len(result.boxes) == 0:
        continue

    for box in result.boxes:

        class_id = int(box.cls[0])
        confidence = float(box.conf[0])

        issue_type = model.names[class_id]

        severity = calculate_severity(
            issue_type,
            confidence
        )

        detections.append({
            "issue": issue_type,
            "confidence": confidence,
            "severity": severity
        })


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n========== SAMVAD SETU AI ==========\n")

if not detections:

    print("No civic issue detected.")

else:

    print(f"Detected objects: {len(detections)}\n")

    for i, detection in enumerate(detections, start=1):

        print(f"Object #{i}")
        print(f"Issue       : {detection['issue']}")
        print(f"Confidence  : {detection['confidence']:.2f}")
        print(f"Severity    : {detection['severity']}")
        print("-----------------------------------")


    # ========================================================
    # OVERALL INCIDENT SEVERITY
    # ========================================================

    if any(
        d["issue"] == "open_manhole"
        for d in detections
    ):
        overall_severity = "CRITICAL"

    elif any(
        d["severity"] == "HIGH"
        for d in detections
    ):
        overall_severity = "HIGH"

    elif any(
        d["severity"] == "MEDIUM"
        for d in detections
    ):
        overall_severity = "MEDIUM"

    else:
        overall_severity = "LOW"


    # Most common detected issue
    issue_counts = {}

    for d in detections:
        issue = d["issue"]
        issue_counts[issue] = issue_counts.get(issue, 0) + 1

    overall_issue = max(
        issue_counts,
        key=issue_counts.get # type: ignore
    ) # type: ignore


    print("\n========== INCIDENT SUMMARY ==========")
    print(f"Overall Issue    : {overall_issue}")
    print(f"Objects Detected : {len(detections)}")
    print(f"Overall Severity : {overall_severity}")
    print("======================================")