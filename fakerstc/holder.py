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
from config import MODELS


class Holder(object):
    '''
    Wrapper class to instatiate 
    user-defined model
    provides easy access to 
    Faker providers and optional arguments
    '''

    def __init__(self, class_name):
        '''
        Require passing the module name and class name
        ensure to throw error to fail init of Holder
        '''
        klass = None
        for module in MODELS:
            klasses = [key for key in dir(module) 
                       if isinstance(getattr(module, key), type)]
            if class_name in klasses:
                klass = getattr(module, class_name)
                continue
        if klass is None:
            print('Cannot find model ', class_name)
        else:
            print('Added Model ', class_name) 
            self.model = klass    
    
    @property
    def model(self):
        return self.__model
    
    @model.setter
    def model(self, ctor):
        self.__model = ctor() 
    
    def providers(self):
        ''' 
        return model metadata dict
        '''
        return self.model.meta['Providers']

    def fakers(self):
        '''
        return model provider list
        '''
        return self.model.schema()

    def generator(self, name):
        return self.model.generator(name)

    def parameters(self, name):
        return self.model.parameters(name)

