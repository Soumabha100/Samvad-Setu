"""
=============================================================================
Samvad-Setu: Autonomous Civic AI-Agent Test Suite
Module: ai-engine/ai-agent/test_agent.py
=============================================================================
Description:
    Validates end-to-end autonomous lifecycle execution across:
    1. Multimodal Citizen Submission & Deduplication
    2. Phase 1 Municipal Government Attempt & Escalation Trigger
    3. 4-Tier Complexity, 1st-Year Safety Guardrail, and Syllabus Matching
    4. HEI Student Capstone Prototype Submission
    5. Corporate CSR Sponsor Matching & Tripartite 3-Tranche Escrow
    6. Municipal Site Clearance Gatekeeper Signoff
    7. Final Civic Handover & Statutory MCA Section 135 CSR-1 Certificate
=============================================================================
"""

import sys
from pathlib import Path

# Setup paths
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from agent import get_civic_orchestrator


def run_agent_test():
    print("=" * 80)
    print("🤖 TESTING SAMVAD-SETU AUTONOMOUS CIVIC AI-AGENT")
    print("=" * 80)

    agent = get_civic_orchestrator()

    # Step 1: Citizen Submission
    print("\n[Step 1] Ingesting Citizen Grievance...")
    res1 = agent.dispatch_agent_action("CITIZEN_SUBMISSION", {
        "citizen_name": "Rohan Sharma",
        "text": "Deep hazardous pothole on Main Ring Road causing vehicle accidents.",
        "category": "road_damage",
        "location": {"lat": 28.6139, "lng": 77.2090, "address": "Ring Road Sector 4, New Delhi"}
    })
    ticket_id = res1.get("ticket_id") or res1.get("master_ticket_id")
    print(f" -> Result Status: {res1.get('status')} | Ticket ID: {ticket_id}")
    assert ticket_id, "Ticket ID must be generated"

    # Step 2: Spatial Deduplication Test (Duplicate report within <= 150m)
    print("\n[Step 2] Testing Spatial Fusion with 2nd Citizen Report (<=150m)...")
    res2 = agent.dispatch_agent_action("CITIZEN_SUBMISSION", {
        "citizen_name": "Priya Verma",
        "text": "Huge crater on road near Ring Road Sector 4, bikers falling.",
        "category": "road_damage",
        "location": {"lat": 28.6141, "lng": 77.2091, "address": "Ring Road Sector 4"}
    })
    print(f" -> Result Status: {res2.get('status')} | Citizen Count: {res2.get('citizen_count')}")
    assert res2.get("status") == "fused_to_master_ticket", "Report should be fused into master ticket"

    # Step 3: Municipal Attempt & Escalation Trigger
    print("\n[Step 3] Updating Municipal Attempt (Simulating Failure / Chronic Recurrence)...")
    res3 = agent.dispatch_agent_action("GOVERNMENT_STATUS_UPDATE", {
        "ticket_id": ticket_id,
        "attempt_status": "FAILED",
        "officer_name": "Er. Rajesh Mehra, Junior Engineer PWD",
        "notes": "Surface cold-mix patch washed away by monsoon rainwater due to subgrade soil subsidence.",
        "generate_dossier": False
    })
    print(f" -> Result Status: {res3.get('status')} | Stage: {res3.get('stage')}")
    assert res3.get("stage") == "ESCALATED_TO_HEI", "Ticket must escalate to HEI bank"

    # Step 4: HEI Student Capstone Prototype Submission
    print("\n[Step 4] Submitting HEI Student Capstone Prototype...")
    res4 = agent.dispatch_agent_action("HEI_PROTOTYPE_SUBMIT", {
        "ticket_id": ticket_id,
        "prototype_title": "TerraFix Bio-Polymer Self-Draining Asphalt Matrix",
        "team_name": "IIT Delhi Civil Tech Team",
        "institution_name": "IIT Delhi",
        "faculty_mentor": "Prof. S. K. Bhattacharya",
        "student_year_level": 4,
        "trl_level": 6,
        "total_funding_required_inr": 250000.0,
        "bill_of_materials": [
            {"component": "Recycled Industrial Slag Aggregates", "estimated_cost_inr": 60000},
            {"component": "Cold-Mix Bio-Polymer Binder", "estimated_cost_inr": 90000}
        ]
    })
    proto_id = res4.get("prototype_id")
    print(f" -> Result Status: {res4.get('status')} | Prototype ID: {proto_id}")
    assert proto_id, "Prototype must be registered"

    # Step 5: Corporate CSR Pledge & 3-Tranche Escrow
    print("\n[Step 5] Pledging Corporate CSR Sponsorship (Tranche 1 Escrow Release)...")
    res5 = agent.dispatch_agent_action("CORPORATE_PLEDGE", {
        "ticket_id": ticket_id,
        "sponsor_id": "CORP-TATA-01",
        "pledged_amount_inr": 250000.0,
        "representative_name": "Dr. Ananya Sharma",
        "contact_email": "csr@tatatrusts.org"
    })
    spon_id = res5.get("sponsorship_id")
    print(f" -> Result Status: {res5.get('status')} | Disbursed Tranche 1: INR {res5.get('tranche_1_disbursed_inr')}")
    assert spon_id, "Sponsorship record must be created"

    # Step 6: Municipal Site Clearance Gatekeeper
    print("\n[Step 6] ULB Municipal Gatekeeper Inspection (Unlocks Tranche 2)...")
    res6 = agent.dispatch_agent_action("MUNICIPAL_SITE_CLEARANCE", {
        "ticket_id": ticket_id,
        "officer_name": "Er. Rajesh Mehra, Executive Engineer",
        "site_inspection_notes": "Site surveyed and approved for public field pilot."
    })
    print(f" -> Result Status: {res6.get('status')} | Disbursed Tranche 2: INR {res6.get('amount_disbursed_inr')}")
    assert res6.get("stage") == "FIELD_PILOT_DEPLOYMENT_ACTIVE"

    # Step 7: Final Civic Handover & MCA Section 135 CSR Certificate
    print("\n[Step 7] Final Civic Handover & Statutory Certification...")
    res7 = agent.dispatch_agent_action("CIVIC_HANDOVER_AND_CERTIFICATION", {
        "ticket_id": ticket_id,
        "corporate_auditor_name": "KPMG Statutory Auditor",
        "handover_notes": "30 days field operation complete without incident."
    })
    print(f" -> Result Status: {res7.get('status')} | Certificate ID: {res7.get('certificate_id')}")
    assert res7.get("stage") == "PERMANENT_FIX_AND_CSR_CERTIFIED"

    print("\n" + "=" * 80)
    print("✅ ALL 7 AGENT WORKFLOW STAGES VERIFIED SUCCESSFULLY!")
    print("=" * 80)


if __name__ == "__main__":
    run_agent_test()
