import re
import unicodedata


def normalize_unicode(text):
    """
    Normalize Unicode characters while preserving
    the original language/script.
    """
    text = unicodedata.normalize("NFKC", text)
    return text


def normalize_whitespace(text):
    """
    Remove unnecessary spaces and line breaks.
    """
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def remove_urls(text):
    """
    Remove URLs from citizen complaints.
    """
    text = re.sub(
        r"https?://\S+|www\.\S+",
        " ",
        text,
        flags=re.IGNORECASE
    )
    return text


def remove_email_addresses(text):
    """
    Remove email addresses.
    """
    text = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        " ",
        text
    )
    return text


def normalize_repeated_characters(text):
    """
    Reduce excessive repeated characters.

    Example:
    "sooooo dangerous" -> "soo dangerous"
    """
    text = re.sub(r"(.)\1{3,}", r"\1\1", text)
    return text


def normalize_punctuation(text):
    """
    Normalize repeated punctuation without removing
    meaningful punctuation completely.
    """

    text = re.sub(r"!{2,}", "!", text)
    text = re.sub(r"\?{2,}", "?", text)
    text = re.sub(r"\.{3,}", "...", text)

    return text


def clean_text(text):
    """
    Complete professional preprocessing pipeline.

    Important:
    We intentionally do NOT remove stopwords,
    numbers, negations, or all punctuation because
    they can contain useful information for civic
    complaint classification and severity detection.
    """

    if not isinstance(text, str):
        return ""

    # Unicode normalization
    text = normalize_unicode(text)

    # Remove URLs
    text = remove_urls(text)

    # Remove email addresses
    text = remove_email_addresses(text)

    # Normalize repeated characters
    text = normalize_repeated_characters(text)

    # Normalize punctuation
    text = normalize_punctuation(text)

    # Normalize whitespace
    text = normalize_whitespace(text)

    return text


def preprocess_complaint(text):
    """
    Main function used by Part A.
    """
    return clean_text(text)


if __name__ == "__main__":

    examples = [
        "There is a HUGE pothole!!! near the school.",
        "सड़क पर बहुत बड़ा गड्ढा है!!! कृपया मदद करें।",
        "রাস্তায় জল জমে গেছে.... Please help!",
        "Road pe soooo much garbage hai!!!",
        "Please check https://example.com urgently."
    ]

    print("========== PREPROCESSING TEST ==========")

    for text in examples:

        processed = preprocess_complaint(text)

        print("\nOriginal :")
        print(text)

        print("Processed:")
        print(processed)

    print("\n========================================")