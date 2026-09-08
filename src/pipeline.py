"""End-to-end KYC risk orchestration."""
import logging
from pathlib import Path
from time import perf_counter
from src.cleaning import clean_text
from src.ingest import extract_pdf, persist_extraction
from src.ner import EntityExtractor

logger=logging.getLogger(__name__)

def analyze_document(pdf_path, classifier, extractor=None, processed_dir="data/processed"):
    """Analyze one PDF and return a structured, non-throwing verdict."""
    started=perf_counter(); extractor=extractor or EntityExtractor()
    raw=extract_pdf(pdf_path)
    if raw["status"] != "success": return raw
    persist_extraction(raw, processed_dir)
    pages=[]; entities=[]
    for page in raw["pages"]:
        cleaned=clean_text(page["raw_text"]); pages.append(cleaned)
        entities.extend(extractor.extract(cleaned, page["page"]))
    full_text="\n".join(pages).strip()
    if not full_text:
        return {"status":"error", "file":str(pdf_path), "reason":"Empty extraction; OCR required"}
    label, confidence=classifier.predict([full_text])[0]
    signal_count=sum(w in full_text.lower() for w in ("sanction","mismatch","expired","unverified","offshore","adverse"))
    rationale=f"Model detected {signal_count} explicit risk signal(s) and {len(entities)} entity mention(s)."
    stem = Path(pdf_path).stem
    document_id = "_".join(stem.split("_")[:2]) if stem.startswith("doc_") else stem
    return {"status":"success", "file":str(pdf_path), "document_id":document_id,
            "risk_verdict":label, "confidence":round(confidence,4), "rationale":rationale,
            "entity_count":len(entities), "entities":entities,
            "runtime_seconds":round(perf_counter()-started,4)}
