import re


SEVERITY_KEYWORDS = {
    "critical": [
        "death", "died", "fatal", "trapped", "collapsed",
        "massive fire", "rapidly spread", "completely flooded",
        "life threatening", "emergency", "dangerous",
        "bridge collapsed", "building collapsed",
        "open manhole", "uncovered manhole", "missing manhole",
        "open drain", "uncovered drain", "manhole cover missing",
        "खुला मैनहोल", "खुला नाला", "ম্যানহোল খোলা",
        "water entering homes", "deep waterlogging"
    ],

    "high": [
        "severe", "serious", "major", "deep", "large",
        "heavy flooding", "fully blocked", "completely blocked",
        "spreading fire", "structural damage",
        "dangerous road", "risk of accident",
        "traffic light", "traffic signal", "signal not working",
        "stray cattle", "cows on road", "stray animal", "traffic hazard",
        "roadway flooding", "waterlogged street", "deep pothole"
    ],

    "medium": [
        "damaged", "broken", "blocked", "overflowing",
        "pothole", "crack", "waterlogging", "garbage",
        "not working", "leaking", "dustbin", "waste container",
        "overflowing dustbin", "dumpster full", "road crack"
    ],

    "low": [
        "minor", "small", "slight", "some garbage",
        "small crack", "little water", "faded signal", "dim light"
    ]
}


SEVERITY_SCORE = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4
}


def detect_severity(text):
    """
    Estimate severity from complaint text.
    Returns severity and confidence.
    """

    if not isinstance(text, str) or not text.strip():
        return "medium", 0.0

    text_lower = text.lower()

    scores = {
        "low": 0,
        "medium": 0,
        "high": 0,
        "critical": 0
    }

    for severity, keywords in SEVERITY_KEYWORDS.items():
        for keyword in keywords:
            if re.search(r"\b" + re.escape(keyword) + r"\b", text_lower):
                scores[severity] += 1

    max_score = max(scores.values())

    if max_score == 0:
        return "medium", 0.25

    candidates = [
        severity for severity, score in scores.items()
        if score == max_score
    ]

    severity = candidates[0]

    total_matches = sum(scores.values())
    confidence = max_score / total_matches

    return severity, round(confidence, 2)


if __name__ == "__main__":

    examples = [
        "There is a small crack on the road.",
        "There is a deep dangerous pothole near the school.",
        "The bridge has completely collapsed and people are trapped.",
        "A massive fire is rapidly spreading near houses.",
        "Some garbage is lying near the road."
    ]

    print("========== SEVERITY TEST ==========")

    for text in examples:
        severity, confidence = detect_severity(text)

        print("\nComplaint :", text)
        print("Severity  :", severity)
        print("Confidence:", confidence)

    print("\n====================================")