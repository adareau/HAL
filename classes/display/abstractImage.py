# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-06 10:34:02
Modified : 2021-05-07 12:05:06

Comments : Abstract classes for data display, dedicated to image display !
"""

# %% IMPORTS

# -- global
import warnings
import pyqtgraph as pg

# -- local
from HAL.classes.display.abstract import AbstractDisplay
from HAL.classes.display.colormaps import get_pyqtgraph_lookuptable
from HAL.gui.misc import warn

# %% FUNCTIONS


def _roi_changed(self):
    # move self.label
    position = self.pos()
    self.label.setPos(position[0], position[1])


# %% CLASS DEFINITION


class AbstractImageDisplay(AbstractDisplay):
    """A generic (Abstract) display for images"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # -- specific attributes
        self.roi_list = {}
        self.image_plot = None
        self.current_image = None
        self.current_data = None
        self._current_colormap = "Greiner"

        # -- other attributes
        self.name = "AbstractImageDisplay"
        self.type = "2D"  # 3D, 2D, meta...

    # == GENERIC METHODS FOR IMAGE DISPLAY ==

    # -- ROI MANAGEMENT

    def addROI(
        self,
        roi_name="ROI",
        roi_style=None,
        roi_hover_style=None,
        handle_style=None,
        handle_hover_style=None,
        label_color="#000000FF",
    ):
        """adds an roi"""

        # check that plot is initialized
        if self.image_plot is None:
            # no 'image plot' initialized, return !
            return

        # check that roi name is unique
        if roi_name in self.roi_list:
            msg = "'%s' roi name is already used."
            warn(msg % roi_name)
            return

        # create roi object
        new_roi = pg.RectROI(
            pos=[0, 0],
            size=[50, 50],
            rotatable=False,
            pen=roi_style,
            hoverPen=roi_hover_style,
            handlePen=handle_style,
            handleHoverPen=handle_hover_style,
        )

        # add scale handles
        for pos in ([1, 0.5], [0, 0.5], [0.5, 0], [0.5, 1]):
            new_roi.addScaleHandle(pos=pos, center=[0.5, 0.5])
        for pos, center in zip(
            ([0, 0], [1, 0], [1, 1], [0, 1]), ([1, 1], [0, 1], [0, 0], [1, 0])
        ):
            new_roi.addScaleHandle(pos=pos, center=center)

        # add a label
        roi_label = pg.TextItem(roi_name, color=label_color)
        roi_label.setPos(0, 0)
        new_roi.label = roi_label  # link to roi !!
        new_roi.name = roi_name

        # make it such that the label follows the ROI !
        # using sigRegionChanged
        new_roi.sigRegionChanged.connect(_roi_changed)

        # add to current plot
        self.image_plot.addItem(new_roi)
        self.image_plot.addItem(roi_label)
        self.roi_list[roi_name] = new_roi

    def getROINames(self):
        """returns list of current roi"""
        return list(self.roi_list.keys())

    def getROIPos(self, roi_name="ROI"):
        """returns a given roi position"""
        if roi_name not in self.roi_list:
            msg = "'%s' roi name not found."
            warn(msg % roi_name)
            return [0, 0]
        return list(self.roi_list[roi_name].pos())

    def getROISize(self, roi_name="ROI"):
        """returns a given roi position"""
        if roi_name not in self.roi_list:
            msg = "'%s' roi name not found."
            warn(msg % roi_name)
            return [0, 0]
        return list(self.roi_list[roi_name].size())

    def removeROI(self, roi_name="ROI"):
        """remove given roi"""
        if roi_name not in self.roi_list:
            msg = "'%s' roi name not found."
            warn(msg % roi_name)
            return
        roi = self.roi_list[roi_name]
        self.image_plot.removeItem(roi.label)
        self.image_plot.removeItem(roi)
        self.roi_list.pop(roi_name)

    def updateROI(self, roi_name="ROI", pos=None, size=None):
        """updates a given ROI"""
        if roi_name not in self.roi_list:
            msg = "'%s' roi name not found."
            warn(msg % roi_name)
            return
        roi = self.roi_list[roi_name]
        if pos is not None:
            roi.setPos(pos, finish=True, update=True)
        if size is not None:
            roi.setSize(size, finish=True, update=True)

    # -- DATA MANAGEMENT

    def getROIData(self, roi_name="ROI"):
        """returns data contained in a given ROI"""
        # check that roi name exists
        if roi_name not in self.roi_list:
            msg = "'%s' roi name not found."
            warn(msg % roi_name)
            return None, (None, None)

        # get roi, image item and image data
        roi = self.roi_list[roi_name]
        data = self.current_data
        image = self.current_image

        # get the roi data
        # use the convenient 'getArrayRegion' to retrieve selected image roi
        Z, XY = roi.getArrayRegion(data, image, returnMappedCoords=True)

        # demux X and Y from XY
        X = XY[0, :, :]
        Y = XY[1, :, :]

        return Z, (X, Y)

    # -- COLORMAP

    def updateColormap(
        self, colormap="Greiner", image=None, update_current=True
    ):
        # set colormap
        lut = get_pyqtgraph_lookuptable(colormap)
        if image is None:
            image = self.current_image
        image.setLookupTable(lut)
        if update_current:
            self._current_colormap = colormap
