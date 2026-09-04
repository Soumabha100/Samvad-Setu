"""
=============================================================================
Samvad-Setu: Civic Innovation Platform (Part B - Voice Verification Engine)
Module: Part B - Audio Verification, Whisper Transcription & Part A NLP Triage
=============================================================================
Description:
    1. Verifies citizen audio file (format, integrity, size).
    2. Transcribes voice report to text using OpenAI Whisper with domain hints.
    3. Seamlessly routes the transcribed complaint through the Part A NLP engine
       to classify category, assign municipal department, and determine SLA severity.
=============================================================================
"""

import os
import sys
import argparse
from pathlib import Path
from typing import Dict, Any, Optional, Union

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore
    except AttributeError:
        pass

import whisper  # type: ignore

# -----------------------------------------------------------------------------
# Configuration & Part A Integration
# -----------------------------------------------------------------------------

VOICE_DIR = Path(__file__).resolve().parent
PART_A_DIR = Path(__file__).resolve().parent.parent.parent / "part-a"
if not PART_A_DIR.exists():
    PART_A_DIR = Path(__file__).resolve().parent.parent.parent.parent / "part-a"

ALLOWED_EXTENSIONS = {".mp3", ".wav", ".m4a", ".flac", ".ogg", ".aac", ".webm"}
MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024  # 25 MB max
CIVIC_DOMAIN_PROMPT = (
    "Civic grievance complaint about road damage, pothole, garbage dump, "
    "drainage blockage, waterlogging, flood, water supply, building damage, "
    "bridge damage, landslide, fire emergency."
)

# Connect to Part A NLP inference engine
try:
    import importlib.util
    part_a_file = PART_A_DIR / "predict.py"
    if part_a_file.exists():
        spec = importlib.util.spec_from_file_location("part_a_inference", str(part_a_file))
        part_a_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(part_a_mod)
        get_classifier_fn = getattr(part_a_mod, "get_classifier", None)
        part_a_classifier = get_classifier_fn() if get_classifier_fn else getattr(part_a_mod, "ComplaintClassifier", lambda: None)()
    else:
        part_a_classifier = None
except Exception as e:
    part_a_classifier = None
    print(f"[WARNING] Part A classifier could not be loaded: {e}")

# Cache Whisper model instance
_whisper_model = None


def get_whisper_model():
    """Loads and caches the Whisper model."""
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = whisper.load_model("base")
    return _whisper_model


# -----------------------------------------------------------------------------
# Step 1: Audio File Verification
# -----------------------------------------------------------------------------

