"""
=============================================================================
Samvad-Setu: Civic Innovation Platform (Path A - Municipal Operations)
Module: Part A - Complaint Classification & Severity Training Pipeline
=============================================================================
Description:
    Trains production-ready NLP models for civic grievance categorization
    and severity SLA triage.

    - Architecture: Dual Multi-Class Classifiers using FeatureUnion
      (Word TF-IDF + Character-wb TF-IDF) with Regularized Logistic Regression.
      Handles code-mixed (Hinglish/Sadri) and multi-script text (Latin,
      Devanagari, Bengali) with high precision and low CPU latency.
    - Output Artifacts:
      1. models/category_model.joblib  (Municipal Department routing)
      2. models/severity_model.joblib  (Urgency & SLA deadline)
      3. models/metadata.json          (Deployment metadata, classes, SLAs)
=============================================================================
"""

import os
import sys
import json
import logging
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Tuple

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace") # type: ignore
        sys.stderr.reconfigure(encoding="utf-8", errors="replace") # type: ignore
    except AttributeError:
        pass

import pandas as pd
# pyrefly: ignore [missing-import]
import numpy as np 
# pyrefly: ignore [missing-import]
import joblib

from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, f1_score


# -----------------------------------------------------------------------------
# Configuration & Constants
# -----------------------------------------------------------------------------

DEFAULT_DATA_PATH = Path(__file__).resolve().parent / "dataset" / "processed_complaints.csv"
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent / "models"

DEPARTMENT_MAPPING: Dict[str, str] = {
    "road_damage": "Public Works Department (PWD - Roads)",
    "garbage": "Solid Waste & Sanitation Department",
    "drainage": "Public Health Engineering Dept (PHED - Drainage)",
    "waterlogging": "Stormwater & Flood Management Cell",
    "flood": "Disaster Management & Emergency Response",
    "building_damage": "Town Planning & Structural Safety",
    "bridge_damage": "PWD - Bridges & Heavy Infrastructure",
    "water_supply": "Municipal Water Supply Board",
    "fire": "Fire Safety & Emergency Services",
    "landslide": "Disaster Response & Geological Hazard Unit"
}

SLA_POLICY: Dict[str, Dict[str, Any]] = {
    "critical": {
        "sla_hours": 4,
        "priority_level": 1,
        "description": "Immediate Life Safety / Critical Hazard Response"
    },
    "high": {
        "sla_hours": 24,
        "priority_level": 2,
        "description": "Urgent Operational Escalation (1 Day)"
    },
    "medium": {
        "sla_hours": 72,
        "priority_level": 3,
        "description": "Standard Municipal Ticket (3 Days)"
    },
    "low": {
        "sla_hours": 168,
        "priority_level": 4,
        "description": "Routine Maintenance Schedule (7 Days)"
    }
}


# -----------------------------------------------------------------------------
# Logger Setup
# -----------------------------------------------------------------------------

def setup_logger(log_level: int = logging.INFO) -> logging.Logger:
    """Configures structured, informative console logging."""
    logger = logging.getLogger("SamvadSetu.PartA.Trainer")
    logger.setLevel(log_level)

    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


logger = setup_logger()


# -----------------------------------------------------------------------------
# Model Pipeline Factory
# -----------------------------------------------------------------------------

def create_text_pipeline(c_param: float = 1.0, max_iter: int = 1000) -> Pipeline:
    """
    Builds a robust, multilingual text classification pipeline.

    Utilizes a FeatureUnion combining:
    1. Word-level TF-IDF: captures unigrams and bigrams across scripts.
    2. Character boundary TF-IDF (char_wb): captures subwords and phonetic
       transliteration patterns in Hinglish / Nagpuri / regional dialects.
    """
    feature_union = FeatureUnion(
        transformer_list=[
            (
                "word_tfidf",
                TfidfVectorizer(
                    analyzer="word",
                    ngram_range=(1, 2),
                    min_df=2,
                    max_features=25000,
                    sublinear_tf=True,
                    token_pattern=r"(?u)\b\w+\b"
                )
            ),
            (
             "char_tfidf",
            TfidfVectorizer(
                 analyzer="char_wb",
                 ngram_range=(3, 5),
                 min_df=3,
                 max_features=40000,
                sublinear_tf=True
                )
            )
        ] # type: ignore
    )

    classifier = LogisticRegression(
        C=c_param,
        max_iter=max_iter,
        class_weight="balanced",
        solver="lbfgs",
        random_state=42
    )

    return Pipeline([
        ("features", feature_union),
        ("classifier", classifier)
    ])


