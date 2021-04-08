# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-08 09:51:10
Modified : 2021-04-08 11:23:48

Comments : Functions related to file browsing, i.e. select the right year,
           month, day folders, and list the files inside.
"""

# %% IMPORTS
import os
from pathlib import Path
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt

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
    self.fileList.addItems(['A', 'B', 'C'])

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
    print(dayPath)
