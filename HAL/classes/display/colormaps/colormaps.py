# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-06 10:10:40
Modified : 2021-05-07 14:59:58

Comments : Variables and functions related to colormaps, used by the display
           classes
"""

# %% IMPORTS

# -- global
import logging
import pyqtgraph as pg
import numpy as np
from matplotlib import cm

# -- local
from HAL.classes.display.colormaps.custom import colormap_dic

# -- logger
logger = logging.getLogger(__name__)


# %% GLOBAL VARIABLES

# -- list of matplotlib colormaps
MATPLOTLIB_COLORMAPS = [
    "Spectral_r",
    "viridis",
    "plasma",
    "inferno",
    "magma",
    "cividis",
    "Greys",
    "Purples",
    "Blues",
    "Greens",
    "Oranges",
    "Reds",
    "YlOrBr",
    "YlOrRd",
    "OrRd",
    "PuRd",
    "RdPu",
    "BuPu",
    "GnBu",
    "PuBu",
    "YlGnBu",
    "PuBuGn",
    "BuGn",
    "YlGn",
    "PiYG",
    "PRGn",
    "BrBG",
    "PuOr",
    "RdGy",
    "RdBu",
    "RdYlBu",
    "RdYlGn",
    "Spectral",
    "coolwarm",
    "bwr",
    "seismic",
]

# -- list of homemade colormaps
CUSTOM_COLORMAPS = list(colormap_dic.keys())

# -- ALL
IMPLEMENTED_COLORMAPS = CUSTOM_COLORMAPS + MATPLOTLIB_COLORMAPS


# %% FUNCTIONS
def get_pyqtgraph_lookuptable(colormap_name):
    global IMPLEMENTED_COLORMAPS, CUSTOM_COLORMAPS, MATPLOTLIB_COLORMAPS

    # -- check that colormap is implemented
    if colormap_name not in IMPLEMENTED_COLORMAPS:
        # if not implemented, we take the first colormap
        # and issue a warning
        msg = "'%s' colormap is not implement, use '%s' instead."
        logger.warning(msg % (colormap_name, IMPLEMENTED_COLORMAPS[0]))
        colormap_name = IMPLEMENTED_COLORMAPS[0]

    # -- generate the lookuptable
    # - for a matplotlib colormap
    if colormap_name in MATPLOTLIB_COLORMAPS:
        colormap = cm.get_cmap(colormap_name)
        colormap._init()
        lookuptable = (colormap._lut[:-1] * 255).view(
            np.ndarray
        )  # Convert matplotlib colormap from 0-1 to 0 -255 for Qt

    # - for a custom
    elif colormap_name in CUSTOM_COLORMAPS:
        lookuptable = np.array(colormap_dic[colormap_name]) * 255

    return lookuptable


# %% TESTS
if __name__ == "__main__":
    lut = get_pyqtgraph_lookuptable("Greiner")
    print(lut)
    lut = get_pyqtgraph_lookuptable("viridis")
    print(lut)
