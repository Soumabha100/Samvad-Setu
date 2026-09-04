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
from typing import Optional, List, Dict, Any, Union
from datetime import datetime

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
from fastapi.responses import FileResponse
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from ultralytics import YOLO  # type: ignore
# pyrefly: ignore [missing-import]
from pydantic import BaseModel

# -----------------------------------------------------------------------------
# Module Paths & Imports
# -----------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
IMAGE_DIR = BASE_DIR / "image"
VOICE_DIR = BASE_DIR / "voice"
MODELS_DIR = BASE_DIR / "models"
ACADEMIC_DIR = BASE_DIR / "academic"
CORPORATE_DIR = BASE_DIR / "corporate"
AGENT_DIR = BASE_DIR.parent / "ai-agent"

# Add image, voice, academic, corporate, and ai-agent folders to sys.path for local module resolution
for d in [str(IMAGE_DIR), str(VOICE_DIR), str(ACADEMIC_DIR), str(CORPORATE_DIR), str(AGENT_DIR), str(BASE_DIR)]:
    if d not in sys.path:
        sys.path.insert(0, d)

import os

# Automatically load the single master environment configuration from ai-engine/.env
MASTER_ENV_FILE = BASE_DIR.parent / ".env"
if MASTER_ENV_FILE.exists():
    try:
        with open(MASTER_ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip("'\"")
                    if k and k not in os.environ:
                        os.environ[k] = v
    except Exception:
        pass

from severity import calculate_severity  # type: ignore
from whisper_service import process_voice_complaint, ALLOWED_EXTENSIONS as ALLOWED_AUDIO_EXTENSIONS  # type: ignore
from academic import (  # type: ignore
    search_institutions,
    get_institution_by_id,
    evaluate_problem_complexity,
    SyllabusMatcher,
    SyllabusCurriculum,
    SAMPLE_SYLLABI,
    evaluate_escalation_eligibility,
    register_chronic_problem_statement,
    get_chronic_problems,
    claim_chronic_problem,
    generate_hei_problem_dossier_pdf,
    CHRONIC_PROBLEMS_POOL
)
from corporate import (  # type: ignore
    register_prototype_submission,
    list_prototypes,
    get_prototype_by_id,
    create_sponsorship_pledge,
    approve_milestone,
    generate_tripartite_agreement_text,
    match_sponsors_for_prototype,
    generate_csr_impact_certificate,
    CORPORATE_SPONSORS_STORE,
    SCHEDULE_VII_CATEGORIES,
    TRL_DESCRIPTIONS
)

# Initialize academic matchers for standard AICTE curricula
ACADEMIC_MATCHERS = {
    key: SyllabusMatcher(SyllabusCurriculum.from_dict(curriculum))
    for key, curriculum in SAMPLE_SYLLABI.items()
}


class ComplexityRequest(BaseModel):
    text: str
    category: Optional[str] = ""
    department: Optional[str] = ""


class SyllabusMatchRequest(BaseModel):
    problem_text: str
    category: Optional[str] = ""
    department_hint: Optional[str] = ""
    target_student_year: Optional[int] = None
    curriculum_key: Optional[str] = "civil_engineering"
    custom_syllabus: Optional[Dict[str, Any]] = None


class EscalationEligibilityRequest(BaseModel):
    status: Optional[str] = "unresolved"
    sla_breached: Optional[bool] = False
    recurrence_count: Optional[int] = 1
    recurrence_period_days: Optional[int] = 0
    failed_resolution_attempts: Optional[int] = 0
    authority_notes: Optional[str] = None


class ChronicProblemRegisterRequest(BaseModel):
    problem_id: Optional[str] = None
    complaint_id: Optional[str] = None
    title: str
    description: str
    category: Optional[str] = "Civic Infrastructure"
    department: Optional[str] = "Public Works Department"
    location: Optional[Union[Dict[str, Any], str]] = None
    coordinates: Optional[Dict[str, Any]] = None
    status: Optional[str] = "unresolved"
    sla_breached: Optional[bool] = True
    recurrence_count: Optional[int] = 3
    recurrence_period_days: Optional[int] = 30
    failed_resolution_attempts: Optional[int] = 2
    authority_notes: Optional[str] = None
    curriculum_key: Optional[str] = "civil_engineering"
    target_student_year: Optional[int] = None


class ClaimProblemRequest(BaseModel):
    escalation_id: str
    institution_name: str
    team_name: str
    student_academic_year: int


class GenerateDossierRequest(BaseModel):
    gemini_api_key: Optional[str] = None


class PrototypeSubmitRequest(BaseModel):
    escalation_id: str
    team_name: str
    institution_name: str
    faculty_mentor: str
    prototype_title: str
    executive_summary: str
    technical_approach: str
    trl_level: Optional[int] = 5
    bill_of_materials: Optional[List[Dict[str, Any]]] = None
    total_funding_required_inr: Optional[float] = 0.0
    demo_video_url: Optional[str] = None
    cad_repo_url: Optional[str] = None
    field_testing_plan: Optional[str] = None
    expected_civic_impact: Optional[Dict[str, Any]] = None
    category: Optional[str] = "road_damage"


class SponsorshipPledgeRequest(BaseModel):
    prototype_id: Optional[str] = None
    sponsor_id: Optional[str] = "CORP-TATA-01"
    pledged_amount_inr: Optional[float] = None
    amount: Optional[float] = None
    corporate_representative_name: Optional[str] = None
    representative_name: Optional[str] = None
    corporate_contact_email: Optional[str] = None
    email: Optional[str] = None
    escrow_terms_accepted: Optional[bool] = True
    civic_commons_license_accepted: Optional[bool] = True


class MilestoneApproveRequest(BaseModel):
    sponsorship_id: str
    tranche_index: int
    approver_role: str  # 'municipal_officer' | 'corporate_auditor' | 'faculty_mentor'
    approver_name: str
    verification_notes: str


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
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}

