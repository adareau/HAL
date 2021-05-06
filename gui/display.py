# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 16:28:03
Modified : 2021-05-06 11:36:24

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


def setupDisplay(self):
    # -- setup data classes list selector
    for name in self.data_classes.keys():
        self.dataTypeComboBox.addItem(name)
    # -- setup min / max scale
    self.scaleMinEdit.setText("0")
    self.scaleMaxEdit.setText("65535")

    # -- initialize display
    # TODO update the menu !
    display_list = list(self.display_classes.keys())

    # setup display
    display_class = self.display_classes["Basic image display"]
    self.display = display_class(screen=self.mainScreen)
    self.display.setup()

    # setup colormaps
    colormap_list = self.display.getColormaps()
    for cmap in colormap_list:
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


def updateColormap(self):
    """
    Updates current colormap
    """
    # get the colormap
    colormap_name = self.colorMapComboBox.currentText()

    # update
    self.display.updateColormap(colormap_name)


def plotSelectedData(self):
    """
    loads the selected data, and plot it
    """
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
    # TODO: we should ensure that the selected data type
    # matches the current display object type! For instance,
    # if an image is selected, the current display should take
    # a 2D array as an input !

    # get the colormap
    colormap_name = self.colorMapComboBox.currentText()

    # get the scale
    if self.autoScaleCheckBox.isChecked():
        scale_min = np.min(data.data)
        scale_max = np.max(data.data)
    else:
        scale_min = float(self.scaleMinEdit.text())
        scale_max = float(self.scaleMaxEdit.text())

    # plot
    self.display.updatePlot(
        image=data.data, levels=(scale_min, scale_max), colormap=colormap_name
    )

    # remove ROI
    # FIXME: we should manage roi conservation when uploading a new image...
    # maybe we should not clear the screen ?
    # self.mainScreen.roi_list = []
    self.mainScreen.current_data = data
