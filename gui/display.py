# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 16:28:03
Modified : 2021-05-06 11:39:32

Comments : Functions related to data visualization
"""

# %% IMPORTS
import numpy as np

from PyQt5 import QtCore


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