# -----------------------------------------------------------------------------
# Data Loader & Validator
# -----------------------------------------------------------------------------

def load_and_validate_data(filepath: Path) -> pd.DataFrame:
    """Loads CSV, validates required columns, and handles missing values."""
    if not filepath.exists():
        raise FileNotFoundError(f"Dataset not found at path: {filepath}")

    logger.info(f"Loading dataset from: {filepath}")
    df = pd.read_csv(filepath, encoding="utf-8-sig")

    required_columns = {"text", "category", "severity"}
    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Dataset missing required columns: {missing}")

    initial_count = len(df)
    df = df.dropna(subset=["text", "category", "severity"]).copy()
    df["text"] = df["text"].astype(str).str.strip()
    df = df[df["text"] != ""].copy()
    dropped_count = initial_count - len(df)

    if dropped_count > 0:
        logger.warning(f"Dropped {dropped_count} invalid / empty rows.")

    logger.info(f"Loaded {len(df):,} valid records.")
    return df


# -----------------------------------------------------------------------------
# Training & Evaluation Engine
# -----------------------------------------------------------------------------

def train_and_evaluate(
    df: pd.DataFrame,
    target_column: str,
    test_size: float = 0.20,
    random_state: int = 42
) -> Tuple[Pipeline, Dict[str, Any]]:
    """
    Trains and evaluates a model for a specific target ('category' or 'severity').
    """
    logger.info(f"--- Training Model for target: '{target_column}' ---")

    X = df["text"].values
    y = df[target_column].values
    classes = sorted(list(np.unique(y))) # type: ignore

    logger.info(f"Total samples: {len(X):,} | Unique classes: {len(classes)} ({classes})")

    # Stratified train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y # type: ignore
    )
    logger.info(f"Train set: {len(X_train):,} | Test set: {len(X_test):,}")

    pipeline = create_text_pipeline()

    logger.info("Fitting FeatureUnion vectorizer and Logistic Regression...")
    pipeline.fit(X_train, y_train)

    logger.info("Evaluating on holdout test set...")
    y_pred = pipeline.predict(X_test)

    acc = float(accuracy_score(y_test, y_pred))
    macro_f1 = float(f1_score(y_test, y_pred, average="macro"))
    weighted_f1 = float(f1_score(y_test, y_pred, average="weighted"))

    logger.info(f"[{target_column.upper()}] Accuracy   : {acc:.4f} ({acc * 100:.2f}%)")
    logger.info(f"[{target_column.upper()}] Macro F1   : {macro_f1:.4f}")
    logger.info(f"[{target_column.upper()}] Weighted F1: {weighted_f1:.4f}")

    report_dict = classification_report(y_test, y_pred, output_dict=True)
    report_text = classification_report(y_test, y_pred, digits=4)

    print(f"\n================ Classification Report: {target_column.upper()} ================")
    print(report_text)
    print("======================================================================\n")

    metrics = {
        "target": target_column,
        "classes": classes,
        "test_size": test_size,
        "accuracy": acc,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "classification_report": report_dict
    }

    return pipeline, metrics


# -----------------------------------------------------------------------------
# Serialization
# -----------------------------------------------------------------------------

