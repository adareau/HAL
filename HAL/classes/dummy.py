# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-04-07 14:55:56

Comments : dummy class to test imports
"""
# %% IMPORTS

# -- global
import sys


# %% CLASS DEFINITION
class Dummy(object):
    """docstring for Dummy"""

    def __init__(self):
        super(Dummy, self).__init__()
        self.name = "foobar"


# %% TEST
if __name__ == "__main__":
    print(sys.path)
    dummy = Dummy()
    print(dummy.name)
