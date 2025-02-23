import logging
import sys
import yaml

from paint import Paint

logger = logging.getLogger('stock')

class YmlFile:
    def __init__(self, filename):
        self.file = filename

    def read_file(self):
        with open(self.file, 'r') as f:
            content = yaml.safe_load(f)
        return content

class Stock(YmlFile):
    def __init__(self, filename):
        YmlFile.__init__(self, filename)
        self.stock = self.read_file()

    def get_paint(self, paintname):
        for manufacturer in self.stock:
            for paint_type in self.stock[manufacturer].keys():
                if paintname in self.stock[manufacturer][paint_type].keys():
                    return Paint(manufacturer, paint_type, paintname,
                                 self.stock[manufacturer][paint_type][paintname]['color'])
        logger.warning("Paint %s not found in stock", paintname)
        return Paint.placeholder(paintname)
