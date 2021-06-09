# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-07 14:33:19

Comments :
"""

from .xenics import XenicsData

implemented_data = [
    XenicsData(),
]

implemented_data_dic = {}
for obj in implemented_data:
    implemented_data_dic[obj.name] = obj
