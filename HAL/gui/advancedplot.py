# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-17 09:36:42
Modified : 2021-05-19 12:11:59

Comments : Implement the "Advanced data analysis"
"""

# %% IMPORTS

# -- global
import logging
import re
import pyqtgraph as pg
import numpy as np
import json
from matplotlib import cm
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QCompleter,
    QLineEdit,
    QTableWidgetItem,
    QInputDialog,
    QMessageBox,
)

# -- local
import HAL.gui.dataexplorer as dataexplorer
from HAL.classes.display import LiveMetaData

# -- logger
logger = logging.getLogger(__name__)


# %% GLOBAL VARIABLES
NAME_SEPARATION_CHARACTER = "."
NAME_REGEXP_FORMAT = "\w*"
PLOT_FORMULA_REGEXP_FORMAT = "[\w\+\-.\*/\(\)]*"  # to allow math formulaes
VARIABLE_REGEXP_FORMAT = "[\w_\-:.\s]*"
VARIABLE_SPLIT_FORMAT = "^([\w_\-:\s]*)\.([\w_\-:\s]*)$"
CONF_SAVE_SUFOLDER = "advanced_plot_saved_configurations"

# %% CUSTOM CLASSES

# -- delegate for table autocompletion and validation
# cf. https://stackoverflow.com/q/60750357


class TableItemCompleter(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        # auto completion
        completionlist, regexp_format = index.data(Qt.UserRole)
        autoCompleter = QCompleter(completionlist, parent)
        autoCompleter.setCaseSensitivity(Qt.CaseInsensitive)
        autoCompleter.setFilterMode(Qt.MatchContains)
        editor.setCompleter(autoCompleter)
        # validation
        rx = QRegExp(regexp_format)
        validator = QRegExpValidator(rx)
        editor.setValidator(validator)
        return editor


class NumberValidator(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        validator = QIntValidator(0, 256)
        editor.setValidator(validator)
        return editor


# %% TOOL


def _isnumber(x):
    try:
        float(x)
        return True
    except (TypeError, ValueError):
        return False


def gimmeColor(i=0):
    """returns a color from the defined color cycle"""
    # TODO : allow the user to define the color cycle ?
    # -- get the colormap from matplotlib
    cmap = cm.get_cmap("Set1")
    cmap._init()
    clist = cmap._lut[:-1]

    # -- get color
    color = clist[i % len(clist)]
    color_RGB = color[:-1] * 255
    out = tuple([int(c) for c in color_RGB])

    return tuple(color_RGB)


def gimmeSymbol(i=0):
    symb_list = [
        "o",
        "t",
        "s",
        "p",
        "h",
        "star",
        "t1",
        "t3",
        "t2",
        "+",
        "d",
        "x",
    ]
    return symb_list[i % len(symb_list)]


# %% SETUP FUNCTIONS


def setupAdvancedPlot(self):
    global NAME_REGEXP_FORMAT, VARIABLE_REGEXP_FORMAT, CONF_SAVE_SUFOLDER

    # -- Variable declaration table
    table = self.variableDeclarationTable
    # init columnt and row number
    table.setColumnCount(2)
    table.setRowCount(10)
    # labels
    table.setHorizontalHeaderLabels(["name", "variable"])
    # selection mode
    table.setSelectionBehavior(QAbstractItemView.SelectRows)
    table.setSelectionMode(QAbstractItemView.SingleSelection)
    # set row height
    header = table.verticalHeader()
    header.setDefaultSectionSize(10)
    header.setSectionResizeMode(QHeaderView.Fixed)
    # hide row numbers
    header.setVisible(False)
    # column width
    table.setColumnWidth(0, 50)
    table.setColumnWidth(1, 182)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
    # set completer
    table.setItemDelegate(TableItemCompleter())
    # init the completer with empty list
    n_row = table.rowCount()
    for rows in range(n_row):
        # row 0 : name
        comp_list = [""]
        regexp = NAME_REGEXP_FORMAT
        data = (comp_list, regexp)
        item = QTableWidgetItem("")
        item.setData(Qt.UserRole, data)
        table.setItem(rows, 0, item)

        # row 1 : variable
        comp_list = [""]
        regexp = VARIABLE_REGEXP_FORMAT
        data = (comp_list, regexp)
        item = QTableWidgetItem("")
        item.setData(Qt.UserRole, data)
        table.setItem(rows, 1, item)

    # -- subplot setup table
    table = self.subplotSetupTable
    # init columnt and row number
    table.setColumnCount(4)
    table.setRowCount(8)
    # labels
    table.setHorizontalHeaderLabels(["col", "row", "cspan", "rspan"])
    # selection mode
    # table.setSelectionBehavior(QAbstractItemView.SelectRows)
    table.setSelectionMode(QAbstractItemView.SingleSelection)
    # set row height
    header = table.verticalHeader()
    header.setDefaultSectionSize(10)
    header.setSectionResizeMode(QHeaderView.Fixed)
    # show row numbers
    header.setVisible(True)
    # column width
    table.setColumnWidth(0, 30)
    table.setColumnWidth(1, 30)
    table.setColumnWidth(2, 40)
    table.setColumnWidth(3, 40)
    header = table.horizontalHeader()
    header.setSectionResizeMode(QHeaderView.Fixed)
    # set completer
    table.setItemDelegate(NumberValidator())
    # init
    table.setItem(0, 0, QTableWidgetItem("0"))
    table.setItem(0, 1, QTableWidgetItem("0"))
    table.setItem(0, 2, QTableWidgetItem("1"))
    table.setItem(0, 3, QTableWidgetItem("1"))

    # -- subplot content table
    table = self.subplotContentTable
    # init columnt and row number
    table.setColumnCount(1)
    table.setRowCount(1)
    table.setHorizontalHeaderLabels(["plot content"])
    # selection mode
    table.setSelectionMode(QAbstractItemView.SingleSelection)
    # set row height
    header = table.verticalHeader()
    header.setDefaultSectionSize(10)
    header.setVisible(True)
    table.setColumnWidth(0, 250)
    table.setItem(0, 0, QTableWidgetItem("(x, y); "))

    # -- init saved configs
    saved_config_folder = self._settings_folder / CONF_SAVE_SUFOLDER
    self.advancedPlotSelectionBox.addItem("----", userData=None)
    for content in saved_config_folder.iterdir():
        if not content.is_file():
            continue
        if content.suffix == ".json":
            self.advancedPlotSelectionBox.addItem(
                content.stem, userData=content
            )


# %% LOW-LEVEL FUNCTIONS AND TOOLS


def refreshMetaDataList(self):
    """
    updates the variable declaration suggestions
    """
    global NAME_SEPARATION_CHARACTER, VARIABLE_REGEXP_FORMAT

    # -- get data
    metadata_list = self.available_numeric_metadata

    # -- generate the suggestion list
    suggestion_list = []
    naming_format = "%s" + NAME_SEPARATION_CHARACTER + "%s"
    for name, param_list in metadata_list.items():
        for par_name in sorted(param_list):
            new_suggestion = naming_format % (name, par_name)
            suggestion_list.append(new_suggestion)

    # -- apply to all rows
    table = self.variableDeclarationTable
    # block signals to avoid calling the variableDeclarationChanged() callback
    table.blockSignals(True)
    n_row = table.rowCount()
    data = (suggestion_list, VARIABLE_REGEXP_FORMAT)
    for row in range(n_row):
        current_item = table.item(row, 1)
        new_item = QTableWidgetItem(current_item.text())
        new_item.setData(Qt.UserRole, data)
        table.setItem(row, 1, new_item)
    # unblock signals
    table.blockSignals(False)


def mapVariables(self, metadata_dic):
    global VARIABLE_SPLIT_FORMAT
    """map the variables names to their values, using the declarations from
      the variableDeclarationTable"""
    # -- get table object and row number
    table = self.variableDeclarationTable
    n_row = table.rowCount()

    # -- loop on all rows
    mapped_variables = {}
    for row in range(n_row):
        # get variable names
        name = table.item(row, 0).text()
        varname = table.item(row, 1).text()
        if not varname or not name:
            continue
        # parse the requested variable name
        res = re.match(VARIABLE_SPLIT_FORMAT, varname)
        if not res:
            logger.warning("varname '%s' could not be parsed !" % varname)
            continue
        meta_name, meta_parname = res.groups()
        # check that medata is present
        if meta_name not in metadata_dic:
            logger.debug("metadata class name '%s' not found" % meta_name)
            continue
        if meta_parname not in metadata_dic[meta_name]:
            msg = "parameter name '%s' not found for metadata class '%s'"
            logger.debug(msg % (meta_parname, meta_name))
            continue
        # store
        var = np.asarray(metadata_dic[meta_name][meta_parname])
        mapped_variables[name] = var
        # store info
        info_key = "_" + meta_parname + "_info"
        if info_key in metadata_dic[meta_name]:
            name_info = "_%s_info" % name
            mapped_variables[name_info] = metadata_dic[meta_name][info_key]

    return mapped_variables


def parseSubplotContent(self):
    """
    Parses the content of the subplotContentTable. The content to plot
    has to be given in the following form :

    '(formula_1, formula_2); (formula_3, formula_4)'

    where the formulaes contain variables with names matching the regexp format
    'NAME_REGEXP_FORMAT', plus math symbols (*+/-) and numpy formulaes such as
    'np.cos()'. White spaces are ignored.
    """
    global PLOT_FORMULA_REGEXP_FORMAT

    # -- get table
    table = self.subplotContentTable
    n_row = table.rowCount()

    # -- get content
    requested_content = {}
    var_fmt = PLOT_FORMULA_REGEXP_FORMAT
    regexp_format = "^\((%s)\,(%s)\)$" % (var_fmt, var_fmt)
    for row in range(n_row):
        requested_content[row] = []
        item = table.item(row, 0)
        # if None : skip
        if item is None:
            continue
        # otherwise, analyze content
        content_str = item.text()
        tuple_list = content_str.split(";")
        for tup in tuple_list:
            tup = tup.replace(" ", "")  # remove white spaces
            res = re.match(regexp_format, tup)
            if res:
                x, y = res.groups()
                requested_content[row].append((x, y))

    return requested_content


def refreshMetadataLivePlot(self):
    """if the current display mode is set to LiveMetaData, refresh the plot"""

    # -- check whether the current display is an instance of LiveMetaData
    if not isinstance(self.display, LiveMetaData):
        return

    # -- get metadata list
    metadata = dataexplorer.getSelectionMetaDataFromCache(self)

    # -- clear all plots
    for subplot in self.live_display_subplots:
        for plot_item in subplot.plotted_data:
            subplot.removeItem(plot_item)
        subplot.plotted_data = []

    # -- get requested content
    requested_content = parseSubplotContent(self)

    # -- plot
    for subplot_number, content in requested_content.items():
        subplot = self.live_display_subplots[subplot_number]
        i_plot = 0
        info = {
            "x": {"name": "x", "unit": ""},
            "y": {"name": "y", "unit": ""},
        }
        for setname, metadata_dic in metadata.items():
            mapped_variables = mapVariables(self, metadata_dic)
            n_content = len(content)
            for i_content, c in enumerate(content):
                # get formulaes
                formula_x, formula_y = c
                # update name, just in case
                for ax, formula in zip(["x", "y"], [formula_x, formula_y]):
                    if info[ax]["name"] == ax:
                        info[ax]["name"] = formula
                # get values
                try:
                    x = eval(formula_x, {"np": np}, mapped_variables)
                    y = eval(formula_y, {"np": np}, mapped_variables)
                except Exception as e:
                    logger.exception(e)
                    continue
                # convert to array
                x = np.asarray(x)
                y = np.asarray(y)
                # remove NaNs
                i_good = np.isfinite(x) * np.isfinite(y)
                x = x[i_good]
                y = y[i_good]
                # if empty: continue
                if len(x)==0:
                    continue

                # if a bare variable is resquested, we get the corresponding
                # information (unit / name), if present
                for ax, form in zip(["x", "y"], [formula_x, formula_y]):
                    info_key = "_%s_info" % form
                    if info_key in mapped_variables:
                        info[ax]["name"] = mapped_variables[info_key]["name"]
                        info[ax]["unit"] = mapped_variables[info_key]["unit"]

                # sort
                isort = np.argsort(x)
                x = x[isort]
                y = y[isort]

                # setname
                if n_content > 1:
                    # then we append the name of the y content
                    # to the displayed name
                    name = "%s (%s)" % (setname, info["y"]["name"])
                else:
                    name = setname
                # plot
                symbol = gimmeSymbol(i_content)
                color = gimmeColor(i_plot)
                data_item = pg.PlotDataItem(
                    x,
                    y,
                    pen=color,
                    symbolBrush=color,
                    symbolPen=color,
                    symbol=symbol,
                    symbolSize=8,
                    name=name,
                )
                subplot.addItem(data_item)
                subplot.plotted_data.append(data_item)

                # -- end of content loop --

            # increment plot
            i_plot += 1

            # -- end of set loop --

        # -- get last item info to update axis labels
        for ax, loc in zip(["x", "y"], ["bottom", "left"]):
            name = info[ax]["name"]
            unit = info[ax]["unit"]
            subplot.setLabel(loc, name, units=unit)


# %% CALLBACKS


def variableDeclarationChanged(self, item):
    """called when the content of the variable declaration table is changed"""
    # -- refresh display
    refreshMetadataLivePlot(self)


def exportToMatplotlib(self):
    """ Placeholder. TODO : implement"""
    logger.debug("export to MPL !")


def updateSubplotLayout(self):
    """updates the subplot layout !"""
    # -- check whether the current display is an instance of LiveMetaData
    if not isinstance(self.display, LiveMetaData):
        return

    # -- reset current layout
    screen = self.mainScreen
    screen.clear()
    self.live_display_subplots = []

    # -- get layout information
    table = self.subplotSetupTable
    n_row = table.rowCount()
    for row in range(n_row):
        # skip if one item not defined
        if None in [table.item(row, i) for i in range(4)]:
            continue
        # get row content
        col_str = table.item(row, 0).text()
        row_str = table.item(row, 1).text()
        colspan_str = table.item(row, 2).text()
        rowspan_str = table.item(row, 3).text()
        # skip if one column is empty
        if "" in [col_str, row_str, colspan_str, rowspan_str]:
            continue
        # init subplot
        r = int(row_str)
        c = int(col_str)
        rs = int(rowspan_str)
        cs = int(colspan_str)
        new_subplot = screen.addPlot(row=r, col=c, rowspan=rs, colspan=cs)
        new_subplot.plotted_data = []  # will be used to store plot items !
        new_subplot.addLegend()
        self.live_display_subplots.append(new_subplot)

    # -- update subplotContentTable
    # save current content
    table = self.subplotContentTable
    n_row = table.rowCount()
    saved_content = {}
    for row in range(n_row):
        item = table.item(row, 0)
        if item is not None:
            saved_content[row] = item.text()
    # clear
    table.clearContents()
    # update
    n_row = len(self.live_display_subplots)
    table.setRowCount(n_row)
    for row in range(n_row):
        new_content = saved_content.get(row, "(x, y); ")
        table.setItem(row, 0, QTableWidgetItem(new_content))


def resetSubplotLayout(self):
    """resets the subplot layout !"""
    # clear
    table = self.subplotSetupTable
    table.clearContents()
    # re-init
    table.setItem(0, 0, QTableWidgetItem("0"))
    table.setItem(0, 1, QTableWidgetItem("0"))
    table.setItem(0, 2, QTableWidgetItem("1"))
    table.setItem(0, 3, QTableWidgetItem("1"))
    # update subplot accordingly
    updateSubplotLayout(self)


def subplotContentChanged(self, item):
    """called when the subplot content table is changed"""
    # -- refresh display
    refreshMetadataLivePlot(self)


# %% LOADING / SAVING CONFIGURATIONS


def _refreshAvailableConfigs(self):
    # -- save current selection and clear
    current_selection = self.advancedPlotSelectionBox.currentText()
    self.advancedPlotSelectionBox.blockSignals(True)
    self.advancedPlotSelectionBox.setCurrentIndex(0)
    self.advancedPlotSelectionBox.clear()
    # -- get list of saved configs
    saved_config_folder = self._settings_folder / CONF_SAVE_SUFOLDER
    self.advancedPlotSelectionBox.addItem("----", userData=None)
    for content in saved_config_folder.iterdir():
        if not content.is_file():
            continue
        if content.suffix == ".json":
            self.advancedPlotSelectionBox.addItem(
                content.stem, userData=content
            )
    # -- retrieve saved selection (if still exists)
    self.advancedPlotSelectionBox.blockSignals(False)
    self.advancedPlotSelectionBox.setCurrentText(current_selection)


def _saveCurrentConfig(self, out_name="config.json"):
    global CONF_SAVE_SUFOLDER
    # -- prepare config dict
    config = {}
    # - variable declaration
    # prepare list
    variable_declaration = []
    table = self.variableDeclarationTable
    n_row = table.rowCount()
    for row in range(n_row):
        # get variable names
        name = table.item(row, 0).text()
        varname = table.item(row, 1).text()
        if not varname or not name:
            continue
        variable_declaration.append((name, varname))
    # store
    config["variable declaration"] = variable_declaration

    # - plot config
    # prepare list
    plot_config = []
    table = self.subplotSetupTable
    n_row = table.rowCount()
    for row in range(n_row):
        # skip if one item not defined
        if None in [table.item(row, i) for i in range(4)]:
            continue
        # get row content
        col_str = table.item(row, 0).text()
        row_str = table.item(row, 1).text()
        colspan_str = table.item(row, 2).text()
        rowspan_str = table.item(row, 3).text()
        # skip if one column is empty
        if "" in [col_str, row_str, colspan_str, rowspan_str]:
            continue
        plot_config.append((col_str, row_str, colspan_str, rowspan_str))
    # store
    config["plot config"] = plot_config

    # - plot content
    # prepare list
    plot_content = []
    table = self.subplotContentTable
    n_row = table.rowCount()
    for row in range(n_row):
        item = table.item(row, 0)
        # if None : skip
        if item is None:
            plot_content.append("")
        else:
            plot_content.append(item.text())
    # store
    config["plot content"] = plot_content

    # -- write
    out_folder = self._settings_folder / CONF_SAVE_SUFOLDER
    out_folder.mkdir(exist_ok=True)
    out_file = out_folder / out_name
    out_file.write_text(json.dumps(config))


def advancedPlotSaveButtonClicked(self):
    """saves the current config, overwrite currently selected"""
    # -- get current selection
    data = self.advancedPlotSelectionBox.currentData()
    # if data is None : ask for a name
    if data is None or not data.is_file():
        advancedPlotSaveAsButtonClicked(self)
        return
    # otherwise, overwrite current selection
    out_name = data.name
    msg = "overwrite existing config '%s' ?" % data.stem
    answer = QMessageBox.question(
        self, "save plot config", msg, QMessageBox.Yes | QMessageBox.No
    )
    if answer == QMessageBox.Yes:
        _saveCurrentConfig(self, out_name=out_name)
        _refreshAvailableConfigs(self)


def advancedPlotSaveAsButtonClicked(self):
    """saves the current config, asks for the name"""
    name, ok = QInputDialog.getText(
        self, "save plot config as", "Enter config name:", text="config"
    )
    if ok:
        _saveCurrentConfig(self, out_name=name + ".json")
        _refreshAvailableConfigs(self)


def advancedPlotDeleteButtonClicked(self):
    """delete the current config"""
    # -- get current selection
    data = self.advancedPlotSelectionBox.currentData()
    #  check that the config still exists
    if data is None or not data.is_file():
        return
    # otherwise, overwrite current selection
    out_name = data.name
    msg = "delete existing config '%s' ?" % data.stem
    answer = QMessageBox.question(
        self, "delete config", msg, QMessageBox.Yes | QMessageBox.No
    )
    if answer == QMessageBox.Yes:
        data.unlink()
        _refreshAvailableConfigs(self)


def advancedPlotSelectionBoxSelectionChanged(self):
    """loads a saved configuration"""
    # -- get current item data
    data = self.advancedPlotSelectionBox.currentData()
    if data is None:
        return

    # -- load config
    # is it a file ?
    if not data.is_file():
        return
    # load json
    json_in = json.loads(data.read_text())
    # check requested fields
    requested = ["variable declaration", "plot config", "plot content"]
    for req in requested:
        if req not in json_in:
            return

    # -- update
    # - variable declaration
    table = self.variableDeclarationTable
    table.blockSignals(True)
    # clear
    for row in range(table.rowCount()):
        table.item(row, 0).setText("")
        table.item(row, 1).setText("")
    # populate
    for row, content in enumerate(json_in["variable declaration"]):
        table.item(row, 0).setText(content[0])
        table.item(row, 1).setText(content[1])
    table.blockSignals(False)

    # - plot config
    table = self.subplotSetupTable
    table.blockSignals(True)
    table.clearContents()
    for row, content in enumerate(json_in["plot config"]):
        for i, c in enumerate(content):
            table.setItem(row, i, QTableWidgetItem(c))
    table.blockSignals(False)
    updateSubplotLayout(self)

    # - plot content
    table = self.subplotContentTable
    table.blockSignals(True)
    table.clearContents()
    table.setRowCount(len(json_in["plot content"]))
    for row, content in enumerate(json_in["plot content"]):
        table.setItem(row, 0, QTableWidgetItem(content))
    table.blockSignals(False)

    refreshMetadataLivePlot(self)
