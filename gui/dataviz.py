# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 16:28:03
Modified : 2021-04-21 18:43:30

Comments : Functions related to data visualization
"""

# %% IMPORTS
import pyqtgraph as pg
import numpy as np

from PyQt5 import QtCore
from matplotlib import cm

# %% GLOBAL

IMPLEMENTED_COLORMAPS = [
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

# %% SETUP FUNCTIONS


def setupDataViz(self):
    # -- setup data classes list selector
    for name in self.data_classes.keys():
        self.dataTypeComboBox.addItem(name)
    # -- setup min / max scale
    self.scaleMinEdit.setText("0")
    self.scaleMaxEdit.setText("65535")
    # -- setup colormaps
    for cmap in IMPLEMENTED_COLORMAPS:
        self.colorMapComboBox.addItem(cmap)


# %% DISPLAY FUNCTIONS


def plotSelectedData(self):
    """
    loads the selected data, and plot it
    """
    # FIXME : preliminary, should call dataViz classes for displaying !
    # -- get selected data
    selection = self.runList.selectedItems()
    if not selection:
        return

    # -- init object data
    # get object data type
    data_type = self.dataTypeComboBox.currentText()
    data = self.data_classes[data_type]
    # get path
    item = selection[0]
    data.path = item.data(QtCore.Qt.UserRole)
    # check
    if not data.filter():
        print("ERROR")
        return
    # load
    data.load()

    # -- plot
    self.mainScreen.clear()
    img = pg.ImageItem()
    p = self.mainScreen.addPlot(0, 0)
    p.addItem(img)
    # Get the colormap
    colormap_name = self.colorMapComboBox.currentText()
    colormap = cm.get_cmap(colormap_name)
    colormap._init()
    lut = (colormap._lut * 255).view(
        np.ndarray
    )  # Convert matplotlib colormap from 0-1 to 0 -255 for Qt

    # Apply the colormap
    img.setLookupTable(lut)
    scale_min = float(self.scaleMinEdit.text())
    scale_max = float(self.scaleMaxEdit.text())
    img.updateImage(image=data.data, levels=(scale_min, scale_max))
