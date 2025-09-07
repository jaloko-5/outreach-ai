"""Simple spam analysis module for Outreach AI emails."""
from typing import Tuple


TRIGGER_WORDS = {
    "free", "guarantee", "winner", "no obligation", "act now", "risk-free",
    "earn", "money", "urgent", "offer"
}


def spam_score(subject: str, body: str) -> Tuple[int, str]:
    """Compute a basic spam score and return a summary of findings.

    The score is based on the number of exclamation points, uppercase words,
    and presence of known trigger words.

    Args:
        subject: Email subject line.
        body: Email body text.

    Returns:
        A tuple of (score, explanation) where score is an integer and
        explanation is a human-readable summary.
    """
    score = 0
    explanations = []

    # Count exclamation marks
    exclamations = subject.count("!") + body.count("!")
    if exclamations:
        score += exclamations
        explanations.append(f"{exclamations} exclamation point(s)")

    # Count uppercase words
    uppercase_words = [word for word in body.split() if word.isupper() and len(word) > 3]
    if uppercase_words:
        score += len(uppercase_words)
        explanations.append(f"{len(uppercase_words)} uppercase word(s)")

    # Trigger words
    found_triggers = [w for w in TRIGGER_WORDS if w in body.lower()]
    if found_triggers:
        score += len(found_triggers)
        explanations.append(f"trigger words: {', '.join(found_triggers)}")

    explanation = "; ".join(explanations) if explanations else "No issues detected"
    return score, explanation
