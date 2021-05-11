# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-21 15:38:07
Modified : 2021-05-11 15:30:29

Comments : Abstract classes for data handling
"""
# %% IMPORTS

# -- global
import logging
from pathlib import Path

# -- logger
logger = logging.getLogger(__name__)


# %% CLASS DEFINITION
class AbstractMetaData(object):
    """Abstract Data object, to use as a model"""

    def __init__(self):

        self.name = "Abstract Meta Data"
        self.path = Path(".")
        self._data = []

    # == MANAGE DATA PROPERTY ==

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, dlist):
        """called when something is fed to self.data. We use this setter
           to analyze the list of parameters stored in data, and ensure the
           compatibility with the gui functions accessing self.data"""

        # check that the data provided is a list
        if not isinstance(dlist, list):
            msg = "[MetaData: %s] " % self.name
            msg += "a list of parameters should be provided to MetaData().data"
            logging.error(msg)
            return

        # check all parameters
        checked_list = []
        for param in dlist:
            p = self._check_param(param)
            if p:
                checked_list.append(p)

        self._data = checked_list

    def _check_param(self, param):
        """checks that the parameter is valid"""
        # -- init error message header
        msg = "[MetaData: %s] " % self.name

        # -- the parameter will fail if no name or value
        # a parameter should have a name
        if "name" not in param:
            msg += "parameter should have a 'name' key"
            logging.error(msg)
            return False
        # a parameter should have a value
        if "value" not in param:
            msg += "parameter '%s' should have a 'value' key" % param["name"]
            logging.error(msg)
            return False

        # -- the other parameters are optionnal
        checked_param = {
            "display": "%.3g",
            "unit": "",
            "comment": "",
            "plottable": True,
        }
        checked_param.update(param)

        return checked_param

    # == EMPTY METHODS ==

    def analyze(self):
        """gather metadata"""
        pass

    def getKeys(self):
        """return the list of keys"""
        return []
