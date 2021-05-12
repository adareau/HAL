# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-12 09:26:01
Modified : 2021-05-12 09:54:04

Comments : Functions related to the window menubar
"""

# %% IMPORTS

# -- global
import logging
import pyautogui
import time
import webbrowser
from PyQt5.QtWidgets import QAction, QMenu
from PyQt5.QtGui import QKeySequence

# -- logger
logger = logging.getLogger(__name__)


# %% SETUP FUNCTIONS


def setupMenubar(self):
    # -- Get menubar
    menuBar = self.menubar
    # -- About section
    # add section
    menuAbout = QMenu("About", menuBar)
    menuBar.addMenu(menuAbout)
    self.menuAbout = menuAbout
    # add "Github repository"
    gotoGithubAction = QAction("Github repository", menuAbout)
    gotoGithubAction.setToolTip("Go to HAL Github repository")
    menuAbout.addAction(gotoGithubAction)
    menuAbout.gotoGithubAction = gotoGithubAction
    # add "HELP"
    onlineHelpAction = QAction("Online Help", menuAbout)
    onlineHelpAction.setToolTip("Find help online")
    onlineHelpAction.setShortcut(QKeySequence("CTRL+H"))
    menuAbout.addAction(onlineHelpAction)
    menuAbout.onlineHelpAction = onlineHelpAction


# %% CALLBACKS


def gotoGithub(self):
    logger.debug("go to Github")
    github_url = self._url
    try:
        webbrowser.open_new_tab(github_url)
    except Exception as e:
        logger.error("error when opening github")
        logger.error(e)


def getOnlineHelp(self):
    logger.debug("online Help requested")
    online_help_url = "https://tinyurl.com/3mjpkdjs"
    try:
        webbrowser.open_new_tab(online_help_url)
        time.sleep(3)
        pyautogui.press('space')
    except Exception as e:
        logger.error("error when opening online help")
        logger.error(e)
