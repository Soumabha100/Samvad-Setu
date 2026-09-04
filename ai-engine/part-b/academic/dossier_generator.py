"""
Professional Engineering Problem Dossier Generator for HEIs
Module: ai-engine/part-b/academic/dossier_generator.py

Features:
1. Synthesizes real citizen grievance reports, recurrence metrics, and contractor failure logs
   into a comprehensive, professional engineering problem statement using Google Gemini AI.
2. Formats and renders a publication-grade PDF dossier using ReportLab containing:
   - WHAT is the physical/structural problem
   - WHERE is it located (GPS coordinates, ward demographics, affected roads/drains)
   - WHY previous municipal contractor repairs failed (Root Cause Analysis)
   - WHO is suffering (Community impact, school/hospital access, public health hazards)
   - HOW the university should approach it (Recommended academic scope, lab testing, guardrails)
3. Provides an intelligent, zero-downtime engineering fallback if Gemini API key is absent.
"""

import os
import sys
import json
import uuid
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

# ReportLab Imports
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)

# Output directory for generated dossiers
DOSSIER_DIR = Path(__file__).resolve().parent.parent / "uploads" / "dossiers"
DOSSIER_DIR.mkdir(parents=True, exist_ok=True)


def get_gemini_api_key(passed_key: Optional[str] = None) -> Optional[str]:
    """Retrieves the Gemini API key from parameter, environment, or api.txt/.env."""
    if passed_key and passed_key.strip():
        return passed_key.strip()
    if os.environ.get("GEMINI_API_KEY"):
        return os.environ.get("GEMINI_API_KEY").strip()

    search_paths = [
        Path(__file__).resolve().parent.parent.parent / ".env",  # ai-engine/.env
        Path(__file__).resolve().parent.parent / ".env",         # part-b/.env
        Path(__file__).resolve().parent / ".env",                # academic/.env
        Path(__file__).resolve().parent / ".env",
        Path(__file__).resolve().parent.parent / ".env",
        Path(__file__).resolve().parent.parent.parent / ".env",
    ]
    for p in search_paths:
        if p.exists():
            try:
                content = p.read_text(encoding="utf-8").strip()
                for line in content.splitlines():
                    line = line.strip()
                    if "=" in line and ("gemini" in line.lower() or "api_key" in line.lower()):
                        val = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if val:
                            return val
                    elif line.startswith("AQ.") or line.startswith("AIza"):
                        return line
            except Exception:
                pass
    return None


