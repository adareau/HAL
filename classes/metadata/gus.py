# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 15:38:07
Modified : 2021-04-22 13:53:45

Comments : Abstract classes for data handling
"""
# %% IMPORTS

# -- global
import numpy as np
from pathlib import Path
from scipy.io import loadmat

# -- local
from HAL.classes.metadata.abstract import AbstractMetaData


# %% TOOL
def is_integer_num(n):
    if isinstance(n, int):
        return True
    if isinstance(n, float):
        return n.is_integer()
    return False


# %% CLASS DEFINITION
class GusData(AbstractMetaData):
    """docstring for Dummy"""

    def __init__(self, path=Path(".")):
        super().__init__()

        # - general
        self.name = "gus"
        self.path = path

    def analyze(self):
        # - init data
        data = []

        # - find script name
        for content in self.path.parent.iterdir():
            if content.suffix == ".m":
                if not content.name.startswith(("x_", "z_")):
                    param = {
                        "name": "script",
                        "value": content.name,
                        "display": "%s",
                        "unit": "",
                        "comment": "",
                    }
                    data.append(param)

        # - gus generated .mat file
        # generate file path
        mat_file = self.path.with_suffix(".mat")
        # load and get params
        if mat_file.is_file():
            # load
            gus_data = loadmat(str(mat_file), squeeze_me=True)
            variables = gus_data["variables"]
            # loop on variables
            name_list = [n for n in variables.dtype.names]
            name_list.sort()
            for name in name_list:
                x = variables[name][()]
                if is_integer_num(x):
                    disp_fmt = "%i"
                else:
                    disp_fmt = "%.3g"
                param = {
                    "name": name,
                    "value": variables[name][()],
                    "display": disp_fmt,
                    "unit": "",
                    "comment": "",
                }
                data.append(param)

        # - store
        self.data = data


# %% TEST
if __name__ == "__main__":
    root = Path().home()
    path = root / "gus_data_dummy" / "cam_example" / "001" / "001_001.png"

    data = GusData(path)
    data.analyze()
    print(data.data)
