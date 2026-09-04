# 🤖 Samvad-Setu AI-Agent: Developer Integration Guide for Backend Team

> **Welcome to the Samvad-Setu AI-Engine!**  
> To make your life as a backend engineer easy, **you do NOT need to learn Python or integrate 10+ separate microservices**.  
> We have unified the entire civic lifecycle into **ONE single HTTP endpoint**:  
> ```http
> POST http://localhost:8000/agent/automate
> ```
> This guide shows you exactly where and how to plug this endpoint into your Node.js/Express backend in `server/`.

---

## 🏛️ End-to-End System Architecture

```text
               👤 CITIZEN GRIEVANCE SUBMISSION
           (Photo / Video / Voice Audio / Text / GPS)
                               ↓
         🧠 MULTIMODAL INGESTION & TRIAGE (Part B)
   [YOLO11 Vision]    [Whisper Voice]    [Part A Indic NLP]
   (Pothole/Garbage)  (Speech-to-Text)   (Dept & SLA Target)
                               ↓
          🔍 SMART DEDUPLICATION & SPATIAL FUSION
    (≤150m + Text/Vision Cosine Sim ➡️ Fuse to Master Ticket)
                               ↓
          🏛️ PHASE 1: MUNICIPAL GOVERNMENT ATTEMPT
                (SLA Window: e.g. 7 - 14 Days)
                               ↓
                    Is the Problem Solved?
                   /                      \
                 YES                       NO (Failed / Chronic Recurrence)
                 /                          \
        ✅ CASE CLOSED                       🚨 ESCALATION ENGINE (Part B)
     (Standard Municipal Fix)          (SLA breached OR ≥3 reports over weeks)
                                             ↓
                                 🎓 HEI PROBLEM STATEMENT BANK
                                   (Zero dummy/mock seed data)
                                             ↓
                                 ⚖️ 4-TIER COMPLEXITY SCORER
                                (Tier 1: Foundation to Tier 4: R&D)
                                             ↓
                                 🛡️ 1ST-YEAR SAFETY GUARDRAIL
                                (Blocks junior 1st-year students from
                                 taking impossible high-risk R&D tasks)
                                             ↓
                                 📚 AICTE SYLLABUS MATCHER
                               (TF-IDF Vector Matching against Course
                                Outcomes: Civil, CSE, Environmental)
                                             ↓
                              📄 PROFESSIONAL ENGINEERING DOSSIER
                               (Gemini 3.6 Flash + ReportLab PDF Engine)
                             [WHAT, WHERE, WHY, WHO, HOW Capstone Scope]
                                             ↓
                              🛠️ HEI STUDENT CAPSTONE PROTOTYPE
                               (Students build real-world working
                                prototype with BoM & TRL 1-7 level)
                                             ↓
                              🏢 CORPORATE PROTOTYPE SHOWCASE
                               (Industry & Corporate Trusts Portal)
                                             ↓
                             🎯 AI CSR SPONSOR MATCHING ENGINE
                              (Matches prototype to Corporate Partner
                               via MCA Schedule VII Tax Taxonomy)
                                             ↓
                           ⚖️ TRIPARTITE GOVERNANCE FRAMEWORK
                          (HEI Students + Municipal ULB + Corporate)
                                             ↓
                           📜 CIVIC COMMONS LICENSE (CCL v1.0)
                         (ULB gets royalty-free public use license;
                          Students keep patent/academic priority;
                          Company gets CSR Title & Tax benefits)
                                             ↓
                           💰 3-TRANCHE MILESTONE ESCROW PLEDGE
                          • Tranche 1 (30%): Lab Build & BoM Buy ➡️ Released
                          • Tranche 2 (40%): Field Pilot ➡️ [LOCKED]
                          • Tranche 3 (30%): Final Handover ➡️ [LOCKED]
                                             ↓
                          🚧 MUNICIPAL SITE CLEARANCE GATEKEEPER
                         (Urban Local Body Engineer must inspect and
                          grant permit before Tranche 2 unlocks)
                                             ↓
                          🚀 REAL-WORLD MUNICIPAL PILOT DEPLOYMENT
                                             ↓
                          🏁 FINAL CIVIC HANDOVER & PERMANENT FIX
                                             ↓
                         📜 MCA SECTION 135 CSR IMPACT CERTIFICATE
                         (Generated automatically for Corporate Board
                          Tax Deductions & Relieved Citizens!)
```

