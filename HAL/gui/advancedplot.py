# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-17 09:36:42
Modified : 2021-05-17 14:09:04

Comments : Implement the "Advanced data analysis"
"""

# %% IMPORTS

# -- global
import logging
import re
import pyqtgraph as pg
import numpy as np
from matplotlib import cm
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QCompleter,
    QLineEdit,
    QTableWidgetItem,
)

# -- local
import HAL.gui.dataexplorer as dataexplorer
from HAL.classes.display import LiveMetaData

# -- logger
logger = logging.getLogger(__name__)


# %% GLOBAL VARIABLES
NAME_SEPARATION_CHARACTER = "."
NAME_REGEXP_FORMAT = "\w*"
VARIABLE_REGEXP_FORMAT = "[\w_\-:.\s]*"
VARIABLE_SPLIT_FORMAT = "^([\w_\-:\s]*)\.([\w_\-:\s]*)$"

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


# %% TOOL

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


# %% SETUP FUNCTIONS


def setupAdvancedPlot(self):
    global NAME_REGEXP_FORMAT, VARIABLE_REGEXP_FORMAT

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
        # return
        mapped_variables[name] = metadata_dic[meta_name][meta_parname]

    return mapped_variables


def refreshMetadataLivePlot(self):
    """if the current display mode is set to LiveMetaData, refresh the plot"""
    logger.debug("refresh metadata display")

    # -- check whether the current display is an instance of LiveMetaData
    if not isinstance(self.display, LiveMetaData):
        logger.debug("NOT A LiveMetaData INSTANCE")
        return

    # -- get metadata list
    metadata = dataexplorer.getSelectionMetaDataFromCache(self)

    # -- refresh
    # TEMP: quick and dirty implementation, to test
    screen = self.mainScreen
    screen.clear()
    subplot = screen.addPlot(0, 0)
    subplot.addLegend()
    iplot = 0
    for setname, metadata_dic in metadata.items():
        mapped_variables = mapVariables(self, metadata_dic)
        if mapped_variables.keys() >= {"x", "y"}:
            color = gimmeColor(iplot)
            iplot += 1
            isort = np.argsort(mapped_variables["x"])
            x = np.array(mapped_variables["x"])
            y = np.array(mapped_variables["y"])
            pitem = pg.PlotDataItem(
                x[isort],
                y[isort],
                pen=color,
                symbolBrush=color,
                symbolPen=color,
                symbol="o",
                symbolSize=8,
                name=setname,
            )
            subplot.addItem(pitem)


# %% CALLBACKS


def variableDeclarationChanged(self, item):
    """called when the content of the variable declaration table is changed"""
    # -- refresh display
    refreshMetadataLivePlot(self)


def exportToMatplotlib(self):
    """ Placeholder. TODO : implement"""
    logger.debug("export to MPL !")
