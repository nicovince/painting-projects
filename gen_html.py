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
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    </head>'''

def html_style():
    return '''<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        line-height: 1.6;
        color: #333;
        background-color: #f9f9f9;
        padding: 1rem;
    }

    h1 {
        font-size: 1.75rem;
        margin-bottom: 1.5rem;
        text-align: center;
        color: #222;
    }

    h2 {
        font-size: 1.5rem;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        color: #333;
        border-bottom: 2px solid #ddd;
        padding-bottom: 0.5rem;
    }

    h3 {
        font-size: 1.1rem;
        margin-top: 1rem;
        margin-bottom: 0.75rem;
        color: #555;
    }

    .container {
        max-width: 1200px;
        margin: 0 auto;
    }

    .image-gallery {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .image-gallery img {
        width: 100%;
        height: auto;
        display: block;
        border-radius: 4px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }

    .image-gallery img:hover {
        transform: scale(1.05);
    }

    .table {
        width: 100%;
        overflow-x: auto;
        margin-bottom: 1.5rem;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        background-color: white;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border-radius: 4px;
        overflow: hidden;
    }

    tr {
        border-bottom: 1px solid #e0e0e0;
    }

    tr:last-child {
        border-bottom: none;
    }

    td {
        padding: 0.75rem 1rem;
        text-align: left;
    }

    td:first-child {
        display: flex;
        align-items: center;
        justify-content: center;
        min-width: 60px;
    }

    td:first-child div {
        width: 40px;
        height: 40px;
        border-radius: 2px;
        border: 1px solid #ddd;
    }

    /* Mobile: < 768px */
    @media (max-width: 767px) {
        body {
            padding: 0.75rem;
        }

        h1 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }

        h2 {
            font-size: 1.25rem;
            margin-top: 1.25rem;
        }

        h3 {
            font-size: 1rem;
        }

        .image-gallery {
            grid-template-columns: repeat(2, 1fr);
            gap: 0.75rem;
            margin-bottom: 1rem;
        }

        .table {
            margin-bottom: 1rem;
        }

        td {
            padding: 0.5rem 0.75rem;
            font-size: 0.9rem;
        }

        td:first-child div {
            width: 32px;
            height: 32px;
        }
    }

    /* Tablet: 768px - 1024px */
    @media (min-width: 768px) and (max-width: 1024px) {
        body {
            padding: 1.25rem;
        }

        .image-gallery {
            grid-template-columns: repeat(3, 1fr);
            gap: 1.25rem;
        }
    }

    /* Desktop: > 1024px */
    @media (min-width: 1025px) {
        .image-gallery {
            grid-template-columns: repeat(4, 1fr);
            gap: 1.5rem;
        }
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
    img = f"<img src='{filename}' alt='{alt}'>"
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
            html_str += "<div class='image-gallery'>"
            for p in self.pictures:
                html_str += f"{html_img(p, self.name)}"
            html_str += "</div>"
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
        f.write("<div class='container'>")
        f.write(html_title(project.get_name(), 1))
        for mini in project.project:
            figurine = Figurine(mini, project.project[mini])
            f.write(figurine.to_html(stock))
        f.write("</div>")
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
