# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-05-06 10:09:31
Modified : 2021-05-06 11:05:50

Comments :
"""

from HAL.classes.display.basicImageDisplay import BasicImageDisplay

implemented_display = [
    BasicImageDisplay,
]

implemented_display_dic = {}
for obj in implemented_display:
    implemented_display_dic[obj().name] = obj
