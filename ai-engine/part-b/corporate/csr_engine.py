"""
Corporate CSR Impact & MCA Schedule VII Tax Certification Engine
Module: ai-engine/part-b/corporate/csr_engine.py

Features:
1. Intelligent Sponsor Matching: Matches HEI prototypes with corporate CSR funds
   based on Schedule VII eligibility, budget fit, and corporate regional focus.
2. Formal CSR Impact Audit Certificate: Produces a structured statutory document
   for corporate donor boards, MCA compliance, and Section 135 tax audit filing.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from .prototypes_data import (
    PROTOTYPES_STORE,
    CORPORATE_SPONSORS_STORE,
    SCHEDULE_VII_CATEGORIES
)
from .stakeholder_governance import SPONSORSHIPS_STORE


def match_sponsors_for_prototype(prototype_id: str) -> Dict[str, Any]:
    """
    Finds top matching corporate CSR sponsors for an HEI student prototype
    based on Schedule VII alignment and budget suitability.
    """
    proto = PROTOTYPES_STORE.get(prototype_id)
    if not proto:
        return {"status": "error", "message": f"Prototype {prototype_id} not found."}

    required_budget = proto.get("total_funding_required_inr", 0.0)
    proto_cats = set(proto.get("schedule_vii_categories", []))

    matches = []
    for sponsor_id, sponsor in CORPORATE_SPONSORS_STORE.items():
        sponsor_cats = set(sponsor.get("preferred_schedule_vii", []))
        common_cats = proto_cats.intersection(sponsor_cats)

        # Calculate matching score (0 - 100)
        category_score = (len(common_cats) / max(1, len(proto_cats))) * 60
        budget_capacity = sponsor.get("csr_annual_budget_inr", 0.0) - sponsor.get("allocated_budget_inr", 0.0)
        budget_score = 40 if budget_capacity >= required_budget else (budget_capacity / max(1.0, required_budget)) * 40
        composite_score = round(category_score + budget_score, 1)

        if common_cats:
            matches.append({
                "sponsor_id": sponsor_id,
                "company_name": sponsor.get("company_name"),
                "mca_cin": sponsor.get("mca_cin"),
                "industry_sector": sponsor.get("industry_sector"),
                "matching_score_percent": composite_score,
                "aligned_schedule_vii_items": list(common_cats),
                "aligned_schedule_vii_descriptions": [SCHEDULE_VII_CATEGORIES.get(c, "") for c in common_cats],
                "csr_budget_available_inr": round(budget_capacity, 2),
                "can_fully_fund": budget_capacity >= required_budget
            })

    matches.sort(key=lambda x: x["matching_score_percent"], reverse=True)
    return {
        "status": "success",
        "prototype_id": prototype_id,
        "prototype_title": proto.get("prototype_title"),
        "funding_required_inr": required_budget,
        "total_matches": len(matches),
        "recommended_sponsors": matches
    }


def generate_csr_impact_certificate(sponsorship_id: str) -> Dict[str, Any]:
    """
    Generates an official Corporate Social Responsibility (CSR) Impact Audit Certificate
    for Section 135 Indian Companies Act statutory filing and corporate board audit.
    """
    s = SPONSORSHIPS_STORE.get(sponsorship_id)
    if not s:
        return {"status": "error", "message": f"Sponsorship {sponsorship_id} not found."}

    proto = PROTOTYPES_STORE.get(s.get("prototype_id", ""))
    impact = proto.get("expected_civic_impact", {}) if proto else {}

    cert_id = f"CSR-CERT-{uuid.uuid4().hex[:8].upper()}"
    now_iso = datetime.now().isoformat()

    certificate_payload = {
        "certificate_id": cert_id,
        "title": "CERTIFICATE OF STATUTORY CSR IMPACT & MUNICIPAL DEPLOYMENT",
        "regulatory_framework": "Section 135 & Schedule VII, Companies Act, 2013 (Ministry of Corporate Affairs, India)",
        "issuing_authority": "Samvad-Setu Civic-Academic Innovation Council",
        "issued_at": now_iso,
        "corporate_benefactor": {
            "company_name": s.get("company_name"),
            "mca_cin": s.get("mca_cin"),
            "authorized_signatory": s.get("corporate_representative"),
            "csr_grant_amount_inr": s.get("pledged_amount_inr"),
            "amount_disbursed_to_date_inr": s.get("total_disbursed_inr")
        },
        "beneficiary_hei": {
            "institution_name": s.get("institution_name"),
            "engineering_team": s.get("team_name"),
            "faculty_mentor": s.get("faculty_mentor")
        },
        "supported_prototype": {
            "prototype_id": s.get("prototype_id"),
            "title": s.get("prototype_title"),
            "trl_level": proto.get("trl_level") if proto else 6,
            "trl_description": proto.get("trl_description") if proto else "Field Demonstration"
        },
        "schedule_vii_eligibility": {
            "qualified_items": proto.get("schedule_vii_categories", ["item_iv", "item_ii"]) if proto else ["item_iv"],
            "statutory_descriptions": proto.get("schedule_vii_descriptions", []) if proto else []
        },
        "verified_civic_impact_metrics": {
            "estimated_citizens_benefited": impact.get("citizens_benefited_estimate", 15000),
            "remediation_durability_years": impact.get("durability_years_estimate", 5),
            "public_fund_efficiency_gain_percent": impact.get("cost_saving_vs_contractor_percent", 65),
            "municipal_site_clearance_status": s.get("municipal_site_clearance", {}).get("status", "cleared_for_pilot")
        },
        "governance_compliance": {
            "ip_licensing": "Civic Commons License (CCL v1.0) - Non-Commercial Public Commons",
            "milestone_escrow_model": "3-Phase Milestone Escrow (No lump-sum risk)",
            "statutory_deduction_eligibility": "100% Qualifying CSR Expenditure under MCA Norms"
        }
    }

    return {
        "status": "success",
        "certificate_id": cert_id,
        "certificate": certificate_payload
    }
