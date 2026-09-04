"""
=============================================================================
Samvad-Setu: Civic Innovation Platform (Part A - Municipal Operations)
Module: Part A - Real-Time Complaint Inference & Triage Engine
=============================================================================
Description:
    Loads trained scikit-learn classification pipelines and metadata to
    provide real-time categorization and SLA triage for citizen grievances.

    Supports:
    - Multilingual & code-mixed text (Latin, Devanagari, Bengali, Hinglish)
    - Automatic text preprocessing (Unicode NFKC, URL/email cleanup)
    - Department routing & SLA deadline computation
    - Command-line single prediction, batch processing, and interactive mode
=============================================================================
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace") # type: ignore
        sys.stderr.reconfigure(encoding="utf-8", errors="replace") # type: ignore
    except AttributeError:
        pass

# pyrefly: ignore [missing-import]
import joblib
# pyrefly: ignore [missing-import]
import numpy as np

# Local preprocessing and severity heuristics
try:
    from preprocess import preprocess_complaint
except ImportError:
    from .preprocess import preprocess_complaint  # type: ignore

try:
    from severity_rules import detect_severity as rule_based_severity
except ImportError:
    from .severity_rules import detect_severity as rule_based_severity  # type: ignore


# -----------------------------------------------------------------------------
# Paths & Artifacts Loading
# -----------------------------------------------------------------------------

MODELS_DIR = Path(__file__).resolve().parent / "models"
CATEGORY_MODEL_PATH = MODELS_DIR / "category_model.joblib"
SEVERITY_MODEL_PATH = MODELS_DIR / "severity_model.joblib"
METADATA_PATH = MODELS_DIR / "metadata.json"


class ComplaintClassifier:
    """Production inference engine for Samvad-Setu Part A."""

    def __init__(self, models_dir: Path = MODELS_DIR):
        self.models_dir = models_dir
        self.category_pipeline = None
        self.severity_pipeline = None
        self.metadata = {}
        self.department_mapping = {}
        self.sla_policy = {}
        self._load_artifacts()

    def _load_artifacts(self) -> None:
        """Loads serialized models and configuration metadata."""
        if not (self.models_dir / "category_model.joblib").exists():
            raise FileNotFoundError(
                f"Category model not found at {self.models_dir / 'category_model.joblib'}. "
                "Please run `python train.py` first."
            )

        self.category_pipeline = joblib.load(self.models_dir / "category_model.joblib")
        self.severity_pipeline = joblib.load(self.models_dir / "severity_model.joblib")

        if (self.models_dir / "metadata.json").exists():
            with open(self.models_dir / "metadata.json", "r", encoding="utf-8") as f:
                self.metadata = json.load(f)
                self.department_mapping = self.metadata.get("department_mapping", {})
                self.sla_policy = self.metadata.get("sla_policy", {})

    def predict_one(self, raw_text: str) -> Dict[str, Any]:
        """
        Classifies a single raw citizen complaint.

        Returns:
            Dict containing preprocessed text, category, department,
            severity, SLA hours, priority level, and confidence scores.
        """
        if not raw_text or not raw_text.strip():
            return {
                "error": "Empty complaint text provided.",
                "status": "failed"
            }

        # 1. Clean and normalize text
        cleaned_text = preprocess_complaint(raw_text)

        # 2. Category Prediction
        cat_probs = self.category_pipeline.predict_proba([cleaned_text])[0]
        cat_classes = self.category_pipeline.classes_
        cat_best_idx = np.argmax(cat_probs)
        category = str(cat_classes[cat_best_idx])
        category_confidence = float(cat_probs[cat_best_idx])

        # 3. Severity Prediction
        sev_probs = self.severity_pipeline.predict_proba([cleaned_text])[0]
        sev_classes = self.severity_pipeline.classes_
        sev_best_idx = np.argmax(sev_probs)
        severity = str(sev_classes[sev_best_idx])
        severity_confidence = float(sev_probs[sev_best_idx])

        # 4. Critical Safety Override: If keyword rules detect critical life threat with high certainty
        rule_sev, rule_conf = rule_based_severity(raw_text)
        if rule_sev == "critical" and rule_conf >= 0.50 and severity != "critical":
            # Safety boost for urgent emergencies
            severity = "critical"
            severity_confidence = max(severity_confidence, rule_conf)

        # 5. Route Department & Resolve SLA Policy
        department = self.department_mapping.get(
            category,
            "General Municipal Helpdesk"
        )
        sla_info = self.sla_policy.get(severity, {
            "sla_hours": 72,
            "priority_level": 3,
            "description": "Standard Municipal Ticket"
        })

        return {
            "original_text": raw_text,
            "cleaned_text": cleaned_text,
            "category": category,
            "department": department,
            "severity": severity,
            "sla_hours": sla_info.get("sla_hours", 72),
            "priority_level": sla_info.get("priority_level", 3),
            "priority_description": sla_info.get("description", ""),
            "confidence": {
                "category": round(category_confidence, 4),
                "severity": round(severity_confidence, 4)
            },
            "status": "success"
        }

    def predict_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """Classifies a batch of citizen complaints."""
        return [self.predict_one(t) for t in texts]


# Global singleton instance for easy import
_engine: Optional[ComplaintClassifier] = None


def get_classifier() -> ComplaintClassifier:
    """Returns or initializes the global singleton classifier."""
    global _engine
    if _engine is None:
        _engine = ComplaintClassifier()
    return _engine


def predict_complaint(text: str) -> Dict[str, Any]:
    """Convenience helper function for importing in other modules."""
    return get_classifier().predict_one(text)


# -----------------------------------------------------------------------------
# CLI Entry Point & Interactive Mode
# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Samvad-Setu Part A: Real-Time Civic Grievance Triage"
    )
    parser.add_argument(
        "text",
        nargs="?",
        type=str,
        help="Single complaint text to classify"
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Launch interactive REPL testing mode"
    )
    parser.add_argument(
        "-j", "--json",
        action="store_true",
        help="Output results in JSON format"
    )

    args = parser.parse_args()
    classifier = get_classifier()

    if args.interactive:
        print("=" * 70)
        print(" Samvad-Setu Part A: Interactive Triage REPL")
        print(" Type your complaint in English, Hindi, Bengali, or Hinglish.")
        print(" Type 'exit' or 'quit' to stop.")
        print("=" * 70)

        while True:
            try:
                user_input = input("\nEnter complaint > ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ("exit", "quit", "q"):
                    print("Exiting.")
                    break

                res = classifier.predict_one(user_input)
                if args.json:
                    print(json.dumps(res, indent=2, ensure_ascii=False))
                else:
                    print(f"\n📂 Category   : {res['category'].upper()} ({res['confidence']['category']:.1%})")
                    print(f"🏢 Department : {res['department']}")
                    print(f"⚡ Severity   : {res['severity'].upper()} ({res['confidence']['severity']:.1%})")
                    print(f"⏱️  SLA Target : {res['sla_hours']} Hours (Priority {res['priority_level']}: {res['priority_description']})")

            except (KeyboardInterrupt, EOFError):
                print("\nExiting.")
                break
        return

    if args.text:
        res = classifier.predict_one(args.text)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            print("\n" + "=" * 70)
            print(" CIVIC GRIEVANCE CLASSIFICATION RESULT")
            print("=" * 70)
            print(f"Complaint  : \"{res['original_text']}\"")
            print(f"Category   : {res['category'].upper()} (Confidence: {res['confidence']['category']:.1%})")
            print(f"Department : {res['department']}")
            print(f"Severity   : {res['severity'].upper()} (Confidence: {res['confidence']['severity']:.1%})")
            print(f"SLA Target : {res['sla_hours']} Hours (Priority {res['priority_level']}: {res['priority_description']})")
            print("=" * 70 + "\n")
        return

    # Default: Run demonstration on sample multilingual cases
    demo_samples = [
        "School ke paas road pe massive deep pothole hai, accident risk!",
        "রাস্তায় আবর্জনা স্তূপ হয়ে পড়ে আছে দুর্গন্ধ ছড়াচ্ছে",
        "मुख्य सड़क पर भारी जलभराव है, गाड़ियाँ नहीं निकल पा रही हैं",
        "Drainage completely blocked and sewage water leaking into homes",
        "Fire rapidly spreading at the village entrance, emergency help needed!"
    ]

    print("\n" + "=" * 70)
    print(" SAMVAD-SETU PART A: MULTILINGUAL INFERENCE DEMO")
    print("=" * 70)

    for sample in demo_samples:
        res = classifier.predict_one(sample)
        print(f"\nComplaint  : \"{res['original_text']}\"")
        print(f"Category   : {res['category'].upper()} ({res['confidence']['category']:.1%}) -> {res['department']}")
        print(f"Severity   : {res['severity'].upper()} ({res['confidence']['severity']:.1%}) -> SLA: {res['sla_hours']}h ({res['priority_description']})")

    print("\n" + "=" * 70)
    print("Tip: Run `python predict.py \"your complaint\"` or `python predict.py -i` for interactive mode.")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
