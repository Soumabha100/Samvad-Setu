# Samvad Setu AI — Part-B Image Verification
## Cross-Machine Setup & Team Member Guide

This guide explains what a teammate needs to do after cloning or pulling the repository to run the existing Part-B image verification model on another machine.

> **Important:** This guide is for running the already-trained model. A teammate does not need to download the original training datasets or retrain the model.

## 1. Included Files

```text
part-b/
├── image/
│   ├── api.py
│   ├── predict.py
│   ├── prepare_dataset.py
│   ├── severity.py
│   ├── taxonomy.json
│   └── train.py
├── voice/
│   ├── api.py
│   ├── citizen_report.mp3
│   └── whisper_service.py
├── models/
│   └── vision_model.pt
├── requirements.txt
├── Docs.md
└── main.py
```

The trained model is:

```text
part-b/models/vision_model.pt
```

The model is approximately **5.47 MB** and is included in Git.

## 2. Supported Civic Issues (8 Classes)

| Class ID | Issue | Scope | Department |
|---:|---|---|---|
| 0 | pothole | Road Pothole | Public Works Department (PWD - Roads) |
| 1 | garbage | Waste Dump / Litter | Solid Waste & Sanitation Department |
| 2 | crack | Surface Crack | Public Works Department (PWD - Roads) |
| 3 | open_manhole | Open Manhole | PHED Drainage (Critical Hazard) |
| 4 | waterlogging | Roadway Flooding | PHED Drainage / Stormwater |
| 5 | stray_animal | Cattle / Stray Animals | Animal Control & Public Safety Unit |
| 6 | traffic_light | Malfunctioning Signal | Traffic Police & Electrical Division |
| 7 | waste_container | Overflowing Dumpster | Solid Waste & Sanitation Department |

The system returns issue type, confidence, object count, individual severity, and overall incident severity.

## 3. Before Pulling

If you already have the repository:

```powershell
git branch
```

For the Part-B branch:

```powershell
git checkout partB
git pull origin partB
```

If Part-B has been merged into `main`:

```powershell
git checkout main
git pull origin main
```

> Use the branch your team has agreed to use. Do not overwrite another teammate's uncommitted work.

## 4. Required Software

Install:

- Git
- Python 3.10+
- VS Code (recommended)
- Internet connection for Python package installation

Check:

```powershell
python --version
git --version
```

## 5. Clone the Repository

For a new machine:

```powershell
git clone https://github.com/Team-Phoenix-100/Samvad-Setu.git
cd Samvad-Setu
cd part-b
```

## 6. Verify the Trained Model

From inside `part-b`:

```powershell
Get-Item ".\models\vision_model.pt"
```

The file must exist.

The original training datasets are **not required for normal prediction**.

## 7. Install Dependencies

From:

```text
Samvad-Setu/part-b
```

run:

```powershell
pip install -r requirements.txt
```

If `pip` is not recognized:

```powershell
python -m pip install -r requirements.txt
```

## 8. Important: No Developer-Specific Paths

The project must not depend on paths such as:

```text
C:\Users\MYPC\OneDrive\Documents\Samvad-Setu\...
```

The trained model should be referenced relative to the project:

```text
part-b/models/vision_model.pt
```

This allows the project to work on different computers and usernames.

## 9. Direct Prediction Test

Go to:

```powershell
cd image
```

Then test an image:

```powershell
python predict.py test.jpg
```

Example output:

```text
Detected objects: 2

Object #1
Issue: garbage
Confidence: 0.68
Severity: MEDIUM

Object #2
Issue: garbage
Confidence: 0.37
Severity: LOW

--------------------------------
INCIDENT SUMMARY
--------------------------------

Overall Issue: garbage
Objects Detected: 2
Overall Severity: MEDIUM
```

## 10. Start the FastAPI Server

From:

```text
Samvad-Setu/part-b/image
```

run:

```powershell
uvicorn api:app --reload
```

If `uvicorn` is not recognized:

```powershell
python -m uvicorn api:app --reload
```

The API should run at:

```text
http://127.0.0.1:8000
```

Keep this terminal running.

## 11. Test the API

Open:

```text
http://127.0.0.1:8000
```

Then open:

```text
http://127.0.0.1:8000/docs
```

The `/docs` page provides an interactive way to test the API.

## 12. Test POST /predict

The main endpoint is:

```text
POST /predict
```

It expects:

```text
multipart/form-data
```

with the field name:

```text
file
```

Using Swagger:

1. Open `/docs`.
2. Find `POST /predict`.
3. Click **Try it out**.
4. Click **Choose File**.
5. Select an image.
6. Click **Execute**.
7. Check the JSON response.

## 13. Test with Postman

Request:

```text
POST http://127.0.0.1:8000/predict
```

Select:

```text
Body → form-data
```

Add:

