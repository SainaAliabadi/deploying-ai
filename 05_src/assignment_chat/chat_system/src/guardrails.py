import re
from typing import Tuple

# Restricted topics (case-insensitive)
RESTRICTED_PATTERNS = [
    r"\bcat(s)?\b",
    r"\bdog(s)?\b",
    r"\bhoroscope(s)?\b",
    r"\bzodiac\b",
    r"\btaylor\s+swift\b"
]

# System prompt protection patterns
SYSTEM_PROMPT_PATTERNS = [
    r"system prompt",
    r"ignore previous instructions",
    r"override instructions",
    r"reveal hidden instructions",
    r"show me your prompt",
    r"change your instructions"
]


def check_guardrails(user_input: str) -> Tuple[bool, str]:
    """
    Returns:
        (allowed: bool, message: str)
    If allowed is False, message contains refusal explanation.
    """

    text = user_input.lower()

    # Check restricted topics
    for pattern in RESTRICTED_PATTERNS:
        if re.search(pattern, text):
            return (
                False,
                "I'm sorry, but I cannot discuss that topic. Let's explore something else!"
            )

    # Check system prompt attacks
    for pattern in SYSTEM_PROMPT_PATTERNS:
        if re.search(pattern, text):
            return (
                False,
                "I’m not able to modify or reveal my internal system instructions."
            )

    return True, ""
