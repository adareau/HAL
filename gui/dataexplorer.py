# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 16:28:03
Modified : 2021-04-22 10:48:44

Comments : Functions related to (meta)data exploration
"""

# %% IMPORTS
import json
from datetime import datetime
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QInputDialog


# %% GLOBAL
TITLE_STR = "[%s]\n"
PREFIX_CORE = "├─ "
PREFIX_LAST = "└─ "


# %% SETUP FUNCTIONS


def setupMetaData(self):
    # -- meta data text display
    self.metaDataText.setReadOnly(True)
    self.metaDataText.setLineWrapMode(self.metaDataText.NoWrap)


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
        self, "create new data", "Enter dataset name:", text=default_name
    )
    # write json file
    if ok:
        json_file = root / ".datasets" / ("%s.json" % name)
        json_txt = json.dumps(json_content)
        json_file.write_text(json_txt)
