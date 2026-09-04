"""
=============================================================================
Samvad-Setu: Civic Innovation Platform (Part B - Voice API)
Module: Part B - Voice Verification, Whisper Transcription & NLP Triage API
=============================================================================
Description:
    FastAPI microservice for citizen voice reports.
    Accepts audio file uploads, verifies file integrity, converts speech to
    text with Whisper, and routes the text through the Part A NLP classifier.

To run manually in your terminal:
    cd part-b/voice
    uvicorn api:app --reload
=============================================================================
"""

import os
import sys
import shutil
import uuid
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore
    except AttributeError:
        pass

# pyrefly: ignore [missing-import]
from fastapi import FastAPI, UploadFile, File, HTTPException, status
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware

# Local voice & NLP processing pipeline
from whisper_service import process_voice_complaint, ALLOWED_EXTENSIONS

# -----------------------------------------------------------------------------
# App Setup & Upload Folder
# -----------------------------------------------------------------------------

app = FastAPI(
    title="Samvad-Setu Part B Voice API",
    description="Citizen Voice Report Verification, Whisper Transcription & Part A NLP Triage",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path(__file__).resolve().parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


# -----------------------------------------------------------------------------
# Endpoints
# -----------------------------------------------------------------------------

@app.get("/")
def home():
    """Service health check."""
    return {
        "status": "online",
        "service": "Samvad-Setu Part B Voice Triage Engine",
        "supported_audio_formats": sorted(list(ALLOWED_EXTENSIONS)),
        "workflow": "Upload audio -> Verify -> Transcribe with Whisper -> Triage with Part A NLP",
        "endpoints": {
            "GET /": "Health check",
            "POST /voice/process": "Upload audio file via form-data in Postman"
        }
    }


@app.post("/voice/process")
async def process_audio(file: UploadFile = File(...)):
    """
    Upload citizen voice recording (form-data: 'file').
    - Verifies audio format and size
    - Transcribes speech to text using Whisper
    - Triages grievance with Part A (Department, Category, Severity & SLA)
    """
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No filename provided in upload."
        )

    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported format '{file_ext}'. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )

    # Save to unique path
    unique_id = uuid.uuid4().hex[:8]
    temp_path = UPLOAD_DIR / f"voice_{unique_id}{file_ext}"

    try:
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Run complete verification, transcription, and NLP triage
        result = process_voice_complaint(temp_path)

        if result.get("status") == "failed":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=result.get("error", "Failed to process audio file.")
            )

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server error processing audio: {str(e)}"
        )
    finally:
        # Clean up temporary uploaded file
        if temp_path.exists():
            try:
                temp_path.unlink()
            except Exception:
                pass
