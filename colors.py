#!/usr/bin/env python
import colorsys
import numpy as np

colors = {
    'Corax White': 0xffffff,
    'Abaddon Black': 0x000000,
    'Averland Sunset': 0xfbba00,
    'Mephiston Red': 0x9b0e05,
    'Caliban Green': 0x003b1d,
    'Kantor Blue': 0x06234f,
}

contrasts = {
    'Moody Mauve': 0xA65285,
    'Highlord Blue': 0x335884,
    'Space Wolves Grey': 0x92B2CB,
    'Absolution Green': 0x243B1F,
    'Plaguebearer Flesh': 0xCCD1A9,
    'Aggaros Dunes': 0xD5BF73,
    'Snakebite Leather': 0xB66E19,
    'Fire Giant Orange': 0xC84916,
    'Guilliman Flesh': 0xD5A79A,
    'Wyldwood': 0x715551,
    'Basilicanum Grey': 0x9D9D9D,
}

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

