#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Author   : alex
Created  : 2020-09-11 15:18:05
Modified : 2021-05-21 15:29:26


Comments :
"""
# %% IMPORTS

# -- global
import sys
import logging
import time

from PyQt5 import QtWidgets
from PyQt5.QtGui import QKeySequence, QFont
from PyQt5.QtWidgets import QShortcut, QMessageBox
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
import HAL.gui.advancedplot as advancedplot

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

    # -- ADVANCED DATA ANALYSIS / PLOT
    ("variableDeclarationTable", "itemChanged", "_variableDeclarationChanged"),
    ("exportToMatplotlibButton", "clicked", "_exportToMatplotlibButtonClicked"),
    ("updateSubplotLayoutButton", "clicked", "_updateSubplotLayoutButtonClicked"),
    ("resetSubplotLayoutButton", "clicked", "_resetSubplotLayoutButtonClicked"),
    ("subplotContentTable", "itemChanged", "_subplotContentTableChanged"),
    ("advancedPlotSaveButton", "clicked", "_advancedPlotSaveButtonClicked"),
    ("advancedPlotSaveAsButton", "clicked", "_advancedPlotSaveAsButtonClicked"),
    ("advancedPlotDeleteButton", "clicked", "_advancedPlotDeleteButtonClicked"),
    ("advancedPlotSelectionBox", "currentIndexChanged", "_advancedPlotSelectionBoxSelectionChanged"),
    ("exportDataButton", "clicked", "_exportDataButtonClicked"),
    ("advancedStatButton", "clicked", "_advancedStatButtonClicked"),
    ("advancedPlotResetButton", "clicked", "_advancedPlotResetButtonClicked"),

    # -- FITTING --
    # ROI
    ("addRoiButton", "clicked", "_addRoiButtonClicked"),
    ("renameRoiButton", "clicked", "_renameRoiButtonClicked"),
    ("deleteRoiButton", "clicked", "_deleteRoiButtonClicked"),
    ("resetRoiButton", "clicked", "_resetRoiButtonClicked"),
    ("addBackgroundButton", "clicked", "_addBackgroundButtonClicked"),
    # background
    ("backgroundCheckBox", "stateChanged", "_backgroundCheckBoxChanged"),

    # fit buttons
    ("fitButton", "clicked", "_fitButtonClicked"),
    ("fitBrowserButton", "clicked", "_fitButtonClicked"),
    ("deleteFitButton", "clicked", "_deleteFitButtonClicked"),

    # -- MENU BAR --
    ("menuAboutGotoGithubAction", "triggered", "_gotoGithub"),
    ("menuAboutOnlineHelpAction", "triggered", "_getOnlineHelp"),
    ("menuPreferencesEditSettingsAction", "triggered", "_editSettings"),

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

        # -- Hidden
        self._version = "0.0"
        self._name = "HAL"
        self._url = "https://github.com/adareau/HAL"
        self._settings_folder = Path().home() / ".HAL"
        self._kl = []
        self._t0 = 0

        # -- FIRST
        # create HAL settings folder
        self._settings_folder.mkdir(exist_ok=True)
        # load settings
        global_config_path = self._settings_folder / "global.conf"
        self.settings = Settings(path=global_config_path)
        # implemented data classes
        self.data_classes = implemented_data_dic
        # implemented metadata classes
        self.metadata_classes = implemented_metadata
        # implemented fit classes
        self.fit_classes = implemented_fit_dic
        # implemented display classes
        self.display_classes = implemented_display_dic

        # -- Set font size and Family
        font_family = self.settings.config["gui"]["font family"]
        font_size = self.settings.config["gui"]["font size"]
        font = QFont("Sans Serif", int(font_size))
        self.setFont(font)
        if parent is not None:
            parent.setFont(font)

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
        # live display subplots
        self.live_display_subplots = []

        # -- Other initializations
        self.dummy = Dummy()
        self.current_folder = None
        self.current_fig = None

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
        # -- Advanced Plot
        advancedplot.setupAdvancedPlot(self)
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

    # -- ADVANCED DATA ANALYSIS / PLOT

    def _variableDeclarationChanged(self, item):
        advancedplot.variableDeclarationChanged(self, item)

    def _exportToMatplotlibButtonClicked(self):
        advancedplot.exportToMatplotlib(self)

    def _updateSubplotLayoutButtonClicked(self):
        advancedplot.updateSubplotLayout(self)

    def _resetSubplotLayoutButtonClicked(self):
        advancedplot.resetSubplotLayout(self)

    def _subplotContentTableChanged(self, item):
        advancedplot.subplotContentChanged(self, item)

    def _advancedPlotSaveButtonClicked(self):
        advancedplot.advancedPlotSaveButtonClicked(self)

    def _advancedPlotSaveAsButtonClicked(self):
        advancedplot.advancedPlotSaveAsButtonClicked(self)

    def _advancedPlotDeleteButtonClicked(self):
        advancedplot.advancedPlotDeleteButtonClicked(self)

    def _advancedPlotSelectionBoxSelectionChanged(self):
        advancedplot.advancedPlotSelectionBoxSelectionChanged(self)

    def _exportDataButtonClicked(self):
        advancedplot.exportDataButtonClicked(self)

    def _advancedStatButtonClicked(self):
        advancedplot.advancedStatButtonClicked(self)

    def _advancedPlotResetButtonClicked(self):
        advancedplot.advancedPlotResetButtonClicked(self)

    # -- FITTING

    def _addRoiButtonClicked(self):
        fitting.addROI(self)

    def _renameRoiButtonClicked(self):
        fitting.renameROI(self)

    def _deleteRoiButtonClicked(self):
        fitting.removeROI(self)

    def _resetRoiButtonClicked(self):
        fitting.clearROIs(self)

    def _addBackgroundButtonClicked(self):
        fitting.addBackground(self)

    def _fitButtonClicked(self):
        # fit
        fitting.fit_data(self)
        # refresh
        filebrowser.refreshCurrentFolder(self)
        dataexplorer.refreshDataSetList(self)

    def _deleteFitButtonClicked(self):
        # fit
        fitting.deleteSavedFits(self)
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

    def _editSettings(self):
        if self.settings.openGuiEditor(parent=self):
            msg = "New user settings loaded. You might have to restart HAL now."
            QMessageBox.warning(self, "I am afraid Dave", msg)


    # -- DEBUG

    def _DEBUG(self):
        # self.autoScaleCheckBox.setChecked(True)
        # testing.open_image_and_fit(self)
        # testing.open_image(self)
        #testing.declare_variables(self)
        #testing.select_livemetadata_display(self)
        self._editSettings()

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
