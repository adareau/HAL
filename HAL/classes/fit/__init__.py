# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-07 14:33:19
Modified : 2021-05-05 15:23:30

Comments :
"""

from HAL.classes.fit.gauss2D import Gauss2DFit
from HAL.classes.fit.statsOnly2D import StatsOnly2D
from HAL.classes.fit.thomasfermi2D import ThomasFermi2DFit

implemented_fit = [
    Gauss2DFit, StatsOnly2D, ThomasFermi2DFit
]

implemented_fit_dic = {}
for fit in implemented_fit:
    implemented_fit_dic[fit().name] = fit
