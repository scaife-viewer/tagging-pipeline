#!/usr/bin/env python3

from hashlib import md5
from pathlib import Path

import spacy


spacy.prefer_gpu()


NLP = {
    "lat": spacy.load("la_core_web_trf", disable=["ner"]),
    "grc": spacy.load("grc_proiel_trf", disable=["ner"]),
} 

DATA_DIR = Path("data")

def get_files(directory):
    for group in directory.iterdir():
        for work in group.iterdir():
            for file in work.iterdir():
                if file.suffix == ".tsv" and ".tagged" not in file.stem:
                    if "lat" in file.stem:
                        yield "lat", file
                    elif "grc" in file.stem:
                        yield "grc", file

unchanged = 0
changed = 0

for shard in DATA_DIR.iterdir():
    for lang, file in get_files(shard):
        indata = open(file).read()
        hash = md5(indata.encode("utf-8")).hexdigest()
        work_dir = file.parent

        if work_dir.joinpath(f"{file.stem}.tagged.md5").exists() and open(work_dir.joinpath(f"{file.stem}.tagged.md5")).read() == hash:
            print(f"{file} unchanged")
            unchanged += 1
        else:
            runtime_error = False
            print(f"{file} changed", end="...")
            with open(file.with_suffix(".tagged.tsv"), "w") as outfile:
                for line in open(file):
                    print(".", end="", flush=True)
                    ref, text = line.rstrip("\n").split("\t")
                    try:
                        nlp = NLP[lang]
                        nlp.max_length = 2_000_000
                        doc = nlp(text)
                    except RuntimeError as e:
                        print(f"Error in {file}: {ref} : {e}")
                        runtime_error = True
                        break
                    for token in doc:
                        print(ref, token.i, token.text, token.pos_, token.tag_, token.morph, token.lemma_, token.dep_, token.head.i, sep="\t", file=outfile)
                if runtime_error:
                    continue
            print("tagged.")
            work_dir.joinpath(f"{file.stem}.tagged.md5").write_text(hash)
            changed += 1


print()
print(f"{changed} changed")
print(f"{unchanged} unchanged")
