# %% IMPORTS

# -- global
import logging
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from datetime import datetime
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
from . import dataexplorer

# -- logger
logger = logging.getLogger(__name__)


def setupUi(self):
    # -- correlations variables list
    # setup selection and scroll mode
    self.correlationsVarsList.setSelectionMode(QAbstractItemView.MultiSelection)
    self.correlationsVarsList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.correlationsVarsList.setSortingEnabled(True)

    # -- hue selection in correlations
    # define menu and selection group
    menuHue = QMenu()
    actionGroupHue = QActionGroup(menuHue)
    actionGroupHue.setExclusive(True)
    # store for future access
    self.correlationsHueToolButtonActionGroup = actionGroupHue
    self.correlationsHueToolButton.actionGroup = actionGroupHue
    # associate the menu with the corresponding toolbutton
    self.correlationsHueToolButton.setMenu(menuHue)
    self.correlationsHueToolButton.setPopupMode(QToolButton.InstantPopup)
    # link label
    self.correlationsHueLabel.setText("no selection")
    self.correlationsHueToolButton.label = self.correlationsHueLabel


def correlationsSelectionChanged(self):
    """Called when the quickPlot ToolButtons selection is changed"""
    # -- refresh string
    tool_buttons = [
        self.correlationsHueToolButton,
    ]
    for button in tool_buttons:
        # get action group
        actionGroup = button.actionGroup
        # currently checked action
        current_action = actionGroup.checkedAction()
        if current_action is None:
            button.label.setText("no selection")
        else:
            name, par_name = current_action.data()
            button.label.setText(f"{name} ⏵ {par_name}")


def refreshMetaDataList(self):
    """
    Updates all the elements that allow the selection of metadata
    """
    # -- get data
    metadata_list = self.available_numeric_metadata

    # -- tool buttons
    tool_buttons = [
        self.correlationsHueToolButton,
    ]
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
            for par_name in sorted(param_list):
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
            button.label.setText(f"{name} ⏵ {par_name}")

    # list of available variables
    self.correlationsVarsList.clear()
    for name, param_list in metadata_list.items():

        if not param_list:
            continue

        for par_name in param_list:
            item = QListWidgetItem()
            item.setText(f"{name} ⏵ {par_name}")
            item.setData(Qt.UserRole, (name, par_name))
            self.correlationsVarsList.addItem(item)


def plotCorrelations(self):

    kind = self.correlationsKindComboBox.currentText()
    diag_kind = self.correlationsDiagKindComboBox.currentText()
    hue = None
    if self.correlationsHueCheckBox.isChecked():
        pass

    selection = self.correlationsVarsList.selectedItems()
    if not selection:
        return

    metadata = dataexplorer.getSelectionMetaDataFromCache(self)
    if len(metadata) == 0:
        logger.debug("plotData() : no dataset selected")
        return

    df = pd.DataFrame()

    for set, data in metadata.items():

        for par in selection:
            data_name = par.data(Qt.UserRole)
            df[f"{data_name[0]} - {data_name[1]}"] = data[data_name[0]][data_name[1]]

    sns.pairplot(df, hue=hue, kind=kind, diag_kind=diag_kind)
    plt.show()
