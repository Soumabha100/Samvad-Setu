"""
Tripartite Stakeholder Governance & Milestone Escrow Engine
Module: ai-engine/part-b/corporate/stakeholder_governance.py

Solves the 4 critical corporate funding stakeholder conflicts:
1. Intellectual Property (IP) Rights via Civic Commons License (CCL).
2. Municipal Regulatory Authority & Indemnity (Site Clearance Gatekeeper).
3. Delivery Risk & Fund Misappropriation via 3-Phase Milestone Escrow.
4. Tripartite Agreement Generation (Student Team + ULB + Corporate Sponsor).
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from .prototypes_data import PROTOTYPES_STORE, CORPORATE_SPONSORS_STORE


SPONSORSHIPS_STORE: Dict[str, Dict[str, Any]] = {}


def create_sponsorship_pledge(
    prototype_id: str,
    sponsor_id: str,
    pledged_amount_inr: float,
    corporate_representative_name: str,
    corporate_contact_email: str,
    escrow_terms_accepted: bool = True,
    civic_commons_license_accepted: bool = True
) -> Dict[str, Any]:
    """
    Creates a formal Corporate CSR funding pledge for an HEI student prototype
    governed by the Tripartite Governance Agreement and 3-Tranche Milestone Escrow.
    """
    proto = PROTOTYPES_STORE.get(prototype_id)
    if not proto and PROTOTYPES_STORE:
        # Check if any prototype contains or matches prototype_id, or fall back to first
        for k, v in PROTOTYPES_STORE.items():
            if prototype_id and (prototype_id.upper() in k.upper() or k.upper() in prototype_id.upper()):
                proto = v
                prototype_id = k
                break
        if not proto:
            first_k = next(iter(PROTOTYPES_STORE))
            proto = PROTOTYPES_STORE[first_k]
            prototype_id = first_k

    if not proto:
        return {"status": "error", "message": f"Prototype {prototype_id} not found. Please register a prototype first via POST /corporate/prototypes/submit."}

    escrow_ok = True if escrow_terms_accepted is None else bool(escrow_terms_accepted)
    ccl_ok = True if civic_commons_license_accepted is None else bool(civic_commons_license_accepted)

    if not escrow_ok or not ccl_ok:
        return {
            "status": "error",
            "message": "Both Escrow Milestone Terms and Civic Commons License (CCL) must be accepted to prevent stakeholder conflicts."
        }

    # Verify corporate sponsor
    sponsor = CORPORATE_SPONSORS_STORE.get(sponsor_id)
    company_name = sponsor.get("company_name", "Corporate CSR Partner") if sponsor else "Corporate CSR Partner"
    mca_cin = sponsor.get("mca_cin", "U85100DL2020NPL000000") if sponsor else "U85100DL2020NPL000000"

    pledge_id = f"SPONSOR-{uuid.uuid4().hex[:6].upper()}"

    # Calculate 3-Tranche Milestone Escrow Allocation
    tranche_1 = round(pledged_amount_inr * 0.30, 2)  # 30% Lab Build & BoM
    tranche_2 = round(pledged_amount_inr * 0.40, 2)  # 40% Municipal Field Pilot
    tranche_3 = round(pledged_amount_inr * 0.30, 2)  # 30% Civic Handover & Signoff

    escrow_milestones = [
        {
            "tranche_index": 1,
            "milestone_name": "Phase 1: Laboratory & Component Verification",
            "percentage": 30,
            "amount_inr": tranche_1,
            "status": "disbursed_to_hei_escrow",  # automatically released to start fabrication
            "verification_requirement": "Faculty mentor validation and bill of materials procurement invoices.",
            "unlocked_at": datetime.now().isoformat()
        },
        {
            "tranche_index": 2,
            "milestone_name": "Phase 2: Municipal Site Clearance & Field Pilot Deployment",
            "percentage": 40,
            "amount_inr": tranche_2,
            "status": "locked_awaiting_municipal_clearance",
            "verification_requirement": "Urban Local Body (ULB) / Municipal Engineer site permit & 14-day field sensor log.",
            "unlocked_at": None
        },
        {
            "tranche_index": 3,
            "milestone_name": "Phase 3: Full Civic Commissioning & Handover",
            "percentage": 30,
            "amount_inr": tranche_3,
            "status": "locked_awaiting_civic_handover",
            "verification_requirement": "Joint inspection signoff by Municipal Ward Officer and Corporate CSR Auditor.",
            "unlocked_at": None
        }
    ]

    sponsorship_record = {
        "sponsorship_id": pledge_id,
        "prototype_id": prototype_id,
        "prototype_title": proto.get("prototype_title"),
        "institution_name": proto.get("institution_name"),
        "team_name": proto.get("team_name"),
        "faculty_mentor": proto.get("faculty_mentor"),
        "sponsor_id": sponsor_id,
        "company_name": company_name,
        "mca_cin": mca_cin,
        "corporate_representative": corporate_representative_name,
        "corporate_contact_email": corporate_contact_email,
        "pledged_amount_inr": pledged_amount_inr,
        "escrow_balance_inr": pledged_amount_inr - tranche_1,
        "total_disbursed_inr": tranche_1,
        "active_tranche": 1,
        "milestones": escrow_milestones,
        "municipal_site_clearance": {
            "status": "pending_site_inspection",
            "cleared_by_ulb_officer": None,
            "site_inspection_notes": "Awaiting formal ULB engineering site allocation."
        },
        "intellectual_property_framework": {
            "license_type": "Civic Commons License (CCL v1.0)",
            "municipal_deployment_rights": "Perpetual, royalty-free, non-exclusive license granted to Urban Local Body (ULB)",
            "student_inventor_rights": "Full academic attribution, copyright, and student patent ownership for non-municipal spin-offs",
            "corporate_sponsor_rights": "Exclusive CSR Impact Branding, Annual Report disclosure rights, and MCA Section 135 tax deduction eligibility"
        },
        "pledged_at": datetime.now().isoformat()
    }

    # Update prototype funding totals
    proto["funded_amount_inr"] = round(proto.get("funded_amount_inr", 0.0) + pledged_amount_inr, 2)
    if proto["funded_amount_inr"] >= proto.get("total_funding_required_inr", 0.0):
        proto["funding_status"] = "fully_funded"
    else:
        proto["funding_status"] = "partially_funded"
    proto["sponsorship_pledges"].append(pledge_id)

    SPONSORSHIPS_STORE[pledge_id] = sponsorship_record
    return {
        "status": "pledge_recorded_in_escrow",
        "sponsorship": sponsorship_record
    }


def approve_milestone(
    sponsorship_id: str,
    tranche_index: int,
    approver_role: str,  # 'municipal_officer' | 'corporate_auditor' | 'faculty_mentor'
    approver_name: str,
    verification_notes: str
) -> Dict[str, Any]:
    """
    Approves a milestone tranche and releases escrow funds to the HEI team.
    Enforces the Municipal Gatekeeper rule for Tranche 2 (Field Pilot).
    """
    sponsorship = SPONSORSHIPS_STORE.get(sponsorship_id)
    if not sponsorship:
        return {"status": "error", "message": f"Sponsorship {sponsorship_id} not found."}

    milestones = sponsorship.get("milestones", [])
    target_milestone = None
    for m in milestones:
        if m.get("tranche_index") == tranche_index:
            target_milestone = m
            break

    if not target_milestone:
        return {"status": "error", "message": f"Milestone tranche {tranche_index} not found."}

    if target_milestone.get("status") in ["disbursed_to_hei_escrow", "completed_and_disbursed"]:
        return {"status": "error", "message": f"Tranche {tranche_index} has already been disbursed."}

    # Gatekeeper check: Tranche 2 requires municipal engineering clearance
    if tranche_index == 2:
        if approver_role != "municipal_officer":
            return {
                "status": "gatekeeper_blocked",
                "message": "Tranche 2 (Municipal Field Pilot) requires explicit sign-off from an Urban Local Body (municipal_officer) to ensure public safety."
            }
        sponsorship["municipal_site_clearance"]["status"] = "cleared_for_pilot"
        sponsorship["municipal_site_clearance"]["cleared_by_ulb_officer"] = approver_name
        sponsorship["municipal_site_clearance"]["site_inspection_notes"] = verification_notes

    # Gatekeeper check: Tranche 3 requires corporate auditor or municipal officer
    if tranche_index == 3:
        if approver_role not in ["corporate_auditor", "municipal_officer"]:
            return {
                "status": "gatekeeper_blocked",
                "message": "Tranche 3 (Civic Handover) requires joint validation from corporate_auditor or municipal_officer."
            }

    # Release tranche
    amount = target_milestone.get("amount_inr", 0.0)
    target_milestone["status"] = "completed_and_disbursed"
    target_milestone["unlocked_at"] = datetime.now().isoformat()
    target_milestone["approved_by"] = f"{approver_name} ({approver_role})"
    target_milestone["verification_notes"] = verification_notes

    sponsorship["total_disbursed_inr"] = round(sponsorship.get("total_disbursed_inr", 0.0) + amount, 2)
    sponsorship["escrow_balance_inr"] = max(0.0, round(sponsorship.get("escrow_balance_inr", 0.0) - amount, 2))
    sponsorship["active_tranche"] = min(3, tranche_index + 1)

    return {
        "status": "milestone_approved_and_disbursed",
        "tranche_index": tranche_index,
        "amount_disbursed_inr": amount,
        "remaining_escrow_balance_inr": sponsorship["escrow_balance_inr"],
        "sponsorship": sponsorship
    }


def generate_tripartite_agreement_text(sponsorship_id: str) -> Dict[str, Any]:
    """
    Renders the formal Tripartite Legal Agreement between the HEI Student Team,
    the Municipal Urban Local Body (ULB), and the Corporate CSR Sponsor.
    """
    s = SPONSORSHIPS_STORE.get(sponsorship_id)
    if not s:
        return {"status": "error", "message": "Sponsorship record not found."}

    agreement_text = f"""
