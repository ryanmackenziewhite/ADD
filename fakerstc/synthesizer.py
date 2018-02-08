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

from config import PROVIDERS
from holder import Holder
from faker import Faker
from writer import Writer


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
    
    def __init__(self, model, local):
        '''
        requires class model name
        '''
        self.holder = Holder(model)
        self.fake = Faker(local)
        self.add_providers()
    
    def set_seed(self, seed):
        self.fake.seed(seed)

    def add_providers(self):
        '''
        Add custom providers
        '''
        klasses = [provider.Provider for provider in PROVIDERS]
        for k in klasses: 
            self.fake.add_provider(k)

    def generate(self):
        fakers = self.holder.fakers()
        darr = []
        for fname in fakers:
            parms = self.holder.parameters(fname)
            fake = None
            try:
                fake = self.fake.get_formatter(self.holder.generator(fname))
            except:
                print('Cannot find fake in Faker ', fname)
            
            if parms is None:
                value = fake()
                darr.append(value)
            else:
                value = fake(parms)
                if isinstance(value, list):
                    darr.extend(value)
                else:
                    darr.append(value)
        return darr        


class TestCase(unittest.TestCase):
    def test(self):
        s = Synthesizer('TestModel', 'en_CA')
        print(s.generate())
        for _ in range(10):
            print(s.generate())
        
        s2 = Synthesizer('TestModel2', 'en_CA')
        print(s2.generate())

        #mywriter = Writer('test', s, 10000)
        #mywriter.write()

        #mywriter2 = Writer('test2', s2, 20000)
        #mywriter2.write()

        #assert mywriter2.nevents == mywriter2.eventcount


if __name__ == '__main__':
    unittest.main()
