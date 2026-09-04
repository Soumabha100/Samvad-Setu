"""
=============================================================================
Samvad-Setu: Civic Innovation Platform (Part B - Multimodal AI Engine)
Module: Part B - Unified Image Verification & Voice Triage Service
=============================================================================
Description:
    Unified FastAPI application for multimodal civic grievance verification:
    1. Vision Model (YOLO11): Detects potholes, garbage, cracks, open manholes,
       waterlogging, stray animals, traffic lights, and overflowing waste containers.
    2. Voice Engine (Whisper + Part A NLP): Transcribes citizen audio and
       routes through municipal department classification and SLA triage.
    3. Multimodal Verification: Verifies image evidence alongside citizen reports.

To run manually in your terminal on Port 8000:
    cd part-b
    uvicorn main:app --reload 
=============================================================================
"""

import sys
import shutil
import uuid
from pathlib import Path
from typing import Optional, List, Dict, Any

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore
    except AttributeError:
        pass

# pyrefly: ignore [missing-import]
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status, Request
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO  # type: ignore

# -----------------------------------------------------------------------------
# Module Paths & Imports
# -----------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "image"
VOICE_DIR = BASE_DIR / "voice"
MODELS_DIR = BASE_DIR / "models"

# Add image and voice folders to sys.path for local module resolution
for d in [str(IMAGE_DIR), str(VOICE_DIR)]:
    if d not in sys.path:
        sys.path.insert(0, d)

from severity import calculate_severity  # type: ignore
from whisper_service import process_voice_complaint, ALLOWED_EXTENSIONS as ALLOWED_AUDIO_EXTENSIONS  # type: ignore

# -----------------------------------------------------------------------------
# Model Initialization
# -----------------------------------------------------------------------------

VISION_MODEL_PATH = MODELS_DIR / "vision_model.pt"
if not VISION_MODEL_PATH.exists():
    VISION_MODEL_PATH = IMAGE_DIR / "runs" / "detect" / "train-2" / "weights" / "best.pt"

vision_model = YOLO(str(VISION_MODEL_PATH))

# Temporary upload folder for uploaded files
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


# -----------------------------------------------------------------------------
# FastAPI App
# -----------------------------------------------------------------------------

app = FastAPI(
    title="Samvad-Setu Part B: Multimodal AI Engine",
    description="Unified API for Civic Issue Computer Vision Detection, Voice Transcription & SLA Triage",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------

def run_vision_inference(image_path: Path) -> Dict[str, Any]:
    """Runs YOLO vision model on an image and returns structured detections."""
    results = vision_model(str(image_path), conf=0.25)
    detections = []

    for result in results:
        if result.boxes is None or len(result.boxes) == 0:
            continue

        for box in result.boxes:
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            issue_type = vision_model.names[class_id]
            severity = calculate_severity(issue_type, confidence)

            detections.append({
                "issue": issue_type,
                "confidence": round(confidence, 3),
                "severity": severity
            })

    if not detections:
        return {
            "detected": False,
            "message": "No civic issue detected in the image.",
            "objects_detected": 0,
            "detections": []
        }

    # Determine overall incident severity
    if any(d["issue"] in ("open_manhole", "waterlogging") and d["severity"] == "CRITICAL" for d in detections) or any(d["issue"] == "open_manhole" for d in detections):
        overall_severity = "CRITICAL"
    elif any(d["severity"] == "HIGH" for d in detections):
        overall_severity = "HIGH"
    elif any(d["severity"] == "MEDIUM" for d in detections):
        overall_severity = "MEDIUM"
    else:
        overall_severity = "LOW"

    # Most frequent detected issue
    issue_counts = {}
    for d in detections:
        issue_counts[d["issue"]] = issue_counts.get(d["issue"], 0) + 1
    overall_issue = max(issue_counts, key=issue_counts.get)  # type: ignore

    return {
        "detected": True,
        "overall_issue": overall_issue,
        "overall_severity": overall_severity,
        "objects_detected": len(detections),
        "detections": detections
    }


# -----------------------------------------------------------------------------
# API Endpoints
# -----------------------------------------------------------------------------

@app.get("/")
def home():
    """Service status and available multimodal endpoints."""
    return {
        "status": "online",
        "service": "Samvad-Setu Part B Multimodal AI Engine",
        "vision_model": "YOLO11n (Civic Issue Detector)",
        "supported_vision_classes": [
            "pothole", "garbage", "crack", "open_manhole",
            "waterlogging", "stray_animal", "traffic_light", "waste_container"
        ],
        "voice_engine": "OpenAI Whisper + Part A NLP Triage",
        "endpoints": {
            "GET /": "Health check & metadata",
            "POST /image/predict": "Upload image file for civic issue detection & severity",
            "POST /voice/process": "Upload audio recording for voice-to-text & NLP triage",
            "POST /verify/multimodal": "Submit photo + voice/text for unified verification"
        }
    }


@app.post("/image/predict")
async def predict_image(file: UploadFile = File(...)):
    """
    Upload a civic grievance image (form-data: 'file').
    - Detects: pothole, garbage, crack, open_manhole, waterlogging,
      stray_animal, traffic_light, and waste_container.
    - Computes object-level and overall incident severity.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported image format '{ext}'. Allowed: {', '.join(sorted(ALLOWED_IMAGE_EXTENSIONS))}"
        )

    file_id = uuid.uuid4().hex[:8]
    temp_path = UPLOAD_DIR / f"img_{file_id}{ext}"

    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = run_vision_inference(temp_path)
        result["file_name"] = file.filename
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image processing error: {str(e)}")
    finally:
        if temp_path.exists():
            try:
                temp_path.unlink()
            except Exception:
                pass


@app.post("/voice/process")
async def process_voice(file: UploadFile = File(...)):
    """
    Upload a citizen voice report (form-data: 'file').
    - Verifies audio format and size.
    - Transcribes speech to text using Whisper.
    - Automatically routes grievance to municipal department with SLA deadline.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_AUDIO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio format '{ext}'. Allowed: {', '.join(sorted(ALLOWED_AUDIO_EXTENSIONS))}"
        )

    file_id = uuid.uuid4().hex[:8]
    temp_path = UPLOAD_DIR / f"audio_{file_id}{ext}"

    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = process_voice_complaint(temp_path)
        if result.get("status") == "failed":
            raise HTTPException(status_code=422, detail=result.get("error"))
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice processing error: {str(e)}")
    finally:
        if temp_path.exists():
            try:
                temp_path.unlink()
            except Exception:
                pass


