#!/usr/bin/env python

# https://stackoverflow.com/questions/31940285/plot-a-polar-color-wheel-based-on-a-colormap-using-python-matplotlib
# https://stackoverflow.com/questions/62531754/how-to-draw-a-hsv-color-wheel-using-matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colormaps
import matplotlib as mpl
import colorsys
from colors import *

fig = plt.figure()

display_axes = fig.add_axes([0.1,0.1,0.8,0.8], projection='polar')
display_axes._direction = 2*np.pi ## This is a nasty hack - using the hidden field to
                                  ## multiply the values such that 1 become 2*pi
                                  ## this field is supposed to take values 1 or -1 only!!

norm = mpl.colors.Normalize(0.0, 2*np.pi)

# Plot the colorbar onto the polar axis
# note - use orientation horizontal so that the gradient goes around
# the wheel rather than centre out
quant_steps = 2056
cb = mpl.colorbar.ColorbarBase(display_axes, cmap=colormaps.get_cmap('hsv'),
                                   norm=norm,
                                   orientation='horizontal')

# aesthetics - get rid of border and axis labels
cb.outline.set_visible(False)
display_axes.set_axis_off()

add_colors(display_axes, colors)
display_axes.legend()
plt.show() # Replace with plt.savefig if you want to save a file
