# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 16:28:03
Modified : 2021-04-30 14:05:31

Comments : Functions related to quick data analysis
"""

# %% IMPORTS

# -- global
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QInputDialog,
    QAbstractItemView,
    QStyle,
    QListWidgetItem,
    QMessageBox,
)


# -- local
import HAL.gui.dataexplorer as dataexplorer

# %% TOOLS


def _isnumber(x):
    try:
        float(x)
        return True
    except (TypeError, ValueError):
        return False


# %% SETUP FUNCTIONS


def setupQuickPlot(self):
    pass


# %% PLOT FUNCTIONS


def plotData(self):
    """
    PLACEHOLDER : Plotting the selected metadata
    """
    # -- load metadata
    # get selected metadata fields
    x_data_name = self.quickPlotXComboBox.currentData()
    y_data_name = self.quickPlotYComboBox.currentData()
    data_list = [x_data_name, y_data_name]
    if x_data_name is None or y_data_name is None:
        return

    # load metadata
    metadata = dataexplorer.getMetaData(self, data_list=data_list)

    # -- PLOT
    # - prepare figure
    # FIXME : allow for new figure / hold on control via GUI
    if self.current_fig is None:
        fig, ax = plt.subplots(1, 1)
        self.current_fig = (fig, ax)
    else:
        fig, ax = self.current_fig
        if not plt.fignum_exists(fig.number):
            fig, ax = plt.subplots(1, 1)
            self.current_fig = (fig, ax)

    # - loop on sets
    for set, data in metadata.items():
        # - filter data
        # get data
        x_raw = data[x_data_name[0]][x_data_name[1]]
        y_raw = data[y_data_name[0]][y_data_name[1]]
        # remove non numeric values
        x_filtered = []
        y_filtered = []
        for i, (x, y) in enumerate(zip(x_raw, y_raw)):
            if not _isnumber(x) or not _isnumber(y):
                continue
            x_filtered.append(float(x))
            y_filtered.append(float(y))

        # if empty : continue
        if not x_filtered:
            continue

        x_filtered = np.array(x_filtered)
        y_filtered = np.array(y_filtered)

        # sort
        isort = np.argsort(x_filtered)
        x_filtered = x_filtered[isort]
        y_filtered = y_filtered[isort]
        # - plot

        ax.plot(x_filtered, y_filtered, ":o", label=set)

    # - figure setup
    # x label
    x_meta, x_name = x_data_name
    x_info = data[x_meta]["%s_info" % x_name]
    x_label = x_info["name"]
    if x_info["unit"]:
        x_label += " (%s)" % x_info["unit"]
    ax.set_xlabel(x_label)

    # y label
    y_meta, y_name = y_data_name
    y_info = data[y_meta]["%s_info" % y_name]
    y_label = y_info["name"]
    if y_info["unit"]:
        y_label += " (%s)" % y_info["unit"]
    ax.set_ylabel(y_label)

    # grid and legend
    plt.grid()
    plt.legend()

    # show
    fig.canvas.draw()
    plt.show()
