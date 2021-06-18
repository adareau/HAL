# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-03 10:49:51

Comments : implements a 1D linear fit
"""
# %% IMPORTS

# -- global
import numpy as np

# -- local
from HAL.classes.fit.abstract import Abstract1DFit


# %% POLYNOMIAL FIT GENERATOR
def polyfit_generator(order):
    name = f"PolynomialDeg{order}"
    return type(name, (Polynomial1D,), {"_overload_order": lambda x: order})


# %% CLASS DEFINITION
class Polynomial1D(Abstract1DFit):
    """a 1D polynomial fit"""

    def __init__(self, order=2, **kwargs):
        super().__init__(**kwargs)

        # -- allows one to overload order
        # will be used to automatically generate classes of polyfit with a given order
        if self._overload_order() is not None:
            order = self._overload_order()

        # -- attributes specific to 2D Gauss fit
        self.order = order
        self.name = f"polynomial deg. {order}"
        self.short_name = f"deg. {order}"
        self.category = "polynomial"
        self.formula_help = "f(x) = p[0]"
        for n in np.arange(1, order + 1):
            self.formula_help += f" + p[{n}] * x"
            if n > 1:
                self.formula_help += f" ** {n}"
        self.parameters_help = ""
        self._version = "1.0"

    def _overload_order(self):
        return None

    def _fitfunc(self, x, *p):
        return np.polyval(p[::-1], x)

    def do_guess(self):
        """guess fit parameters / not needed here"""
        pass

    def do_fit(self):
        """fits the data"""

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
        # do the fit
        popt, pcov = np.polyfit(x, z, self.order, cov=True)
        popt = popt[::-1]

        # estimate standard dev
        perr = np.sqrt(np.diag(pcov))

        # -- store
        self.popt = popt
        self.pcov = pcov
        self.perr = perr

    def compute_values(self):
        """compute some physical values from the fit optimal parameters"""

        # -- check that the data and coordinates were provided
        if len(self.z) * len(self.x) * len(self.popt) == 0:
            return

        # -- get data
        z = self.z
        x = self.x
        zfit = self._fitfunc(x, *self.popt)

        # -- init values list
        values = []

        for i, (val, err) in enumerate(zip(self.popt, self.perr)):
            if i == 0:
                unit = f"{self.z_unit}"
            elif i == 1:
                unit = f"{self.z_unit} / {self.x_unit}"
            else:
                unit = f"{self.z_unit} / {self.x_unit} ** {i}"
            param = {
                "name": f"p{i}",
                "value": val,
                "error": err,
                "display": "%.3g",
                "unit": unit,
                "comment": f"polynomial {i} power coefficient",
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


# %% TESTS
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    if False:
        try:
            n = 3
            fitClass = polyfit_generator(n)
            fit = fitClass()
            print(fit.formula_help)
            # -- generate noisy data
            x = np.linspace(-10, 10, 200)
            p = np.arange(n + 1)
            z = fit.eval(x, p)
            noise = (np.random.rand(*x.shape) - 0.5) * 2
            z += noise
            # -- Fit
            fit.x = x
            fit.z = z
            fit.z_unit = "km"
            fit.x_unit = "h"
            fit.do_guess()
            print(">> guess")
            print(fit.guess)
            fit.do_fit()
            xfit = np.linspace(x.min(), x.max(), 1000)
            zfit = fit.eval(xfit)

            print(">> popt")
            print(fit.popt)

            fit.compute_values()
            print(fit.export_json_str())

            plt.figure()
            plt.plot(x, z, "o")
            plt.plot(xfit, zfit)
            plt.show()
        except Exception as e:
            print(e)
        sys.path.remove(hal_path)
