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


def refreshMetaDataList(self):
    """
    Updates all the elements that allow the selection of metadata
    """
    # -- get data
    metadata_list = self.available_numeric_metadata
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

    print(df)

    sns.pairplot(df, diag_kind="kde")
    plt.show()

    # for set, data in metadata.items():
