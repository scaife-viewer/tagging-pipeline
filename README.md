# tagging-pipeline

- extracts passages from CapiTainS-compliant repos
- (soon) tags them using spaCy
- (later) allows overriding with human-curated tagging

In a venv with `requirements.txt` installed, run `build.py repos.tsv`.

This script is re-entrant and detects changes by hashing the text and comparing to a hash stored in the output directory.
