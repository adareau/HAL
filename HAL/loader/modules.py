# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-06-24 15:38:56

Comments : Functions to load modules, user-defined and default
"""

# %% IMPORTS

# -- global
import logging

# -- local
from .. import default_modules as default

# -- logger
logger = logging.getLogger(__name__)


# %% MODULE LOADING FUNCTION
def load(self):
    """Loads all the modules, both the default ones located in `default_modules`
    and the user-defined ones located in `~/.HAL/user_modules`"""

    # -- init the module list
    loaded_modules = []
    loaded_modules_names = []

    # -- include the default
    loaded_modules.append(default)
    loaded_modules_names.append("default")

    return loaded_modules, loaded_modules_names
