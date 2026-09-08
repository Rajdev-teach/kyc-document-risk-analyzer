"""PDF ingestion with per-page provenance and explicit OCR-needed flags."""
import json
import logging
from pathlib import Path
from pypdf import PdfReader

logger = logging.getLogger(__name__)

def extract_pdf(path: str | Path) -> dict:
    """Return page text and metadata; flag image-only pages rather than silently failing."""
    path = Path(path)
    try:
        reader = PdfReader(str(path))
        pages = []
        for number, page in enumerate(reader.pages, 1):
            text = page.extract_text() or ""
            method = "embedded_text" if len(text.strip()) >= 20 else "ocr_required_skipped"
            if method != "embedded_text": logger.warning("OCR required: %s page %s", path, number)
            pages.append({"page": number, "raw_text": text, "method": method})
        return {"status": "success", "file": str(path), "page_count": len(pages), "pages": pages}
    except Exception as exc:
        logger.exception("PDF extraction failed for %s", path)
        return {"status": "error", "file": str(path), "reason": str(exc), "pages": []}

def persist_extraction(result: dict, output_dir: str | Path) -> Path:
    output = Path(output_dir); output.mkdir(parents=True, exist_ok=True)
    target = output / f"{Path(result['file']).stem}.json"
    target.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return target

