#!/bin/bash -e
OUT_DIR="${1:-output}"

while read -r yml;
do
    ./gen_html.py "$(realpath --relative-to . "${yml}")" --output-folder "${OUT_DIR}"
done < <(find . -maxdepth 1 -name '*.yml')

cp -r pics/ "${OUT_DIR}"
