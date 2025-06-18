#!/bin/bash -e

while read -r yml;
do
    ./gen_html.py "$(realpath --relative-to . "${yml}")"
done < <(find . -name '*.yml')
