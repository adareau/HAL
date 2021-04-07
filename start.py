# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-07 14:35:18
Modified : 2021-04-07 15:08:54

Comments : starts the HAL gui
"""

# %% IMPORTS

# -- global
from PyQt5 import QtWidgets
import sys

# -- local
from HAL.gui.main import MainWindow

# %% RUN
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.main()
    app.exec_()
