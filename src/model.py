"""Interpretable hybrid text and engineered-signal risk classifier."""
import re
from pathlib import Path
import joblib
import numpy as np
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

RISK_TERMS = ["sanction", "mismatch", "expired", "unverified", "cash", "offshore", "adverse", "missing"]

def engineered_features(texts):
    rows=[]
    for t in texts:
        lower=t.lower()
        rows.append([sum(lower.count(w) for w in RISK_TERMS), lower.count("$"),
                     len(re.findall(r"\b\d{7,}\b", t)), len(t), int("verified" in lower)])
    return csr_matrix(np.asarray(rows, dtype=float))

class RiskClassifier:
    """TF-IDF plus risk-term, money, long-number, length, and verification features."""
    def __init__(self):
        self.vectorizer=TfidfVectorizer(ngram_range=(1,2), min_df=1, max_features=3000)
        self.model=LogisticRegression(class_weight="balanced", max_iter=1000, random_state=42)
    def fit(self, texts, labels):
        x=hstack([self.vectorizer.fit_transform(texts), engineered_features(texts)])
        self.model.fit(x, labels); return self
    def predict(self, texts):
        x=hstack([self.vectorizer.transform(texts), engineered_features(texts)])
        labels=self.model.predict(x); probs=self.model.predict_proba(x)
        return [(str(label), float(max(prob))) for label, prob in zip(labels, probs)]
    def save(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True); joblib.dump(self, path)
    @staticmethod
    def load(path): return joblib.load(path)

