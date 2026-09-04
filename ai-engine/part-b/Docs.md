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
| `dedup.py` | Standalone Multimodal Incident Deduplication, Spatial Clustering, & Fusion Engine. |
| `main.py` | Unified FastAPI application serving vision, voice, verification, and deduplication. |
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

## 🧩 Multimodal Incident Deduplication & Grievance Fusion

When multiple citizens submit complaints about the same civic issue in the same neighborhood (e.g., **9 separate citizen reports about a deep road pothole near a school**), this AI engine prevents duplicate tickets and aggregates them into **1 Master Incident Ticket**.

### 📐 4-Pillar Similarity Formula:
* **Spatial Proximity (GPS)**: Haversine distance ($\le 50$m = 100% match, $\le 150$m = 85% match, $> 350$m = 0% match).
* **Category Match**: Exact civic issue alignment (e.g., both are `road_damage` / `pothole`).
* **Semantic Text Similarity**: TF-IDF cosine similarity across English, Hindi, and Hinglish complaints.
* **Visual Perceptual Hash (dHash)**: Compares photo evidence similarity via 64-bit difference hashing.

### 🧪 Run the Standalone Demo in Terminal:
```powershell
python dedup.py
```
*Output: Simulates 10 raw complaints (9 near school, 1 in a distant market). Automatically merges the 9 complaints into **1 Master Ticket**, counts 9 reporting citizens, and auto-escalates urgency to **CRITICAL (4 Hours SLA)**!*

---

### 🌐 Backend Integration Endpoints (For Node.js / Express Teammates)

Your backend teammate can call these endpoints from `http://127.0.0.1:8000`:

#### 🌟 1. `POST /incident/submit` (All-in-One Automated Pipeline)
The primary endpoint for citizen grievance submission. Ingests any file (photo, audio, video) or text, runs Whisper/YOLO/Part A, and automatically checks deduplication in the background.

* **Method:** `POST`
* **URL:** `http://127.0.0.1:8000/incident/submit`
* **Body Type:** `form-data`
  * `image` / `file` (File): Photo of problem (e.g. pothole).
  * `audio` (File): Voice note recording.
  * `video` (File): Video recording (OpenCV extracts keyframe).
  * `text` (Text): Written complaint description.
  * `citizen_name` (Text): Citizen's name.
  * `lat` & `lng` (Text): GPS coordinates.
  * `address` (Text): Landmark or street name.

* **Response (Auto-Fused Duplicate):**
```json
{
  "status": "success",
  "action": "MERGED_INTO_MASTER_TICKET",
  "is_duplicate": true,
  "matched_ticket_id": "MTR-1001",
  "similarity_score": 0.912,
  "message": "Duplicate incident detected (91.2% match). Automatically merged into Master Ticket MTR-1001.",
  "master_ticket": {
    "master_ticket_id": "MTR-1001",
    "category": "road_damage",
    "department": "Public Works Department (PWD - Roads)",
    "citizen_count": 9,
    "severity": "critical",
    "sla_hours": 4
  }
}
```

---

#### 2. `POST /dedup/check` (Real-Time Duplicate Prevention)
Call this when a citizen submits a new complaint. Pass the `new_report` and an array of `active_reports` currently unresolved in the database.

* **Request Body (JSON):**
```json
{
  "new_report": {
    "text": "Deep road pothole near school gate",
    "category": "road_damage",
    "location": { "lat": 23.5121, "lng": 87.3111 }
  },
  "active_reports": [
    {
      "id": "TKT-1001",
      "text": "Huge dangerous pothole in front of school",
      "category": "road_damage",
      "location": { "lat": 23.5120, "lng": 87.3110 },
      "citizen_count": 8,
      "severity": "high"
    }
  ]
}
```

* **Response (JSON):**
```json
{
  "status": "success",
  "is_duplicate": true,
  "matched_ticket_id": "TKT-1001",
  "similarity_score": 0.892,
  "action": "MERGE_INTO_MASTER",
  "merged_incident": {
    "citizen_count": 9,
    "severity": "critical",
    "sla_hours": 4,
    "summary": "Master Ticket: Confirmed Road Damage verified by 9 citizens. Severity escalated to CRITICAL (4h SLA target)."
  }
}
```

#### 2. `POST /dedup/cluster` (Batch Grievance Aggregation)
Pass an array of raw reports. The AI clusters duplicates together and returns consolidated Master Tickets with full evidence galleries.

* **Request Body:** `{ "reports": [ {...}, {...} ] }`
* **Response:** Returns `master_tickets` array with aggregated citizen counts and escalated severities.

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

---

## 🏛️ Academic & HEI Syllabus Allocation Engine (NEW)

The Academic Engine connects real-world municipal problems to Higher Education Institutions (HEIs), matching problem statements directly to **Department Core Subjects** (e.g. Civil, CSE, Environmental) while enforcing a strict **Student Year Safety Guardrail** (so 1st-year students only receive foundation/survey problems, and unsolvable research/capstone problems are strictly escalated to senior/Tier-1 labs).

