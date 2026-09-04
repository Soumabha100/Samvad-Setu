"""
Academic Engine Package for Samvad-Setu Part B:
- Institutions Directory & AISHE Master Data
- 4-Tier Problem Complexity & Prerequisite Evaluator
- Syllabus Parser, Core Subject Matcher & Academic Year Guardrail
"""

from .institutions_data import search_institutions, get_institution_by_id, INDIAN_INSTITUTIONS_MASTER
# pyrefly: ignore [missing-import]
from .complexity_scorer import evaluate_problem_complexity, ComplexityTier, ComplexityResult
# pyrefly: ignore [missing-import]
from .syllabus_engine import SyllabusMatcher, SyllabusSubject, SyllabusCurriculum
# pyrefly: ignore [missing-import]
from .sample_syllabi import AICTE_CIVIL_ENGINEERING, AICTE_COMPUTER_SCIENCE, AICTE_ENVIRONMENTAL_ENGG, SAMPLE_SYLLABI
from .escalation_engine import (
    evaluate_escalation_eligibility,
    register_chronic_problem_statement,
    get_chronic_problems,
    claim_chronic_problem,
    CHRONIC_PROBLEMS_POOL
)
from .dossier_generator import (
    generate_hei_problem_dossier_pdf,
    synthesize_engineering_dossier_with_gemini
)

__all__ = [
    "search_institutions",
    "get_institution_by_id",
    "INDIAN_INSTITUTIONS_MASTER",
    "evaluate_problem_complexity",
    "ComplexityTier",
    "ComplexityResult",
    "SyllabusMatcher",
    "SyllabusSubject",
    "SyllabusCurriculum",
    "AICTE_CIVIL_ENGINEERING",
    "AICTE_COMPUTER_SCIENCE",
    "AICTE_ENVIRONMENTAL_ENGG",
    "SAMPLE_SYLLABI",
    "evaluate_escalation_eligibility",
    "register_chronic_problem_statement",
    "get_chronic_problems",
    "claim_chronic_problem",
    "CHRONIC_PROBLEMS_POOL",
    "generate_hei_problem_dossier_pdf",
    "synthesize_engineering_dossier_with_gemini"
]
