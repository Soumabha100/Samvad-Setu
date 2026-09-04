"""
Syllabus Engine & Guardrail Matcher
Indexes curriculum subjects, computes semantic similarity with municipal problems,
maps to Core Department Subjects, and enforces the Student Year Safety Guardrail.
"""

from typing import List, Dict, Any, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# pyrefly: ignore [missing-import]
import numpy as np

from .complexity_scorer import evaluate_problem_complexity, ComplexityTier, ComplexityResult
from .sample_syllabi import SAMPLE_SYLLABI, AICTE_CIVIL_ENGINEERING


class SyllabusSubject:
    def __init__(
        self,
        subject_code: str,
        subject_name: str,
        academic_year: int,
        semester: int,
        is_core: bool,
        complexity_ceiling: int,
        course_outcomes: List[str],
        units: List[str]
    ):
        self.subject_code = subject_code
        self.subject_name = subject_name
        self.academic_year = academic_year
        self.semester = semester
        self.is_core = is_core
        self.complexity_ceiling = complexity_ceiling
        self.course_outcomes = course_outcomes
        self.units = units

    def get_searchable_text(self) -> str:
        # Boost subject name and course outcomes so core domain concepts dominate
        name_boost = f"{self.subject_name} " * 4
        outcomes_boost = (" ".join(self.course_outcomes) + " ") * 2
        units_text = " ".join(self.units)
        return f"{self.subject_code} {name_boost} {outcomes_boost} {units_text}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "subject_code": self.subject_code,
            "subject_name": self.subject_name,
            "academic_year": self.academic_year,
            "semester": self.semester,
            "is_core": self.is_core,
            "complexity_ceiling": self.complexity_ceiling,
            "course_outcomes": self.course_outcomes,
            "units": self.units
        }


class SyllabusCurriculum:
    def __init__(self, department: str, degree: str, subjects: List[SyllabusSubject]):
        self.department = department
        self.degree = degree
        self.subjects = subjects

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SyllabusCurriculum":
        subjects = [
            SyllabusSubject(
                subject_code=s.get("subject_code", "GEN-100"),
                subject_name=s.get("subject_name", "General Course"),
                academic_year=s.get("academic_year", 1),
                semester=s.get("semester", 1),
                is_core=s.get("is_core", True),
                complexity_ceiling=s.get("complexity_ceiling", 2),
                course_outcomes=s.get("course_outcomes", []),
                units=s.get("units", [])
            )
            for s in data.get("subjects", [])
        ]
        return cls(
            department=data.get("department", "Engineering"),
            degree=data.get("degree", "B.Tech"),
            subjects=subjects
        )


CATEGORY_DOMAIN_EXPANSION = {
    "road_damage": "road damage highway transportation pavement asphalt pothole cracking road bituminous",
    "drainage": "drainage sewer sewerage wastewater manhole overflow stormwater pipeline",
    "garbage": "garbage solid waste sanitation refuse landfill recycling composting",
    "waterlogging": "waterlogging stormwater flood drainage open channel runoff rainwater",
    "traffic_light": "traffic signal intersection vehicle congestion road transport",
    "stray_animal": "animal public safety civic health municipal"
}


