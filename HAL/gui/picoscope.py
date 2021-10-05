# -*- coding: utf-8 -*-

# %% IMPORTS

# -- global
import logging
import matplotlib.pyplot as plt
import numpy as np
import h5py
from datetime import datetime
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (
    QInputDialog,
    QAbstractItemView,
    QStyle,
    QListWidgetItem,
    QMessageBox,
    QMenu,
    QAction,
    QActionGroup,
    QToolButton,
)

# -- local
from . import dataexplorer

# -- logger
logger = logging.getLogger(__name__)


# %% TOOLS


def _isnumber(x):
    try:
        float(x)
        return True
    except (TypeError, ValueError):
        return False


# %% SETUP FUNCTIONS



def plotpico(self):
    #open file
    filename = "/home/charlie/Bureau/tmp/20211005_105200_769042_79d3a08.hdf5"
    f = h5py.File(filename,'r')

    #open data
    datapicoscope = f.get('data/picoscope/0/data')[()]


    time = datapicoscope[0]
    chA=datapicoscope[1]
    chB=datapicoscope[2]
    chC=datapicoscope[3]
    chD=datapicoscope[4]

    #plot data
    plt.figure()
    plt.grid(True)
    plt.plot(time,chA,label='chA')
    plt.plot(time,chB,label='chB')
    plt.plot(time,chC,label='chC')
    plt.plot(time,chD,label='chD')
    plt.xlabel('Time (ns)')
    plt.ylabel('Voltage (mV)')
    plt.legend()
    plt.show()

def statspico(self):
    #open file
    filename = "/home/charlie/Bureau/tmp/20211005_105200_769042_79d3a08.hdf5"
    f = h5py.File(filename,'r')

    #open data
    datapicoscope = f.get('data/picoscope/0/data')[()]


    time = datapicoscope[0]
    chA=datapicoscope[1]
    chB=datapicoscope[2]
    chC=datapicoscope[3]
    chD=datapicoscope[4]

    #stats
    print('============STATS chA============')
    print(f" mean: {round(np.mean(chA))} mV\n stdev: {round(np.std(chA))} mV\n min: {round(np.min(chA))} mV\n max: {round(np.max(chA))} mV\n")
    print('============STATS chB============')
    print(f" mean: {round(np.mean(chB))} mV\n stdev: {round(np.std(chB))} mV\n min: {round(np.min(chB))} mV\n max: {round(np.max(chB))} mV\n")
    print('============STATS chC============')
    print(f" mean: {round(np.mean(chC))} mV\n stdev: {round(np.std(chC))} mV\n min: {round(np.min(chC))} mV\n max: {round(np.max(chC))} mV\n")
    print('============STATS chD============')
    print(f" mean: {round(np.mean(chD))} mV\n stdev: {round(np.std(chD))} mV\n min: {round(np.min(chD))} mV\n max: {round(np.max(chD))} mV\n")
