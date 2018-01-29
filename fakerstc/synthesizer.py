#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ryan Mackenzie White <ryan.white4@canada.ca>
#
# Distributed under terms of the  license.

"""
Generates the data using faker
"""

import unittest
import functools

from holder import Holder
from faker import Faker


class Synthesizer(object):
    '''
    Yields row of fake data
    given a metadata model
    instance of faker needs to
    be accesible to providers
    for accessing the random number generator
    Consider as a base class
    to allow for various generators
    
    e.g. generate data and insert null for imputation

    '''
    
    def __init__(self, module, model, local):
        '''
        requires class model name
        '''
        self.holder = Holder(module, model)
        self.fake = Faker(local)
    
    def add_provider(self, provider):
        '''
        Add custom providers
        '''
        pass

    def generate(self):
        providers = self.holder.providers()
        darr = []
        for fname in providers:
            parms = providers[fname]
            fake = None
            try:
                fake = functools.partial(self.fake.__getattribute__(fname))
            except:
                print('Cannot find fake in Faker')
                
            if parms is None:
                darr.append(fake())
            else:
                darr.append(fake(parms))
        return darr        


class TestCase(unittest.TestCase):
    def test(self):
        s = Synthesizer('examples', 'SampleModelA', 'en_CA')
        print(s.generate())
        for _ in range(10):
            print(s.generate())
        
        s2 = Synthesizer('examples', 'CustomModel', 'en_CA')
        print(s2.generate())


if __name__ == '__main__':
    unittest.main()
