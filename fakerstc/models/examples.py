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

from .model import Model


class SampleModelA(Model):
    def __init__(self):
        meta = {'Providers': [],
                'Fakers': {'name': None,
                           'ean': 13}
                }
        #meta = OrderedDict
        #meta['Name'] = {'Meta':(str,10),
        #                'Generator':('name',None)}
        #meta['UPC'] = {'Meta':(int,13),
        #               'Generator':('ean',13)}
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

