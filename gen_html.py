#!/usr/bin/env python3

import argparse
import logging
import sys
import yaml

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


class Paint:
    def __init__(self, manufacturer, painttype, name, colorcode):
        self.manufacturer = manufacturer
        self.painttype = painttype
        self.name = name
        self.colorcode = colorcode

class Stock:
    def __init__(self, file):
        stock_file = file
        self.stock = self.read_stock(file)

    def read_stock(self, yaml_stock):
        with open(yaml_stock, 'r') as f:
            stock = yaml.safe_load(f)
            return stock

    def get_manufacturers(self):
        return self.stock.keys()

    def get_paint(self, paintname):
        for manufacturer in self.stock:
            for paint_type in self.stock[manufacturer].keys():
                if paintname in self.stock[manufacturer][paint_type].keys():
                    return Paint(manufacturer, paint_type, paintname,
                                 self.stock[manufacturer][paint_type][paintname]['color'])
        assert False, f"Paint {paintname} not found in stock"
        return None


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

    def to_html(self, stock):
        html_str = f"{html_title(self.name, 2)}"
        for part in self.parts:
            html_str += f"{html_title(part, 3)}"
            part_paints  = []
            paints = self.parts[part]
            if type(paints) != list and type(paints) != dict:
                paints = [paints]

            logger.info(f"Paints: {paints} for {part}")
            for paintname in paints:
                part_paints.append(stock.get_paint(paintname))
            html_str += f"{html_table_paints(part_paints)}"
        return html_str


def generate(project, stock):
    html_file = f"{project.get_name()}.html"
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
    args = parser.parse_args()
    stock = Stock('stock.yml')
    project = Project(args.project)
    generate(project, stock)


if __name__ == "__main__":
    main()
