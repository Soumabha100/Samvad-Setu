"""
=============================================================================
Samvad-Setu: Autonomous Multi-Modal Civic AI-Agent Orchestrator
Module: ai-engine/ai-agent/agent.py
=============================================================================
Description:
    Autonomous, zero-training AI-Agent that unifies Part A (Indic NLP, Department
    Triage, SLA Target) and Part B (YOLO11 Vision, Whisper Voice, Spatial Dedup,
    HEI Problem Bank, AICTE Syllabus Matcher, Gemini Dossier, CSR Escrow Engine,
    and MCA Section 135 CSR Certification) into a single, cohesive workflow.

    The backend developer only needs to connect ONE endpoint:
        POST /agent/automate
=============================================================================
"""

import sys
import uuid
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Path setup for local module resolution across part-a and part-b
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
PART_A_DIR = ROOT_DIR / "part-a"
PART_B_DIR = ROOT_DIR / "part-b"
IMAGE_DIR = PART_B_DIR / "image"
VOICE_DIR = PART_B_DIR / "voice"
ACADEMIC_DIR = PART_B_DIR / "academic"
CORPORATE_DIR = PART_B_DIR / "corporate"

for p in [str(BASE_DIR), str(ROOT_DIR), str(PART_A_DIR), str(PART_B_DIR), str(IMAGE_DIR), str(VOICE_DIR), str(ACADEMIC_DIR), str(CORPORATE_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

import os

# Automatically load the single master environment configuration from ai-engine/.env
MASTER_ENV_FILE = ROOT_DIR / ".env"
if MASTER_ENV_FILE.exists():
    try:
        with open(MASTER_ENV_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    k = k.strip()
                    v = v.strip().strip("'\"")
                    if k and k not in os.environ:
                        os.environ[k] = v
    except Exception:
        pass

logger = logging.getLogger("SamvadSetuAgent")
logging.basicConfig(level=logging.INFO)

# -----------------------------------------------------------------------------
# Import Existing Part A & Part B Modules (Strictly Zero Retraining)
# -----------------------------------------------------------------------------

# Part A: Indic NLP & SLA Classifier
try:
    # pyrefly: ignore [missing-import]
    from predict import ComplaintClassifier
    part_a_classifier = ComplaintClassifier()
    logger.info("Agent: Part A ComplaintClassifier successfully loaded.")
except Exception as e:
    part_a_classifier = None
    logger.warning(f"Agent: Part A ComplaintClassifier fallback mode: {e}")

# Part B: Deduplication & Spatial Fusion
# pyrefly: ignore [missing-import]
from dedup import (
    calculate_incident_similarity,
    merge_reports,
    haversine_distance,
    DUPLICATE_THRESHOLD
)

# Part B: Academic Escalation, Syllabus Matching & Gemini Dossier
# pyrefly: ignore [missing-import]
from academic import (
    evaluate_problem_complexity,
    SyllabusMatcher,
    SyllabusCurriculum,
    SAMPLE_SYLLABI,
    register_chronic_problem_statement,
    generate_hei_problem_dossier_pdf,
    CHRONIC_PROBLEMS_POOL,
    search_institutions
)

# Part B: Corporate Showcase, AI CSR Matcher, Escrow & MCA 135 Certificate
# pyrefly: ignore [missing-import]
from corporate import (
    register_prototype_submission,
    list_prototypes,
    get_prototype_by_id,
    create_sponsorship_pledge,
    approve_milestone,
    match_sponsors_for_prototype,
    generate_csr_impact_certificate,
    PROTOTYPES_STORE,
    SPONSORSHIPS_STORE
)

# Initialize AICTE Syllabus matchers
ACADEMIC_MATCHERS = {
    key: SyllabusMatcher(SyllabusCurriculum.from_dict(curriculum))
    for key, curriculum in SAMPLE_SYLLABI.items()
}


# =============================================================================
# Master In-Memory State Store for Agent Orchestration
# =============================================================================
MASTER_AGENT_STORE: Dict[str, Dict[str, Any]] = {}


class CivicOrchestratorAgent:
    """
    Autonomous Agent orchestrating the full civic innovation lifecycle:
    1. Multimodal Citizen Grievance Submission (YOLO11, Whisper, Part A NLP)
    2. Smart Deduplication & Spatial Fusion (<=150m + Cosine Similarity)
    3. Phase 1: Municipal Government SLA Attempt (7-14 days window)
    4. Escalation Trigger: Chronic failure / SLA breach -> HEI Problem Bank
    5. Academic Routing: 4-Tier Complexity + 1st-Year Safety + AICTE Matcher + Gemini PDF Dossier
    6. HEI Capstone Prototype Submission (TRL 1-7, BoM)
    7. Corporate Showcase & AI CSR Sponsor Matching (MCA Schedule VII)
    8. Tripartite Governance & 3-Tranche Milestone Escrow (CCL v1.0)
    9. Municipal Site Clearance Gatekeeper (ULB signoff for Tranche 2)
    10. Final Civic Handover & MCA Section 135 CSR Impact Certification
    """

    def __init__(self):
        self.store = MASTER_AGENT_STORE

    # -------------------------------------------------------------------------
    # 1. Citizen Grievance Submission & Multimodal Ingestion + Spatial Fusion
    # -------------------------------------------------------------------------
    def ingest_citizen_submission(
        self,
        text: Optional[str] = None,
        category: Optional[str] = None,
        severity: Optional[str] = None,
        location: Optional[Dict[str, Any]] = None,
        image_path: Optional[str] = None,
        audio_path: Optional[str] = None,
        citizen_name: Optional[str] = None,
        yolo_detections: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Step 1 & Step 2: Ingests grievance, runs Part A NLP / Part B Vision if needed,
        and deduplicates against active tickets within <= 150m.
        """
        text = text or ""
        citizen_name = citizen_name or "Anonymous Citizen"
        location = location or {"lat": 28.6139, "lng": 77.2090, "address": "New Delhi Central"}

        # 1. Indic NLP Triage (Part A)
        detected_category = category
        detected_department = "Public Works Department"
        sla_hours = 72

        if part_a_classifier and text.strip():
            try:
                res = part_a_classifier.predict(text)
                if not detected_category or detected_category.lower() in ["general", "other", ""]:
                    detected_category = res.get("category", "road_damage")
                detected_department = res.get("department", "Public Works Department")
                sla_hours = res.get("sla_hours", 72)
                if not severity:
                    severity = res.get("severity", "medium")
            except Exception as e:
                logger.warning(f"Part A inference warning: {e}")

        # Fallbacks if text was brief or image-driven
        if not detected_category:
            if yolo_detections:
                first_label = yolo_detections[0].get("class_name", "pothole")
                detected_category = "road_damage" if "pothole" in first_label else "garbage"
            else:
                detected_category = "road_damage"

        severity = (severity or "medium").lower()

        incoming_report = {
            "id": f"rep_{uuid.uuid4().hex[:8]}",
            "citizen_name": citizen_name,
            "text": text,
            "category": detected_category,
            "department": detected_department,
            "severity": severity,
            "location": location,
            "image_path": image_path,
            "audio_path": audio_path,
            "timestamp": datetime.now().isoformat()
        }

        # 2. Smart Deduplication & Spatial Fusion (<= 150m + Text/Vision Cosine Sim)
        matched_ticket_id = None
        highest_sim = 0.0

        for t_id, ticket in self.store.items():
            sim_res = calculate_incident_similarity(incoming_report, ticket)
            if sim_res.get("is_duplicate") and sim_res.get("composite_score", 0) > highest_sim:
                highest_sim = sim_res["composite_score"]
                matched_ticket_id = t_id

        if matched_ticket_id:
            # Fuse into existing Master Ticket
            master = self.store[matched_ticket_id]
            merge_reports(master, incoming_report)
            master["updated_at"] = datetime.now().isoformat()
            
            # Check if recurring volume reaches chronic threshold (>=3 reports)
            if master["citizen_count"] >= 3 and master["stage"] == "PHASE_1_MUNICIPAL_ATTEMPT":
                master["escalation_recommended"] = True
                master["escalation_reason"] = f"Chronic community reports: {master['citizen_count']} citizens independently reported within <=150m."

            return {
                "status": "fused_to_master_ticket",
                "action_taken": "SPATIAL_FUSION",
                "master_ticket_id": matched_ticket_id,
                "citizen_count": master["citizen_count"],
                "severity": master["severity"],
                "sla_hours": master["sla_hours"],
                "composite_similarity": highest_sim,
                "ticket": master
            }

        # Create New Master Ticket
        ticket_id = f"TICKET-{uuid.uuid4().hex[:6].upper()}"
        new_ticket = {
            "ticket_id": ticket_id,
            "master_ticket_id": ticket_id,
            "stage": "PHASE_1_MUNICIPAL_ATTEMPT",
            "title": f"Incident: {detected_category.replace('_', ' ').title()} at {location.get('address', 'Location')}",
            "description": text,
            "category": detected_category,
            "department": detected_department,
            "severity": severity,
            "sla_hours": sla_hours,
            "sla_window_days": 14,
            "sla_deadline": (datetime.now()).isoformat(),
            "location": location,
            "citizen_count": 1,
            "evidence_gallery": [image_path] if image_path else [],
            "audio_gallery": [audio_path] if audio_path else [],
            "citizen_reports": [incoming_report],
            "escalation_recommended": False,
            "escalation_data": None,
            "prototype_data": None,
            "sponsorship_data": None,
            "csr_certificate": None,
            "audit_trail": [
                {
                    "timestamp": datetime.now().isoformat(),
                    "actor": "CITIZEN",
                    "event": "GRIEVANCE_REGISTERED",
                    "details": f"Registered by {citizen_name}. Triaged to {detected_department} with {severity.upper()} severity."
                }
            ],
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

        self.store[ticket_id] = new_ticket
        return {
            "status": "master_ticket_created",
            "action_taken": "INITIAL_TRIAGE",
            "ticket_id": ticket_id,
            "stage": "PHASE_1_MUNICIPAL_ATTEMPT",
            "ticket": new_ticket
        }

    # -------------------------------------------------------------------------
    # 2. Phase 1: Municipal Government Attempt & Escalation Trigger
    # -------------------------------------------------------------------------
    def update_government_attempt(
        self,
        ticket_id: str,
        attempt_status: str,  # 'RESOLVED' | 'FAILED' | 'CHRONIC_RECURRENCE' | 'SLA_BREACHED'
        officer_name: Optional[str] = None,
        notes: Optional[str] = None,
        generate_dossier_now: bool = True
    ) -> Dict[str, Any]:
        """
        Step 3 & Step 4: Handles Municipal resolution outcome.
        - If RESOLVED -> Case Closed.
        - If FAILED or CHRONIC -> Autonomously escalates to HEI Problem Statement Bank,
          scores 4-tier complexity, verifies 1st-year safety, matches AICTE syllabus,
          and generates publication-grade Gemini ReportLab PDF Dossier.
        """
        ticket = self.store.get(ticket_id)
        if not ticket:
            return {"status": "error", "message": f"Ticket {ticket_id} not found."}

        officer_name = officer_name or "Ward Junior Engineer"
        notes = notes or "Surface patch applied but water seepage caused recurring breakdown."

        # Branch A: Problem Solved
        if attempt_status.upper() == "RESOLVED":
            ticket["stage"] = "CASE_CLOSED"
            ticket["audit_trail"].append({
                "timestamp": datetime.now().isoformat(),
                "actor": "MUNICIPAL_ULB",
                "event": "CASE_CLOSED_MUNICIPAL_FIX",
                "details": f"Standard municipal fix completed by {officer_name}. Notes: {notes}"
            })
            ticket["updated_at"] = datetime.now().isoformat()
            return {
                "status": "case_closed",
                "ticket_id": ticket_id,
                "stage": "CASE_CLOSED",
                "message": "Problem successfully remediated by municipal authority.",
                "ticket": ticket
            }

        # Branch B: Escalation Engine Triggered (Part B Academic)
        ticket["stage"] = "ESCALATED_TO_HEI"
        ticket["audit_trail"].append({
            "timestamp": datetime.now().isoformat(),
            "actor": "ESCALATION_ENGINE",
            "event": "ESCALATED_TO_HEI_BANK",
            "details": f"Municipal remediation failed / chronic recurrence detected ({attempt_status}). Escalating to HEI Problem Bank."
        })

        # Run 4-Tier Complexity Scorer + AICTE Syllabus Matching
        comp_obj = evaluate_problem_complexity(ticket["description"] or ticket["title"], ticket["category"])
        comp_dict = comp_obj.to_dict() if hasattr(comp_obj, "to_dict") else comp_obj
        
        # Match against AICTE Syllabi (Civil, CSE, Environmental)
        matched_syllabi = {}
        primary_academic_routing = None
        for code, matcher in ACADEMIC_MATCHERS.items():
            try:
                res = matcher.match_problem(
                    problem_text=ticket["description"] or ticket["title"],
                    category=ticket.get("category", ""),
                    department_hint=ticket.get("department", "")
                )
                matched_syllabi[code] = {
                    "department": res.get("department", code),
                    "best_matched_subject": res.get("best_matched_subject"),
                    "ranked_candidates": res.get("ranked_candidates", [])
                }
                if not primary_academic_routing:
                    primary_academic_routing = res
            except Exception as e:
                logger.warning(f"Syllabus match warning for {code}: {e}")

        # Register in Chronic Problem Bank
        chronic_reg = register_chronic_problem_statement(
            problem_id=ticket_id,
            title=ticket["title"],
            description=ticket["description"] or f"Recurrent failure in {ticket['category']}",
            category=ticket["category"],
            department=ticket["department"],
            location=ticket["location"],
            recurrence_count=max(3, ticket.get("citizen_count", 1)),
            failed_resolution_attempts=2,
            authority_notes=notes
        )

        chronic_entry = chronic_reg.get("chronic_problem", {})
        escalation_id = chronic_entry.get("escalation_id", f"ESC-{ticket_id}")
        dossier_pdf_path = chronic_entry.get("dossier_pdf_path")

        # Fallback to direct dossier generator if not already rendered
        if not dossier_pdf_path and generate_dossier_now:
            try:
                problem_payload = {
                    "escalation_id": escalation_id,
                    "title": ticket["title"],
                    "description": ticket["description"],
                    "category": ticket["category"],
                    "municipal_department": ticket["department"],
                    "location": ticket["location"],
                    "chronic_metrics": {
                        "recurrence_count": ticket.get("citizen_count", 3),
                        "recurrence_period_days": 30,
                        "failed_attempts": 2,
                        "authority_notes": notes
                    },
                    "ai_academic_routing": primary_academic_routing or {
                        "best_matched_subject": {"subject_name": "Transportation & Pavement Engineering", "subject_code": "CE-401"},
                        "problem_complexity": comp_dict
                    }
                }
                dossier_pdf_path = generate_hei_problem_dossier_pdf(problem_payload)
            except Exception as e:
                logger.error(f"Error generating PDF dossier: {e}")

        escalation_payload = {
            "escalation_id": escalation_id,
            "chronic_problem_statement": chronic_entry,
            "complexity_scoring": comp_dict,
            "safety_guardrail": {
                "tier": comp_dict.get("tier"),
                "is_first_year_eligible": comp_dict.get("tier") in [1, "Tier 1: Foundational/Basic"],
                "policy_note": "1st-year junior students are restricted to Tier 1 tasks. Higher tiers require 2nd-4th year capstone cohorts."
            },
            "aicte_syllabus_alignment": matched_syllabi,
            "dossier_pdf_path": str(dossier_pdf_path) if dossier_pdf_path else None
        }

        ticket["escalation_data"] = escalation_payload
        ticket["updated_at"] = datetime.now().isoformat()

        return {
            "status": "escalated_to_hei",
            "action_taken": "HEI_PROBLEM_BANK_ROUTED",
            "ticket_id": ticket_id,
            "escalation_id": escalation_id,
            "stage": "ESCALATED_TO_HEI",
            "dossier_pdf_path": str(dossier_pdf_path) if dossier_pdf_path else None,
            "escalation_summary": escalation_payload,
            "ticket": ticket
        }

    # -------------------------------------------------------------------------
    # 3. HEI Student Capstone Prototype Submission
    # -------------------------------------------------------------------------
    def submit_hei_prototype(
        self,
        ticket_id: str,
        prototype_title: str,
        team_name: str,
        institution_name: str,
        faculty_mentor: str,
        student_year_level: int,
        trl_level: int,
        bill_of_materials: List[Dict[str, Any]],
        total_funding_required_inr: float,
        schedule_vii_categories: Optional[List[str]] = None,
        technical_abstract: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Step 5 & Step 6: HEI student capstone team submits their working prototype.
        Verifies 1st-year safety guardrail, registers in Corporate Showcase,
        and matches corporate sponsors via MCA Schedule VII taxonomy.
        """
        ticket = self.store.get(ticket_id)
        if not ticket:
            return {"status": "error", "message": f"Ticket {ticket_id} not found."}

        # 1st-Year Safety Guardrail Check
        comp = ticket.get("escalation_data", {}).get("complexity_scoring", {})
        tier_num = comp.get("tier", 2)
        if isinstance(tier_num, str):
            tier_num = 1 if "Tier 1" in tier_num else 3

        if student_year_level == 1 and tier_num > 1:
            return {
                "status": "safety_guardrail_blocked",
                "message": (
                    f"1st-Year Safety Guardrail Activated: Student team year level ({student_year_level}) "
                    f"is not authorized for high-complexity Tier {tier_num} problem statements. "
                    f"Requires 2nd-4th year Capstone cohort with certified faculty mentor."
                )
            }

        schedule_vii = schedule_vii_categories or ["item_iv", "item_ii"]  # Environmental sustainability & Education
        proto_reg = register_prototype_submission(
            escalation_id=ticket.get("escalation_data", {}).get("escalation_id", f"ESC-{ticket_id}"),
            team_name=team_name,
            institution_name=institution_name,
            faculty_mentor=faculty_mentor,
            prototype_title=prototype_title,
            executive_summary=technical_abstract or f"Applied engineering prototype to remediate {ticket['title']}",
            technical_approach=f"Engineered working prototype addressing {ticket.get('category', 'civic infrastructure')} failure.",
            trl_level=trl_level,
            bill_of_materials=bill_of_materials,
            total_funding_required_inr=total_funding_required_inr,
            category=ticket.get("category", "road_damage")
        )

        proto_id = proto_reg.get("prototype", {}).get("prototype_id", f"PROTO-{uuid.uuid4().hex[:6].upper()}")

        # AI CSR Sponsor Match
        sponsor_matches = match_sponsors_for_prototype(proto_id)

        prototype_payload = {
            "prototype_id": proto_id,
            "prototype_details": proto_reg.get("prototype"),
            "matched_corporate_sponsors": sponsor_matches.get("top_matches", []),
            "showcase_status": "PUBLISHED_IN_CORPORATE_PORTAL"
        }

        ticket["stage"] = "PROTOTYPE_SUBMITTED_SHOWCASE"
        ticket["prototype_data"] = prototype_payload
        ticket["audit_trail"].append({
            "timestamp": datetime.now().isoformat(),
            "actor": "HEI_STUDENTS",
            "event": "PROTOTYPE_REGISTERED_IN_SHOWCASE",
            "details": f"Prototype '{prototype_title}' (TRL {trl_level}) submitted by {team_name} ({institution_name})."
        })
        ticket["updated_at"] = datetime.now().isoformat()

        return {
            "status": "prototype_registered",
            "prototype_id": proto_id,
            "stage": "PROTOTYPE_SUBMITTED_SHOWCASE",
            "matched_sponsors": sponsor_matches.get("top_matches", []),
            "ticket": ticket
        }

    # -------------------------------------------------------------------------
    # 4. Corporate CSR Pledge & Tripartite Governance Framework
    # -------------------------------------------------------------------------
    def pledge_corporate_sponsorship(
        self,
        ticket_id: str,
        sponsor_id: str,
        pledged_amount_inr: float,
        representative_name: str,
        contact_email: str
    ) -> Dict[str, Any]:
        """
        Step 7: Corporate partner pledges CSR funding with Tripartite Governance:
        - Grants Civic Commons License (CCL v1.0).
        - Establishes 3-Tranche Milestone Escrow (30% Lab -> 40% Pilot -> 30% Handover).
        - Releases Tranche 1 (30%) immediately for lab prototype build.
        """
        ticket = self.store.get(ticket_id)
        if not ticket:
            return {"status": "error", "message": f"Ticket {ticket_id} not found."}

        proto_data = ticket.get("prototype_data", {})
        proto_id = proto_data.get("prototype_id")
        if not proto_id:
            # Fallback to first in PROTOTYPES_STORE
            proto_id = next(iter(PROTOTYPES_STORE.keys()), "PROTO-TERRAFIX-01")

        pledge_res = create_sponsorship_pledge(
            prototype_id=proto_id,
            sponsor_id=sponsor_id,
            pledged_amount_inr=pledged_amount_inr,
            corporate_representative_name=representative_name,
            corporate_contact_email=contact_email,
            escrow_terms_accepted=True,
            civic_commons_license_accepted=True
        )

        if pledge_res.get("status") == "error":
            return pledge_res

        sponsorship = pledge_res["sponsorship"]
        ticket["stage"] = "CSR_PLEDGED_TRANCHE_1_RELEASED"
        ticket["sponsorship_data"] = sponsorship
        ticket["audit_trail"].append({
            "timestamp": datetime.now().isoformat(),
            "actor": "CORPORATE_SPONSOR",
            "event": "CSR_PLEDGE_AND_ESCROW_INITIATED",
            "details": f"Pledged INR {pledged_amount_inr:,.2f} by {sponsorship['company_name']}. Tranche 1 (30%) disbursed to HEI Lab Escrow."
        })
        ticket["updated_at"] = datetime.now().isoformat()

        return {
            "status": "pledge_recorded",
            "stage": "CSR_PLEDGED_TRANCHE_1_RELEASED",
            "sponsorship_id": sponsorship["sponsorship_id"],
            "tranche_1_disbursed_inr": sponsorship["total_disbursed_inr"],
            "escrow_balance_inr": sponsorship["escrow_balance_inr"],
            "intellectual_property": sponsorship["intellectual_property_framework"],
            "ticket": ticket
        }

    # -------------------------------------------------------------------------
    # 5. Municipal Site Clearance Gatekeeper (Unlocks Tranche 2)
    # -------------------------------------------------------------------------
    def municipal_gatekeeper_clearance(
        self,
        ticket_id: str,
        officer_name: str,
        site_inspection_notes: str
    ) -> Dict[str, Any]:
        """
        Step 8: ULB Municipal Engineer inspects site and grants permit.
        Unlocks Tranche 2 (40%) Milestone Escrow for Real-World Field Pilot.
        """
        ticket = self.store.get(ticket_id)
        if not ticket:
            return {"status": "error", "message": f"Ticket {ticket_id} not found."}

        s_data = ticket.get("sponsorship_data") or {}
        s_id = s_data.get("sponsorship_id")
        if not s_id:
            return {
                "status": "error",
                "message": "No active sponsorship escrow found on this ticket. You must first execute action 'CORPORATE_PLEDGE' to establish the 3-tranche milestone escrow before municipal site clearance can unlock Tranche 2."
            }

        approval_res = approve_milestone(
            sponsorship_id=s_id,
            tranche_index=2,
            approver_role="municipal_officer",
            approver_name=officer_name,
            verification_notes=site_inspection_notes
        )

        if approval_res.get("status") in ["error", "gatekeeper_blocked"]:
            return approval_res

        ticket["stage"] = "FIELD_PILOT_DEPLOYMENT_ACTIVE"
        ticket["sponsorship_data"] = approval_res["sponsorship"]
        ticket["audit_trail"].append({
            "timestamp": datetime.now().isoformat(),
            "actor": "MUNICIPAL_GATEKEEPER",
            "event": "SITE_CLEARANCE_AND_TRANCHE_2_RELEASED",
            "details": f"Site permit granted by {officer_name}. Tranche 2 released. Field Pilot Active."
        })
        ticket["updated_at"] = datetime.now().isoformat()

        return {
            "status": "site_cleared_tranche_2_released",
            "stage": "FIELD_PILOT_DEPLOYMENT_ACTIVE",
            "amount_disbursed_inr": approval_res["amount_disbursed_inr"],
            "remaining_escrow_inr": approval_res["remaining_escrow_balance_inr"],
            "ticket": ticket
        }

    # -------------------------------------------------------------------------
    # 6. Final Civic Handover & MCA Section 135 CSR Impact Certification
    # -------------------------------------------------------------------------
    def civic_handover_and_certification(
        self,
        ticket_id: str,
        corporate_auditor_name: str,
        handover_notes: str
    ) -> Dict[str, Any]:
        """
        Step 9 & Step 10: Releases Tranche 3 (30%), marks civic problem permanently fixed,
        and generates official MCA Section 135 CSR Impact Audit Certificate.
        """
        ticket = self.store.get(ticket_id)
        if not ticket:
            return {"status": "error", "message": f"Ticket {ticket_id} not found."}

        s_data = ticket.get("sponsorship_data") or {}
        s_id = s_data.get("sponsorship_id")
        if not s_id:
            return {
                "status": "error",
                "message": "No active sponsorship escrow found on this ticket. A corporate partner must pledge funding via 'CORPORATE_PLEDGE' before final handover certification."
            }

        # Disburse final Tranche 3
        approval_res = approve_milestone(
            sponsorship_id=s_id,
            tranche_index=3,
            approver_role="corporate_auditor",
            approver_name=corporate_auditor_name,
            verification_notes=handover_notes
        )

        # Generate official MCA Section 135 CSR Certificate
        cert_res = generate_csr_impact_certificate(s_id)

        ticket["stage"] = "PERMANENT_FIX_AND_CSR_CERTIFIED"
        ticket["sponsorship_data"] = approval_res.get("sponsorship", s_data)
        ticket["csr_certificate"] = cert_res.get("certificate")
        ticket["audit_trail"].append({
            "timestamp": datetime.now().isoformat(),
            "actor": "CSR_AUDITOR_COUNCIL",
            "event": "FINAL_HANDOVER_AND_CERTIFICATE_ISSUED",
            "details": f"Tranche 3 disbursed. Civic Handover complete. MCA Section 135 Certificate: {cert_res.get('certificate_id')}."
        })
        ticket["updated_at"] = datetime.now().isoformat()

        return {
            "status": "permanent_fix_completed",
            "stage": "PERMANENT_FIX_AND_CSR_CERTIFIED",
            "certificate_id": cert_res.get("certificate_id"),
            "certificate": cert_res.get("certificate"),
            "final_ticket_state": ticket
        }

    # -------------------------------------------------------------------------
    # Master Dispatcher: Single Unified Interface for Backend Developer
    # -------------------------------------------------------------------------
    def dispatch_agent_action(self, action: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Single entry-point dispatcher covering the entire 10-step lifecycle.
        Supported actions:
        - 'CITIZEN_SUBMISSION'
        - 'GOVERNMENT_STATUS_UPDATE'
        - 'HEI_PROTOTYPE_SUBMIT'
        - 'CORPORATE_PLEDGE'
        - 'MUNICIPAL_SITE_CLEARANCE'
        - 'CIVIC_HANDOVER_AND_CERTIFICATION'
        """
        act = action.upper().strip()

        if act in ["CITIZEN_SUBMISSION", "GRIEVANCE_SUBMISSION", "SUBMIT"]:
            return self.ingest_citizen_submission(
                text=payload.get("text") or payload.get("description"),
                category=payload.get("category"),
                severity=payload.get("severity"),
                location=payload.get("location"),
                image_path=payload.get("image_path"),
                audio_path=payload.get("audio_path"),
                citizen_name=payload.get("citizen_name"),
                yolo_detections=payload.get("yolo_detections")
            )

        elif act in ["GOVERNMENT_STATUS_UPDATE", "MUNICIPAL_ATTEMPT", "GOV_UPDATE"]:
            return self.update_government_attempt(
                ticket_id=payload.get("ticket_id", ""),
                attempt_status=payload.get("attempt_status") or payload.get("status", "FAILED"),
                officer_name=payload.get("officer_name"),
                notes=payload.get("notes"),
                generate_dossier_now=payload.get("generate_dossier", True)
            )

        elif act in ["HEI_PROTOTYPE_SUBMIT", "PROTOTYPE_SUBMISSION", "HEI_SUBMIT"]:
            return self.submit_hei_prototype(
                ticket_id=payload.get("ticket_id", ""),
                prototype_title=payload.get("prototype_title", "Eco-Drainage Modular Trap"),
                team_name=payload.get("team_name", "IIT Delhi Civil Innovation Lab"),
                institution_name=payload.get("institution_name", "IIT Delhi"),
                faculty_mentor=payload.get("faculty_mentor", "Prof. R. Sengupta"),
                student_year_level=int(payload.get("student_year_level", 4)),
                trl_level=int(payload.get("trl_level", 6)),
                bill_of_materials=payload.get("bill_of_materials", [
                    {"component": "Permeable Geotextile", "estimated_cost_inr": 45000},
                    {"component": "IoT Pressure Sensor", "estimated_cost_inr": 25000}
                ]),
                total_funding_required_inr=float(payload.get("total_funding_required_inr", 250000.0)),
                schedule_vii_categories=payload.get("schedule_vii_categories"),
                technical_abstract=payload.get("technical_abstract")
            )

        elif act in ["CORPORATE_PLEDGE", "CSR_PLEDGE", "SPONSOR_PLEDGE"]:
            return self.pledge_corporate_sponsorship(
                ticket_id=payload.get("ticket_id", ""),
                sponsor_id=payload.get("sponsor_id", "CORP-TATA-01"),
                pledged_amount_inr=float(payload.get("pledged_amount_inr", 250000.0)),
                representative_name=payload.get("representative_name", "Dr. Ananya Sharma"),
                contact_email=payload.get("contact_email", "csr@tatatrusts.org")
            )

        elif act in ["MUNICIPAL_SITE_CLEARANCE", "CLEAR_SITE", "SITE_PERMIT"]:
            return self.municipal_gatekeeper_clearance(
                ticket_id=payload.get("ticket_id", ""),
                officer_name=payload.get("officer_name", "Er. Rajesh Mehra, Executive Engineer"),
                site_inspection_notes=payload.get("site_inspection_notes", "Site surveyed. Safe for public pilot installation.")
            )

        elif act in ["CIVIC_HANDOVER_AND_CERTIFICATION", "FINAL_HANDOVER", "CSR_CERTIFY"]:
            return self.civic_handover_and_certification(
                ticket_id=payload.get("ticket_id", ""),
                corporate_auditor_name=payload.get("corporate_auditor_name", "KPMG / PwC Statutory Auditor"),
                handover_notes=payload.get("handover_notes", "Prototype deployed and verified in public service for 30 consecutive days.")
            )

        else:
            return {
                "status": "error",
                "message": f"Unknown agent action '{action}'. Supported actions: CITIZEN_SUBMISSION, GOVERNMENT_STATUS_UPDATE, HEI_PROTOTYPE_SUBMIT, CORPORATE_PLEDGE, MUNICIPAL_SITE_CLEARANCE, CIVIC_HANDOVER_AND_CERTIFICATION."
            }


# Singleton accessor
_GLOBAL_AGENT = None

def get_civic_orchestrator() -> CivicOrchestratorAgent:
    global _GLOBAL_AGENT
    if _GLOBAL_AGENT is None:
        _GLOBAL_AGENT = CivicOrchestratorAgent()
    return _GLOBAL_AGENT
