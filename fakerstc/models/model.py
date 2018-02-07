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
import unittest

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
        #if isinstance(mdata, OrderedDict):
        #    self.__meta = mdata
        #else:
        #    print('Model not defined as OrderDict')

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
        return len(self.model.keys())

    def schema(self):
        '''
        Names of the dataset variables
        '''
        return self.model.keys()

    def meta(self, name):
        '''
        Type information for the associated schema object
        '''
        return self.model[name]['Meta']

    def generator(self, name):
        '''
        generator name
        '''
        return self.model[name]['Generator']

    def parameters(self, name):
        '''
        Parameters to pass to generator method
        '''
        return self.model[name]['Parameters']


class TestModel(OrderedModel):

    def __init__(self):    
        meta = OrderedDict()
        meta['Name'] = {'Meta': ['String', 10],
                        'Generator': 'name',
                        'Parameters': None}
        meta['UPC'] = {'Meta': ['Integer', 13],
                       'Generator': 'ean',
                       'Parameters': None}
        super(TestModel, self).__init__(meta)


class TestModel2(OrderedModel):        
    
    def __init__(self):
        meta = OrderedDict()
    
        meta['Name'] = {'Meta': ['String', 10],
                        'Generator': 'name',
                        'Parameters': None}

        meta['UPC'] = {'Meta': ['String', 10],
                       'Generator': 'ean',
                       'Parameters': 13}
    
        meta['Foo'] = {'Meta': ['Integer', 10],
                       'Generator': 'foo',
                       'Parameters': None}
    
        meta['Prediction'] = {'Meta': ['Float', None],
                              'Generator': 'glm',
                              'Parameters': {'Fakers': ['random_int', 'random_int'],
                                             'Parameters': [10, 0.1, 100, 1]
                                             }
                              }
        super(TestModel2, self).__init__(meta)

    
class TestCase(unittest.TestCase):
    def test(self):
        model = TestModel()
        print(model.attributes())
        print(model.schema())
        for key in model.schema():
            print(model.generator(key))
            print(model.parameters(key))
        
        model.display_from_json()


if __name__ == '__main__':
    unittest.main()
