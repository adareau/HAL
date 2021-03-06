# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-04 09:30:49

Comments : developer functions, meant to test / debug the gui
"""

# %% IMPORTS

# -- GLOBAL
import logging
from datetime import datetime
from PyQt5.QtCore import Qt

# -- LOCAL
from . import filebrowser, dataexplorer, fitting, display
from ..classes.display import LiveMetaData

# -- logger
logger = logging.getLogger(__name__)

# %% FUNCTIONS


def open_image(self):
    """directly selects a given year/month/day in the filebrowser, and then
    a given image"""
    logger.debug("open_image()")

    # -- image selection
    year = 2020
    month = 1
    day = 2
    image = "001_001"
    selected_date = datetime(year, month, day)

    # -- set new path
    filebrowser.updateDayBrowser(self, selected_date)

    # -- refresh datasets
    dataexplorer.refreshDataSetList(self)

    # -- find item
    image_item = self.runList.findItems(image, Qt.MatchContains)
    if image_item:
        self.runList.setCurrentItem(image_item[0])


def open_image_and_fit(self):
    """directly selects a given year/month/day in the filebrowser, and then
    a given image"""
    logger.debug("open_image_and_fit()")

    # -- open image
    open_image(self)

    # -- set ROI and fit
    self.mainScreen.roi_list = []
    fitting.addROI(self)
    roi_names = self.display.getROINames()
    self.display.updateROI(roi_names[0], pos=(82, 100), size=(164, 94))
    fitting.fitData(self)


def declare_variables(self):
    """defines some variables in the variable declaration table"""
    table = self.variableDeclarationTable
    var_list = [
        ("x", "gus.TOF"),
        ("y", "HeV-fit.cx"),
        ("size", "file.size"),
        ("t", "file.timestamp"),
    ]
    for i, v in enumerate(var_list):
        table.item(i, 0).setText(v[0])
        table.item(i, 1).setText(v[1])


def select_livemetadata_display(self):
    for action in self.displaySelectionGroup.actions():
        displayClass = action.data()
        if isinstance(displayClass(), LiveMetaData):
            action.setChecked(True)
            display.displaySelectionChanged(self, action)
