# tagging-pipeline

- extracts passages from CapiTainS-compliant repos
- tags them using spaCy (just Latin for now)
- (soon) allows overriding with human-curated tagging

With dependencies installed in a venv, run `build.py repos.tsv`.

Then, run `tag.py`.

These scripts are re-entrant and detect changes by hashing their input and comparing to a hash stored in the output directory.
