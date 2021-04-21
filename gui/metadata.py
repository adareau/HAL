# -*- coding: utf-8 -*-
'''
Author   : Alexandre
Created  : 2021-04-21 16:28:03
Modified : 2021-04-21 17:55:41

Comments : Functions related to data visualization
'''

# %% IMPORTS
from PyQt5 import QtCore


# %% DISPLAY FUNCTIONS

def displayMetaData(self):
    '''
    loads related meta data and display it
    '''
    # FIXME : preliminary, should call dataViz classes for displaying !
    # -- get selected data
    selection = self.runList.selectedItems()
    if not selection:
        return

    # -- get data path
    item = selection[0]
    path = item.data(QtCore.Qt.UserRole)

    # -- display
    text = '[cat]\n'
    text += '├─ hum \t= 0.5\n'
    text += '├─ lol \t= 0.5\n'
    text += '├─ hum \t= 0.5\n'
    text += '└─ hum \t= 0.5\n'

    self.metaDataText.setText(text)

