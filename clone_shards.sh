#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="${1:-./data}"

for i in $(seq -w 1 23); do
    repo="tagging-shard-${i}"
    target="${BASE_DIR}/${repo}"
    if [ -d "$target" ]; then
        echo "Skipping ${repo} (already exists)"
    else
        git clone "git@github.com:scaife-viewer/${repo}.git" "$target"
    fi
done
