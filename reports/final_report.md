# Final Evaluation Report

## Dataset summary

The held-out demonstration corpus contains 15 synthetic, selectable-text PDFs: five passports, five bank statements, and five business records. Risk labels are balanced (five each for low, medium, and high) and split deterministically into 9 training, 3 validation, and 3 test documents. No duplicates, scans, or real personal data were found. This is a wiring demonstration, not evidence of production-level model performance.

## Verified results

| Metric | Result |
|---|---:|
| Held-out classification accuracy | 1.000 (3/3) |
| Macro precision / recall / F1 | 1.000 / 1.000 / 1.000 |
| Mean NER expected-type presence | 0.767 |
| Mean end-to-end runtime | 0.0018 seconds/document |

Confusion matrix (rows=true, columns=predicted; order low, medium, high):

| | Low | Medium | High |
|---|---:|---:|---:|
| Low | 1 | 0 | 0 |
| Medium | 0 | 1 | 0 |
| High | 0 | 0 | 1 |

The perfect classifier result must be interpreted cautiously: the test set has only three synthetic documents and deliberately explicit risk language.

## NER and error analysis

Gold annotations contain expected entity types rather than exact character spans, so evaluation uses type presence rather than span precision/recall. The 0.767 mean shows that the regex fallback handles common identifiers, dates, money, organizations, locations, and labeled names but misses implicit entities and some organization-name shapes.

There were no held-out misclassifications. For useful qualitative review, the five lowest-confidence cases were doc_012 (predicted medium, 0.551), doc_004 (medium, 0.574), doc_013 (low, 0.621), doc_014 (medium, 0.622), and doc_001 (low, 0.678). Likely causes are the tiny training set, overlapping words such as “verified/unverified,” and limited semantic context. These are model/feature issues, not extraction failures.

## Focused fix and edge cases

The focused fix added bigram TF-IDF features so phrases such as “sanction match,” “address mismatch,” and “identity verified” remain distinct. This reduces collisions between positive and negative uses of similar words. A near-empty PDF returns a defined error state and requests OCR instead of producing a risk verdict. A conflicting document containing both verified and sanction/offshore signals is accepted by the classifier but should be routed to manual review in production; the current model reports its confidence rather than concealing ambiguity.

## Annotated sample

`doc_008_bank_statement.pdf` is classified **high**. The analyzer identifies the person, account number, organization, and `$850,000`, while the rationale notes explicit offshore, adverse-media, and sanctions signals. Each entity includes text offsets, page number, and confidence in `run_results.json`.

## Next steps

The slowest likely production stage is transformer NER/OCR, although regex-mode PDF extraction dominates this small run. Next steps are OCR benchmarking, exact-span gold labels, a larger licensed dataset, calibrated probabilities, threshold-based manual review, layout-aware models, encryption, and compliance validation.

