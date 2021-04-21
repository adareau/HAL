# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 15:38:07
Modified : 2021-04-21 15:54:30

Comments : Abstract classes for data handling
"""
# %% IMPORTS
from pathlib import Path


# %% CLASS DEFINITION
class AbstractData(object):
    """Abstract Data object, to use as a model"""

    def __init__(self):

        self.name = 'Abstract Data'
        self.dimension = None  # should be 1, 2 or 3
        self.path = Path(".")
        self.pixel_scale = ()  # should be a tuple, with same size as dimension
        self.pixel_unit = ()  # should be a tuple, with same size as dimension
        self.data = []

    def filter(self):
        """should filter from name"""
        return True

    def load(self):
        """should load data"""
        pass
