# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-06 10:55:48
Modified : 2021-05-06 14:54:14

Comments : a basic (2D) image display. Can be used as an example when building
           more complex display objects
"""

# %% IMPORTS

# -- global
import pyqtgraph as pg

# -- local
from HAL.classes.display.abstractImage import AbstractImageDisplay


# %% CLASS DEFINITION


class BasicImageDisplay(AbstractImageDisplay):
    """a basic (2D) image display
       NB : inherits a LOT of methods from AbstractImageDisplay().
            Have a look at this class if you do not find a method here !
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        """ Initialization.

        Note that the AbstractImageDisplay() class initializes some methods,
        related for instance to ROI management, and defines some attributes
        that should be "populated" in the setup() method, such as :

        self.image_plot    : plotItem containing the main image
        self.current_image : imageItem of the main image
        self.current_data  : current data for the displayed image

        """
        # -- hidden
        self._current_levels = (0, 1)
        # -- other attributes
        self.name = "Basic image display"

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

    def updatePlot(
        self, image=None, levels=(0, 1), colormap="Greiner", dataobject=None
    ):
        """updates the data plot"""
        if image is None:
            return
        self.current_data_object = dataobject

        # redefine limits
        self.image_plot.setLimits(
            xMin=0, yMin=0, xMax=image.shape[0], yMax=image.shape[1]
        )
        # update image
        self.current_image.updateImage(image=image, levels=levels)
        self.current_data = image
        self._current_levels = levels
        # set colormap
        self.updateColormap(colormap)

    def clearFit(self):
        """resets fit display"""
        pass

    def updateFit(
        self, fit_dic, selected_ROI,
    ):
        """updates the fit display"""

        # -- get roi and fit data
        # get roi data
        Z, (X, Y) = self.getROIData(selected_ROI)
        if Z is None:
            return

        # generate fit for roi
        fit = fit_dic[selected_ROI]
        Zfit = fit.eval((X, Y))

        # -- display
        #TEMP
        self.current_image.updateImage(image=Zfit, levels=self._current_levels)
