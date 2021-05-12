# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-07 14:33:19
Modified : 2021-05-11 15:51:48

Comments :
"""
from HAL.classes.metadata.file import FileData
from HAL.classes.metadata.gus import GusData
from HAL.classes.metadata.hev_fit import HevFitData
from HAL.classes.metadata.hal_fit import HALFitData

implemented_metadata = [FileData, GusData, HALFitData, HevFitData]

implemented_metadata_dic = {}
for obj in implemented_metadata:
    implemented_metadata_dic[obj().name] = obj
