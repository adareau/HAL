# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 16:28:03
Modified : 2021-05-06 14:44:34

Comments : Functions related to data visualization
"""

# %% IMPORTS

# -- global
import numpy as np
from PyQt5 import QtCore

# -- local
import HAL.gui.fitting as fitting

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
        image=data.data,
        levels=(scale_min, scale_max),
        colormap=colormap_name,
        dataobject=data,
    )

    # update fit
    updateFitForSelectedData(self)


def updateFitForSelectedData(self):
    """
    Load a saved fit for the selected data (if exist), and update
    the display accordingly
    """
    # -- load saved fit
    fit_collection = fitting.load_saved_fit(self)
    if fit_collection is None:
        return

    # -- update / create rois
    current_rois = self.display.getROINames()
    for roi_name, roi_data in fit_collection.items():
        # get pos and size
        roi_pos = roi_data["pos"]["value"]
        roi_size = roi_data["size"]["value"]
        # create if does not exist
        if roi_name not in current_rois:
            fitting.addROI(self, roi_name=roi_name)
        # update
        self.display.updateROI(roi_name, pos=roi_pos, size=roi_size)

    # -- update the fit
    # FIXME : let the user choose the selected roi !!!
    selected_roi = ""
    # we take the first roi, if selected roi does not exist
    if selected_roi not in fit_collection:
        selected_roi = list(fit_collection.keys())[0]
    # get selected fit
    fit = fit_collection[selected_roi]['fit']
    self.display.updateFit(fit, selected_roi)
