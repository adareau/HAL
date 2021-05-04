# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-04 09:30:49
Modified : 2021-05-04 15:32:39

Comments : developer functions, meant to test / debug the gui
"""

# %% IMPORTS

# -- GLOBAL
from datetime import datetime
from PyQt5.QtCore import Qt

# -- LOCAL
import HAL.gui.filebrowser as filebrowser
import HAL.gui.dataexplorer as dataexplorer
import HAL.gui.fitting as fitting

# %% FUNCTIONS


def open_image(self):
    """directly selects a given year/month/day in the filebrowser, and then
    a given image"""
    print(">> TESTING : open_image")

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
    print(">> TESTING : open_image_and_fit")

    # -- open image
    open_image(self)

    # -- set ROI and fit
    self.mainScreen.roi_list = []
    fitting.addROI(self)
    roi = self.mainScreen.roi_list[0]
    roi.setPos((82, 100), finish=True, update=True)
    roi.setSize((164, 94), finish=True, update=True)
    fitting.fit_data(self)
