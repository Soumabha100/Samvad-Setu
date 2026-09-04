# 🤖 Samvad-Setu Autonomous Civic AI-Agent

Module: `ai-engine/ai-agent/`

---

## 📌 Purpose
The **Samvad-Setu AI-Agent** is a zero-retraining autonomous orchestrator that unites:
- **`part-a/`**: Indic NLP, municipal department classification, SLA computation, and rule-based severity.
- **`part-b/`**: Multimodal YOLO11 vision detection, Whisper voice triage, spatial deduplication ($\le 150\text{m}$), HEI Problem Bank escalation, 4-tier complexity scoring, 1st-year safety guardrail, AICTE syllabus matching, publication-grade Gemini 3.6 Flash PDF Engineering Dossier generation, corporate CSR showcase, Tripartite Governance (Civic Commons License CCL v1.0), 3-tranche milestone escrow, ULB site clearance gatekeeper, and official MCA Section 135 CSR impact audit certification.

---

## 📁 Package Contents

```text
ai-engine/ai-agent/
├── __init__.py         # Exports CivicOrchestratorAgent & get_civic_orchestrator
├── agent.py            # Master autonomous orchestrator class and lifecycle state machine
├── test_agent.py       # End-to-end unit test suite validating all 6 lifecycle stages
└── README.md           # This documentation
```

---

## ⚡ Integration for Backend Developers
Your backend teammate only needs to call:
```http
POST http://localhost:8000/agent/automate
```

For complete integration instructions and payload schemas, see:
- [`../BACKEND_AGENT_INTEGRATION_GUIDE.md`](../BACKEND_AGENT_INTEGRATION_GUIDE.md)
