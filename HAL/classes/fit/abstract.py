# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-03 10:08:22

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


# %% FUNCTIONS


def Gauss1D(x, *p):
    return p[0] + p[1] * np.exp(-((x - p[3]) ** 2) / 2 / p[2] ** 2)


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
        json_str = json.dumps(out_dic, ensure_ascii=False, cls=NumpyArrayEncoder)
        json_str = jsb.beautify(json_str)
        return json_str


# %% 2D ABSTRACT CLASSES


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

    def _get_spatial_stats(self, Z_offset=0):
        """returns the spatial center of mass and standard deviation.
        intended to be used in compute_values(), to add stats values"""

        # -- get data
        if len(self.z) * len(self.x) == 0:
            return

        Z = self.z - Z_offset
        X, Y = self.x

        # -- compute stats
        values = []
        # center of mass (pixels)
        com = {}
        for ax, U in zip(["x", "y"], [X, Y]):
            com[ax] = np.average(U, weights=Z)
            param = {
                "name": "com_%s_px" % ax,
                "value": com[ax],
                "display": "%.3g",
                "unit": "px",
                "comment": "center of mass along %s, in pixels" % ax,
            }
            values.append(param)

        # standard dev (pixels)
        std = {}
        for ax, U in zip(["x", "y"], [X, Y]):
            std[ax] = np.sqrt(np.average((U - com[ax]) ** 2, weights=Z))
            param = {
                "name": "std_%s_px" % ax,
                "value": std[ax],
                "display": "%.3g",
                "unit": "px",
                "comment": "standard deviation along %s, in pixels" % ax,
            }
            values.append(param)

        # now with real physical units
        display = {
            "com": "center of mass along %s, in %s",
            "std": "standard deviation along %s, in %s",
        }
        for name, val in zip(["com", "std"], [com, std]):
            for ax in ["x", "y"]:
                conversion = self.__getattribute__("pixel_size_%s" % ax)
                unit = self.__getattribute__("pixel_size_%s_unit" % ax)
                param = {
                    "name": "%s_%s" % (name, ax),
                    "value": val[ax] * conversion,
                    "display": "%.3g",
                    "unit": unit,
                    "comment": display[name] % (ax, unit),
                }
                values.append(param)

        # min / max
        param = {
            "name": "max",
            "value": np.max(Z),
            "display": "%.3g",
            "unit": "",
            "comment": "maximum count value in ROI",
        }
        values.append(param)

        param = {
            "name": "min",
            "value": np.min(Z),
            "display": "%.3g",
            "unit": "",
            "comment": "maximum count value in ROI",
        }
        values.append(param)
        return values


class Abstract2DBellShaped(Abstract2DFit):
    """abstract class for 'bell shaped' functions. the idea is to define once
    and for all some methods (such as do_guess()) that will be shared by
    all fit models based such functions (that is, basically, all of them)"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Abstract2DBellShaped"

    def guess_center_size_ampl_offset(self):
        """guess some parameters from preliminary data analysis. this is done
        by fitting the integrated data along the two axes using a Gaussian
        shape"""

        # -- check that the data and coordinates were provided
        if len(self.z) == 0 or len(self.x) == 0:
            return

        # -- get data
        Z = self.z
        (X, Y) = self.x  # this is a 2D fit !

        # should be arrays
        X = np.asarray(X)
        Y = np.asarray(Y)
        Z = np.asarray(Z)

        # 1D x,y arrays
        x = X[:, 0]
        y = Y[0, :]

        # -- use 1D fits on integrated data to estimate 2D fit parameters
        results = {}
        for axis, u, label in zip([1, 0], [x, y], ["x", "y"]):
            # -- integrate
            z = np.mean(Z, axis=axis)

            # -- guess for 1D fit
            # min, max, amp
            threshold = 0.05
            zmin = np.min(z)
            zmax = np.max(z)
            A = zmax - zmin

            # offset, amplitude
            offset_guess = np.mean(z[z < zmin + threshold * A])
            amp_guess = zmax - offset_guess

            # filter to remove noise
            i_filter = (z - offset_guess) > threshold * amp_guess
            weights = z[i_filter] - offset_guess
            uf = u[i_filter]

            # center = center of mass
            c_guess = np.average(uf, weights=weights)

            # size = standard deviation
            s_guess = np.sqrt(np.average((uf - c_guess) ** 2, weights=weights))

            # -- 1D fit
            p0 = [offset_guess, amp_guess, s_guess, c_guess]
            try:
                popt, _ = opt.curve_fit(Gauss1D, u, z, p0=p0)
            except Exception as e:
                print(e)
                popt = p0

            results[label] = popt

        # -- get 2D guess
        cx = results["x"][3]
        cy = results["y"][3]
        sx = np.abs(results["x"][2])
        sy = np.abs(results["y"][2])
        offset = 0.5 * (results["x"][0] + results["y"][0])
        # find max
        xr = X.ravel()
        yr = Y.ravel()
        zr = Z.ravel()
        imax = np.argmin((cx - xr) ** 2 + (cy - yr) ** 2)
        amplitude = zr[imax]
        # return
        res = {
            "offset": offset,
            "amplitude": amplitude,
            "sx": sx,
            "sy": sy,
            "cx": cx,
            "cy": cy,
        }
        return res


class Abstract1DFit(AbstractFit):
    """Abstract 1D fit object"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Abstract1DFit"
        self.short_name = "AbsFit"
        self.category = None
        self.x_unit = ""
        self.z_unit = ""

    def do_fit(self, **fit_options):
        """fits the data. Any keyword option is passed to the fitting routine
        (scipy.optimize.curve_fit)"""

        # -- check that the data and coordinates were provided
        if self.z == [] or self.x == []:
            return

        # -- prepare data
        # get data
        z = self.z
        x = self.x  # this is a 2D fit !

        # should be arrays
        x = np.asarray(x)
        z = np.asarray(z)

        # -- fit
        # guess
        p0 = self.guess  # guess
        if not p0:
            p0 = None

        # do the fit
        popt, pcov = opt.curve_fit(self._fitfunc, x, z, p0=p0, **fit_options)

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
