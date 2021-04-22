# -*- coding: utf-8 -*-
'''
Author   : Alexandre
Created  : 2021-04-21 16:28:03
Modified : 2021-04-22 09:57:06

Comments : Functions related to (meta)data exploration
'''

# %% IMPORTS
from PyQt5 import QtCore

# %% GLOBAL
TITLE_STR = '[%s]\n'
PREFIX_CORE = '├─ '
PREFIX_LAST = '└─ '


# %% SETUP FUNCTIONS


def setupMetaData(self):
    # -- meta data text display
    self.metaDataText.setReadOnly(True)
    self.metaDataText.setLineWrapMode(self.metaDataText.NoWrap)


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

    # -- get metadata
    # we store names in a sorted way
    metadata_names = [meta.name for meta in self.metadata_classes]
    # values are then sorted in a dict
    metadata = {}
    for meta in self.metadata_classes:
        meta.path = path
        meta.analyze()
        metadata[meta.name] = meta.data

    # -- display
    # generate text string
    text = ''
    for name in metadata_names:
        param_list = metadata[name]
        if not param_list:
            # not displayed if empty
            continue
        # loop on parameters
        n_param = len(param_list)
        text += TITLE_STR % name
        for i, par in enumerate(param_list):
            # choose good prefix
            if i == n_param - 1:
                param_str = PREFIX_LAST
            else:
                param_str = PREFIX_CORE
            # prepare param string
            param_str += par['name'] + '\t= ' + par['display'] % par['value']
            if par['unit']:
                param_str += ' %s' % par['unit']
            param_str += '\n'
            # append
            text += param_str

    self.metaDataText.setPlainText(text)

