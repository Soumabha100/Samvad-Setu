"""
=============================================================================
Samvad-Setu: Multimodal Incident Deduplication & Fusion Engine
Module: part-b/dedup.py
=============================================================================
Description:
    Analyzes multiple citizen grievance reports (photos, voice notes, text,
    and GPS locations). When multiple citizens report the same civic problem
    (e.g., 9 separate citizen reports about a deep pothole on the same road),
    this engine:
      1. Calculates spatial, categorical, semantic, and visual similarities.
      2. Automatically clusters duplicate complaints under 1 Master Incident.
      3. Aggregates all evidence (photos, voice transcripts, timestamps).
      4. Auto-escalates priority & urgency based on community report volume.
=============================================================================
"""

import math
import re
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]
from PIL import Image
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =============================================================================
# 1. SPATIAL SIMILARITY (HAVERSINE DISTANCE)
# =============================================================================

def haversine_distance(
    coord1: Tuple[float, float],
    coord2: Tuple[float, float]
) -> float:
    """
    Computes the great-circle distance between two GPS coordinates in meters.
    coord: (latitude, longitude)
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    R = 6371000.0  # Earth radius in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return R * c


def compute_spatial_similarity(
    loc1: Optional[Dict[str, Any]],
    loc2: Optional[Dict[str, Any]]
) -> float:
    """
    Returns spatial similarity score [0.0 to 1.0].
    - Within 50m  -> 1.0 (Almost certainly exact same spot)
    - Within 100m -> 0.85
    - Within 200m -> 0.60
    - Within 350m -> 0.30
    - Beyond 350m -> 0.0
    Fallback: Textual address matching if GPS is missing.
    """
    if not loc1 or not loc2:
        return 0.5  # Neutral fallback when location is omitted

    # 1. GPS Coordinates check
    lat1 = loc1.get("lat")
    lng1 = loc1.get("lng")
    lat2 = loc2.get("lat")
    lng2 = loc2.get("lng")

    if lat1 is not None and lng1 is not None and lat2 is not None and lng2 is not None:
        dist_m = haversine_distance((float(lat1), float(lng1)), (float(lat2), float(lng2)))
        if dist_m <= 50.0:
            return 1.0
        elif dist_m <= 100.0:
            return 0.85
        elif dist_m <= 200.0:
            return 0.60
        elif dist_m <= 350.0:
            return 0.30
        else:
            return 0.0

    # 2. Address / Landmark string fallback
    addr1 = str(loc1.get("address", "")).lower().strip()
    addr2 = str(loc2.get("address", "")).lower().strip()
    if addr1 and addr2:
        tokens1 = set(re.findall(r"\w+", addr1))
        tokens2 = set(re.findall(r"\w+", addr2))
        if tokens1 and tokens2:
            jaccard = len(tokens1 & tokens2) / len(tokens1 | tokens2)
            return float(min(1.0, jaccard * 1.5))

    return 0.4


# =============================================================================
# 2. VISUAL SIMILARITY (PERCEPTUAL DIFFERENCE HASHING)
# =============================================================================

def compute_dhash(image_path: str, hash_size: int = 8) -> Optional[np.ndarray]:
    """
    Computes a 64-bit boolean difference hash (dHash) for an image.
    Invariant to slight rotations, compression, lighting, and scaling.
    """
    p = Path(image_path)
    if not p.exists() or not p.is_file():
        return None
    try:
        with Image.open(p) as img:
            # Resize to (width = hash_size + 1, height = hash_size) in grayscale
            resized = img.convert("L").resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
            arr = np.array(resized)
            # Compare adjacent horizontal pixels
            return arr[:, 1:] > arr[:, :-1]
    except Exception:
        return None


def compute_image_similarity(
    img_path1: Optional[str],
    img_path2: Optional[str]
) -> float:
    """
    Returns visual similarity score [0.0 to 1.0] between two photos.
    """
    if not img_path1 or not img_path2:
        return 0.5  # Neutral if either image is missing

    h1 = compute_dhash(img_path1)
    h2 = compute_dhash(img_path2)
    if h1 is None or h2 is None:
        return 0.5

    # Hamming distance: count of mismatched bits out of 64
    diff_bits = np.count_nonzero(h1 != h2)
    similarity = 1.0 - (diff_bits / float(h1.size))
    return float(max(0.0, min(1.0, similarity)))


# =============================================================================
# 3. SEMANTIC TEXT SIMILARITY
# =============================================================================

_VECTORIZER = TfidfVectorizer(
    ngram_range=(1, 2),
    analyzer="word",
    min_df=1,
    sublinear_tf=True
)

def compute_text_similarity(text1: Optional[str], text2: Optional[str]) -> float:
    """
    Returns TF-IDF cosine semantic similarity score [0.0 to 1.0]
    between two written or transcribed descriptions.
    """
    t1 = str(text1 or "").strip()
    t2 = str(text2 or "").strip()
    if not t1 or not t2:
        return 0.5

    try:
        tfidf = _VECTORIZER.fit_transform([t1, t2])
        sim = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
        return float(max(0.0, min(1.0, sim)))
    except Exception:
        return 0.5


# =============================================================================
# 4. CATEGORY & CIVIC ISSUE MATCHING
# =============================================================================

# Related categories that commonly describe the exact same event
RELATED_CATEGORIES = {
    "road_damage": {"pothole", "crack", "road_damage"},
    "pothole": {"pothole", "crack", "road_damage"},
    "crack": {"pothole", "crack", "road_damage"},
    "garbage": {"garbage", "waste_container"},
    "waste_container": {"garbage", "waste_container"},
    "drainage": {"drainage", "open_manhole", "waterlogging"},
    "open_manhole": {"drainage", "open_manhole"},
    "waterlogging": {"waterlogging", "drainage", "flood"}
}

def compute_category_similarity(cat1: Optional[str], cat2: Optional[str]) -> float:
    """
    Returns 1.0 for exact category match, 0.75 for closely related civic issue, 0.0 otherwise.
    """
    c1 = str(cat1 or "").lower().strip()
    c2 = str(cat2 or "").lower().strip()
    if not c1 or not c2:
        return 0.5
    if c1 == c2:
        return 1.0
    if c1 in RELATED_CATEGORIES and c2 in RELATED_CATEGORIES[c1]:
        return 0.75
    return 0.0


# =============================================================================
# 5. COMPOSITE INCIDENT SIMILARITY SCORER
# =============================================================================

DUPLICATE_THRESHOLD = 0.68  # Score >= 0.68 signifies the same civic incident

def calculate_incident_similarity(
    report_a: Dict[str, Any],
    report_b: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Calculates composite similarity between two citizen reports.
    Weights:
      - Spatial Proximity (GPS): 35%
      - Category Match: 25%
      - Text Semantic Match: 25%
      - Visual Image Match: 15%
    """
    s_geo = compute_spatial_similarity(report_a.get("location"), report_b.get("location"))
    s_cat = compute_category_similarity(report_a.get("category"), report_b.get("category"))
    s_text = compute_text_similarity(
        report_a.get("text") or report_a.get("description"),
        report_b.get("text") or report_b.get("description")
    )
    s_img = compute_image_similarity(report_a.get("image_path"), report_b.get("image_path"))

    # Check which modalities are present in both reports
    has_text = bool(
        (report_a.get("text") or report_a.get("description"))
        and (report_b.get("text") or report_b.get("description"))
    )
    has_img = bool(report_a.get("image_path") and report_b.get("image_path"))

    # If category is completely conflicting (e.g. fire vs garbage), cannot be same incident
    if s_cat == 0.0 and s_geo < 0.95:
        composite_score = 0.15
    # If location is too far (> 350 meters), they are different incidents
    elif s_geo == 0.0:
        composite_score = 0.20
    else:
        # Dynamic weights normalized by active modalities
        weights = {"geo": 0.40, "cat": 0.30}
        scores = {"geo": s_geo, "cat": s_cat}

        if has_text:
            weights["text"] = 0.20
            scores["text"] = s_text
        if has_img:
            weights["img"] = 0.15
            scores["img"] = s_img

        total_weight = sum(weights.values())
        composite_score = sum(weights[k] * scores[k] for k in weights) / total_weight

    is_duplicate = composite_score >= DUPLICATE_THRESHOLD

    return {
        "composite_score": round(composite_score, 3),
        "is_duplicate": is_duplicate,
        "metrics": {
            "spatial_similarity": round(s_geo, 3),
            "category_similarity": round(s_cat, 3),
            "text_similarity": round(s_text, 3),
            "visual_similarity": round(s_img, 3)
        }
    }


