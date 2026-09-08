"""Normalized entity extraction with optional transformer and deterministic fallback."""
import re

PATTERNS = {
    "MONEY": r"(?:USD|\$)\s?[\d,]+(?:\.\d{2})?",
    "DATE": r"\b(?:19|20)\d{2}[-/]\d{2}[-/]\d{2}\b",
    "ID_NUMBER": r"\b(?:P[A-Z0-9]{7,9}|ID[- ]?\d{5,12}|ACCT[- ]?\d{5,12})\b",
    "GPE": r"\b(?:United States|India|New York|Missouri|Delaware|Texas|California)\b",
    "ORG": r"\b[A-Z][A-Za-z& ]{2,35}(?:Bank|LLC|Inc|Corporation|Ltd)\b",
    "PERSON": r"(?m)(?<=Name: )[A-Z][a-z]+(?: [A-Z][a-z]+){1,2}",
}

class EntityExtractor:
    """Extract entities into type/text/span/page/confidence schema."""
    def __init__(self, backend="regex", model="dslim/bert-base-NER"):
        self.backend = backend
        self.pipe = None
        if backend == "transformer":
            from transformers import pipeline
            self.pipe = pipeline("ner", model=model, aggregation_strategy="simple")

    def extract(self, text: str, page: int = 1) -> list[dict]:
        if self.pipe:
            return [{"type": e["entity_group"], "text": e["word"].strip(" .,"),
                     "start": int(e["start"]), "end": int(e["end"]), "page": page,
                     "confidence": round(float(e["score"]), 4)} for e in self.pipe(text[:4000])]
        found = []
        for kind, pattern in PATTERNS.items():
            for m in re.finditer(pattern, text):
                found.append({"type": kind, "text": m.group().strip(), "start": m.start(),
                              "end": m.end(), "page": page, "confidence": 1.0})
        return sorted(found, key=lambda x: x["start"])

