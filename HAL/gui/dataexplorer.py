# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 16:28:03

Comments : Functions related to (meta)data exploration
"""

# %% IMPORTS

# -- global
import json
import logging
import re
from numpy import NaN
from random import choice
from collections import OrderedDict
from pathlib import Path
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
    QToolButton,
)

# -- local
from . import quickplot, advancedplot, correlations, quotes
from .misc import wrap_text, dialog

# -- logger
logger = logging.getLogger(__name__)

# %% GLOBAL
TITLE_STR = "[%s]\n"
PREFIX_CORE = "├─ "
PREFIX_LAST = "└─ "


# %% SETUP FUNCTIONS


def setupUi(self):
    # -- dataset managements
    menu = QMenu()
    self.dataSetCreateAction = QAction("create new set", self.dataSetToolButton)
    menu.addAction(self.dataSetCreateAction)
    self.dataSetDeleteAction = QAction("delete sets", self.dataSetToolButton)
    menu.addAction(self.dataSetDeleteAction)
    self.dataSetRenameAction = QAction("rename set", self.dataSetToolButton)
    menu.addAction(self.dataSetRenameAction)
    self.dataSetAddAction = QAction("add run(s) to set", self.dataSetToolButton)
    menu.addAction(self.dataSetAddAction)
    self.dataSetFavAction = QAction("add set to favorite", self.dataSetToolButton)
    menu.addAction(self.dataSetFavAction)
    self.dataSetToolButtonMenu = menu
    self.dataSetToolButton.setMenu(menu)
    self.dataSetToolButton.setPopupMode(QToolButton.InstantPopup)

    # -- meta data text display
    self.metaDataText.setReadOnly(True)
    self.metaDataText.setLineWrapMode(self.metaDataText.NoWrap)

    # -- meta data list
    # setup selection and scroll mode
    self.metaDataList.setSelectionMode(QAbstractItemView.MultiSelection)
    self.metaDataList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    # add all metadata classes names
    for metadata in self.metadata_classes:
        item = QListWidgetItem()
        item.setText(metadata().name)
        self.metaDataList.addItem(item)
    # select all
    self.metaDataList.blockSignals(True)
    for i in range(self.metaDataList.count()):
        self.metaDataList.item(i).setSelected(True)
    self.metaDataList.blockSignals(False)

    # -- set list
    self.setList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.setList.setSelectionMode(QAbstractItemView.ExtendedSelection)
    self.setList.setIconSize(QSize(15, 15))

    # -- setup display text
    selected_quote = choice(quotes)
    selected_quote = wrap_text(selected_quote, 38)
    self.metaDataText.setPlainText(selected_quote)


# %% META DATA MANAGEMENT


def _loadFileMetaData(self, path):
    """
    Subfunction, loads the metadata linked to one file
    """
    # -- get metadata
    # get selected metadata sources
    selected_metadata = [item.text() for item in self.metaDataList.selectedItems()]

    # values are then sorted in an ordered dict
    metadata_dic = OrderedDict()
    for meta_class in self.metadata_classes:
        # init metadata object
        meta = meta_class()
        # only keep the selected ones
        if meta.name not in selected_metadata:
            continue
        # load metadata
        meta.path = path
        meta.analyze()
        # store in dic
        metadata_dic[meta.name] = meta

    return metadata_dic


def updateMetadataCache(self, reset_cache=False):
    """
    Updates the metadata cache
    """
    # logger.debug("update metadata cache")

    # -- reset ?
    if reset_cache:
        self.metadata_cache = {}

    # -- get list of selected runs and datasets
    # total selection
    all_selected_files = set()

    # add the current selection
    for item in self.runList.selectedItems():
        all_selected_files.add(item.data(Qt.UserRole))

    # get selected datasets
    selected_datasets = [
        item.data(Qt.UserRole) for item in self.setList.selectedItems()
    ]
    # get corresponding paths
    for dataset in selected_datasets:
        if dataset is None:
            continue
        if dataset.is_file():
            # load json
            set_json = json.loads(dataset.read_text())
            # get list of paths
            json_paths = set_json.get("paths", [])
            # get "data root" tag, and replace it by the local data root
            if "root tag" in set_json:
                conf = self.settings.config
                root = Path(conf["data"]["root"])
                root = str(root.expanduser())
                tag = set_json["root tag"]
                pattern = "^%s" % tag
                json_paths = [re.sub(pattern, root, p) for p in json_paths]
            # convert to path objects
            for path in json_paths:
                all_selected_files.add(Path(path))

    # -- remove from cache
    for cached_file in list(self.metadata_cache.keys()):
        if cached_file not in all_selected_files:
            self.metadata_cache.pop(cached_file)

    # -- update cache
    for i_file, file_to_cache in enumerate(all_selected_files):
        if file_to_cache in self.metadata_cache:
            # ignore
            continue
        if not file_to_cache.is_file():
            logger.debug("'%s' does not exist." % file_to_cache)
            continue
        file_metadata = _loadFileMetaData(self, file_to_cache)
        self.metadata_cache[file_to_cache] = file_metadata

    # logger.debug("Files in cache : %i" % len(self.metadata_cache))

    # -- update available metadata lists
    # init new list
    meta_names = [m().name for m in self.metadata_classes]
    available_metadata = OrderedDict([(m, set()) for m in meta_names])
    available_numeric_metadata = OrderedDict([(m, set()) for m in meta_names])
    # loop
    for cached_file, metadata in self.metadata_cache.items():
        for name, meta in metadata.items():
            keys = {p["name"] for p in meta.data}
            num_keys = {k for k in meta.get_numeric_keys()}
            available_metadata[name] |= keys  # set union !!
            available_numeric_metadata[name] |= num_keys  # set union !!

    # store
    self.available_metadata = available_metadata
    self.available_numeric_metadata = available_numeric_metadata

    # -- update gui elements
    quickplot.refreshMetaDataList(self)
    advancedplot.refreshMetaDataList(self)
    advancedplot.refreshMetadataLivePlot(self)
    correlations.refreshMetaDataList(self)


def _generateMetadaListFromCache(self, path_list):
    """
    Subfunction, generates a list of metadata from cache
    """
    # -- initialize output dictionnary, populated with 'NaNs'
    meta_dic = {}
    for meta_name, meta_param_list in self.available_metadata.items():
        meta_dic[meta_name] = {}
        for param_name in meta_param_list:
            meta_dic[meta_name][param_name] = [NaN for p in path_list]

    # -- populate from cache
    for i_file, file_path in enumerate(path_list):
        # if file not cached : skip
        # NB : this should not happen, due to the way the programm is
        #      structured...
        if file_path not in self.metadata_cache:
            logger.warning("file %s not cached" % file_path)
            continue
        # get cached metadata
        cached_metadata = self.metadata_cache[file_path]
        for meta_name, meta in cached_metadata.items():
            for param in meta.data:
                # store value
                meta_dic[meta_name][param["name"]][i_file] = param["value"]
                # store param to get info
                meta_dic[meta_name]["_%s_info" % param["name"]] = param

    return meta_dic


def getSelectionMetaDataFromCache(self, update_cache=False):
    """
    returns a dictionnary of metadata lists for all the selected runs and
    datasets
    """
    # -- update cache if requested
    if update_cache:
        updateMetadataCache(self)

    # -- get run selections
    # get selected datasets
    selected_datasets = [
        item.data(Qt.UserRole) for item in self.setList.selectedItems()
    ]
    # get corresponding paths
    dataset_list = {}
    for dataset in selected_datasets:
        if dataset is None:
            continue
        if dataset.is_file():
            # load json
            set_json = json.loads(dataset.read_text())
            # get list of paths
            json_paths = set_json.get("paths", [])
            # get "data root" tag, and replace it by the local data root
            if "root tag" in set_json:
                conf = self.settings.config
                root = Path(conf["data"]["root"])
                root = str(root.expanduser())
                tag = set_json["root tag"]
                pattern = "^%s" % tag
                json_paths = [re.sub(pattern, root, p) for p in json_paths]
            # convert to path objects
            json_paths = [Path(p) for p in json_paths]
            # store
            dataset_list[dataset.stem] = json_paths

    # add the current selection
    selected_runs = [item.data(Qt.UserRole) for item in self.runList.selectedItems()]
    if len(selected_runs) > 1:
        dataset_list["current selection"] = selected_runs

    # -- generate metadata lists from cache
    metadata = {}
    for set_name, path_list in dataset_list.items():
        metadata[set_name] = _generateMetadaListFromCache(self, path_list)

    return metadata


def displayMetaData(self):
    """
    loads related meta data and display it
    """
    # -- get selected data
    selection = self.runList.selectedItems()
    if not selection:
        return

    # -- get data path
    item = selection[0]
    path = item.data(Qt.UserRole)

    # -- get metadata
    metadata_dic = _loadFileMetaData(self, path)  # returns an ordered dic

    # -- display metadata
    # init
    text = ""
    for name, meta in metadata_dic.items():
        # get param list
        param_list = meta.data
        # exclude 'hidden' parameters
        param_list = [p for p in param_list if not p["hidden"]]
        if not param_list:
            # not displayed if empty
            continue
        # loop on parameters
        n_param = len(param_list)
        text += TITLE_STR % name
        for i, par in enumerate(param_list):
            # choose good prefix
            if i == n_param - 1:
                param_str = PREFIX_LAST
            else:
                param_str = PREFIX_CORE
            # prepare param string
            param_str += par["name"] + " : " + par["display"] % par["value"]
            if par["unit"]:
                param_str += " %s" % par["unit"]
            param_str += "\n"
            # append
            text += param_str

    self.metaDataText.setPlainText(text)


# %% SET MANAGEMENT


def _writeDataSet(self, setname, selected_paths, overwrite_ok=False, dataset_dir=None):
    """
    Low-level function to write data sets. Called by createNewDataSet()
    or addToDataSet()
    """
    # -- process selected paths
    # replace the data root by '{data_root}'
    conf = self.settings.config
    root = Path(conf["data"]["root"])
    root = root.expanduser()
    pattern = "^%s" % root  # only replace at the beginning of the path
    tag = "{data_root}"
    selected_paths = [re.sub(pattern, tag, p) for p in selected_paths]

    # -- save dataset
    # prepare json content
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    json_content = {
        "created": date_str,
        "program": self._name,
        "version": self._version,
        "root tag": tag,
        "local root": str(root),
        "paths": selected_paths,
    }

    # prepare .dataset dir (create if does not exist)
    if dataset_dir is None:
        root = self.current_folder
        dataset_dir = root / ".datasets"
        dataset_dir.mkdir(exist_ok=True)

    json_file = dataset_dir / ("%s.json" % setname)
    # check if file exists
    if json_file.is_file() and not overwrite_ok:
        # are you sure ?
        answer = QMessageBox.question(
            self,
            "This mission is too important...",
            f"Overwrite the existing dataset '{setname}' ?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if answer == QMessageBox.No:
            return
    # create dataset
    json_txt = json.dumps(json_content)
    json_file.write_text(json_txt)


def createNewDataSet(self):
    """
    Add a new dataset, consisting of the currently selected runs.
    The dataset is saved in the day folder, in a '.datasets' subfolder
    """
    # -- get selected data
    # get runs
    selected_runs = self.runList.selectedItems()
    if not selected_runs:
        # if empty >> do nothing
        return

    # get paths
    selected_paths = [str(s.data(Qt.UserRole)) for s in selected_runs]

    # ask name
    default_name = str(selected_runs[0].data(Qt.UserRole).parent.name)
    setname, ok = QInputDialog.getText(
        self, "create new data set", "Enter dataset name:", text=default_name
    )
    # write json file
    if ok:
        _writeDataSet(self, setname, selected_paths, overwrite_ok=False)

    # refresh
    refreshDataSetList(self)


def addToDataSet(self):
    """
    Add the currently selected runs to the selected DataSet.
    """
    # -- get selected runs
    selected_runs = self.runList.selectedItems()
    if not selected_runs:
        # if empty >> do nothing
        QMessageBox.warning(
            self, "No run selected", "Please select runs to add to the dataset."
        )
        return

    # -- get selected datasets
    # selected dataset list
    dataset_list = [
        s for s in self.setList.selectedItems() if s.data(Qt.UserRole) is not None
    ]
    # if list is empty, use all dataset list, and ask the user which one to select
    # (see below for the user choice)
    if len(dataset_list) == 0:
        items = [self.setList.item(i) for i in range(self.setList.count())]
        dataset_list = [s for s in items if s.data(Qt.UserRole) is not None]
        # if still empty >> do nothing
        if len(dataset_list) == 0:
            QMessageBox.warning(
                self,
                "No exising dataset",
                "You have to create a dataset first, Dave !",
            )
            return

    # if only one selected >> OK !
    if len(dataset_list) == 1:
        current_dataset = dataset_list[0]
    # if multiple selection >> ask the user
    else:
        # prepare a list of choices
        # to avoid names that would appear twice (for instance in the current folder
        # and in the favorite folder), we append a number to the set names in the list
        name_list = [s.data(Qt.UserRole).stem for s in dataset_list]
        choice = {
            f"{i + 1} - {name}": s
            for i, (name, s) in enumerate(zip(name_list, dataset_list))
        }
        item, ok = QInputDialog.getItem(
            self,
            "Add to dataset",
            "In which dataset shall I add those runs, Dave ?",
            list(choice.keys()),
            0,
            False,
        )
        if ok and item:
            current_dataset = choice[item]
        else:
            return

    # get selected dataset path
    path = current_dataset.data(Qt.UserRole)

    # -- ask for confirmation
    #  are you sure ?
    n_runs = len(selected_runs)
    answer = QMessageBox.question(
        self,
        "add to dataset",
        f"add {n_runs} runs to dataset '{path.stem}' ?",
        QMessageBox.Yes | QMessageBox.No,
    )
    if answer == QMessageBox.No:
        return

    # -- add to dataset

    # - paths to append
    selected_paths = [str(s.data(Qt.UserRole)) for s in selected_runs]

    # - current path list
    # prepare "root" substitution
    conf = self.settings.config
    root = Path(conf["data"]["root"])
    root = str(root.expanduser())
    with open(str(path)) as json_file:
        data = json.load(json_file)
        tag = data["root tag"]
        pattern = "^%s" % tag
        json_paths = [re.sub(pattern, root, p) for p in data["paths"]]
        total_paths = json_paths + selected_paths

    # -- save set
    _writeDataSet(
        self, path.stem, total_paths, overwrite_ok=True, dataset_dir=path.parents[0]
    )

    # refresh
    refreshDataSetList(self)

    # -- add to dataset

    # get paths
    selected_paths = [str(s.data(Qt.UserRole)) for s in selected_runs]

    # replace the data root by '{data_root}'
    conf = self.settings.config
    root = Path(conf["data"]["root"])
    root = root.expanduser()
    pattern = "^%s" % root  # only replace at the beginning of the path
    tag = "{data_root}"
    selected_paths = [re.sub(pattern, tag, p) for p in selected_paths]

    with open(str(path)) as json_file:
        data = json.load(json_file)
        total_paths = data["paths"] + selected_paths

    # -- save set
    # prepare json file
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    json_content = {
        "created": date_str,
        "program": self._name,
        "version": self._version,
        "root tag": tag,
        "local root": str(root),
        "paths": total_paths,
    }

    # prepare .dataset dir (create if does not exist)
    root = self.current_folder
    dataset_dir = root / ".datasets"
    dataset_dir.mkdir(exist_ok=True)

    # get name
    name = str(path.stem)

    # write json file
    json_file = path
    json_txt = json.dumps(json_content)
    json_file.write_text(json_txt)

    # refresh
    refreshDataSetList(self)


def renameDataSet(self):
    """
    Rename the currently selected dataset
    """
    # -- get dataset
    current_dataset = self.setList.currentItem()
    if current_dataset is None:
        dialog(self, "You have to select a dataset first, Dave")
        return
    path = current_dataset.data(Qt.UserRole)
    if path is None or not path.is_file():
        return

    # -- rename
    # ask for name
    current_name = str(path.stem)
    new_name, ok = QInputDialog.getText(
        self, "rename data set", "Enter new dataset name:", text=current_name
    )
    # OK, let's do it
    if ok:
        path.rename(path.with_name(f"{new_name}.json"))

    # -- refresh
    refreshDataSetList(self)


def deleteDataSet(self):
    """
    Delete the currently selected datasets
    """
    # -- get selected datasets
    selected_datasets = self.setList.selectedItems()

    # -- remove
    # are you sure ?
    answer = QMessageBox.question(
        self,
        "delete data set",
        "delete %i datasets ?" % len(selected_datasets),
        QMessageBox.Yes | QMessageBox.No,
    )
    # OK, let's do it
    if answer == QMessageBox.Yes:
        for item in selected_datasets:
            path = item.data(Qt.UserRole)
            if path is not None:
                path.unlink()
    # refresh
    refreshDataSetList(self)


def favDataSet(self):
    """
    Move currently dataset to home folder (as favorite)
    """
    # get selected datasets
    selected_datasets = self.setList.selectedItems()
    if not selected_datasets:
        return

    # target directory
    root = self._settings_folder
    fav_dir = root / "datasets"
    fav_dir.mkdir(parents=True, exist_ok=True)

    # copy
    for item in selected_datasets:
        path = item.data(Qt.UserRole)
        if path is not None and path.is_file():
            setname = path.name
            new_path = fav_dir / setname
            new_path.write_text(path.read_text())  # copy !

    # refresh
    refreshDataSetList(self)


def refreshDataSetList(self):
    """
    Refresh the data set list, with all datasets in the current folder, and the
    favorite ones stored in ~/.HAL/datasets
    """

    # -- get datasets
    # in current folder
    current_datasets = []
    root = self.current_folder
    dataset_dir = root / ".datasets"
    if dataset_dir.is_dir():
        for content in dataset_dir.iterdir():
            if content.suffix == ".json":
                current_datasets.append(content)
    # in home folder
    fav_datasets = []
    root = self._settings_folder
    dataset_dir = root / "datasets"
    if dataset_dir.is_dir():
        for content in dataset_dir.iterdir():
            if content.suffix == ".json":
                fav_datasets.append(content)

    # -- show in setList
    # save dataset selection
    selection = [item.data(Qt.UserRole) for item in self.setList.selectedItems()]
    item = self.setList.currentItem()
    current_set = item.data(Qt.UserRole) if item is not None else None

    # refresh set list
    self.setList.blockSignals(True)
    self.setList.clear()
    for name, datasets in zip(
        ["current folder", "favorite"], [current_datasets, fav_datasets]
    ):
        if datasets:
            # title
            item = QListWidgetItem()
            item.setText(name)
            item.setData(Qt.UserRole, None)
            item.setForeground(QColor(255, 0, 0))
            item.setIcon(self.style().standardIcon(QStyle.SP_DirIcon))
            self.setList.addItem(item)
            # sets
            n_files = len(datasets)
            for i, file in enumerate(datasets):
                # good prefix
                if i == n_files - 1:
                    prefix = "└─ "
                else:
                    prefix = "├─ "
                # add item
                item = QListWidgetItem()
                item.setText(prefix + file.stem)  # NB: use file.stem to remove ext
                item.setData(Qt.UserRole, file)
                self.setList.addItem(item)
                # restore selection ?
                if file in selection:
                    item.setSelected(True)
                if file == current_set:
                    self.setList.setCurrentItem(item)

    self.setList.blockSignals(False)


# %% 1D FIT DISPLAY


def display1DFitResults(self, fit_results={}):
    """
    loads related meta data and display it
    """
    if len(fit_results) == 0:
        return

    # -- display fit info
    # init
    fit = fit_results["__fit__"]
    text = f" ▶▷▶ {fit.name.upper()} FIT ◀◁◀ \n"
    help_str = wrap_text(fit.formula_help, 33)
    text += help_str + "\n"
    if fit.parameters_help:
        text += f" {fit.parameters_help} \n"
    text += "\n"
    # -- display fit parameters
    for name, value_list in fit_results.items():
        # exclude hidden
        if name.startswith("__"):
            continue
        # loop on parameters
        n_value = len(value_list)
        text += TITLE_STR % name
        for i, val in enumerate(value_list):
            # choose good prefix
            if i == n_value - 1:
                param_str = PREFIX_LAST
            else:
                param_str = PREFIX_CORE
            # prepare param string
            param_str += val["name"] + " : " + val["display"] % val["value"]
            if "error" in val:
                param_str += " ± " + val["display"] % val["error"]
            if val["unit"]:
                param_str += " %s" % val["unit"]
            param_str += "\n"
            # append
            text += param_str

        text += "\n"

    self.metaDataText.setPlainText(text)
