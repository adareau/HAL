# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 15:38:07

Comments : Imports fit information, as saved by HAL
"""
# %% IMPORTS

# -- global

import json
from pathlib import Path
from ...classes.settings import Settings
# -- local
from HAL.classes.metadata.abstract import AbstractMetaData

# %% DECLARATIONS
# FIXME : can we link this to the actual user settings ?
FIT_FOLDER_NAME = ".HAL_fits"


# %% CLASS DEFINITION
class HALFitData(AbstractMetaData):
    """docstring for Dummy"""

    def __init__(self, path=Path(".")):
        super().__init__()

        # - general
        self.name = "fit"
        self.path = path
        self._settings_folder = Path().home() / ".HAL"
        global_config_path = self._settings_folder / "global.conf"
        self.settings = Settings(path=global_config_path)


    def analyze(self):
        # - init / reset data
        self.data = []
        data = []

        # - find HAL-generated fit file
        # (this is a json file)
        # generate file path
        fit_folder = self.path.parent / FIT_FOLDER_NAME
        fit_file = fit_folder / (self.path.stem + ".json")
        # check that file exists
        if not fit_file.is_file():
            return

        # - load json
        json_data = json.loads(fit_file.read_text())

        # - general info
        fit_info = json_data["__fit_info__"]
        data_info = json_data["__data_info__"]
        param = {
            "name": "fit name",
            "value": fit_info["fit name"],
            "display": "%s",
            "unit": "",
            "comment": "fit type",
        }
        data.append(param)

        param = {
            "name": "fit date",
            "value": fit_info["generated on"],
            "display": "%s",
            "unit": "",
            "comment": "fit date",
        }
        data.append(param)

        if "camera pixel size" in data_info:
            param = {
                "name": "camera pixel size",
                "value": data_info["camera pixel size"]["value"],
                "display": "%.2f",
                "unit": data_info["camera pixel size"]["unit"],
                "comment": "camera pixel size",
            }
            data.append(param)

        if "magnification" in data_info:
            param = {
                "name": "magnification",
                "value": data_info["magnification"],
                "display": "%.2f",
                "unit": "",
                "comment": "camera magnification",
            }
            data.append(param)

        # - get values
        fit_collection = json_data["collection"]
        for roi, fitres in fit_collection.items():
            do_not_display = self.settings.config["metadata"]["do not display"].split(", ")
            for value in fitres["result"]["values"]:
                param = {k: v for k, v in value.items()}
                if param["name"] in do_not_display:
                    pass
                else:
                    param["name"] = "%s::%s" % (roi, value["name"])
                    data.append(param)
        # - store
        self.data = data


# %% TEST
if __name__ == "__main__":
    root = Path().home()
    path = root / "gus_data_dummy" / "cam_example" / "001" / "001_001.png"

    data = HALFitData(path)
    data.analyze()
    print([p["name"] for p in data.data])
