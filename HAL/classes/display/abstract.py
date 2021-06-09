# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-06 10:34:02

Comments : Abstract classes for data display
"""

# %% IMPORTS

# -- local
from .colormaps import IMPLEMENTED_COLORMAPS


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

    def clearPlot(self, *args, **kwargs):
        """clear all the data plot"""
        pass

    def updatePlot(self, *args, **kwargs):
        """to update the current plot with image, 3D atoms position...
           depending on the display type"""
        pass

    def updateColormap(self, *args, **kwargs):
        """update colormap"""
        pass

    def clearFit(self, *args, **kwargs):
        """resets fit display"""
        pass

    def updateFit(self, *args, **kwargs):
        """updates the fit display"""
        pass

    # -- ROI MANAGEMENT

    def addROI(self, *args, **kwargs):
        """adds an roi"""
        pass

    def updateROI(self, *args, **kwargs):
        """adds an roi"""
        pass

    def getROINames(self, *args, **kwargs):
        """returns list of current roi"""
        return []

    def getROIPos(self, *args, **kwargs):
        """returns a given roi position"""
        pass

    def getROISize(self, *args, **kwargs):
        """returns a given roi position"""
        pass

    def removeROI(self, *args, **kwargs):
        """remove given roi"""
        pass

    def clearROIs(self):
        """clear all ROIs"""
        for roi_name in self.getROINames():
            self.removeROI(roi_name)

    # -- BACKGROUND MANAGEMENT

    def addBackground(self, *args, **kwargs):
        """add a background"""
        pass

    def removeBackground(self, *args, **kwargs):
        """remove background"""
        pass

    # -- DATA MANAGEMENT

    def getROIData(self, *args, **kwargs):
        """returns data contained in a given ROI"""
        pass

    def getCurrentDataObject(self):
        """returns current data"""
        return self.current_data_object

    # -- MISC

    def getColormaps(self, *args, **kwargs):
        """returns the list of available colormaps"""
        return IMPLEMENTED_COLORMAPS
