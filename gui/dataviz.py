# -*- coding: utf-8 -*-
'''
Author   : Alexandre
Created  : 2021-04-21 16:28:03
Modified : 2021-04-21 16:44:38

Comments : Functions related to data visualization
'''

# %% IMPORTS
import pyqtgraph as pg
import numpy as np

from PyQt5 import QtCore
from matplotlib import cm

# %% SETUP FUNCTIONS


def setupDataViz(self):
    # -- setup data classes list selector
    for name in self.data_classes.keys():
        self.dataTypeComboBox.addItem(name)


# %% DISPLAY FUNCTIONS

def plotSelectedData(self):
    '''
    loads the selected data, and plot it
    '''
    # FIXME : preliminary, should call dataViz classes for displaying !
    # -- get selected data
    selection = self.runList.selectedItems()
    if not selection:
        return

    # -- init object data
    # get object data type
    data_type = self.dataTypeComboBox.currentText()
    data = self.data_classes[data_type]
    # get path
    item = selection[0]
    data.path = item.data(QtCore.Qt.UserRole)
    # check
    if not data.filter():
        print('ERROR')
        return
    # load
    data.load()

    # -- plot
    self.mainScreen.clear()
    img = pg.ImageItem()
    p = self.mainScreen.addPlot(0, 0)
    p.addItem(img)
    # Get the colormap
    colormap = cm.get_cmap("RdBu")
    colormap._init()
    lut = (colormap._lut * 255).view(np.ndarray)  # Convert matplotlib colormap from 0-1 to 0 -255 for Qt

    # Apply the colormap
    img.setLookupTable(lut)
    img.updateImage(image=data.data,
                    levels=(np.min(data.data),
                            np.max(data.data)))

