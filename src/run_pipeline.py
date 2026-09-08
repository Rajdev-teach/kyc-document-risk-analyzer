import argparse, json, logging
from pathlib import Path
from src.model import RiskClassifier
from src.ner import EntityExtractor
from src.pipeline import analyze_document

def main():
    p=argparse.ArgumentParser(description="Run KYC document risk analysis")
    p.add_argument("--input_dir", default="data/raw"); p.add_argument("--output_file", default="reports/run_results.json")
    p.add_argument("--model", default="models/risk_classifier.joblib"); p.add_argument("--ner", choices=["regex","transformer"], default="regex")
    a=p.parse_args(); logging.basicConfig(level=logging.INFO)
    clf=RiskClassifier.load(a.model); extractor=EntityExtractor(a.ner)
    results=[analyze_document(path, clf, extractor) for path in sorted(Path(a.input_dir).glob("*.pdf"))]
    target=Path(a.output_file); target.parent.mkdir(parents=True,exist_ok=True); target.write_text(json.dumps(results,indent=2))
    print(f"Processed {len(results)} PDFs; results saved to {target}")
if __name__=="__main__": main()

