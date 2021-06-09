# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-06 10:09:31

Comments :
"""

from .basicImageDisplay import BasicImageDisplay
from .imageOnlyDisplay import ImageOnlyDisplay
from .focusOnFit2D import FocusOnFit2D
from .liveMetaData import LiveMetaData

implemented_display = [
    BasicImageDisplay,
    ImageOnlyDisplay,
    FocusOnFit2D,
]

implemented_display_dic = {}
for obj in implemented_display:
    implemented_display_dic[obj().name] = obj