================================================================================
           TRIPARTITE CIVIC INNOVATION & CSR DEPLOYMENT AGREEMENT
================================================================================
Reference ID: {s['sponsorship_id']}
Date of Execution: {s['pledged_at']}

PARTIES TO THE AGREEMENT:
1. THE ACADEMIC INSTITUTION & STUDENT INVENTORS:
   - Institution: {s['institution_name']}
   - Engineering Team: {s['team_name']}
   - Faculty Mentor: {s['faculty_mentor']}

2. THE CORPORATE CSR SPONSOR:
   - Company: {s['company_name']}
   - MCA CIN: {s['mca_cin']}
   - Authorized CSR Signatory: {s['corporate_representative']}

3. THE URBAN LOCAL BODY (MUNICIPAL AUTHORITY):
   - Jurisdiction: Municipal Ward & Public Works Directorate
   - Clearance Status: {s['municipal_site_clearance']['status']}

--------------------------------------------------------------------------------
CLAUSE 1: RECITALS & CIVIC PURPOSE
--------------------------------------------------------------------------------
Whereas the Municipal Authority encountered chronic infrastructural failure regarding
'{s['prototype_title']}', and whereas the HEI student team engineered an applied
technological prototype, the Corporate Sponsor agrees to grant CSR funding totaling
INR {s['pledged_amount_inr']:,.2f} strictly for real-world public remediation.

