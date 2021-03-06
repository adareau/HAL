# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-06-25 10:02:28

Comments : Functions related to the command palette
"""

# %% IMPORTS

# -- global
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut, QCompleter, QDialog, QVBoxLayout, QLineEdit

# -- local
from ..gui import misc

# -- logger
logger = logging.getLogger(__name__)


# %% CLASS


class CommandPalette(QDialog):
    """A customized QDialog to use as a command palette"""

    def __init__(self, parent):
        super(CommandPalette, self).__init__()
        # set parent and various properties
        self.setParent(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.resize(300, 30)
        self.hal = parent
        # bind ctrl+P to close
        ctrlP = QShortcut(QKeySequence("Ctrl+P"), self)
        ctrlP.activated.connect(self.reject)
        # setup layout
        layout = QVBoxLayout(self)
        # add the command palette input
        cmdline = QLineEdit(self)
        layout.addWidget(cmdline)
        self.cmdline = cmdline
        # connect callback
        cmdline.returnPressed.connect(self.accept)
        # setup completer
        command_list = sorted(parent.palette_commands.keys())
        autoCompleter = QCompleter(command_list, self)
        autoCompleter.setCaseSensitivity(Qt.CaseInsensitive)
        autoCompleter.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        autoCompleter.setFilterMode(Qt.MatchContains)
        cmdline.setCompleter(autoCompleter)


# %% BUILTIN COMMAND LIST
# format = ("category", "name", "method name")
SEP = ":"
BUILTIN_COMMAND_LIST = [
    # -- global
    ("HAL", "go to github", "_gotoGithub"),
    ("HAL", "edit settings", "_editSettings"),
    ("HAL", "get online help", "_getOnlineHelp"),
    # -- data related
    ("data", "fit", "_fitButtonClicked"),
    ("data", "fit:delete", "_deleteFitButtonClicked"),
    ("data", "open current folder", "_openDataFolder"),
    # -- display related
    ("display", "add ROI", "_addRoiButtonClicked"),
    ("display", "reset ROI", "_resetRoiButtonClicked"),
]

# %% CORE FUNCTIONS


def setupPaletteList(self):
    """
    Builds a dictionnary containing command names and functions to call
    """
    global BUILTIN_COMMAND_LIST
    # - initialize the dictionnary
    palette_commands = {}
    # - include builtin commands
    for command in BUILTIN_COMMAND_LIST:
        cat, name, method = command
        if hasattr(self, method):
            if cat:
                cmd = cat + SEP + name
            else:
                cmd = name
            palette_commands[cmd] = getattr(self, method)
        else:
            logger.debug(f"method '{method}' not found")

    # - add user scripts
    for script in self.user_scripts:
        cmd = "scripts"
        if script.CATEGORY:
            cmd += SEP + script.CATEGORY
        cmd += SEP + script.NAME
        palette_commands[cmd] = script.main
    self.palette_commands = palette_commands


def showPalette(self):
    """
    shows the command palette
    """
    palette = CommandPalette(self)
    if palette.exec():
        command = palette.cmdline.text()
        logger.debug(f"running command '{command}'")
        if command in self.palette_commands:
            cmd = self.palette_commands[command]
            cmd(self)
        elif command == "darkside":
            misc.toggle_dark_theme(self)
        else:
            logger.debug("command not found...")
