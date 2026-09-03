"""
=============================================================================
Samvad-Setu: Civic Innovation Platform (Part B - Computer Vision)
Module: Part B - Civic Issue Severity Assessment Engine (8 Classes)
=============================================================================
"""

def calculate_severity(issue_type: str, confidence: float) -> str:
    """
    Calculates severity level for detected civic issues.

    Parameters:
        issue_type : detected class name (e.g. pothole, waterlogging)
        confidence : YOLO detection confidence score (0.0 to 1.0)

    Returns:
        severity level: 'CRITICAL', 'HIGH', 'MEDIUM', or 'LOW'
    """
    issue = issue_type.lower().strip()

    # 1. Immediate Life-Safety Hazards (Highest Priority)
    if issue == "open_manhole":
        return "CRITICAL"

    # 2. Roadway Flooding & Waterlogging
    if issue == "waterlogging":
        if confidence >= 0.75:
            return "CRITICAL"
        elif confidence >= 0.45:
            return "HIGH"
        else:
            return "MEDIUM"

    # 3. Traffic Light / Signal Failures
    if issue == "traffic_light":
        if confidence >= 0.70:
            return "HIGH"
        elif confidence >= 0.40:
            return "MEDIUM"
        else:
            return "LOW"

    # 4. Road Potholes
    if issue == "pothole":
        if confidence >= 0.75:
            return "HIGH"
        elif confidence >= 0.50:
            return "MEDIUM"
        else:
            return "LOW"

    # 5. Stray Animals on Active Roadways
    if issue == "stray_animal":
        if confidence >= 0.75:
            return "HIGH"
        elif confidence >= 0.45:
            return "MEDIUM"
        else:
            return "LOW"

    # 6. Garbage Dumps and Waste Containers
    if issue in ("garbage", "waste_container"):
        if confidence >= 0.75:
            return "HIGH"
        elif confidence >= 0.50:
            return "MEDIUM"
        else:
            return "LOW"

    # 7. Structural Road Cracks
    if issue == "crack":
        if confidence >= 0.75:
            return "HIGH"
        elif confidence >= 0.50:
            return "MEDIUM"
        else:
            return "LOW"

    # Default fallback
    return "LOW"


if __name__ == "__main__":
    tests = [
        ("open_manhole", 0.65),
        ("waterlogging", 0.85),
        ("waterlogging", 0.55),
        ("pothole", 0.80),
        ("stray_animal", 0.78),
        ("traffic_light", 0.72),
        ("waste_container", 0.60),
        ("garbage", 0.76),
        ("crack", 0.45),
    ]

    print(f"{'Issue Type':<18} | {'Confidence':<10} | {'Calculated Severity'}")
    print("-" * 50)
    for issue, conf in tests:
        sev = calculate_severity(issue, conf)
        print(f"{issue:<18} | {conf:<10.2f} | {sev}")