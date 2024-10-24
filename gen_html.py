#!/usr/bin/env python3

import argparse
import yaml

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

    def gen_part(part):
        paints = []
        for paintname in part:
            paints.append(stock.get_paint(paintname))

def html_table_paints(paints):
    paintnames = [p.name for p in paints]
    colorcodes = [p.colorcode for p in paints]
    return html_table(paintnames, colorcodes_to_html_divs(colorcodes))

def html_title(title, n):
    return f'<h{n}>{title}</h{n}>'

def generate(project, stock):
    print(html_header())
    print(html_head('pwet'))
    print("<body>")
    print(html_style())
    print(html_title(project.project_file, 1))
    for mini in project.project:
        print(html_title(mini, 2))
        for part in project.project[mini]:
            print(html_title(part, 3))
            part_paints = []

            paints = project.project[mini][part]
            for paintname in paints:
                part_paints.append(stock.get_paint(paintname))
                print(html_table_paints(part_paints))
    print("</body>")
    print('</html>')




def main():
    parser = argparse.ArgumentParser(prog='gen_html.py',
                                     description='Generate HTML file with colors used for figurines')
    parser.add_argument('project',
                        help=('Painting project yaml file containing the colors used in '
                              'a project.'))
    args = parser.parse_args()
    stock = Stock('stock.yml')
    #print(html_header())
    #print(html_head(args.project))
    #print("<body>")
    #print(html_style())
    #print(html_table(['Red', 'Green', 'Blue'], colorcodes_to_html_divs(['#ff0000', '#00ff00', '#0000ff'])))
    #print("</body>")
    #print('</html>')
    project = Project(args.project)
    generate(project, stock)




if __name__ == "__main__":
    main()
