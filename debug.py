#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-07 14:35:18
Modified : 2021-06-10 15:47:38

Comments : starts the HAL gui in debug mode
"""

# %% IMPORTS

# -- global
from PyQt5 import QtWidgets
import sys
import logging

# -- setup logger
# setup format
fmt = "[%(asctime)s] - %(name)s - %(levelname)s - %(message)s"
# config : default level set to Warning
logging.basicConfig(format=fmt, datefmt="%H:%M:%S", level=logging.WARNING)
# rise level to DEBUG for HAL
logger = logging.getLogger("HAL")
logger.setLevel(logging.DEBUG)

# -- local
from HAL.gui.main import MainWindow

# %% RUN
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(debug=True)
    window.main()
    app.exec_()
