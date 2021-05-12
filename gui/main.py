#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Author   : alex
Created  : 2020-09-11 15:18:05
Modified : 2021-05-12 09:40:54

Comments :
"""
# %% IMPORTS

# -- global
import sys
import logging

from PyQt5 import QtWidgets
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from pathlib import Path

# -- local
import HAL.gui.filebrowser as filebrowser
import HAL.gui.display as display
import HAL.gui.dataexplorer as dataexplorer
import HAL.gui.quickplot as quickplot
import HAL.gui.fitting as fitting
import HAL.gui.testing as testing
import HAL.gui.misc as misc
import HAL.gui.menubar as menubar

from HAL.gui.MainUI import Ui_mainWindow
from HAL.classes.dummy import Dummy
from HAL.classes.settings import Settings
from HAL.classes.data import implemented_data_dic
from HAL.classes.metadata import implemented_metadata
from HAL.classes.fit import implemented_fit_dic
from HAL.classes.display import implemented_display_dic


# %% DEFINE GUI CLASS


class MainWindow(QtWidgets.QMainWindow, Ui_mainWindow):

    # == INITIALIZATIONS

    def __init__(self, parent=None, debug=False):
        super(MainWindow, self).__init__(parent)

        # -- SETUP LOGGER
        # setup log level
        self.__DEBUG__ = debug  # debug mode
        if self.__DEBUG__:
            log_level = logging.DEBUG
        else:
            log_level = logging.WARNING
        # setup format
        fmt = "[%(asctime)s] - %(name)s - %(levelname)s - %(message)s"
        # config
        logging.basicConfig(format=fmt, datefmt="%H:%M:%S", level=log_level)
        # define logger
        self.logger = logging.getLogger(__name__)
        # print first log
        self.logger.debug("HAL started")

        # -- FIRST
        # load settings
        self.settings = Settings()
        # implemented data classes
        self.data_classes = implemented_data_dic
        # implemented metadata classes
        self.metadata_classes = implemented_metadata
        # implemented fit classes
        self.fit_classes = implemented_fit_dic
        # implemented display classes
        self.display_classes = implemented_display_dic

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
        self.metadata = {}
        self.current_fig = None

        # -- Hidden
        self._version = "0.0"
        self._name = "HAL"
        self._url = "https://github.com/adareau/HAL"
        self._settings_folder = Path().home() / ".HAL"
        self._kl = []

        # -- Keyboard shortcuts
        self.ctrlF = QShortcut(QKeySequence("Ctrl+F"), self)
        self.ctrlF.activated.connect(self._ctrlF)
        self.ctrlD = QShortcut(QKeySequence("Ctrl+D"), self)
        self.ctrlD.activated.connect(self._ctrlD)

    def setupElements(self):
        # -- File Browser
        filebrowser.setupFileListBrowser(self)
        # -- Data Visualization
        display.setupDisplay(self)
        # -- Meta data
        dataexplorer.setupDataExplorer(self)
        # -- Quick Plot
        quickplot.setupQuickPlot(self)
        # -- Fitting
        fitting.setupFitting(self)
        # -- Menu Bar
        menubar.setupMenubar(self)

    def connectActions(self):

        # -- File Browser --
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
        self.todayButton.clicked.connect(self._todayButtonClicked)
        # calendar
        self.dateEdit.dateChanged.connect(self._dateEditClicked)

        # -- Data visualization --

        # select data type
        self.dataTypeComboBox.currentIndexChanged.connect(
            self._dataTypeComboBoxSelectionChanged
        )
        # select colormap
        self.colorMapComboBox.currentIndexChanged.connect(
            self._colorMapComboBoxSelectionChanged
        )
        # colormap scale min
        self.scaleMinEdit.editingFinished.connect(self._scaleMinEditChanged)
        # colormap scale max
        self.scaleMaxEdit.editingFinished.connect(self._scaleMaxEditChanged)
        # autoscale
        self.autoScaleCheckBox.stateChanged.connect(
            self._autoScaleCheckBoxChanged
        )
        # display type selector
        self.displaySelectionGroup.triggered.connect(
            self._displaySelectionChanged
        )

        # -- Data explorer --

        # - meta data management
        self.metaDataList.itemSelectionChanged.connect(
            self._metaDataListSelectionChanged
        )
        # - sets management

        # new set
        self.newSetButton.clicked.connect(self._newSetButtonClicked)
        # delete set
        self.deleteSetButton.clicked.connect(self._deleteSetButtonClicked)
        # add to favorite
        self.favSetButton.clicked.connect(self._favSetButtonClicked)
        # rename
        self.setList.doubleClicked.connect(self._setListDoubleClicked)

        # - quickplot
        self.quickPlotButton.clicked.connect(self._quickPlotButtonClicked)

        # -- Fitting --
        # add ROI
        self.addRoiButton.clicked.connect(self._addRoiButtonClicked)
        # fit button(s)
        self.fitButton.clicked.connect(self._fitButtonClicked)
        self.fitBrowserButton.clicked.connect(self._fitButtonClicked)
        # background check box
        self.backgroundCheckBox.stateChanged.connect(
            self._backgroundCheckBoxChanged
        )

        # -- Menu Bar --
        self.menuAbout.gotoGithubAction.triggered.connect(self._gotoGithub)
        self.menuAbout.onlineHelpAction.triggered.connect(self._getOnlineHelp)

        # -- DEBUG --
        self.debugButton.clicked.connect(self._DEBUG)

    # == CALLBACKS

    # -- FILE BROWSER (defined in gui.filebrowser)

    def _yearListSelectionChanged(self):
        filebrowser.yearListSelectionChanged(self)

    def _monthListSelectionChanged(self):
        filebrowser.monthListSelectionChanged(self)

    def _dayListSelectionChanged(self):
        filebrowser.dayListSelectionChanged(self)
        dataexplorer.refreshDataSetList(self)

    def _runListSelectionChanged(self):
        # handle special selection rules
        # (for instance, if a sequence is selected)
        filebrowser.runListSelectionChanged(self)
        # display
        display.plotSelectedData(self)
        # metadata
        dataexplorer.displayMetaData(self)

    def _seqListSelectionChanged(self):
        filebrowser.refreshCurrentFolder(self)
        dataexplorer.refreshDataSetList(self)

    def _dateEditClicked(self):
        filebrowser.dateEditClicked(self)
        dataexplorer.refreshDataSetList(self)

    def _refreshRunListButtonClicked(self):
        filebrowser.refreshCurrentFolder(self)
        dataexplorer.refreshDataSetList(self)

    def _todayButtonClicked(self):
        filebrowser.todayButtonClicked(self)
        dataexplorer.refreshDataSetList(self)

    # -- DATA VISUALIZATION

    def _dataTypeComboBoxSelectionChanged(self):
        filebrowser.refreshCurrentFolder(self)

    def _colorMapComboBoxSelectionChanged(self):
        display.updateColormap(self)

    def _scaleMaxEditChanged(self):
        new_max = self.scaleMaxEdit.text()
        if not new_max.isnumeric():
            self.scaleMaxEdit.setText("65535")
        display.plotSelectedData(self, update_fit=False)

    def _scaleMinEditChanged(self):
        new_min = self.scaleMinEdit.text()
        if not new_min.isnumeric():
            self.scaleMinEdit.setText("0")
        display.plotSelectedData(self, update_fit=False)

    def _displaySelectionChanged(self, action):
        display.displaySelectionChanged(self, action)

    def _autoScaleCheckBoxChanged(self):
        display.plotSelectedData(self, update_fit=False)

    # -- DATA EXPLORER

    def _metaDataListSelectionChanged(self):
        dataexplorer.displayMetaData(self)
        dataexplorer.refreshMetaDataList(self)

    def _newSetButtonClicked(self):
        dataexplorer.addNewSet(self)

    def _deleteSetButtonClicked(self):
        dataexplorer.deleteDataSet(self)

    def _favSetButtonClicked(self):
        dataexplorer.favDataSet(self)

    def _setListDoubleClicked(self):
        dataexplorer.renameDataSet(self)

    def _quickPlotButtonClicked(self):
        quickplot.plotData(self)

    # -- FITTING

    def _addRoiButtonClicked(self):
        fitting.addROI(self)

    def _fitButtonClicked(self):
        # fit
        fitting.fit_data(self)
        # refresh
        filebrowser.refreshCurrentFolder(self)
        dataexplorer.refreshDataSetList(self)

    def _backgroundCheckBoxChanged(self):
        if self.backgroundCheckBox.isChecked():
            fitting.addBackground(self)
        else:
            fitting.removeBackground(self)
        display.plotSelectedData(self, update_fit=False)

    # -- MENUBAR

    def _gotoGithub(self):
        menubar.gotoGithub(self)

    def _getOnlineHelp(self):
        menubar.getOnlineHelp(self)

    # -- DEBUG

    def _DEBUG(self):
        self.autoScaleCheckBox.setChecked(True)
        # testing.open_image_and_fit(self)
        testing.open_image(self)

    # == KEYBOARD SHORTCUTS

    def _ctrlF(self):
        """called when 'Ctrl+F' is pressed"""
        self._fitButtonClicked()

    def _ctrlD(self):
        """called when 'Ctrl+D' is pressed"""
        self._DEBUG()

    def keyPressEvent(self, event):
        """key pressed"""
        self._kl.append(event.key())
        misc.analyse_keylog(self)

    # == MAIN

    def main(self):
        self.show()


# %% RUN
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(debug=True)
    window.main()
    app.exec_()
