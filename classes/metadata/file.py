# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 15:38:07
Modified : 2021-04-21 18:04:55

Comments : Abstract classes for data handling
"""
# %% IMPORTS

# -- global
from pathlib import Path


# -- local
from HAL.classes.metadata.abstract import AbstractMetaData


# %% CLASS DEFINITION
class FileData(AbstractMetaData):
    """docstring for Dummy"""

    def __init__(self, path=Path(".")):
        super().__init__()

        # - general
        self.name = "File Data"
        self.path = path

    def analyze(self):
        data = {}
        #  name
        data['name'] = self.path.name

        #  store
        self.data = data

# %% TEST
if __name__ == "__main__":
    root = Path().home()
    path = root / "gus_data_dummy" / "cam_example" / "001" / "001_001.png"

    data = FileData(path)
    data.analyze()
    print(data.data)
