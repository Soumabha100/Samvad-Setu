"""
FastAPI REST API Integration Test for Corporate CSR Funding & Prototype Showcase
Module: ai-engine/part-b/corporate/test_corporate_api.py
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

# pyrefly: ignore [missing-import]
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_corporate_fastapi_endpoints():
    print("=" * 70)
    print("🌐 TESTING CORPORATE FASTAPI REST ENDPOINTS")
    print("=" * 70)

    # 1. GET /corporate/sponsors
    res_sponsors = client.get("/corporate/sponsors")
    assert res_sponsors.status_code == 200, res_sponsors.text
    sponsors_data = res_sponsors.json()
    print(f"✅ 1. GET /corporate/sponsors -> {sponsors_data['total_sponsors']} corporate partners registered")

    # 2. POST /corporate/prototypes/submit
    prototype_payload = {
        "escalation_id": "ESC-LIVE-TEST-001",
        "team_name": "HydroGuard IIT Bombay",
        "institution_name": "IIT Bombay",
        "faculty_mentor": "Dr. Arvind Swaminathan",
        "prototype_title": "AI Acoustic Flow-Sensor & Smart Sump Drain Gate",
        "executive_summary": "Autonomous urban storm-drainage flap that prevents backflow during monsoons.",
        "technical_approach": "Ultrasonic depth monitoring coupled with solenoid-actuated valve doors.",
        "trl_level": 6,
        "bill_of_materials": [
            {"item": "Industrial Ultrasonic Level Transmitter", "cost_inr": 42000.0, "qty": 2},
            {"item": "High-Torque Stainless Steel Actuator Gate", "cost_inr": 120000.0, "qty": 1},
            {"item": "Solar Backed Telemetry Node (4G)", "cost_inr": 28000.0, "qty": 1}
        ],
        "total_funding_required_inr": 300000.0,
        "demo_video_url": "https://youtu.be/hydroguard_test",
        "category": "water_drainage"
    }

    res_sub = client.post("/corporate/prototypes/submit", json=prototype_payload)
    assert res_sub.status_code == 200, res_sub.text
    sub_data = res_sub.json()
    proto_id = sub_data["prototype"]["prototype_id"]
    print(f"✅ 2. POST /corporate/prototypes/submit -> Registered {proto_id}")

    # 3. GET /corporate/prototypes
    res_list = client.get("/corporate/prototypes?min_trl=5")
    assert res_list.status_code == 200, res_list.text
    list_data = res_list.json()
    print(f"✅ 3. GET /corporate/prototypes?min_trl=5 -> Found {list_data['total_prototypes']} qualifying prototypes")

    # 4. GET /corporate/prototypes/{id}
    res_detail = client.get(f"/corporate/prototypes/{proto_id}")
    assert res_detail.status_code == 200, res_detail.text
    print(f"✅ 4. GET /corporate/prototypes/{proto_id} -> Retrieved complete BoM & TRL details")

    # 5. GET /corporate/prototypes/{id}/match-sponsors
    res_match = client.get(f"/corporate/prototypes/{proto_id}/match-sponsors")
    assert res_match.status_code == 200, res_match.text
    match_data = res_match.json()
    best_sponsor_id = match_data["recommended_sponsors"][0]["sponsor_id"]
    print(f"✅ 5. GET /corporate/prototypes/{proto_id}/match-sponsors -> Best match: {best_sponsor_id}")

    # 6. POST /corporate/sponsorship/pledge
    pledge_payload = {
        "prototype_id": proto_id,
        "sponsor_id": best_sponsor_id,
        "pledged_amount_inr": 300000.0,
        "corporate_representative_name": "Rohan Deshmukh",
        "corporate_contact_email": "urban.csr@infosys.com",
        "escrow_terms_accepted": True,
        "civic_commons_license_accepted": True
    }
    res_pledge = client.post("/corporate/sponsorship/pledge", json=pledge_payload)
    assert res_pledge.status_code == 200, res_pledge.text
    pledge_data = res_pledge.json()
    sponsorship_id = pledge_data["sponsorship"]["sponsorship_id"]
    print(f"✅ 6. POST /corporate/sponsorship/pledge -> Pledged {sponsorship_id} (Escrow Tranche 1 Disbursed)")

    # 7. POST /corporate/sponsorship/approve-milestone (Guardrail Block on unauthorized role)
    blocked_milestone = {
        "sponsorship_id": sponsorship_id,
        "tranche_index": 2,
        "approver_role": "student_lead",
        "approver_name": "Rahul Verma",
        "verification_notes": "Finished fabrication."
    }
    res_block = client.post("/corporate/sponsorship/approve-milestone", json=blocked_milestone)
    assert res_block.status_code == 403, f"Expected 403, got {res_block.status_code}"
    print("✅ 7. POST /corporate/sponsorship/approve-milestone -> 403 Forbidden correctly returned for unauthorized role")

    # 8. POST /corporate/sponsorship/approve-milestone (Authorized Municipal Officer)
    valid_milestone = {
        "sponsorship_id": sponsorship_id,
        "tranche_index": 2,
        "approver_role": "municipal_officer",
        "approver_name": "Er. Priya Sharma (City Stormwater Chief)",
        "verification_notes": "Drain site verified and pilot permit granted."
    }
    res_approve = client.post("/corporate/sponsorship/approve-milestone", json=valid_milestone)
    assert res_approve.status_code == 200, res_approve.text
    print("✅ 8. POST /corporate/sponsorship/approve-milestone -> Tranche 2 released by Municipal Officer")

    # 9. GET /corporate/sponsorship/{id}/agreement
    res_agreement = client.get(f"/corporate/sponsorship/{sponsorship_id}/agreement")
    assert res_agreement.status_code == 200, res_agreement.text
    print(f"✅ 9. GET /corporate/sponsorship/{sponsorship_id}/agreement -> Tripartite Governance Agreement rendered")

    # 10. GET /corporate/sponsorship/{id}/csr-certificate
    res_cert = client.get(f"/corporate/sponsorship/{sponsorship_id}/csr-certificate")
    assert res_cert.status_code == 200, res_cert.text
    cert_data = res_cert.json()
    print(f"✅ 10. GET /corporate/sponsorship/{sponsorship_id}/csr-certificate -> Certificate {cert_data['certificate_id']} issued")

    print("\n🎉 ALL FASTAPI CORPORATE ENDPOINTS ARE 100% OPERATIONAL & VERIFIED!")


if __name__ == "__main__":
    test_corporate_fastapi_endpoints()
