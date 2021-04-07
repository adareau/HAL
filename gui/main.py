#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Author   : alex
Created  : 2020-09-11 15:18:05
Modified : 2021-04-07 15:14:52

Comments :
'''
# %% IMPORTS

# -- global
import sys
from PyQt5 import QtWidgets

# -- local
from HAL.gui.MainUI import Ui_mainWindow
from HAL.classes.dummy import Dummy


class MainWindow(QtWidgets.QMainWindow, Ui_mainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.connectActions()
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