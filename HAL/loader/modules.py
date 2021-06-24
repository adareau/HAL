# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-06-24 15:38:56

Comments : Functions to load modules, user-defined and default
"""

# %% IMPORTS

# -- global
import logging
import sys
import importlib

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

    # -- loader user-defined
    # get user module folder and add to system path
    user_modules_folder = self._user_modules_folder
    parent_folder = str(user_modules_folder.parent)
    if parent_folder not in sys.path:
        sys.path.append(parent_folder)
    # scan for modules folders
    module_folder_list = []
    for content in user_modules_folder.iterdir():
        if content.is_dir():
            if content.name.startswith((".", "_")):
                continue
            init_file = content / "__init__.py"
            if init_file.is_file():
                module_folder_list.append(content)

    # load all user modules
    for content in module_folder_list:
        logger.debug(f"found user module '{content.name}'")
        try:
            module = importlib.import_module(f"user_modules.{content.name}")
            if "user_modules" in module.__dict__.keys():
                logger.debug(f">> user module '{content.name}' loaded !")
                loaded_modules.append(module)
                loaded_modules_names.append(content.name)
            else:
                msg = f"user module '{content.name}' has no 'user_module' list defined >> skip import"
                logger.warning(msg)
        except Exception as e:
            logger.warning(f"ERROR when loading user module '{content.name}'")
            logger.warning(e)
            raise (e)

    return loaded_modules, loaded_modules_names