---

## ⚙️ 1. Quick Setup in `server/`

### Step 1: Install Axios in `server/`
```bash
cd server
npm install axios
```

### Step 2: Add AI-Engine URL to `server/.env`
Add this line to your `server/.env` file:
```env
AI_ENGINE_URL=http://localhost:8000
```

---

## 📁 2. Where to Add Code in Your Backend

All grievance routing in your backend is located in:
👉 `server/src/routes/problemRoutes.js`

Here is the **complete, copy-paste ready Express.js implementation** for `server/src/routes/problemRoutes.js`:

```javascript
const express = require("express");
const router = express.Router();
const axios = require("axios");
const { protect, authorize } = require("../middleware/authMiddleware");
const Problem = require("../models/Problem");

// Central URL pointing to the Python AI Engine
const AI_ENGINE = process.env.AI_ENGINE_URL || "http://localhost:8000";

// ============================================================================
// STAGE 1: CITIZEN SUBMITS GRIEVANCE
// Runs: Part A NLP (Dept & SLA), YOLO11 Vision, & Spatial Deduplication (<=150m)
// ============================================================================
router.post("/", protect, authorize("citizen"), async (req, res) => {
  try {
    // 1. Forward citizen grievance to AI-Agent
    const aiResponse = await axios.post(`${AI_ENGINE}/agent/automate`, {
      action: "CITIZEN_SUBMISSION",
      payload: {
        citizen_name: req.user.name || "Citizen",
        text: req.body.description || req.body.title,
        category: req.body.category,
        location: req.body.location, // { lat: 28.6139, lng: 77.2090, address: "Ward 4" }
        image_path: req.body.image
      }
    });

    const aiData = aiResponse.data;

    // 2. Save problem to MongoDB with the AI Master Ticket ID & SLA targets
    const newProblem = new Problem({
      ...req.body,
      ticketId: aiData.ticket_id || aiData.master_ticket_id,
      category: aiData.ticket?.category || req.body.category,
      department: aiData.ticket?.department || "Public Works Department",
      severity: aiData.ticket?.severity || "medium",
      slaHours: aiData.ticket?.sla_hours || 72,
      reportedBy: req.user._id,
      timeline: [
        { stage: "Reported", timestamp: new Date(), actor: "Citizen" },
        { stage: "Triaged by AI-Agent", timestamp: new Date(), actor: "Samvad-Setu AI" }
      ]
    });

    const savedProblem = await newProblem.save();

    res.status(201).json({
      status: "success",
      problem: savedProblem,
      ai_result: aiData
    });
  } catch (error) {
    res.status(500).json({ message: "Grievance submission error", error: error.message });
  }
});

// ============================================================================
// STAGE 2: MUNICIPAL GOVERNMENT ATTEMPT & ESCALATION TRIGGER
// If RESOLVED -> Problem closed
// If FAILED -> Autonomously escalates to HEI Bank & generates Gemini PDF Dossier
// ============================================================================
router.patch("/:id/moderate", protect, authorize("government_admin", "govt_admin"), async (req, res) => {
  try {
    const problem = await Problem.findById(req.params.id);
    if (!problem) return res.status(404).json({ message: "Problem not found" });

    // Call AI-Agent with Municipal Attempt Outcome
    const aiResponse = await axios.post(`${AI_ENGINE}/agent/automate`, {
      action: "GOVERNMENT_STATUS_UPDATE",
      payload: {
        ticket_id: problem.ticketId || req.params.id,
        attempt_status: req.body.status, // "RESOLVED" or "FAILED"
        officer_name: req.user.name,
        notes: req.body.notes || "Contractor cold patch washed away by rain.",
        generate_dossier: true
      }
    });

    // Update MongoDB status
    problem.status = req.body.status === "RESOLVED" ? "Resolved" : "Escalated_To_HEI";
    problem.timeline.push({
      stage: problem.status,
      timestamp: new Date(),
      actor: req.user.name
    });

    await problem.save();

    res.json({
      status: "success",
      problem_status: problem.status,
      ai_result: aiResponse.data
    });
  } catch (error) {
    res.status(500).json({ message: "Moderation error", error: error.message });
  }
});

// ============================================================================
// STAGE 3: HEI STUDENT CAPSTONE PROTOTYPE SUBMISSION
// Validates 1st-Year Safety Guardrail, registers in Showcase, & matches CSR sponsors
// ============================================================================
router.post("/:id/prototype", protect, authorize("hei", "hei_admin"), async (req, res) => {
  try {
    const problem = await Problem.findById(req.params.id);
    if (!problem) return res.status(404).json({ message: "Problem not found" });

    const aiResponse = await axios.post(`${AI_ENGINE}/agent/automate`, {
      action: "HEI_PROTOTYPE_SUBMIT",
      payload: {
        ticket_id: problem.ticketId || req.params.id,
        prototype_title: req.body.prototype_title,
        team_name: req.body.team_name,
        institution_name: req.body.institution_name,
        faculty_mentor: req.body.faculty_mentor,
        student_year_level: req.body.student_year_level || 4, // 1st-year students blocked from Tier 3-4
        trl_level: req.body.trl_level || 6,
        total_funding_required_inr: req.body.total_funding_required_inr || 250000.0,
        bill_of_materials: req.body.bill_of_materials || [],
        technical_abstract: req.body.technical_abstract
      }
    });

    res.json({
      status: "success",
      message: "Prototype registered in Corporate Showcase",
      data: aiResponse.data
    });
  } catch (error) {
    res.status(error.response?.status || 500).json({
      message: error.response?.data?.detail || error.message
    });
  }
});

// ============================================================================
// STAGE 4: CORPORATE CSR FUNDING PLEDGE
// Tripartite Governance (CCL v1.0) & 3-Tranche Milestone Escrow (30% released)
// ============================================================================
router.post("/:id/pledge", protect, authorize("corporate", "sponsor"), async (req, res) => {
  try {
    const problem = await Problem.findById(req.params.id);
    if (!problem) return res.status(404).json({ message: "Problem not found" });

    const aiResponse = await axios.post(`${AI_ENGINE}/agent/automate`, {
      action: "CORPORATE_PLEDGE",
      payload: {
        ticket_id: problem.ticketId || req.params.id,
        sponsor_id: req.body.sponsor_id || "CORP-TATA-01",
        pledged_amount_inr: req.body.pledged_amount_inr || 250000.0,
        representative_name: req.user.name,
        contact_email: req.user.email
      }
    });

    res.json({
      status: "success",
      message: "CSR Pledge registered & Tranche 1 (30%) disbursed to HEI Lab Escrow",
      data: aiResponse.data
    });
  } catch (error) {
    res.status(500).json({ message: "Corporate pledge error", error: error.message });
  }
});

// ============================================================================
// STAGE 5: MUNICIPAL SITE CLEARANCE GATEKEEPER
// ULB Engineer inspects public site and unlocks Tranche 2 (40%) Field Pilot
// ============================================================================
router.post("/:id/site-clearance", protect, authorize("government_admin"), async (req, res) => {
  try {
    const problem = await Problem.findById(req.params.id);
    if (!problem) return res.status(404).json({ message: "Problem not found" });

    const aiResponse = await axios.post(`${AI_ENGINE}/agent/automate`, {
      action: "MUNICIPAL_SITE_CLEARANCE",
      payload: {
        ticket_id: problem.ticketId || req.params.id,
        officer_name: req.user.name,
        site_inspection_notes: req.body.notes || "Site surveyed. Traffic diversion verified. Pilot permitted."
      }
    });

    res.json({
      status: "success",
      message: "Site clearance granted & Tranche 2 (40%) disbursed for Field Pilot",
      data: aiResponse.data
    });
  } catch (error) {
    res.status(500).json({ message: "Site clearance error", error: error.message });
  }
});

// ============================================================================
// STAGE 6: FINAL CIVIC HANDOVER & MCA SECTION 135 CSR CERTIFICATE
// Disburses Tranche 3 (30%) & auto-generates Statutory CSR Tax Certificate
// ============================================================================
router.post("/:id/handover-certificate", protect, authorize("corporate_auditor", "government_admin"), async (req, res) => {
  try {
    const problem = await Problem.findById(req.params.id);
    if (!problem) return res.status(404).json({ message: "Problem not found" });

    const aiResponse = await axios.post(`${AI_ENGINE}/agent/automate`, {
      action: "CIVIC_HANDOVER_AND_CERTIFICATION",
      payload: {
        ticket_id: problem.ticketId || req.params.id,
        corporate_auditor_name: req.user.name,
        handover_notes: req.body.notes || "Tested for 30 consecutive days with zero defects. Remediation permanent."
      }
    });

    res.json({
      status: "success",
      message: "Civic Handover complete & MCA Section 135 CSR Certificate issued",
      data: aiResponse.data
    });
  } catch (error) {
    res.status(500).json({ message: "Handover certification error", error: error.message });
  }
});

module.exports = router;
```

