# 🎨 Samvad-Setu: Frontend Integration Blueprint & Field Specification

> **For Web Team (`client/`) & Mobile App Team (`mobile-app/`)**  
> This document details **exactly which frontend pages and components exist**, **what is missing**, and the **mandatory input fields each persona must submit** so that the AI Engine and AI-Agent work seamlessly without missing data or failures.

---

## 🏛️ End-to-End Persona & Lifecycle Architecture

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

## 📊 1. Frontend Audit: What Exists vs. What is Missing

### A. Web Application (`client/src/pages/`)

| Page / Persona | Existing File | What Already Exists | What is MISSING (Must Be Added) |
|---|---|---|---|
| **1. Citizen Submission** | `client/src/pages/citizen/SubmitProblem.jsx` | Text description, title, category dropdown, mock GPS, file upload. | **Real Voice Recording button** (`MediaRecorder` API) for Whisper audio. Display of **AI Triage Badge** (Department & SLA hours). Display of **Spatial Deduplication Notification** when report is fused into a nearby Master Ticket ($\le 150\text{m}$). |
| **2. Problem Details / Timeline** | `client/src/pages/public/ProblemDetail.jsx` | Static timeline, basic status badge, description. | **Municipal SLA Countdown Timer** (e.g., 7–14 days window). Dynamic action modals depending on logged-in user role (Govt, HEI, Industry). |
| **3. Municipal Admin (ULB)** | `client/src/pages/admin/AdminAnalytics.jsx` | High-level analytics graphs. | **Municipal Resolution Attempt Modal**: Allows ULB officer to mark problem as `RESOLVED` (standard fix) or `FAILED` (chronic recurrence with failure notes). **Site Clearance Gatekeeper Panel**: Allows ULB Engineer to inspect site and sign off to unlock Tranche 2. |
| **4. HEI Problem Bank** | `client/src/pages/hei/HeiProblemReview.jsx` | Basic list of issues with simulated claim alert. | Display of **4-Tier Complexity Badge** (Tier 1 Foundation to Tier 4 R&D). **Download PDF Engineering Dossier** button (Gemini ReportLab brief). **1st-Year Safety Guardrail Warning Banner** (blocks junior students from Tier 3–4). |
| **5. HEI Prototype Submit** | `client/src/pages/hei/HeiDashboard.jsx` | Basic student dashboard overview. | **Capstone Prototype Submission Form**: Fields for TRL Level (1–7), Bill of Materials (BoM array), Funding Goal, and Technical Abstract. |
| **6. Industry CSR Portal** | `client/src/pages/industry/IndustryBrowse.jsx` | Card list with a simulated alert button. | Display of **MCA Schedule VII CSR Eligibility Categories** (`item_iv`, `item_ii`). Display of **TRL Badge**. **Corporate Funding Pledge Modal** (accepts 3-Tranche Escrow terms & Civic Commons License). |
| **7. Final Handover & Audit** | *Missing component* | None. | **Handover Certification Panel**: Corporate auditor and ULB sign-off button to disburse Tranche 3 and **Download the Official MCA Section 135 CSR-1 Impact Certificate**. |

---

### B. Mobile App (`mobile-app/app/`)

| Persona | Existing Screen | What Exists | What is Missing |
|---|---|---|---|
| **Citizen** | `app/(citizen)/submit-problem/` | Camera upload, location picker. | Audio recorder component for speech-to-text; Live duplicate banner showing nearby reports ($\le 150\text{m}$). |
| **Government** | `app/(government)/ticket/` | Ticket status view. | Inspection sign-off button with GPS camera capture for the **Municipal Site Clearance Gatekeeper**. |

---

## 📝 2. Exact Fields Required by the AI Engine for Each Persona

To prevent the AI Engine from throwing missing-field errors, your frontend forms must collect and send the following **exact fields** to the backend at each stage:

---

### STAGE 1: Citizen Submission Form (`citizen`)
**Frontend Page**: `client/src/pages/citizen/SubmitProblem.jsx`  
**Backend Action**: `CITIZEN_SUBMISSION`

