"""Composable, conservative text-cleaning functions for NER."""
import re
import unicodedata

def remove_page_numbers(text: str) -> str:
    return re.sub(r"(?i)(Page\s+\d+\s+of\s+\d+|-\s*\d+\s*-)", "", text)

def fix_hyphenated_newlines(text: str) -> str:
    return re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)

def normalize_whitespace(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()

def clean_text(text: str) -> str:
    """Normalize Unicode and layout noise while preserving case for NER."""
    text = unicodedata.normalize("NFKC", text)
    return normalize_whitespace(remove_page_numbers(fix_hyphenated_newlines(text)))

def segment_text(text: str, max_chars: int = 1500) -> list[str]:
    paragraphs, result, current = text.split("\n"), [], ""
    for paragraph in paragraphs:
        if current and len(current) + len(paragraph) + 1 > max_chars:
            result.append(current.strip()); current = ""
        current += ("\n" if current else "") + paragraph
    if current.strip(): result.append(current.strip())
    return result

