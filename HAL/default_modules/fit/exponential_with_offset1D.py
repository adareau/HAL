# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-03 10:49:51

Comments : implements a 1D Gauss fit
"""
# %% IMPORTS

# -- global
import numpy as np

# -- local
from HAL.classes.fit.abstract import Abstract1DFit


# %% FUNCTIONS


def Exponentialoffset1D(x, *p):
    return p[0] * np.exp(-(x - p[1]) / p[2]) + p[3]


# %% CLASS DEFINITION
class ExponentialOffset1DFit(Abstract1DFit):
    """a 1D Gauss fit"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # -- attributes specific to fit
        self.name = "exponential with offset"
        self.short_name = self.name
        self.category = "math"
        self.formula_help = "f(x) = p[0] * exp( - (x-p[1]) / p[2]) + p[3]"
        self.parameters_help = "p = [amplitude, center, damping rate, offset]"
        self._version = "1.0"

    def _fitfunc(self, x, *p):
        return Exponentialoffset1D(x, *p)

    def do_guess(self):
        """guess fit parameters"""

        # -- check that the data and coordinates were provided
        if len(self.z) == 0 or len(self.x) == 0:
            return

        # -- get data
        z = self.z
        x = self.x

        # should be arrays
        x = np.asarray(x)
        z = np.asarray(z)

        # -- guess amplitude / offset / center / size

        # min, max, amp
        zmin = np.min(z)
        zmax = np.max(z)
        xmin = np.min(x)
        xmax = np.max(x)
        A = zmax - zmin

        amp_guess = A
        center_guess = xmin
        damping_rate_guess = (xmax - xmin) / 2
        # -- adapt to the current fit function
        p0 = [amp_guess, center_guess, damping_rate_guess, 0]

        # save guess
        self.guess = p0

    def compute_values(self):
        """compute some physical values from the fit optimal parameters"""

        # -- check that the data and coordinates were provided
        if len(self.z) * len(self.x) * len(self.popt) == 0:
            return

        # -- get data
        z = self.z
        x = self.x
        zfit = self._fitfunc(x, *self.popt)

        # -- get fit results
        amplitude, center, damping_rate, offset = self.popt
        (
            amplitude_err,
            center_err,
            damping_rate_err,
            offset_err,
        ) = self.perr

        # -- init values list
        values = []

        # -- compute values
        # amplitude
        param = {
            "name": "amplitude",
            "value": amplitude,
            "error": amplitude_err,
            "display": "%.3g",
            "unit": self.z_unit,
            "comment": "amplitude",
        }
        values.append(param)

        param = {
            "name": "center",
            "value": center,
            "error": center_err,
            "display": "%.3g",
            "unit": self.x_unit,
            "comment": "center",
        }
        values.append(param)

        param = {
            "name": "damping rate",
            "value": damping_rate,
            "error": damping_rate_err,
            "display": "%.3g",
            "unit": self.x_unit,
            "comment": "damping rate",
        }
        values.append(param)
        param = {
            "name": "offset",
            "value": offset,
            "error": offset_err,
            "display": "%.3g",
            "unit": self.y_unit,
            "comment": "offset",
        }
        values.append(param)
        # -- spatial values in pixels
        # -- other
        # fit error
        fit_error = np.mean(np.sqrt((z - zfit) ** 2))
        param = {
            "name": "fit error",
            "value": fit_error,
            "display": "%.3g",
            "unit": "",
            "comment": "fit error = mean(sqrt((data - fit)**2)))",
        }
        values.append(param)

        # -- store
        self.values = values