@app.post("/verify/multimodal")
async def verify_multimodal(
    request: Request,
    image: Optional[UploadFile] = File(None),
    audio: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None)
):
    """
    Unified multimodal verification endpoint.
    Accepts any combination of:
    - Image photo evidence (Key: 'image', 'photo', or 'file')
    - Voice audio recording (Key: 'audio', 'voice', or 'file')
    - Written complaint text (Key: 'text' or 'description')
    """
    response = {
        "status": "success",
        "vision_evidence": None,
        "voice_evidence": None,
        "final_assessment": {}
    }

    # Automatically inspect all uploaded files in the form to prevent key-name mismatch errors
    try:
        form = await request.form()
        for field_name, form_value in form.multi_items():
            if hasattr(form_value, "filename") and form_value.filename:
                file_ext = Path(form_value.filename).suffix.lower()
                if file_ext in ALLOWED_IMAGE_EXTENSIONS and (image is None or not getattr(image, "filename", None)):
                    image = form_value
                elif file_ext in ALLOWED_AUDIO_EXTENSIONS and (audio is None or not getattr(audio, "filename", None)):
                    audio = form_value
            elif isinstance(form_value, str) and form_value.strip() and not text:
                if field_name.lower() in ("text", "description", "complaint", "message", "details"):
                    text = form_value
    except Exception:
        pass

    # Process Image if provided
    if image and image.filename:
        ext = Path(image.filename).suffix.lower()
        if ext in ALLOWED_IMAGE_EXTENSIONS:
            file_id = uuid.uuid4().hex[:8]
            temp_img = UPLOAD_DIR / f"multi_img_{file_id}{ext}"
            try:
                with open(temp_img, "wb") as buffer:
                    shutil.copyfileobj(image.file, buffer)
                response["vision_evidence"] = run_vision_inference(temp_img)
            except Exception as e:
                response["vision_evidence"] = {"error": f"Failed to process image: {str(e)}"}
            finally:
                if temp_img.exists():
                    temp_img.unlink()

    # Process Audio if provided
    if audio and audio.filename:
        ext = Path(audio.filename).suffix.lower()
        if ext in ALLOWED_AUDIO_EXTENSIONS:
            file_id = uuid.uuid4().hex[:8]
            temp_audio = UPLOAD_DIR / f"multi_audio_{file_id}{ext}"
            try:
                with open(temp_audio, "wb") as buffer:
                    shutil.copyfileobj(audio.file, buffer)
                response["voice_evidence"] = process_voice_complaint(temp_audio)
            except Exception as e:
                response["voice_evidence"] = {"error": f"Failed to process audio: {str(e)}"}
            finally:
                if temp_audio.exists():
                    temp_audio.unlink()

    # Process written text if provided
    if text and text.strip():
        # pyrefly: ignore [missing-import]
        from whisper_service import triage_with_part_a
        response["text_evidence"] = triage_with_part_a(text.strip())

    # Cross-reference overall severity
    severities = []
    if response["vision_evidence"] and response["vision_evidence"].get("detected"):
        severities.append(response["vision_evidence"].get("overall_severity", "LOW"))
    if response["voice_evidence"] and response["voice_evidence"].get("nlp_triage"):
        severities.append(response["voice_evidence"]["nlp_triage"].get("severity", "low").upper())
    elif response.get("text_evidence") and response["text_evidence"].get("severity"):
        severities.append(response["text_evidence"]["severity"].upper())

    if "CRITICAL" in severities:
        unified_severity = "CRITICAL"
    elif "HIGH" in severities:
        unified_severity = "HIGH"
    elif "MEDIUM" in severities:
        unified_severity = "MEDIUM"
    else:
        unified_severity = "LOW"

    response["final_assessment"] = {
        "unified_severity": unified_severity,
        "verified_with_photo": response["vision_evidence"] is not None and response["vision_evidence"].get("detected", False),
        "verified_with_voice": response["voice_evidence"] is not None and response["voice_evidence"].get("status") == "success"
    }

    return response
