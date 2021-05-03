# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-03 10:08:22
Modified : 2021-05-03 14:17:33

Comments : Abstract classes for data fitting
"""
# %% IMPORTS
from pathlib import Path
import numpy as np
import scipy.optimize as opt


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

    # == SAVE / LOAD ==

    def save_results(self, out_path=None):
        """saves the fit results"""
        # TODO: implement
        pass

    def load_results(self, out_path=None):
        """loads fit results"""
        # TODO: implement
        pass


class Abstract2DFit(AbstractFit):
    """Abstract 2D fit object"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # -- 2D attributes
        self.pixel_size_x = 1
        self.pixel_size_x_unit = "µm"
        self.pixel_size_y = 1
        self.pixel_size_y_unit = "µm"

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


# %% TESTS
if __name__ == "__main__":
    fit2D = Abstract2DFit(x=[1, 2, 3])
    print(fit2D._version)
    print(fit2D.x)
