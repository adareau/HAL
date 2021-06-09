# -*- coding: utf-8 -*-
"""
Author   : Alexandre
Created  : 2021-06-09 10:21:17

Comments :
"""
import pkgutil

__all__ = []
loaded_modules = []
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    _module = loader.find_module(module_name).load_module(module_name)
    globals()[module_name] = _module
    loaded_modules.append(module_name)
