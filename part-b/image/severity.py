# severity.py

def calculate_severity(issue_type, confidence):
    """
    Prototype severity engine for Samvad Setu AI.

    Parameters:
        issue_type  : detected issue class
        confidence  : YOLO confidence (0.0 - 1.0)

    Returns:
        severity level
    """

    issue_type = issue_type.lower()

    # Critical issues
    if issue_type == "open_manhole":
        return "CRITICAL"

    # High severity issues
    if issue_type == "pothole":
        if confidence >= 0.75:
            return "HIGH"
        elif confidence >= 0.50:
            return "MEDIUM"
        else:
            return "LOW"

    # Garbage
    if issue_type == "garbage":
        if confidence >= 0.75:
            return "HIGH"
        elif confidence >= 0.50:
            return "MEDIUM"
        else:
            return "LOW"

    # Cracks
    if issue_type == "crack":
        if confidence >= 0.75:
            return "HIGH"
        elif confidence >= 0.50:
            return "MEDIUM"
        else:
            return "LOW"

    # Unknown issue
    return "LOW"


# Simple test
if __name__ == "__main__":

    tests = [
        ("pothole", 0.85),
        ("garbage", 0.65),
        ("crack", 0.45),
        ("open_manhole", 0.80),
    ]

    for issue, confidence in tests:
        severity = calculate_severity(issue, confidence)

        print(
            f"Issue: {issue:15} "
            f"Confidence: {confidence:.2f} "
            f"Severity: {severity}"
        )