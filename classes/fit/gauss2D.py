# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-03 10:49:51
Modified : 2021-05-03 15:25:24

Comments : implements a 2D Gauss fit
"""
# %% IMPORTS

# -- global
import numpy as np
import scipy.optimize as opt

# -- local
from HAL.classes.fit.abstract import Abstract2DFit


# %% FUNCTIONS


def Gauss(x, A, sigma, c):
    return A * np.exp(-((x - c) ** 2) / 2 / sigma ** 2)


def Gauss1D(x, *p):
    return p[0] + p[1] * np.exp(-((x - p[3]) ** 2) / 2 / p[2] ** 2)


def Gauss2D(xy, *p):
    """ p = [offset, amplitude, size_x, size_y, center_x, center_y]"""
    (x, y) = xy
    return p[0] + p[1] * Gauss(x, 1, p[2], p[4]) * Gauss(y, 1, p[3], p[5])


# %% CLASS DEFINITION
class Gauss2DFit(Abstract2DFit):
    """a 2D Gauss fit"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # -- attributes specific to 2D Gauss fit
        self.name = "Gauss2D"
        self.formula_help = "f(x) = p[0] "
        self.formula_help += "+ p[1] * exp(-(x - p[4]) ** 2 / (2 * p[2]**2))"
        self.formula_help += " * exp(-(x - p[5]) ** 2 / (2 * p[3]**2))"
        self.parameters_help = (
            "p = [offset, amplitude, size_x, size_y, center_x, center_y]"
        )
        self._version = "1.0"

    def _fitfunc(self, x, *p):
        return Gauss2D(x, *p)

    def do_guess(self):
        """guess fit parameters from preliminary data analysis"""

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
        x = X[0, :]
        y = Y[:, 0]

        # -- use 1D fits on integrated data to estimate 2D fit parameters
        results = {}
        for axis, u, label in zip([0, 1], [x, y], ["x", "y"]):
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
        sx = results["x"][2]
        sy = results["y"][2]
        offset = 0.5 * (results["x"][0] + results["y"][0])
        # find max
        xr = X.ravel()
        yr = Y.ravel()
        zr = Z.ravel()
        imax = np.argmin((cx - xr) ** 2 + (cy - yr) ** 2)
        amplitude = zr[imax]
        # guess
        p0 = [offset, amplitude, sx, sy, cx, cy]
        self.guess = p0


# %% TESTS
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # -- generate noisy data
    x = np.linspace(-10, 10, 200)
    X, Y = np.meshgrid(x, x)
    p = [0.5, 5.0, 0.5, 2.0, 5, 1.0]
    Z = Gauss2D((X, Y), *p)
    noise = (np.random.rand(*X.shape) - 0.5) * 2
    Z += noise

    # -- Fit
    g2Dfit = Gauss2DFit(x=(X, Y), z=Z)
    g2Dfit.guess = [0.4, 6, 3.2, 1.8, 0, 0]
    g2Dfit.do_guess()
    print('>> guess')
    print(g2Dfit.guess)
    g2Dfit.do_fit()

    Zfit = g2Dfit.eval((X, Y))
    print('>> popt')
    print(g2Dfit.popt)

    print(g2Dfit.export_json_str())
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


