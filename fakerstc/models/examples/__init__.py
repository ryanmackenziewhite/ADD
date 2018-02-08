#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ryan Mackenzie White <ryan.white4@canada.ca>
#
# Distributed under terms of the  license.

"""
Data model is a nested dictionary

model = {CustomProviders: 
            {Provider: Optional Pdf}
         Pdfs:
            {Pdf: Optional list of fakes used}
         MetaData:
            {fake: args}
        }
"""
from collections import OrderedDict
import unittest

from ..model import Model
from ..model import OrderedModel


class SampleModelA(Model):
    def __init__(self):
        meta = {'Providers': [],
                'Fakers': {'name': None,
                           'ean': 13}
                }
        super(SampleModelA, self).__init__(meta)


class CustomModel(Model):
    def __init__(self):
        '''
        Here we can set the pdf
        pass to the provider 
        as an argument
        '''
        meta = {'Providers': {'foo': ['FooProvider'],
                              'glm': ['GLMProvider']},
                'Fakers': {'name': None,
                           'ean': 13,
                           'foo': None,
                           'glm': {'Fakers': ['random_int', 'random_int'],
                                   'Parameters': [10, 0.1, 100, 1] 
                                   }
                           },
                'Pdfs': None
                }
        
        super(CustomModel, self).__init__(meta)


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