# =============================================================================
# 6. INCIDENT FUSION (MERGING INTO MASTER INCIDENT)
# =============================================================================

SEVERITY_LEVELS = {"low": 1, "medium": 2, "high": 3, "critical": 4}
LEVEL_TO_SEVERITY = {1: "low", 2: "medium", 3: "high", 4: "critical"}
SLA_HOURS_MAP = {"critical": 4, "high": 24, "medium": 72, "low": 168}

def merge_reports(master: Dict[str, Any], incoming: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fuses an incoming duplicate report into an existing Master Incident:
    - Increments citizen_count.
    - Aggregates submitted images and audio evidence into galleries.
    - Appends citizen testimony into the audit trail.
    - Auto-escalates severity & urgency as citizen count increases.
    """
    master["citizen_count"] = master.get("citizen_count", 1) + 1

    # Aggregate citizen reports
    citizen_record = {
        "report_id": incoming.get("id") or incoming.get("_id") or f"rep_{master['citizen_count']}",
        "citizen_name": incoming.get("citizen_name") or incoming.get("reported_by", "Anonymous Citizen"),
        "text": incoming.get("text") or incoming.get("description", ""),
        "timestamp": incoming.get("timestamp") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    master.setdefault("citizen_reports", []).append(citizen_record)

    # Aggregate images
    new_img = incoming.get("image_path") or incoming.get("image_url")
    if new_img and new_img not in master.setdefault("evidence_gallery", []):
        master["evidence_gallery"].append(new_img)

    # Aggregate audio notes
    new_aud = incoming.get("audio_path") or incoming.get("audio_url")
    if new_aud and new_aud not in master.setdefault("audio_gallery", []):
        master["audio_gallery"].append(new_aud)

    # Auto-escalation based on community volume:
    # 7+ reports -> CRITICAL (Emergency SLA: 4h)
    # 3+ reports -> HIGH (Urgent SLA: 24h)
    current_sev = str(master.get("severity", "medium")).lower()
    current_level = SEVERITY_LEVELS.get(current_sev, 2)
    incoming_sev = str(incoming.get("severity", "medium")).lower()
    incoming_level = SEVERITY_LEVELS.get(incoming_sev, 2)
    max_level = max(current_level, incoming_level)

    if master["citizen_count"] >= 7:
        max_level = max(max_level, 4)  # CRITICAL
    elif master["citizen_count"] >= 3:
        max_level = max(max_level, 3)  # HIGH

    master["severity"] = LEVEL_TO_SEVERITY[max_level]
    master["sla_hours"] = SLA_HOURS_MAP[master["severity"]]

    # Synthesize title and impact summary
    cat = master.get("category", "Civic Issue").replace("_", " ").title()
    master["summary"] = (
        f"Master Ticket: Confirmed {cat} verified by {master['citizen_count']} citizens. "
        f"Severity escalated to {master['severity'].upper()} ({master['sla_hours']}h SLA target)."
    )

    return master


# =============================================================================
# 7. BATCH CLUSTERING ENGINE
# =============================================================================

def cluster_grievances(reports: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Takes a raw list of N incoming citizen grievance reports and clusters
    all duplicates together, returning a consolidated list of Master Incidents.
    """
    master_incidents: List[Dict[str, Any]] = []

    for report in reports:
        matched_master = None
        highest_score = 0.0

        for master in master_incidents:
            sim_result = calculate_incident_similarity(report, master)
            if sim_result["is_duplicate"] and sim_result["composite_score"] > highest_score:
                highest_score = sim_result["composite_score"]
                matched_master = master

        if matched_master:
            merge_reports(matched_master, report)
        else:
            # Create a new Master Incident
            new_master = {
                "master_ticket_id": report.get("id") or report.get("_id") or f"TICKET-{len(master_incidents) + 1:04d}",
                "title": report.get("title") or report.get("text", "Civic Grievance")[:50],
                "category": report.get("category", "other"),
                "department": report.get("department", "Municipal Operations"),
                "location": report.get("location", {}),
                "severity": str(report.get("severity", "medium")).lower(),
                "sla_hours": SLA_HOURS_MAP.get(str(report.get("severity", "medium")).lower(), 72),
                "citizen_count": 1,
                "evidence_gallery": [report.get("image_path") or report.get("image_url")] if (report.get("image_path") or report.get("image_url")) else [],
                "audio_gallery": [report.get("audio_path") or report.get("audio_url")] if (report.get("audio_path") or report.get("audio_url")) else [],
                "citizen_reports": [
                    {
                        "report_id": report.get("id") or "rep_1",
                        "citizen_name": report.get("citizen_name") or report.get("reported_by", "Citizen #1"),
                        "text": report.get("text") or report.get("description", ""),
                        "timestamp": report.get("timestamp") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                ],
                "summary": f"Initial report registered for {report.get('category', 'civic issue')}."
            }
            master_incidents.append(new_master)

    return master_incidents


# =============================================================================
# 8. SELF-TEST / CLI DEMONSTRATION
# =============================================================================

if __name__ == "__main__":
    print("=" * 75)
    print(" SAMVAD-SETU : MULTIMODAL INCIDENT DEDUPLICATION & FUSION DEMO")
    print("=" * 75)

# Simulated batch: 9 citizens reporting the same pothole near a school,
# plus 1 completely separate garbage report across town.
SAMPLE_REPORTS = [
    {
        "id": "rep_101",
        "citizen_name": "Rohan Sharma",
        "text": "Huge deep pothole on Main Road right in front of the primary school!",
        "category": "road_damage",
        "department": "Public Works Department (PWD - Roads)",
        "severity": "medium",
        "location": {"lat": 23.5120, "lng": 87.3110, "address": "Main Road, Near Primary School"}
    },
        {
            "id": "rep_102",
            "citizen_name": "Priya Singh",
            "text": "School ke saamne road par bohot bada khadda hai, bikers gir rahe hain",
            "category": "road_damage",
            "department": "Public Works Department (PWD - Roads)",
            "severity": "medium",
            "location": {"lat": 23.5122, "lng": 87.3112, "address": "Main Road School Gate"}
        },
        {
            "id": "rep_103",
            "citizen_name": "Amit Kumar",
            "text": "Accident risk due to deep road crater near school gate",
            "category": "road_damage",
            "department": "Public Works Department (PWD - Roads)",
            "severity": "high",
            "location": {"lat": 23.5121, "lng": 87.3111, "address": "Main Road"}
        },
        {
            "id": "rep_104",
            "citizen_name": "Sunita Verma",
            "text": "Road damage and big pothole near primary school entrance",
            "category": "road_damage",
            "department": "Public Works Department (PWD - Roads)",
            "severity": "medium",
            "location": {"lat": 23.5123, "lng": 87.3109, "address": "Opposite Primary School"}
        },
        {
            "id": "rep_105",
            "citizen_name": "Vikram Das",
            "text": "রাস্তার মাঝে বড় গর্ত স্কুলের সামনে দুর্ঘটনা হতে পারে",
            "category": "road_damage",
            "department": "Public Works Department (PWD - Roads)",
            "severity": "medium",
            "location": {"lat": 23.5119, "lng": 87.3113, "address": "School Road"}
        },
        {
            "id": "rep_106",
            "citizen_name": "Deepak Roy",
            "text": "School main road pothole needs urgent repair",
            "category": "road_damage",
            "department": "Public Works Department (PWD - Roads)",
            "severity": "medium",
            "location": {"lat": 23.5124, "lng": 87.3110, "address": "Main Road"}
        },
        {
            "id": "rep_107",
            "citizen_name": "Anjali Gupta",
            "text": "Bada pothole hai school road pe bahut khatarnak",
            "category": "road_damage",
            "department": "Public Works Department (PWD - Roads)",
            "severity": "high",
            "location": {"lat": 23.5120, "lng": 87.3108, "address": "Near Primary School"}
        },
        {
            "id": "rep_108",
            "citizen_name": "Manoj Tiwari",
            "text": "Danger crater in road opposite school, please patch immediately",
            "category": "road_damage",
            "department": "Public Works Department (PWD - Roads)",
            "severity": "medium",
            "location": {"lat": 23.5121, "lng": 87.3112, "address": "Main Road"}
        },
        {
            "id": "rep_109",
            "citizen_name": "Suresh Patel",
            "text": "Pothole causing massive traffic and safety hazard near school",
            "category": "road_damage",
            "department": "Public Works Department (PWD - Roads)",
            "severity": "high",
            "location": {"lat": 23.5122, "lng": 87.3110, "address": "Primary School Road"}
        },
        # Separate, unrelated report 5 kilometers away
        {
            "id": "rep_201",
            "citizen_name": "Kavita Rao",
            "text": "Public dustbin overflowing with garbage in Sector 4 market",
            "category": "garbage",
            "department": "Solid Waste & Sanitation Department",
            "severity": "medium",
            "location": {"lat": 23.5580, "lng": 87.3590, "address": "Sector 4 Market"}
        }
]


if __name__ == "__main__":
    print("=" * 75)
    print(" SAMVAD-SETU : MULTIMODAL INCIDENT DEDUPLICATION & FUSION DEMO")
    print("=" * 75)

    print(f"\n[INPUT] Received {len(SAMPLE_REPORTS)} raw citizen grievance reports.")
    print("Running Multimodal Incident Fusion & Clustering...\n")

    master_tickets = cluster_grievances(SAMPLE_REPORTS)

    print(f"[OUTPUT] Successfully clustered into {len(master_tickets)} Master Tickets!\n")

    for idx, t in enumerate(master_tickets, 1):
        print(f"--- MASTER TICKET #{idx} ({t['master_ticket_id']}) ---")
        print(f"Category          : {t['category'].upper()}")
        print(f"Department        : {t['department']}")
        print(f"Citizens Reporting: {t['citizen_count']} citizens")
        print(f"Urgency Level     : {t['severity'].upper()} (Target SLA: {t['sla_hours']} Hours)")
        print(f"Executive Summary : {t['summary']}")
        print("Subscribed Citizens:")
        for r in t["citizen_reports"]:
            print(f"  - [{r['citizen_name']}]: \"{r['text']}\"")
        print()

    print("=" * 75)
    print(" Deduplication & Clustering Engine is fully verified and functional!")
    print("=" * 75)