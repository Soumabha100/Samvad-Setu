"""
Samvad-Setu: Civic Innovation Platform (Part A - Municipal Operations)
Module: Part A - Complaint Categorization & Severity Triage API

To run manually in your terminal:
    cd part-a
    uvicorn api:app --reload --port 8000
"""

import sys
import warnings
# pyrefly: ignore [missing-import]
from fastapi import FastAPI, HTTPException
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
# pyrefly: ignore [missing-import]
from pydantic import BaseModel

# Suppress sklearn unpickle version warnings if different Python envs are used
warnings.filterwarnings("ignore")

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore
    except AttributeError:
        pass

from predict import get_classifier

# Initialize FastAPI app
app = FastAPI(
    title="Samvad-Setu Part A API",
    description="Automated Civic Grievance Classification and Severity SLA Triage",
    version="1.0.0"
)

# Enable CORS for Postman and Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load inference engine
classifier = get_classifier()


class ComplaintRequest(BaseModel):
    text: str


# -----------------------------------------------------------------------------
# Endpoints for Postman & Manual Testing
# -----------------------------------------------------------------------------

@app.get("/")
def home():
    """Simple health check endpoint."""
    return {
        "status": "online",
        "service": "Samvad-Setu Part A Triage API",
        "message": "API is ready. Send a POST request to /predict.",
        "sample_postman_body": {
            "text": "School ke paas road pe massive deep pothole hai, accident risk!"
        }
    }


@app.get("/test")
def test_get(text: str = "School ke paas road pe massive deep pothole hai, accident risk!"):
    """
    Quick GET test endpoint for Postman or browser without setting up request body.
    Usage in Postman/Browser:
        GET http://127.0.0.1:8000/test?text=Road+pe+pothole+hai
    """
    return classifier.predict_one(text)


@app.post("/predict")
def predict_complaint(payload: ComplaintRequest):
    """
    Main prediction endpoint for Postman.
    Method: POST
    URL: http://127.0.0.1:8000/predict
    Body (raw JSON):
    {
        "text": "School ke paas road pe massive deep pothole hai, accident risk!"
    }
    """
    if not payload.text or not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text field cannot be empty.")

    return classifier.predict_one(payload.text)