---

## ⚡ 3. Master Endpoint API Reference (`POST /agent/automate`)

All requests go to: `http://localhost:8000/agent/automate`  
Format:
```json
{
  "action": "<ACTION_NAME>",
  "payload": { ... }
}
```

### Supported Actions Table

| Action Name | When to Call It | What the AI Does |
|---|---|---|
| `CITIZEN_SUBMISSION` | Citizen files report | Ingests text/photo/voice, computes SLA, & fuses nearby duplicates ($\le 150\text{m}$) into a Master Ticket |
| `GOVERNMENT_STATUS_UPDATE` | Govt attempts fix | If `RESOLVED` $\rightarrow$ Closes ticket. If `FAILED` $\rightarrow$ Escalates to HEI Bank & generates Gemini PDF Dossier |
| `HEI_PROTOTYPE_SUBMIT` | Students submit prototype | Enforces 1st-year guardrail, publishes to Corporate Portal, & matches CSR sponsors |
| `CORPORATE_PLEDGE` | Company funds prototype | Signs Civic Commons License & disburses **Tranche 1 (30%)** to HEI lab |
| `MUNICIPAL_SITE_CLEARANCE` | ULB Engineer inspects site | Verifies public safety & unlocks **Tranche 2 (40%)** for field pilot |
| `CIVIC_HANDOVER_AND_CERTIFICATION` | Permanent fix validated | Disburses **Tranche 3 (30%)** & issues official **MCA Section 135 CSR-1 Impact Certificate** |

