# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-08 09:51:10
Modified : 2021-04-20 18:03:34

Comments : Functions related to file browsing, i.e. select the right year,
           month, day folders, and list the files inside.
"""

# %% IMPORTS
import os
from datetime import date
from pathlib import Path
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QIcon
from PyQt5.QtWidgets import QListWidgetItem, QStyle

# %% TOOLS


class EmptyIconProvider(QtWidgets.QFileIconProvider):
    def icon(self, _):
        return QtGui.QIcon()


# %% SETUP FUNCTIONS


def setupFileListBrowser(self):
    """Setup the file list browser (year, month, day)"""

    # -- definitions
    conf = self.settings.config
    root_str = os.path.expanduser(conf["data"]["root"])
    root = Path(root_str)
    qdir = QtCore.QDir

    # -- year
    # setup ListViewModel
    year_dir = root
    self.yearListViewModel = QtWidgets.QFileSystemModel()
    self.yearListViewModel.setRootPath(str(year_dir))
    self.yearListViewModel.setIconProvider(EmptyIconProvider())
    self.yearListViewModel.sort(0, QtCore.Qt.DescendingOrder)
    self.yearListViewModel.setFilter(
        qdir.Dirs | qdir.Drives | qdir.NoDotAndDotDot | qdir.AllDirs
    )
    # initialize ListView widget
    self.yearListView.setModel(self.yearListViewModel)
    idx = self.yearListViewModel.index(str(year_dir))
    self.yearListView.setRootIndex(idx)
    # scrollbar
    self.yearListView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.yearListView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    #

    # -- month
    # setup ListViewModel
    self.monthListViewModel = QtWidgets.QFileSystemModel()
    self.monthListViewModel.setRootPath("")
    self.monthListViewModel.setIconProvider(EmptyIconProvider())
    self.monthListViewModel.sort(0, QtCore.Qt.AscendingOrder)
    self.monthListViewModel.setFilter(
        qdir.Dirs | qdir.Drives | qdir.NoDotAndDotDot | qdir.AllDirs
    )
    # scrollbar
    self.monthListView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.monthListView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    # NB : no need to initialize ListView widget here
    self.monthListView.setModel(self.monthListViewModel)

    # -- day
    # setup ListViewModel
    self.dayListViewModel = QtWidgets.QFileSystemModel()
    self.dayListViewModel.setRootPath("")
    self.dayListViewModel.setIconProvider(EmptyIconProvider())
    self.dayListViewModel.sort(0, QtCore.Qt.AscendingOrder)
    self.dayListViewModel.setFilter(
        qdir.Dirs | qdir.Drives | qdir.NoDotAndDotDot | qdir.AllDirs
    )
    # scrollbar
    self.dayListView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.dayListView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    # NB : no need to initialize ListView widget here
    self.dayListView.setModel(self.dayListViewModel)

    # -- file list

    self.fileList.setIconSize(QSize(15, 15))
    self.fileList.addItems(['A', 'B', 'C'])
    # - custom item
    item = QListWidgetItem()
    item.setText('lol')
    item.setData(QtCore.Qt.UserRole, 'a path maybe ?')
    #item.setFont(QFont('Verdana', QFont.bold))
    item.setBackground(QColor(0, 0, 255))
    item.setForeground(QColor(255, 255, 255))
    # https://joekuan.files.wordpress.com/2015/09/screen3.png
    item.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
    self.fileList.addItem(item)
    # - otehr test
    self.fileList.addItems(['├─ hum', '└─ lol.png'])
    # -- calendar
    self.dateEdit.setCalendarPopup(True)
    self.dateEdit.setDateTime(QtCore.QDateTime.currentDateTime())

# %%  CALLBACKS


def yearListViewClicked(self, index):
    # get selected year
    indexItem = self.yearListViewModel.index(index.row(), 0, index.parent())
    yearPath = self.yearListViewModel.filePath(indexItem)
    # set month listview index
    self.monthListViewModel.setRootPath(yearPath)
    self.monthListView.setModel(self.monthListViewModel)
    idx = self.monthListViewModel.index(yearPath)
    self.monthListView.setRootIndex(idx)


def monthListViewClicked(self, index):
    # get selected month
    indexItem = self.monthListViewModel.index(index.row(), 0, index.parent())
    monthPath = self.monthListViewModel.filePath(indexItem)
    # set month listview index
    self.dayListViewModel.setRootPath(monthPath)
    self.dayListView.setModel(self.dayListViewModel)
    idx = self.dayListViewModel.index(monthPath)
    self.dayListView.setRootIndex(idx)


def dayListViewClicked(self, index):
    # get selected month
    indexItem = self.dayListViewModel.index(index.row(), 0, index.parent())
    dayPath = self.dayListViewModel.filePath(indexItem)

    # change current folder
    changeCurrentFolder(self, Path(dayPath))


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
    year_fmt = conf['data']['year folder']
    year_folder = selected_date.strftime(year_fmt)
    year_path = root / year_folder

    self.monthListViewModel.setRootPath(str(year_path))
    self.monthListView.setModel(self.monthListViewModel)
    idx = self.monthListViewModel.index(str(year_path))
    self.monthListView.setRootIndex(idx)

    # month
    month_fmt = conf['data']['month folder']
    month_folder = selected_date.strftime(month_fmt)
    month_path = year_path / month_folder

    self.dayListViewModel.setRootPath(str(month_path))
    self.dayListView.setModel(self.dayListViewModel)
    idx = self.dayListViewModel.index(str(month_path))
    self.dayListView.setRootIndex(idx)

    # day
    day_fmt = conf['data']['day folder']
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
        self.fileList.addItems(['Folder does not exists'])
        return

