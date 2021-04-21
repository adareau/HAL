# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-08 09:51:10
Modified : 2021-04-21 10:35:56

Comments : Functions related to file browsing, i.e. select the right year,
           month, day folders, and list the files inside.
"""

# %% IMPORTS
import os
from datetime import date, datetime
from pathlib import Path
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QIcon
from PyQt5.QtWidgets import QListWidgetItem, QStyle

# %% TOOLS


class EmptyIconProvider(QtWidgets.QFileIconProvider):
    def icon(self, _):
        return QtGui.QIcon()


def validateDateFormat(date_string, date_format):
    try:
        # if this fails, then format is bad
        date_object = datetime.strptime(date_string, date_format)
        # this is to ensuire zero paddings
        if date_string != date_object.strftime(date_format):
            raise ValueError
        return True
    except ValueError:
        return False


# %% LOW LEVEL FUNCTIONS


def getSubfolders(folder_path, date_format):
    """
    analyzes folder, looking for subfolders with the right date format
    folder_path needs to be a pathlib.Path() object
    """
    # if the path does no correspond to a directory : return
    if not folder_path.is_dir():
        return []

    # browse folder content
    selected_content = []
    for content in folder_path.iterdir():
        if content.is_dir() and validateDateFormat(content.name, date_format):
            selected_content.append(content)

    return selected_content


def refreshListContent(list, folder, date_format):
    """
    Low-level function to refresh the content of the
    year / month / day lists
    """
    # clear current content
    list.clear()

    # analyze folder
    subdir_list = getSubfolders(folder, date_format)
    subdir_list.sort(reverse=False)

    # populate list
    for subdir in subdir_list:
        item = QListWidgetItem()
        item.setText(subdir.name)
        item.setData(QtCore.Qt.UserRole, subdir)
        list.addItem(item)


# %% SETUP FUNCTIONS


def setupFileListBrowser(self):
    """Setup the file list browser (year, month, day)"""

    # -- definitions : setup root
    conf = self.settings.config
    root = Path(conf["data"]["root"])
    root = root.expanduser()

    # -- year
    # initialize year list
    year_fmt = conf["data"]["year folder"]
    refreshListContent(self.yearList, root, year_fmt)

    # scrollbar
    self.yearList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.yearList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    # -- month
    # scrollbar
    self.monthList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.monthList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    # -- day
    # scrollbar
    self.dayList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.dayList.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    # -- file list
    self.fileList.setIconSize(QSize(15, 15))
    self.fileList.addItems(["A", "B", "C"])
    # - custom item
    item = QListWidgetItem()
    item.setText("lol")
    item.setData(QtCore.Qt.UserRole, "a path maybe ?")
    # item.setFont(QFont('Verdana', QFont.bold))
    item.setBackground(QColor(0, 0, 255))
    item.setForeground(QColor(255, 255, 255))
    # https://joekuan.files.wordpress.com/2015/09/screen3.png
    item.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
    self.fileList.addItem(item)
    # - otehr test
    self.fileList.addItems(["├─ hum", "└─ lol.png"])
    # -- calendar
    self.dateEdit.setCalendarPopup(True)
    self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())


# %%  CALLBACKS


def yearListSelectionChanged(self):
    # if nothing seleted, return
    if not self.yearList.selectedItems():
        return
    # get selected year
    year = self.yearList.selectedItems()[0]
    year_dir = year.data(QtCore.Qt.UserRole)
    # get month formatting
    conf = self.settings.config
    month_fmt = conf["data"]["month folder"]
    # refresh month list
    refreshListContent(self.monthList, year_dir, month_fmt)
    # clear day list
    self.dayList.clear()


def monthListSelectionChanged(self):
    # if nothing seleted, return
    if not self.monthList.selectedItems():
        return
    # get selected month
    month = self.monthList.selectedItems()[0]
    month_dir = month.data(QtCore.Qt.UserRole)
    # get day formatting
    conf = self.settings.config
    day_fmt = conf["data"]["day folder"]
    # refresh day list
    refreshListContent(self.dayList, month_dir, day_fmt)


def dayListSelectionChanged(self):
    # if nothing seleted, return
    if not self.dayList.selectedItems():
        return
    # get selected day
    day = self.dayList.selectedItems()[0]
    day_dir = day.data(QtCore.Qt.UserRole)
    print(day_dir)


def dateEditClicked(self):
    # -- get selected date
    selected_date = self.dateEdit.date()  # QDate format
    selected_date = selected_date.toPyDate()  # datetime.date format

    # -- update file browser
    # get config
    conf = self.settings.config
    root_str = os.path.expanduser(conf["data"]["root"])
    root = Path(root_str)

    # year
    year_fmt = conf["data"]["year folder"]
    year_folder = selected_date.strftime(year_fmt)
    year_path = root / year_folder

    self.monthListViewModel.setRootPath(str(year_path))
    self.monthListView.setModel(self.monthListViewModel)
    idx = self.monthListViewModel.index(str(year_path))
    self.monthListView.setRootIndex(idx)

    # month
    month_fmt = conf["data"]["month folder"]
    month_folder = selected_date.strftime(month_fmt)
    month_path = year_path / month_folder

    self.dayListViewModel.setRootPath(str(month_path))
    self.dayListView.setModel(self.dayListViewModel)
    idx = self.dayListViewModel.index(str(month_path))
    self.dayListView.setRootIndex(idx)

    # day
    day_fmt = conf["data"]["day folder"]
    day_folder = selected_date.strftime(day_fmt)
    day_path = month_path / day_folder

    # --
    changeCurrentFolder(self, day_path)


def changeCurrentFolder(self, new_folder):
    # -- update gui file browser
    self.current_folder = new_folder

    # -- check that the folder exists
    if not new_folder.is_dir():
        self.fileList.clear()
        self.fileList.addItems(["Folder does not exists"])
        return
