# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-06 10:55:48
Modified : 2021-05-06 12:12:36

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

    def clearFit(self):
        """resets fit display"""
        pass

    def updateFit(self):
        """updates the fit display"""
        pass
