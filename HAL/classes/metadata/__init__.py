# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-07 14:33:19

Comments :
"""
from .file import FileData
from .gus import GusData
from .hev_fit import HevFitData
from .hal_fit import HALFitData

implemented_metadata = [FileData, GusData, HALFitData, HevFitData]

implemented_metadata_dic = {}
for obj in implemented_metadata:
    implemented_metadata_dic[obj().name] = obj
