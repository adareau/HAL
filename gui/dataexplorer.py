# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 16:28:03
Modified : 2021-04-23 15:49:33

Comments : Functions related to (meta)data exploration
"""

# %% IMPORTS
import json
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

    # -- meta data list
    # setup selection and scroll mode
    self.metaDataList.setSelectionMode(QAbstractItemView.MultiSelection)
    self.metaDataList.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    # add all metadata classes names
    for metadata in self.metadata_classes:
        item = QListWidgetItem()
        item.setText(metadata.name)
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


def _loadSetMetaData(self, path_list, data_list=None):
    """
    Subfunction, used for instance by getMetaData. Loads the selected metaData
    from the list of paths (i.e., for one dataset)
    """
    # -- prepare metadata classes
    if data_list is None:
        # then load all
        metadata_classes = self.metadata_classes
    else:
        # get requested names
        requested_names = [d[0] for d in data_list]
        metadata_classes = [
            m for m in self.metadata_classes if m.name in requested_names
        ]

    # -- prepare lists
    metadata = {}
    for d in data_list:  # FIXME handle case where data_list is None : take all
        if d[0] not in metadata:
            metadata[d[0]] = {}
        metadata[d[0]][d[1]] = [None for p in path_list]

    # -- collect
    # loop on all files
    for i, path in enumerate(path_list):
        path = Path(path)
        # loop on metadata classes
        for meta in metadata_classes:
            meta.path = path
            meta.analyze()
            # check all gathered parameters
            for param in meta.data:
                pname = param["name"]
                if pname in metadata[meta.name]:
                    # if parameter name is requested : store it
                    pvalue = param["value"]
                    metadata[meta.name][pname][i] = pvalue
                    # store info
                    if "%s_info" % pname not in metadata[meta.name]:
                        metadata[meta.name]["%s_info" % pname] = param

    return metadata


def getMetaData(self, data_list=None):
    """
    For each selected set (and selected run), gather
    the metadata listed in data_list (name, param_name)

    LOW LEVEL FUNCTION, will be called by plotting / stats functions !
    """
    # -- prepare datasets lists
    # get selected datasets
    selected_datasets = [
        item.data(Qt.UserRole) for item in self.setList.selectedItems()
    ]
    # get corresponding paths
    dataset_list = {}
    for set in selected_datasets:
        if set.is_file():
            set_json = json.loads(set.read_text())
            if "paths" in set_json:
                dataset_list[set.stem] = set_json["paths"]

    # add the current selection
    selected_runs = [
        item.data(Qt.UserRole) for item in self.runList.selectedItems()
    ]
    if len(selected_runs) > 1:
        dataset_list["current selection"] = selected_runs

    # -- load metadata
    metadata = {}
    for setname, paths in dataset_list.items():
        metadata[setname] = _loadSetMetaData(self, paths, data_list)

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
    # get selected metadata
    selected_metadata = [
        item.text() for item in self.metaDataList.selectedItems()
    ]
    # we store names in a sorted way
    metadata_names = [
        meta.name
        for meta in self.metadata_classes
        if meta.name in selected_metadata
    ]
    # values are then sorted in a dict
    metadata = {}
    for meta in self.metadata_classes:
        meta.path = path
        meta.analyze()
        metadata[meta.name] = meta.data

    # -- store
    self.metadata = metadata

    # -- display and store available metadata
    # init
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
            param_str += par["name"] + " : " + par["display"] % par["value"]
            if par["unit"]:
                param_str += " %s" % par["unit"]
            param_str += "\n"
            # append
            text += param_str

    self.metaDataText.setPlainText(text)

    # -- refresh dataexplorer metadata list
    refreshMetaDataList(self)


def refreshMetaDataList(self):
    """
    Updates all the GUI elements that allows the selection of metadata
    """
    # -- get data
    # get selected metadata
    selected_metadata = [
        item.text() for item in self.metaDataList.selectedItems()
    ]
    # we store names in a sorted way
    metadata_names = [
        meta.name
        for meta in self.metadata_classes
        if meta.name in selected_metadata
    ]
    metadata = self.metadata

    # -- combo box elements
    combo_boxes = [self.quickPlotXComboBox, self.quickPlotYComboBox]
    for box in combo_boxes:
        # get current selection
        current_selection = box.currentText()
        box.clear()
        for name in metadata_names:
            param_list = metadata[name]
            if not param_list:
                continue
            for par in param_list:
                # TODO : filter numeric ?? ??
                display_name = "%s > %s" % (name, par["name"])
                box.addItem(display_name, (name, par["name"]))
        # restore
        if current_selection:
            index = box.findText(current_selection)
            if index != -1:
                box.setCurrentIndex(index)


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
