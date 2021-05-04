# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 16:28:03
Modified : 2021-05-04 11:23:01

Comments : Functions related to data fitting
"""

# %% IMPORTS

# -- global
import pyqtgraph as pg
import numpy as np
import matplotlib.pyplot as plt
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
    # -- setup fit selection combo box
    for fit_name in self.fit_classes:
        self.fitTypeComboBox.addItem(fit_name)


# %% ROI MANAGEMENT


def addROI(self):
    """
    FIXME: this is a test with PyQtGraph ROIs, we will have the think the ROI
    management when working on the fitting classes !
    """
    # -- add new ROI
    if self.mainScreen.image_plot is None:
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
    n_roi = len(self.mainScreen.roi_list)
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
    for pos, center in zip(
        ([0, 0], [1, 0], [1, 1], [0, 1]), ([1, 1], [0, 1], [0, 0], [1, 0])
    ):
        new_roi.addScaleHandle(pos=pos, center=center)

    # add to current image plot
    self.mainScreen.image_plot.addItem(new_roi)
    self.mainScreen.image_plot.addItem(roi_label)
    self.mainScreen.roi_list.append(new_roi)


def _roi_changed(self):
    # TODO : move self.label
    position = self.pos()
    size = self.size()
    self.label.setPos(position[0], position[1])


# %% FIT

# == low level functions


# == high level fit function


def fit_data(self):
    """FIXME: temporary test for data fitting #quickanddirty"""
    # -- get roi information
    # select last roi
    if len(self.mainScreen.roi_list) == 0:
        return
    roi = self.mainScreen.roi_list[-1]
    # get position and size
    pos = roi.pos()
    size = roi.size()

    # -- get image region
    # get current image data (=array)
    # TODO : migrate to a method in the display data class ?
    Z = self.mainScreen.current_data.data
    # use the convenient 'getArrayRegion' to retrieve selected image roi
    Z_roi, XY_roi = roi.getArrayRegion(
        Z, self.mainScreen.current_image, returnMappedCoords=True
    )
    # separate X and Y coordinates
    X_roi = XY_roi[0, :, :]
    Y_roi = XY_roi[1, :, :]

    # -- FIT
    # get selected fit
    selected_fit = self.fitTypeComboBox.currentText()
    if selected_fit not in self.fit_classes:
        return
    fit_class = self.fit_classes[selected_fit]
    # init fit object
    fit = fit_class(x=(X_roi, Y_roi), z=Z_roi)
    # guess / fit / compute values
    fit.do_guess()
    print(fit.guess)
    fit.do_fit()
    fit.compute_values()
    # TEMP : print results
    print(fit.export_json_str())
    fit.plot_fit_result()
