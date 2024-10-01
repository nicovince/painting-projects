#!/usr/bin/env python

# https://stackoverflow.com/questions/31940285/plot-a-polar-color-wheel-based-on-a-colormap-using-python-matplotlib
# https://stackoverflow.com/questions/62531754/how-to-draw-a-hsv-color-wheel-using-matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colormaps
import matplotlib as mpl
import colorsys

def rgb_to_hsv(r, g, b):
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h = h * 2*np.pi
    print(f"{r=}, {g=}, {b=} -> {h=}, {s=}, {v=}")
    return (h, s, v)

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
display_axes.scatter(0, 1)
print(colorsys.rgb_to_hsv(1, 0, 0))
print(colorsys.rgb_to_hsv(1, 1, 0))
display_axes.scatter(*rgb_to_hsv(1, 1, 0)[0:2])
display_axes.scatter(*rgb_to_hsv(0.5, 0.4, 0)[0:2])
plt.show() # Replace with plt.savefig if you want to save a file
