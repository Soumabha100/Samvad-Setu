"""
Unit Tests for Corporate CSR Funding & Prototype Showcase Engine
Module: ai-engine/part-b/corporate/test_corporate.py
"""

import sys
from pathlib import Path

# Setup paths
CORPORATE_DIR = Path(__file__).resolve().parent
PART_B_DIR = CORPORATE_DIR.parent
for p in [str(PART_B_DIR), str(CORPORATE_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore
    except AttributeError:
        pass

from corporate.prototypes_data import (
    register_prototype_submission,
    list_prototypes,
    get_prototype_by_id,
    CORPORATE_SPONSORS_STORE
)
from corporate.stakeholder_governance import (
    create_sponsorship_pledge,
    approve_milestone,
    generate_tripartite_agreement_text
)
from corporate.csr_engine import (
    match_sponsors_for_prototype,
    generate_csr_impact_certificate
)


def test_corporate_lifecycle():
    print("=" * 70)
    print("🏢 TESTING CORPORATE CSR FUNDING & PROTOTYPE ENGINE")
    print("=" * 70)

    # 1. Register Prototype Submission by HEI Student Team
    proto = register_prototype_submission(
        escalation_id="ESC-27A23A",
        team_name="Team TerraFix",
        institution_name="IIT Bombay (AISHE: U-0306)",
        faculty_mentor="Prof. R. K. Banerjee",
        prototype_title="Bio-Polymer Geogrid Sub-base Remediation Rig",
        executive_summary="Modular geotechnical injection unit that stabilizes waterlogged black cotton soil subgrades.",
        technical_approach="High-pressure cold emulsion injection combined with recycled PET geogrids preventing sinkhole collapse.",
        trl_level=5,
        bill_of_materials=[
            {"item": "High-Pressure Hydraulic Injection Pump", "cost_inr": 85000.0, "qty": 1},
            {"item": "Modified Bio-Polymer Grout (500kg)", "cost_inr": 45000.0, "qty": 1},
            {"item": "IoT Pore-Pressure Telemetry Sensors", "cost_inr": 35000.0, "qty": 4}
        ],
        total_funding_required_inr=250000.0,
        demo_video_url="https://youtube.com/watch?v=terrafix_demo",
        cad_repo_url="https://github.com/terrafix/geogrid-cad",
        category="road_damage"
    )

    proto_id = proto["prototype_id"]
    print(f"✅ 1. Prototype registered: {proto_id} ('{proto['prototype_title']}')")
    print(f"   • TRL: {proto['trl_level']} ({proto['trl_description']})")
    print(f"   • Funding Goal: INR {proto['total_funding_required_inr']:,.2f}")
    print(f"   • Schedule VII Items: {proto['schedule_vii_categories']}")

    # 2. Browse Showcase Feed
    all_protos = list_prototypes(min_trl=4)
    assert len(all_protos) >= 1
    print(f"✅ 2. Corporate Showcase Query (min_trl=4): {len(all_protos)} prototypes listed")

    # 3. Match Sponsors for Prototype
    matches = match_sponsors_for_prototype(proto_id)
    assert matches["total_matches"] > 0
    top_sponsor = matches["recommended_sponsors"][0]
    print(f"✅ 3. CSR AI Matcher: Top sponsor is '{top_sponsor['company_name']}' with {top_sponsor['matching_score_percent']}% fit")

    # 4. Corporate CSR Pledge into 3-Tranche Milestone Escrow
    sponsor_id = top_sponsor["sponsor_id"]
    pledge_res = create_sponsorship_pledge(
        prototype_id=proto_id,
        sponsor_id=sponsor_id,
        pledged_amount_inr=250000.0,
        corporate_representative_name="Dr. Ananya Sharma",
        corporate_contact_email="csr.initiative@tatasustainability.org",
        escrow_terms_accepted=True,
        civic_commons_license_accepted=True
    )
    assert pledge_res["status"] == "pledge_recorded_in_escrow"
    sponsorship = pledge_res["sponsorship"]
    sponsorship_id = sponsorship["sponsorship_id"]
    print(f"✅ 4. CSR Pledge Committed: {sponsorship_id}")
    print(f"   • Escrow Milestone 1 (30% Lab Build): INR {sponsorship['milestones'][0]['amount_inr']:,.2f} [Disbursed]")
    print(f"   • Escrow Milestone 2 (40% ULB Field Pilot): INR {sponsorship['milestones'][1]['amount_inr']:,.2f} [Locked]")
    print(f"   • Escrow Milestone 3 (30% Civic Handover): INR {sponsorship['milestones'][2]['amount_inr']:,.2f} [Locked]")

    # 5. Stakeholder Conflict Guardrail Test:
    # Attempting to unlock Tranche 2 WITHOUT municipal officer must be blocked!
    blocked_res = approve_milestone(
        sponsorship_id=sponsorship_id,
        tranche_index=2,
        approver_role="faculty_mentor",  # Unauthorized role for municipal field clearance
        approver_name="Prof. R. K. Banerjee",
        verification_notes="Lab tests passed."
    )
    assert blocked_res["status"] == "gatekeeper_blocked"
    print(f"✅ 5. Gatekeeper Guardrail Blocked unauthorized field pilot unlock (Protected public safety)")

    # 6. Legitimate Municipal ULB Clearance
    approved_res = approve_milestone(
        sponsorship_id=sponsorship_id,
        tranche_index=2,
        approver_role="municipal_officer",  # Authorized ULB Engineer
        approver_name="Er. Suresh Patil (Executive Engineer, PWD)",
        verification_notes="Station Road site inspected and cleared for 14-day field pilot installation."
    )
    assert approved_res["status"] == "milestone_approved_and_disbursed"
    print(f"✅ 6. Municipal Gatekeeper Signoff Approved: INR {approved_res['amount_disbursed_inr']:,.2f} released to HEI team")

    # 7. Tripartite Legal & IP Agreement Generation
    agreement = generate_tripartite_agreement_text(sponsorship_id)
    assert agreement["status"] == "success"
    assert "CIVIC COMMONS LICENSE" in agreement["agreement_text"].upper()
    print(f"✅ 7. Tripartite Governance Agreement rendered: {agreement['agreement_id']}")

    # 8. Formal MCA Schedule VII CSR Impact & Tax Audit Certificate
    cert = generate_csr_impact_certificate(sponsorship_id)
    assert cert["status"] == "success"
    print(f"✅ 8. Statutory CSR-1 Impact Certificate generated: {cert['certificate_id']}")
    print(f"   • Corporate Benefactor: {cert['certificate']['corporate_benefactor']['company_name']}")
    print(f"   • Citizens Benefited: {cert['certificate']['verified_civic_impact_metrics']['estimated_citizens_benefited']}")
    print(f"   • Regulatory Code: {cert['certificate']['regulatory_framework']}")

    print("\n🎉 ALL CORPORATE CSR & PROTOTYPE TESTS PASSED (100% SUCCESS)!")


if __name__ == "__main__":
    test_corporate_lifecycle()
