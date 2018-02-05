# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 12:15:35 2018

@author: ryanwhi
"""

import unittest

from synthesizer import Synthesizer
from writer import Writer

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import statsmodels.api as sm


class TestCase(unittest.TestCase):
    def test(self):
        s = Synthesizer('examples', 'SampleModelA', 'en_CA')
        print(s.generate())
        for _ in range(10):
            print(s.generate())
        
        s2 = Synthesizer('examples', 'CustomModel', 'en_CA')
        print(s2.generate())

        #mywriter = Writer('test', s, 10000)
        #mywriter.write()

        mywriter2 = Writer('test2', s2, 1000)
        mywriter2.write()

        assert mywriter2.nevents == mywriter2.eventcount
        
        df = pd.read_csv('test2.0000.csv', header = None)
        #print(df)
        X = df.loc[:,[3,4]].values
        #print(X)
        y = df.loc[:,[5]].values
        #print(y)
        
        # Fit
        # beta = np.array([1, 0.1, 10])
        model = sm.OLS(y, X)
        results = model.fit()
        print(results.summary())
        print(*results.params)
        
        y_fit = np.dot(X, (results.params))
        #print(y_fit)
        # Create a plot of our work, showing both the data and the fit.
        fig, ax = plt.subplots(2, 2)
        fig.subplots_adjust(hspace=0.3)

    
        ax[0, 0].scatter(df.loc[:,[3]], df.loc[:,[5]])
        ax[0, 0].scatter(df.loc[:,[3]], y_fit, color='red')
    
        ax[0, 0].set_xlabel(r'$x$')
        ax[0, 0].set_ylabel(r'$f(x)$')
    
        ax[0, 1].scatter(X[:,[1]], y)
        #ax[0, 1].scatter(X[:,[1]], y_fit, color='red')
    
        miny=df.loc[:,[5]].min()
        maxy=df.loc[:,[5]].max()
        print(miny)
        print(maxy)
        #ax[1,0].hist(y,10,range=[miny,maxy])
        #ax[1,0].hist(y_fit,10, range=[miny,maxy],color='red',lw=2)
    
        #ax[0, 0].set_xlabel(r'$x$')
        #ax[0, 0].set_ylabel(r'$f(x)$')
        fig.savefig('closure.pdf', format='pdf')
        
        


if __name__ == '__main__':
    unittest.main()