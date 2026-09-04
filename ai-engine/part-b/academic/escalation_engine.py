"""
Government Authority Failure & Chronic Problem Escalation Engine
Module: part-b/academic/escalation_engine.py

Business Logic:
1. Normal municipal grievances are handled by government municipal authorities first.
2. An incident is ONLY escalated to Higher Education Institutions (HEIs) if:
   a) The government authority failed to provide a permanent solution (SLA breached, marked unresolved, or failed contractor attempts).
   b) The problem is CHRONIC: repeatedly occurs over weeks or months at the same location, indicating a structural/engineering design flaw.
3. Once escalated, the AI categorizes technical complexity, matches to Core Department Subjects, and lists it in the Institutional Problem Bank for colleges to adopt.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid

from .complexity_scorer import evaluate_problem_complexity, ComplexityTier
from .syllabus_engine import SyllabusMatcher, SyllabusCurriculum
from .sample_syllabi import SAMPLE_SYLLABI, AICTE_CIVIL_ENGINEERING
from .dossier_generator import generate_hei_problem_dossier_pdf


# In-memory repository of chronic municipal problems available to colleges
CHRONIC_PROBLEMS_POOL: List[Dict[str, Any]] = []


def evaluate_escalation_eligibility(
    status: str = "unresolved",
    sla_breached: bool = False,
    recurrence_count: int = 1,
    recurrence_period_days: int = 0,
    failed_resolution_attempts: int = 0,
    authority_notes: Optional[str] = None
) -> Dict[str, Any]:
    """
    Determines whether a municipal complaint qualifies for HEI Academic Routing.
    A problem qualifies ONLY IF government authority failed to solve it OR it is chronically recurring.
    """
    reasons = []
    is_eligible = False

    # Condition 1: Repeated recurrence over weeks or months (Chronic engineering issue)
    if recurrence_count >= 3:
        is_eligible = True
        reasons.append(
            f"CHRONIC_RECURRENCE: Problem reported {recurrence_count} times across {recurrence_period_days} days. "
            "Repeated failure indicates a chronic systemic or engineering design flaw requiring academic R&D."
        )
    elif recurrence_count >= 2 and recurrence_period_days >= 14:
        is_eligible = True
        reasons.append(
            f"RECURRENT_FAILURE: Recurring issue observed across {recurrence_period_days} days "
            "without permanent municipal resolution."
        )

    # Condition 2: Government authority SLA breach or unresolvable status
    if sla_breached or status.lower() in ["unresolved_breached", "failed", "unsolvable_by_contractor"]:
        is_eligible = True
        reasons.append(
            "GOV_AUTHORITY_SLA_BREACH: Municipal department exceeded statutory SLA deadline without a viable solution."
        )

    # Condition 3: Multiple failed contractor repair attempts
    if failed_resolution_attempts >= 1:
        is_eligible = True
        reasons.append(
            f"FAILED_REPAIR_HISTORY: Municipal contractors attempted resolution {failed_resolution_attempts} time(s) "
            "but the defect resurfaced, proving standard maintenance methods are inadequate."
        )

    if not is_eligible:
        return {
            "is_eligible_for_academic_routing": False,
            "lifecycle_stage": "GOVERNMENT_AUTHORITY_ACTIVE",
            "decision": "REJECTED_REMAINS_WITH_GOVERNMENT",
            "explanation": (
                "Problem does not meet chronic escalation threshold. Municipal authority is still actively "
                "handling this under standard SLA. It must first breach SLA or repeatedly recur across weeks "
                "before being routed to academic institutions."
            ),
            "reasons": []
        }

    return {
        "is_eligible_for_academic_routing": True,
        "lifecycle_stage": "ESCALATED_TO_ACADEMIC_R_AND_D",
        "decision": "APPROVED_FOR_INSTITUTION_PORTAL",
        "explanation": "Problem verified as chronic civic failure / government solution shortfall. Approved for college student projects.",
        "reasons": reasons
    }


def register_chronic_problem_statement(
    problem_id: str,
    title: str,
    description: str,
    category: str,
    department: str,
    location: Dict[str, Any],
    status: str = "unresolved",
    sla_breached: bool = True,
    recurrence_count: int = 3,
    recurrence_period_days: int = 30,
    failed_resolution_attempts: int = 2,
    authority_notes: Optional[str] = None,
    curriculum_key: str = "civil_engineering",
    target_student_year: Optional[int] = None
) -> Dict[str, Any]:
    """
    Validates escalation criteria, runs AI complexity & syllabus core subject matching,
    and publishes the chronic problem statement into the institutional problem bank.
    """
    eligibility = evaluate_escalation_eligibility(
        status=status,
        sla_breached=sla_breached,
        recurrence_count=recurrence_count,
        recurrence_period_days=recurrence_period_days,
        failed_resolution_attempts=failed_resolution_attempts,
        authority_notes=authority_notes
    )

    if not eligibility["is_eligible_for_academic_routing"]:
        return {
            "status": "not_escalated",
            "problem_id": problem_id,
            "eligibility": eligibility,
            "message": eligibility["explanation"]
        }

    # Match to appropriate syllabus curriculum
    curriculum_data = SAMPLE_SYLLABI.get(curriculum_key.lower().strip(), AICTE_CIVIL_ENGINEERING)
    matcher = SyllabusMatcher(SyllabusCurriculum.from_dict(curriculum_data))
    
    match_result = matcher.match_problem(
        problem_text=f"{title}. {description}. Chronic recurrence history: {authority_notes or ''}",
        category=category,
        department_hint=department,
        target_student_year=target_student_year
    )

    esc_id = f"ESC-{uuid.uuid4().hex[:6].upper()}"
    chronic_entry = {
        "escalation_id": esc_id,
        "original_problem_id": problem_id,
        "title": title,
        "description": description,
        "category": category,
        "municipal_department": department,
        "location": location,
        "chronic_metrics": {
            "recurrence_count": recurrence_count,
            "recurrence_period_days": recurrence_period_days,
            "failed_attempts": failed_resolution_attempts,
            "authority_notes": authority_notes or "Repeated complaints from ward citizens; standard bitumen/filling washed away."
        },
        "escalation_reasons": eligibility["reasons"],
        "ai_academic_routing": match_result,
        "claim_status": "AVAILABLE",
        "claimed_by_institution": None,
        "claimed_by_team": None,
        "dossier_pdf_path": None,
        "dossier_pdf_url": f"/academic/chronic-problems/{esc_id}/dossier-pdf",
        "escalated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Automatically generate professional PDF dossier for HEIs
    try:
        pdf_path = generate_hei_problem_dossier_pdf(chronic_entry)
        chronic_entry["dossier_pdf_path"] = pdf_path
    except Exception as e:
        print(f"[WARNING] Could not generate dossier PDF: {e}")

    # Check if already present in pool
    existing = next((item for item in CHRONIC_PROBLEMS_POOL if item["original_problem_id"] == problem_id), None)
    if existing:
        existing.update(chronic_entry)
        entry_to_return = existing
    else:
        CHRONIC_PROBLEMS_POOL.append(chronic_entry)
        entry_to_return = chronic_entry

    return {
        "status": "success",
        "action": "PUBLISHED_TO_INSTITUTIONAL_PROBLEM_BANK",
        "eligibility": eligibility,
        "chronic_problem": entry_to_return
    }


def get_chronic_problems(
    department: Optional[str] = None,
    academic_year: Optional[int] = None,
    complexity_tier: Optional[int] = None,
    claim_status: Optional[str] = "AVAILABLE"
) -> List[Dict[str, Any]]:
    """
    Returns available chronic problem statements filtered by department, year suitability, or tier.
    """
    filtered = []
    dep_filter = (department or "").lower().strip()

    for item in CHRONIC_PROBLEMS_POOL:
        if claim_status and item.get("claim_status") != claim_status:
            continue
        
        match_info = item.get("ai_academic_routing", {})
        item_dept = match_info.get("department", "").lower()
        if dep_filter and dep_filter not in item_dept:
            continue

        comp_info = match_info.get("problem_complexity", {})
        if complexity_tier is not None and comp_info.get("tier") != complexity_tier:
            continue

        if academic_year is not None:
            # Check student year guardrail: student year must be >= min_academic_year
            min_year = comp_info.get("min_academic_year", 1)
            if academic_year < min_year:
                continue

        filtered.append(item)

    return filtered


def claim_chronic_problem(
    escalation_id: str,
    institution_name: str,
    team_name: str,
    student_academic_year: int
) -> Dict[str, Any]:
    """
    Allows a college student/faculty team to claim an unsolved problem statement,
    with guardrail validation on student academic year.
    """
    target = next((item for item in CHRONIC_PROBLEMS_POOL if item["escalation_id"] == escalation_id), None)
    if not target:
        return {"status": "error", "message": f"Problem with escalation ID '{escalation_id}' not found."}

    if target["claim_status"] == "CLAIMED":
        return {
            "status": "already_claimed",
            "message": f"This problem has already been claimed by '{target['claimed_by_institution']}' ({target['claimed_by_team']})."
        }

    # Guardrail check
    min_year = target.get("ai_academic_routing", {}).get("problem_complexity", {}).get("min_academic_year", 1)
    if student_academic_year < min_year:
        return {
            "status": "guardrail_blocked",
            "is_eligible": False,
            "message": (
                f"Cannot assign problem to Year {student_academic_year} students. This problem requires "
                f"minimum Year {min_year} skills due to chronic structural complexity."
            )
        }

    target["claim_status"] = "CLAIMED"
    target["claimed_by_institution"] = institution_name
    target["claimed_by_team"] = team_name
    target["claimed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "status": "success",
        "action": "PROBLEM_CLAIMED_BY_INSTITUTION",
        "message": f"Successfully allocated '{target['title']}' to {team_name} from {institution_name}.",
        "problem": target
    }
