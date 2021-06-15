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

# -- fit
from .fit.gauss2D import Gauss2DFit
from .fit.statsOnly2D import StatsOnly2D
from .fit.thomasfermi2D import ThomasFermi2DFit

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
]
