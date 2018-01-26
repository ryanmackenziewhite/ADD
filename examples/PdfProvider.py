# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 09:05:29 2018

@author: ryanwhi
"""
import logging
import unittest

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

from faker.providers import BaseProvider
from faker import Faker
from scipy.stats import norm
import numpy as np

class PdfProvider(BaseProvider):
    '''
    pass arbitrary Pdf for accept/reject sampling
    Requieres caching maximum pdf value
    may require scan of pdf space to find maximum
    Probably requires a seperate pdf class
    which holds the required pdf information
    easy wrapper to any function
    
    Allow for updating parameters
    and rescanning the phase space
    
    Allow updating the phase space (xmin,xmax)
    
    Extend to arbitrary number of dimensions
    e.g., sample from 5D model!!!
    
    '''
    
    def __init__(self,generator,pdf,*args):
        self.xmin=args[0]
        self.xmax=args[1]
        self._parms=args[2:]
        self._pdf=pdf
        self.ntrials=0
        self.naccept=0
        self.ymax=0
        self.scan()
        super(PdfProvider,self).__init__(generator)
    
    @property
    def xmin(self):
        '''
        '''
        return self.__xmin
    
    @xmin.setter
    def xmin(self,x):
        '''
        '''
        self.__xmin = x
        
    @property
    def xmax(self):
        '''
        '''
        return self.__xmax
    
    @xmax.setter
    def xmax(self,x):
        '''
        '''
        self.__xmax = x
    
    @property
    def ymax(self):
        '''
        '''
        return self.__ymax
        
    @ymax.setter
    def ymax(self,y):
        '''
        '''
        self.__ymax = y
        
    @property
    def ntrials(self):
        '''
        '''
        return self.__ntrials
    
    @property
    def naccept(self):
        '''
        '''
        return self.__naccept
    
    @ntrials.setter
    def ntrials(self,count):
        '''
        '''
        if(count == 0):
            self.__ntrials = 0
        elif(count == 1):
            self.__ntrials += 1
        else:
            log.error('Cannot increment counter')
    
    @naccept.setter
    def naccept(self,count):
        '''
        '''
        if(count == 0):
            self.__naccept = 0
        elif(count == 1):
            self.__naccept += 1
        else:
            log.error('Cannot increment counter')
        
    
    def sample(self):
        '''
        return the sampled value (after accept)
        clearly, not optimzed solution
        but this is so easy
        update to use faker random
        '''
        x = np.random.uniform(self.xmin,self.xmax)        
        y = np.random.uniform(0,self.ymax)
        yp = self._pdf(x,*self._parms)
        self.ntrials = 1
        if(y<yp):
            self.naccept = 1
            return x
        else:
            return self.sample()
           
        
    def scan(self):
        '''
        Find maximum value of pdf
        '''
        xvals=np.linspace(self.xmin,self.xmax,1000)
        yvals=self._pdf(xvals,*self._parms)
        ymax=max(yvals)
        if(ymax>self.ymax):
            self.ymax = ymax

class Provider(BaseProvider):
    def upc_code(self):
        return self.generator.random.randint(0,999999999)
                       
class TestCase(unittest.TestCase):
    def test(self):
    
        def myfcn(x,*args):
            '''
            Normal pdf
            '''
            mu, sigma = args
            return norm.pdf(x,mu,sigma)
    
        modelargs=[-1,1,0,0.1]
        fake = Faker()
    
        provider = PdfProvider(fake,myfcn,*modelargs)
        print(provider.xmin,provider.xmax,provider.ymax)
        fake.add_provider(provider)
        print(fake.sample(),provider.naccept,provider.ntrials)
        
        fake.add_provider(Provider(fake))
        print(fake.upc_code())
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
    unittest.main()
        
        