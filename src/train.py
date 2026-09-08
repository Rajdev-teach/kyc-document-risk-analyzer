import argparse
import pandas as pd
from pypdf import PdfReader
from src.cleaning import clean_text
from src.model import RiskClassifier

def pdf_text(path): return clean_text("\n".join((p.extract_text() or "") for p in PdfReader(path).pages))

def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--inventory", default="data/labels/inventory.csv")
    parser.add_argument("--model", default="models/risk_classifier.joblib"); args=parser.parse_args()
    df=pd.read_csv(args.inventory); train=df[df.split=="train"]
    model=RiskClassifier().fit([pdf_text(p) for p in train.file_path], train.risk_label)
    model.save(args.model); print(f"Trained on {len(train)} documents; saved {args.model}")
if __name__=="__main__": main()

