#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Author   : alex
Created  : 2020-09-11 15:18:05
Modified : 2021-04-21 15:14:31

Comments :
"""
# %% IMPORTS

# -- global
import sys
import numpy as np
from PyQt5 import QtWidgets, QtCore
from matplotlib import image
from matplotlib import cm

# -- PyQtGraph
import pyqtgraph as pg

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
        # sequences
        self.seqList.itemSelectionChanged.connect(
            self._seqListSelectionChanged
        )
        # runs
        self.runList.itemSelectionChanged.connect(
            self._runListSelectionChanged
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

    def _runListSelectionChanged(self):
        # handle special selection rules
        # (for instance, if a sequence is selected)
        filebrowser.runListSelectionChanged(self)
        # display file
        # FIXME : this is a placeholder
        selection = self.runList.selectedItems()
        if selection:
            item = selection[0]
            path = item.data(QtCore.Qt.UserRole)
            if path.is_dir():
                return
            if path.suffix != '.png':
                return
            im_data = image.imread(path)
            im_data = np.asarray(im_data)
            self.mainScreen.clear()
            img = pg.ImageItem()
            p = self.mainScreen.addPlot(0, 0)
            p.addItem(img)
            # Get the colormap
            colormap = cm.get_cmap("RdBu")
            colormap._init()
            lut = (colormap._lut * 255).view(np.ndarray)  # Convert matplotlib colormap from 0-1 to 0 -255 for Qt

            # Apply the colormap
            img.setLookupTable(lut)
            img.updateImage(image=im_data, levels=(np.min(im_data), np.max(im_data)))




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
