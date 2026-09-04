"""
4-Tier Problem Complexity & Prerequisite Evaluator
Evaluates municipal problem statements and civic complaints to determine:
- Complexity Tier (Tier 1: Foundation to Tier 4: R&D)
- Minimum Recommended Academic Year (Year 1 to Year 4+)
- Prerequisite Knowledge & Safety Scope
- Student Eligibility Guardrail
"""

import re
from typing import Dict, Any, List
from enum import IntEnum


class ComplexityTier(IntEnum):
    TIER_1_FOUNDATION = 1    # 1st Year Undergrad / Diploma
    TIER_2_APPLIED = 2       # 2nd - 3rd Year Core Labs & Software
    TIER_3_ADVANCED = 3      # 4th Year Capstone & Functional Prototypes
    TIER_4_RESEARCH = 4      # PG / PhD / Premier Research Labs (IITs/NITs)


class ComplexityResult:
    def __init__(
        self,
        tier: ComplexityTier,
        complexity_score: float,
        min_academic_year: int,
        target_audience: str,
        prerequisites: List[str],
        recommended_deliverable: str,
        rationale: str
    ):
        self.tier = tier
        self.complexity_score = complexity_score
        self.min_academic_year = min_academic_year
        self.target_audience = target_audience
        self.prerequisites = prerequisites
        self.recommended_deliverable = recommended_deliverable
        self.rationale = rationale

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tier": int(self.tier),
            "tier_name": self.tier.name,
            "complexity_score": round(self.complexity_score, 2),
            "min_academic_year": self.min_academic_year,
            "target_audience": self.target_audience,
            "prerequisites": self.prerequisites,
            "recommended_deliverable": self.recommended_deliverable,
            "rationale": self.rationale
        }


# Lexical and contextual indicators for difficulty levels
TIER_4_INDICATORS = [
    "unsolved", "research", "acoustic tomography", "computational fluid dynamics", "cfd",
    "nanotechnology", "polymer modified", "pyrolysis", "bioremediation of heavy metals",
    "reinforcement learning", "city-wide dynamic simulation", "seismic retrofitting",
    "supercomputer", "structural resonance", "spectrometry", "zero liquid discharge",
    "patentable", "novel material", "deep mathematical model"
]

TIER_3_INDICATORS = [
    "computer vision", "yolo", "edge ai", "iot sensor", "microcontroller", "raspberry pi",
    "arduino", "scada", "telemetry", "automated valve", "real-time detection", "live tracking",
    "machine learning model", "deep learning", "optical flow", "accelerometer", "acoustic sensor",
    "structural health monitoring", "hydrological surge modeling", "automated alert",
    "neural network", "sewer network redesign", "smart drainage automation"
]

TIER_2_INDICATORS = [
    "database", "sql", "dashboard", "gis", "qgis", "map coordinates", "web portal",
    "crud", "water testing", "ph level", "turbidity", "bod", "cod", "leveling",
    "theodolite", "surveying", "road cross-section", "culvert discharge", "pipe flow",
    "cad drawing", "autocad", "manning formula", "route optimization", "spatial query",
    "rest api", "solid waste audit", "air quality index", "aqi monitoring"
]

TIER_1_INDICATORS = [
    "survey", "citizen feedback", "photo", "observe", "measure", "count", "report",
    "awareness", "leaflet", "door-to-door", "solid waste segregation", "cleanliness drive",
    "basic form", "excel", "csv", "simple inspection", "pothole count", "garbage pile photo",
    "street light outage reporting", "drain blockage observation"
]