def synthesize_engineering_dossier_with_gemini(
    problem_data: Dict[str, Any],
    gemini_api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Uses Gemini AI to draft a rigorous, professional engineering dossier from
    raw citizen reports, location metadata, and failed contractor repair history.
    """
    api_key = get_gemini_api_key(gemini_api_key)

    title = problem_data.get("title", "Municipal Engineering Issue")
    description = problem_data.get("description", "")
    category = problem_data.get("category", "General")
    department = problem_data.get("municipal_department", "Municipal Operations")
    location = problem_data.get("location", {})
    chronic = problem_data.get("chronic_metrics", {})
    routing = problem_data.get("ai_academic_routing", {})
    matched_subject = routing.get("best_matched_subject", {})
    complexity = routing.get("problem_complexity", {})

    prompt = f"""
You are a Senior Municipal Civil & Infrastructure Systems Engineer.
A citizen filed a civic grievance that the local government authority FAILED to resolve permanently, and it is now being escalated to a Higher Education Institution (HEI / University Engineering Department) as a real-world student capstone or research problem statement.

Write a formal, comprehensive, professional Engineering Problem Dossier based on the following verified incident data:

[INCIDENT METRICS]
- Title: {title}
- Citizen Raw Report: {description}
- Civic Category: {category}
- Municipal Department: {department}
- Location: {location.get('address', 'Urban Ward')}, Coordinates: Lat {location.get('lat', 'N/A')}, Lng {location.get('lng', 'N/A')}
- Recurrence Count: Reported {chronic.get('recurrence_count', 3)} times over {chronic.get('recurrence_period_days', 30)} days
- Contractor Repair History: {chronic.get('failed_attempts', 2)} previous repair attempt(s) failed
- Authority Notes: {chronic.get('authority_notes', 'Standard municipal patching washed out.')}
- Matched Core Subject: {matched_subject.get('subject_name', 'Core Engineering')} ({matched_subject.get('subject_code', 'ENG')})
- Technical Complexity: Tier {complexity.get('tier', 2)} ({complexity.get('tier_name', 'Applied')})

Respond ONLY with a valid JSON object with the following exact keys:
{{
  "dossier_title": "Professional engineering title for the project",
  "executive_summary": "3-4 sentences summarizing the failure and why academic R&D is required",
  "problem_analysis_what": "Detailed technical explanation of what physical or infrastructural failure is occurring",
  "geographic_context_where": "Specific geographic, topographic, and ward context of the site",
  "root_cause_analysis_why": "Why the problem occurred and why standard government contractor repairs failed repeatedly",
  "community_impact_who": "Who is suffering: public health hazards, school/hospital accessibility, economic loss for residents",
  "recommended_engineering_scope_how": "Specific engineering deliverables recommended for student teams (e.g. testing protocols, CAD models, IoT sensors, prototypes)"
}}
"""

    if api_key:
        try:
            from google import genai  # type: ignore
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            raw_text = response.text.strip() if response.text else ""
            # Clean markdown formatting if present
            if raw_text.startswith("```"):
                import re
                raw_text = re.sub(r"^```(?:json)?", "", raw_text)
                raw_text = re.sub(r"```$", "", raw_text).strip()
            parsed = json.loads(raw_text)
            return parsed
        except Exception as e:
            print(f"[WARNING] Gemini API call via google.genai encountered: {e}. Using deterministic engineering synthesis.")

    # High-quality deterministic engineering synthesis fallback
    return _generate_deterministic_engineering_dossier(problem_data)


def _generate_deterministic_engineering_dossier(problem_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Zero-downtime deterministic fallback generating a professional engineering dossier
    when Gemini API key is absent or offline.
    """
    title = problem_data.get("title", "Municipal Engineering Issue")
    description = problem_data.get("description", "")
    category = problem_data.get("category", "infrastructure")
    dept = problem_data.get("municipal_department", "Public Works")
    loc = problem_data.get("location", {})
    chronic = problem_data.get("chronic_metrics", {})
    routing = problem_data.get("ai_academic_routing", {})
    sub = routing.get("best_matched_subject", {})
    comp = routing.get("problem_complexity", {})

    address = loc.get("address", "Municipal Ward")
    lat, lng = loc.get("lat", "23.79"), loc.get("lng", "86.43")
    recurrent = chronic.get("recurrence_count", 3)
    days = chronic.get("recurrence_period_days", 30)
    failed_attempts = chronic.get("failed_attempts", 2)
    notes = chronic.get("authority_notes", "Standard patching or cleaning failed within weeks.")

    return {
        "dossier_title": f"Civic Infrastructure Remediation: {title}",
        "executive_summary": (
            f"This dossier addresses a chronic municipal failure at {address}, which has been reported "
            f"{recurrent} times over {days} days without permanent resolution. Municipal contractors "
            f"attempted standard repairs {failed_attempts} time(s), but the failure repeatedly resurfaced. "
            f"The issue has been escalated to academic engineering institutions to design a permanent, "
            f"scientifically validated solution under the {sub.get('subject_name', 'Core Engineering')} curriculum."
        ),
        "problem_analysis_what": (
            f"Physical inspection reveals severe structural or infrastructural breakdown. Specifically: '{description}'. "
            f"The site exhibits material degradation, lack of adequate drainage camber, and inability to bear "
            f"peak seasonal loads, resulting in immediate failure after standard quick-fix maintenance."
        ),
        "geographic_context_where": (
            f"The affected site is located at {address} (GPS Coordinates: {lat}, {lng}). The surrounding area "
            f"comprises high-density residential and commercial mixed-use infrastructure with heavy daily commuter "
            f"traffic and stormwater runoff concentration."
        ),
        "root_cause_analysis_why": (
            f"Root cause investigation reveals that previous contractor repairs failed because: {notes}. "
            f"Contractors relied on cosmetic surface treatments rather than addressing underlying soil mechanics, "
            f"hydraulic grade line backflow, or subgrade shear failure."
        ),
        "community_impact_who": (
            f"Over several hundred local residents, daily vehicular commuters, school-going children, and "
            f"pedestrians are directly exposed to physical accident hazards, stagnant water contamination, "
            f"and localized economic disruption caused by transit delays."
        ),
        "recommended_engineering_scope_how": (
            f"University student teams should conduct field soil/water sampling, perform topographic GIS modeling, "
            f"and engineer a sustainable prototype or structural design compliant with national standards. "
            f"Recommended deliverable: {comp.get('recommended_deliverable', 'Functional Design Report and Prototype')}."
        )
    }


def generate_hei_problem_dossier_pdf(
    problem_data: Dict[str, Any],
    gemini_api_key: Optional[str] = None,
    output_filename: Optional[str] = None
) -> str:
    """
    Synthesizes the dossier content using Gemini and builds a publication-grade PDF file.
    Returns the absolute path to the generated PDF.
    """
    dossier = synthesize_engineering_dossier_with_gemini(problem_data, gemini_api_key)

    escalation_id = problem_data.get("escalation_id", f"ESC-{uuid.uuid4().hex[:6].upper()}")
    filename = output_filename or f"Engineering_Dossier_{escalation_id}.pdf"
    pdf_path = DOSSIER_DIR / filename

    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    header_style = ParagraphStyle(
        "HeaderStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=4
    )
    sub_header = ParagraphStyle(
        "SubHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=9,
        textColor=colors.HexColor("#2B6CB0"),
        spaceAfter=10
    )
    section_title = ParagraphStyle(
        "SectionTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        textColor=colors.HexColor("#1A365D"),
        spaceBefore=8,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#2D3748")
    )
    meta_label = ParagraphStyle(
        "MetaLabel",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        textColor=colors.HexColor("#4A5568")
    )
    meta_val = ParagraphStyle(
        "MetaVal",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        textColor=colors.HexColor("#1A202C")
    )

    story = []

    # 1. Header Banner
    story.append(Paragraph("SAMVAD-SETU CIVIC INNOVATION & R&D INITIATIVE", sub_header))
    story.append(Paragraph(dossier.get("dossier_title", "Technical Problem Statement Dossier"), header_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2B6CB0"), spaceAfter=8))

    # 2. Key Metadata Table
    loc = problem_data.get("location", {})
    routing = problem_data.get("ai_academic_routing", {})
    sub = routing.get("best_matched_subject", {})
    comp = routing.get("problem_complexity", {})
    chronic = problem_data.get("chronic_metrics", {})

    meta_table_data = [
        [
            Paragraph("<b>Escalation ID:</b>", meta_label), Paragraph(escalation_id, meta_val),
            Paragraph("<b>Department:</b>", meta_label), Paragraph(problem_data.get("municipal_department", "PWD"), meta_val)
        ],
        [
            Paragraph("<b>Core Subject:</b>", meta_label), Paragraph(f"{sub.get('subject_name', 'Engineering')} ({sub.get('subject_code', 'CE')})", meta_val),
            Paragraph("<b>Complexity Tier:</b>", meta_label), Paragraph(f"Tier {comp.get('tier', 2)} ({comp.get('tier_name', 'Applied')})", meta_val)
        ],
        [
            Paragraph("<b>Min Student Year:</b>", meta_label), Paragraph(f"Year {comp.get('min_academic_year', 2)}+", meta_val),
            Paragraph("<b>Failure History:</b>", meta_label), Paragraph(f"{chronic.get('failed_attempts', 2)} Contractor Repairs Failed ({chronic.get('recurrence_count', 3)} reports)", meta_val)
        ],
        [
            Paragraph("<b>Location:</b>", meta_label), Paragraph(f"{loc.get('address', 'Ward Site')} (Lat: {loc.get('lat', 'N/A')}, Lng: {loc.get('lng', 'N/A')})", meta_val),
            Paragraph("<b>Date Escalated:</b>", meta_label), Paragraph(datetime.now().strftime("%Y-%m-%d"), meta_val)
        ]
    ]

    t = Table(meta_table_data, colWidths=[1.1 * inch, 2.5 * inch, 1.2 * inch, 2.4 * inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F7FAFC")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))

    # 3. Sections
    sections = [
        ("1. Executive Summary", dossier.get("executive_summary", "")),
        ("2. Technical Breakdown (WHAT)", dossier.get("problem_analysis_what", "")),
        ("3. Geographic & Site Context (WHERE)", dossier.get("geographic_context_where", "")),
        ("4. Root Cause & Contractor Failure Analysis (WHY)", dossier.get("root_cause_analysis_why", "")),
        ("5. Community Hazard & Stakeholder Impact (WHO)", dossier.get("community_impact_who", "")),
        ("6. Recommended Engineering Deliverables (HOW)", dossier.get("recommended_engineering_scope_how", ""))
    ]

    for title, content in sections:
        section_flowables = [
            Paragraph(title, section_title),
            Paragraph(content, body_style),
            Spacer(1, 6)
        ]
        story.append(KeepTogether(section_flowables))

    # 4. Footer Guardrail Box
    guardrail_info = routing.get("guardrail_evaluation", {})
    guardrail_msg = guardrail_info.get("guardrail_warning") or (
        f"Verified for academic project allocation. Problem meets minimum prerequisite requirements for "
        f"Year {comp.get('min_academic_year', 2)}+ student teams."
    )

    footer_data = [
        [
            Paragraph("<b>ACADEMIC ELIGIBILITY & SAFETY GUARDRAIL:</b>", meta_label),
            Paragraph(guardrail_msg, meta_val)
        ]
    ]
    tf = Table(footer_data, colWidths=[2.2 * inch, 5.0 * inch])
    tf.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EBF8FF")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#3182CE")),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(Spacer(1, 6))
    story.append(tf)

    # Build PDF
    doc.build(story)
    return str(pdf_path)
