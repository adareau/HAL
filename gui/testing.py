# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-04 09:30:49
Modified : 2021-05-04 13:40:33

Comments : developer functions, meant to test / debug the gui
"""

# %% IMPORTS

# -- GLOBAL
from datetime import datetime
from pathlib import Path
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
    # TODO : when Victor's new function 'updateDayBrowser' is merged,
    #        rewrite this part of the code
    conf = self.settings.config
    root = Path(conf["data"]["root"])
    root = root.expanduser()
    year_fmt = conf["data"]["year folder"]
    month_fmt = conf["data"]["month folder"]
    day_fmt = conf["data"]["day folder"]

    # new path
    year = selected_date.strftime(year_fmt)
    month = selected_date.strftime(month_fmt)
    day = selected_date.strftime(day_fmt)
    day_dir = root / year / month / day

    # -- update current folder
    filebrowser.refreshCurrentFolder(self, day_dir)

    # -- update file browser
    # year
    year_items = self.yearList.findItems(year, Qt.MatchExactly)
    if year_items:
        # note : the month list will automatically update !!
        self.dayList.blockSignals(True)
        self.yearList.setCurrentItem(year_items[0])
        self.dayList.blockSignals(False)
    else:
        # if year not found, we stop here !
        return

    # month
    month_items = self.monthList.findItems(month, Qt.MatchExactly)
    if month_items:
        # note : the day list will automatically update !!
        self.dayList.blockSignals(True)
        self.monthList.setCurrentItem(month_items[0])
        self.dayList.blockSignals(False)
    else:
        # if month not found, we stop here !
        return

    # day
    day_items = self.dayList.findItems(day, Qt.MatchExactly)
    if day_items:
        # note : we prevent the dayListSelectionChanged to be trigged
        self.dayList.blockSignals(True)
        self.dayList.setCurrentItem(day_items[0])
        self.dayList.blockSignals(False)

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
