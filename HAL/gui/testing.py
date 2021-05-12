# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-04 09:30:49
Modified : 2021-05-07 14:58:12

Comments : developer functions, meant to test / debug the gui
"""

# %% IMPORTS

# -- GLOBAL
import logging
from datetime import datetime
from PyQt5.QtCore import Qt

# -- LOCAL
import HAL.gui.filebrowser as filebrowser
import HAL.gui.dataexplorer as dataexplorer
import HAL.gui.fitting as fitting

# -- logger
logger = logging.getLogger(__name__)

# %% FUNCTIONS


def open_image(self):
    """directly selects a given year/month/day in the filebrowser, and then
    a given image"""
    logger.debug('open_image()')

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
    logger.debug('open_image_and_fit()')

    # -- open image
    open_image(self)

    # -- set ROI and fit
    self.mainScreen.roi_list = []
    fitting.addROI(self)
    roi_names = self.display.getROINames()
    self.display.updateROI(roi_names[0], pos=(82, 100), size=(164, 94))
    fitting.fit_data(self)
