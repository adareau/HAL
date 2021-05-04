# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 16:28:03
Modified : 2021-05-04 11:39:22

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


def _get_2D_roi_data(self, roi):
    """ returns the currently displayed data in the provided roi"""
    # -- get current data and image item
    # TODO : migrate to a method in the display data class ?
    data = self.mainScreen.current_data.data
    image_item = self.mainScreen.current_image

    # -- get roi data
    # use the convenient 'getArrayRegion' to retrieve selected image roi
    Z, XY = roi.getArrayRegion(data, image_item, returnMappedCoords=True)
    X = XY[0, :, :]
    Y = XY[1, :, :]

    return Z, (X, Y)


def _fit_2D_data(self, Z, XY):
    """handles data fitting"""
    # -- get selected fit
    selected_fit = self.fitTypeComboBox.currentText()
    if selected_fit not in self.fit_classes:
        print("ERROR : fit '%s' is not implemented ?!" % selected_fit)
        return
    fit_class = self.fit_classes[selected_fit]
    # -- fit
    # init fit object
    fit = fit_class(x=XY, z=Z)
    # guess / fit / compute values
    fit.do_guess()
    fit.do_fit()
    fit.compute_values()

    return fit


# == high level fit function


def fit_data(self):
    """high level function for data fitting. Loop on all defined ROIs,
       fit the data, and save results"""

    # -- check current data object (for dimension)
    # TODO : migrate to a method in the display data class ?
    data_object = self.mainScreen.current_data
    if data_object.dimension != 2:
        print("ERROR : fit only implemented for 2D data !")
        return

    # -- loop on roi list
    if len(self.mainScreen.roi_list) == 0:
        print("ERROR : no ROI selected !!")
        return

    for roi in self.mainScreen.roi_list:
        # get roi data
        Z, XY = _get_2D_roi_data(self, roi)
        # fit the data
        fit = _fit_2D_data(self, Z, XY)
        if fit is None:
            # to handle the cas where the fit is not implemented
            # (cf. _fit_2D_data)
            # TODO : raise an error instead ?
            return
        # TEMP : plot
        fit.plot_fit_result()