```json
{
  "action": "CITIZEN_SUBMISSION",
  "payload": {
    "citizen_name": "Rohan Sharma",
    "text": "Deep hazardous pothole on Main Ring Road near National High School.",
    "category": "road_damage",
    "location": {
      "lat": 28.6139,
      "lng": 77.2090,
      "address": "Ring Road Sector 4, New Delhi"
    },
    "image_path": "uploads/pothole1.jpg",
    "audio_path": "uploads/voice_complaint.mp3"
  }
}
```

#### Field Validation Rules for Frontend:
* `text`: **Required** (string, min 10 chars). If citizen uses voice note, send transcribed text or audio binary.
* `location.lat` & `location.lng`: **Required** (floats). Captured from browser `navigator.geolocation` or mobile GPS.
* `location.address`: **Recommended** (string, landmark or ward name).
* `image_path` / file: **Optional but recommended** (JPG/PNG). Passed to YOLO11 for visual defect bounding boxes.
* `audio_path`: **Optional** (MP3/WAV). Passed to Whisper for Indic voice transcription.

---

### STAGE 2: Municipal Resolution Attempt Modal (`government_admin`)
**Frontend Page**: `client/src/pages/public/ProblemDetail.jsx` or `client/src/pages/admin/`  
**Backend Action**: `GOVERNMENT_STATUS_UPDATE`

```json
{
  "action": "GOVERNMENT_STATUS_UPDATE",
  "payload": {
    "ticket_id": "TICKET-AB4129",
    "attempt_status": "FAILED",
    "officer_name": "Er. Rajesh Mehra, Junior Engineer PWD",
    "notes": "Surface cold-mix patch washed away by monsoon rainwater due to subgrade soil subsidence.",
    "generate_dossier": true
  }
}
```

#### Field Validation Rules for Frontend:
* `ticket_id`: **Required** (string). The Master Ticket ID.
* `attempt_status`: **Required** (`"RESOLVED"` or `"FAILED"`).
  * If `"RESOLVED"`: Closes the grievance with standard municipal repair.
  * If `"FAILED"`: Automatically triggers the Part B Escalation Engine, AICTE syllabus matching, and Gemini PDF Dossier generation.
* `officer_name`: **Required** (string). Name and designation of the inspecting engineer.
* `notes`: **Required if FAILED** (string). Why the standard contractor repair failed (e.g. soil mechanics, water table, heavy traffic).
* `generate_dossier`: **Boolean** (`true` by default). Triggers Gemini 3.6 Flash + ReportLab PDF generation.

---

### STAGE 3: HEI Student Prototype Submission Modal (`hei`)
**Frontend Page**: `client/src/pages/hei/HeiProblemReview.jsx` or `HeiDashboard.jsx`  
**Backend Action**: `HEI_PROTOTYPE_SUBMIT`

```json
{
  "action": "HEI_PROTOTYPE_SUBMIT",
  "payload": {
    "ticket_id": "TICKET-AB4129",
    "prototype_title": "TerraFix Bio-Polymer Self-Draining Asphalt Matrix",
    "team_name": "IIT Delhi Civil Tech Team",
    "institution_name": "Indian Institute of Technology Delhi",
    "faculty_mentor": "Prof. S. K. Bhattacharya",
    "student_year_level": 4,
    "trl_level": 6,
    "total_funding_required_inr": 250000.0,
    "bill_of_materials": [
      { "component": "Recycled Industrial Slag Aggregates", "estimated_cost_inr": 60000 },
      { "component": "Cold-Mix Bio-Polymer Binder", "estimated_cost_inr": 90000 },
      { "component": "Subsurface Pore-Pressure Sensor Mesh", "estimated_cost_inr": 50000 },
      { "component": "Field Compaction Pilot Testing", "estimated_cost_inr": 50000 }
    ],
    "technical_abstract": "Self-draining permeable asphalt matrix that prevents subsurface water saturation and structural cracking."
  }
}
```

#### Field Validation Rules for Frontend:
* `student_year_level`: **Required** (integer 1 to 4).
  * ⚠️ **Guardrail Notice**: If a 1st-year student selects year `1` for a Tier 2, 3, or 4 problem, the AI Engine returns `403 Forbidden` (`safety_guardrail_blocked`). Display this error banner to the user!
