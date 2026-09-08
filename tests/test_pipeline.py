from src.cleaning import clean_text
from src.ner import EntityExtractor
from src.model import RiskClassifier
from pathlib import Path
from src.pipeline import analyze_document

def test_cleaning_preserves_case_and_repairs_hyphen():
    assert clean_text("John doc-\nument\nPage 1 of 2") == "John document"

def test_regex_entities_normalized():
    entities=EntityExtractor().extract("Name: John Carter\nPassport ID: PUS1234567\nExpiry: 2029-04-10")
    assert {e["type"] for e in entities} >= {"PERSON","ID_NUMBER","DATE"}
    assert all(set(e)=={"type","text","start","end","page","confidence"} for e in entities)

def test_classifier_predictions_have_confidence():
    texts=["identity verified valid", "cash mismatch missing", "sanction offshore expired adverse"]*2
    labels=["low","medium","high"]*2
    model=RiskClassifier().fit(texts,labels); result=model.predict(["sanction offshore alert"])[0]
    assert result[0] in labels and 0 <= result[1] <= 1

def test_corrupt_pdf_returns_defined_error(tmp_path):
    bad = tmp_path / "broken.pdf"
    bad.write_bytes(b"not a pdf")
    result = analyze_document(bad, object())
    assert result["status"] == "error" and "reason" in result
