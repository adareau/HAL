#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Author   : alex
Created  : 2020-09-11 15:18:05
Modified : 2021-04-21 14:23:02

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
        self.current_folder = None

    def setupElements(self):
        # -- File Browser
        filebrowser.setupFileListBrowser(self)

    def connectActions(self):
        # -- File Browser
        # year
        self.yearList.itemSelectionChanged.connect(
            self._yearListSelectionChanged
        )
        # month
        self.monthList.itemSelectionChanged.connect(
            self._monthListSelectionChanged
        )
        # day
        self.dayList.itemSelectionChanged.connect(
            self._dayListSelectionChanged
        )
        self.seqList.itemSelectionChanged.connect(
            self._seqListSelectionChanged
        )
        # buttons
        self.refreshRunListButton.clicked.connect(
            self._refreshRunListButtonClicked
        )
        # calendar
        self.dateEdit.dateChanged.connect(self._dateEditClicked)

        # -- GUI
        self.testButton.clicked.connect(self.printText)

    # == CALLBACKS

    # -- FILE BROWSER (defined in gui.filebrowser)

    def _yearListSelectionChanged(self):
        filebrowser.yearListSelectionChanged(self)

    def _monthListSelectionChanged(self):
        filebrowser.monthListSelectionChanged(self)

    def _dayListSelectionChanged(self):
        filebrowser.dayListSelectionChanged(self)

    def _seqListSelectionChanged(self):
        filebrowser.refreshCurrentFolder(self)

    def _dateEditClicked(self):
        filebrowser.dateEditClicked(self)

    def _refreshRunListButtonClicked(self):
        filebrowser.refreshCurrentFolder(self)

    # -- GUI
    def printText(self, event, msg="lol"):
        print(self.dummy.name)
        print(self.current_folder)

    # == MAIN

    def main(self):
        self.show()


# %% RUN
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.main()
    app.exec_()
