#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ryan Mackenzie White <ryan.white4@canada.ca>
#
# Distributed under terms of the  license.

"""
General linear model to add linear dependence between a predictor and set of 
independent random variables
"""
import functools

from faker.providers import BaseProvider
import numpy as np


class Provider(BaseProvider):
    '''
    Simple General Linear Model with noise
    '''
    def sample(self, X, beta, sigma):
        '''
        Sample from a normal distribution with
        width defined as sigma
        mean defined as a GLM 
        y(X) = beta.X
        otherwise, one can simply use the transformation
        y(X) = beta.X + sigma
        i.e. the mean of the predictor is a linear combination
        of independent variables, where the predictor follows a normal
        distribution, i.e. link function is normal. 
        This can be extended to logistic function, for example,
        where the predictor is either 0 or 1 with a logit link function.

        How to get the maximum of a faker? Need to scan the phase space?
        I need to get ymin and ymax to sample from y, X.

        For now, just implement as y(X), ok this is equivalent
        as below.
        Xmin = min(X)
        Xmax = max(X)
        mu = np.dot(X,beta)
        ymin = np.dot(Xmin,beta)
        ymax = np.dot(Xmax,beta)
        pdfmax = stats.norm.pdf(mu, mu, sigma)

        y = np.random.uniform(ymin,ymax)
        throw = np.random.uniform(0,pdfmax)
        if(throw < y):
            accept!!!
        
        Should the scale go as 1/sqrt(sample size)?
        '''
        y = np.dot(np.asarray(X), beta) + self.generator.random.gauss(0., sigma)
        return y

    def glm(self, params):
        '''
        expect a dictionary
        '''
        fields = params['Fakers']
        beta = params['Parameters'][:-1]
        sigma = params['Parameters'][-1]
        ndof = len(params['Parameters']) 
        X = np.ones(ndof)
        fakers = []
        for counter, f in enumerate(fields):
            fake = None
            try:
                fake = self.generator.get_formatter(f)
            except:
                print('Cannot find fake in Faker')
            X[counter] = fake()
            fakers.append(X[counter])
        fakers.append(self.sample(X[:-1], beta, sigma))

        return fakers

