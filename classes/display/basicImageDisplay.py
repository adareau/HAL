# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-06 10:55:48
Modified : 2021-05-06 11:36:48

Comments : a basic (2D) image display. Can be used as an example when building
           more complex display objects
"""

# %% IMPORTS

# -- global
import numpy as np
import pyqtgraph as pg

# -- local
from HAL.classes.display.abstract import AbstractDisplay
from HAL.classes.display.colormaps import get_pyqtgraph_lookuptable


# %% CLASS DEFINITION


class BasicImageDisplay(AbstractDisplay):
    """a basic (2D) image display"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # -- attributes
        self.roi_list = []
        self.image_plot = None
        self.current_image = None
        self.current_data = None

        # -- other attributes
        self.name = "Basic image display"
        self.type = "2D"

    # -- DISPLAY MANAGEMENT

    def setup(self):
        """sets up display"""
        # -- reset
        self.screen.clear()

        # -- create image plot
        # add subplot
        p = self.screen.addPlot(0, 0)
        # configure subplot
        p.setAspectLocked(lock=True, ratio=1)
        p.setLabel("bottom", "X", units="px")
        p.setLabel("left", "Y", units="px")
        # store
        self.image_plot = p

        # -- init image itemp
        img = pg.ImageItem()
        p.addItem(img)
        self.current_image = img

    def clearPlot(self):
        """clear all the data plot"""
        pass

    def updatePlot(self, image=None, levels=(0, 1), colormap="Greiner"):
        """updates the data plot"""
        if image is None:
            return

        # redefine limits
        self.image_plot.setLimits(
            xMin=0, yMin=0, xMax=image.shape[0], yMax=image.shape[1]
        )
        # update image
        self.current_image.updateImage(image=image, levels=levels)
        self.current_data = image

        # set colormap
        self.updateColormap(colormap)

    def updateColormap(self, colormap="Greiner"):
        # set colormap
        lut = get_pyqtgraph_lookuptable(colormap)
        self.current_image.setLookupTable(lut)

    def clearFit(self):
        """resets fit display"""
        pass

    def updateFit(self):
        """updates the fit display"""
        pass

    # -- ROI MANAGEMENT

    def addRoi(self):
        """adds an roi"""
        pass

    def getRoiNames(self):
        """returns list of current roi"""
        pass

    def getRoiPos(self):
        """returns a given roi position"""
        pass

    def getRoiSize(self):
        """returns a given roi position"""
        pass

    def removeRoi(self):
        """remove given roi"""
        pass

    # -- DATA MANAGEMENT

    def getRoiData(self):
        """returns data contained in a given ROI"""
        pass
