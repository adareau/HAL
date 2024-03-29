# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-06-10 09:25:47

Comments : test
"""

# %% IMPORT
# -- metadata
from .metadata.fit import HALFitData
from .metadata.file import FileData

# -- fit (2D)
from .fit.gauss2D import Gauss2DFit
from .fit.statsOnly2D import StatsOnly2D
from .fit.thomasfermi2D import ThomasFermi2DFit

# -- fit (1D)
from .fit.gauss1D import Gauss1DFit
from .fit.lorentz1D import Lorentz1DFit
from .fit.oscillations import Oscillation1DFit
from .fit.dampedoscillations import DampedOscillation1DFit
from .fit.exponential1D import Exponential1DFit
from .fit.exponential_with_offset1D import ExponentialOffset1DFit
from .fit.hyperbolictangent1D import Hyperbolictangent1DFit
from .fit.polynomial1D import polyfit_generator

# -- data
from .data.rawCamera import RawCamData

# -- display
from .display.basicImageDisplay import BasicImageDisplay
from .display.imageOnlyDisplay import ImageOnlyDisplay
from .display.focusOnFit2D import FocusOnFit2D

# %% STORE
user_modules = [
    # metadata
    FileData,
    HALFitData,
    # fits
    Gauss2DFit,
    StatsOnly2D,
    ThomasFermi2DFit,
    # data
    RawCamData,
    # display
    BasicImageDisplay,
    ImageOnlyDisplay,
    FocusOnFit2D,
    # fits (1D)
    Gauss1DFit,
    Lorentz1DFit,
    Oscillation1DFit,
    DampedOscillation1DFit,
    Exponential1DFit,
    ExponentialOffset1DFit,
    Hyperbolictangent1DFit,
]

# - add poly fit
n_max = 4
for order in range(1, n_max + 1):
    user_modules.append(polyfit_generator(order))