* `trl_level`: **Required** (integer 1 to 7). Technology Readiness Level (e.g., `4` = Lab validated, `6` = Pilot ready).
* `bill_of_materials`: **Required** (array of `{ component: string, estimated_cost_inr: number }`).
* `total_funding_required_inr`: **Required** (float). The total CSR budget requested.

---

### STAGE 4: Corporate CSR Pledge Modal (`industry_csr`)
**Frontend Page**: `client/src/pages/industry/IndustryBrowse.jsx`  
**Backend Action**: `CORPORATE_PLEDGE`

```json
{
  "action": "CORPORATE_PLEDGE",
  "payload": {
    "ticket_id": "TICKET-AB4129",
    "sponsor_id": "CORP-TATA-01",
    "pledged_amount_inr": 250000.0,
    "representative_name": "Dr. Ananya Sharma, Head of CSR",
    "contact_email": "csr.initiative@tatatrusts.org"
  }
}
```

#### Field Validation Rules for Frontend:
* `sponsor_id`: **Required** (dropdown of registered corporate foundations, e.g., Tata Trusts, Infosys Foundation, Reliance Foundation).
* `pledged_amount_inr`: **Required** (float). Total amount funded.
* **Escrow Checkbox 1**: *"I agree to the 3-Tranche Milestone Escrow Terms (30% Lab -> 40% Pilot -> 30% Handover)."*
* **Escrow Checkbox 2**: *"I accept the Civic Commons License (CCL v1.0) granting perpetual municipal royalty-free public use."*

---

### STAGE 5: Municipal Site Clearance Gatekeeper (`government_admin`)
**Frontend Page**: `client/src/pages/public/ProblemDetail.jsx` (Municipal Officer View)  
**Backend Action**: `MUNICIPAL_SITE_CLEARANCE`

```json
{
  "action": "MUNICIPAL_SITE_CLEARANCE",
  "payload": {
    "ticket_id": "TICKET-AB4129",
    "officer_name": "Er. Rajesh Mehra, Executive Engineer",
    "site_inspection_notes": "Site inspection completed. Traffic diversion plan verified. Authorized for public road pilot."
  }
}
```

#### Field Validation Rules for Frontend:
* `officer_name`: **Required** (string). Name of the Urban Local Body (ULB) officer.
* `site_inspection_notes`: **Required** (string). Technical confirmation that the site is safe for public student deployment.
* *Effect*: Unlocks **Tranche 2 (40%)** from escrow and transitions status to `"FIELD_PILOT_DEPLOYMENT_ACTIVE"`.

---

### STAGE 6: Civic Handover & CSR Impact Certificate (`corporate_auditor` / `government_admin`)
**Frontend Page**: `client/src/pages/public/ProblemDetail.jsx`  
**Backend Action**: `CIVIC_HANDOVER_AND_CERTIFICATION`

```json
{
  "action": "CIVIC_HANDOVER_AND_CERTIFICATION",
  "payload": {
    "ticket_id": "TICKET-AB4129",
    "corporate_auditor_name": "KPMG Statutory Auditor",
    "handover_notes": "Field pilot tested for 30 consecutive days under heavy monsoon traffic with zero defects. Permanent civic remediation complete."
  }
}
```

#### Field Validation Rules for Frontend:
* `corporate_auditor_name`: **Required** (string). Name of the statutory auditor or independent evaluator.
* `handover_notes`: **Required** (string). Confirmation of 30-day continuous operation.
* *Effect*: Unlocks **Tranche 3 (30%)**, marks problem permanently solved, and returns the official **MCA Section 135 CSR-1 Impact Certificate**.
* Frontend should display a **"Download MCA Section 135 CSR Certificate"** button!

---

## 🎨 3. UI Component Templates for Frontend Developers

### Component 1: 4-Tier Complexity & Guardrail Badge
Use this in `HeiProblemReview.jsx`:

