#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Author   : alex
Created  : 2020-09-11 15:18:05
Modified : 2021-04-08 11:19:14

Comments :
"""
# %% IMPORTS

# -- global
import sys
from PyQt5 import QtWidgets

# -- local
import HAL.gui.filebrowser as filebrowser
from HAL.gui.MainUI import Ui_mainWindow
from HAL.classes.dummy import Dummy
from HAL.classes.settings import Settings


# %% DEFINE GUI CLASS


class MainWindow(QtWidgets.QMainWindow, Ui_mainWindow):

    # == INITIALIZATIONS

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # -- FIRST : load settings
        self.settings = Settings()

        # -- GUI related initializations
        # setup UI (as defined in HAL.gui.MainUI)
        self.setupUi(self)
        # setup UI (define here)
        self.setupElements()
        # connect callbacks
        self.connectActions()

        # -- Other initializations
        self.dummy = Dummy()

    def setupElements(self):
        # -- File Browser
        filebrowser.setupFileListBrowser(self)

    def connectActions(self):
        # -- File Browser
        # year
        self.yearListView.clicked.connect(self._yearListViewClicked)
        model = self.yearListView.selectionModel()
        model.currentChanged.connect(self._yearListViewClicked)
        # month
        self.monthListView.clicked.connect(self._monthListViewClicked)
        model = self.monthListView.selectionModel()
        model.currentChanged.connect(self._monthListViewClicked)
        # day
        self.dayListView.clicked.connect(self._dayListViewClicked)
        model = self.dayListView.selectionModel()
        model.currentChanged.connect(self._dayListViewClicked)

        # -- GUI
        self.testButton.clicked.connect(self.printText)

    # == CALLBACKS

    # -- FILE BROWSER (defined in gui.filebrowser)

    def _yearListViewClicked(self, index):
        filebrowser.yearListViewClicked(self, index)

    def _monthListViewClicked(self, index):
        filebrowser.monthListViewClicked(self, index)

    def _dayListViewClicked(self, index):
        filebrowser.dayListViewClicked(self, index)

    def printText(self, event, msg="lol"):
        print(self.dummy.name)

    # == MAIN

    def main(self):
        self.show()


# %% RUN
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.main()
    app.exec_()
