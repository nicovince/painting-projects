#!/usr/bin/env python

# https://stackoverflow.com/questions/31940285/plot-a-polar-color-wheel-based-on-a-colormap-using-python-matplotlib
# https://stackoverflow.com/questions/62531754/how-to-draw-a-hsv-color-wheel-using-matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colormaps
import matplotlib as mpl
import colorsys
from colors import *


def configure_axes(rowcolind):
    axes = plt.subplot(rowcolind, projection='polar')
    axes._direction = 2*np.pi ## This is a nasty hack - using the hidden field to
                              ## multiply the values such that 1 become 2*pi
                              ## this field is supposed to take values 1 or -1 only!!
    axes.set_axis_off()
    # Plot the colorbar onto the polar axis
    # note - use orientation horizontal so that the gradient goes around
    # the wheel rather than centre out
    norm = mpl.colors.Normalize(0.0, 2*np.pi)
    cb = mpl.colorbar.ColorbarBase(axes, cmap=colormaps.get_cmap('hsv'),
                                   norm=norm, orientation='horizontal')
    # aesthetics - get rid of border and axis labels
    cb.outline.set_visible(False)

    return axes

base_colors_axes = configure_axes(221)
contrast_axes = configure_axes(223)

add_colors(base_colors_axes, bases)
add_colors(contrast_axes, contrasts)
base_colors_axes.legend(bbox_to_anchor=(1.05, 1), loc=2)
contrast_axes.legend(bbox_to_anchor=(1.05, 1), loc=2)
plt.show() # Replace with plt.savefig if you want to save a file
