#!/usr/bin/env python
import colorsys
import numpy as np
from stock import Stock

stock = Stock('stock.yml')
bases = stock.get_paints_by_type('Base')
contrasts = stock.get_paints_by_type('Contrast')
contrasts.update(stock.get_paints_by_type('Speed Paint'))

def hexcode_to_rgb(code):
    r = ((code >> 16) & 0xff) / 0xff
    g = ((code >> 8) & 0xff) / 0xff
    b = ((code >> 0) & 0xff) / 0xff
    return (r, g, b)

def rgb_to_hsv(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h = h * 2*np.pi
    print(f"{r=}, {g=}, {b=} -> {h=}, {s=}, {v=}")
    return (h, s, v)

def add_colors(axes, colors):
    for c in colors:
        r, g, b = hexcode_to_rgb(colors[c])
        h, s, v = rgb_to_hsv(r, g, b)
        axes.scatter(h, s, label=c, c=[r, g, b], edgecolors='black')

