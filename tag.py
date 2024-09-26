#!/usr/bin/env python3

from hashlib import md5
from pathlib import Path

import spacy


nlp = {
    "lat": spacy.load("la_core_web_trf"),
} 

DATA_DIR = Path("data")

def get_files(directory):
    for group in directory.iterdir():
        for work in group.iterdir():
            for file in work.iterdir():
                if file.suffix == ".tsv" and ".tagged" not in file.stem:
                    if "lat" in file.stem:
                        yield "lat", file

unchanged = 0
changed = 0

for lang, file in get_files(DATA_DIR):
    indata = open(file).read()
    hash = md5(indata.encode("utf-8")).hexdigest()
    work_dir = file.parent

    if work_dir.joinpath(f"{file.stem}.tagged.md5").exists() and open(work_dir.joinpath(f"{file.stem}.tagged.md5")).read() == hash:
        print(f"{file} unchanged")
        unchanged += 1
    else:
        print(f"{file} changed", end="...")
        with open(file.with_suffix(".tagged.tsv"), "w") as outfile:
            for line in open(file):
                print(".", end="", flush=True)
                ref, text = line.rstrip("\n").split("\t")
                doc = nlp[lang](text)
                for token in doc:
                    print(ref, token.i, token.text, token.pos_, token.tag_, token.morph, token.lemma_, token.dep_, token.head.i, sep="\t", file=outfile)
        print("tagged.")
        work_dir.joinpath(f"{file.stem}.tagged.md5").write_text(hash)
        changed += 1


print()
print(f"{changed} changed")
print(f"{unchanged} unchanged")
