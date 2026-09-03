from fastapi import FastAPI, UploadFile, File
from pathlib import Path
import shutil
import uuid

from ultralytics import YOLO  # type: ignore
from severity import calculate_severity


# ============================================================
# APP
# ============================================================

app = FastAPI(
    title="Samvad Setu AI - Image Verification API",
    description="AI-based civic issue detection and severity analysis",
    version="1.0"
)


# ============================================================
# MODEL
# ============================================================

MODEL_PATH = "../models/vision_model.pt"

model = YOLO(MODEL_PATH)


# ============================================================
# UPLOAD DIRECTORY
# ============================================================

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def home():
    return {
        "message": "Samvad Setu AI Image Verification API is running",
        "model": "YOLO11n",
        "classes": [
            "pothole",
            "garbage",
            "crack",
            "open_manhole"
        ]
    }


# ============================================================
# IMAGE PREDICTION
# ============================================================

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):

    # Create unique filename
    file_id = str(uuid.uuid4())

    extension = Path(file.filename).suffix       #type:ignore

    image_path = UPLOAD_DIR / f"{file_id}{extension}"

    # Save uploaded image
    with open(image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)


    # Run YOLO
    results = model(
        str(image_path),
        conf=0.25
    )


    detections = []


    # ========================================================
    # COLLECT DETECTIONS
    # ========================================================

    for result in results:

        if result.boxes is None:
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
                "confidence": round(confidence, 3),
                "severity": severity
            })


    # ========================================================
    # NO DETECTION
    # ========================================================

    if not detections:

        return {
            "success": True,
            "detected": False,
            "message": "No civic issue detected",
            "detections": []
        }


    # ========================================================
    # OVERALL SEVERITY
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


    # ========================================================
    # OVERALL ISSUE
    # ========================================================

    issue_counts = {}

    for d in detections:

        issue = d["issue"]

        issue_counts[issue] = (
            issue_counts.get(issue, 0) + 1
        )


    overall_issue = max(
        issue_counts,
        key=issue_counts.get # type: ignore
    ) # type: ignore


    # ========================================================
    # RESPONSE
    # ========================================================

    return {
        "success": True,
        "detected": True,
        "overall_issue": overall_issue,
        "overall_severity": overall_severity,
        "objects_detected": len(detections),
        "detections": detections
    }