# -*- coding: utf-8 -*-
'''
Author   : Alexandre
Created  : 2021-04-07 14:33:19
Modified : 2021-04-22 13:21:13

Comments :
'''
from HAL.classes.metadata.file import FileData
from HAL.classes.metadata.gus import GusData

implemented_metadata = [FileData(), GusData()]

implemented_metadata_dic = {}
for obj in implemented_metadata:
    implemented_metadata_dic[obj.name] = obj