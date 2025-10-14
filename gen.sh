#!/bin/bash -e
OUT_DIR="${1:-output}"
INDEX="${OUT_DIR}/index.html"

gen_header()
{
    echo "<!DOCTYPE html>"
    echo "<head>"
    echo "<title> Painting Projects</title>"
    echo "</head>"
    echo "<body>"
}

gen_link()
{
    local project="$1"
    echo "<h3><a href='${project}.html'>${project}</a></h3>"
}
gen_footer()
{
    echo "</body>"
    echo "</html>"
}

mkdir -p "${OUT_DIR}"
gen_header > "${INDEX}"

while read -r yml;
do
    ./gen_html.py "$(realpath --relative-to . "${yml}")" --output-folder "${OUT_DIR}"
    gen_link "${yml%%.yml}" >> "${INDEX}"
done < <(find . -maxdepth 1 -name '*.yml')

gen_footer >> "${INDEX}"

cp -r pics/ "${OUT_DIR}"
