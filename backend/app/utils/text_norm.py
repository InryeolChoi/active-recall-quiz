import re

PUNCTUATION_PATTERN = re.compile(r"[,\.\(\)\[\]\{\}]")
SPACE_PATTERN = re.compile(r"\s+")


def normalize_text(value: str) -> str:
    value = value.strip().lower()
    value = PUNCTUATION_PATTERN.sub(" ", value)
    value = SPACE_PATTERN.sub(" ", value)
    return value.strip()
