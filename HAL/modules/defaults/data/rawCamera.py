# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 15:38:07

Comments : Abstract classes for data handling
"""
# %% IMPORTS

# -- global
import cv2
from pathlib import Path


# -- local
from HAL.classes.data.abstract import AbstractCameraPictureData


# %% CLASS DEFINITION
class RawCamData(AbstractCameraPictureData):
    """docstring for Dummy"""

    def __init__(self, path=Path(".")):
        super().__init__()

        # - general
        self.name = "Camera"
        self.dimension = 2  # should be 1, 2 or 3
        self.path = path

        # - special for camera
        self.pixel_size = 1  # µm
        self.pixel_size_unit = "µm"
        self.magnification = 1
        self.default_display_scale = (0, 65535)

        # - data related
        x = self.pixel_size / self.magnification
        self.pixel_scale = (x, x)
        self.pixel_unit = (self.pixel_size_unit, self.pixel_size_unit)
        self.data = []

    def filter(self):
        """check whether path is compatible with extension / naming"""
        return self.path.suffix == ".png"

    def load(self):
        """loads data"""
        # load (as 16bit array)
        data = cv2.imread(str(self.path), cv2.IMREAD_UNCHANGED)
        # store
        self.data = data
