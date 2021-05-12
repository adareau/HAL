# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-06 10:09:31
Modified : 2021-05-07 11:57:55

Comments :
"""

from HAL.classes.display.basicImageDisplay import BasicImageDisplay
from HAL.classes.display.imageOnlyDisplay import ImageOnlyDisplay
from HAL.classes.display.focusOnFit2D import FocusOnFit2D

implemented_display = [
    BasicImageDisplay,
    ImageOnlyDisplay,
    FocusOnFit2D,
]

implemented_display_dic = {}
for obj in implemented_display:
    implemented_display_dic[obj().name] = obj
