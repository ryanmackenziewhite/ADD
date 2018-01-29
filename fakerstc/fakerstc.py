# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 12:24:32 2018

@author: ryanwhi
"""

import logging
import unittest
import argparse
import json
import functools

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

from faker.providers import BaseProvider
from faker import Faker

# Use functools.partial
# https://stackoverflow.com/questions/29832410/python-use-dictionary-keys-as-function-names

class ModelType(object):
    '''
    Base Model class
    provides all the required functions 
    needed for accessing properties
    of the model
    '''
    
    def __init__(self,mdata):
        self.__meta = mdata
    
    @property
    def meta(self):
        return self.__meta
    
    @meta.setter
    def meta(self,mdata):
        self.__meta = mdata
        
    def provider(self,name):
        return self.meta[name]
                 

                        
class MetaModel(object):
    '''
    Wrapper class to instatiate 
    user-defined model
    provides easy access to 
    Faker providers and optional arguments
    '''
    def __init__(self,name):
        self.model = globals()[name]
    
    @property
    def model(self):
        return self.__model
    
    @model.setter
    def model(self,ctor):
        self.__model = ctor() 
    
    def providers(self):
        ''' 
        return model dict
        '''
        return self.model.meta


class MyModel(ModelType):
    '''
    User-defined model
    Define a dictionary
    with the Faker provider (or custom provider)
    
    optional arguments
    
    @TODO
    add the header information for column names
    '''    
    def __init__(self):
        meta = {'name':None,
                     'ean':13}
        super(MyModel,self).__init__(meta)
        
class AltModel(ModelType):
    
    def __init__(self):
        meta = {'name':None,
                'address':None,
                'longitude':None,
                'iban':None,
                'credit_card_full':'visa16'
                }
        super(AltModel,self).__init__(meta)
        
def fakerstc(*args):
    
    mymodel = MetaModel(args[0])
    
    print(mymodel.model.meta)
    print(mymodel.providers())
    print(mymodel.model.provider('name')) 
    
    fake = Faker('en_CA')
    
    for _ in range(args[1]):
        row=[]
        for key in mymodel.providers():
            parms=mymodel.providers()[key]
            if parms is None:
                row.append(functools.partial(fake.__getattribute__(key))())
            else:
                row.append(functools.partial(fake.__getattribute__(key))(parms)) 
        print(row)   
    
    
if __name__ == '__main__':
    fakerstc('MyModel',10)
    fakerstc('AltModel',10)        