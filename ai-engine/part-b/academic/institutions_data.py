"""
Indian Institutions Master Directory
Contains curated data of premier and state engineering institutions across India,
including AISHE identifiers, category tiers, and top department specializations.
"""

from typing import List, Dict, Any, Optional

INDIAN_INSTITUTIONS_MASTER: List[Dict[str, Any]] = [
    # ------------------ Tier 1: Premier Research (IITs, IISc, BITS, Top NITs) ------------------
    {
        "id": "inst_iisc_blr",
        "name": "Indian Institute of Science (IISc), Bangalore",
        "short_name": "IISc Bangalore",
        "aishe_code": "U-0220",
        "category": "Tier-1 Premier Research",
        "state": "Karnataka",
        "city": "Bengaluru",
        "nirf_rank_engg": 2,
        "best_departments": [
            {"department": "Civil & Environmental Engineering", "focus": "Urban Hydrology, Soil Mechanics, Water Resources"},
            {"department": "Computer Science & Automation", "focus": "AI/ML, Distributed Systems, IoT Architecture"},
            {"department": "Electrical Communication Engineering", "focus": "Signal Processing, 5G/6G Networks, Sensor Networks"}
        ],
        "research_capacity": "High R&D / Advanced PhD & Capstone Only (Tier 3-4)"
    },
    {
        "id": "inst_iit_b",
        "name": "Indian Institute of Technology (IIT) Bombay",
        "short_name": "IIT Bombay",
        "aishe_code": "U-0306",
        "category": "Tier-1 Premier Research",
        "state": "Maharashtra",
        "city": "Mumbai",
        "nirf_rank_engg": 3,
        "best_departments": [
            {"department": "Civil Engineering", "focus": "Transportation Systems, Geospatial Tech, Structural Integrity"},
            {"department": "Environmental Science and Engineering", "focus": "Municipal Wastewater Remediation, Air Quality Control"},
            {"department": "Computer Science and Engineering", "focus": "Computer Vision, Smart Cities Big Data, Edge AI"}
        ],
        "research_capacity": "High R&D / Advanced PhD & Capstone Only (Tier 3-4)"
    },
    {
        "id": "inst_iit_d",
        "name": "Indian Institute of Technology (IIT) Delhi",
        "short_name": "IIT Delhi",
        "aishe_code": "U-0092",
        "category": "Tier-1 Premier Research",
        "state": "Delhi",
        "city": "New Delhi",
        "nirf_rank_engg": 2,
        "best_departments": [
            {"department": "Civil Engineering", "focus": "Urban Traffic Management, Pavement Materials, Flood Risk Analysis"},
            {"department": "Computer Science & Engineering", "focus": "Cyber-Physical Systems, Autonomous Navigation, NLP"},
            {"department": "Energy Science and Engineering", "focus": "Renewable Microgrids, Waste-to-Energy Systems"}
        ],
        "research_capacity": "High R&D / Advanced PhD & Capstone Only (Tier 3-4)"
    },
    {
        "id": "inst_iit_m",
        "name": "Indian Institute of Technology (IIT) Madras",
        "short_name": "IIT Madras",
        "aishe_code": "U-0456",
        "category": "Tier-1 Premier Research",
        "state": "Tamil Nadu",
        "city": "Chennai",
        "nirf_rank_engg": 1,
        "best_departments": [
            {"department": "Civil Engineering", "focus": "Coastal Hydrology, Sustainable Construction, Road Infrastructure"},
            {"department": "Computer Science and Engineering", "focus": "Sensor Networks, Data Science, AI Systems"},
            {"department": "Ocean & Hydraulic Engineering", "focus": "Urban Drainage, Stormwater Surge Modeling"}
        ],
        "research_capacity": "High R&D / Advanced PhD & Capstone Only (Tier 3-4)"
    },
    {
        "id": "inst_iit_kgp",
        "name": "Indian Institute of Technology (IIT) Kharagpur",
        "short_name": "IIT Kharagpur",
        "aishe_code": "U-0573",
        "category": "Tier-1 Premier Research",
        "state": "West Bengal",
        "city": "Kharagpur",
        "nirf_rank_engg": 5,
        "best_departments": [
            {"department": "Civil Engineering", "focus": "Geotechnical, GIS/Remote Sensing, Municipal Drainage"},
            {"department": "Computer Science & Engineering", "focus": "Deep Learning, Edge Computing, Systems"},
            {"department": "Architecture and Regional Planning", "focus": "Smart City Master Planning, Urban Slum Regeneration"}
        ],
        "research_capacity": "High R&D / Advanced PhD & Capstone Only (Tier 3-4)"
    },
    {
        "id": "inst_iit_r",
        "name": "Indian Institute of Technology (IIT) Roorkee",
        "short_name": "IIT Roorkee",
        "aishe_code": "U-0500",
        "category": "Tier-1 Premier Research",
        "state": "Uttarakhand",
        "city": "Roorkee",
        "nirf_rank_engg": 6,
        "best_departments": [
            {"department": "Civil Engineering", "focus": "Hydrology & Water Resources, Pavement Quality, Seismic Engineering"},
            {"department": "Earthquake Engineering", "focus": "Structural Damage Diagnostics, Early Warning Systems"}
        ],
        "research_capacity": "High R&D / Advanced PhD & Capstone Only (Tier 3-4)"
    },
    {
        "id": "inst_nit_trichy",
        "name": "National Institute of Technology (NIT) Tiruchirappalli",
        "short_name": "NIT Trichy",
        "aishe_code": "U-0467",
        "category": "Tier-1 Premier Research",
        "state": "Tamil Nadu",
        "city": "Tiruchirappalli",
        "nirf_rank_engg": 9,
        "best_departments": [
            {"department": "Civil Engineering", "focus": "Traffic Engineering, Water Treatment, Concrete Technology"},
            {"department": "Computer Applications", "focus": "Distributed Cloud, Mobile Enterprise Solutions"}
        ],
        "research_capacity": "Undergraduate Capstone + PG Research (Tier 2-4)"
    },
    {
        "id": "inst_nit_surathkal",
        "name": "National Institute of Technology Karnataka (NITK) Surathkal",
        "short_name": "NITK Surathkal",
        "aishe_code": "U-0237",
        "category": "Tier-1 Premier Research",
        "state": "Karnataka",
        "city": "Mangalore",
        "nirf_rank_engg": 12,
        "best_departments": [
            {"department": "Water Resources & Ocean Engineering", "focus": "Coastal Runoff, Urban Drainage, Remote Sensing"},
            {"department": "Information Technology", "focus": "Real-time Civic Data Analytics, Blockchain Grievances"}
        ],
        "research_capacity": "Undergraduate Capstone + PG Research (Tier 2-4)"
    },
    {
        "id": "inst_bits_pilani",
        "name": "Birla Institute of Technology and Science (BITS) Pilani",
        "short_name": "BITS Pilani",
        "aishe_code": "U-0391",
        "category": "Tier-1 Premier Research",
        "state": "Rajasthan",
        "city": "Pilani",
        "nirf_rank_engg": 20,
        "best_departments": [
            {"department": "Computer Science", "focus": "Intelligent Software, Autonomous IoT, Cloud Computing"},
            {"department": "Civil Engineering", "focus": "Smart Mobility, Pavement Management Systems"}
        ],
        "research_capacity": "Undergraduate Capstone + PG Research (Tier 2-4)"
    },

    # ------------------ Tier 2: State Technical Universities & Autonomous Colleges ------------------
    {
        "id": "inst_vtu",
        "name": "Visvesvaraya Technological University (VTU)",
        "short_name": "VTU Belagavi",
        "aishe_code": "U-0249",
        "category": "Tier-2 State Technical University",
        "state": "Karnataka",
        "city": "Belagavi",
        "nirf_rank_engg": 52,
        "best_departments": [
            {"department": "Civil Engineering", "focus": "Highway Engineering, Soil Mechanics, Water Supply Systems"},
            {"department": "Computer Science and Engineering", "focus": "Web/Mobile Applications, Database Systems, IoT"},
            {"department": "Environmental Engineering", "focus": "Solid Waste Management, Effluent Treatment"}
        ],
        "research_capacity": "All Undergrad Tiers (Tier 1-3) + M.Tech Capstones"
    },
    {
        "id": "inst_aktu",
        "name": "Dr. A.P.J. Abdul Kalam Technical University (AKTU)",
        "short_name": "AKTU Lucknow",
        "aishe_code": "U-0508",
        "category": "Tier-2 State Technical University",
        "state": "Uttar Pradesh",
        "city": "Lucknow",
        "nirf_rank_engg": 70,
        "best_departments": [
            {"department": "Civil Engineering", "focus": "Rural & Urban Roads, Municipal Sanitation, Surveying"},
            {"department": "Computer Science and Information Tech", "focus": "Citizen Portals, Database Applications, GIS Web Apps"}
        ],
        "research_capacity": "All Undergrad Tiers (Tier 1-3) + Final Year Projects"
    },
    {
        "id": "inst_anna_univ",
        "name": "Anna University, CEG Campus",
        "short_name": "Anna University",
        "aishe_code": "U-0439",
        "category": "Tier-2 State Technical University",
        "state": "Tamil Nadu",
        "city": "Chennai",
        "nirf_rank_engg": 13,
        "best_departments": [
            {"department": "Civil Engineering", "focus": "Traffic & Highway Planning, Structural Health, Wastewater Systems"},
            {"department": "Centre for Water Resources", "focus": "Urban Waterlogging, Stormwater Network Optimization"},
            {"department": "Information Science and Tech", "focus": "Location Intelligence, Citizen Response Platforms"}
        ],
        "research_capacity": "All Undergrad Tiers (Tier 1-3) + Research"
    },
    {
        "id": "inst_sppu",
        "name": "Savitribai Phule Pune University (SPPU)",
        "short_name": "SPPU Pune",
        "aishe_code": "U-0329",
        "category": "Tier-2 State Technical University",
        "state": "Maharashtra",
        "city": "Pune",
        "nirf_rank_engg": 35,
        "best_departments": [
            {"department": "Civil Engineering", "focus": "Smart Transport, Municipal Infrastructure, Environmental Auditing"},
            {"department": "Computer Engineering", "focus": "Full Stack Dev, Civic GIS, Machine Learning"}
        ],
        "research_capacity": "All Undergrad Tiers (Tier 1-3) + Capstone"
    },
    {
        "id": "inst_makaut",
        "name": "Maulana Abul Kalam Azad University of Technology (MAKAUT)",
        "short_name": "MAKAUT WB",
        "aishe_code": "U-0584",
        "category": "Tier-2 State Technical University",
        "state": "West Bengal",
        "city": "Kolkata",
        "nirf_rank_engg": 85,
        "best_departments": [
            {"department": "Civil Engineering", "focus": "Drainage Design, Geotechnical Testing, Urban Roadways"},
            {"department": "Information Technology", "focus": "Public Service Portals, Cloud Computing"}
        ],
        "research_capacity": "All Undergrad Tiers (Tier 1-3)"
    },
    {
        "id": "inst_bit_sindri",
        "name": "Birsa Institute of Technology (BIT) Sindri",
        "short_name": "BIT Sindri",
        "aishe_code": "C-44243",
        "category": "Tier-2 State Autonomous College",
        "state": "Jharkhand",
        "city": "Dhanbad",
        "nirf_rank_engg": 150,
        "best_departments": [
            {"department": "Civil Engineering", "focus": "Mining belt infrastructure, PWD road audits, Water distribution"},
            {"department": "Computer Science & Engineering", "focus": "Local governance apps, Field tracking, IoT telemetry"}
        ],
        "research_capacity": "All Undergrad Tiers (Tier 1-3) - Foundation to Capstone"
    },
    {
        "id": "inst_bit_mesra",
        "name": "Birla Institute of Technology (BIT) Mesra",
        "short_name": "BIT Mesra",
        "aishe_code": "U-0202",
        "category": "Tier-2 Autonomous Deemed University",
        "state": "Jharkhand",
        "city": "Ranchi",
        "nirf_rank_engg": 53,
        "best_departments": [
            {"department": "Remote Sensing & GIS", "focus": "Pothole Satellite/Aerial Mapping, Urban Sprawl Analysis"},
            {"department": "Civil Engineering", "focus": "Structural Analysis, Environmental Engineering, Traffic Flow"}
        ],
        "research_capacity": "Undergrad Tiers 1-3 + Capstone & M.Tech"
    },
    {
        "id": "inst_coep",
        "name": "COEP Technological University",
        "short_name": "COEP Pune",
        "aishe_code": "U-1199",
        "category": "Tier-2 State Autonomous College",
        "state": "Maharashtra",
        "city": "Pune",
        "nirf_rank_engg": 73,
        "best_departments": [
            {"department": "Civil Engineering", "focus": "Town Planning, Transportation Systems, Stormwater Networks"},
            {"department": "Computer Engineering", "focus": "Edge Computing, Civic Dashboard Analytics"}
        ],
        "research_capacity": "Undergrad Tiers 1-3 + Capstone"
    },
    {
        "id": "inst_vjti",
        "name": "Veermata Jijabai Technological Institute (VJTI)",
        "short_name": "VJTI Mumbai",
        "aishe_code": "C-33827",
        "category": "Tier-2 State Autonomous College",
        "state": "Maharashtra",
        "city": "Mumbai",
        "nirf_rank_engg": 101,
        "best_departments": [
            {"department": "Civil and Environmental Engineering", "focus": "Coastal Road Inundation, Solid Waste Audits"},
            {"department": "Computer Engineering", "focus": "Smart City IoT, Municipal Complaint Triaging"}
        ],
        "research_capacity": "Undergrad Tiers 1-3 + Capstone"
    }
]


def search_institutions(
    query: Optional[str] = None,
    state: Optional[str] = None,
    category: Optional[str] = None,
    limit: int = 20
) -> List[Dict[str, Any]]:
    """
    Searches and filters Indian institutions by name, state, or tier category.
    """
    results = []
    q = (query or "").lower().strip()
    s = (state or "").lower().strip()
    c = (category or "").lower().strip()

    for inst in INDIAN_INSTITUTIONS_MASTER:
        if q and not (
            q in inst["name"].lower()
            or q in inst["short_name"].lower()
            or q in inst["city"].lower()
            or q in inst["aishe_code"].lower()
        ):
            continue
        if s and s not in inst["state"].lower():
            continue
        if c and c not in inst["category"].lower():
            continue
        results.append(inst)
        if len(results) >= limit:
            break

    return results


def get_institution_by_id(inst_id: str) -> Optional[Dict[str, Any]]:
    """Returns the institution details by ID."""
    for inst in INDIAN_INSTITUTIONS_MASTER:
        if inst["id"] == inst_id:
            return inst
    return None
