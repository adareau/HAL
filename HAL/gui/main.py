#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Author   : alex
Created  : 2020-09-11 15:18:05
Modified : 2021-05-12 15:37:44

Comments :
"""
# %% IMPORTS

# -- global
import sys
import logging
import time

from PyQt5 import QtWidgets
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from pathlib import Path
from collections import OrderedDict

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


# %% CALLBACK DEFINITIONS
# for the sake of readability, we define all the
# callbacks in a list of tuples, with the following form :
#    ("widget", "signal", "callback")
# where "widget" is the name of the widget object, "signal"
# is a string containing the signal name, and "callback" the name
# of the callback function. All the callbacks are then automatically
# set in a loop.
#
# Example :
# --------
# adding ("todayButton", "clicked", "_todayButtonClicked") to
# the callback list will result in a callback definition leading to
# the same result as the following :
#
# self.todayButton.clicked.connect(self._todayButtonClicked)

# We disable black formatting : some lines will to too long, but
# this is better for readability IMHO
# fmt: off
CALLBACK_LIST = [

    # -- FILE BROWSER --
    # year / month / day lists
    ("yearList", "itemSelectionChanged", "_yearListSelectionChanged"),
    ("monthList", "itemSelectionChanged", "_monthListSelectionChanged"),
    ("dayList", "itemSelectionChanged", "_dayListSelectionChanged"),
    # seq / run / sets lists
    ("seqList", "itemSelectionChanged", "_seqListSelectionChanged"),
    ("runList", "itemSelectionChanged", "_runListSelectionChanged"),
    ("setList", "itemSelectionChanged", "_setListSelectionChanged"),
    # buttons
    ("refreshRunListButton", "clicked", "_refreshRunListButtonClicked"),
    ("todayButton", "clicked", "_todayButtonClicked"),
    ("dateEdit", "dateChanged", "_dateEditClicked"),

    # -- DATA DISPLAY --
    # select data type
    ("dataTypeComboBox", "currentIndexChanged", "_dataTypeComboBoxSelectionChanged"),
    # select colormap
    ("colorMapComboBox", "currentIndexChanged", "_colorMapComboBoxSelectionChanged"),
    # colormap scale
    ("scaleMinEdit", "editingFinished", "_scaleMinEditChanged"),
    ("scaleMaxEdit", "editingFinished", "_scaleMaxEditChanged"),
    ("autoScaleCheckBox", "stateChanged", "_autoScaleCheckBoxChanged"),
    # display type selector
    ("displaySelectionGroup", "triggered", "_displaySelectionChanged"),

    # -- DATA EXPLORER --
    # meta data management
    ("metaDataList", "itemSelectionChanged", "_metaDataListSelectionChanged"),
    ("metaDataList", "itemSelectionChanged", "_metaDataListSelectionChanged"),
    # sets management
    ("newSetButton", "clicked", "_newSetButtonClicked"),
    ("deleteSetButton", "clicked", "_deleteSetButtonClicked"),
    ("favSetButton", "clicked", "_favSetButtonClicked"),
    ("setList", "doubleClicked", "_setListDoubleClicked"),
    # quickplot
    ("quickPlotButton", "clicked", "_quickPlotButtonClicked"),
    ("quickPlotYToolButtonActionGroup", "triggered", "_quickPlotSelectionChanged"),
    ("quickPlotXToolButtonActionGroup", "triggered", "_quickPlotSelectionChanged"),

    # -- FITTING --
    # ROI
    ("addRoiButton", "clicked", "_addRoiButtonClicked"),
    # background
    ("backgroundCheckBox", "stateChanged", "_backgroundCheckBoxChanged"),

    # fit buttons
    ("fitButton", "clicked", "_fitButtonClicked"),
    ("fitBrowserButton", "clicked", "_fitButtonClicked"),

    # -- MENU BAR --
    ("menuAboutGotoGithubAction", "triggered", "_gotoGithub"),
    ("menuAboutOnlineHelpAction", "triggered", "_getOnlineHelp"),

    # -- DEBUG --
    ("debugButton", "clicked", "_DEBUG"),
]
# fmt: on


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

        # -- Metadata cache
        # cache
        self.metadata_cache = {}
        # init "lists" of available meta data
        # those are in fact "sets", so that the fields are only
        # counted once
        meta_names = [m().name for m in implemented_metadata]
        ordered_dic_init = [(m, set()) for m in meta_names]
        self.available_metadata = OrderedDict(ordered_dic_init)
        self.available_numeric_metadata = OrderedDict(ordered_dic_init)

        # -- Other initializations
        self.dummy = Dummy()
        self.current_folder = None
        self.current_fig = None

        # -- Hidden
        self._version = "0.0"
        self._name = "HAL"
        self._url = "https://github.com/adareau/HAL"
        self._settings_folder = Path().home() / ".HAL"
        self._kl = []
        self._t0 = 0

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
        # automatic definition of callbacks
        # from the CALLBACK_LIST, defined at the top of this file !
        global CALLBACK_LIST
        for callback in CALLBACK_LIST:
            widget_name, signal_name, callback_name = callback
            widget = getattr(self, widget_name)
            signal = getattr(widget, signal_name)
            callback = getattr(self, callback_name)
            signal.connect(callback)

        return

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
        dataexplorer.updateMetadataCache(self)

    def _seqListSelectionChanged(self):
        filebrowser.refreshCurrentFolder(self)
        dataexplorer.refreshDataSetList(self)
        dataexplorer.updateMetadataCache(self)

    def _setListSelectionChanged(self):
        dataexplorer.updateMetadataCache(self)

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
        dataexplorer.updateMetadataCache(self, reset_cache=True)
        quickplot.refreshMetaDataList(self)

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

    def _quickPlotSelectionChanged(self):
        quickplot.quickPlotSelectionChanged(self)

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

    def _tic(self, msg=None, name=""):
        if msg is not None:
            logger = logging.getLogger(name)
            logger.debug(msg)
        self._t0 = time.time()

    def _toc(self, name=""):
        tf = time.time()
        logger = logging.getLogger(name)
        logger.debug("DONE in %.2f seconds" % (tf - self._t0))

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