def evaluate_problem_complexity(text: str, category: str = "", department: str = "") -> ComplexityResult:
    """
    Evaluates a problem statement and civic description to calculate its complexity tier,
    minimum eligible academic year, and prerequisite skills.
    """
    content = f"{text} {category} {department}".lower()

    score_t4 = sum(2.5 for kw in TIER_4_INDICATORS if kw in content)
    score_t3 = sum(1.8 for kw in TIER_3_INDICATORS if kw in content)
    score_t2 = sum(1.2 for kw in TIER_2_INDICATORS if kw in content)
    score_t1 = sum(0.8 for kw in TIER_1_INDICATORS if kw in content)

    # Word count and sentence length heuristic: longer, technical descriptions correlate with complex engineering
    words = re.findall(r'\w+', content)
    word_count = len(words)
    if word_count > 80:
        score_t3 += 0.8
        score_t4 += 0.5
    elif word_count > 40:
        score_t2 += 0.6

    # Specific engineering terminology boosts
    if any(term in content for term in ["sensor", "iot", "algorithm", "automated", "vision", "ai"]):
        score_t3 += 2.0
    if any(term in content for term in ["novel", "unsolved", "experimental", "material science"]):
        score_t4 += 3.0

    # Determine dominant tier
    if score_t4 >= 3.0 or (score_t4 > 1.5 and score_t4 >= score_t3):
        tier = ComplexityTier.TIER_4_RESEARCH
        normalized_score = min(0.98, 0.75 + (score_t4 * 0.05))
        min_year = 4
        target_audience = "M.Tech / PhD Scholars & Premier Tier-1 Research Labs (IITs, IISc, NITs)"
        prerequisites = [
            "Advanced domain research capability",
            "Specialized laboratory instrumentation / High-performance computing",
            "Deep theoretical mathematics and chemical/fluid mechanics"
        ]
        deliverable = "Funded Research Paper, Patent Application, or Municipal Policy Advisory"
        rationale = "Involves open-ended civic engineering R&D, specialized laboratory analysis, or unproven technological methods."

    elif score_t3 >= 2.5 or (score_t3 > score_t2 and score_t3 >= 1.8):
        tier = ComplexityTier.TIER_3_ADVANCED
        normalized_score = min(0.74, 0.50 + (score_t3 * 0.05))
        min_year = 4
        target_audience = "4th-Year Undergraduate Capstone Engineering Teams (B.Tech Final Year)"
        prerequisites = [
            "Microcontroller / Embedded IoT hardware interfacing",
            "Applied Computer Vision or Deep Learning deployment",
            "Core Structural / Hydraulics engineering design standards"
        ]
        deliverable = "Functional Hardware/Software Prototype, Field-Tested Edge Device, or Capstone Thesis"
        rationale = "Requires multi-disciplinary engineering synthesis (hardware, computer vision, or advanced mathematical modeling)."

    elif score_t2 >= 1.5 or (score_t2 > score_t1 and score_t2 >= 1.0):
        tier = ComplexityTier.TIER_2_APPLIED
        normalized_score = min(0.49, 0.26 + (score_t2 * 0.05))
        min_year = 2
        target_audience = "2nd & 3rd Year Engineering Undergraduates (Core Lab & Mini-Projects)"
        prerequisites = [
            "Relational Database / GIS mapping software (PostgreSQL, QGIS)",
            "Standard lab testing protocols (Water quality titration, soil mechanics)",
            "Basic Web/Mobile API development"
        ]
        deliverable = "Interactive Municipal Web Portal, GIS Ward Map, or Standard Engineering Lab Analysis Report"
        rationale = "Suited for standard engineering laboratory projects, database application design, or applied spatial analysis."

    else:
        tier = ComplexityTier.TIER_1_FOUNDATION
        normalized_score = max(0.10, min(0.25, 0.10 + (score_t1 * 0.04)))
        min_year = 1
        target_audience = "1st-Year Engineering Students (All Branches) & Diploma/Polytechnic Students"
        prerequisites = [
            "Basic computer literacy (Spreadsheets, forms, photographic documentation)",
            "Foundational environmental & civic awareness",
            "Community survey and communication skills"
        ]
        deliverable = "Field Survey Audit, Photographic Documentation Catalog, or Citizen Awareness Campaign"
        rationale = "Focuses on foundational data collection, citizen sentiment, and civic field observations without requiring senior engineering tools."

    return ComplexityResult(
        tier=tier,
        complexity_score=normalized_score,
        min_academic_year=min_year,
        target_audience=target_audience,
        prerequisites=prerequisites,
        recommended_deliverable=deliverable,
        rationale=rationale
    )
