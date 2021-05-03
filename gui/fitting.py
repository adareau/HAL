# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 16:28:03
Modified : 2021-05-03 17:13:58

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
    for pos, center in zip(([0, 0], [1, 0], [1, 1], [0, 1]),
                           ([1, 1], [0, 1], [0, 0], [1, 0])):
        new_roi.addScaleHandle(pos=pos, center=center)

    # add to current image plot
    self.image_plot.addItem(new_roi)
    self.image_plot.addItem(roi_label)
    self.roi_list.append(new_roi)


def _roi_changed(self):
    # TODO : move self.label
    position = self.pos()
    size = self.size()
    self.label.setPos(position[0], position[1])


# %% FIT


def fit_data(self):
    """FIXME: temporary test for data fitting #quickanddirty"""
    # -- get last roi
    if len(self.roi_list) == 0:
        return

    roi = self.roi_list[-1]

    xmin, ymin = roi.pos()
    delta_x, delta_y = roi.size()
    xmax = xmin + delta_x
    ymax = ymin + delta_y

    Z = self.current_data.data

    Ny, Nx = Z.shape
    x = np.arange(Nx)
    y = np.arange(Ny)
    X, Y = np.meshgrid(x, y)

    print(xmin, xmax)
    print(np.min(X), np.max(X))
    print('------')
    print(ymin, ymax)
    print(np.min(Y), np.max(Y))
    print('------')

    # -- any shape  roi
    i_roi = (X > xmin) * (X < xmax) * (Y > ymin) * (Y < ymax)

    # -- square roi
    ix_min = np.searchsorted(x, xmin)
    ix_max = np.searchsorted(x, xmax)
    iy_min = np.searchsorted(y, ymin)
    iy_max = np.searchsorted(y, ymax)
    #X_roi = X[iy_min:iy_max, ix_min:ix_max]
    #Y_roi = Y[iy_min:iy_max, ix_min:ix_max]
    Z_roi = Z[ix_min:ix_max, iy_min:iy_max]
    print(ix_min, ix_max, iy_min, iy_max)
    plt.figure()
    #plt.pcolormesh(X_roi, Y_roi, Z_roi)
    plt.imshow(Z_roi)
    plt.show()
