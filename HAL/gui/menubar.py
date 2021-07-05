# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-12 09:26:01

Comments : Functions related to the window menubar
"""

# %% IMPORTS

# -- global
import logging
import pyautogui
import time
import webbrowser
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QAction, QMenu, QActionGroup
from PyQt5.QtGui import QKeySequence, QMessageBox

# -- local
from .misc import open_file

# -- logger
logger = logging.getLogger(__name__)


# %% SETUP FUNCTIONS


def setupUi(self):
    # -- Get menubar
    menuBar = self.menubar
    # -- Preferences
    # add section
    menuPreferences = QMenu("Preferences", menuBar)
    menuBar.addMenu(menuPreferences)
    self.menuPreferences = menuPreferences
    # add "settings"
    editSettingsAction = QAction("Settings", menuPreferences)
    editSettingsAction.setToolTip("Edit user settings")
    menuPreferences.addAction(editSettingsAction)
    self.menuPreferencesEditSettingsAction = editSettingsAction
    # add "open module folder"
    openModuleFolderAction = QAction("Open user modules folder", menuPreferences)
    menuPreferences.addAction(openModuleFolderAction)
    self.openModuleFolderAction = openModuleFolderAction
    # -- Data
    # add section
    menuData = QMenu("Data", menuBar)
    menuBar.addMenu(menuData)
    self.menuData = menuData
    # add "data"
    openDataFolderAction = QAction("Open current folder", menuData)
    menuData.addAction(openDataFolderAction)
    self.menuDataOpenDataFolderAction = openDataFolderAction
    # -- Scripts
    menuScripts = QMenu("Scripts", menuBar)
    menuBar.addMenu(menuScripts)
    self.menuScripts = menuScripts
    self.menuScriptsActionGroup = QActionGroup(menuScripts)
    _setupScripts(self)
    # -- About section
    # add section
    menuAbout = QMenu("About", menuBar)
    menuBar.addMenu(menuAbout)
    self.menuAbout = menuAbout
    # add "Github repository"
    gotoGithubAction = QAction("Github repository", menuAbout)
    gotoGithubAction.setToolTip("Go to HAL Github repository")
    menuAbout.addAction(gotoGithubAction)
    self.menuAboutGotoGithubAction = gotoGithubAction
    # add "HELP"
    onlineHelpAction = QAction("Online Help", menuAbout)
    onlineHelpAction.setToolTip("Find help online")
    onlineHelpAction.setShortcut(QKeySequence("CTRL+SHIFT+H"))
    menuAbout.addAction(onlineHelpAction)
    self.menuAboutOnlineHelpAction = onlineHelpAction
    # add "Show keyboard shortcuts"
    displayShortcutsAction = QAction("Display keyboard shorcuts", menuAbout)
    displayShortcutsAction.setShortcut(QKeySequence("CTRL+H"))
    menuAbout.addAction(displayShortcutsAction)
    self.menuAboutdisplayShortcutsAction = displayShortcutsAction


# %% SETUP SUBROUTINES
def _setupScripts(self):
    """Setup the 'Script' menu, allowing to run user-defined scripts"""
    # initialize some variables
    menu = self.menuScripts
    script_list = self.user_scripts
    actionGroup = self.menuScriptsActionGroup
    script_dic = {}
    # sort all scripts in a dic
    for script in script_list:
        cat = script.CATEGORY
        name = script.NAME
        func = script.main
        if cat not in script_dic:
            script_dic[cat] = {}
        script_dic[cat][name] = func
    # populate
    for cat in sorted(script_dic.keys()):
        cat_dic = script_dic[cat]
        if cat:
            submenu = QMenu(cat.title(), menu)
        else:
            submenu = menu
        for name in sorted(cat_dic.keys()):
            func = cat_dic[name]
            action = QAction(name.title(), submenu)
            action.setData((cat, name, func))
            submenu.addAction(action)
            actionGroup.addAction(action)
        if cat:
            menu.addMenu(submenu)

    # add a "open script folder"
    menu.addSeparator()
    action = QAction("Open script folder", menu)
    menu.addAction(action)
    self.openScriptFolderMenuAction = action


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
        pyautogui.press("space")
    except Exception as e:
        logger.error("error when opening online help")
        logger.error(e)


def openUserScriptFolder(self):
    folder = self._user_scripts_folder
    logger.debug(f"open script folder : {folder.expanduser()} ")
    open_file(str(folder.expanduser()))


def openUserModuleFolder(self):
    folder = self._user_modules_folder
    logger.debug(f"open module folder : {folder.expanduser()} ")
    open_file(str(folder.expanduser()))


def openDataFolder(self):
    folder = self.current_folder
    if folder is None:
        return
    logger.debug(f"open current data folder : {folder.expanduser()} ")
    open_file(str(folder.expanduser()))


def displayShortcuts(self):
    # -- prepare list
    n_max = 20
    shortcut_list = self.keyboard_shortcuts_lists
    help_str = ""
    base_fmt = " ◉ {1:{0}s} \t ▶▶  {2} \n"
    for shortcut in shortcut_list:
        sequence, _, description = shortcut
        if description:
            help_str += base_fmt.format(n_max, sequence, description)

    # -- display window
    msgBox = QMessageBox(self)
    msgBox.setBaseSize(300, 500)
    msgBox.setText("༼ HAL KEYBOARD SHORTCUTS LIST ༽")
    msgBox.setInformativeText(help_str)
    msgBox.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
    msgBox.exec()