---

## 🔍 4. Helpful Query Endpoints

Your backend can also query ticket state anytime:

1. **Get Single Ticket Audit Trail & Status**:
   ```http
   GET http://localhost:8000/agent/tickets/:ticket_id
   ```
   *Returns full evidence gallery, dossier PDF path, milestone escrow balances, and CSR certificate.*

2. **List All Managed Tickets**:
   ```http
   GET http://localhost:8000/agent/tickets
   ```

3. **Get Full Workflow State Machine Specification**:
   ```http
   GET http://localhost:8000/agent/workflow
   ```

---

## 🛑 5. HTTP Error Handling Guide

| Status Code | Meaning | What to Do |
|---|---|---|
| **`200 OK`** | Action completed successfully | Proceed to next stage |
| **`400 Bad Request`** | Missing required payload field (e.g. missing `ticket_id`) | Check payload keys against this guide |
| **`403 Forbidden`** | **Guardrail Activated**: Either a 1st-year student tried submitting a high-risk Tier 3/4 task, or a non-municipal user attempted site clearance | Display warning to user in frontend |
| **`404 Not Found`** | Ticket ID not found in active store | Verify the ticket ID |
| **`500 Internal Error`** | AI Engine internal error | Check terminal logs in `part-b` |

---

## 🚀 6. Starting the AI-Engine Locally

Make sure the Python AI engine is running in your terminal on Port 8000:
```powershell
cd ai-engine/part-b
uvicorn main:app --reload --port 8000
```
Interactive Swagger UI is live at: **`http://localhost:8000/docs`**
