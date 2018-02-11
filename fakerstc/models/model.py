#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ryan Mackenzie White <ryan.white4@canada.ca>
#
# Distributed under terms of the  license.

"""

"""
from collections import OrderedDict
import json


class Model(object):
    '''
    Base Model class
    define properties, setters
    utilities to access the meta data
    Requires custom providers with optional pdfs

    Use nested dictionary, allows easy serialization to JSON
    '''
    def __init__(self, mdata):
        self.__meta = mdata

    @property
    def meta(self):
        return self.__meta

    @meta.setter
    def meta(self, mdata):
        self.__meta = mdata

    def provider(self, name):
        return self.meta['Providers'][name]

    def faker(self, name):
        return self.meta['Fakers'][name]


class OrderedModel(object):
    '''
    Base model class as an OrderedDict
    '''

    def __init__(self, model):
        if isinstance(model, OrderedDict):
            self._model = model
        else:
            print('Model not defined as OrderDict')

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model):
        self._model = model
    
    @property
    def config(self):
        return self.model['Model']['Configuration']

    def save_to_json(self, filename):
        with open(filename, 'w') as ofile:
            json.dump(self.meta, ofile, indent=4)

    def display_from_json(self):
        '''
        '''
        print(json.dumps(self.model, indent=4))

    def parse_from_json(self, filename):
        with open(filename, 'r') as ifile:
            data = json.loads(ifile, object_pairs_hook=OrderedDict)
            self.model = data

    def attributes(self):
        '''
        return total number of model attributes
        '''
        return len(self.config.keys())

    def schema(self):
        '''
        Names of the dataset variables
        '''
        return self.config.keys()

    def meta(self, name):
        '''
        Type information for the associated schema object
        '''
        return self.config[name]['Meta']

    def generator(self, name):
        '''
        generator name
        '''
        return self.config[name]['Generator']

    def parameters(self, name):
        '''
        Parameters to pass to generator method
        '''
        return self.config[name]['Parameters']

    def dependent(self, name):
        '''
        Checks if variable is passed to another fake for generation
        '''
        if self.config[name]['Dependent'] is None:
            return False
        else:
            return True



