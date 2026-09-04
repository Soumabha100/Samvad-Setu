"""
Academic Engine Verification Test Script
Tests:
1. Indian Institutions master search & AISHE directory
2. 4-Tier Problem Complexity Evaluation
3. 1st-Year Student Safety Guardrail (blocking unsolvable research problems)
4. Syllabus Core Subject Matching across Civil, CSE, and Environmental Engineering
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

from academic import (
    search_institutions,
    get_institution_by_id,
    evaluate_problem_complexity,
    ComplexityTier,
    SyllabusMatcher,
    SyllabusCurriculum,
    AICTE_CIVIL_ENGINEERING,
    AICTE_COMPUTER_SCIENCE,
    AICTE_ENVIRONMENTAL_ENGG
)


def run_tests():
    print("=" * 70)
    print("🏛️  SAMVAD-SETU ACADEMIC ENGINE VERIFICATION SUITE")
    print("=" * 70)

    # -------------------------------------------------------------
    # Test 1: Indian Institutions Directory & Search
    # -------------------------------------------------------------
    print("\n--- TEST 1: Indian Institutions Search & AISHE Directory ---")
    results = search_institutions(query="Bombay")
    assert len(results) > 0, "Failed to find IIT Bombay"
    print(f"✅ Found: {results[0]['name']} (AISHE: {results[0]['aishe_code']})")

    jh_results = search_institutions(state="Jharkhand")
    assert len(jh_results) >= 2, "Expected Jharkhand institutions (BIT Sindri, BIT Mesra)"
    print(f"✅ Found {len(jh_results)} institutions in Jharkhand: {[i['short_name'] for i in jh_results]}")

    # -------------------------------------------------------------
    # Test 2: Problem Complexity Evaluation (4 Tiers)
    # -------------------------------------------------------------
    print("\n--- TEST 2: 4-Tier Problem Complexity Evaluation ---")

    # Case A: Tier 1 (Foundation)
    prob_t1 = "Ward 4 door-to-door solid waste segregation survey and citizen photo documentation drive."
    res_t1 = evaluate_problem_complexity(prob_t1)
    print(f"• Problem: '{prob_t1[:50]}...'")
    print(f"  -> Tier: {res_t1.tier.name} (Min Year: {res_t1.min_academic_year}) | Score: {res_t1.complexity_score}")
    assert res_t1.tier == ComplexityTier.TIER_1_FOUNDATION, f"Expected Tier 1, got {res_t1.tier}"

    # Case B: Tier 2 (Applied)
    prob_t2 = "Create a web database portal with GIS map coordinates to record municipal water pipe leaks and valve pressure levels."
    res_t2 = evaluate_problem_complexity(prob_t2)
    print(f"• Problem: '{prob_t2[:50]}...'")
    print(f"  -> Tier: {res_t2.tier.name} (Min Year: {res_t2.min_academic_year}) | Score: {res_t2.complexity_score}")
    assert res_t2.tier == ComplexityTier.TIER_2_APPLIED, f"Expected Tier 2, got {res_t2.tier}"

    # Case C: Tier 3 (Advanced Capstone)
    prob_t3 = "Deploy real-time edge computer vision YOLO object detection with IoT sensors on municipal garbage trucks for automated pothole scanning."
    res_t3 = evaluate_problem_complexity(prob_t3)
    print(f"• Problem: '{prob_t3[:50]}...'")
    print(f"  -> Tier: {res_t3.tier.name} (Min Year: {res_t3.min_academic_year}) | Score: {res_t3.complexity_score}")
    assert res_t3.tier == ComplexityTier.TIER_3_ADVANCED, f"Expected Tier 3, got {res_t3.tier}"

    # Case D: Tier 4 (R&D Research)
    prob_t4 = "Unsolved research problem: Acoustic tomography and computational fluid dynamics (CFD) for deep underground sewer surge modeling and novel polymer material healing."
    res_t4 = evaluate_problem_complexity(prob_t4)
    print(f"• Problem: '{prob_t4[:50]}...'")
    print(f"  -> Tier: {res_t4.tier.name} (Min Year: {res_t4.min_academic_year}) | Score: {res_t4.complexity_score}")
    assert res_t4.tier == ComplexityTier.TIER_4_RESEARCH, f"Expected Tier 4, got {res_t4.tier}"
    print("✅ All 4 complexity tiers classified correctly!")

    # -------------------------------------------------------------
    # Test 3: Safety Guardrail (Blocking Tier 3/4 from 1st Year)
    # -------------------------------------------------------------
    print("\n--- TEST 3: Safety Guardrail (Junior Student Protection) ---")
    civil_matcher = SyllabusMatcher(SyllabusCurriculum.from_dict(AICTE_CIVIL_ENGINEERING))

    # Try assigning Tier 4 research problem to a 1st-year student
    match_t4_year1 = civil_matcher.match_problem(
        problem_text=prob_t4,
        category="drainage",
        target_student_year=1
    )
    guardrail_1 = match_t4_year1["guardrail_evaluation"]
    print(f"• Attempting to assign Tier 4 problem to 1st-Year Student:")
    print(f"  -> is_eligible: {guardrail_1['is_eligible']}")
    print(f"  -> status: {guardrail_1['guardrail_status']}")
    print(f"  -> warning: {guardrail_1['guardrail_warning']}")
    assert guardrail_1["is_eligible"] is False, "Guardrail failed! Tier 4 problem was not blocked from 1st-year student!"
    assert guardrail_1["guardrail_status"] == "BLOCKED_EXCEEDS_STUDENT_YEAR"
    print("✅ 1st-Year student safety guardrail successfully BLOCKED unsolvable research problem!")

    # Try assigning Tier 1 problem to a 1st-year student
    match_t1_year1 = civil_matcher.match_problem(
        problem_text=prob_t1,
        category="solid_waste",
        target_student_year=1
    )
    guardrail_2 = match_t1_year1["guardrail_evaluation"]
    print(f"\n• Attempting to assign Tier 1 problem to 1st-Year Student:")
    print(f"  -> is_eligible: {guardrail_2['is_eligible']}")
    print(f"  -> status: {guardrail_2['guardrail_status']}")
    assert guardrail_2["is_eligible"] is True, "Tier 1 problem should be eligible for 1st-year students"
    print("✅ 1st-Year student successfully APPROVED for foundation civic survey!")

    # -------------------------------------------------------------
    # Test 4: Core Subject Matching Accuracy
    # -------------------------------------------------------------
    print("\n--- TEST 4: Core Subject Matching Accuracy ---")
    
    # Pothole & Road Damage -> Should match Highway & Transportation Engg (CE-301)
    pothole_problem = "Deep structural potholes and asphalt disintegration on main arterial road causing vehicle accidents."
    pothole_match = civil_matcher.match_problem(pothole_problem, category="road_damage")
    best_sub = pothole_match["best_matched_subject"]
    print(f"• Pothole Complaint Matched To:")
    print(f"  -> Subject: {best_sub['subject_code']} - {best_sub['subject_name']}")
    print(f"  -> Semester: {best_sub['semester']} (Year {best_sub['academic_year']}) | Core: {best_sub['is_core']}")
    print(f"  -> Match Similarity: {best_sub['similarity_percent']}%")
    assert best_sub["subject_code"] == "CE-301", f"Expected CE-301, got {best_sub['subject_code']}"

    # Sewage Overflow -> Should match Wastewater and Environmental Engg (CE-302)
    sewage_problem = "Underground sewage line clogged, manhole overflowing with foul stench onto residential colony street."
    sewage_match = civil_matcher.match_problem(sewage_problem, category="drainage")
    sewage_sub = sewage_match["best_matched_subject"]
    print(f"\n• Sewage Complaint Matched To:")
    print(f"  -> Subject: {sewage_sub['subject_code']} - {sewage_sub['subject_name']}")
    print(f"  -> Semester: {sewage_sub['semester']} (Year {sewage_sub['academic_year']}) | Core: {sewage_sub['is_core']}")
    print(f"  -> Match Similarity: {sewage_sub['similarity_percent']}%")
    assert sewage_sub["subject_code"] == "CE-302", f"Expected CE-302, got {sewage_sub['subject_code']}"

    # Computer Science Test: Database Grievance Portal
    cse_matcher = SyllabusMatcher(SyllabusCurriculum.from_dict(AICTE_COMPUTER_SCIENCE))
    cs_problem = "Build a web application with relational SQL tables, user authentication, and map pins for tracking municipal grievances."
    cs_match = cse_matcher.match_problem(cs_problem, category="other")
    cs_sub = cs_match["best_matched_subject"]
    print(f"\n• CS Grievance Portal Matched To:")
    print(f"  -> Subject: {cs_sub['subject_code']} - {cs_sub['subject_name']}")
    print(f"  -> Similarity: {cs_sub['similarity_percent']}%")
    assert cs_sub["subject_code"] == "CS-201", f"Expected CS-201, got {cs_sub['subject_code']}"

    # -------------------------------------------------------------
    # Test 5: Government Failure & Chronic Escalation Engine
    # -------------------------------------------------------------
    print("\n--- TEST 5: Government Failure & Chronic Escalation Engine ---")
    from academic import (
        evaluate_escalation_eligibility,
        register_chronic_problem_statement,
        get_chronic_problems,
        claim_chronic_problem
    )

    # Scenario 5A: Fresh normal complaint within SLA -> Should NOT escalate to college
    fresh_check = evaluate_escalation_eligibility(
        status="in_progress",
        sla_breached=False,
        recurrence_count=1,
        recurrence_period_days=2,
        failed_resolution_attempts=0
    )
    print(f"• Fresh Complaint Evaluation: {fresh_check['decision']}")
    assert fresh_check["is_eligible_for_academic_routing"] is False
    print("✅ Fresh municipal complaint kept with government authority as intended.")

    # Scenario 5B: Chronic failure over 45 days + 2 failed contractor attempts -> Escalates to HEI
    chronic_reg = register_chronic_problem_statement(
        problem_id="PROB-DHN-8821",
        title="Chronic road subsidence and repeating sinkhole outside Railway Colony",
        description="Pavement collapses every monsoon. PWD contractor filled gravel twice, but road broke open within 2 weeks again.",
        category="road_damage",
        department="Public Works Department (PWD - Roads)",
        location={"lat": 23.7957, "lng": 86.4304, "address": "Station Road, Dhanbad"},
        status="unresolved_breached",
        sla_breached=True,
        recurrence_count=4,
        recurrence_period_days=45,
        failed_resolution_attempts=2,
        authority_notes="PWD engineers report sub-base drainage washout; standard cold-mix patch fails repeatedly."
    )
    print(f"\n• Chronic Incident Escalated:")
    print(f"  -> Action: {chronic_reg['action']}")
    print(f"  -> Escalation ID: {chronic_reg['chronic_problem']['escalation_id']}")
    print(f"  -> Matched Subject: {chronic_reg['chronic_problem']['ai_academic_routing']['best_matched_subject']['subject_name']}")
    assert chronic_reg["status"] == "success"
    esc_id = chronic_reg["chronic_problem"]["escalation_id"]

    # Scenario 5C: College browses available chronic problems
    avail = get_chronic_problems(department="Civil Engineering")
    print(f"✅ Available chronic problems in HEI Problem Bank: {len(avail)}")
    assert len(avail) >= 1

    # Scenario 5D: 1st Year Team tries to claim it -> Blocked by Guardrail!
    guardrail_claim = claim_chronic_problem(
        escalation_id=esc_id,
        institution_name="BIT Sindri",
        team_name="Freshers Civil Team",
        student_academic_year=1
    )
    print(f"• 1st Year Student Claim Attempt: status = {guardrail_claim['status']}")
    assert guardrail_claim["status"] == "guardrail_blocked"
    print("✅ 1st Year team blocked from claiming chronic structural engineering problem.")

    # Scenario 5E: 4th Year Final Year Capstone Team claims it -> Successfully allocated!
    req_year = chronic_reg["chronic_problem"]["ai_academic_routing"]["problem_complexity"]["min_academic_year"]
    senior_claim = claim_chronic_problem(
        escalation_id=esc_id,
        institution_name="BIT Sindri",
        team_name="Final Year Capstone Team",
        student_academic_year=req_year
    )
    print(f"• Year {req_year} Capstone Team Claim Attempt: status = {senior_claim['status']}")
    assert senior_claim["status"] == "success"
    print(f"✅ Allocated to: {senior_claim['problem']['claimed_by_team']} ({senior_claim['problem']['claimed_by_institution']})")

    print("\n" + "=" * 70)
    print("🎉 ALL ACADEMIC & CHRONIC ESCALATION TESTS PASSED WITH 100% SUCCESS!")
    print("=" * 70)


if __name__ == "__main__":
    run_tests()
