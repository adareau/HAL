# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-06 10:34:02
Modified : 2021-05-06 13:36:32

Comments : Abstract classes for data display
"""

# %% IMPORTS

# -- local
from HAL.classes.display.colormaps import IMPLEMENTED_COLORMAPS


# %% CLASS DEFINITION

class AbstractDisplay(object):
    """Abstract display object, to use as a model"""

    def __init__(self, **kwargs):

        # -- inputs
        self.screen = kwargs.get("screen", None)  # display widget

        # -- other attributes
        self.current_data_object = None
        self.name = "AbstractDisplay"
        self.type = None  # 3D, 2D, meta...

    # == THOSE METHODS HAVE TO BE IMPLEMENTED IN THE ACTUAL DISPLAY CLASSES ==

    # -- DISPLAY MANAGEMENT

    def setup(self):
        """sets up display"""
        pass

    def clearPlot(self):
        """clear all the data plot"""
        pass

    def updatePlot(self):
        """to update the current plot with image, 3D atoms position...
           depending on the display type"""
        pass

    def updateColormap(self):
        """update colormap"""
        pass

    def clearFit(self):
        """resets fit display"""
        pass

    def updateFit(self):
        """updates the fit display"""
        pass

    # -- ROI MANAGEMENT

    def addROI(self):
        """adds an roi"""
        pass

    def getROINames(self):
        """returns list of current roi"""
        pass

    def getROIPos(self):
        """returns a given roi position"""
        pass

    def getROISize(self):
        """returns a given roi position"""
        pass

    def removeROI(self):
        """remove given roi"""
        pass

    # -- DATA MANAGEMENT

    def getROIData(self):
        """returns data contained in a given ROI"""
        pass

    def getCurrentDataObject(self):
        """returns current data"""
        return self.current_data_object

    # -- MISC

    def getColormaps(self):
        """returns the list of available colormaps"""
        return IMPLEMENTED_COLORMAPS
