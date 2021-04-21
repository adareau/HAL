# -*- coding: utf-8 -*-
'''
Author   : Alexandre
Created  : 2021-04-07 14:33:19
Modified : 2021-04-21 18:04:05

Comments :
'''
from HAL.classes.metadata.file import FileData

implemented_metadata = [FileData(), ]

implemented_metadata_dic = {}
for obj in implemented_metadata:
    implemented_metadata_dic[obj.name] = obj