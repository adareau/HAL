# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 16:28:03
Modified : 2021-04-30 16:29:32

Comments : Functions related to data fitting
"""

# %% IMPORTS

# -- global
import pyqtgraph as pg
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


# %% TOOLS


def _isnumber(x):
    try:
        float(x)
        return True
    except (TypeError, ValueError):
        return False


# %% SETUP FUNCTIONS


def setupFitting(self):
    pass


# %% ROI MANAGEMENT


def addROI(self):
    """
    FIXME: this is a test with PyQtGraph ROIs, we will have the think the ROI
    management when working on the fitting classes !
    """
    # -- add new ROI
    if self.image_plot is None:
        # no 'image plot' initialized, return !
        return

    # define roi style
    roi_style = {"color": "#3FFF53FF", "width": 2}
    roi_hover_style = {"color": "#FFF73FFF", "width": 2}
    handle_style = {"color": "#3FFF53FF", "width": 2}
    handle_hover_style = {"color": "#FFF73FFF", "width": 2}

    # create roi object
    new_roi = pg.RectROI(
        pos=[0, 0],
        size=[50, 50],
        rotatable=False,
        pen=roi_style,
        hoverPen=roi_hover_style,
        handlePen=handle_style,
        handleHoverPen=handle_hover_style,
    )

    # add a label
    n_roi = len(self.roi_list)
    roi_label = pg.TextItem("ROI %i" % n_roi, color="#3FFF53FF")
    roi_label.setPos(0, 0)
    new_roi.label = roi_label  # link to roi !!
    new_roi.number = n_roi

    # TODO : make it such that the label follows the ROI !
    # using sigRegionChanged
    new_roi.sigRegionChanged.connect(_roi_changed)

    # add scale handles
    for pos in ([1, 0.5], [0, 0.5], [0.5, 0], [0.5, 1]):
        new_roi.addScaleHandle(pos=pos, center=[0.5, 0.5])

    # add to current image plot
    self.image_plot.addItem(new_roi)
    self.image_plot.addItem(roi_label)
    self.roi_list.append(new_roi)


def _roi_changed(self):
    # TODO : move self.label
    position = self.pos()
    size = self.size()
    self.label.setPos(position[0], position[1])