| Key | Type | Value |
|---|---|---|
| `file` | File | Select an image |

The key must be exactly:

```text
file
```

Do **not** manually set the `Content-Type` header. Postman creates the multipart boundary automatically.

## 14. Example API Response

```json
{
    "success": true,
    "detected": true,
    "overall_issue": "garbage",
    "overall_severity": "MEDIUM",
    "objects_detected": 2,
    "detections": [
        {
            "issue": "garbage",
            "confidence": 0.68,
            "severity": "MEDIUM"
        },
        {
            "issue": "garbage",
            "confidence": 0.37,
            "severity": "LOW"
        }
    ]
}
```

Exact confidence values depend on the uploaded image.

## 15. Node.js Integration

Node.js does **not** need to load the `.pt` file directly.

The architecture is:

```text
Citizen
   |
   | Upload Image
   v
Frontend
   |
   | multipart/form-data
   v
Node.js Backend
   |
   | POST /predict
   v
Python FastAPI
   |
   v
YOLO11n Model
   |
   v
Prediction JSON
   |
   v
Node.js Backend
   |
   v
Frontend / Database
```

### Same computer

If Node.js and Python run on the same computer:

```text
http://127.0.0.1:8000/predict
```

Both services must be running.

### Different computers

`127.0.0.1` means the current computer, so it will not connect two different machines.

The Python API must be reachable through a network address or deployed service, for example:

```text
http://<python-machine-ip>:8000/predict
```

or a deployed API URL.

## 16. Do Not Retrain Just to Run It

A teammate who only wants inference should **not** run the training process.

The trained model is already:

```text
part-b/models/vision_model.pt
```

The training datasets are not required for normal inference.

## 17. Severity Logic

Current prototype rules:

```text
open_manhole → CRITICAL

confidence >= 0.75 → HIGH
confidence >= 0.50 → MEDIUM
confidence < 0.50 → LOW
```

This is a prototype rule. Detection confidence is not the same as real-world severity. The final system can later combine image evidence with location, affected population, road importance, multiple reports, and other information.

## 18. Common Errors

### `uvicorn` is not recognized

```powershell
python -m uvicorn api:app --reload
```

### `ModuleNotFoundError`

```powershell
pip install -r requirements.txt
```

or:

```powershell
python -m pip install -r requirements.txt
```

### Model not found

Verify:

```text
part-b/models/vision_model.pt
```

Also make sure the API is started from:

```text
part-b/image
```

### `422 Unprocessable Content`

In Postman verify:

```text
Body → form-data
Key = file
Type = File
```

Do not send the image as raw JSON.

### No detection

Try a clear image containing one of the supported classes:

```text
pothole
garbage
crack
open manhole
```

The current model is a prototype and can produce false positives or false negatives.

## 19. Beginner Quick Start

If you already have Git and Python:

```powershell
git checkout main
git pull origin main

cd part-b

pip install -r requirements.txt

Get-Item ".\models\vision_model.pt"

cd image

python -m uvicorn api:app --reload
```

Then open:

```text
http://127.0.0.1:8000/docs
```

Use:

```text
POST /predict
```

and upload an image using the field:

```text
file
```

## 20. Final Checklist

- [ ] Repository cloned or latest branch pulled
- [ ] Python installed
- [ ] `part-b` directory accessible
- [ ] `requirements.txt` installed
- [ ] `part-b/models/vision_model.pt` exists
- [ ] No developer-specific Windows path is required
- [ ] FastAPI starts successfully
- [ ] `http://127.0.0.1:8000` opens
- [ ] `/docs` opens
- [ ] `/predict` is visible
- [ ] Image upload works
- [ ] Issue type is returned
- [ ] Confidence is returned
- [ ] Severity is returned
- [ ] Object count is returned

## 21. Current Module Status

| Component | Status |
|---|---|
| Dataset preparation | Completed |
| YOLO11n model | Trained |
| Trained model included in Git | Yes |
| Pothole detection | Supported |
| Garbage detection | Supported |
| Crack detection | Supported |
| Open manhole detection | Supported |
| Severity calculation | Implemented |
| Direct prediction script | Implemented |
| FastAPI API | Implemented |
| Postman testing | Completed |
| Node.js integration | Ready |

## 22. Important Git Rule

If the model is replaced, make sure the new:

```text
part-b/models/vision_model.pt
```

is committed and pushed.

If Python dependencies change, update:

```text
part-b/requirements.txt
```

If the setup process changes, update this documentation.

## Goal

A new teammate should be able to:

```text
CLONE / PULL
     ↓
INSTALL REQUIREMENTS
     ↓
VERIFY MODEL
     ↓
START API
     ↓
UPLOAD IMAGE
     ↓
GET AI RESULT
```

without needing the original developer's computer, local Windows paths, training datasets, or training process.

---

**Samvad Setu AI — Part-B Image Verification Engine**
