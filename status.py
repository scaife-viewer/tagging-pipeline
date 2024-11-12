#!/usr/bin/env python3

from pathlib import Path

DATA_DIR = Path("data")

count = 0
count_tagged = 0

for shard in DATA_DIR.iterdir():
    for group in shard.iterdir():
        for work in group.iterdir():
            for file in work.iterdir():
                if file.suffix == ".tsv" and ".tagged" not in file.stem:
                    count += 1
                    if file.with_suffix(".tagged.tsv").exists():
                        count_tagged += 1

print(f"{count_tagged} of {count} files tagged.")
