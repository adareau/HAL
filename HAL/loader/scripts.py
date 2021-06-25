# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-06-24 15:38:56

Comments : Functions to load user-defined scripts
"""

# %% IMPORTS

# -- global
import logging
import sys
import importlib


# -- logger
logger = logging.getLogger(__name__)


# %% MODULE LOADING FUNCTION
def load(self):
    """Loads all the scripts located in `~/.HAL/user_scripts`"""

    # -- init the script list
    loaded_scripts = []

    # -- loader user-defined
    # get user script folder and add to system path
    user_scripts_folder = self._user_scripts_folder
    parent_folder = str(user_scripts_folder.parent)
    if parent_folder not in sys.path:
        sys.path.append(parent_folder)
    # scan for modules folders
    for content in user_scripts_folder.iterdir():
        if content.suffix == ".py":
            logger.debug(f"found user script '{content.name}'")
            try:
                script = importlib.import_module(f"user_scripts.{content.stem}")
                if {"CATEGORY", "NAME", "main"} <= script.__dict__.keys():
                    logger.debug(f">> user script '{content.name}' loaded !")
                    loaded_scripts.append(script)
                else:
                    msg = f"bad format for user script '{content.name}'"
                    logger.warning(msg)
            except Exception as e:
                logger.warning(f"ERROR when loading user script '{content.name}'")
                logger.warning(e)
                raise (e)

    # store
    self.user_scripts = loaded_scripts
