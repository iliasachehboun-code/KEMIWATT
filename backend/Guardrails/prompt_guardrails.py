import re

INJECTION_PATTERNS = [
    r"ignore\s+previous\s+instructions",
    r"override\s+rules",
    r"system\s+prompt",
    r"show\s+api\s*key",
    r"disable\s+(guardrails|safety)",
]

def detect_prompt_injection(text: str) -> bool:
    return any(re.search(p, text, re.IGNORECASE) for p in INJECTION_PATTERNS)

def mask_pii(text: str) -> str:
    text = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '[EMAIL]', text)
    text = re.sub(r'\b(\+?\d[\d\s\-()]{8,})\b', '[PHONE]', text)
    return text

def is_on_topic(text: str) -> bool:
    keywords = ["battery","voltage","temperature","microgrid","solar","consumption","energy","storage","charge","discharge"]
    return any(k in text.lower() for k in keywords)
