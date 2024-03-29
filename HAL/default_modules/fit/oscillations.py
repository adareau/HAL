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


def Oscillation1D(x, *p):
    return p[0] + p[1] * np.sin(2 * np.pi * p[2] * x + p[3])


# %% CLASS DEFINITION
class Oscillation1DFit(Abstract1DFit):
    """a 1D Gauss fit"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # -- attributes specific to fit
        self.name = "oscillation"
        self.short_name = self.name
        self.category = "math"
        self.formula_help = "f(x) = p[0] "
        self.formula_help += "+ p[1] *sin(2*pi*p[2]*x+p[3])"
        self.parameters_help = "p = [offset, amplitude, \n frequency, phasee]"
        self._version = "1.0"

    def _fitfunc(self, x, *p):
        return Oscillation1D(x, *p)

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
        threshold = 0.05
        zmin = np.min(z)
        zmax = np.max(z)
        xmin = np.min(x)
        xmax = np.max(x)
        A = zmax - zmin

        offset_guess = (zmax + zmin) / 2
        amp_guess = A
        freq_guess = 3 / (xmax - xmin)
        # frequency guess
        # If data are equally spaced, we try FFT to compute the guess
        if len(x) > 3:
            # check if data are well separated. If not, keep the value above.
            deltaX = x[1] - x[0]
            vector = x[1:-1] - x[0:-2] - deltaX
            # We check if datas are equally spaced, we can guess using fft
            if np.max(np.abs(vector)) < 0.0001*deltaX:
                ft = np.fft.fft(z)
                N = len(z)
                fourier_trans = np.abs(ft[0 : int(N / 2)])
                argu = np.argmax(fourier_trans[1:])+1
                freq_guess = argu /(N * deltaX)
            else:
                print("Data are not equallys spaced : I did not use Fourier Transform to guess frequency.")
        phase_guess = 0
        # -- adapt to the current fit function
        p0 = [offset_guess, amp_guess, freq_guess, phase_guess]

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
        offset, amplitude, frequency, phase = self.popt
        (
            offset_err,
            amplitude_err,
            frequency_err,
            phase_err,
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

        # offset
        param = {
            "name": "offset",
            "value": offset,
            "error": offset_err,
            "display": "%.3g",
            "unit": self.z_unit,
            "comment": "offset",
        }
        values.append(param)

        # center

        if self.x_unit == "ms":
            frequency_unit = "kHz"
        elif self.x_unit == "us":
            frequency_unit = "MHz"
        elif self.x_unit == "s":
            frequency_unit = "Hz"
        else:
            frequency_unit = self.x_unit + "^-1"

        param = {
            "name": "frequency",
            "value": frequency,
            "error": frequency_err,
            "display": "%.3g",
            "unit": frequency_unit,
            "comment": "frequency",
        }
        values.append(param)
        # size
        param = {
            "name": "periode",
            "value": 1 / frequency,
            "error": frequency_err / (frequency**2),
            "display": "%.3g",
            "unit": self.x_unit,
            "comment": "periode",
        }
        values.append(param)
        # size
        param = {
            "name": "phase",
            "value": phase,
            "error": phase_err,
            "display": "%.3g",
            "unit": "rad",
            "comment": "phase at origin",
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
