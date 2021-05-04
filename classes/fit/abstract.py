# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-03 10:08:22
Modified : 2021-05-04 13:05:06

Comments : Abstract classes for data fitting
"""
# %% IMPORTS
import json
import jsbeautifier as jsb
import numpy as np
import scipy.optimize as opt
import matplotlib.pyplot as plt
from datetime import datetime


# %% USEFUL : JSON ARRAY ENCODER


class NumpyArrayEncoder(json.JSONEncoder):
    """convert ndarray into list to avoid the error :
    TypeError: Object of type ndarray is not JSON serializable
    """

    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


# %% CLASS DEFINITION


class AbstractFit(object):
    """Abstract fit object, to use as a model"""

    def __init__(self, **kwargs):

        # -- inputs
        self.x = kwargs.get("x", [])  # coordinates (x in 1D, (x,y) in 2D)
        self.z = kwargs.get("z", [])  # data
        self.guess = kwargs.get("guess", None)  # fit guess

        # -- fit results
        self.popt = []  # optimum parameters from fit routine
        self.pcov = []  # estimated covariance of popt
        self.perr = []  # estimated stdev : perr = np.sqrt(np.diag(pcov))
        self.values = []  # list physical values computed from fit parameters

        # -- other attributes
        self.name = "AbstractFit"
        self.formula_help = "f(x) = p[0] * x"
        self.parameters_help = "p = []"
        self._version = "0.0"

    # == ACTUAL FITTING ==

    def do_fit(self):
        """fits the data"""
        # WILL BE IMPLEMENTED IN SPECIFIC 1D / 2D ABSTRACT FIT CLASSES
        pass

    def do_guess(self):
        """initial guess of fit parameters from data"""
        # HAS TO BE IMPLEMENTED IN ALL REAL FIT MODELS !!
        pass

    def eval(self, x, params=None):
        """eval fit formula at coordinates 'x', with given set of 'params'

        Parameters
        ----------
        x : array or tuple of arrays
            list of coordinates, 1D or 2D depending on the fit model
        params : None, optional
            fit parameters. If None is provided, the current fitted parameters
            (popt) will be used
        """
        if params is None:
            params = self.popt
        if params != []:
            return self._fitfunc(x, *params)
        else:
            return []

    def _fitfunc(self, x, *p):
        pass

    # == ANALYZE OF FIT PARAMETERS ==

    def compute_values(self):
        """compute some physical values from the fit optimal parameters"""
        # HAS TO BE IMPLEMENTED IN ALL REAL FIT MODELS !!
        self.values = []

    # == EXPORT / SHOW RESULTS ==

    def export_dic(self):
        """exports fit info and results as a python dictionnary"""
        # -- prepare dictionnary
        out = {}
        out["fit name"] = self.name
        out["fit formula"] = self.formula_help
        out["fit parameters"] = self.parameters_help
        out["fit version"] = self._version
        out["date"] = str(datetime.now())
        out["popt"] = self.popt
        out["pcov"] = self.pcov
        out["perr"] = self.perr
        out["values"] = self.values
        return out

    def export_json_str(self):
        """exports fit info and results as a json string"""
        # get dictionnary
        out_dic = self.export_dic()
        json_str = json.dumps(
            out_dic, ensure_ascii=False, cls=NumpyArrayEncoder
        )
        json_str = jsb.beautify(json_str)
        return json_str


class Abstract2DFit(AbstractFit):
    """Abstract 2D fit object"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # -- 2D attributes
        self.pixel_size_x = 1
        self.pixel_size_x_unit = "px"
        self.pixel_size_y = 1
        self.pixel_size_y_unit = "px"
        # convert pixel counts into something (for instance, atoms !)
        # example : for fluo, we have :
        #  > count_conversion_factor = 1 / N_phot_per_atom
        #                                / quantum_efficiency
        #                                / solid_angle
        # with N_phot_per_atom = 0.5 * Gamma * fluo_exposure_duration
        self.count_conversion_factor = 1
        self.converted_count_unit = ""

    def do_fit(self, **fit_options):
        """fits the data. Any keyword option is passed to the fitting routine
        (scipy.optimize.curve_fit)"""

        # -- check that the data and coordinates were provided
        if self.z == [] or self.x == []:
            return

        # -- prepare data
        # get data
        z = self.z
        (x, y) = self.x  # this is a 2D fit !

        # should be arrays
        x = np.asarray(x)
        y = np.asarray(y)
        z = np.asarray(z)

        # ravel, so that everything is 1D
        x_rav = x.ravel()
        y_rav = y.ravel()
        z_rav = z.ravel()

        # -- fit
        # guess
        p0 = self.guess  # guess
        if not p0:
            p0 = None

        # do the fit
        popt, pcov = opt.curve_fit(
            self._fitfunc, (x_rav, y_rav), z_rav, p0=p0, **fit_options
        )

        # estimate standard dev
        perr = np.sqrt(np.diag(pcov))

        # -- store
        self.popt = popt
        self.pcov = pcov
        self.perr = perr

    def plot_fit_result(self, figsize=(10, 4)):
        """plots the fit result, for a rapid check"""
        # -- check that the data and coordinates were provided
        if len(self.z) * len(self.x) * len(self.popt) == 0:
            return

        # -- prepare data
        Z = self.z
        X, Y = self.x
        Zfit = self.eval((X, Y))

        # -- plot
        # setup
        fig, ax = plt.subplots(1, 3, figsize=(10, 4), constrained_layout=True)
        # min / max
        vmin = np.min(Z)
        vmax = np.max(Z)
        # data
        ax[0].pcolormesh(X, Y, Z, vmin=vmin, vmax=vmax, shading="auto")
        ax[0].set_title("data")
        # fit
        ax[1].pcolormesh(X, Y, Zfit, vmin=vmin, vmax=vmax, shading="auto")
        ax[1].set_title("fit")
        # err
        ax[2].pcolormesh(
            X, Y, Z - Zfit, vmin=-0.5 * vmax, vmax=0.5 * vmax, shading="auto"
        )
        ax[2].set_title("error")
        # show
        plt.show()


# %% TESTS
if __name__ == "__main__":
    fit2D = Abstract2DFit(x=[1, 2, 3])
    print(fit2D._version)
    print(fit2D.x)
