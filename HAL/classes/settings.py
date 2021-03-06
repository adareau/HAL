# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-07 15:25:18

Comments : implements the Settings class, that manages user settings
"""

# %% IMPORTS

# -- global
import os
import configparser
import logging
from pathlib import Path
from io import StringIO
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QDialogButtonBox,
    QVBoxLayout,
    QHBoxLayout,
    QSpacerItem,
    QGridLayout,
    QLabel,
    QDialog,
    QPlainTextEdit,
    QPushButton,
    QSizePolicy,
    QMessageBox,
    QShortcut,
)

# -- logger
logger = logging.getLogger(__name__)

# %% GLOBAL VARIABLES

GLOBAL_DEFAULTS = {
    "ignored modules list": "",
}

DATA_DEFAULTS = {
    "root": "~/gus_data",
    "day folder": "%d",
    "month folder": "%m",
    "year folder": "%Y",
}

METADATA_DEFAULTS = {"autorefresh cache": True, "do not display": "com_x, com_y"}

FIT_DEFAULTS = {"fit folder name": ".HAL_fits", "custom guess": "false"}

GUI_DEFAULT = {
    "font family": "Sans Serif",
    "font size": 9,
}

DEV_DEFAULT = {
    "log callbacks": False,
}


# %% SETTINGS EDITOR DIALG CLASS


class SettingsEditor(QDialog):
    def __init__(self, user_config_path, default_config="", parent=None):
        super().__init__(parent)

        self.setWindowTitle("Config editor")
        self.resize(800, 600)
        # -- Config editors
        # create
        self.defaultConfigDisplay = QPlainTextEdit()
        self.defaultConfigDisplay.setPlainText(default_config)
        self.defaultConfigDisplay.setReadOnly(True)
        self.userConfigEdit = QPlainTextEdit()
        # titles
        default_title = QLabel("Default config")
        user_title = QLabel("User config (overrides default)")
        # join in layout
        self.configLayout = QGridLayout()
        self.configLayout.addWidget(default_title, 0, 0)
        self.configLayout.addWidget(self.defaultConfigDisplay, 1, 0)
        self.configLayout.addWidget(user_title, 0, 1)
        self.configLayout.addWidget(self.userConfigEdit, 1, 1)

        # -- Buttons
        # check button
        self.checkButton = QPushButton("Check config")
        self.checkButton.clicked.connect(self.checkConfig)
        # cancel / save
        QBtn = QDialogButtonBox.Cancel | QDialogButtonBox.Save
        # create dialog button box & connect callbacks
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.checkBeforeAccept)
        self.buttonBox.rejected.connect(self.reject)
        # button layout
        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.addWidget(self.checkButton)
        spacer = QSpacerItem(40, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.buttonLayout.addItem(spacer)
        self.buttonLayout.addWidget(self.buttonBox)

        # -- Setting up main layout
        self.layout = QVBoxLayout()
        self.layout.addLayout(self.configLayout)
        message = QLabel("user config path: %s" % user_config_path)
        self.layout.addWidget(message)
        self.layout.addLayout(self.buttonLayout)
        self.setLayout(self.layout)

        # -- keyboard shortcut
        self.ctrlS = QShortcut(QKeySequence("Ctrl+S"), self)
        self.ctrlS.activated.connect(self.checkBeforeAccept)

        # -- load user config
        self.config_path = Path(user_config_path)
        if self.config_path.is_file():
            current_config_text = self.config_path.read_text()
            self.userConfigEdit.setPlainText(current_config_text)
        else:
            placeholder = "edit here to create a custom settings file"
            self.userConfigEdit.setPlaceholderText(placeholder)

    def checkConfig(self, show_sucess=True):
        """checks that the config will be parsed by configparser"""
        # create parser
        parser = configparser.RawConfigParser()
        # get user config
        user_config = self.userConfigEdit.toPlainText()
        # try / catch
        try:
            parser.read_string(user_config)
        except Exception as e:
            msg = "Parsing the current config as raised the following exception :"
            msg += "\n\n"
            msg += repr(e)
            QMessageBox.warning(self, "Exception caught while parsing", msg)
            return False

        if show_sucess:
            QMessageBox.information(self, "Good boi", "Config parsed sucessfully !")

        return True

    def checkBeforeAccept(self):
        """checks the config before accepting"""
        #  check
        if not self.checkConfig(show_sucess=False):
            return
        #  write
        self.config_path.write_text(self.userConfigEdit.toPlainText())
        # close window with "accept()"
        self.accept()


# %% MAIN CLASS DEFINITION


class Settings(object):
    """docstring for Settings"""

    def __init__(self, path):
        super(Settings, self).__init__()

        self.conf_file_path = path

        # initialize config parser
        self.config = configparser.RawConfigParser()
        self.initDefaults()

        # store default as a string
        # the configparser class does not have
        output = StringIO()
        self.config.write(output)
        self._default_settings_as_string = output.getvalue()

        # load
        self.load()

    def initDefaults(self):
        self.config["data"] = DATA_DEFAULTS
        self.config["global"] = GLOBAL_DEFAULTS
        self.config["fit"] = FIT_DEFAULTS
        self.config["gui"] = GUI_DEFAULT
        self.config["dev"] = DEV_DEFAULT
        self.config["metadata"] = METADATA_DEFAULTS

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

    def openGuiEditor(self, parent=None):
        """opens a gui settings editor"""
        logger.debug("edit settings in gui")
        # execute gui
        default_config = self._default_settings_as_string
        editor = SettingsEditor(
            self.conf_file_path,
            parent=parent,
            default_config=default_config,
        )
        res = editor.exec()
        # take results
        if res:
            logger.debug("settings changed, reload !")
            self.config = configparser.RawConfigParser()
            self.initDefaults()
            self.load()
            return True
        else:
            return False

    def toString(self):
        """export current settings as a string"""
        out_str = ""
        for section in self.config.sections():
            out_str += "[%s]\n" % section
            for k in self.config[section]:
                out_str += "%s=%s \n" % (k, self.config[section][k])
            out_str += "\n"
        return out_str


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
    print(set.toString())
