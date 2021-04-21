#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Author   : alex
Created  : 2020-09-11 15:18:05
Modified : 2021-04-21 19:20:55

Comments :
"""
# %% IMPORTS

# -- global
import sys
from PyQt5 import QtWidgets

# -- local
import HAL.gui.filebrowser as filebrowser
import HAL.gui.dataviz as dataviz
import HAL.gui.metadata as metadata
from HAL.gui.MainUI import Ui_mainWindow
from HAL.classes.dummy import Dummy
from HAL.classes.settings import Settings
from HAL.classes.data import implemented_data_dic
from HAL.classes.metadata import implemented_metadata

# %% DEFINE GUI CLASS


class MainWindow(QtWidgets.QMainWindow, Ui_mainWindow):

    # == INITIALIZATIONS

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # -- FIRST
        # load settings
        self.settings = Settings()
        # implemented data classes
        self.data_classes = implemented_data_dic
        # implemented metadata classes
        self.metadata_classes = implemented_metadata

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
        # -- Data Visualization
        dataviz.setupDataViz(self)
        # -- Meta data
        metadata.setupMetaData(self)

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

        # -- Data visualization
        self.dataTypeComboBox.currentIndexChanged.connect(
            self._dataTypeComboBoxSelectionChanged
        )

        self.colorMapComboBox.currentIndexChanged.connect(
            self._colorMapComboBoxSelectionChanged
        )

        self.scaleMinEdit.editingFinished.connect(self._scaleMinEditChanged)

        self.scaleMaxEdit.editingFinished.connect(self._scaleMaxEditChanged)

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
        # display
        dataviz.plotSelectedData(self)
        # metadata
        metadata.displayMetaData(self)

    def _seqListSelectionChanged(self):
        filebrowser.refreshCurrentFolder(self)

    def _dateEditClicked(self):
        filebrowser.dateEditClicked(self)

    def _refreshRunListButtonClicked(self):
        filebrowser.refreshCurrentFolder(self)

    # -- Data visualization
    def _dataTypeComboBoxSelectionChanged(self):
        filebrowser.refreshCurrentFolder(self)

    def _colorMapComboBoxSelectionChanged(self):
        dataviz.plotSelectedData(self)

    def _scaleMaxEditChanged(self):
        new_max = self.scaleMaxEdit.text()
        if not new_max.isnumeric():
            self.scaleMaxEdit.setText("65535")
        dataviz.plotSelectedData(self)

    def _scaleMinEditChanged(self):
        new_min = self.scaleMinEdit.text()
        if not new_min.isnumeric():
            self.scaleMinEdit.setText("0")
        dataviz.plotSelectedData(self)

    # == MAIN

    def main(self):
        self.show()


# %% RUN
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.main()
    app.exec_()
