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
from .abstractImage import AbstractImageDisplay


# %% CLASS DEFINITION


class FocusOnFit2D(AbstractImageDisplay):
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
        self._data_in = None
        # -- other attributes
        self.name = "Focus on fit 2D"

    # -- DISPLAY MANAGEMENT

    def setup(self):
        """sets up display"""
        # -- reset
        self.screen.clear()

        # -- create plot layout
        roi_plot = self.screen.addPlot(1, 1, title="Data (ROI)")
        fit_plot = self.screen.addPlot(2, 1, title="Fit (ROI)")
        err_plot = self.screen.addPlot(2, 2, title="Error")
        im_plot = self.screen.addPlot(1, 2, title="Data (all)")

        # stretch
        layout = self.screen.ci.layout
        layout.setColumnStretchFactor(1, 1)

        # configure subplot
        im_plot.setAspectLocked(lock=True, ratio=1)
        im_plot.setLabel("bottom", "X", units="px")
        im_plot.setLabel("left", "Y", units="px")

        # store
        self.image_plot = im_plot
        self.fit_plot = fit_plot
        self.roi_plot = roi_plot
        self.err_plot = err_plot

        # -- init image item
        # main image
        img = pg.ImageItem()
        im_plot.addItem(img)
        self.current_image = img

        # roi image
        roi_img = pg.ImageItem()
        roi_plot.addItem(roi_img)
        self.current_roi_image = roi_img

        # fit image
        fit_img = pg.ImageItem()
        fit_plot.addItem(fit_img)
        self.current_fit_image = fit_img

        # err image
        err_img = pg.ImageItem()
        err_plot.addItem(err_img)
        self.current_err_image = err_img

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

        # update roi (so that the roi is refreshed even if no fit is loaded)
        if selected_ROI is not None:
            Z, _ = self.getROIData(selected_ROI)
            if Z is not None:
                # roi
                self.current_roi_image.updateImage(image=Z, levels=levels)
                self.updateColormap(
                    colormap=colormap,
                    image=self.current_roi_image,
                )

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
        image = np.zeros((10, 10))
        self.current_fit_image.updateImage(image=image, levels=(0, 1))
        self.current_err_image.updateImage(image=image, levels=(0, 1))
        self.err_plot.setTitle("Error")

    def updateFit(
        self,
        fit_dic,
        selected_ROI,
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

        # error
        Zerr = Z - Zfit

        # -- display
        # roi
        self.current_roi_image.updateImage(image=Z, levels=self._current_levels)
        self.updateColormap(
            colormap=self._current_colormap, image=self.current_roi_image
        )

        # fit
        self.current_fit_image.updateImage(image=Zfit, levels=self._current_levels)
        self.updateColormap(
            colormap=self._current_colormap, image=self.current_fit_image
        )

        # err
        err_ampl = np.max(np.abs(Zerr))
        self.current_err_image.updateImage(image=Zerr, levels=(-err_ampl, err_ampl))
        new_title = "Error : range = ± %.2g" % err_ampl
        self.err_plot.setTitle(new_title)
        self.updateColormap(
            colormap="RdBu", image=self.current_err_image, update_current=False
        )
