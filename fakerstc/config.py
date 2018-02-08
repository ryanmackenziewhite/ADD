#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ryan Mackenzie White <ryan.white4@canada.ca>
#
# Distributed under terms of the  license.

"""

"""
from pkgutil import iter_modules
from importlib import import_module


MODULES = [name for finder, name, 
           is_pkg in iter_modules(['providers']) if is_pkg] 
    
PROVIDERS = [import_module('providers.' + module) 
             for module in MODULES]


MODULESS = [name for finder, name, 
            is_pkg in iter_modules(['models']) if is_pkg] 

MODELS = [import_module('models.' + module) 
             for module in MODULESS]

print(MODULESS)
print(MODELS)
