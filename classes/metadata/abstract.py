# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 15:38:07
Modified : 2021-04-21 17:58:25

Comments : Abstract classes for data handling
"""
# %% IMPORTS
from pathlib import Path


# %% CLASS DEFINITION
class AbstractMetaData(object):
    """Abstract Data object, to use as a model"""

    def __init__(self):

        self.name = 'Abstract Meta Data'
        self.data = {}
        self.path = Path(".")

    def analyze(self):
        """gather metadata"""
        pass