# Municipal mapping from YOLO vision detections to Part A categories and departments
VISION_TO_PART_A = {
    "pothole": ("road_damage", "Public Works Department (PWD - Roads)"),
    "crack": ("road_damage", "Public Works Department (PWD - Roads)"),
    "garbage": ("garbage", "Solid Waste & Sanitation Department"),
    "waste_container": ("garbage", "Solid Waste & Sanitation Department"),
    "open_manhole": ("drainage", "Public Health Engineering Dept (PHED - Drainage)"),
    "waterlogging": ("waterlogging", "Stormwater & Flood Management Cell"),
    "traffic_light": ("other", "Traffic Police & Electrical Division"),
    "stray_animal": ("other", "Animal Control & Public Safety Unit")
}


def extract_keyframes_from_video(video_path: Path, max_frames: int = 3) -> List[Path]:
    """
    Extracts keyframes from an uploaded video file to analyze through YOLO.
    """
    # pyrefly: ignore [missing-import]
    import cv2
    cap = cv2.VideoCapture(str(video_path))
    frames: List[Path] = []
    if not cap.isOpened():
        return frames

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if total_frames <= 0:
        cap.release()
        return frames

    step = max(1, total_frames // max_frames)
    frame_indices = [i * step for i in range(min(max_frames, total_frames))]

    for idx, f_idx in enumerate(frame_indices):
        cap.set(cv2.CAP_PROP_POS_FRAMES, f_idx)
        ret, frame = cap.read()
        if ret:
            keyframe_path = UPLOAD_DIR / f"vframe_{uuid.uuid4().hex[:8]}_{idx}.jpg"
            cv2.imwrite(str(keyframe_path), frame)
            frames.append(keyframe_path)

    cap.release()
    return frames


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
            "POST /verify/multimodal": "Submit photo + voice/text for unified verification",
            "POST /dedup/check": "Check if an incoming complaint is duplicate of an active ticket",
            "POST /dedup/cluster": "Cluster a batch of raw citizen reports into Master Incident Tickets"
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


# =============================================================================
# DEDUPLICATION & INCIDENT FUSION ENDPOINTS
# =============================================================================

# pyrefly: ignore [missing-import]
from pydantic import BaseModel
from dedup import calculate_incident_similarity, cluster_grievances, merge_reports
import copy


class CheckDuplicateRequest(BaseModel):
    new_report: Dict[str, Any]
    active_reports: List[Dict[str, Any]] = []


@app.post("/dedup/check")
async def check_duplicate(payload: CheckDuplicateRequest):
    """
    Checks if an incoming citizen complaint is a duplicate of any active ticket.
    Returns whether to MERGE into an existing ticket or CREATE a new one.
    """
    new_rep = payload.new_report
    active_reps = payload.active_reports

    best_match = None
    highest_score = 0.0
    best_metrics = {}

    for existing in active_reps:
        sim = calculate_incident_similarity(new_rep, existing)
        if sim["composite_score"] > highest_score:
            highest_score = sim["composite_score"]
            best_metrics = sim["metrics"]
            if sim["is_duplicate"]:
                best_match = existing

    if best_match:
        merged = merge_reports(copy.deepcopy(best_match), new_rep)
        return {
            "status": "success",
            "is_duplicate": True,
            "matched_ticket_id": best_match.get("id") or best_match.get("_id") or best_match.get("master_ticket_id"),
            "similarity_score": highest_score,
            "similarity_metrics": best_metrics,
            "action": "MERGE_INTO_MASTER",
            "merged_incident": merged
        }
    else:
        return {
            "status": "success",
            "is_duplicate": False,
            "matched_ticket_id": None,
            "similarity_score": highest_score,
            "similarity_metrics": best_metrics,
            "action": "CREATE_NEW_MASTER_TICKET"
        }


class ClusterReportsRequest(BaseModel):
    reports: List[Dict[str, Any]]


@app.post("/dedup/cluster")
async def cluster_reports_endpoint(payload: ClusterReportsRequest):
    """
    Takes an array of raw citizen reports and clusters duplicates together,
    returning a consolidated list of Master Incidents with evidence galleries
    and escalated community severity.
    """
    if not payload.reports:
        return {
            "status": "success",
            "raw_reports_count": 0,
            "master_tickets_count": 0,
            "master_tickets": []
        }

    master_tickets = cluster_grievances(payload.reports)
    return {
        "status": "success",
        "raw_reports_count": len(payload.reports),
        "master_tickets_count": len(master_tickets),
        "master_tickets": master_tickets
    }


# =============================================================================
# UNIFIED ALL-IN-ONE CITIZEN SUBMISSION & BACKGROUND DEDUPLICATION PIPELINE
# =============================================================================

ACTIVE_INCIDENTS: List[Dict[str, Any]] = []


@app.post("/incident/submit")
async def submit_incident_automated(
    request: Request,
    file: Optional[UploadFile] = File(None),
    image: Optional[UploadFile] = File(None),
    audio: Optional[UploadFile] = File(None),
    video: Optional[UploadFile] = File(None),
    text: Optional[str] = Form(None),
    citizen_name: Optional[str] = Form(None),
    lat: Optional[float] = Form(None),
    lng: Optional[float] = Form(None),
    address: Optional[str] = Form(None)
):
    """
    Unified All-in-One Grievance Pipeline:
    1. Ingests ANY citizen input: photo, voice audio, video, or text.
    2. Runs Whisper for voice transcription.
    3. Runs YOLO for image/video issue detection.
    4. Runs Part A NLP for municipal department and SLA classification.
    5. Automatically checks deduplication against active neighborhood tickets:
       - If matching incident exists (≤150m, same problem): automatically fuses into Master Ticket!
       - If new: creates a new Master Ticket.
    """
    # 1. Flexible Form-data Extraction (handles any key name used by frontend/Postman)
    uploaded_image_path: Optional[Path] = None
    uploaded_audio_path: Optional[Path] = None
    uploaded_video_path: Optional[Path] = None

    try:
        form = await request.form()
        for field_name, form_value in form.multi_items():
            if hasattr(form_value, "filename") and form_value.filename:
                file_ext = Path(form_value.filename).suffix.lower()
                temp_id = uuid.uuid4().hex[:8]

                if file_ext in ALLOWED_IMAGE_EXTENSIONS and not uploaded_image_path:
                    temp_p = UPLOAD_DIR / f"auto_img_{temp_id}{file_ext}"
                    with open(temp_p, "wb") as buf:
                        shutil.copyfileobj(form_value.file, buf)
                    uploaded_image_path = temp_p

                elif file_ext in ALLOWED_AUDIO_EXTENSIONS and not uploaded_audio_path:
                    temp_p = UPLOAD_DIR / f"auto_aud_{temp_id}{file_ext}"
                    with open(temp_p, "wb") as buf:
                        shutil.copyfileobj(form_value.file, buf)
                    uploaded_audio_path = temp_p

                elif file_ext in ALLOWED_VIDEO_EXTENSIONS and not uploaded_video_path:
                    temp_p = UPLOAD_DIR / f"auto_vid_{temp_id}{file_ext}"
                    with open(temp_p, "wb") as buf:
                        shutil.copyfileobj(form_value.file, buf)
                    uploaded_video_path = temp_p

            elif isinstance(form_value, str) and form_value.strip():
                k = field_name.lower()
                if k in ("text", "description", "complaint", "message") and not text:
                    text = form_value
                elif k in ("name", "citizen_name", "user") and not citizen_name:
                    citizen_name = form_value
                elif k in ("address", "location_name", "landmark") and not address:
                    address = form_value
                elif k == "lat" and lat is None:
                    try:
                        lat = float(form_value)
                    except ValueError:
                        pass
                elif k in ("lng", "lon", "long") and lng is None:
                    try:
                        lng = float(form_value)
                    except ValueError:
                        pass
    except Exception:
        pass

    # 2. Multimodal Feature Extraction
    detected_category = "other"
    detected_department = "General Municipal Helpdesk"
    detected_severity = "medium"
    sla_hours = 72
    final_text = (text or "").strip()
    evidence_image_str = str(uploaded_image_path) if uploaded_image_path else None
    evidence_audio_str = str(uploaded_audio_path) if uploaded_audio_path else None

    # Process Voice Note if provided
    if uploaded_audio_path and uploaded_audio_path.exists():
        try:
            voice_res = process_voice_complaint(uploaded_audio_path)
            if voice_res.get("status") == "success":
                transcribed = voice_res.get("transcription", {}).get("text", "")
                if transcribed:
                    final_text = f"{final_text} (Voice: {transcribed})".strip() if final_text else transcribed
                nlp = voice_res.get("nlp_triage", {})
                if nlp:
                    detected_category = nlp.get("category", detected_category)
                    detected_department = nlp.get("department", detected_department)
                    detected_severity = nlp.get("severity", detected_severity)
                    sla_hours = nlp.get("sla_hours", sla_hours)
        except Exception:
            pass

    # Process Video (extract keyframe) if provided
    if uploaded_video_path and uploaded_video_path.exists():
        try:
            k_frames = extract_keyframes_from_video(uploaded_video_path, max_frames=1)
            if k_frames and k_frames[0].exists():
                uploaded_image_path = k_frames[0]
                evidence_image_str = str(uploaded_image_path)
        except Exception:
            pass

    # Process Image if provided (or from video keyframe)
    if uploaded_image_path and uploaded_image_path.exists():
        try:
            vision_res = run_vision_inference(uploaded_image_path)
            if vision_res.get("detected"):
                issue = vision_res.get("overall_issue")
                if issue in VISION_TO_PART_A:
                    detected_category, detected_department = VISION_TO_PART_A[issue]
                detected_severity = vision_res.get("overall_severity", detected_severity).lower()
                if not final_text:
                    final_text = f"Visual incident: Detected {issue} with {vision_res.get('overall_severity')} severity."
        except Exception:
            pass

    # Process plain text with Part A if still unclassified
    if final_text and detected_category == "other":
        try:
            # pyrefly: ignore [missing-import]
            from whisper_service import triage_with_part_a
            nlp_res = triage_with_part_a(final_text)
            if nlp_res and nlp_res.get("status") == "success":
                detected_category = nlp_res.get("category", detected_category)
                detected_department = nlp_res.get("department", detected_department)
                detected_severity = nlp_res.get("severity", detected_severity)
                sla_hours = nlp_res.get("sla_hours", sla_hours)
        except Exception:
            pass

    # 3. Construct Normalized Incident Object
    new_report = {
        "id": f"rep_{uuid.uuid4().hex[:6]}",
        "citizen_name": citizen_name or "Citizen Reporter",
        "text": final_text or f"Reported {detected_category}",
        "category": detected_category,
        "department": detected_department,
        "severity": detected_severity,
        "sla_hours": sla_hours,
        "location": {"lat": lat, "lng": lng, "address": address or "GPS Location"},
        "image_path": evidence_image_str,
        "audio_path": evidence_audio_str
    }

    # 4. Automatic Background Deduplication & Fusion Check
    matched_master = None
    highest_sim = 0.0

    for active_ticket in ACTIVE_INCIDENTS:
        sim_res = calculate_incident_similarity(new_report, active_ticket)
        if sim_res["is_duplicate"] and sim_res["composite_score"] > highest_sim:
            highest_sim = sim_res["composite_score"]
            matched_master = active_ticket

    if matched_master:
        # MERGE INTO EXISTING MASTER TICKET
        merge_reports(matched_master, new_report)
        return {
            "status": "success",
            "action": "MERGED_INTO_MASTER_TICKET",
            "is_duplicate": True,
            "matched_ticket_id": matched_master["master_ticket_id"],
            "similarity_score": round(highest_sim, 3),
            "message": f"Duplicate incident detected ({round(highest_sim * 100, 1)}% match). Automatically merged into Master Ticket {matched_master['master_ticket_id']}.",
            "master_ticket": matched_master
        }
    else:
        # CREATE NEW MASTER TICKET
        new_master = {
            "master_ticket_id": f"MTR-{len(ACTIVE_INCIDENTS) + 1001}",
            "title": f"Reported {detected_category.replace('_', ' ').title()}",
            "category": detected_category,
            "department": detected_department,
            "severity": detected_severity,
            "sla_hours": sla_hours,
            "location": new_report["location"],
            "citizen_count": 1,
            "evidence_gallery": [evidence_image_str] if evidence_image_str else [],
            "audio_gallery": [evidence_audio_str] if evidence_audio_str else [],
            "citizen_reports": [
                {
                    "report_id": new_report["id"],
                    "citizen_name": new_report["citizen_name"],
                    "text": new_report["text"],
                    # pyrefly: ignore [unknown-name]
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            ],
            "summary": f"Initial report registered for {detected_category.replace('_', ' ')}."
        }
        ACTIVE_INCIDENTS.append(new_master)
        return {
            "status": "success",
            "action": "CREATED_NEW_MASTER_TICKET",
            "is_duplicate": False,
            "matched_ticket_id": None,
            "similarity_score": round(highest_sim, 3),
            "message": f"New civic problem registered. Created Master Ticket {new_master['master_ticket_id']}.",
            "master_ticket": new_master
        }


@app.get("/incidents/active")
def get_active_incidents():
    """Returns all currently registered Master Incident Tickets."""
    return {
        "status": "success",
        "total_active_master_tickets": len(ACTIVE_INCIDENTS),
        "master_tickets": ACTIVE_INCIDENTS
    }


@app.post("/incidents/reset")
def reset_active_incidents():
    """Resets the in-memory active incidents pool."""
    ACTIVE_INCIDENTS.clear()
    return {"status": "success", "message": "Active incidents pool cleared."}


# -----------------------------------------------------------------------------
# Academic & HEI Syllabus Allocation Routes
# -----------------------------------------------------------------------------

@app.get("/academic/institutions")
def get_institutions_endpoint(
    query: Optional[str] = None,
    state: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 20
):
    """
    Search and filter Indian higher education institutions (IITs, NITs, State Univs, etc.)
    by name, AISHE code, state, or tier category.
    """
    results = search_institutions(query=query, state=state, category=category, limit=limit)
    return {
        "status": "success",
        "total_results": len(results),
        "institutions": results
    }


@app.get("/academic/institutions/{institution_id}")
def get_institution_endpoint(institution_id: str):
    """Retrieve details for a specific Indian institution by its identifier."""
    inst = get_institution_by_id(institution_id)
    if not inst:
        raise HTTPException(status_code=404, detail=f"Institution '{institution_id}' not found.")
    return {"status": "success", "institution": inst}


@app.post("/academic/complexity/evaluate")
def evaluate_complexity_endpoint(req: ComplexityRequest):
    """
    Evaluates a problem statement's technical complexity tier (Tier 1-4),
    minimum eligible academic year (1-4), prerequisites, and suggested deliverables.
    """
    res = evaluate_problem_complexity(
        text=req.text,
        category=req.category or "",
        department=req.department or ""
    )
    return {
        "status": "success",
        "complexity": res.to_dict()
    }


@app.get("/academic/sample-syllabi")
def get_sample_syllabi_endpoint():
    """
    Returns available standard AICTE model curricula (Civil, CSE, Environmental)
    with their subjects, academic years, and course outcomes.
    """
    return {
        "status": "success",
        "available_curricula": list(SAMPLE_SYLLABI.keys()),
        "syllabi": SAMPLE_SYLLABI
    }


@app.post("/academic/syllabus/match")
def match_syllabus_endpoint(req: SyllabusMatchRequest):
    """
    Matches a civic problem statement against an institution's curriculum, assigns to
    the Core Department Subject, and enforces the Student Year Safety Guardrail.
    """
    if req.custom_syllabus:
        matcher = SyllabusMatcher(SyllabusCurriculum.from_dict(req.custom_syllabus))
    else:
        key = (req.curriculum_key or "civil_engineering").lower().strip()
        if key not in ACADEMIC_MATCHERS:
            key = "civil_engineering"
        matcher = ACADEMIC_MATCHERS[key]

    match_result = matcher.match_problem(
        problem_text=req.problem_text,
        category=req.category or "",
        department_hint=req.department_hint or "",
        target_student_year=req.target_student_year
    )
    return match_result


# -----------------------------------------------------------------------------
# Chronic Problem & Government Failure Escalation Routes
# -----------------------------------------------------------------------------

@app.post("/academic/escalation/check-eligibility")
def check_escalation_eligibility_endpoint(req: EscalationEligibilityRequest):
    """
    Evaluates whether a municipal incident meets the chronic escalation criteria:
    1. Government authority failed to solve it (SLA breached / failed contractor attempts)
    2. Problem repeatedly recurs over weeks or months indicating systemic engineering failure.
    """
    eligibility = evaluate_escalation_eligibility(
        status=req.status or "unresolved",
        sla_breached=bool(req.sla_breached),
        recurrence_count=req.recurrence_count or 1,
        recurrence_period_days=req.recurrence_period_days or 0,
        failed_resolution_attempts=req.failed_resolution_attempts or 0,
        authority_notes=req.authority_notes
    )
    return {"status": "success", "eligibility": eligibility}


@app.post("/academic/escalation/register")
def register_chronic_problem_endpoint(req: ChronicProblemRegisterRequest):
    """
    Escalates a failed or chronic municipal problem into the Institutional Problem Bank.
    Runs AI complexity analysis, matches to Core Department Subjects, and publishes
    for colleges/universities to adopt.
    """
    pid = req.problem_id or req.complaint_id or f"CIVIC-{uuid.uuid4().hex[:6].upper()}"
    dept = req.department or "Public Works Department"

    loc_dict: Dict[str, Any] = {}
    if isinstance(req.location, dict):
        loc_dict = dict(req.location)
    elif isinstance(req.location, str):
        loc_dict = {"address": req.location}
    else:
        loc_dict = {"address": "Municipal Ward"}

    if req.coordinates and isinstance(req.coordinates, dict):
        loc_dict.update(req.coordinates)

    result = register_chronic_problem_statement(
        problem_id=pid,
        title=req.title,
        description=req.description,
        category=req.category or "Civic Infrastructure",
        department=dept,
        location=loc_dict,
        status=req.status or "unresolved",
        sla_breached=bool(req.sla_breached),
        recurrence_count=req.recurrence_count or 3,
        recurrence_period_days=req.recurrence_period_days or 30,
        failed_resolution_attempts=req.failed_resolution_attempts or 2,
        authority_notes=req.authority_notes,
        curriculum_key=req.curriculum_key or "civil_engineering",
        target_student_year=req.target_student_year
    )
    return result


@app.get("/academic/chronic-problems")
def get_chronic_problems_endpoint(
    department: Optional[str] = None,
    academic_year: Optional[int] = None,
    complexity_tier: Optional[int] = None,
    claim_status: Optional[str] = "AVAILABLE"
):
    """
    Returns unsolved chronic civic problems available for institutions/colleges to adopt.
    Can be filtered by department, student academic year, or complexity tier.
    """
    problems = get_chronic_problems(
        department=department,
        academic_year=academic_year,
        complexity_tier=complexity_tier,
        claim_status=claim_status
    )
    return {
        "status": "success",
        "total_available": len(problems),
        "chronic_problems": problems
    }


@app.post("/academic/chronic-problems/claim")
def claim_chronic_problem_endpoint(req: ClaimProblemRequest):
    """
    Allows an institution's student/faculty team to claim an unsolved problem statement
    with student academic year guardrail validation.
    """
    claim_res = claim_chronic_problem(
        escalation_id=req.escalation_id,
        institution_name=req.institution_name,
        team_name=req.team_name,
        student_academic_year=req.student_academic_year
    )
    if claim_res.get("status") == "error":
        raise HTTPException(status_code=404, detail=claim_res.get("message"))
    if claim_res.get("status") == "guardrail_blocked":
        raise HTTPException(status_code=403, detail=claim_res.get("message"))
    return claim_res


@app.get("/academic/chronic-problems/{escalation_id}/dossier-pdf")
def get_dossier_pdf_endpoint(escalation_id: str):
    """
    Downloads or renders the professional Engineering Problem Statement Dossier PDF
    for Higher Education Institutions.
    """
    target = next((item for item in CHRONIC_PROBLEMS_POOL if item["escalation_id"] == escalation_id), None)
    if not target:
        raise HTTPException(status_code=404, detail=f"Chronic problem '{escalation_id}' not found in Problem Bank.")

    pdf_path = target.get("dossier_pdf_path")
    if not pdf_path or not Path(pdf_path).exists():
        try:
            pdf_path = generate_hei_problem_dossier_pdf(target)
            target["dossier_pdf_path"] = pdf_path
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to render dossier PDF: {e}")

    return FileResponse(
        path=pdf_path,
        media_type="application/pdf",
        filename=f"Engineering_Dossier_{escalation_id}.pdf"
    )


@app.post("/academic/chronic-problems/{escalation_id}/generate-dossier")
def generate_dossier_endpoint(escalation_id: str, req: GenerateDossierRequest):
    """
    Synthesizes and builds a formal Engineering Problem Dossier PDF using Gemini AI
    (with automatic zero-downtime engineering fallback).
    """
    target = next((item for item in CHRONIC_PROBLEMS_POOL if item["escalation_id"] == escalation_id), None)
    if not target:
        raise HTTPException(status_code=404, detail=f"Chronic problem '{escalation_id}' not found in Problem Bank.")

    try:
        pdf_path = generate_hei_problem_dossier_pdf(target, gemini_api_key=req.gemini_api_key)
        target["dossier_pdf_path"] = pdf_path
        target["dossier_pdf_url"] = f"/academic/chronic-problems/{escalation_id}/dossier-pdf"
        return {
            "status": "success",
            "action": "DOSSIER_PDF_GENERATED",
            "escalation_id": escalation_id,
            "pdf_path": pdf_path,
            "download_url": target["dossier_pdf_url"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate dossier PDF: {e}")


# =============================================================================
# Corporate CSR Funding & Prototype Showcase Endpoints
# =============================================================================

@app.post("/corporate/prototypes/submit")
def submit_prototype_endpoint(req: PrototypeSubmitRequest):
    """
    Allows an HEI student/faculty engineering team to submit their working prototype,
    Bill of Materials (BoM), and TRL verification for corporate CSR funding.
    """
    proto = register_prototype_submission(
        escalation_id=req.escalation_id,
        team_name=req.team_name,
        institution_name=req.institution_name,
        faculty_mentor=req.faculty_mentor,
        prototype_title=req.prototype_title,
        executive_summary=req.executive_summary,
        technical_approach=req.technical_approach,
        trl_level=req.trl_level or 5,
        bill_of_materials=req.bill_of_materials or [],
        total_funding_required_inr=req.total_funding_required_inr or 0.0,
        demo_video_url=req.demo_video_url,
        cad_repo_url=req.cad_repo_url,
        field_testing_plan=req.field_testing_plan,
        expected_civic_impact=req.expected_civic_impact,
        category=req.category or "road_damage"
    )
    return {
        "status": "prototype_registered_for_corporate_sponsorship",
        "prototype": proto
    }


@app.get("/corporate/prototypes")
def list_prototypes_endpoint(
    schedule_vii: Optional[str] = None,
    min_trl: Optional[int] = None,
    max_budget: Optional[float] = None,
    funding_status: Optional[str] = None
):
    """
    Corporate Investor Portal: Browse verified HEI prototypes filtered by
    Schedule VII item, Technology Readiness Level (TRL 1-7), and budget cap.
    """
    protos = list_prototypes(
        schedule_vii=schedule_vii,
        min_trl=min_trl,
        max_budget=max_budget,
        funding_status=funding_status
    )
    return {
        "status": "success",
        "total_prototypes": len(protos),
        "prototypes": protos
    }


@app.get("/corporate/prototypes/{prototype_id}")
def get_prototype_detail_endpoint(prototype_id: str):
    """
    Retrieves full prototype specifications, Bill of Materials, TRL rating,
    and civic impact projections.
    """
    proto = get_prototype_by_id(prototype_id)
    if not proto:
        raise HTTPException(status_code=404, detail=f"Prototype '{prototype_id}' not found.")
    return {"status": "success", "prototype": proto}


@app.get("/corporate/prototypes/{prototype_id}/match-sponsors")
def match_prototype_sponsors_endpoint(prototype_id: str):
    """
    AI-driven CSR Matching Engine: Matches the prototype against corporate partners
    by Schedule VII alignment, CSR budget headroom, and regional focus.
    """
    match_result = match_sponsors_for_prototype(prototype_id)
    if match_result.get("status") == "error":
        raise HTTPException(status_code=404, detail=match_result.get("message"))
    return match_result


@app.post("/corporate/sponsorship/pledge")
def pledge_corporate_sponsorship_endpoint(req: SponsorshipPledgeRequest):
    """
    Corporate CSR Funding Pledge: Commits CSR funds under the Tripartite Governance
    Agreement with 3-Tranche Milestone Escrow (30% Lab -> 40% Municipal Pilot -> 30% Handover).
    """
    proto_id = req.prototype_id or "PROTO-TERRAFIX-01"
    sponsor_id = req.sponsor_id or "CORP-TATA-01"
    amount = req.pledged_amount_inr if req.pledged_amount_inr is not None else (req.amount if req.amount is not None else 250000.0)
    rep_name = req.corporate_representative_name or req.representative_name or "Dr. Ananya Sharma"
    rep_email = req.corporate_contact_email or req.email or "csr.initiative@tatasustainability.org"

    res = create_sponsorship_pledge(
        prototype_id=proto_id,
        sponsor_id=sponsor_id,
        pledged_amount_inr=float(amount),
        corporate_representative_name=rep_name,
        corporate_contact_email=rep_email,
        escrow_terms_accepted=True if req.escrow_terms_accepted is None else bool(req.escrow_terms_accepted),
        civic_commons_license_accepted=True if req.civic_commons_license_accepted is None else bool(req.civic_commons_license_accepted)
    )
    if res.get("status") == "error":
        raise HTTPException(status_code=400, detail=res.get("message"))
    return res


@app.post("/corporate/sponsorship/approve-milestone")
def approve_milestone_endpoint(req: MilestoneApproveRequest):
    """
    Approves a milestone tranche and disburses escrow funds to the HEI team.
    Enforces Municipal Gatekeeper check (Tranche 2 requires ULB municipal_officer signoff).
    """
    res = approve_milestone(
        sponsorship_id=req.sponsorship_id,
        tranche_index=req.tranche_index,
        approver_role=req.approver_role,
        approver_name=req.approver_name,
        verification_notes=req.verification_notes
    )
    if res.get("status") == "error":
        raise HTTPException(status_code=400, detail=res.get("message"))
    if res.get("status") == "gatekeeper_blocked":
        raise HTTPException(status_code=403, detail=res.get("message"))
    return res


@app.get("/corporate/sponsorship/{sponsorship_id}/agreement")
def get_tripartite_agreement_endpoint(sponsorship_id: str):
    """
    Generates the legal Tripartite Governance Agreement resolving IP rights (Civic Commons License),
    Municipal site indemnity, and Escrow rules.
    """
    res = generate_tripartite_agreement_text(sponsorship_id)
    if res.get("status") == "error":
        raise HTTPException(status_code=404, detail=res.get("message"))
    return res


@app.get("/corporate/sponsorship/{sponsorship_id}/csr-certificate")
def get_csr_certificate_endpoint(sponsorship_id: str):
    """
    Generates the official MCA Schedule VII CSR-1 Impact Audit & Tax Certificate
    for corporate donors under Section 135 of the Indian Companies Act, 2013.
    """
    res = generate_csr_impact_certificate(sponsorship_id)
    if res.get("status") == "error":
        raise HTTPException(status_code=404, detail=res.get("message"))
    return res


@app.get("/corporate/sponsors")
def list_corporate_sponsors_endpoint():
    """
    Lists registered corporate CSR trusts and foundations available for civic co-funding.
    """
    return {
        "status": "success",
        "total_sponsors": len(CORPORATE_SPONSORS_STORE),
        "corporate_sponsors": list(CORPORATE_SPONSORS_STORE.values())
    }


# =============================================================================
# UNIFIED AUTONOMOUS CIVIC AI-AGENT ENDPOINTS
# =============================================================================

from agent import get_civic_orchestrator


class AgentAutomateRequest(BaseModel):
    action: str  # CITIZEN_SUBMISSION | GOVERNMENT_STATUS_UPDATE | HEI_PROTOTYPE_SUBMIT | CORPORATE_PLEDGE | MUNICIPAL_SITE_CLEARANCE | CIVIC_HANDOVER_AND_CERTIFICATION
    payload: Dict[str, Any] = {}


@app.post("/agent/automate")
def agent_automate_dispatcher_endpoint(req: AgentAutomateRequest):
    """
    Unified AI-Agent Master Dispatcher:
    Enables the backend developer to trigger any stage of the 10-step civic lifecycle
    through a single endpoint without needing to manage multi-folder sub-services.
    
    Supported Actions:
      1. CITIZEN_SUBMISSION: Ingestion, Part A NLP, YOLO11, and Spatial Fusion (<=150m)
      2. GOVERNMENT_STATUS_UPDATE: Municipal SLA outcome (RESOLVED or ESCALATE to HEI)
      3. HEI_PROTOTYPE_SUBMIT: Student capstone with BoM & 1st-Year Safety Guardrail
      4. CORPORATE_PLEDGE: CSR pledge, Civic Commons License (CCL), and 3-Tranche Escrow
      5. MUNICIPAL_SITE_CLEARANCE: ULB engineer inspection unlocks Tranche 2 Field Pilot
      6. CIVIC_HANDOVER_AND_CERTIFICATION: Tranche 3 release & MCA Section 135 CSR Certificate
    """
    agent = get_civic_orchestrator()
    result = agent.dispatch_agent_action(req.action, req.payload)
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
    if result.get("status") in ["gatekeeper_blocked", "safety_guardrail_blocked"]:
        raise HTTPException(status_code=403, detail=result.get("message"))
    return result


@app.get("/agent/tickets")
def list_agent_tickets_endpoint():
    """
    Lists all civic grievance tickets currently managed across the autonomous AI-Agent lifecycle.
    """
    agent = get_civic_orchestrator()
    return {
        "status": "success",
        "total_tickets": len(agent.store),
        "tickets": list(agent.store.values())
    }


@app.get("/agent/tickets/{ticket_id}")
def get_agent_ticket_detail_endpoint(ticket_id: str):
    """
    Retrieves full real-time state, audit trail, evidence galleries, academic dossiers,
    prototype details, milestone escrow balances, and CSR certificates for a ticket.
    """
    agent = get_civic_orchestrator()
    ticket = agent.store.get(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail=f"Ticket '{ticket_id}' not found.")
    return {
        "status": "success",
        "ticket": ticket
    }


@app.get("/agent/workflow")
def get_agent_workflow_architecture_endpoint():
    """
    Returns the official architecture, state diagram, and actions supported by the AI-Agent.
    """
    return {
        "platform": "Samvad-Setu Autonomous Civic AI-Agent",
        "version": "2.0.0",
        "zero_training_guarantee": True,
        "unified_endpoint": "POST /agent/automate",
        "workflow_stages": [
            {
                "step": 1,
                "name": "Citizen Grievance Submission",
                "action": "CITIZEN_SUBMISSION",
                "modalities": ["photo", "video", "voice", "text", "gps"],
                "engines": ["YOLO11 Vision", "Whisper Audio", "Part A Indic NLP"]
            },
            {
                "step": 2,
                "name": "Smart Deduplication & Spatial Fusion",
                "condition": "<=150m proximity + Text/Vision Cosine Similarity",
                "output": "Fuse into Master Incident or create new Master Ticket"
            },
            {
                "step": 3,
                "name": "Phase 1: Municipal Government Attempt",
                "sla_window": "7 to 14 days",
                "action": "GOVERNMENT_STATUS_UPDATE",
                "branch_yes": "CASE_CLOSED (Standard Municipal Fix)",
                "branch_no": "ESCALATION_ENGINE (Part B Academic)"
            },
            {
                "step": 4,
                "name": "HEI Problem Statement Bank & Academic Triage",
                "sub_modules": [
                    "4-Tier Complexity Scorer (Tier 1 Foundation to Tier 4 R&D)",
                    "1st-Year Safety Guardrail (Blocks junior students from high-risk R&D)",
                    "AICTE Syllabus Matcher (Civil, CSE, Environmental)",
                    "Professional Engineering Dossier (Gemini 3.6 Flash + ReportLab PDF)"
                ]
            },
            {
                "step": 5,
                "name": "HEI Student Capstone Prototype Submission",
                "action": "HEI_PROTOTYPE_SUBMIT",
                "requirements": ["Working Prototype", "TRL 1-7", "Bill of Materials (BoM)"]
            },
            {
                "step": 6,
                "name": "Corporate Prototype Showcase & AI CSR Sponsor Matching",
                "taxonomy": "MCA Schedule VII (Companies Act Section 135)",
                "matching_criteria": ["Schedule VII Alignment", "Budget Headroom", "Regional Ward"]
            },
            {
                "step": 7,
                "name": "Tripartite Governance & 3-Tranche Milestone Escrow",
                "action": "CORPORATE_PLEDGE",
                "governance": "Civic Commons License (CCL v1.0)",
                "escrow_tranches": {
                    "Tranche 1 (30%)": "Lab Validation & BoM Buy -> Released immediately",
                    "Tranche 2 (40%)": "ULB Municipal Field Pilot -> LOCKED until Site Clearance",
                    "Tranche 3 (30%)": "Final Handover & Public Commissioning -> LOCKED until Audit"
                }
            },
            {
                "step": 8,
                "name": "Municipal Site Clearance Gatekeeper",
                "action": "MUNICIPAL_SITE_CLEARANCE",
                "condition": "ULB Municipal Engineer site inspection sign-off unlocks Tranche 2"
            },
            {
                "step": 9,
                "name": "Real-World Municipal Field Pilot Deployment",
                "verification": "Field testing and citizen impact validation"
            },
            {
                "step": 10,
                "name": "Final Civic Handover & Statutory CSR Certification",
                "action": "CIVIC_HANDOVER_AND_CERTIFICATION",
                "output": "Permanent Civic Fix + MCA Section 135 CSR-1 Tax Exemption Certificate"
            }
        ]
    }


