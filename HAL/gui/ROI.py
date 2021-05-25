# -*- coding: utf-8 -*-
"""
Author   : QM
Comments : Methods related to the ROIs management
"""

# -- global

class ROI(object):

    __init__(self):
        return 0

    def add(
        self,
        roi_name=None,
        type='ROI',
        roi_style = {"color": "#3FFF53FF", "width": 2},
        roi_hover_style = {"color": "#FFF73FFF", "width": 2},
        handle_style = {"color": "#3FFF53FF", "width": 2},
        handle_hover_style = {"color": "#FFF73FFF", "width": 2},
        label_color = "#3FFF53FF",
        ):
        """
        adds a new roi to the current display
        """

        if roi_name is None:
            n_roi = len(self.display.getROINames())
            roi_name = "ROI %i" % n_roi

        # add roi
        self.display.add(
            roi_name=roi_name,
            roi_style=roi_style,
            roi_hover_style=roi_hover_style,
            handle_style=handle_style,
            handle_hover_style=handle_hover_style,
            label_color=label_color,
        )


    def addBackground(self):
        """ add a background"""

        if roi_name is None:
            n_roi = len(self.display.getBCGNames())
            roi_name = "Background %i" % n_roi

        # add roi
        self.display.add(
            roi_name=roi_name,
            type='Background',
            roi_style={"color": "#FF3F3FFF", "width": 2},
            roi_hover_style={"color": "#FFF73FFF", "width": 2},
            handle_style={"color": "#FF3F3FFF", "width": 2},
            handle_hover_style={"color": "#FFF73FFF", "width": 2},
            label_color="#FF3F3FFF",
        )
