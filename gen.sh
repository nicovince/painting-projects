#!/bin/bash -e

while read -r yml;
do
    ./gen_html.py "${yml}"
done < <(find . -name '*.yml')
