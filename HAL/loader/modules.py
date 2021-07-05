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
import inspect

# -- local
from .. import default_modules as default

# - abstract classes
from ..classes.metadata.abstract import AbstractMetaData
from ..classes.fit.abstract import Abstract2DFit, Abstract1DFit
from ..classes.data.abstract import AbstractData
from ..classes.display.abstract import AbstractDisplay

# -- logger
logger = logging.getLogger(__name__)


# %% LOW LEVEL FUNCTIONS


def _getModules(self):
    """Gets all modules, both the default ones located in `default_modules`
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


def _sortModules(self, loaded_modules, loaded_modules_names):
    """Sorts the user modules"""

    # -- init lists / dict
    # implemented data classes
    self.data_classes = []
    # implemented metadata classes
    self.metadata_classes = []
    # implemented 2D fit classes
    self.fit_classes = []
    # implemented display classes
    self.display_classes = []
    # implemented 1D fit classes
    self.fit_classes_1D = []

    # -- generate list of ignored packages
    ignored = self.settings.config["global"]["ignored modules list"]
    ignored = ignored.split(",")
    ignored = [name.replace(" ", "") for name in ignored]
    logger.debug(f"ignored packages : {', '.join(ignored)}")
    # -- parse the content of ..module and append to lists
    for module, name in zip(loaded_modules, loaded_modules_names):
        logger.debug(f"parsing user module {name}")
        # check that the module has a 'user_module' list implemented
        # this should be already checked in the __init__.py of ..modules
        # but ¯\_(ツ)_/¯ why not check again ?
        if "user_modules" not in module.__dict__.keys():
            msg = f"user module '{name}' has no 'user_module' list defined"
            logger.warning(msg)
            continue
        # parse the user modules
        for usermod in module.user_modules:
            # if it is not a class: we do not want it
            if not inspect.isclass(usermod):
                logger.debug("skipped one 'non-class' object.. strange..")
                continue
            # is it ignored ?
            if usermod.__name__ in ignored:
                logger.debug(f"ignored package '{usermod.__name__}'")
                continue
            # if it is a child of AbstractMetaData >> to self.metadata_classes !
            if issubclass(usermod, AbstractMetaData):
                logger.debug(f"found one metadata class '{usermod.__name__}'")
                self.metadata_classes.append(usermod)
            # if it is a child of Abstract2DFit >> to self.fit_classes !
            elif issubclass(usermod, Abstract2DFit):
                logger.debug(f"found one fit class '{usermod.__name__}'")
                self.fit_classes.append(usermod)
            # if it is a child of AbstractData >> to self.data_classes !
            elif issubclass(usermod, AbstractData):
                logger.debug(f"found one fit class '{usermod.__name__}'")
                self.data_classes.append(usermod)
            # if it is a child of AbstractDisplay >> to self.display_classes !
            elif issubclass(usermod, AbstractDisplay):
                logger.debug(f"found one fit class '{usermod.__name__}'")
                self.display_classes.append(usermod)
            # if it is a child of Abstract1DFit >> to self.fit_classes_1D !
            elif issubclass(usermod, Abstract1DFit):
                logger.debug(f"found one fit class '{usermod.__name__}'")
                self.fit_classes_1D.append(usermod)
            # otherwise raise warning
            else:
                msg = f"Unknown class type for user module '{usermod.__name__}'"
                logger.warning(msg)

    # -- generate a list of implemented fit names
    # this will be useful for loading fit
    self.fit_classes_dic = {}
    for fit_class in self.fit_classes:
        name = fit_class().name
        if name in self.fit_classes_dic:
            msg = f"fit name '{name}' was already taken... it will be overriden "
            msg += "in the fit dictionnary. This might cause bugs when loading "
            msg += "saved fit. You should rename your fits so that they have "
            msg += "unique names !"
            logger.warning(msg)
        self.fit_classes_dic[name] = fit_class


# %% MAIN FUNCTION


def load(self):
    """the main function, called by the gui"""
    # -- get available modules
    loaded_modules, loaded_modules_names = _getModules(self)
    # -- sort them
    _sortModules(self, loaded_modules, loaded_modules_names)
