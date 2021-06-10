# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-06-09 10:21:17

Comments :
"""

# %% IMPORTS

# -- global
import importlib
import logging

from pathlib import Path

# -- logger
logger = logging.getLogger(__name__)

# %% LOAD ALL SUBMODULES

# init list
loaded_modules = []
loaded_modules_names = []

# get current folder
root = Path(__file__).parents[0]

# scan for modules
module_folder_list = []
for content in root.iterdir():
    if content.is_dir():
        if content.name.startswith((".", "_")):
            continue
        init_file = content / "__init__.py"
        if init_file.is_file():
            module_folder_list.append(content)

# sort to make sure that "defaults" comes first
folder_names = [c.name for c in module_folder_list]
if "defaults" in folder_names:
    default_path = module_folder_list.pop(folder_names.index("defaults"))
    module_folder_list.insert(0, default_path)

# load all user modules
for content in module_folder_list:
    logger.debug(f"found user module '{content.name}'")
    try:
        module = importlib.import_module(f"HAL.modules.{content.name}")
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
