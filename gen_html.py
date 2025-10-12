#!/usr/bin/env python3

import argparse
import logging
import sys
import yaml
import os
from stock import Stock
from paint import Paint

logger = logging.getLogger('PP')

def colorcode_to_html_div(colorcode):
    nbsp = '&nbsp'
    return f'<div style="background-color: #{colorcode:06x}">{4*nbsp}</div>'

def colorcodes_to_html_divs(colorcodes):
    html_array = []
    nbsp = '&nbsp'
    for colorcode in colorcodes:
        html_array.append(colorcode_to_html_div(colorcode))
    return html_array

def html_header():
    return '''<!DOCTYPE html>'''

def html_head(title):
    return f'''<head>
    <title>{title}</title>
    </head>'''

def html_style():
    return ''
    return '''<style>
    .table {
        width: 10%;
        margin: auto;
    }
    </style>'''

def html_table(colornames, html_divs):
    table = []
    table.append("  <div class='table'>")
    table.append("    <table>")
    for colorname, html_div in zip(colornames, html_divs):
        table.append("      <tr>")
        table.append(f'        <td>{html_div}</td>')
        table.append(f'        <td>{colorname}</td>')
        table.append("      </tr>")
    table.append("    </table>")
    table.append("  </div>")
    return '\n'.join(table)

def html_img(filename, alt):
    img = f"<img src='{filename}' alt='{alt}' width='20%' height='20%'>"
    return img


class Project:
    def __init__(self, project_file):
        self.project_file = project_file
        self.project = self.read_project()

    def read_project(self):
        with open(self.project_file, 'r') as f:
            project = yaml.safe_load(f)
        return project

    def get_name(self):
        return self.project_file.split('.')[0]


def html_table_paints(paints):
    paintnames = [p.name for p in paints]
    colorcodes = [p.colorcode for p in paints]
    return html_table(paintnames, colorcodes_to_html_divs(colorcodes))

def html_title(title, n):
    return f'<h{n}>{title}</h{n}>'


class Figurine:
    def __init__(self, name, parts):
        self.name = name
        self.parts = parts
        self.pictures = None
        if "pictures" in parts.keys():
            self.pictures = self.parts.pop("pictures")

    def to_html(self, stock):
        html_str = f"{html_title(self.name, 2)}"
        if self.pictures is not None:
            for p in self.pictures:
                html_str += f"{html_img(p, self.name)}"
        for part in self.parts:
            html_str += f"{html_title(part, 3)}"
            part_paints  = []
            paints = self.parts[part]
            if type(paints) != list and type(paints) != dict:
                paints = [paints]

            logger.debug(f"Paints: {paints} for {part}")
            for paintname in paints:
                part_paints.append(stock.get_paint(paintname))
            html_str += f"{html_table_paints(part_paints)}"
        return html_str

    def __str__(self):
        s = ""
        s += f"{self.name}:\n"
        for p in self.parts:
            s += f"  - {p}\n"
            for c in self.parts[p]:
                s += f"    - {c}\n"
        return s


def generate(project, stock, out_dir):
    html_file = f"{out_dir}/{project.get_name()}.html"
    # Create out_dir
    os.makedirs(out_dir, exist_ok=True)
    logger.info("Processing %s", project.project_file)
    with open(html_file, 'w') as f:
        f.write(html_header())
        f.write(html_head(project.get_name()))
        f.write("<body>")
        f.write(html_style())
        f.write(html_title(project.get_name(), 1))
        for mini in project.project:
            figurine = Figurine(mini, project.project[mini])
            f.write(figurine.to_html(stock))
        f.write("</body>")
        f.write('</html>')


def main():
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    parser = argparse.ArgumentParser(prog='gen_html.py',
                                     description='Generate HTML file with colors used for figurines')
    parser.add_argument('project',
                        help=('Painting project yaml file containing the colors used in '
                              'a project.'))
    parser.add_argument("--output-folder", default="./output/",
                        help='Folder where html pages are created.')
    args = parser.parse_args()
    stock = Stock('stock.yml')
    project = Project(args.project)
    generate(project, stock, args.output_folder)


if __name__ == "__main__":
    main()
