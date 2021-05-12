# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 16:28:03
Modified : 2021-05-12 16:45:47

Comments : Functions related to (meta)data exploration
"""

# %% IMPORTS

# -- global
import json
import logging
import time
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
    QAction,
    QActionGroup,
    QMenu,
    QToolButton,
)

# -- local
import HAL.gui.quickplot as quickplot

# -- logger
logger = logging.getLogger(__name__)

# %% GLOBAL
TITLE_STR = "[%s]\n"
PREFIX_CORE = "├─ "
PREFIX_LAST = "└─ "


# %% SETUP FUNCTIONS


def setupDataExplorer(self):
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


# %% META DATA MANAGEMENT


def _loadFileMetaData(self, path):
    """
    Subfunction, loads the metadata linked to one file
    """
    # -- get metadata
    # get selected metadata sources
    selected_metadata = [
        item.text() for item in self.metaDataList.selectedItems()
    ]

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
    dataset_list = {}
    for dataset in selected_datasets:
        if dataset is None:
            continue
        if dataset.is_file():
            set_json = json.loads(dataset.read_text())
            for path in set_json.get("paths", []):
                all_selected_files.add(Path(path))

    # -- remove from cache
    for cached_file in list(self.metadata_cache.keys()):
        if cached_file not in all_selected_files:
            self.metadata_cache.pop(cached_file)

    # -- update cache
    n_files = len(all_selected_files)
    for i_file, file_to_cache in enumerate(all_selected_files):
        if file_to_cache in self.metadata_cache:
            # ignore
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


def _generateMetadaListFromCache(self, path_list):
    """
    Subfunction, generates a list of metadata from cache
    """
    # -- initialize output dictionnary, populated with 'None'
    meta_dic = {}
    for meta_name, meta_param_list in self.available_metadata.items():
        meta_dic[meta_name] = {}
        for param_name in meta_param_list:
            meta_dic[meta_name][param_name] = [None for p in path_list]

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
        self.updateMetadataCache()

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
            set_json = json.loads(dataset.read_text())
            json_paths = [Path(p) for p in set_json.get("paths", [])]
            dataset_list[dataset.stem] = json_paths

    # add the current selection
    selected_runs = [
        item.data(Qt.UserRole) for item in self.runList.selectedItems()
    ]
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
        param_list = meta.data
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


def addNewSet(self):
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

    # -- save set
    # prepare json file
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    json_content = {
        "created": date_str,
        "program": self._name,
        "version": self._version,
        "paths": selected_paths,
    }

    # prepare .dataset dir (create if does not exist)
    root = self.current_folder
    dataset_dir = root / ".datasets"
    dataset_dir.mkdir(exist_ok=True)

    # ask name
    default_name = str(selected_runs[0].data(Qt.UserRole).parent.name)
    name, ok = QInputDialog.getText(
        self, "create new data set", "Enter dataset name:", text=default_name
    )
    # write json file
    if ok:
        json_file = root / ".datasets" / ("%s.json" % name)
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
        path.rename(path.with_stem(new_name))

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
                item.setText(
                    prefix + file.stem
                )  # NB: use file.stem to remove ext
                item.setData(Qt.UserRole, file)
                self.setList.addItem(item)


# %% TEST
if __name__ == "__main__":
    from HAL.classes.metadata import implemented_metadata

    root = Path().home()
    path = (
        root / "gus_data_dummy" / "cam_example" / "033_Raman" / "033_001.png"
    )

    print(path.is_file())
    path_list = [
        path,
    ]
    data_list = [("HeV-fit", "cx"), ("file", "size"), ("HeV-fit", "Nint")]

    class Dummy(object):
        def __init__(self):
            self.metadata_classes = implemented_metadata

    mdata = _loadSetMetaData(Dummy(), path_list, data_list)
    print(mdata)
