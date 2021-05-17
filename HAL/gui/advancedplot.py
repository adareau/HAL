# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-17 09:36:42
Modified : 2021-05-17 10:42:52

Comments : Implement the "Advanced data analysis"
"""

# %% IMPORTS

# -- global
import logging
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QCompleter,
    QLineEdit,
    QTableWidgetItem,
)

# -- local

# -- logger
logger = logging.getLogger(__name__)


# %% CUSTOM CLASS FOR AUTOCOMPLETION
# cf. https://stackoverflow.com/q/60750357


class TableItemCompleter(QtWidgets.QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        completionlist = index.data(Qt.UserRole)
        autoCompleter = QCompleter(completionlist, parent)
        autoCompleter.setCaseSensitivity(Qt.CaseInsensitive)
        autoCompleter.setFilterMode(Qt.MatchContains)
        editor.setCompleter(autoCompleter)
        return editor


# %% SETUP FUNCTIONS


def setupAdvancedPlot(self):
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
        comp_list = [""]
        item = QTableWidgetItem("")
        item.setData(Qt.UserRole, comp_list)
        table.setItem(rows, 1, item)


# %% LOW-LEVEL FUNCTIONS AND TOOLS


def _checkVariableDeclaration(self):
    """checks that the variable declaration is sound, and issue warnings"""
    # -- get table object and row number
    table = self.variableDeclarationTable
    n_row = table.rowCount()
    print(n_row)
    # --


# %% CALLBACKS


def variableDeclarationChanged(self, item):
    """called when the content of the variable declaration table is changed"""
    # -- check the declaration
    _checkVariableDeclaration(self)


def exportToMatplotlib(self):
    """ Placeholder. TODO : implement"""
    logger.debug("export to MPL !")
