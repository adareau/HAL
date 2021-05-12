# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 16:28:03
Modified : 2021-05-07 16:21:46

Comments : Functions related to data fitting
"""

# %% IMPORTS

# -- global
import logging
import json
import jsbeautifier as jsb
from datetime import datetime
from pathlib import Path

# -- local
from HAL.classes.fit.abstract import NumpyArrayEncoder, Abstract2DFit
from HAL.classes.fit import implemented_fit_dic
from HAL.classes.data.abstract import AbstractCameraPictureData

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


def setupFitting(self):
    # -- setup fit selection combo box
    for fit_name in self.fit_classes:
        self.fitTypeComboBox.addItem(fit_name)


# %% ROI MANAGEMENT


def addROI(self, roi_name=None):
    """ adds a new roi to the current display"""

    # define roi style
    roi_style = {"color": "#3FFF53FF", "width": 2}
    roi_hover_style = {"color": "#FFF73FFF", "width": 2}
    handle_style = {"color": "#3FFF53FF", "width": 2}
    handle_hover_style = {"color": "#FFF73FFF", "width": 2}

    # define label style
    label_color = "#3FFF53FF"
    if roi_name is None:
        n_roi = len(self.display.getROINames())
        roi_name = "ROI %i" % n_roi

    # add roi
    self.display.addROI(
        roi_name=roi_name,
        roi_style=roi_style,
        roi_hover_style=roi_hover_style,
        handle_style=handle_style,
        handle_hover_style=handle_hover_style,
        label_color=label_color,
    )


# %% BACKGROUND MANAGEMENT


def addBackground(self):
    """ add a background"""

    # define roi style
    background_style = {"color": "#FF3F3FFF", "width": 2}
    background_hover_style = {"color": "#FFF73FFF", "width": 2}
    handle_style = {"color": "#FF3F3FFF", "width": 2}
    handle_hover_style = {"color": "#FFF73FFF", "width": 2}

    # define label style
    label_color = "#FF3F3FFF"

    # add roi
    self.display.addBackground(
        background_style=background_style,
        background_hover_style=background_hover_style,
        handle_style=handle_style,
        handle_hover_style=handle_hover_style,
        label_color=label_color,
    )


def removeBackground(self):
    """removes the background"""
    self.display.removeBackground()


# %% FIT

# == low level functions


def _fit_2D_data(self, Z, XY, data_object):
    """handles data fitting"""
    # -- get selected fit
    selected_fit = self.fitTypeComboBox.currentText()
    if selected_fit not in self.fit_classes:
        logger.error("fit '%s' is not implemented ?!" % selected_fit)
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


def _generate_roi_result_dic(display, roi_name, fit):
    """generates a dictionnary with the fit results for a given roi,
       including information about the roi itself, in order to be
       saved as part of the global fit result """

    # -- initialize the dictionnary
    roi_dic = {}

    # -- store roi info
    # position
    roi_dic["pos"] = {
        "value": display.getROIPos(roi_name),
        "unit": "px",
        "comment": "roi position (lower left corner)",
    }
    # position
    roi_dic["size"] = {
        "value": display.getROISize(roi_name),
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
    fit_info["generated on"] = datetime.now().strftime("%y-%m-%d %H:%M:%S")

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

    # get background
    background = getattr(self.display, "background", None)
    if background is not None:
        logger.debug("saving background")
        back = {}
        back["pos"] = {
            "value": self.display.getBackgroundPos(),
            "unit": "px",
            "comment": "background position (lower left corner)",
        }
        back["size"] = {
            "value": self.display.getBackgroundSize(),
            "unit": "px",
            "comment": "background size",
        }
        fit_info["background"] = back
    else:
        logger.debug("NOT saving background")

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
            "unit": data_object.pixel_size_unit,
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
    fit_file = _gen_saved_fit_path(self, data_object.path)
    fit_folder = fit_file.parent
    fit_folder.mkdir(exist_ok=True)
    # write
    fit_file.write_text(json_str)


def _gen_saved_fit_path(self, data_path):
    """generates a saved fit path from data path"""

    # take data path
    data_path = Path(data_path)  # ensure we have a Path() object
    data_root = data_path.parent  # data folder
    data_stem = data_path.stem  # data name (without extension !)

    # gen fit folder path
    fit_folder_name = self.settings.config["fit"]["fit folder name"]
    fit_folder = data_root / fit_folder_name

    # get fit file path
    fit_file = fit_folder / (data_stem + ".json")
    return fit_file


def saved_fit_exist(self, data_path=None):
    """checks whether there is a saved fit for the data. If a path is provided,
       look for a fit linked to this data path. Otherwise, use current data
       path"""

    # if no path provided: use current data
    if data_path is None:
        data_object = self.display.getCurrentDataObject()
        data_path = Path(data_object.path)

    # generate saved fit path
    fit_file = _gen_saved_fit_path(self, data_path)

    return fit_file.is_file()


def load_saved_fit(self, data_path=None):
    """loads a saved fit"""

    # -- load saved fit
    # if no path provided: use current data
    if data_path is None:
        data_object = self.display.getCurrentDataObject()
        data_path = Path(data_object.path)

    # generate saved fit path
    fit_file = _gen_saved_fit_path(self, data_path)

    # if does not exist : return
    if not fit_file.is_file():
        return None, None

    # load
    fit_json = json.loads(fit_file.read_text())

    # -- analyze fit
    # get fit info
    if "__fit_info__" not in fit_json:
        logger.warning("no fit info found...")
        return None, None

    fit_info = fit_json["__fit_info__"]
    fit_name = fit_info["fit name"]
    fit_version = fit_info["fit version"]

    # check fit name
    if fit_name not in implemented_fit_dic:
        logger.warning("saved fit '%s' is not implemented !" % fit_name)
        return None, None

    # check fit version
    fit_class = implemented_fit_dic[fit_name]
    if fit_class()._version != fit_version:
        msg = "saved fit version (%s) does not match " % fit_version
        msg += "the current implemented version (%s) " % fit_class()._version
        msg += "for the '%s' fit class" % fit_name
        msg += "I will try to go on though..."
        logger.warning(msg)

    # load
    fit_collection = {}
    for roi_name, roi_info in fit_json["collection"].items():
        # get fit result
        fit_res = roi_info["result"]
        # generate a fit object
        fit = fit_class()
        fit.popt = fit_res["popt"]
        fit.pcov = fit_res["pcov"]
        fit.perr = fit_res["perr"]
        # save
        fit_collection[roi_name] = {
            "pos": roi_info["pos"],
            "size": roi_info["size"],
            "fit": fit,
        }

    return fit_collection, fit_info


# == high level fit function


def fit_data(self):
    """high level function for data fitting. Loop on all defined ROIs,
       fit the data, and save results"""

    # -- check current data object (for dimension)
    data_object = self.display.getCurrentDataObject()
    if data_object is None:
        logger.warning("select data first...")
        return

    if data_object.dimension != 2:
        logger.warning("fit only implemented for 2D data !")
        return

    # -- loop on roi list
    if len(self.display.getROINames()) == 0:
        logger.warning("ERROR : no ROI defined !!")
        return

    fit_collection = []
    for roi_name in self.display.getROINames():
        # get roi data
        Z, XY = self.display.getROIData(roi_name)
        if Z is None:
            continue
        # fit the data
        fit = _fit_2D_data(self, Z, XY, data_object)
        if fit is None:
            # to handle the cas where the fit is not implemented
            # (cf. _fit_2D_data)
            # TODO : raise an error instead ?
            return
        # fit.plot_fit_result()  # TEMP
        # store for later
        fit_collection.append((roi_name, fit))

    # -- save fit
    # - prepare fit collection
    roi_collection = {}
    for (roi_name, fit) in fit_collection:
        # prepare dictionnary with results for the current roi
        roi_dic = _generate_roi_result_dic(self.display, roi_name, fit)
        # save it to the global dic
        roi_collection[roi_name] = roi_dic

    # - prepare fit dict
    fit_dic = _generate_fit_result_dic(self, roi_collection, fit, data_object)

    # - save as json
    _save_fit_result_as_json(self, fit_dic, data_object)
