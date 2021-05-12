# -*- coding: utf-8 -*-
'''
Author   : Alexandre
Created  : 2021-04-29 17:00:13
Modified : 2021-05-12 17:32:00

Comments : a python script to compile the Qt gui, i.e. to convert the language
           agnostic 'main.ui' into a class that can be imported in a Python
           script
'''

# %% IMPORTS
from PyQt5 import uic
from pathlib import Path

# %% SETTINGS
file_in = Path('.') / 'HAL' / 'gui' / 'main.ui'
file_out = Path('.') / 'HAL' / 'gui' / 'MainUI.py'

# %% BUILD
with open(file_out, 'w+') as out_file:
    uic.compileUi(file_in, out_file)