#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ryan Mackenzie White <ryan.white4@canada.ca>
#
# Distributed under terms of the  license.

"""
Dynamically import
module, class and instantiate 
from string
Instance of Holder contains one model
"""
import importlib


class Holder(object):
    '''
    Wrapper class to instatiate 
    user-defined model
    provides easy access to 
    Faker providers and optional arguments
    '''
    _basemod = "models"

    def __init__(self, module_name, class_name):
        '''
        Require passing the module name and class name
        ensure to throw error to fail init of Holder
        '''
        klass = None
        try:
            module_name = self._basemod + "." + module_name
            module = importlib.import_module(module_name)
            try:
                klass = getattr(module, class_name)
            except AttributeError:
                print('Class does not exist')
        except ImportError:
            print('Module does not exist')
        
        self.model = klass    
    
    @property
    def model(self):
        return self.__model
    
    @model.setter
    def model(self, ctor):
        self.__model = ctor() 
    
    def providers(self):
        ''' 
        return model dict
        '''
        return self.model.meta
