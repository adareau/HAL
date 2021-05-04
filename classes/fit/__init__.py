# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-07 14:33:19
Modified : 2021-05-03 15:00:09

Comments :
"""

from HAL.classes.fit.gauss2D import Gauss2DFit

implemented_fit = [
    Gauss2DFit,
]

implemented_fit_dic = {}
for fit in implemented_fit:
    implemented_fit_dic[fit().name] = fit
