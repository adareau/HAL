# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-06 10:55:48
Modified : 2021-05-06 16:36:25

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

        # -- create plot layout
        # add plots
        im_plot = self.screen.addPlot(1, 1)
        fit_plot = self.screen.addPlot(2, 2)
        cx_plot = self.screen.addPlot(2, 1)
        cy_plot = self.screen.addPlot(1, 2)

        # stretch
        layout = self.screen.ci.layout
        layout.setColumnStretchFactor(1, 3)
        layout.setRowStretchFactor(1, 3)

        # configure subplot
        im_plot.setAspectLocked(lock=True, ratio=1)
        im_plot.setLabel("bottom", "X", units="px")
        im_plot.setLabel("left", "Y", units="px")

        # store
        self.image_plot = im_plot
        self.fit_plot = fit_plot
        self.cx_plot = cx_plot
        self.cy_plot = cy_plot

        # -- init image item
        # main image
        img = pg.ImageItem()
        im_plot.addItem(img)
        self.current_image = img

        # fit image
        fit_img = pg.ImageItem()
        fit_plot.addItem(fit_img)
        self.current_fit_image = fit_img

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

        # -- plot cuts
        # coordinates cuts
        x = X[:, 0]
        y = Y[0, :]

        # get argmax
        i, j = np.unravel_index(Zfit.argmax(), Zfit.shape)

        # plot x cut
        self.cx_plot.clear()
        self.cx_plot.plot(x, Z[:, j], symbol="+", size=1, symbolSize=5)
        self.cx_plot.plot(
            x, Zfit[:, j], pen=pg.mkPen(color=(255, 0, 0), width=2)
        )

        # plot y cut
        self.cy_plot.clear()
        self.cy_plot.plot(Z[i, :], y, symbol="+", size=1, symbolSize=5)
        self.cy_plot.plot(
            Zfit[i, :], y, pen=pg.mkPen(color=(255, 0, 0), width=2)
        )

        # -- display
        # fit
        self.current_fit_image.updateImage(
            image=Zfit, levels=self._current_levels
        )
        self.updateColormap(
            colormap=self._current_colormap, image=self.current_fit_image
        )
