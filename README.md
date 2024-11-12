# tagging-pipeline

- extracts passages from CapiTainS-compliant repos
- tags them using spaCy
- (soon) allows overriding with human-curated tagging

Each of the shards under `data/` needs to be cloned.

Then, with dependencies installed in a venv, run `build.py repos.tsv`.

Then, run `tag.py`.

These scripts are re-entrant and detect changes by hashing their input and comparing to a hash stored in the output directory.

Note that the lowest-level citeable chunks are passed into spaCy individually which is often not desirable (at least for the dependency annotation) so further work is definitely needed in this area.

If you have more texts you would like included, please let me know. New texts don't have to be CapiTainS-compliant. The flat "ref + text" TSV format produced by `build.py` would suffice.

## notes on getting things working

To work with `uv` in particular, I had to do the following

- downgrade to Python 3.11
- download the grecy and latincy wheels and renamed them with explicit versions 3.7.5 and 3.7.7 respectively
