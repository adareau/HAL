# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 16:28:03
Modified : 2021-05-04 11:05:29

Comments : Functions related to data visualization
"""

# %% IMPORTS
import pyqtgraph as pg
import numpy as np

from PyQt5 import QtCore
from matplotlib import cm

# %% GLOBAL

IMPLEMENTED_COLORMAPS = [
    "Greiner",
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

GREINER = [
    [1.0000, 1.0000, 1.0000, 1.0000],
    [0.9474, 0.9474, 1.0000, 1.0000],
    [0.8947, 0.8947, 1.0000, 1.0000],
    [0.8421, 0.8421, 1.0000, 1.0000],
    [0.7895, 0.7895, 1.0000, 1.0000],
    [0.7368, 0.7368, 1.0000, 1.0000],
    [0.6842, 0.6842, 1.0000, 1.0000],
    [0.6316, 0.6316, 1.0000, 1.0000],
    [0.5789, 0.5789, 1.0000, 1.0000],
    [0.5263, 0.5263, 1.0000, 1.0000],
    [0.4737, 0.4737, 1.0000, 1.0000],
    [0.4211, 0.4211, 1.0000, 1.0000],
    [0.3684, 0.3684, 1.0000, 1.0000],
    [0.3158, 0.3158, 1.0000, 1.0000],
    [0.2632, 0.2632, 1.0000, 1.0000],
    [0.2105, 0.2105, 1.0000, 1.0000],
    [0.1579, 0.1579, 1.0000, 1.0000],
    [0.1053, 0.1053, 1.0000, 1.0000],
    [0.0526, 0.0526, 1.0000, 1.0000],
    [0.0000, 0.0000, 1.0000, 1.0000],
    [0.0000, 0.0769, 1.0000, 1.0000],
    [0.0000, 0.1538, 1.0000, 1.0000],
    [0.0000, 0.2308, 1.0000, 1.0000],
    [0.0000, 0.3077, 1.0000, 1.0000],
    [0.0000, 0.3846, 1.0000, 1.0000],
    [0.0000, 0.4615, 1.0000, 1.0000],
    [0.0000, 0.5385, 1.0000, 1.0000],
    [0.0000, 0.6154, 1.0000, 1.0000],
    [0.0000, 0.6923, 1.0000, 1.0000],
    [0.0000, 0.7692, 1.0000, 1.0000],
    [0.0000, 0.8462, 1.0000, 1.0000],
    [0.0000, 0.9231, 1.0000, 1.0000],
    [0.0000, 1.0000, 1.0000, 1.0000],
    [0.0769, 1.0000, 0.9231, 1.0000],
    [0.1538, 1.0000, 0.8462, 1.0000],
    [0.2308, 1.0000, 0.7692, 1.0000],
    [0.3077, 1.0000, 0.6923, 1.0000],
    [0.3846, 1.0000, 0.6154, 1.0000],
    [0.4615, 1.0000, 0.5385, 1.0000],
    [0.5385, 1.0000, 0.4615, 1.0000],
    [0.6154, 1.0000, 0.3846, 1.0000],
    [0.6923, 1.0000, 0.3077, 1.0000],
    [0.7692, 1.0000, 0.2308, 1.0000],
    [0.8462, 1.0000, 0.1538, 1.0000],
    [0.9231, 1.0000, 0.0769, 1.0000],
    [1.0000, 1.0000, 0.0000, 1.0000],
    [1.0000, 0.9231, 0.0000, 1.0000],
    [1.0000, 0.8462, 0.0000, 1.0000],
    [1.0000, 0.7692, 0.0000, 1.0000],
    [1.0000, 0.6923, 0.0000, 1.0000],
    [1.0000, 0.6154, 0.0000, 1.0000],
    [1.0000, 0.5385, 0.0000, 1.0000],
    [1.0000, 0.4615, 0.0000, 1.0000],
    [1.0000, 0.3846, 0.0000, 1.0000],
    [1.0000, 0.3077, 0.0000, 1.0000],
    [1.0000, 0.2308, 0.0000, 1.0000],
    [1.0000, 0.1538, 0.0000, 1.0000],
    [1.0000, 0.0769, 0.0000, 1.0000],
    [1.0000, 0.0000, 0.0000, 1.0000],
    [0.9000, 0.0000, 0.0000, 1.0000],
    [0.8000, 0.0000, 0.0000, 1.0000],
    [0.7000, 0.0000, 0.0000, 1.0000],
    [0.6000, 0.0000, 0.0000, 1.0000],
    [0.5000, 0.0000, 0.0000, 1.0000],
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
    # -- add some attributes to mainScreen
    # (will be useful for easy access to some data)
    # TODO : maybe we remove that in the future, and replace
    #        it by methods / attributes linked to the data display
    #        classes that will handle data visualization ?
    self.mainScreen.roi_list = []
    self.mainScreen.image_plot = None
    self.mainScreen.current_data = None
    self.mainScreen.current_image = None


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
    # lock aspect ratio
    p.setAspectLocked(lock=True, ratio=1)
    # set limits
    p.setLimits(
        xMin=0, yMin=0, xMax=data.data.shape[0], yMax=data.data.shape[1]
    )
    # axis
    p.setLabel("bottom", "X", units="px")
    p.setLabel("left", "Y", units="px")
    # p.setXRange(0, data.data.shape[0])
    # p.setYRange(0, data.data.shape[1])
    # image
    p.addItem(img)
    self.mainScreen.image_plot = p
    self.mainScreen.current_image = img
    # Get the colormap
    colormap_name = self.colorMapComboBox.currentText()
    if colormap_name == "Greiner":
        lut = np.array(GREINER) * 255
    else:
        colormap = cm.get_cmap(colormap_name)
        colormap._init()
        lut = (colormap._lut[:-1] * 255).view(
            np.ndarray
        )  # Convert matplotlib colormap from 0-1 to 0 -255 for Qt

    # greiner style ?
    # TODO : option ?
    if False:
        lut = np.append([[255, 255, 255, 255]], lut, axis=0)
    # Apply the colormap
    img.setLookupTable(lut)
    scale_min = float(self.scaleMinEdit.text())
    scale_max = float(self.scaleMaxEdit.text())
    # update
    img.updateImage(image=data.data, levels=(scale_min, scale_max))

    # add ROIS
    # FIXME: prelim
    for roi in self.mainScreen.roi_list:
        p.addItem(roi)

    self.mainScreen.current_data = data
