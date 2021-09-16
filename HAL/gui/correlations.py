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


def refreshMetaDataList(self):
    """
    Updates all the elements that allow the selection of metadata
    """
    # -- get data
    metadata_list = self.available_numeric_metadata

    for name, param_list in metadata_list.items():

        if not param_list:
            continue

        item = QListWidgetItem()
        item.setText(name)
        self.correlationsVarsList.addItem(item)
