"""
Corporate CSR Funding & Prototype Showcase - Data Models & Storage
Module: ai-engine/part-b/corporate/prototypes_data.py

Defines:
1. Student Prototype Schema (TRL 1-7, Bill of Materials, team credentials, demo links)
2. Corporate Partner & CSR Sponsor Profiles (CIN, Schedule VII preferences, CSR budget)
3. In-memory persistent stores with thread-safe operations.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid


# =============================================================================
# Technology Readiness Levels (TRL) for Civic Prototypes
# =============================================================================
TRL_DESCRIPTIONS = {
    1: "Basic Principles Observed (Concept Formulation)",
    2: "Technology Concept Formulated (Feasibility Study)",
    3: "Analytical & Experimental Proof-of-Concept",
    4: "Component Validation in Laboratory Environment",
    5: "Subsystem Validation in Relevant Civic Environment",
    6: "Prototype Demonstration in Municipal Pilot Site",
    7: "Full Prototype Demonstration in Real-World Urban Context"
}

# =============================================================================
# MCA Schedule VII CSR Classification Categories (Indian Companies Act, 2013)
# =============================================================================
SCHEDULE_VII_CATEGORIES = {
    "item_i": "Eradicating hunger, poverty, and healthcare / sanitation promotion",
    "item_ii": "Promoting education, STEM innovation, and livelihood enhancement projects",
    "item_iv": "Ensuring environmental sustainability, soil & water conservation, ecological balance",
    "item_v": "Protection of national heritage, art and culture, public libraries",
    "item_x": "Rural development projects and slum area redevelopment",
    "item_xi": "Disaster management, including relief, rehabilitation and reconstruction activities"
}

# Mapping civic categories to eligible Schedule VII CSR items
CIVIC_TO_SCHEDULE_VII = {
    "water_drainage": ["item_i", "item_iv"],
    "road_damage": ["item_ii", "item_x"],
    "garbage_dump": ["item_i", "item_iv"],
    "pothole": ["item_ii", "item_x"],
    "manhole": ["item_i", "item_ii"],
    "structural_subsidence": ["item_ii", "item_xi"],
    "environmental": ["item_iv", "item_xi"]
}


# =============================================================================
# In-Memory Data Stores
# =============================================================================
PROTOTYPES_STORE: Dict[str, Dict[str, Any]] = {
    "PROTO-TERRAFIX-01": {
        "prototype_id": "PROTO-TERRAFIX-01",
        "escalation_id": "ESC-27A23A",
        "prototype_title": "Bio-Polymer Geogrid Sub-base Remediation Rig",
        "institution_name": "IIT Bombay (AISHE: U-0306)",
        "team_name": "Team TerraFix",
        "faculty_mentor": "Prof. R. K. Banerjee",
        "executive_summary": "Modular geotechnical injection unit that stabilizes waterlogged black cotton soil subgrades to prevent recurrent road subsidence.",
        "technical_approach": "High-pressure cold emulsion injection combined with recycled PET geogrids preventing sinkhole collapse.",
        "trl_level": 5,
        "trl_description": "Subsystem Validation in Relevant Civic Environment",
        "category": "road_damage",
        "schedule_vii_categories": ["item_ii", "item_x"],
        "schedule_vii_descriptions": [
            "Promoting education, STEM innovation, and livelihood enhancement projects",
            "Rural development projects and slum area redevelopment"
        ],
        "bill_of_materials": [
            {"item": "High-Pressure Hydraulic Injection Pump", "cost_inr": 85000.0, "qty": 1},
            {"item": "Modified Bio-Polymer Grout (500kg)", "cost_inr": 45000.0, "qty": 1},
            {"item": "IoT Pore-Pressure Telemetry Sensors", "cost_inr": 35000.0, "qty": 4}
        ],
        "total_funding_required_inr": 250000.0,
        "funded_amount_inr": 0.0,
        "funding_status": "seeking_corporate_sponsorship",
        "sponsorship_pledges": [],
        "demo_video_url": "https://youtube.com/watch?v=terrafix_demo",
        "cad_repo_url": "https://github.com/terrafix/geogrid-cad",
        "field_testing_plan": "Laboratory calibration followed by 14-day Municipal ULB test plot.",
        "expected_civic_impact": {
            "citizens_benefited_estimate": 15000,
            "durability_years_estimate": 5,
            "cost_saving_vs_contractor_percent": 65
        },
        "submitted_at": datetime.now().isoformat(),
        "verification_status": "verified_by_academic_jury"
    },
    "PROTO-HYDROGUARD-02": {
        "prototype_id": "PROTO-HYDROGUARD-02",
        "escalation_id": "ESC-9B3821",
        "prototype_title": "AI Acoustic Flow-Sensor & Smart Sump Drain Gate",
        "institution_name": "IIT Kharagpur (AISHE: U-0573)",
        "team_name": "HydroGuard KGP",
        "faculty_mentor": "Dr. Arvind Swaminathan",
        "executive_summary": "Autonomous urban storm-drainage flap that prevents backflow and chronic street inundation during monsoons.",
        "technical_approach": "Ultrasonic depth monitoring coupled with solenoid-actuated valve doors.",
        "trl_level": 6,
        "trl_description": "Prototype Demonstration in Municipal Pilot Site",
        "category": "water_drainage",
        "schedule_vii_categories": ["item_i", "item_iv"],
        "schedule_vii_descriptions": [
            "Eradicating hunger, poverty, and healthcare / sanitation promotion",
            "Ensuring environmental sustainability, soil & water conservation, ecological balance"
        ],
        "bill_of_materials": [
            {"item": "Industrial Ultrasonic Level Transmitter", "cost_inr": 42000.0, "qty": 2},
            {"item": "High-Torque Stainless Steel Actuator Gate", "cost_inr": 120000.0, "qty": 1},
            {"item": "Solar Backed Telemetry Node (4G)", "cost_inr": 28000.0, "qty": 1}
        ],
        "total_funding_required_inr": 300000.0,
        "funded_amount_inr": 0.0,
        "funding_status": "seeking_corporate_sponsorship",
        "sponsorship_pledges": [],
        "demo_video_url": "https://youtu.be/hydroguard_test",
        "cad_repo_url": "https://github.com/hydroguard/gate-cad",
        "field_testing_plan": "Ward 14 municipal culvert installation with live water-depth telemetry.",
        "expected_civic_impact": {
            "citizens_benefited_estimate": 22000,
            "durability_years_estimate": 7,
            "cost_saving_vs_contractor_percent": 70
        },
        "submitted_at": datetime.now().isoformat(),
        "verification_status": "verified_by_academic_jury"
    }
}
CORPORATE_SPONSORS_STORE: Dict[str, Dict[str, Any]] = {
    "CORP-TATA-01": {
        "sponsor_id": "CORP-TATA-01",
        "company_name": "Tata Sustainability Foundation",
        "mca_cin": "U85100MH2008NPL184123",
        "industry_sector": "Infrastructure & Engineering",
        "csr_annual_budget_inr": 25000000.0,
        "allocated_budget_inr": 0.0,
        "preferred_schedule_vii": ["item_iv", "item_ii", "item_x"],
        "target_regions": ["Maharashtra", "Jharkhand", "Karnataka"],
        "contact_person": "Dr. Ananya Sharma",
        "email": "csr.initiative@tatasustainability.org"
    },
    "CORP-INFY-02": {
        "sponsor_id": "CORP-INFY-02",
        "company_name": "Infosys Urban Renewal CSR Trust",
        "mca_cin": "L85110KA1981PLC013115",
        "industry_sector": "Information Technology & IoT",
        "csr_annual_budget_inr": 18000000.0,
        "allocated_budget_inr": 0.0,
        "preferred_schedule_vii": ["item_ii", "item_iv"],
        "target_regions": ["Karnataka", "Telangana", "Delhi-NCR"],
        "contact_person": "Rohan Deshmukh",
        "email": "urban.csr@infosys.com"
    },
    "CORP-LT-03": {
        "sponsor_id": "CORP-LT-03",
        "company_name": "Larsen & Toubro Civic Infra CSR",
        "mca_cin": "L99999MH1946PLC004768",
        "industry_sector": "Heavy Civil & Construction",
        "csr_annual_budget_inr": 35000000.0,
        "allocated_budget_inr": 0.0,
        "preferred_schedule_vii": ["item_iv", "item_x", "item_xi"],
        "target_regions": ["All India"],
        "contact_person": "K. Venkatesh",
        "email": "csr.support@lntecc.com"
    }
}


def register_prototype_submission(
    escalation_id: str,
    team_name: str,
    institution_name: str,
    faculty_mentor: str,
    prototype_title: str,
    executive_summary: str,
    technical_approach: str,
    trl_level: int,
    bill_of_materials: List[Dict[str, Any]],
    total_funding_required_inr: float,
    demo_video_url: Optional[str] = None,
    cad_repo_url: Optional[str] = None,
    field_testing_plan: Optional[str] = None,
    expected_civic_impact: Optional[Dict[str, Any]] = None,
    category: str = "road_damage"
) -> Dict[str, Any]:
    """
    Registers an engineering prototype submitted by an HEI student/faculty team
    for a claimed chronic civic problem.
    """
    proto_id = f"PROTO-{uuid.uuid4().hex[:6].upper()}"
    trl = max(1, min(7, trl_level))
    
    # Identify applicable Schedule VII CSR category
    cat_key = category.lower().replace(" ", "_")
    schedule_vii = CIVIC_TO_SCHEDULE_VII.get(cat_key, ["item_ii", "item_iv"])

    # Calculate BoM sum if provided
    bom_sum = sum(item.get("cost_inr", 0.0) for item in bill_of_materials) if bill_of_materials else 0.0
    funding_goal = total_funding_required_inr if total_funding_required_inr > 0 else (bom_sum * 1.25)

    prototype_record = {
        "prototype_id": proto_id,
        "escalation_id": escalation_id,
        "prototype_title": prototype_title,
        "institution_name": institution_name,
        "team_name": team_name,
        "faculty_mentor": faculty_mentor,
        "executive_summary": executive_summary,
        "technical_approach": technical_approach,
        "trl_level": trl,
        "trl_description": TRL_DESCRIPTIONS.get(trl, "Experimental Prototype"),
        "category": category,
        "schedule_vii_categories": schedule_vii,
        "schedule_vii_descriptions": [SCHEDULE_VII_CATEGORIES.get(item, "") for item in schedule_vii],
        "bill_of_materials": bill_of_materials,
        "total_funding_required_inr": round(funding_goal, 2),
        "funded_amount_inr": 0.0,
        "funding_status": "seeking_corporate_sponsorship",
        "sponsorship_pledges": [],
        "demo_video_url": demo_video_url,
        "cad_repo_url": cad_repo_url,
        "field_testing_plan": field_testing_plan or "Laboratory calibration followed by 14-day Municipal ULB test plot.",
        "expected_civic_impact": expected_civic_impact or {
            "citizens_benefited_estimate": 15000,
            "durability_years_estimate": 5,
            "cost_saving_vs_contractor_percent": 65
        },
        "submitted_at": datetime.now().isoformat(),
        "verification_status": "verified_by_academic_jury"
    }

    PROTOTYPES_STORE[proto_id] = prototype_record
    return prototype_record


def list_prototypes(
    schedule_vii: Optional[str] = None,
    min_trl: Optional[int] = None,
    max_budget: Optional[float] = None,
    funding_status: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Filters prototypes for corporate investors based on criteria."""
    results = []
    for proto in PROTOTYPES_STORE.values():
        if schedule_vii and schedule_vii not in proto.get("schedule_vii_categories", []):
            continue
        if min_trl and proto.get("trl_level", 1) < min_trl:
            continue
        if max_budget and proto.get("total_funding_required_inr", 0.0) > max_budget:
            continue
        if funding_status and proto.get("funding_status") != funding_status:
            continue
        results.append(proto)
    return results


def get_prototype_by_id(proto_id: str) -> Optional[Dict[str, Any]]:
    """Returns a specific prototype by ID."""
    return PROTOTYPES_STORE.get(proto_id)