### 1. `GET /academic/institutions`
Search and filter Indian premier & state technical institutions (IITs, NITs, State Tech Universities, Autonomous Colleges) with AISHE codes and top departments.

* **Query Parameters:**
  * `query`: (e.g. `Bombay`, `Sindri`, `Trichy`, `AKTU`)
  * `state`: (e.g. `Jharkhand`, `Maharashtra`, `Tamil Nadu`)
  * `category`: (e.g. `Tier-1 Premier Research`, `Tier-2 State Technical University`)
* **Response (JSON):**
```json
{
  "status": "success",
  "total_results": 1,
  "institutions": [
    {
      "id": "inst_iit_b",
      "name": "Indian Institute of Technology (IIT) Bombay",
      "short_name": "IIT Bombay",
      "aishe_code": "U-0306",
      "category": "Tier-1 Premier Research",
      "state": "Maharashtra",
      "best_departments": [
        {"department": "Civil Engineering", "focus": "Transportation Systems, Geospatial Tech"},
        {"department": "Environmental Science", "focus": "Municipal Wastewater Remediation"}
      ]
    }
  ]
}
```

### 2. `POST /academic/complexity/evaluate`
Evaluates technical complexity (4-Tier Difficulty Matrix), minimum eligible academic year, prerequisites, and suggested deliverables.

* **Method:** `POST`
* **URL:** `http://127.0.0.1:8000/academic/complexity/evaluate`
* **Request Body:**
```json
{
  "text": "Citizen survey on household plastic waste and photo collection in Ward 10",
  "category": "garbage"
}
```
* **Response (JSON):**
```json
{
  "status": "success",
  "complexity": {
    "tier": 1,
    "tier_name": "TIER_1_FOUNDATION",
    "complexity_score": 0.23,
    "min_academic_year": 1,
    "target_audience": "1st-Year Engineering Students (All Branches) & Diploma/Polytechnic Students",
    "prerequisites": ["Basic computer literacy", "Community survey and communication skills"],
    "recommended_deliverable": "Field Survey Audit, Photographic Documentation Catalog",
    "rationale": "Focuses on foundational data collection, citizen sentiment, and civic field observations."
  }
}
```

### 3. `POST /academic/syllabus/match` (With Safety Guardrail)
Matches a civic problem against an institution's curriculum, finds the best matching Core Subject, and enforces the Student Year Guardrail.

* **Method:** `POST`
* **URL:** `http://127.0.0.1:8000/academic/syllabus/match`
* **Request Body (Example A: Safe Year 3 Match):**
```json
{
  "problem_text": "Potholes and bitumen breakdown on arterial highway causing road accidents",
  "category": "road_damage",
  "department_hint": "Civil Engineering",
  "target_student_year": 3,
  "curriculum_key": "civil_engineering"
}
```
* **Response (JSON):**
```json
{
  "status": "success",
  "department": "Civil Engineering",
  "guardrail_evaluation": {
    "target_student_year": 3,
    "is_eligible": true,
    "guardrail_status": "APPROVED",
    "guardrail_warning": null
  },
  "best_matched_subject": {
    "subject_code": "CE-301",
    "subject_name": "Highway and Transportation Engineering",
    "academic_year": 3,
    "semester": 5,
    "is_core": true,
    "similarity_percent": 23.9,
    "recommended_student_deliverable": "Functional Hardware/Software Prototype, Field-Tested Edge Device, or Capstone Thesis"
  }
}
```

* **Guardrail Trigger Example (When complex problem is sent to Year 1):**
```json
{
  "problem_text": "Acoustic tomography and computational fluid dynamics to study deep underground sewer surge and novel polymer healing",
  "category": "drainage",
  "target_student_year": 1
}
```
* **Response:**
```json
{
  "guardrail_evaluation": {
    "target_student_year": 1,
    "is_eligible": false,
    "guardrail_status": "BLOCKED_EXCEEDS_STUDENT_YEAR",
    "guardrail_warning": "GUARDRAIL TRIGGERED: Problem complexity is classified as Tier 4 (TIER_4_RESEARCH), requiring Year 4+ skills. It is strictly BLOCKED from Year 1 students to prevent assigning unsolvable/open-ended research problems to junior students. Recommended escalation: M.Tech / PhD Scholars & Premier Tier-1 Research Labs (IITs, IISc, NITs)."
  }
}
```

---

## ⚡ Chronic Recurrence & Government Failure Escalation Pipeline

> [!IMPORTANT]
> **Trigger Condition**: Normal daily complaints remain with the municipal authority. An incident is **ONLY** escalated to Higher Education Institutions (HEIs) when:
> 1. The **Government authority failed to resolve it** (SLA breached, contractor attempts failed, or marked unresolvable).
> 2. The problem **chronically recurs over weeks or months** (recurrent count $\ge 3$ or spanning $\ge 14$ days) indicating a structural/engineering flaw requiring academic R&D.

### 4. `POST /academic/escalation/check-eligibility`
Check if a municipal incident qualifies for academic escalation before transferring.

