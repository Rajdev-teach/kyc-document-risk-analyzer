# Architecture and Decisions

## Pipeline

PDF → per-page extraction → conservative cleaning → entity extraction → hybrid features → risk classifier → JSON report.

## Schema and success criteria

Inputs are unstructured KYC PDFs. The two ML tasks are entity extraction and document risk classification. Output is a structured verdict with entities, low/medium/high risk, confidence, rationale, provenance, and runtime. Low means identity and source information are consistent; medium means incomplete or reviewable anomalies; high means serious signals such as sanctions, expired evidence, adverse media, or opaque/offshore activity.

Success criteria are: mean NER type-presence ≥0.75 on the synthetic corpus, test classification accuracy ≥0.67, and mean runtime below one second per text-based PDF on a typical laptop.

## Documents and entities

- Passport: PERSON, DATE, GPE, ID_NUMBER; signals include expiration and identity mismatch.
- Bank statement: PERSON, ORG, MONEY, ID_NUMBER; signals include unexplained cash and offshore movement.
- Business registration: PERSON, ORG, DATE, GPE; signals include missing registration and opaque ownership.
- Address proof: PERSON, GPE, DATE; signals include mismatched addresses.
- Tax record: PERSON, ORG, MONEY, ID_NUMBER; signals include inconsistent identifiers and income.

The demo uses regex NER for deterministic offline execution. `--ner transformer` enables `dslim/bert-base-NER` (Apache-2.0, roughly 110M parameters, standard CoNLL PERSON/ORG/LOC/MISC labels). A surveyed alternative is `Jean-Baptiste/roberta-large-ner-english` (MIT, roughly 355M parameters); it can be stronger but is heavier. Domain-specific ID_NUMBER and MONEY rules complement general NER.

## Classifier

The model combines word/bigram TF-IDF with five engineered features: risk-keyword count, currency-symbol count, long-number count, document length, and verified-keyword presence. Logistic regression is fast and interpretable but cannot capture layout or nuanced semantic relationships. The nine-document training set only proves pipeline wiring; production metrics require a larger licensed dataset such as FinBench or Gretel Financial Risk Analysis.

## Data and OCR decisions

The 15 demonstration PDFs are synthetic, contain no PII, cover three document categories, and are split deterministically 9/3/3. The audit found balanced risk labels, no duplicates, and selectable text. Pages below 20 extracted characters are flagged `ocr_required_skipped`; OCR is deliberately skipped to avoid a system Tesseract dependency. Raw and cleaned content are never overwritten.

