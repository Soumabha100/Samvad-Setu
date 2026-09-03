# 👁️🎙️ Samvad-Setu: Part B — Multimodal AI Quick Start Guide

Welcome! This folder contains **Part B (Multimodal Civic Verification)** of the Samvad-Setu platform.

Part B provides two core capabilities:
1. **Computer Vision (YOLO11)**: Detects physical civic issues in photos across **8 categories** (`pothole`, `garbage`, `crack`, `open_manhole`, `waterlogging`, `stray_animal`, `traffic_light`, `waste_container`) and assigns severity levels.
2. **Voice Verification (OpenAI Whisper + Part A)**: Transcribes citizen voice notes and automatically routes the grievance to the right municipal department with a legally binding SLA deadline.

---

## 🚀 Quick Setup (3 Steps)

> **Note:** The trained vision model is already included in `models/vision_model.pt`. You **do not** need to retrain any models to test the system!

### Step 1: Navigate to Part B
Open your terminal and enter `part-b`:
```powershell
cd part-b
```

### Step 2: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 3: Run Direct Tests in Terminal

#### 📸 Test Computer Vision on an Image:
```powershell
cd image
python predict.py test2.jpg
cd ..
```
*Output: Detects potholes, computes confidence, and outputs `Overall Severity: HIGH`.*

#### 🎙️ Test Voice Transcription & NLP Triage:
```powershell
cd voice
python whisper_service.py citizen_report.mp3
cd ..
```
*Output: Transcribes speech $\rightarrow$ `"There is a big pothole in the road. Please help."` $\rightarrow$ Routes to `Public Works Department (PWD - Roads)` with `72 Hours SLA`.*

---

## ⚡ Running the Unified Server on Port 8000

We built a single unified **FastAPI** service in `main.py` that serves both Image and Voice endpoints together:

```powershell
cd part-b
uvicorn main:app --reload --port 8000
```
*(Server will start at `http://127.0.0.1:8000`)*

---

## 📬 Testing with Postman

### 1. 🖼️ Image Grievance Detection
* **Method:** `POST`
* **URL:** `http://127.0.0.1:8000/image/predict`
* **Body:** 
  1. Select **form-data**.
  2. Set Key = `file` and change dropdown from *Text* to **File**.
  3. Select any image (e.g. `part-b/image/test2.jpg`).
  4. Click **Send**.

#### Expected Response:
```json
{
  "detected": true,
  "overall_issue": "pothole",
  "overall_severity": "HIGH",
  "objects_detected": 4,
  "detections": [
    {
      "issue": "pothole",
      "confidence": 0.902,
      "severity": "HIGH"
    },
    {
      "issue": "pothole",
      "confidence": 0.653,
      "severity": "MEDIUM"
    }
  ],
  "file_name": "test2.jpg"
}
```

---

### 2. 🎙️ Voice Report Transcription & NLP Triage
* **Method:** `POST`
* **URL:** `http://127.0.0.1:8000/voice/process`
* **Body:** 
  1. Select **form-data**.
  2. Set Key = `file` and change dropdown to **File**.
  3. Select any audio file (e.g. `part-b/voice/citizen_report.mp3`).
  4. Click **Send**.

#### Expected Response:
```json
{
  "status": "success",
  "audio_info": {
    "file_name": "citizen_report.mp3",
    "size_kb": 86.58,
    "format": ".mp3"
  },
  "transcription": {
    "text": "There is a big pothole in the road. Please help.",
    "language": "en"
  },
  "nlp_triage": {
    "category": "road_damage",
    "department": "Public Works Department (PWD - Roads)",
    "severity": "medium",
    "sla_hours": 72,
    "priority_level": 3,
    "priority_description": "Standard Municipal Ticket (3 Days)"
  }
}
```

---

### 3. 🔍 Multimodal Cross-Verification
* **Method:** `POST`
* **URL:** `http://127.0.0.1:8000/verify/multimodal`
* **Body:** form-data with `image` (photo file) and `audio` (voice recording).
* Cross-references visual evidence against voice report to verify authenticity and determine unified urgency.

---

## 🏛️ Supported Civic Issue Classes (8 Classes)

| ID | Issue Name | Civic Scope | Responsible Municipal Department | Default Severity |
| :---: | :--- | :--- | :--- | :---: |
| **0** | `pothole` | Road Crater / Cavity | Public Works Department (PWD - Roads) | `HIGH` |
| **1** | `garbage` | Waste Dump / Litter | Solid Waste & Sanitation Department | `MEDIUM` |
| **2** | `crack` | Road Surface Crack | Public Works Department (PWD - Roads) | `MEDIUM` |
| **3** | `open_manhole` | Uncovered Drain/Manhole | PHED Drainage *(Immediate Safety Hazard)* | `CRITICAL` |
| **4** | `waterlogging` | Roadway Flooding | PHED Drainage & Stormwater Management | `HIGH` / `CRITICAL` |
| **5** | `stray_animal` | Cattle / Animals on Road | Municipal Animal Control & Public Safety | `MEDIUM` / `HIGH` |
| **6** | `traffic_light` | Signal Failure / Dark Light | Traffic Police & Municipal Electrical Division | `HIGH` |
| **7** | `waste_container` | Overflowing Dustbin/Dumpster | Solid Waste & Sanitation Department | `MEDIUM` |

---

## 📂 File Directory Overview

| File / Folder | Purpose |
| :--- | :--- |
| `main.py` | Unified FastAPI application serving `/image/predict`, `/voice/process`, and `/verify/multimodal`. |
| `models/vision_model.pt` | Trained YOLO11 model weights (portable relative path). |
| `image/predict.py` | Standalone CLI inference script for images. |
| `image/severity.py` | 8-class multi-tier severity calculation logic. |
| `image/taxonomy.json` | Civic class dictionary, department routing, and SLA guidelines. |
| `image/prepare_dataset.py` | Converts raw images and flooding masks into 2,759 annotated YOLO samples. |
| `image/train.py` | Automated YOLO11 training script with model export. |
| `voice/whisper_service.py` | Audio integrity checker, Whisper transcriber, and Part A NLP caller. |
| `voice/citizen_report.mp3` | Sample citizen voice report for testing. |
| `requirements.txt` | Production dependencies for Part B. |

---

## 🔄 How to Retrain the Vision Model (Optional)

If you ever wish to retrain the YOLO model on all 8 classes from scratch:

```powershell
cd image

# 1. Prepare/regenerate the 8-class dataset
python prepare_dataset.py

# 2. Train YOLO11 (configurable epochs & batch size)
python train.py --epochs 5 --batch 8
```
*(The best weights will automatically be exported to `part-b/models/vision_model.pt`)*
