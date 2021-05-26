# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-06 10:34:02
Modified : 2021-05-07 16:05:54

Comments : Abstract classes for data display, dedicated to image display !
"""

# %% IMPORTS

# -- global
import logging
import pyqtgraph as pg

# -- local
from HAL.classes.display.abstract import AbstractDisplay
from HAL.classes.display.colormaps import get_pyqtgraph_lookuptable

# -- logger
logger = logging.getLogger(__name__)

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
        self.background = None
        self.image_plot = None
        self.current_image = None
        self.current_data = None
        self._current_colormap = "Greiner"
        self._selected_ROI = None

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
            logger.warning(msg % roi_name)
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
        new_roi.label_color = label_color
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

    def getROI(self, roi_name="ROI"):
        """returns a given roi"""
        if roi_name not in self.roi_list:
            msg = "'%s' roi name not found."
            logger.warning(logger.warning(msg % roi_name))
            return None
        else:
            return self.roi_list[roi_name]

    def getROINames(self):
        """returns list of current roi"""
        return list(self.roi_list.keys())

    def getROIPos(self, roi_name="ROI"):
        """returns a given roi position"""
        roi = self.getROI(roi_name)
        return [0, 0] if roi is None else list(roi.pos())

    def getROISize(self, roi_name="ROI"):
        """returns a given roi position"""
        roi = self.getROI(roi_name)
        return [0, 0] if roi is None else list(roi.size())

    def removeROI(self, roi_name="ROI"):
        """remove given roi"""
        roi = self.getROI(roi_name)
        if roi is None:
            return
        self.image_plot.removeItem(roi.label)
        self.image_plot.removeItem(roi)
        self.roi_list.pop(roi_name)

    def updateROI(self, roi_name="ROI", pos=None, size=None, name=None):
        """updates a given ROI"""
        roi = self.getROI(roi_name)
        if roi is None:
            return
        if pos is not None:
            roi.setPos(pos, finish=True, update=True)
        if size is not None:
            roi.setSize(size, finish=True, update=True)
        if name is not None:
            if name in self.roi_list:
                msg = f"{name} roi name is already used."
                logger.warning(msg)
                return
            roi.name = name
            roi.label.setText(roi.name)
            self.roi_list[roi.name] = self.roi_list.pop(roi_name)
            return 0

    def clearROIs(self):
        """ clears the whole set of existing ROIs"""
        for roi in self.roi_list.values():
            self.image_plot.removeItem(roi.label)
            self.image_plot.removeItem(roi)
        self.roi_list = {}


    # -- DATA MANAGEMENT

    def getROIData(self, roi_name="ROI"):
        """returns data contained in a given ROI"""
        # check that roi name exists
        roi = self.getROI(roi_name)
        if roi is None:
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

    # -- BACKGROUND MANAGEMENT

    def addBackground(
        self,
        background_style=None,
        background_hover_style=None,
        handle_style=None,
        handle_hover_style=None,
        label_color="#000000FF",
    ):
        """adds a background"""
        # check if background exists
        if self.background is not None:
            logger.debug("background already added : skip")
            return

        # check that plot is initialized
        if self.image_plot is None:
            logger.debug("no image defined : do not add background")
            return

        # create roi object
        background = pg.RectROI(
            pos=[0, 0],
            size=[30, 30],
            rotatable=False,
            pen=background_style,
            hoverPen=background_hover_style,
            handlePen=handle_style,
            handleHoverPen=handle_hover_style,
        )

        # add scale handles
        for pos in ([1, 0.5], [0, 0.5], [0.5, 0], [0.5, 1]):
            background.addScaleHandle(pos=pos, center=[0.5, 0.5])
        for pos, center in zip(
            ([0, 0], [1, 0], [1, 1], [0, 1]), ([1, 1], [0, 1], [0, 0], [1, 0])
        ):
            background.addScaleHandle(pos=pos, center=center)

        # add a label
        bck_label = pg.TextItem("Background", color=label_color)
        bck_label.setPos(0, 0)
        background.label = bck_label  # link to roi !!
        background.name = "Background"

        # make it such that the label follows the ROI !
        # using sigRegionChanged
        background.sigRegionChanged.connect(_roi_changed)
        # when finished, call self.BackgroundChangedFinished
        background.sigRegionChangeFinished.connect(
            self.BackgroundChangedFinished
        )

        # add to current plot
        self.image_plot.addItem(background)
        self.image_plot.addItem(bck_label)
        self.background = background

    def removeBackground(self):
        """remove background"""
        if None not in (self.background, self.image_plot):
            self.image_plot.removeItem(self.background.label)
            self.image_plot.removeItem(self.background)
            self.background = None

    def updateBackground(self, pos=None, size=None):
        """updates background"""
        background = self.background
        if background is None:
            return
        if pos is not None:
            background.setPos(pos, finish=True, update=True)
        if size is not None:
            background.setSize(size, finish=True, update=True)

    def getBackgroundPos(self):
        """returns the background position"""
        background = self.background
        return [0, 0] if background is None else list(background.pos())

    def getBackgroundSize(self):
        """returns the background position"""
        background = self.background
        return [0, 0] if background is None else list(background.size())

    def BackgroundChangedFinished(self):
        # SHOULD BE IMPLEMENTED IN SPECIFIC CLASSES
        # TRIGGERED WHEN THE BACKGROUND IS CHANGED
        logger.debug("background changed !")
        pass

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
