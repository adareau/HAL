# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 16:28:03
Modified : 2021-05-12 16:35:32

Comments : Functions related to quick data analysis
"""

# %% IMPORTS

# -- global
import logging
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
    QMenu,
    QAction,
    QActionGroup,
    QToolButton,
)

# -- local
import HAL.gui.dataexplorer as dataexplorer

# -- logger
logger = logging.getLogger(__name__)


# %% TOOLS


def _isnumber(x):
    try:
        float(x)
        return True
    except (TypeError, ValueError):
        return False


# %% SETUP FUNCTIONS


def setupQuickPlot(self):
    # -- data selection in quickplot
    # - X
    # define menu and selection group
    menuX = QMenu()
    actionGroupX = QActionGroup(menuX)
    actionGroupX.setExclusive(True)
    # store for future access
    self.quickPlotXToolButtonActionGroup = actionGroupX
    self.quickPlotXToolButton.actionGroup = actionGroupX
    # associate the menu with the corresponding toolbutton
    self.quickPlotXToolButton.setMenu(menuX)
    self.quickPlotXToolButton.setPopupMode(QToolButton.InstantPopup)
    # link label
    self.quickPlotXLabel.setText("no selection")
    self.quickPlotXToolButton.label = self.quickPlotXLabel

    # - Y
    # define menu and selection group
    menuY = QMenu()
    actionGroupY = QActionGroup(menuY)
    actionGroupY.setExclusive(True)
    # store for future access
    self.quickPlotYToolButtonActionGroup = actionGroupY
    self.quickPlotYToolButton.actionGroup = actionGroupY
    # associate the menu with the corresponding toolbutton
    self.quickPlotYToolButton.setMenu(menuY)
    self.quickPlotYToolButton.setPopupMode(QToolButton.InstantPopup)
    # link label
    self.quickPlotYLabel.setText("no selection")
    self.quickPlotYToolButton.label = self.quickPlotYLabel


# %% CALLBACKS


def quickPlotSelectionChanged(self):
    """Called when the quickPlot ToolButtons selection is changed"""
    # -- refresh string
    tool_buttons = [self.quickPlotXToolButton, self.quickPlotYToolButton]
    for button in tool_buttons:
        # get action group
        actionGroup = button.actionGroup
        # currently checked action
        current_action = actionGroup.checkedAction()
        if current_action is None:
            button.label.setText("no selection")
        else:
            name, par_name = current_action.data()
            button.label.setText("%s ⏵ %s" % (name, par_name))


def refreshMetaDataList(self):
    """
    Updates all the quickplot elements that allow the selection of metadata
    """
    # -- get data
    metadata_list = self.available_numeric_metadata

    # -- tool buttons
    tool_buttons = [self.quickPlotXToolButton, self.quickPlotYToolButton]
    for button in tool_buttons:
        # get action group
        actionGroup = button.actionGroup
        # currently checked action
        current_action = actionGroup.checkedAction()
        if current_action is not None:
            current_data = current_action.data()
        else:
            current_data = ("", "")
        # get menu and clear
        menu = button.menu()
        menu.clear()
        # remove all actions
        for action in actionGroup.actions():
            actionGroup.removeAction(action)
        # populate
        for name, param_list in metadata_list.items():
            # if empty list : stop
            if not param_list:
                continue
            # add submenu, and populate
            submenu = menu.addMenu(name)
            for par_name in param_list:
                action = QAction(
                    par_name,
                    menu,
                    checkable=True,
                    checked=current_data == (name, par_name),
                )
                action.setData((name, par_name))
                submenu.addAction(action)
                actionGroup.addAction(action)
        # update label
        current_action = actionGroup.checkedAction()
        if current_action is None:
            button.label.setText("no selection")
        else:
            name, par_name = current_action.data()
            button.label.setText("%s ⏵ %s" % (name, par_name))


# %% PLOT FUNCTIONS


def plotData(self):
    """
    PLACEHOLDER : Plotting the selected metadata
    """
    # -- load metadata
    # get selected metadata fields
    checkedDataX = self.quickPlotXToolButton.actionGroup.checkedAction()
    checkedDataY = self.quickPlotYToolButton.actionGroup.checkedAction()
    if None in [checkedDataX, checkedDataY]:
        logger.debug('plotData() : data selection missing')
        return

    # get data names
    # it is stored in the data() field of the quickPlot ToolButtons actions
    # in the form (meta_data_name, parameter_name)
    x_data_name = checkedDataX.data()
    y_data_name = checkedDataY.data()
    data_list = [x_data_name, y_data_name]

    # load metadata
    metadata = dataexplorer.getSelectionMetaDataFromCache(self)
    if len(metadata) == 0:
        logger.debug('plotData() : no dataset selected')
        return

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
    x_label = '%s - %s' % x_data_name
    x_info = data[x_meta].get("_%s_info" % x_name, None)
    if x_info is not None:
        unit = x_info.get("unit", "")
        if unit:
            x_label += " (%s)" % unit
    ax.set_xlabel(x_label)

    # y label
    y_meta, y_name = y_data_name
    y_label = '%s - %s' % y_data_name
    y_info = data[y_meta].get("_%s_info" % y_name, None)
    if y_info is not None:
        unit = y_info.get("unit", "")
        if unit:
            y_label += " (%s)" % unit
    ax.set_ylabel(y_label)

    # grid and legend
    plt.grid()
    plt.legend()

    # show
    fig.canvas.draw()
    plt.show()