* **Request Body:**
```json
{
  "status": "unresolved_breached",
  "sla_breached": true,
  "recurrence_count": 3,
  "recurrence_period_days": 30,
  "failed_resolution_attempts": 2
}
```
* **Response (JSON):**
```json
{
  "status": "success",
  "eligibility": {
    "is_eligible_for_academic_routing": true,
    "lifecycle_stage": "ESCALATED_TO_ACADEMIC_R_AND_D",
    "decision": "APPROVED_FOR_INSTITUTION_PORTAL",
    "reasons": [
      "CHRONIC_RECURRENCE: Problem reported 3 times across 30 days. Repeated failure indicates a chronic systemic or engineering design flaw requiring academic R&D.",
      "GOV_AUTHORITY_SLA_BREACH: Municipal department exceeded statutory SLA deadline without a viable solution.",
      "FAILED_REPAIR_HISTORY: Municipal contractors attempted resolution 2 time(s) but the defect resurfaced."
    ]
  }
}
```

### 5. `POST /academic/escalation/register`
Escalate an unsolved municipal problem into the **Institutional Problem Bank**. The AI automatically evaluates technical complexity and matches it to the Core Department Subject.

* **Request Body:**
```json
{
  "problem_id": "CIVIC-RNC-9901",
  "title": "Recurrent main storm drain collapse during monsoon",
  "description": "Drain retaining wall collapses repeatedly over 60 days. Contractor rebuilt twice, but wall washed away again.",
  "category": "drainage",
  "department": "Public Health Engineering Dept (PHED - Drainage)",
  "location": { "lat": 23.3441, "lng": 85.3096, "address": "Kanke Road, Ranchi" },
  "status": "unresolved_breached",
  "sla_breached": true,
  "recurrence_count": 3,
  "recurrence_period_days": 60,
  "failed_resolution_attempts": 2,
  "curriculum_key": "civil_engineering"
}
```
* **Response:** Returns `escalation_id` (e.g. `ESC-00FDBE`), complexity tier, and matched core department subject.

### 6. `GET /academic/chronic-problems`
When any college or institution logs into the portal, they call this endpoint to view unsolved, chronic municipal problems ready for their student teams.

* **Query Parameters (Optional Filters):**
  * `department`: `Civil Engineering`, `Computer Science`, `Environmental`
  * `academic_year`: `1`, `2`, `3`, `4` (Applies guardrail filter)
  * `complexity_tier`: `1`, `2`, `3`, `4`
  * `claim_status`: `AVAILABLE` (Default) or `CLAIMED`
* **Response:** Returns list of available chronic problem statements with full engineering context.

### 7. `POST /academic/chronic-problems/claim`
Allows a college student or capstone team to claim an unsolved problem statement.

* **Request Body:**
```json
{
  "escalation_id": "ESC-00FDBE",
  "institution_name": "Birla Institute of Technology (BIT) Mesra",
  "team_name": "Team Environmental Hydro",
  "student_academic_year": 4
}
```
* **Response:** Allocates problem to the team if student year meets the complexity threshold. If a 1st-year team attempts to claim an advanced Tier 3/4 problem, returns HTTP 403 Forbidden with guardrail explanation.

### 8. `GET /academic/chronic-problems/{escalation_id}/dossier-pdf`
Renders and downloads the publication-grade **Engineering Problem Statement Dossier (PDF)** for Higher Education Institutions.
* **Format:** Downloadable PDF (`application/pdf`)
* **Content:**
  * Formal engineering banner & institutional metadata table (Escalation ID, Core Subject, Complexity Tier, Min Student Year, GPS coordinates).
  * Section 1: Executive Summary & Context.
  * Section 2: Technical Problem Breakdown (WHAT).
  * Section 3: Geographic & Site Topography (WHERE).
  * Section 4: Root Cause Analysis & Previous Repair Failure History (WHY).
  * Section 5: Community Hazard & Stakeholder Impact (WHO).
  * Section 6: Recommended Engineering Scope & Prototypes (HOW).
  * Academic Eligibility & Safety Guardrail Box.

### 9. `POST /academic/chronic-problems/{escalation_id}/generate-dossier`
Synthesizes and regenerates the engineering dossier using Google Gemini AI.
* **Request Body (Optional):**
```json
{
  "gemini_api_key": "YOUR_GEMINI_API_KEY_HERE"
}
```
* **Response (JSON):**
```json
{
  "status": "success",
  "action": "DOSSIER_PDF_GENERATED",
  "escalation_id": "ESC-00FDBE",
  "pdf_path": "ai-engine/part-b/uploads/dossiers/Engineering_Dossier_ESC-00FDBE.pdf",
  "download_url": "/academic/chronic-problems/ESC-00FDBE/dossier-pdf"
}
```
*(Note: If `gemini_api_key` is omitted, the engine uses the environment variable or its deterministic municipal engineering fallback with 100% uptime).*

---

### 🧪 Running Academic Engine Tests

Both test verification suites are located inside `part-b/academic/`:

```powershell
# From the 'part-b' root:
python academic/test_academic.py
python academic/test_academic_api.py

# Or directly inside 'part-b/academic':
cd academic
python test_academic.py
python test_academic_api.py
```
