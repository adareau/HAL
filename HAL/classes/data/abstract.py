# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 15:38:07

Comments : Abstract classes for data handling
"""
# %% IMPORTS
from pathlib import Path


# %% CLASS DEFINITION
class AbstractData(object):
    """Abstract Data object, to use as a model"""

    def __init__(self):

        self.name = "Abstract Data"
        self.dimension = None  # should be 1, 2 or 3
        self.path = Path(".")
        self.pixel_scale = ()  # should be a tuple, with same size as dimension
        self.pixel_unit = ()  # should be a tuple, with same size as dimension
        self.data = []

    def filter(self):
        """should filter from name"""
        return True

    def getDisplayName(self):
        """returns the name to be displayed"""
        return self.path.stem

    def load(self):
        """should load data"""
        pass


class AbstractCameraPictureData(AbstractData):
    """Abstract Data object, for camera pictures"""

    def __init__(self):
        super().__init__()
        # - special for camera
        self.pixel_size = 1
        self.pixel_unit = ""
        self.magnification = 1
