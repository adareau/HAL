# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-06-30 11:58:56

Comments : (low-level) functions handling export of data / figures for HAL
"""

# %% IMPORTS

# -- global
import logging
import h5py
import numpy as np
from pathlib import Path
from datetime import datetime
from PyQt5.QtWidgets import QFileDialog, QMessageBox

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


def _exportDataDictAsHDF5(self, dic, file_out):
    with h5py.File(str(file_out), "w") as f:
        # set global attributes
        f.attrs["software name"] = self._name
        f.attrs["software version"] = self._version
        f.attrs["software url"] = self._url
        f.attrs["created on"] = f"{datetime.now():%Y-%m-%d %H:%M:%S}"
        # store data for each dataset
        for dataset, meta_dic in dic.items():
            group = f.create_group(dataset)
            for name, value in meta_dic.items():
                dset = group.create_dataset(name, data=value["val"])
                for k, v in value["info"].items():
                    if k in ["unit", "comment", "name"]:
                        dset.attrs[k] = v


# == HIGH LEVEL


def exportDataDictAs(self, dic):
    """Exports a data dictionnary in various formats"""
    # -- prepare available formats
    export_list = {}
    export_list["csv file (*.csv)"] = (_exportDataDictAsCSV, ".csv")
    export_list["hdf5 file (*.hdf5)"] = (_exportDataDictAsHDF5, ".hdf5")
    # -- select output file
    folder = self.current_export_folder
    folder = str(folder) if folder is not None else folder
    dlg = QFileDialog(self, "Select output file", folder)
    dlg.setNameFilters(list(export_list.keys()))
    dlg.setFileMode(QFileDialog.AnyFile)
    dlg.setAcceptMode(QFileDialog.AcceptSave)
    if not dlg.exec():
        logger.debug("Why do you bother me then ?")
        return
    # -- save
    # get file name
    filename = dlg.selectedFiles()[0]
    filepath = Path(filename)
    # check if the file exist, so that we don't ask overwrite confirmation twice
    license_to_kill = filepath.is_file()
    # check selected format
    fmt = dlg.selectedNameFilter()
    if fmt not in export_list:
        logger.warning(f"Requested format '{fmt}'' is not implemented")
        return
    # get extension / append default if missing
    export_func, default_suffix = export_list[fmt]
    if not filepath.suffix:
        filepath = filepath.with_suffix(default_suffix)
    # store current folder
    self.current_export_folder = filepath.parent
    # if file exist, ask for confirmation
    # NB : already handled by QFileDialog, but since we might hav
    # changed the suffix we have to check a second time
    if filepath.is_file() and not license_to_kill:
        msg = f"{filepath} exists : overwrite ?"
        title = "This mission is too important..."
        answer = QMessageBox.question(
            self, title, msg, QMessageBox.Yes | QMessageBox.No
        )
        if answer == QMessageBox.No:
            return
    # export
    export_func(self, dic, str(filepath))
    logger.debug(f"Saved as {filepath}")
