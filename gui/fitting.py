# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 16:28:03
Modified : 2021-05-04 15:06:01

Comments : Functions related to data fitting
"""

# %% IMPORTS

# -- global
import json
import jsbeautifier as jsb
import pyqtgraph as pg
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path
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
from HAL.classes.fit.abstract import NumpyArrayEncoder, Abstract2DFit
from HAL.classes.data.abstract import AbstractCameraPictureData

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


def _fit_2D_data(self, Z, XY, data_object):
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
    # get sizes / units from data object
    px_size_x, px_size_y = data_object.pixel_scale
    unit_x, unit_y = data_object.pixel_unit
    # update sizez / units in fit object
    fit.pixel_size_x = px_size_x
    fit.pixel_size_y = px_size_y
    fit.pixel_size_x_unit = unit_x
    fit.pixel_size_y_unit = unit_y
    # guess / fit / compute values
    fit.do_guess()
    fit.do_fit()
    fit.compute_values()

    return fit


def _generate_roi_result_dic(roi, fit):
    """generates a dictionnary with the fit results for a given roi,
       including information about the roi itself, in order to be
       saved as part of the global fit result """

    # -- initialize the dictionnary
    roi_dic = {}

    # -- store roi info
    # position
    roi_dic["pos"] = {
        "value": list(roi.pos()),
        "unit": "px",
        "comment": "roi position (lower left corner)",
    }
    # position
    roi_dic["size"] = {
        "value": list(roi.size()),
        "unit": "px",
        "comment": "roi size",
    }

    # -- store fit info
    roi_dic["result"] = fit.export_dic()

    return roi_dic


def _generate_fit_result_dic(self, roi_collection, fit, data_object):
    """generates the global fit dictionnary, to be exported/saved"""

    # -- initialize
    fit_dic = {}

    # -- store comments
    name = self._name
    version = self._version
    url = self._url
    com_str = "Generated with %s v%s (need help? check %s)"
    fit_dic["__comment__"] = com_str % (name, version, url)
    fit_dic["__program__"] = name
    fit_dic["__version__"] = version
    fit_dic["__url__"] = url

    # -- fit info
    fit_info = {}

    # generic fit info
    fit_info["fit name"] = fit.name
    fit_info["fit formula"] = fit.formula_help
    fit_info["fit parameters"] = fit.parameters_help
    fit_info["fit version"] = fit._version
    fit_info["generated on"] = str(datetime.now())

    # specific to 2D fits
    if isinstance(fit, Abstract2DFit):
        fit_info["pixel_size_x"] = {
            "value": fit.pixel_size_x,
            "unit": fit.pixel_size_x_unit,
            "comment": "physical size of a pixel (x axis)",
        }
        fit_info["pixel_size_y"] = {
            "value": fit.pixel_size_y,
            "unit": fit.pixel_size_y_unit,
            "comment": "physical size of a pixel (y axis)",
        }
        fit_info["count_conversion_factor"] = {
            "value": fit.count_conversion_factor,
            "unit": fit.converted_count_unit,
            "comment": "converts image counts into physically meaning quantity (e.g. atom number)",
        }

    # store
    fit_dic["__fit_info__"] = fit_info

    # -- data info
    data_info = {}

    # generic data info
    data_info["data path"] = str(data_object.path)
    data_info["data type"] = data_object.name
    data_info["data dimension"] = data_object.dimension
    data_info["pixel scale"] = data_object.pixel_scale
    data_info["pixel unit"] = data_object.pixel_unit

    # specific to camera pictures
    if isinstance(data_object, AbstractCameraPictureData):
        data_info["data class"] = "camera picture"
        data_info["camera pixel size"] = {
            "value": data_object.pixel_size,
            "unit": data_object.pixel_unit,
        }
        data_info["magnification"] = data_object.magnification

    # store
    fit_dic["__data_info__"] = data_info

    # -- store roi collection
    fit_dic["collection"] = roi_collection

    return fit_dic


def _save_fit_result_as_json(self, fit_dic, data_object):
    """saves all fit information as a json file"""
    # -- format json
    # normal json
    json_str = json.dumps(fit_dic, ensure_ascii=False, cls=NumpyArrayEncoder)
    # make it BeAUTiFuL !!!!
    json_str = jsb.beautify(json_str)

    # -- save it
    # generate path
    data_path = Path(data_object.path)  # ensure we have a Path() object
    data_root = data_path.parent  # data folder
    data_stem = data_path.stem  # data name (without extension !)
    # create fit folder
    fit_folder_name = self.settings.config["fit"]["fit folder name"]
    fit_folder = data_root / fit_folder_name
    fit_folder.mkdir(exist_ok=True)
    # write
    fit_file = fit_folder / (data_stem + ".json")
    fit_file.write_text(json_str)


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

    fit_collection = []
    for roi in self.mainScreen.roi_list:
        # get roi data
        Z, XY = _get_2D_roi_data(self, roi)
        # fit the data
        fit = _fit_2D_data(self, Z, XY, data_object)
        if fit is None:
            # to handle the cas where the fit is not implemented
            # (cf. _fit_2D_data)
            # TODO : raise an error instead ?
            return
        # fit.plot_fit_result()  # TEMP
        # store for later
        fit_collection.append((roi, fit))

    # -- save fit
    # - prepare fit collection
    roi_collection = {}
    for (roi, fit) in fit_collection:
        # prepare dictionnary with results for the current roi
        roi_dic = _generate_roi_result_dic(roi, fit)
        # save it to the global dic
        n_roi = roi.number
        roi_collection["roi%i" % n_roi] = roi_dic

    # - prepare fit dict
    fit_dic = _generate_fit_result_dic(self, roi_collection, fit, data_object)

    # - save as json
    _save_fit_result_as_json(self, fit_dic, data_object)
