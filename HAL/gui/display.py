# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 16:28:03

Comments : Functions related to data visualization
"""

# %% IMPORTS

# -- global
import logging
import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QActionGroup
from PyQt5.QtGui import QKeySequence

# -- local
from . import fitting, advancedplot
from ..classes.display import LiveMetaData

# -- logger
logger = logging.getLogger(__name__)


# %% GLOBAL
SWITCH_DISPLAY_SHORTCUT = "ALT+SHIFT"


# %% SETUP FUNCTIONS


def setupUi(self):
    global SWITCH_DISPLAY_SHORTCUT

    # -- setup data classes list selector
    for data_class in self.data_classes:
        name = data_class().name
        self.dataTypeComboBox.addItem(name, data_class)

    # -- setup min / max scale
    data_class = self.dataTypeComboBox.currentData()
    sc_min, sc_max = data_class().default_display_scale
    self.scaleMinEdit.setText(str(sc_min))
    self.scaleMaxEdit.setText(str(sc_max))

    # -- initialize display
    # - display mode list
    # get list of implemented display types
    # we use a set {...} in order to get the values once
    display_type_set = {disp().type for disp in self.display_classes}
    # update the menu "Data Display" accordingly
    menu = self.menuDataDisplay
    self.menu_data_display_cat_list = {}
    for display_type in display_type_set:
        new_menu = menu.addMenu(display_type)  # add menu
        self.menu_data_display_cat_list[display_type] = new_menu  # store

    # chose default display
    default_display_name = "Basic 2D"  # FIXME migrate to config ?
    default_display = None
    if default_display_name not in self.display_classes:
        default_display_name = list(self.display_classes)[0]

    # add actions corresponding to available displays
    # we make it such that only one action can be selected
    # cf. https://stackoverflow.com/a/48447711
    displaySelectionGroup = QActionGroup(menu)  # group for display selection
    n_shortcut = 1
    for display in self.display_classes:
        display_type = display().type
        display_name = display().name
        displaySubmenu = self.menu_data_display_cat_list[display_type]
        action = QAction(
            display_name,
            displaySubmenu,
            checkable=True,
            checked=(display_name == default_display_name),
        )
        # set shortcut
        seq = "%s+%i" % (SWITCH_DISPLAY_SHORTCUT, n_shortcut)
        action.setShortcut(QKeySequence(seq))
        n_shortcut += 1
        # the display class is stored in the action data for later access
        action.setData(display)
        displaySubmenu.addAction(action)
        displaySelectionGroup.addAction(action)
        # did we find the default display ?
        if display == default_display_name:
            default_display = display

    # special case : the "live meta data" class
    # this is a basically empty class, used when we
    # switch to the "live metadata" display
    action = QAction(
        "Live metadata plot",
        menu,
        checkable=True,
        checked=(display_name == default_display_name),
    )
    action.setData(LiveMetaData)
    # keyboard shortcut
    seq = "%s+0" % SWITCH_DISPLAY_SHORTCUT
    action.setShortcut(QKeySequence(seq))
    action.setShortcut(QKeySequence(seq))
    # add
    menu.addAction(action)
    displaySelectionGroup.addAction(action)

    # set the group to be exclusive, and store it in self
    displaySelectionGroup.setExclusive(True)
    self.displaySelectionGroup = displaySelectionGroup

    # - setup display
    # if we did not find the default display name, use the first one in the list
    if default_display is None:
        default_display = self.display_classes[0]
    self.display = default_display(screen=self.mainScreen)
    self.display.setup()

    # setup colormaps
    colormap_list = self.display.getColormaps()
    for cmap in colormap_list:
        self.colorMapComboBox.addItem(cmap)


# %% DISPLAY FUNCTIONS


def displaySelectionChanged(self, action):
    """
    triggered when the display type selection is changed
    """
    # get the new requested display class
    display_class = action.data()

    # setup display
    self.display = display_class(screen=self.mainScreen)
    self.display.setup()

    # setup ROIs
    self.selectRoiComboBox.clear()

    # setup colormaps
    colormap_list = self.display.getColormaps()
    self.colorMapComboBox.clear()
    for cmap in colormap_list:
        self.colorMapComboBox.addItem(cmap)

    # refresh display
    plotSelectedData(self)
    advancedplot.updateSubplotLayout(self)
    advancedplot.refreshMetadataLivePlot(self)


def updateColormap(self):
    """
    Updates current colormap
    """
    # get the colormap
    colormap_name = self.colorMapComboBox.currentText()

    # update
    self.display.updateColormap(colormap_name)


def plotSelectedData(self, update_fit=True):
    """
    loads the selected data, and plots it
    """
    # -- get selected data
    selection = self.runList.selectedItems()
    if not selection:
        return

    # -- init object data
    # get object data type
    data_class = self.dataTypeComboBox.currentData()
    data = data_class()
    # get path
    item = selection[0]
    data.path = item.data(QtCore.Qt.UserRole)
    # check
    if not data.filter():
        print("ERROR")
        return
    # load
    data.load()

    # -- get the selected roi
    selected_roi = self.selectRoiComboBox.currentText()
    current_rois = self.display.getROINames()
    if current_rois and selected_roi not in current_rois:
        selected_roi = current_rois[0]

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
    if len(data.data) > 0:
        self.display.updatePlot(
            image=data.data,
            levels=(scale_min, scale_max),
            colormap=colormap_name,
            dataobject=data,
            selected_ROI=selected_roi,
        )

        # update fit
        if update_fit:
            updateFitForSelectedData(self)


def updateFitForSelectedData(self):
    """
    Load a saved fit for the selected data (if exist), and update
    the display accordingly
    """
    self.selectRoiComboBox.blockSignals(True)
    # -- clear current fit
    self.display.clearFit()
    # -- load saved fit
    fit_collection, fit_info = fitting.load_saved_fit(self)
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

    # -- update / create background
    if "background" in list(fit_info.keys()):
        self.backgroundCheckBox.setChecked(True)
        fitting.addBackground(self)
        pos = fit_info["background"]["pos"]["value"]
        size = fit_info["background"]["size"]["value"]
        self.display.updateBackground(pos=pos, size=size)
    else:
        self.backgroundCheckBox.setChecked(False)
        fitting.removeBackground(self)

    # -- update the fit
    selected_roi = self.selectRoiComboBox.currentText()
    # we take the first roi, if selected roi does not exist
    if selected_roi not in fit_collection:
        selected_roi = list(fit_collection.keys())[0]
    # get selected fit
    fit_dic = {roi_name: res["fit"] for roi_name, res in fit_collection.items()}
    self.display.updateFit(fit_dic, selected_roi)
    self.selectRoiComboBox.blockSignals(False)
