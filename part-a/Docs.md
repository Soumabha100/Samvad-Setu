# 🌉 Samvad-Setu: Part A — Quick Start Guide

Welcome! This folder contains **Part A (Municipal Operations AI)** of the Samvad-Setu platform.

Part A is a lightweight, high-speed NLP engine that reads citizen complaints in **English, Hindi, Bengali, or Hinglish** and automatically outputs:
1. **Municipal Department Routing** (e.g., Public Works, Sanitation, PHED Drainage, Fire Safety).
2. **Urgency & SLA Response Deadline** (Critical: 4h, High: 24h, Medium: 72h, Low: 7 days).

---

## 🚀 Quick Setup (3 Steps)

> **Note:** The trained AI models are already saved in `models/`. You **do not** need to retrain them to start using the system!

### Step 1: Navigate to Part A
Open your terminal and enter the `part-a` directory:
```bash
cd part-a
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Test a Complaint in the Terminal
Run the CLI inference script:
```bash
python predict.py "School ke paas road pe massive deep pothole hai, accident risk!"
```

You can also launch the **interactive terminal mode**:
```bash
python predict.py -i
```

---

## ⚡ Running the API & Testing in Postman

We built a simple **FastAPI** service so you or our backend teammates can test predictions via Postman.

### 1. Start the Server
Run this in your terminal:
```bash
uvicorn api:app --reload --port 8000
```
*(The server will start at `http://127.0.0.1:8000`)*

### 2. Test in Postman

#### 🔹 Method: POST
* **URL:** `http://127.0.0.1:8000/predict`
* **Headers:** 
  * `Content-Type`: `application/json`
* **Body** (Select `raw` -> `JSON`):
```json
{
  "text": "রাস্তায় আবর্জনা স্তূপ হয়ে পড়ে আছে দুর্গন্ধ ছড়াচ্ছে"
}
```

#### 🔹 Sample Response:
```json
{
  "category": "garbage",
  "department": "Solid Waste & Sanitation Department",
  "severity": "medium",
  "sla_hours": 72,
  "priority_level": 3,
  "priority_description": "Standard Municipal Ticket (3 Days)",
  "confidence": {
    "category": 0.9537,
    "severity": 0.8575
  },
  "status": "success"
}
```

#### 🔹 Verified Postman Test Cases:
Try testing any of these real citizen reports:
* **Open Manhole Emergency:**
  `"Open manhole on the street without cover"` $\rightarrow$ Category: `drainage`, Severity: `critical` (4h SLA)
* **Road Damage:**
  `"School ke paas road pe massive deep pothole hai"` $\rightarrow$ Category: `road_damage`, Severity: `critical` (4h SLA)
* **Overflowing Waste Container:**
  `"Public dustbin is overflowing with waste on the footpath"` $\rightarrow$ Category: `garbage`, Severity: `medium` (72h SLA)
* **Monsoon Road Flooding:**
  `"Heavy waterlogging after rain water is entering shops"` $\rightarrow$ Category: `waterlogging`, Severity: `high` (24h SLA)
* **Traffic Signal Failure:**
  `"Traffic light is not working at the intersection"` $\rightarrow$ Category: `other`, Severity: `high` (24h SLA)

#### 🔹 Quick Browser / GET Test (No JSON needed):
Open your browser or Postman and visit:
```text
http://127.0.0.1:8000/test?text=Open manhole on the street without cover
```

---

## 📂 File Directory Overview

| File | What it does |
| :--- | :--- |
| `api.py` | FastAPI server for Postman & Node.js backend integration. |
| `predict.py` | Real-time prediction tool (CLI, Python function, or interactive). |
| `preprocess.py` | Cleans text (removes junk characters, URLs, normalizes Unicode). |
| `severity_rules.py` | Rule-based keyword detector for emergency safety checks. |
| `train.py` | Model training script (TF-IDF + Logistic Regression). |
| `prepare_training_data.py` | Preprocessing script to clean raw dataset into processed data. |
| `models/` | Contains the saved `.joblib` model files and metadata. |
| `dataset/` | Contains dataset generation scripts and CSV data files. |
| `requirements.txt` | List of required Python packages. |

---

## 🔄 How to Retrain Models (Optional)

If you ever add new complaint categories or change dataset templates, you can re-generate the dataset and retrain the models in 3 commands:

```bash
# 1. Generate 20,000 synthetic complaints
cd dataset
python generate_dataset.py
cd ..

# 2. Preprocess the dataset
python prepare_training_data.py

# 3. Train both Category and Severity models
python train.py
```

---

## 🤝 Questions or Integration
If you are integrating this with the Node.js Express backend (`/server`), send a `POST` request with `{ "text": complaintDescription }` to `http://localhost:8000/predict` to receive the category, department routing, and SLA turnaround hours.
