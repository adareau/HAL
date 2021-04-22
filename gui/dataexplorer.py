# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 16:28:03
Modified : 2021-04-22 11:43:47

Comments : Functions related to (meta)data exploration
"""

# %% IMPORTS
import json
from datetime import datetime
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QInputDialog,
    QAbstractItemView,
    QStyle,
    QListWidgetItem,
    QMessageBox,
)


# %% GLOBAL
TITLE_STR = "[%s]\n"
PREFIX_CORE = "├─ "
PREFIX_LAST = "└─ "


# %% SETUP FUNCTIONS


def setupDataExplorer(self):
    # -- meta data text display
    self.metaDataText.setReadOnly(True)
    self.metaDataText.setLineWrapMode(self.metaDataText.NoWrap)

    # -- set list
    self.setList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    self.setList.setSelectionMode(QAbstractItemView.ExtendedSelection)
    self.setList.setIconSize(QSize(15, 15))


# %% DISPLAY FUNCTIONS


def displayMetaData(self):
    """
    loads related meta data and display it
    """
    # FIXME : preliminary, should call dataViz classes for displaying !
    # -- get selected data
    selection = self.runList.selectedItems()
    if not selection:
        return

    # -- get data path
    item = selection[0]
    path = item.data(Qt.UserRole)

    # -- get metadata
    # we store names in a sorted way
    metadata_names = [meta.name for meta in self.metadata_classes]
    # values are then sorted in a dict
    metadata = {}
    for meta in self.metadata_classes:
        meta.path = path
        meta.analyze()
        metadata[meta.name] = meta.data

    # -- display
    # generate text string
    text = ""
    for name in metadata_names:
        param_list = metadata[name]
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
            param_str += par["name"] + "\t= " + par["display"] % par["value"]
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
