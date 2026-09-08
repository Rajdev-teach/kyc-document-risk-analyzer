import json
from pathlib import Path
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from src.model import RiskClassifier
from src.ner import EntityExtractor
from src.pipeline import analyze_document

def main():
    df=pd.read_csv("data/labels/inventory.csv"); model=RiskClassifier.load("models/risk_classifier.joblib"); ner=EntityExtractor()
    results=[analyze_document(row.file_path,model,ner) for row in df.itertuples()]
    pred={r["document_id"]:r for r in results if r["status"]=="success"}; test=df[df.split=="test"]
    y_true=list(test.risk_label); y_pred=[pred[x]["risk_verdict"] for x in test.doc_id]
    labels=["low","medium","high"]
    report=classification_report(y_true,y_pred,labels=labels,zero_division=0,output_dict=True)
    cm=confusion_matrix(y_true,y_pred,labels=labels).tolist()
    presence=[]
    for row in df.itertuples():
        expected=set(row.expected_entities.split(",")); actual={e["type"] for e in pred[row.doc_id]["entities"]}
        presence.append(len(expected&actual)/len(expected))
    metrics={"test_accuracy":accuracy_score(y_true,y_pred),"classification_report":report,
             "confusion_matrix":{"labels":labels,"matrix":cm},"mean_ner_type_presence":sum(presence)/len(presence),
             "mean_runtime_seconds":sum(r["runtime_seconds"] for r in results)/len(results)}
    Path("reports").mkdir(exist_ok=True); Path("reports/metrics.json").write_text(json.dumps(metrics,indent=2))
    Path("reports/run_results.json").write_text(json.dumps(results,indent=2)); print(json.dumps(metrics,indent=2))
if __name__=="__main__": main()