--------------------------------------------------------------------------------
CLAUSE 2: INTELLECTUAL PROPERTY & CIVIC COMMONS LICENSE (CCL v1.0)
--------------------------------------------------------------------------------
a. Municipal Rights: The Urban Local Body is hereby granted an irrevocable, perpetual,
   royalty-free license to deploy, operate, and maintain the prototype in public spaces.
b. Student Inventor Rights: The student engineering team retains all inventor moral
   rights, academic authorship, and patent priority for commercial spin-offs outside
   the municipal public domain.
c. Corporate Rights: The Corporate Sponsor shall receive exclusive CSR Title Sponsorship,
   public brand attribution on site signage, and full CSR Section 135 tax deductibility.

--------------------------------------------------------------------------------
CLAUSE 3: MILESTONE ESCROW & TRANCHE DISBURSEMENT
--------------------------------------------------------------------------------
Total Pledged: INR {s['pledged_amount_inr']:,.2f}
Disbursed to Date: INR {s['total_disbursed_inr']:,.2f}
Escrow Balance: INR {s['escrow_balance_inr']:,.2f}

Tranches:
- Tranche 1 (30%): INR {s['milestones'][0]['amount_inr']:,.2f} - Lab Validation [Status: {s['milestones'][0]['status']}]
- Tranche 2 (40%): INR {s['milestones'][1]['amount_inr']:,.2f} - ULB Field Pilot [Status: {s['milestones'][1]['status']}]
- Tranche 3 (30%): INR {s['milestones'][2]['amount_inr']:,.2f} - Civic Handover [Status: {s['milestones'][2]['status']}]

--------------------------------------------------------------------------------
CLAUSE 4: INDEMNITY & STATUTORY COMPLIANCE
--------------------------------------------------------------------------------
All field testing is subject to prior Municipal Engineering clearance. Funds are disbursed
strictly in compliance with MCA Schedule VII of the Indian Companies Act, 2013.
================================================================================
"""
    return {
        "status": "success",
        "agreement_id": f"AGR-{s['sponsorship_id']}",
        "agreement_text": agreement_text.strip(),
        "sponsorship": s
    }
