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
        config = OrderedDict()
    
        model = OrderedDict()
        
        model['Model'] = OrderedDict({'Name': 'TestModel',
                                      'Description': 'Testing Purposes',
                                      'Configuration': config} 
                                     )

        model['Client'] = {'Name': 'FooBar Enterprises'}
        
        model['Taxonomy'] = {}

        config['Name'] = {'Meta': ['String', 10],
                          'Generator': 'name',
                          'Parameters': None,
                          'Dependent': None}

        config['UPC'] = {'Meta': ['Integer', 13],
                         'Generator': 'ean',
                         'Parameters': None,
                         'Dependent': None
                         }

        super(TestModel, self).__init__(model)


class TestModel2(OrderedModel):        
    
    def __init__(self):
        config = OrderedDict()
    
        model = OrderedDict()
        
        model['Model'] = OrderedDict({'Name': 'TestModel2',
                                      'Description': 'Testing Purposes',
                                      'Configuration': config} 
                                     )

        model['Client'] = {'Name': 'FooBar Enterprises'}
        
        model['Taxonomy'] = {}
    
        config['Name'] = {'Meta': ['String', 10],
                          'Generator': 'name',
                          'Parameters': None,
                          'Dependent': None}

        config['UPC'] = {'Meta': ['String', 10],
                         'Generator': 'ean',
                         'Parameters': 13,
                         'Dependent': None}
    
        config['Foo'] = {'Meta': ['Integer', 10],
                         'Generator': 'foo',
                         'Parameters': None,
                         'Dependent': None}
    
        config['Prediction'] = {'Meta': ['Float', None],
                                'Generator': 'glm',
                                'Parameters': {'Fakers': ['random_int', 'random_int'],
                                               'Parameters': [10, 0.1, 100, 1]
                                               },
                                'Dependent': None
                              }
        super(TestModel2, self).__init__(model)

    
class EvolveModel(OrderedModel):        
    '''
    Model info required for generator:
    Dataset variables must be generated in
    order defined in header, e.g. as an OrderedDict
    Requires:
        Variable Name
        Variable Type and Length (required for DQ/schema check)
        Generator name
        Arguments to pass to generator (i.e. the method in the Provider class)
        Dependence on another variable, allow to generate a list of values within phase space
    Metadata information:
        Model name, i.e. class name 
        Related real dataset information (e.g. modeling Tax Data)
        Taxonomy information

    '''
    def __init__(self):
        config = OrderedDict()
    
        model = OrderedDict()
        
        model['Model'] = OrderedDict({'Name': 'EvolveModel',
                                      'Description': 'Testing Purposes',
                                      'Configuration': config} 
                                     )

        model['Client'] = {'Name': 'FooBar Enterprises'}
        
        model['Taxonomy'] = {}
        
        config['Name'] = {'Meta': ['String', 10],
                          'Generator': 'name',
                          'Parameters': None,
                          'Dependent': None}

        config['UPC'] = {'Meta': ['String', 10],
                         'Generator': 'ean',
                         'Parameters': 13,
                         'Dependent': None}
    
        config['Foo'] = {'Meta': ['Integer', 10],
                         'Generator': 'foo',
                         'Parameters': None,
                         'Dependent': None}
    
        config['Value1'] = {'Meta': ['Integer', 10],
                            'Generator': 'random_int',
                            'Parameters': None,
                            'Dependent': 'Prediction'}

        config['Value2'] = {'Meta': ['Integer', 10],
                            'Generator': 'random_int',
                            'Parameters': None,
                            'Dependent': 'Prediction'}
        
        config['Prediction'] = {'Meta': ['Float', None],
                                'Generator': 'glm',
                                'Parameters': {'Variables': [config['Value1'], 
                                                             config['Value2']],
                                               'Parameters': [10, 0.1, 100, 1]
                                               },
                                'Dependent': None
                                }
        
        super(EvolveModel, self).__init__(model)


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
