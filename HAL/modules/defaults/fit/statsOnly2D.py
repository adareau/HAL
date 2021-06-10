# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-03 10:49:51

Comments : implements a "null" fit, that only returns spatial stats
"""
# %% IMPORTS

# -- global
import numpy as np

# -- local
from HAL.classes.fit.abstract import Abstract2DBellShaped


# %% CLASS DEFINITION
class StatsOnly2D(Abstract2DBellShaped):
    """a void 2D fit, only returning spatial stats"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # -- attributes specific to 2D Gauss fit
        self.name = "StatsOnly2D"
        self.formula_help = "no formula, only stats"
        self.parameters_help = ""
        self._version = "1.0"

    def _fitfunc(self, x, *p):
        X, Y = x
        return np.zeros_like(X)

    def do_guess(self):
        return

    def do_fit(self):
        return

    def compute_values(self):
        """compute some physical values from the fit optimal parameters"""
        # spatial statistics (c.o.m, std dev)
        # see Abstract2DFit Class
        values = self._get_spatial_stats(Z_offset=0)

        # -- store
        self.values = values
