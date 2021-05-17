# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-17 09:36:42
Modified : 2021-05-17 13:06:08

Comments : Implement the "Advanced data analysis"
"""

# %% IMPORTS

# -- global
import logging
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
from HAL.classes.display import LiveMetaData

# -- logger
logger = logging.getLogger(__name__)


# %% GLOBAL VARIABLES
NAME_SEPARATION_CHARACTER = "."
NAME_REGEXP_FORMAT = "\w*"
VARIABLE_REGEXP_FORMAT = "[\w_\-:.\s]*"


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


def checkVariableDeclaration(self):
    """checks that the variable declaration is sound, and issue warnings"""
    # -- get table object and row number
    table = self.variableDeclarationTable
    n_row = table.rowCount()
    print(n_row)
    # --


def refreshMetadataLivePlot(self):
    """if the current display mode is set to LiveMetaData, refresh the plot"""
    logger.debug("refresh metadata display")

    # -- check whether the current display is an instance of LiveMetaData
    if not isinstance(self.display, LiveMetaData):
        logger.debug("NOT A LiveMetaData INSTANCE")
        return

    # -- refresh
    logger.debug("GO ON !")


# %% CALLBACKS


def variableDeclarationChanged(self, item):
    """called when the content of the variable declaration table is changed"""
    # -- check the declaration
    checkVariableDeclaration(self)


def exportToMatplotlib(self):
    """ Placeholder. TODO : implement"""
    logger.debug("export to MPL !")
