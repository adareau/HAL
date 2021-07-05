# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-06 10:55:48

Comments : a basic (2D) image display. Can be used as an example when building
           more complex display objects
"""

# %% IMPORTS

# -- global
import pyqtgraph as pg
import numpy as np

# -- local
from HAL.classes.display.abstractImage import AbstractImageDisplay


# %% CLASS DEFINITION


class ImageOnlyDisplay(AbstractImageDisplay):
    """a basic (2D) image display, with no cuts nor fit display
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
        self._data_in = None
        # -- other attributes
        self.name = "Image only"

    # -- DISPLAY MANAGEMENT

    def setup(self):
        """sets up display"""
        # -- reset
        self.screen.clear()

        # -- create plot layout
        # add image plot
        im_plot = self.screen.addPlot(1, 1)
        im_plot.setAspectLocked(lock=True, ratio=1)
        im_plot.setLabel("bottom", "X", units="px")
        im_plot.setLabel("left", "Y", units="px")

        # store
        self.image_plot = im_plot

        # -- init image item
        # main image
        img = pg.ImageItem()
        im_plot.addItem(img)
        self.current_image = img

    def clearPlot(self):
        """clear all the data plot"""
        pass

    def updatePlot(
        self,
        image=None,
        levels=(0, 1),
        colormap="Greiner",
        dataobject=None,
        selected_ROI=None,
    ):
        """updates the data plot"""
        if image is None:
            return
        self.current_data_object = dataobject

        # redefine limits
        """
        self.image_plot.setLimits(
            xMin=0, yMin=0, xMax=image.shape[0], yMax=image.shape[1]
        )
        """
        # get background
        if self.background is not None:
            background, _ = self.background.getArrayRegion(
                image, self.current_image, returnMappedCoords=True
            )
            background_value = np.mean(background)
        else:
            background_value = 0

        # update image
        self.current_image.updateImage(image=image - background_value, levels=levels)
        self.current_data = image - background_value
        self._data_in = image
        self._current_levels = levels
        # set colormap
        self.updateColormap(colormap)

    def BackgroundChangedFinished(self):
        """triggered when the background area was moved"""
        if self._data_in is None:
            return
        # get current values / data
        image = self._data_in
        levels = self._current_levels
        colormap = self._current_colormap
        selected_ROI = self._selected_ROI
        dataobject = self.current_data_object
        # update plot
        self.updatePlot(
            image=image,
            levels=levels,
            colormap=colormap,
            dataobject=dataobject,
            selected_ROI=selected_ROI,
        )

    def clearFit(self):
        """resets fit display"""
        pass

    def updateFit(
        self,
        fit_dic,
        selected_ROI,
    ):
        """updates the fit display"""
        # DOES NOTHING :)
        pass