def verify_audio_file(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Checks and validates an audio file before transcription.

    Returns:
        Dict with "valid": True/False and diagnostic metadata or error message.
    """
    path = Path(file_path)

    if not path.exists():
        return {
            "valid": False,
            "error": f"Audio file not found: {path.name}",
            "file_name": path.name
        }

    ext = path.suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return {
            "valid": False,
            "error": f"Unsupported audio format '{ext}'. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
            "file_name": path.name
        }

    size_bytes = path.stat().st_size
    if size_bytes == 0:
        return {
            "valid": False,
            "error": "Audio file is empty (0 bytes).",
            "file_name": path.name
        }

    if size_bytes > MAX_FILE_SIZE_BYTES:
        return {
            "valid": False,
            "error": f"File size ({size_bytes / (1024 * 1024):.1f} MB) exceeds maximum allowed 25 MB.",
            "file_name": path.name
        }

    return {
        "valid": True,
        "file_name": path.name,
        "size_bytes": size_bytes,
        "extension": ext
    }


# -----------------------------------------------------------------------------
# Step 2: Whisper Transcription
# -----------------------------------------------------------------------------

def transcribe_audio(
    file_path: Union[str, Path],
    language: Optional[str] = None
) -> Dict[str, Any]:
    """
    Transcribes the citizen voice note into text using Whisper.
    """
    path = Path(file_path)
    model = get_whisper_model()

    transcribe_options = {
        "fp16": False,
        "initial_prompt": CIVIC_DOMAIN_PROMPT
    }
    if language:
        transcribe_options["language"] = language

    result = model.transcribe(str(path), **transcribe_options)

    return {
        "text": result.get("text", "").strip(),
        "detected_language": result.get("language", "unknown")
    }


# -----------------------------------------------------------------------------
# Step 3: Part A NLP Triage
# -----------------------------------------------------------------------------

def triage_with_part_a(text: str) -> Dict[str, Any]:
    """
    Sends the transcribed text to Part A for municipal classification & SLA triage.
    """
    if part_a_classifier is None:
        return {
            "error": "Part A model is not loaded.",
            "status": "failed"
        }

    return part_a_classifier.predict_one(text)


# -----------------------------------------------------------------------------
# Complete End-to-End Pipeline
# -----------------------------------------------------------------------------

def process_voice_complaint(
    file_path: Union[str, Path],
    language: Optional[str] = None
) -> Dict[str, Any]:
    """
    Complete pipeline:
    1. Verify audio file
    2. Transcribe voice with Whisper
    3. Triage transcribed text with Part A NLP engine
    """
    path = Path(file_path)

    # 1. Verify Audio
    verify_res = verify_audio_file(path)
    if not verify_res["valid"]:
        return {
            "status": "failed",
            "stage": "audio_verification",
            "error": verify_res["error"],
            "file_name": path.name
        }

    # 2. Transcribe with Whisper
    try:
        transcription_res = transcribe_audio(path, language=language)
        transcribed_text = transcription_res["text"]
        detected_language = transcription_res["detected_language"]
    except Exception as e:
        return {
            "status": "failed",
            "stage": "audio_transcription",
            "error": f"Transcription error: {str(e)}",
            "file_name": path.name
        }

    if not transcribed_text:
        return {
            "status": "failed",
            "stage": "audio_transcription",
            "error": "No clear speech detected in audio file.",
            "file_name": path.name
        }

    # 3. Verify & Triage with Part A
    nlp_triage = triage_with_part_a(transcribed_text)

    return {
        "status": "success",
        "audio_info": {
            "file_name": path.name,
            "size_kb": round(verify_res["size_bytes"] / 1024, 2),
            "format": verify_res["extension"]
        },
        "transcription": {
            "text": transcribed_text,
            "language": detected_language
        },
        "nlp_triage": nlp_triage
    }


# -----------------------------------------------------------------------------
# CLI Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    import json

    parser = argparse.ArgumentParser(
        description="Verify citizen voice report, transcribe with Whisper, and triage with Part A NLP."
    )
    parser.add_argument(
        "audio_path",
        nargs="?",
        type=str,
        help="Path to audio file (e.g. citizen_report.mp3)"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print result in JSON format"
    )

    args = parser.parse_args()

    # Determine audio file to test
    if args.audio_path:
        target_path = Path(args.audio_path)
    else:
        # Auto-detect audio file in current folder
        voice_files = [
            f for f in VOICE_DIR.iterdir()
            if f.suffix.lower() in ALLOWED_EXTENSIONS
        ]
        if not voice_files:
            print("No audio file provided and none found in voice folder.")
            sys.exit(1)
        target_path = voice_files[0]

    print("=" * 70)
    print(" SAMVAD-SETU : VOICE VERIFICATION & NLP TRIAGE PIPELINE")
    print("=" * 70)
    print(f"Target Audio: {target_path.name}")
    print("Step 1: Verifying audio integrity...")
    print("Step 2: Transcribing speech with Whisper...")
    print("Step 3: Triaging with Part A NLP classifier...\n")

    result = process_voice_complaint(target_path)

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if result["status"] == "success":
            audio = result["audio_info"]
            trans = result["transcription"]
            nlp = result["nlp_triage"]

            print(" [1] AUDIO VERIFICATION")
            print(f"     Status   : Valid ({audio['format'].upper()}, {audio['size_kb']} KB)")

            print("\n [2] WHISPER TRANSCRIPTION")
            print(f"     Language : {trans['language'].upper()}")
            print(f"     Text     : \"{trans['text']}\"")

            print("\n [3] PART A MUNICIPAL NLP TRIAGE")
            print(f"     Category : {nlp['category'].upper()} ({nlp['confidence']['category']:.1%})")
            print(f"     Routing  : {nlp['department']}")
            print(f"     Severity : {nlp['severity'].upper()} ({nlp['confidence']['severity']:.1%})")
            print(f"     SLA Target: {nlp['sla_hours']} Hours (Priority {nlp['priority_level']}: {nlp['priority_description']})")
        else:
            print(f"❌ Failed at stage '{result.get('stage')}': {result.get('error')}")

    print("=" * 70 + "\n")