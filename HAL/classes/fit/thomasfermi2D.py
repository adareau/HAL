# -*- coding: utf-8 -*-
"""
Author   : Victor
Created  : 2021-05-25T14:18:21+02:00
Modified : 2021-05-25 16:51:24

Comments : implements a 2D Thomas Fermi fit
"""
# %% IMPORTS

# -- global
import numpy as np
from collections import namedtuple

# -- local
from HAL.classes.fit.abstract import Abstract2DBellShaped


# %% FUNCTIONS
def ThomasFermi2D(parameters):
    """
    Returns the Thomas-Fermi distributrion in 2D.
    The argument is a tuple such that:
    (x, y, sizeX, sizeY, centerX, centerY, offset, amplitude)
    """
    Parameters = namedtuple(
        "Parameters", "x y sizeX sizeY centerX centerY offset amplitude"
    )
    p = Parameters(*parameters)

    shiftX = (p.x - p.centerX)/p.sizeX
    shiftY = (p.y - p.centerY)/p.sizeY
    parabValue = 1 - np.square(shiftX) - np.square(shiftY)

    s = np.maximum(p.offset + p.amplitude * parabValue, p.offset)
    return s


# %% CLASS DEFINITION
class ThomasFermi2DFit(Abstract2DBellShaped):
    """a 2D Thomas Fermi fit. Inherits methods from the Abstract2DBellShaped
       (for instance the do_guess() one)"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # -- attributes specific to 2D Gauss fit
        self.name = "ThomasFermi2D"
        self.formula_help = "f(x) = p[0] + p[1] * (1 - (x - p[4])**2 / p[2]**2"
        self.formula_help += " - (x - p[5])**2 / p[3]**2)**(3/2)"
        self.parameters_help = (
            "p = [offset, amplitude, size_x, size_y, center_x, center_y]"
        )
        self._version = "1.0"

    def _fitfunc(self, x, *p):
        return ThomasFermi2D(x, *p)

    def do_guess(self):
        """guess fit parameters. use the guess_center_size_ampl_offset()
           method defined in the Abstract2DBellShaped class"""

        # guess amplitude / offset / center / size
        res = self.guess_center_size_ampl_offset()

        # adapt to the current fit function
        p0 = [
            res["offset"],
            res["amplitude"],
            res["sx"],
            res["sy"],
            res["cx"],
            res["cy"],
        ]

        # save guess
        self.guess = p0

    def compute_values(self):
        """compute some physical values from the fit optimal parameters"""

        # -- check that the data and coordinates were provided
        if len(self.z) * len(self.x) * len(self.popt) == 0:
            return

        # -- get data
        Z = self.z
        (X, Y) = self.x
        Zfit = self._fitfunc((X, Y), *self.popt)
        dx = np.abs(X[1, 0] - X[0, 0])
        dy = np.abs(Y[0, 1] - Y[0, 0])

        # -- get fit results
        offset, amplitude, sx, sy, cx, cy = self.popt
        offset_err, amplitude_err, sx_err, sy_err, cx_err, cy_err = self.perr

        # -- init values list
        values = []

        # -- counts
        conv_factor = self.count_conversion_factor
        # Nfit
        Nfit = np.sum(Zfit - offset) * conv_factor
        param = {
            "name": "Nfit",
            "value": Nfit,
            "display": "%.3g",
            "unit": self.converted_count_unit,
            "comment": "counts, from fit, restricted to ROI",
        }
        values.append(param)

        # Nint
        Nint = np.sum(Z) * conv_factor
        param = {
            "name": "Nint",
            "value": Nint,
            "display": "%.3g",
            "unit": self.converted_count_unit,
            "comment": "counts, from integrated raw data, restricted to ROI",
        }
        values.append(param)

        # Ncalc
        Ncal = 2 * np.pi / 5 * amplitude * sx * sy / dx / dy * conv_factor
        param = {
            "name": "Ncal",
            "value": Ncal,
            "display": "%.3g",
            "unit": self.converted_count_unit,
            "comment": "counts, calculated from fit results, not restricted to ROI",
        }
        values.append(param)

        # -- spatial values in pixels

        for name, key in zip(["center", "size"], ["c", "s"]):
            for ax in ["x", "y"]:
                # values
                v = eval("%s%s" % (key, ax))
                v_err = eval("%s%s_err" % (key, ax))

                # save value
                param = {
                    "name": "%s%s_px" % (key, ax),
                    "value": v,
                    "display": "%.3g",
                    "unit": "px",
                    "comment": "%s along %s, in pixels" % (name, ax),
                }
                values.append(param)

                # save values error
                param = {
                    "name": "%s%s_err_px" % (key, ax),
                    "value": v_err,
                    "display": "%.3g",
                    "unit": "px",
                    "comment": "%s fit error along %s, in pixels" % (name, ax),
                }
                values.append(param)

        # -- spatial values in physical units
        for name, key in zip(["center", "size"], ["c", "s"]):
            for ax in ["x", "y"]:
                # values
                conversion = self.__getattribute__("pixel_size_%s" % ax)
                unit = self.__getattribute__("pixel_size_%s_unit" % ax)
                v = eval("%s%s" % (key, ax)) * conversion
                v_err = eval("%s%s_err" % (key, ax)) * conversion

                # save value
                param = {
                    "name": "%s%s" % (key, ax),
                    "value": v,
                    "display": "%.3g",
                    "unit": unit,
                    "comment": "%s along %s, in %s" % (name, ax, unit),
                }
                values.append(param)

                # save values error
                param = {
                    "name": "%s%s_err" % (key, ax),
                    "value": v_err,
                    "display": "%.3g",
                    "unit": unit,
                    "comment": "%s fit error along %s, in %s"
                    % (name, ax, unit),
                }
                values.append(param)

        # -- other
        # center of mass
        fit_error = np.mean(np.sqrt((Z - Zfit) ** 2))
        param = {
            "name": "fit error",
            "value": fit_error,
            "display": "%.3g",
            "unit": "",
            "comment": "fit error = mean(sqrt((data - fit)**2)))",
        }
        values.append(param)

        # spatial statistics (c.o.m, std dev)
        # see Abstract2DFit Class
        values += self._get_spatial_stats(Z_offset=offset)

        # -- store
        self.values = values


# %% TESTS
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # -- generate noisy data
    x = np.linspace(-10, 10, 200)
    Y, X = np.meshgrid(x, x)
    p = [0.5, 5.0, 0.5, 2.0, 5, 1.0]
    Z = ThomasFermi2D((X, Y), *p)
    noise = (np.random.rand(*X.shape) - 0.5) * 2
    Z += noise

    # -- Fit
    g2Dfit = ThomasFermi2DFit(x=(X, Y), z=Z)
    g2Dfit.guess = [0.4, 6, 3.2, 1.8, 0, 0]
    g2Dfit.do_guess()
    print(">> guess")
    print(g2Dfit.guess)
    g2Dfit.do_fit()
    Zfit = g2Dfit.eval((X, Y))

    print(">> popt")
    print(g2Dfit.popt)

    g2Dfit.compute_values()
    print(g2Dfit.export_json_str())

    g2Dfit.plot_fit_result()
    if False:
        # -- Plot
        # setup
        fig, ax = plt.subplots(1, 3, figsize=(10, 4), constrained_layout=True)
        vmin = 0
        vmax = np.max(Z)

        # input data
        cax = ax[0]
        cax.pcolormesh(X, Y, Z, vmin=vmin, vmax=vmax, shading="auto")

        # fit
        cax = ax[1]
        cax.pcolormesh(X, Y, Zfit, vmin=vmin, vmax=vmax, shading="auto")

        # err
        cax = ax[2]
        cax.pcolormesh(
            X, Y, Z - Zfit, vmin=-0.5 * vmax, vmax=0.5 * vmax, shading="auto"
        )
        plt.show()
