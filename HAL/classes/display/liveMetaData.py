# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-17 12:52:39

Comments : implement the liveMetaData display, basically an empty class
           that replaces the "normal" display classes when switching to
           the "advanced" meta data plot mode
"""

# %% IMPORTS

# -- local
from .abstract import AbstractDisplay


# %% CLASS DEFINITION


class LiveMetaData(AbstractDisplay):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # -- other attributes
        self.current_data_object = None
        self.name = "Live MetaData"
        self.type = "meta"  # 3D, 2D, meta..

    def setup(self):
        """sets up display"""
        # -- reset
        self.screen.clear()
