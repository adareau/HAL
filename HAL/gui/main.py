#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Author   : alex
Created  : 2020-09-11 15:18:05


Comments :
"""
# %% IMPORTS

# -- global
import logging
import time

from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QShortcut, QMessageBox, QAction, QMenu
from pathlib import Path
from collections import OrderedDict
from functools import wraps

# -- local
from .. import loader
from . import (
    filebrowser,
    display,
    dataexplorer,
    quickplot,
    fitting,
    testing,
    misc,
    menubar,
    advancedplot,
    commandpalette,
)

from .MainUI import Ui_mainWindow
from ..classes.settings import Settings
from ..gui import local_folder


# %% TOOLS
def _isnumber(x):
    try:
        float(x)
        return True
    except (TypeError, ValueError):
        return False


# %% DECORATOR FOR DEBUGGING
def logCallback(f):
    """a wrapper for callback, for debug purposes"""

    @wraps(f)
    def wrapper(*args, **kwds):
        # get log callback setting
        log_callbacks = args[0].settings.config["dev"]["log callbacks"]
        if eval(log_callbacks):
            name = f.__name__
            args[0].logger.debug(f"called {name}")
        return f(*args, **kwds)

    return wrapper


# cf. https://stackoverflow.com/a/6307868
def forAllCallbacks(decorator):
    """should decorate all methods with names starting with '_'"""

    def decorate(cls):
        for attr in cls.__dict__:
            if attr == "__init__":
                continue
            if attr.startswith("_") and callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return decorate


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
    # custom context menu (when right click on list)
    ("runList", "customContextMenuRequested", "_runListShowContextMenu"),
    ("setList", "customContextMenuRequested", "_setListShowContextMenu"),
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
    # remote screen
    ("remoteScreenAction", "triggered", "_toggleRemoteScreen"),

    # -- DATA EXPLORER --
    # meta data management
    ("metaDataList", "itemSelectionChanged", "_metaDataListSelectionChanged"),
    ("refreshMetadataCachebutton", "clicked", "_refreshMetadataCachebuttonClicked"),
    # sets management
    ("setList", "doubleClicked", "_renameDataSet"),
    ("dataSetCreateAction", "triggered", "_createNewDataSet"),
    ("dataSetDeleteAction", "triggered", "_deleteDataSet"),
    ("dataSetFavAction", "triggered", "_favDataSet"),
    ("dataSetAddAction", "triggered", "_addToDataSet"),
    ("dataSetRenameAction", "triggered", "_renameDataSet"),

    # quickplot
    ("quickPlotButton", "clicked", "_quickPlotButtonClicked"),
    ("quickPlotYToolButtonActionGroup", "triggered", "_quickPlotSelectionChanged"),
    ("quickPlotXToolButtonActionGroup", "triggered", "_quickPlotSelectionChanged"),
    ("quickPlotFitToolButtonActionGroup", "triggered", "_quickPlotFitSelectionChanged"),

    # -- ADVANCED DATA ANALYSIS / PLOT
    ("variableDeclarationTable", "itemChanged", "_variableDeclarationChanged"),
    ("exportToMatplotlibButton", "clicked", "_exportToMatplotlibButtonClicked"),
    ("updateSubplotLayoutButton", "clicked", "_updateSubplotLayoutButtonClicked"),
    ("resetSubplotLayoutButton", "clicked", "_resetSubplotLayoutButtonClicked"),
    ("subplotContentTable", "itemChanged", "_subplotContentTableChanged"),
    ("advancedPlotSaveButton", "clicked", "_advancedPlotSaveButtonClicked"),
    ("advancedPlotSaveAsButton", "clicked", "_advancedPlotSaveAsButtonClicked"),
    ("advancedPlotDeleteButton", "clicked", "_advancedPlotDeleteButtonClicked"),
    (
        "advancedPlotSelectionBox",
        "currentIndexChanged",
        "_advancedPlotSelectionBoxSelectionChanged"
    ),
    ("exportDataButton", "clicked", "_exportDataButtonClicked"),
    ("advancedStatButton", "clicked", "_advancedStatButtonClicked"),
    ("advancedPlotResetButton", "clicked", "_advancedPlotResetButtonClicked"),

    # -- FITTING --
    # ROI
    ("addRoiButton", "clicked", "_addRoiButtonClicked"),
    ("renameRoiButton", "clicked", "_renameRoiButtonClicked"),
    ("deleteRoiButton", "clicked", "_deleteRoiButtonClicked"),
    ("resetRoiButton", "clicked", "_resetRoiButtonClicked"),
    ("selectRoiComboBox", "currentIndexChanged", "_selectRoiComboBoxSelectionChanged"),
    # background
    ("backgroundCheckBox", "stateChanged", "_backgroundCheckBoxChanged"),

    # fit buttons
    ("fitButton", "clicked", "_fitButtonClicked"),
    ("deleteFitButton", "clicked", "_deleteFitButtonClicked"),

    # -- MENU BAR --
    ("menuAboutGotoGithubAction", "triggered", "_gotoGithub"),
    ("menuAboutOnlineHelpAction", "triggered", "_getOnlineHelp"),
    ("menuPreferencesEditSettingsAction", "triggered", "_editSettings"),
    ("menuScriptsActionGroup", "triggered", "_playScript"),
    ("openScriptFolderMenuAction", "triggered", "_openUserScriptFolder"),
    ("openModuleFolderAction", "triggered", "_openUserModuleFolder"),
    ("menuDataOpenDataFolderAction", "triggered", "_openDataFolder"),
    ("menuAboutdisplayShortcutsAction", "triggered", "_displayShortcuts"),

]
# fmt: on

# Format for keyboard shorcut = ("shortcut", "callback", "description for help")
# is description is empty ==> do not appear in help
KEYBOARD_SHORTCUTS = [
    ("F5", "_refreshRunListButtonClicked", "refresh run list"),
    ("Shift+F5", "_refreshMetadataCachebuttonClicked", "refresh metadata cache"),
    ("Ctrl+B", "_ctrlB", "add background"),
    ("Ctrl+D", "_DEBUG", ""),
    ("Ctrl+F", "_fitButtonClicked", "fit current selection"),
    ("Ctrl+P", "_ctrlP", "show command palette"),
    ("Ctrl+R", "_addRoiButtonClicked", "add ROI"),
    ("Ctrl+Shift+R", "_resetRoiButtonClicked", "reset all ROIs"),
    ("Ctrl+-", "_ctrlMinus", ""),
]

# %% DEFINE GUI CLASS


@forAllCallbacks(logCallback)
class MainWindow(QtWidgets.QMainWindow, Ui_mainWindow):

    # == INITIALIZATIONS

    def __init__(self, parent=None, debug=False):
        super(MainWindow, self).__init__(parent)

        # -- SETUP LOGGER
        # setup log level
        self.__DEBUG__ = debug  # debug mode
        self.logger = logging.getLogger(__name__)
        # print first log
        self.logger.debug("HAL started")

        # -- Hidden
        self._version = "0.1-beta"
        self._name = "HAL"
        self._url = "https://github.com/adareau/HAL"
        self._settings_folder = Path().home() / ".HAL"
        self._user_modules_folder = self._settings_folder / "user_modules"
        self._user_scripts_folder = self._settings_folder / "user_scripts"
        self._kl = []
        self._t0 = 0

        # -- FIRST
        # create HAL settings folder
        self._settings_folder.mkdir(exist_ok=True)
        self._user_modules_folder.mkdir(exist_ok=True)
        self._user_scripts_folder.mkdir(exist_ok=True)
        # load settings
        global_config_path = self._settings_folder / "global.conf"
        self.settings = Settings(path=global_config_path)

        # -- configure window
        # icon
        icon_file = Path(local_folder) / "icon.png"
        if icon_file.is_file():
            icon = QIcon(str(icon_file))
            self.setWindowIcon(icon)
        else:
            self.logger.warning(f"icon file '{icon_file}' not found")

        # -- USER MODULES AND SCRIPTS
        loader.modules.load(self)
        loader.scripts.load(self)

        # -- Set font size and Family
        font_family = self.settings.config["gui"]["font family"]
        font_size = self.settings.config["gui"]["font size"]
        font = QFont(font_family, int(font_size))
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
        # setup palette
        commandpalette.setupPaletteList(self)
        # setup keyboard shortcuts
        self.setupKeyboardShortcuts()

        # -- Metadata cache
        # cache
        self.metadata_cache = {}
        # init "lists" of available meta data
        # those are in fact "sets", so that the fields are only
        # counted once
        meta_names = [m().name for m in self.metadata_classes]
        ordered_dic_init = [(m, set()) for m in meta_names]
        self.available_metadata = OrderedDict(ordered_dic_init)
        self.available_numeric_metadata = OrderedDict(ordered_dic_init)
        # live display subplots
        self.live_display_subplots = []

        # -- Other initializations
        self.current_folder = None
        self.current_export_folder = None
        self.current_fig = None
        self.dark_theme = False
        self.default_palette = self.palette()
        self.remoteScreen = None
        self.remoteWindow = None

        # -- Keyboard shortcuts

    def setupElements(self):
        submodule_list = [
            filebrowser,
            display,
            dataexplorer,
            quickplot,
            advancedplot,
            fitting,
            menubar,
        ]
        for submodule in submodule_list:
            submodule.setupUi(self)

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

    def setupKeyboardShortcuts(self):
        # automatic definition of keyboard shortcuts
        # from the KEYBOARD_SHORTCUTS list, defined at the top of this file !
        global KEYBOARD_SHORTCUTS
        # save for later acces
        self.keyboard_shortcuts_lists = KEYBOARD_SHORTCUTS
        # assign shortcuts
        for shortcut in KEYBOARD_SHORTCUTS:
            sequence, callback_name, tooltip = shortcut
            qshortcut = QShortcut(sequence, self)
            callback = getattr(self, callback_name)
            qshortcut.activated.connect(callback)

    # == CALLBACKS

    # -- FILE BROWSER (defined in gui.filebrowser)
    def _yearListSelectionChanged(self, *args, **kwargs):
        filebrowser.yearListSelectionChanged(self)

    def _monthListSelectionChanged(self, *args, **kwargs):
        filebrowser.monthListSelectionChanged(self)

    def _dayListSelectionChanged(self, *args, **kwargs):
        filebrowser.dayListSelectionChanged(self)
        dataexplorer.refreshDataSetList(self)

    def _runListSelectionChanged(self, *args, **kwargs):
        # handle special selection rules
        # (for instance, if a sequence is selected)
        filebrowser.runListSelectionChanged(self)
        # display
        display.plotSelectedData(self)
        # metadata
        dataexplorer.displayMetaData(self)
        if eval(self.settings.config["metadata"]["autorefresh cache"]):
            dataexplorer.updateMetadataCache(self)

    def _runListShowContextMenu(self, position, *args, **kwargs):
        # -- return if no item
        if not self.runList.itemAt(position):
            return
        # -- create context menu
        contextMenu = QMenu()
        # -- Fit related actions
        # do fit
        fitAction = QAction("fit", self)
        fitAction.triggered.connect(self._fitButtonClicked)
        contextMenu.addAction(fitAction)
        # delete fit
        delFitAction = QAction("delete fit", self)
        delFitAction.triggered.connect(self._deleteFitButtonClicked)
        contextMenu.addAction(delFitAction)
        # -- Dataset related
        contextMenu.addSeparator()
        # crate dataset
        createSetAction = QAction("create set", self)
        createSetAction.triggered.connect(self._createNewDataSet)
        contextMenu.addAction(createSetAction)
        # add to selected set
        addToSetAction = QAction("add to selected set", self)
        addToSetAction.triggered.connect(self._addToDataSet)
        contextMenu.addAction(addToSetAction)
        # -- show
        contextMenu.exec_(self.runList.mapToGlobal(position))

    def _setListShowContextMenu(self, position, *args, **kwargs):
        # -- return if no item
        if not self.setList.itemAt(position):
            return
        # -- create context menu
        contextMenu = QMenu()
        # -- Dataset related
        # rename
        renameSetAction = QAction("rename", self)
        renameSetAction.triggered.connect(self._renameDataSet)
        contextMenu.addAction(renameSetAction)
        # delete
        deleteSetAction = QAction("delete", self)
        deleteSetAction.triggered.connect(self._deleteDataSet)
        contextMenu.addAction(deleteSetAction)
        # add to favorite
        favDataSetAction = QAction("add to favorite", self)
        favDataSetAction.triggered.connect(self._favDataSet)
        contextMenu.addAction(favDataSetAction)
        # add to selected set
        addToSetAction = QAction("add selected runs", self)
        addToSetAction.triggered.connect(self._addToDataSet)
        contextMenu.addAction(addToSetAction)
        # -- show
        contextMenu.exec_(self.setList.mapToGlobal(position))

    def _seqListSelectionChanged(self, *args, **kwargs):
        filebrowser.refreshCurrentFolder(self)
        dataexplorer.refreshDataSetList(self)
        if eval(self.settings.config["metadata"]["autorefresh cache"]):
            dataexplorer.updateMetadataCache(self)

    def _setListSelectionChanged(self, *args, **kwargs):
        if eval(self.settings.config["metadata"]["autorefresh cache"]):
            dataexplorer.updateMetadataCache(self)

    def _dateEditClicked(self, date):
        filebrowser.dateEditClicked(self)
        dataexplorer.refreshDataSetList(self)

    def _refreshRunListButtonClicked(self, *args, **kwargs):
        filebrowser.refreshCurrentFolder(self)
        dataexplorer.refreshDataSetList(self)

    def _todayButtonClicked(self, checked=False):
        filebrowser.todayButtonClicked(self)
        dataexplorer.refreshDataSetList(self)

    # -- DATA VISUALIZATION

    def _dataTypeComboBoxSelectionChanged(self, *args, **kwargs):
        # update scale
        data_class = self.dataTypeComboBox.currentData()
        sc_min, sc_max = data_class().default_display_scale
        self.scaleMinEdit.setText(str(sc_min))
        self.scaleMaxEdit.setText(str(sc_max))
        # refresh
        filebrowser.refreshCurrentFolder(self)
        display.plotSelectedData(self)

    def _colorMapComboBoxSelectionChanged(self, *args, **kwargs):
        display.updateColormap(self)

    def _scaleMaxEditChanged(self, *args, **kwargs):
        new_max = self.scaleMaxEdit.text()
        if not _isnumber(new_max):
            data_class = self.dataTypeComboBox.currentData()
            _, sc_max = data_class().default_display_scale
            self.scaleMaxEdit.setText(str(sc_max))
        display.plotSelectedData(self, update_fit=False)

    def _scaleMinEditChanged(self, *args, **kwargs):
        new_min = self.scaleMinEdit.text()
        if not _isnumber(new_min):
            data_class = self.dataTypeComboBox.currentData()
            sc_min, _ = data_class().default_display_scale
            self.scaleMinEdit.setText(str(sc_min))
        display.plotSelectedData(self, update_fit=False)

    def _displaySelectionChanged(self, action):
        display.displaySelectionChanged(self, action)

    def _autoScaleCheckBoxChanged(self, *args, **kwargs):
        display.plotSelectedData(self, update_fit=False)

    def _toggleRemoteScreen(self, checked, *args, **kwargs):
        if checked:
            display.createRemoteScreen(self)
        else:
            display.deleteRemoteScreen(self)

    # -- DATA EXPLORER

    def _metaDataListSelectionChanged(self, *args, **kwargs):
        dataexplorer.displayMetaData(self)
        dataexplorer.updateMetadataCache(self, reset_cache=True)
        quickplot.refreshMetaDataList(self)

    def _refreshMetadataCachebuttonClicked(self, *args, **kwargs):
        dataexplorer.updateMetadataCache(self, reset_cache=True)

    def _createNewDataSet(self, *args, **kwargs):
        dataexplorer.createNewDataSet(self)

    def _addToDataSet(self, *args, **kwargs):
        dataexplorer.addToDataSet(self)

    def _deleteDataSet(self, *args, **kwargs):
        dataexplorer.deleteDataSet(self)

    def _favDataSet(self, *args, **kwargs):
        dataexplorer.favDataSet(self)

    def _renameDataSet(self, *args, **kwargs):
        dataexplorer.renameDataSet(self)

    def _quickPlotButtonClicked(self, *args, **kwargs):
        quickplot.plotData(self)

    def _quickPlotSelectionChanged(self, *args, **kwargs):
        quickplot.quickPlotSelectionChanged(self)

    def _quickPlotFitSelectionChanged(self, *args, **kwargs):
        quickplot.quickPlotFitSelectionChanged(self)

    # -- ADVANCED DATA ANALYSIS / PLOT

    def _variableDeclarationChanged(self, item):
        advancedplot.variableDeclarationChanged(self, item)

    def _exportToMatplotlibButtonClicked(self, *args, **kwargs):
        advancedplot.exportToMatplotlib(self)

    def _updateSubplotLayoutButtonClicked(self, *args, **kwargs):
        advancedplot.updateSubplotLayout(self)

    def _resetSubplotLayoutButtonClicked(self, *args, **kwargs):
        advancedplot.resetSubplotLayout(self)

    def _subplotContentTableChanged(self, item):
        advancedplot.subplotContentChanged(self, item)

    def _advancedPlotSaveButtonClicked(self, *args, **kwargs):
        advancedplot.advancedPlotSaveButtonClicked(self)

    def _advancedPlotSaveAsButtonClicked(self, *args, **kwargs):
        advancedplot.advancedPlotSaveAsButtonClicked(self)

    def _advancedPlotDeleteButtonClicked(self, *args, **kwargs):
        advancedplot.advancedPlotDeleteButtonClicked(self)

    def _advancedPlotSelectionBoxSelectionChanged(self, *args, **kwargs):
        advancedplot.advancedPlotSelectionBoxSelectionChanged(self)

    def _exportDataButtonClicked(self, *args, **kwargs):
        advancedplot.exportDataButtonClicked(self)

    def _advancedStatButtonClicked(self, *args, **kwargs):
        advancedplot.advancedStatButtonClicked(self)

    def _advancedPlotResetButtonClicked(self, *args, **kwargs):
        advancedplot.advancedPlotResetButtonClicked(self)

    # -- FITTING

    def _addRoiButtonClicked(self, *args, **kwargs):
        fitting.addROI(self)

    def _renameRoiButtonClicked(self, *args, **kwargs):
        fitting.renameROI(self)
        # refresh
        filebrowser.refreshCurrentFolder(self)
        dataexplorer.refreshDataSetList(self)

    def _deleteRoiButtonClicked(self, *args, **kwargs):
        fitting.removeROI(self)
        # refresh
        filebrowser.refreshCurrentFolder(self)
        dataexplorer.refreshDataSetList(self)

    def _resetRoiButtonClicked(self, *args, **kwargs):
        fitting.clearROIs(self)
        # refresh
        filebrowser.refreshCurrentFolder(self)
        dataexplorer.refreshDataSetList(self)

    def _selectRoiComboBoxSelectionChanged(self, *args, **kwargs):
        display.updateFitForSelectedData(self)

    def _fitButtonClicked(self, *args, **kwargs):
        # fit
        fitting.batchFitData(self)
        # refresh
        filebrowser.refreshCurrentFolder(self)
        dataexplorer.refreshDataSetList(self)
        display.updateFitForSelectedData(self)
        dataexplorer.displayMetaData(self)

    def _deleteFitButtonClicked(self, *args, **kwargs):
        # fit
        fitting.deleteSavedFits(self)
        # refresh
        filebrowser.refreshCurrentFolder(self)
        dataexplorer.refreshDataSetList(self)

    def _backgroundCheckBoxChanged(self, *args, **kwargs):
        if self.backgroundCheckBox.isChecked():
            fitting.addBackground(self)
        else:
            fitting.removeBackground(self)
        display.plotSelectedData(self, update_fit=False)

    # -- MENUBAR

    def _gotoGithub(self, *args, **kwargs):
        menubar.gotoGithub(self)

    def _getOnlineHelp(self, *args, **kwargs):
        menubar.getOnlineHelp(self)

    def _editSettings(self, *args, **kwargs):
        if self.settings.openGuiEditor(parent=self):
            msg = "New user settings loaded. You might have to restart HAL now."
            QMessageBox.warning(self, "I am afraid Dave", msg)

    def _playScript(self, action, *args, **kwargs):
        """runs the selected script"""
        # get script info from action data
        cat, name, func = action.data()
        # play
        sname = cat + ":" + name if cat else name
        self.logger.debug(f"running script {sname}")
        func(self)

    def _openUserScriptFolder(self, *args, **kwargs):
        menubar.openUserScriptFolder(self)

    def _openUserModuleFolder(self, *args, **kwargs):
        menubar.openUserModuleFolder(self)

    def _openDataFolder(self, *args, **kwargs):
        menubar.openDataFolder(self)

    def _displayShortcuts(self, *args, **kwargs):
        menubar.displayShortcuts(self)

    # -- DEBUG

    def _DEBUG(self, *args, **kwargs):
        # self.autoScaleCheckBox.setChecked(True)
        testing.open_image(self)
        # testing.open_image_and_fit(self)
        # testing.declare_variables(self)
        # testing.select_livemetadata_display(self)
        # self._editSettings()

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

    def _ctrlB(self, *args, **kwargs):
        """called when 'Ctrl+B' is pressed"""
        self.backgroundCheckBox.toggle()

    def _ctrlP(self, *args, **kwargs):
        """called when 'Ctrl+P' is pressed"""
        commandpalette.showPalette(self)

    def _ctrlMinus(self, *args, **kwargs):
        """called when 'Ctrl+-' is pressed"""
        self.logger.debug("-" * 50)

    def keyPressEvent(self, event):
        """key pressed"""
        self._kl.append(event.key())
        misc.analyse_keylog(self)

    # == MAIN

    def main(self):
        self.show()
