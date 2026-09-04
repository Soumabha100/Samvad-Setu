"""
Academic API Integration Test
Tests all FastAPI endpoints on main.py:
- GET /academic/institutions
- GET /academic/institutions/{id}
- POST /academic/complexity/evaluate
- GET /academic/sample-syllabi
- POST /academic/syllabus/match
"""

import sys
from pathlib import Path

# Add part-b root and academic directory to path
ACADEMIC_DIR = Path(__file__).resolve().parent
PART_B_DIR = ACADEMIC_DIR.parent
for p in [str(PART_B_DIR), str(ACADEMIC_DIR)]:
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


def test_academic_api():
    print("=" * 70)
    print("🌐 TESTING PART-B FASTAPI ACADEMIC ENDPOINTS")
    print("=" * 70)

    # 1. Test GET /academic/institutions
    res = client.get("/academic/institutions?query=IIT")
    assert res.status_code == 200, f"Failed: {res.status_code}"
    data = res.json()
    print(f"✅ GET /academic/institutions?query=IIT -> {data['total_results']} institutions found")

    # 2. Test GET /academic/institutions/{id}
    res_inst = client.get("/academic/institutions/inst_iit_b")
    assert res_inst.status_code == 200
    inst_data = res_inst.json()["institution"]
    print(f"✅ GET /academic/institutions/inst_iit_b -> {inst_data['name']} (AISHE: {inst_data['aishe_code']})")

    # 3. Test POST /academic/complexity/evaluate
    comp_payload = {
        "text": "Citizen survey on household plastic waste and photo collection in Ward 10",
        "category": "garbage"
    }
    res_comp = client.post("/academic/complexity/evaluate", json=comp_payload)
    assert res_comp.status_code == 200
    comp_data = res_comp.json()["complexity"]
    print(f"✅ POST /academic/complexity/evaluate -> Tier: {comp_data['tier_name']} (Year {comp_data['min_academic_year']})")

    # 4. Test GET /academic/sample-syllabi
    res_syl = client.get("/academic/sample-syllabi")
    assert res_syl.status_code == 200
    syl_list = res_syl.json()["available_curricula"]
    print(f"✅ GET /academic/sample-syllabi -> Curricula: {syl_list}")

    # 5. Test POST /academic/syllabus/match (with guardrail)
    # 5a. Advanced problem with Year 1 target (should be BLOCKED)
    match_payload_blocked = {
        "problem_text": "Acoustic tomography and computational fluid dynamics to study deep underground sewer surge and novel polymer healing",
        "category": "drainage",
        "department_hint": "Civil Engineering",
        "target_student_year": 1,
        "curriculum_key": "civil_engineering"
    }
    res_match_1 = client.post("/academic/syllabus/match", json=match_payload_blocked)
    assert res_match_1.status_code == 200
    m1_data = res_match_1.json()
    print(f"✅ POST /academic/syllabus/match (Advanced problem + Year 1 target):")
    print(f"   -> is_eligible: {m1_data['guardrail_evaluation']['is_eligible']} ({m1_data['guardrail_evaluation']['guardrail_status']})")
    assert m1_data['guardrail_evaluation']['is_eligible'] is False

    # 5b. Highway pothole problem (should match CE-301)
    match_payload_ok = {
        "problem_text": "Potholes and bitumen breakdown on arterial highway causing road accidents",
        "category": "road_damage",
        "department_hint": "Civil Engineering",
        "target_student_year": 3,
        "curriculum_key": "civil_engineering"
    }
    res_match_2 = client.post("/academic/syllabus/match", json=match_payload_ok)
    assert res_match_2.status_code == 200
    m2_data = res_match_2.json()
    best_sub = m2_data["best_matched_subject"]
    print(f"✅ POST /academic/syllabus/match (Highway pothole + Year 3 target):")
    print(f"   -> is_eligible: {m2_data['guardrail_evaluation']['is_eligible']}")
    print(f"   -> Matched Core Subject: {best_sub['subject_code']} - {best_sub['subject_name']}")
    assert best_sub["subject_code"] == "CE-301"

    # 6. Test POST /academic/escalation/check-eligibility
    elig_payload_fail = {
        "status": "in_progress",
        "sla_breached": False,
        "recurrence_count": 1,
        "recurrence_period_days": 1
    }
    res_elig_fail = client.post("/academic/escalation/check-eligibility", json=elig_payload_fail)
    assert res_elig_fail.status_code == 200
    assert res_elig_fail.json()["eligibility"]["is_eligible_for_academic_routing"] is False
    print("✅ POST /academic/escalation/check-eligibility (Fresh complaint) -> Kept with Government")

    # 7. Test POST /academic/escalation/register (Gov failure / chronic recurrence)
    reg_payload = {
        "problem_id": "CIVIC-RNC-9901",
        "title": "Recurrent main storm drain collapse during monsoon",
        "description": "Drain retaining wall collapses repeatedly over 60 days. Contractor rebuilt twice, but wall washed away again.",
        "category": "drainage",
        "department": "Public Health Engineering Dept (PHED - Drainage)",
        "location": {"lat": 23.3441, "lng": 85.3096, "address": "Kanke Road, Ranchi"},
        "status": "unresolved_breached",
        "sla_breached": True,
        "recurrence_count": 3,
        "recurrence_period_days": 60,
        "failed_resolution_attempts": 2,
        "curriculum_key": "civil_engineering"
    }
    res_reg = client.post("/academic/escalation/register", json=reg_payload)
    assert res_reg.status_code == 200
    reg_data = res_reg.json()
    assert reg_data["status"] == "success"
    esc_id = reg_data["chronic_problem"]["escalation_id"]
    print(f"✅ POST /academic/escalation/register -> Escalation ID: {esc_id} (Published to Bank)")

    # 8. Test GET /academic/chronic-problems
    res_bank = client.get("/academic/chronic-problems?department=Civil")
    assert res_bank.status_code == 200
    bank_data = res_bank.json()
    assert bank_data["total_available"] >= 1
    print(f"✅ GET /academic/chronic-problems -> {bank_data['total_available']} chronic problems available for colleges")

    # 9. Test POST /academic/chronic-problems/claim
    claim_payload = {
        "escalation_id": esc_id,
        "institution_name": "BIT Mesra",
        "team_name": "Team Environmental Hydro",
        "student_academic_year": 4
    }
    res_claim = client.post("/academic/chronic-problems/claim", json=claim_payload)
    assert res_claim.status_code == 200
    assert res_claim.json()["status"] == "success"
    print(f"✅ POST /academic/chronic-problems/claim -> Claimed successfully by {claim_payload['team_name']}")

    # 10. Test POST /academic/chronic-problems/{id}/generate-dossier (Gemini AI synthesis)
    res_gen_pdf = client.post(f"/academic/chronic-problems/{esc_id}/generate-dossier", json={})
    assert res_gen_pdf.status_code == 200
    pdf_info = res_gen_pdf.json()
    assert pdf_info["status"] == "success"
    print(f"✅ POST /academic/chronic-problems/{esc_id}/generate-dossier -> PDF generated: {pdf_info['pdf_path']}")

    # 11. Test GET /academic/chronic-problems/{id}/dossier-pdf (Download PDF stream)
    res_pdf_dl = client.get(f"/academic/chronic-problems/{esc_id}/dossier-pdf")
    assert res_pdf_dl.status_code == 200
    assert res_pdf_dl.headers["content-type"] == "application/pdf"
    assert len(res_pdf_dl.content) > 1000  # Non-trivial PDF size
    print(f"✅ GET /academic/chronic-problems/{esc_id}/dossier-pdf -> Downloaded {len(res_pdf_dl.content)} bytes of professional PDF dossier")

    print("\n" + "=" * 70)
    print("🎉 ALL FASTAPI ACADEMIC, CHRONIC ESCALATION & PDF DOSSIER ENDPOINTS VERIFIED!")
    print("=" * 70)


if __name__ == "__main__":
    test_academic_api()
