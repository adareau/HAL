# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-07 15:25:18
Modified : 2021-05-20 14:47:13

Comments : implements the Settings class, that manages user settings
"""

# %% IMPORTS

# -- global
import os
import configparser
import logging

# -- local
import HAL

# -- logger
logger = logging.getLogger(__name__)

# %% GLOBAL VARIABLES
DATA_DEFAULTS = {
    "root": "~/gus_data",
    "day folder": "%d",
    "month folder": "%m",
    "year folder": "%Y",
}

FIT_DEFAULTS = {
    "fit folder name": ".HAL_fits",
}


# %% CLASS DEFINITION
class Settings(object):
    """docstring for Settings"""

    def __init__(self, path=None):
        super(Settings, self).__init__()

        # if no path is given, use HAL root folder
        if path is None:
            HAL_path = HAL.__file__
            HAL_root, _ = os.path.split(HAL_path)
            path = os.path.join(HAL_root, "global.conf")

        self.conf_file_path = path

        # initialize config parser
        self.config = configparser.RawConfigParser()
        self.init_default()

        # load
        self.load()

    def init_default(self):
        self.config["data"] = DATA_DEFAULTS
        self.config["fit"] = FIT_DEFAULTS

    def load(self):
        """load the configuration file and parse it"""
        logger.debug("loading settings from %s" % self.conf_file_path)
        # check that the file exists
        if not os.path.isfile(self.conf_file_path):
            logger.warning("ERROR IN SETTINGS LOADER")
            logger.warning(">> '%s' do not exist" % self.conf_file_path)
            return

        # load
        self.config.read(self.conf_file_path)

    def save(self, out_file=None):
        if out_file is None:
            out_file = self.conf_file_path
        with open(out_file, "w") as fout:
            self.config.write(fout)


# %% TEST
if __name__ == "__main__":
    from pathlib import Path

    settings_folder = Path().home() / ".HAL"
    global_config_path = settings_folder / "global.conf"
    set = Settings(path=global_config_path)
    set.load()
    """
    print(set.config.sections())
    for k in set.config["data"]:
        print("%s : %s" % (k, set.config["data"][k]))

    """
    set.save()
