# Automated KYC & Document Risk Analyzer

An end-to-end NLP/ML lab that reads unstructured PDFs, extracts normalized entities, and returns a structured KYC risk verdict. The included documents are synthetic demonstration data—not real customer records or compliance advice.

## Architecture

`PDF → text/OCR detection → cleaning → NER → hybrid feature assembly → logistic-regression classifier → JSON report`

## Setup (Python 3.11 recommended)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Complete reproducible run

```bash
python scripts/generate_demo_data.py
python -m src.train
python -m src.run_pipeline --input_dir data/raw --output_file reports/run_results.json
python -m evaluation.evaluate
python -m pytest -q
```

Results are written to `reports/run_results.json` and `reports/metrics.json`; raw extraction snapshots go to `data/processed/`. To use Hugging Face NER, add `--ner transformer` to the pipeline command. The first execution downloads the selected model; regex mode is the reproducible offline default.

## Risk schema

- **Low:** information is present, consistent, and verified.
- **Medium:** missing information, unusual cash activity, or a mismatch requires manual review.
- **High:** sanctions, adverse media, expired evidence, or offshore/opaque ownership signals.

## Project structure

- `src/`: PDF ingestion, composable cleaning, NER, model, training, orchestration, and CLI.
- `scripts/`: synthetic dataset generator.
- `data/labels/inventory.csv`: gold inventory and deterministic split.
- `evaluation/`: metrics runner.
- `reports/architecture.md`: problem, entities, modeling decisions, features, dataset audit, and OCR policy.
- `reports/final_report.md`: verified results and error analysis.
- `tests/`: offline unit tests.

## Real-data extension

This small dataset demonstrates end-to-end integration; it is not large enough for a stable production classifier. For meaningful training, verify licensing and replace it with FUNSD/MIDV for document extraction plus FinBench or Gretel data for risk labels. Never use customer KYC data without authorization, access controls, encryption, retention limits, and compliance review.