def save_artifacts(
    category_pipeline: Pipeline,
    category_metrics: Dict[str, Any],
    severity_pipeline: Pipeline,
    severity_metrics: Dict[str, Any],
    output_dir: Path
) -> None:
    """Saves serialized models and metadata for production deployment."""
    output_dir.mkdir(parents=True, exist_ok=True)

    category_model_path = output_dir / "category_model.joblib"
    severity_model_path = output_dir / "severity_model.joblib"
    metadata_path = output_dir / "metadata.json"

    logger.info(f"Saving Category model to: {category_model_path}")
    joblib.dump(category_pipeline, category_model_path, compress=3)

    logger.info(f"Saving Severity model to: {severity_model_path}")
    joblib.dump(severity_pipeline, severity_model_path, compress=3)

    metadata = {
        "project": "Samvad-Setu",
        "component": "Part A - Municipal Operations Triage",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "models": {
            "category_model": {
                "file": "category_model.joblib",
                "metrics": category_metrics
            },
            "severity_model": {
                "file": "severity_model.joblib",
                "metrics": severity_metrics
            }
        },
        "department_mapping": DEPARTMENT_MAPPING,
        "sla_policy": SLA_POLICY
    }

    logger.info(f"Writing deployment metadata to: {metadata_path}")
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    logger.info("Artifacts saved successfully!")


# -----------------------------------------------------------------------------
# Live Smoke Test / Inference Demo
# -----------------------------------------------------------------------------

def run_smoke_test(category_pipeline: Pipeline, severity_pipeline: Pipeline) -> None:
    """Validates the live models on multilingual sample complaints."""
    test_cases = [
        "School ke paas road pe massive deep pothole hai, accident risk!",
        "রাস্তায় আবর্জনা স্তূপ হয়ে পড়ে আছে দুর্গন্ধ ছড়াচ্ছে",
        "मुख्य सड़क पर भारी जलभराव है, गाड़ियाँ नहीं निकल पा रही हैं",
        "Drainage completely blocked and sewage water leaking into homes",
        "Fire rapidly spreading at the village entrance, emergency help needed!"
    ]

    print("\n" + "=" * 70)
    print(" LIVE SMOKE TEST / INFERENCE DEMONSTRATION")
    print("=" * 70)

    for text in test_cases:
        cat_pred = category_pipeline.predict([text])[0]
        cat_proba = np.max(category_pipeline.predict_proba([text])[0])

        sev_pred = severity_pipeline.predict([text])[0]
        sev_proba = np.max(severity_pipeline.predict_proba([text])[0])

        dept = DEPARTMENT_MAPPING.get(cat_pred, "Municipal General Helpdesk") # type: ignore
        sla = SLA_POLICY.get(sev_pred, {}).get("sla_hours", "N/A") # type: ignore

        print(f"\nComplaint  : \"{text}\"")
        print(f"Category   : {cat_pred.upper()} (Confidence: {cat_proba:.2%})") # type: ignore
        print(f"Department : {dept}")
        print(f"Severity   : {sev_pred.upper()} (Confidence: {sev_proba:.2%}) -> SLA: {sla} Hours") # type: ignore

    print("\n" + "=" * 70 + "\n")


# -----------------------------------------------------------------------------
# Main Entry Point
# -----------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Train Samvad-Setu Part A Civic Complaint Classifiers."
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Path to processed_complaints.csv dataset"
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory to save models and metadata"
    )
    parser.add_argument(
        "--test-size",
        type=float,
        default=0.20,
        help="Proportion of dataset for testing (default: 0.20)"
    )

    args = parser.parse_args()

    print("======================================================================")
    print("   SAMVAD-SETU : PART A MODEL TRAINING PIPELINE")
    print("======================================================================")

    # 1. Load data
    df = load_and_validate_data(args.data)

    # 2. Train Category Model
    category_pipeline, category_metrics = train_and_evaluate(
        df,
        target_column="category",
        test_size=args.test_size
    )

    # 3. Train Severity Model
    severity_pipeline, severity_metrics = train_and_evaluate(
        df,
        target_column="severity",
        test_size=args.test_size
    )

    # 4. Save artifacts
    save_artifacts(
        category_pipeline,
        category_metrics,
        severity_pipeline,
        severity_metrics,
        args.output_dir
    )

    # 5. Smoke test
    run_smoke_test(category_pipeline, severity_pipeline)

    logger.info("Training pipeline completed successfully.")


if __name__ == "__main__":
    main()