class SyllabusMatcher:
    def __init__(self, curriculum: Optional[SyllabusCurriculum] = None):
        if curriculum is None:
            curriculum = SyllabusCurriculum.from_dict(AICTE_CIVIL_ENGINEERING)
        self.curriculum = curriculum
        self.vectorizer: Optional[TfidfVectorizer] = None
        self.subject_vectors = None
        self._build_index()

    def _build_index(self):
        """Builds TF-IDF vector representations of all subjects in the syllabus."""
        if not self.curriculum.subjects:
            return

        corpus = [s.get_searchable_text() for s in self.curriculum.subjects]
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True,
            max_features=3000
        )
        self.subject_vectors = self.vectorizer.fit_transform(corpus)

    def update_curriculum(self, curriculum: SyllabusCurriculum):
        """Updates the active curriculum and re-indexes."""
        self.curriculum = curriculum
        self._build_index()

    def match_problem(
        self,
        problem_text: str,
        category: str = "",
        department_hint: str = "",
        target_student_year: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Matches a problem statement against the curriculum subjects, assigns to the core
        department subject, and enforces the Student Year Guardrail.
        """
        # Step 1: Evaluate problem complexity
        complexity = evaluate_problem_complexity(problem_text, category, department_hint)

        if not self.curriculum.subjects or self.vectorizer is None or self.subject_vectors is None:
            return {
                "status": "error",
                "message": "Syllabus is empty or not indexed.",
                "complexity": complexity.to_dict()
            }

        # Step 2: Compute semantic vector similarity
        cat_expanded = CATEGORY_DOMAIN_EXPANSION.get(category.lower().strip(), category)
        query_text = f"{problem_text} {cat_expanded} {department_hint}"
        query_vec = self.vectorizer.transform([query_text])
        similarities = cosine_similarity(query_vec, self.subject_vectors)[0]

        # Step 3: Score subjects with core-subject boost
        scored_subjects = []
        for idx, subject in enumerate(self.curriculum.subjects):
            base_sim = float(similarities[idx])
            
            # Core subjects receive priority over general electives
            core_multiplier = 1.20 if subject.is_core else 1.0
            
            # Year alignment heuristic if target year is specified
            year_multiplier = 1.0
            if target_student_year is not None:
                if subject.academic_year == target_student_year:
                    year_multiplier = 1.15

            final_score = base_sim * core_multiplier * year_multiplier

            scored_subjects.append({
                "subject": subject,
                "base_similarity": base_sim,
                "composite_score": final_score
            })

        # Sort by composite score descending
        scored_subjects.sort(key=lambda x: x["composite_score"], reverse=True)
        top_match = scored_subjects[0] if scored_subjects else None

        if not top_match:
            return {
                "status": "no_match",
                "message": "No matching subject found in the syllabus.",
                "complexity": complexity.to_dict()
            }

        matched_subject: SyllabusSubject = top_match["subject"]
        raw_sim = top_match["base_similarity"]

        # Step 4: Academic Year Guardrail Check
        # Rule: A student can only be assigned a problem if their academic year >= min_academic_year
        is_eligible = True
        guardrail_status = "APPROVED"
        guardrail_warning = None

        check_year = target_student_year if target_student_year is not None else matched_subject.academic_year

        if complexity.min_academic_year > check_year:
            is_eligible = False
            guardrail_status = "BLOCKED_EXCEEDS_STUDENT_YEAR"
            guardrail_warning = (
                f"GUARDRAIL TRIGGERED: Problem complexity is classified as Tier {int(complexity.tier)} "
                f"({complexity.tier.name}), requiring Year {complexity.min_academic_year}+ skills. "
                f"It is strictly BLOCKED from Year {check_year} students to prevent assigning "
                f"unsolvable/open-ended research problems to junior students. "
                f"Recommended escalation: {complexity.target_audience}."
            )
        elif check_year > complexity.min_academic_year + 1 and int(complexity.tier) == 1:
            # Informational notice: Problem is very easy for a senior student
            guardrail_status = "APPROVED_FOUNDATIONAL"
            guardrail_warning = (
                f"NOTICE: This is a Tier 1 (Foundation) problem. While Year {check_year} students can "
                f"execute it, it is best suited for 1st-year exploratory mini-projects."
            )

        # Build candidate ranked list
        ranked_candidates = []
        for item in scored_subjects[:3]:
            sub: SyllabusSubject = item["subject"]
            ranked_candidates.append({
                "subject_code": sub.subject_code,
                "subject_name": sub.subject_name,
                "academic_year": sub.academic_year,
                "semester": sub.semester,
                "is_core": sub.is_core,
                "similarity_percent": round(item["base_similarity"] * 100, 1),
                "is_suitable_for_target_year": sub.academic_year >= complexity.min_academic_year
            })

        return {
            "status": "success",
            "department": self.curriculum.department,
            "problem_complexity": complexity.to_dict(),
            "guardrail_evaluation": {
                "target_student_year": check_year,
                "is_eligible": is_eligible,
                "guardrail_status": guardrail_status,
                "guardrail_warning": guardrail_warning
            },
            "best_matched_subject": {
                "subject_code": matched_subject.subject_code,
                "subject_name": matched_subject.subject_name,
                "academic_year": matched_subject.academic_year,
                "semester": matched_subject.semester,
                "is_core": matched_subject.is_core,
                "similarity_percent": round(raw_sim * 100, 1),
                "relevant_course_outcomes": matched_subject.course_outcomes[:2],
                "recommended_student_deliverable": complexity.recommended_deliverable
            },
            "candidate_subjects": ranked_candidates
        }
