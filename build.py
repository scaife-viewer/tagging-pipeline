#!/usr/bin/env python3

import re
import sys

from hashlib import md5
from pathlib import Path

from lxml.etree import XPathEvalError, XMLSyntaxError
from MyCapytain.errors import MissingRefsDecl
from MyCapytain.resources.texts.local.capitains.cts import CapitainsCtsText

if len(sys.argv) != 2:
    print("Usage: build.py <repo_file>")
    sys.exit(1)

REPO_FILE = sys.argv[1]

repos = [
    line.strip().split("\t") for line in open(REPO_FILE)
]


def get_files(directory):
    for group in directory.iterdir():
        if group.is_dir():
            for work in group.iterdir():
                if work.is_dir():
                    for file in work.iterdir():
                        if file.suffix == ".xml" and ("grc" in file.stem or "lat" in file.stem):
                            yield group.name, work.name, file.stem, file


def get_passages(text):

    try:
        for ref in text.getReffs(level=len(text.citation)):
            node = text.getTextualNode(ref)
            yield ref, node.text
    except XPathEvalError:
        print(f"error with {text.urn}")


DATA_DIR = Path("data")

changed = 0
unchanged = 0

for repo, urn_prefix in repos:
    print()
    print(f"Processing {repo}")
    directory = Path(repo) / "data"
    for group, work, stem, file in get_files(directory):
        urn = f"{urn_prefix}:{group}.{work}.{stem}"
        try:
            text = CapitainsCtsText(urn=urn, resource=open(file))
        except MissingRefsDecl:
            continue  # @@@ log
        except XMLSyntaxError:
            continue  # @@@ log

        hash = md5(text.text.encode("utf-8")).hexdigest()

        work_dir = DATA_DIR / group / work
        work_dir.mkdir(exist_ok=True, parents=True)

        if work_dir.joinpath(f"{stem}.md5").exists() and open(work_dir.joinpath(f"{stem}.md5")).read() == hash:
            print(".", end="", flush=True)  # print(f"{urn} unchanged")
            unchanged += 1
        else:
            print(f"{urn} changed", end="...")
            with open(work_dir.joinpath(f"{stem}.tsv"), "w") as outfile:
                for ref, text in get_passages(text):
                    text = re.sub(r"\s+", " ", text)
                    outfile.write(f"{ref}\t{text}\n")
            work_dir.joinpath(f"{stem}.md5").write_text(hash)
            changed += 1
            print("built.")

print()
print(f"{changed} changed")
print(f"{unchanged} unchanged")
