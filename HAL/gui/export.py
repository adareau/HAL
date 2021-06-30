# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-06-30 11:58:56

Comments : (low-level) functions handling export of data / figures for HAL
"""

# %% IMPORTS

# -- global
import logging
import numpy as np
from datetime import datetime
from PyQt5.QtWidgets import QFileDialog

# -- local


# -- logger
logger = logging.getLogger(__name__)


# %% DATA EXPORT FUNCTION

# == LOW LEVEL
def _exportDataDictAsCSV(self, dic, file_out):
    # -- gather all data from dic
    # get variable names
    variables = set()
    for dataset, meta_dic in dic.items():
        variables.update(meta_dic.keys())
    # gather all values
    dic_out = {"dataset": []}
    dic_out.update({name: [] for name in variables})
    for dataset, meta_dic in dic.items():
        if not meta_dic:
            continue
        n_runs = len(next(iter(meta_dic.values()))["val"])
        dataset_name = dataset.replace(" ", "_")
        dic_out["dataset"] += [dataset_name for i in range(n_runs)]
        for name, value in meta_dic.items():
            dic_out[name] += list(value["val"])
    # -- prepare output array
    set_name_length = np.max([len(name) for name in dic.keys()])
    dtype = [("dataset", f"U{set_name_length}")] + [(name, float) for name in variables]
    fmt = ["%s"] + ["%.8e" for name in variables]
    array_out = np.zeros(len(dic_out["dataset"]), dtype=dtype)
    for key, value in dic_out.items():
        array_out[key] = value
    # -- prepare header
    sep = "-" * 48 + "\n"
    header = f"Generated by {self._name} v{self._version}"
    header += f" on {datetime.now():%Y-%m-%d %H:%M:%S} \n"
    header += sep
    header += "data info : \n"
    header += "----------- \n"
    for name, value in meta_dic.items():
        info = value["info"]
        info_str = ""
        for field in ["name", "unit", "comment"]:
            if field in info and info[field]:
                info_str += f"     - {field} : {info[field]} \n"
        if info_str:
            header += f"  + {name} \n" + info_str
    header += sep
    header += "data order : " + ", ".join([d[0] for d in dtype]) + "\n"
    header += sep[:-1]
    # -- save
    np.savetxt(file_out, array_out, header=header, comments="# ", fmt=" ".join(fmt))


# == HIGH LEVEL
def exportDataDictAs(self, dic):
    """Exports a data dictionnary in various formats"""
    # -- select output file
    if False:
        dlg = QFileDialog(self, "Select output file", None)
        dlg.setNameFilters(["Text files (*.txt)", "Images (*.png *.jpg)"])
        dlg.selectNameFilter("Images (*.png *.jpg)")
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        if dlg.exec():
            filename = dlg.selectedFiles()
            print(filename)
    file_out = "test.csv"
    _exportDataDictAsCSV(self, dic, file_out)