```jsx
export function ComplexityBadge({ tier, minYear, userYear }) {
  const isBlocked = userYear && userYear < minYear;
  
  const colors = {
    1: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
    2: "bg-blue-500/10 text-blue-400 border-blue-500/30",
    3: "bg-amber-500/10 text-amber-400 border-amber-500/30",
    4: "bg-purple-500/10 text-purple-400 border-purple-500/30"
  };

  return (
    <div className="flex flex-col gap-1">
      <span className={`px-2.5 py-1 text-xs font-mono rounded border ${colors[tier] || colors[2]}`}>
        Tier {tier}: {tier === 1 ? "Foundational" : tier === 4 ? "Advanced R&D" : "Applied Engineering"}
      </span>
      {isBlocked && (
        <span className="text-[10px] text-red-400 bg-red-500/10 px-2 py-0.5 rounded border border-red-500/20">
          ⚠️ 1st-Year Guardrail: Requires Year {minYear}+ cohort
        </span>
      )}
    </div>
  );
}
```

---

### Component 2: 3-Tranche Milestone Escrow Tracker
Use this in `ProblemDetail.jsx` and `IndustryBrowse.jsx`:

```jsx
export function EscrowMilestoneTracker({ milestones, activeTranche }) {
  return (
    <div className="p-4 bg-[#16262A] border border-[#1D3238] rounded-xl space-y-3">
      <h4 className="text-xs font-mono text-[#2F9E8F] uppercase">Milestone Escrow Pledge (CCL v1.0)</h4>
      <div className="grid grid-cols-3 gap-2 text-xs">
        {/* Tranche 1 */}
        <div className="p-3 bg-[#0F1B1E] rounded-lg border border-emerald-500/30">
          <span className="text-emerald-400 font-bold">Tranche 1 (30%)</span>
          <p className="text-[#9BA8A6] text-[11px] mt-1">Lab Validation & BoM</p>
          <span className="text-emerald-400 text-[10px] uppercase font-mono">✅ Disbursed</span>
        </div>

        {/* Tranche 2 */}
        <div className={`p-3 bg-[#0F1B1E] rounded-lg border ${activeTranche >= 2 ? "border-blue-500/30 text-blue-400" : "border-[#1D3238] text-[#9BA8A6]"}`}>
          <span className="font-bold">Tranche 2 (40%)</span>
          <p className="text-[11px] mt-1">Municipal Field Pilot</p>
          <span className="text-[10px] uppercase font-mono">
            {activeTranche >= 2 ? "🚀 Active" : "🔒 Locked (ULB Site Permit Req.)"}
          </span>
        </div>

        {/* Tranche 3 */}
        <div className={`p-3 bg-[#0F1B1E] rounded-lg border ${activeTranche >= 3 ? "border-purple-500/30 text-purple-400" : "border-[#1D3238] text-[#9BA8A6]"}`}>
          <span className="font-bold">Tranche 3 (30%)</span>
          <p className="text-[11px] mt-1">Final Handover</p>
          <span className="text-[10px] uppercase font-mono">
            {activeTranche >= 3 ? "📜 Certified" : "🔒 Locked (30d Pilot Req.)"}
          </span>
        </div>
      </div>
    </div>
  );
}
```

---

## 🚀 4. Summary Action Items for Frontend Team

1. **In `SubmitProblem.jsx`**:
   - Ensure `lat`, `lng`, and `address` are included in `location`.
   - Call the unified endpoint via backend (`POST /api/problems`).
2. **In `HeiProblemReview.jsx`**:
   - Add the **"Download Engineering Dossier (PDF)"** button pointing to `/academic/chronic-problems/:id/dossier-pdf`.
   - Add the **"Submit Capstone Prototype"** modal collecting `student_year_level`, `trl_level`, and `bill_of_materials`.
3. **In `IndustryBrowse.jsx`**:
   - Add the **"Pledge CSR Funds"** modal with the 3-Tranche Escrow checkboxes and sponsor selection.
4. **In `ProblemDetail.jsx`**:
   - Add the role-based action buttons:
     - Government role: **"Site Clearance Gatekeeper"** button.
     - Corporate Auditor role: **"Verify Handover & Generate CSR Certificate"** button.
