# 🤖 Samvad-Setu AI Engine

This directory consolidates all Artificial Intelligence, Natural Language Processing, Multimodal Computer Vision, Voice Triage, Academic HEI Routing, and Corporate CSR Escrow services for the Samvad-Setu platform.

---

## ⚙️ Environment Configuration (`.env`)

API keys and service settings are configured via the single central `.env` at `ai-engine/.env`:
```bash
GEMINI_API_KEY="Your_Gemini_API_Key"
AI_ENGINE_HOST=127.0.0.1
AI_ENGINE_PORT=8000
```

---

## 📁 Directory Architecture

```text
ai-engine/
├── .env                                # Master environment configuration (active API key)
├── .env.example                        # Environment template for team members
├── BACKEND_AGENT_INTEGRATION_GUIDE.md   # Unified single-endpoint integration guide
├── FRONTEND_INTEGRATION_GUIDE.md       # Integration guide for frontend & backend teams
├── README.md                           # Central AI Engine architecture overview
│
├── ai-agent/                           # Autonomous Civic AI-Agent Orchestrator
│   ├── __init__.py                     # Package exports
│   ├── agent.py                        # Master CivicOrchestratorAgent lifecycle engine
│   ├── test_agent.py                   # Full end-to-end 6-stage lifecycle test suite
│   └── README.md                       # Agent package documentation
│
├── part-a/                             # Indic NLP & Municipal Department Triage
│   ├── dataset/                        # Training datasets
│   ├── models/                         # Model weights and vectorizers
│   ├── api.py                          # Part A standalone microservice
│   ├── predict.py                      # Text inference script
│   ├── preprocess.py                   # Indic text normalizer
│   ├── severity_rules.py               # SLA and urgency heuristic rules
│   ├── train.py                        # Model training pipeline
│   ├── requirements.txt                # Part A Python dependencies
│   └── Docs.md                         # Part A documentation
│
└── part-b/                             # Multimodal AI, Academic & Corporate Engine
    ├── .env                            # Part B environment configuration
    ├── .gitignore                      # Git ignore rules
    ├── main.py                         # Unified FastAPI server (Port 8000)
    ├── dedup.py                        # Spatial & semantic deduplication engine
    ├── requirements.txt                # Part B Python dependencies
    ├── Docs.md                         # Complete API and schema documentation
    │
    ├── academic/                       # Academic HEI Routing & Problem Bank
    │   ├── __init__.py
    │   ├── institutions_data.py        # Indian HEIs (IITs/NITs) with AISHE codes
    │   ├── complexity_scorer.py        # 4-tier problem complexity classifier
    │   ├── syllabus_engine.py          # AICTE syllabus matching & 1st-year guardrail
    │   ├── sample_syllabi.py           # AICTE model curricula (Civil, CSE, Env)
    │   ├── escalation_engine.py        # SLA breach & chronic recurrence pool
    │   ├── dossier_generator.py        # Gemini 3.6 Flash + ReportLab PDF engine
    │   ├── test_academic.py            # Academic unit tests
    │   └── test_academic_api.py        # Academic FastAPI integration tests
    │
    ├── corporate/                      # Corporate CSR Funding & Prototype Showcase
    │   ├── __init__.py
    │   ├── prototypes_data.py          # Prototype models (TRL 1-7, BoM) & corporate trusts
    │   ├── stakeholder_governance.py   # Tripartite agreement & 3-tranche milestone escrow
    │   ├── csr_engine.py               # Schedule VII matching & CSR-1 audit certificates
    │   ├── test_corporate.py           # Corporate unit tests
    │   └── test_corporate_api.py       # Corporate FastAPI integration tests
    │
    ├── image/                          # YOLO11 vision detection model
    ├── voice/                          # Whisper voice transcription service
    ├── models/                         # Trained vision weights
    └── uploads/                        # Runtime uploads & generated dossiers
        └── dossiers/                   # Generated engineering PDF briefs
```

---

## 🤖 Unified Autonomous AI-Agent (`POST /agent/automate`)

To prevent the backend team from having to manage 10+ disparate endpoints across `part-a` and `part-b`, a **unified autonomous AI-Agent orchestrator** (`agent.py`) connects the entire civic lifecycle:

- **Single Master Dispatcher**: `POST http://localhost:8000/agent/automate`
- **Audit & State Tracking**: `GET http://localhost:8000/agent/tickets` & `GET /agent/tickets/{ticket_id}`
- **Zero Training Guarantee**: Uses pre-existing trained models from Part A and Part B without any retraining or model modifications.
- **Complete Documentation & Payloads**: See [`BACKEND_AGENT_INTEGRATION_GUIDE.md`](./BACKEND_AGENT_INTEGRATION_GUIDE.md).

---

## 🚀 Running the Engine & Verification Tests

### 1. Start the Unified Server
```powershell
cd ai-engine/part-b
uvicorn main:app --reload --port 8000
```
Interactive Swagger API documentation is live at **`http://localhost:8000/docs`**.

### 2. Run Academic HEI Test Suite
```powershell
cd ai-engine/part-b
python academic/test_academic.py
python academic/test_academic_api.py
```

### 3. Run Corporate CSR & Escrow Test Suite
```powershell
cd ai-engine/part-b
python corporate/test_corporate.py
python corporate/test_corporate_api.py
```

---

## 🔗 Integration Guides

- **Unified Backend AI-Agent Guide**: [`BACKEND_AGENT_INTEGRATION_GUIDE.md`](./BACKEND_AGENT_INTEGRATION_GUIDE.md) (Single endpoint integration for backend developer)
- **Frontend Integration Guide**: [`FRONTEND_INTEGRATION_GUIDE.md`](./FRONTEND_INTEGRATION_GUIDE.md) (UI checklist and styling tokens)
- Teammate directories `client/` and `server/` remain strictly isolated and protected.

