#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Author   : alex
Created  : 2020-09-11 15:18:05
Modified : 2021-04-07 16:19:24

Comments :
'''
# %% IMPORTS

# -- global
import sys
from PyQt5 import QtWidgets

# -- local
from HAL.gui.MainUI import Ui_mainWindow
from HAL.classes.dummy import Dummy
from HAL.classes.settings import Settings


# %% DEFINE GUI CLASS

class MainWindow(QtWidgets.QMainWindow, Ui_mainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # -- GUI related initializations
        # setup UI (as defined in HAL.gui.MainUI)
        self.setupUi(self)
        # connect callbacks
        self.connectActions()

        # -- Other initializations
        # load settings from config file
        self.settings = Settings()
        self.dummy = Dummy()

    def connectActions(self):
        self.testButton.clicked.connect(self.printText)

    def printText(self, event, msg='lol'):
        print(self.dummy.name)

    def main(self):
        self.show()


# %% RUN
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.main()
    app.exec_()