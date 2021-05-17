# -*- coding: utf-8 -*-
'''
Author   : Alexandre
Created  : 2021-05-17 13:47:49
Modified : 2021-05-17 14:01:24

Comments :
'''

from matplotlib import cm
cmap = cm.get_cmap('Pastel1')
cmap._init()
clist = cmap._lut[:-1]
n = len(clist)



def gimmeColor(i=0):
    """returns a color from the defined color cycle"""
    # TODO : allow the user to define the color cycle ?
    # -- get the colormap from matplotlib
    cmap = cm.get_cmap("Pastel1")
    cmap._init()
    clist = cmap._lut[:-1]

    # -- get color
    color = clist[i % len(clist)]
    color_RGB = color[:-1] * 255
    out = tuple([int(c) for c in color_RGB])

    return tuple(color_RGB)


for i in range(20):
    print(tuple(gimmeColor(i)))