# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 15:38:07
Modified : 2021-04-21 16:17:04

Comments : Abstract classes for data handling
"""
# %% IMPORTS

# -- global
import cv2
from pathlib import Path


# -- local
from HAL.classes.data.abstract import AbstractData


# %% CLASS DEFINITION
class XenicsData(AbstractData):
    """docstring for Dummy"""

    def __init__(self, path=Path(".")):
        super().__init__()

        # - general
        self.name = "Xenics"
        self.dimension = 2  # should be 1, 2 or 3
        self.path = path

        # - special for camera
        self.pixel_size = 6.45  # µm
        self.magnification = 0.27

        # - data related
        x = self.pixel_size / self.magnification
        self.pixel_scale = (x, x)
        self.pixel_unit = ("µm", "µm")
        self.data = []

    def filter(self):
        """check whether path is compatible with extension / naming"""
        return self.path.suffix == ".png"

    def load(self):
        """loads data"""
        self.data = cv2.imread(str(self.path), cv2.IMREAD_UNCHANGED)


# %% TEST
if __name__ == "__main__":
    import numpy as np
    root = Path().home()
    path = root / "gus_data_dummy" / "cam_example" / "001" / "001_001.png"

    data = XenicsData(path)
    if data.filter():
        data.load()
    print(np.max(data.data))
