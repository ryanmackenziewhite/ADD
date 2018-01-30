#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ryan Mackenzie White <ryan.white4@canada.ca>
#
# Distributed under terms of the  license.

"""
Example multivariate linear regression
"""

import logging
import pandas as pd
import numpy as np

'''
Visualization
'''

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

from scipy.stats import norm
'''
For least square fit to function
'''
import scipy.optimize as optimization
'''
Minimizer to define your own nll function
'''
from scipy.optimize import minimize
import scipy.stats as stats
import statsmodels.api as sm

from scipy.optimize import curve_fit

def createplot(ax, xObs, yObs, xFit, yFit, size="20%", pad=0):
    divider = make_axes_locatable(ax)
    ax2 = divider.append_axes("bottom", size=size, pad=pad)
    ax.figure.add_axes(ax2)
    ax.scatter(xObs, yObs)
    ax.scatter(xFit, yFit, color='red')
    diff = (yObs - yFit)
    ax2.plot(xFit, diff, color="crimson")
    ax.set_xticks([])

def residual():
    #Data
    x = np.arange(1,10,0.2)
    ynoise = x*np.random.rand(len(x)) 
    #Noise; noise is scaled by x, in order to it be noticable on a x-squared function
    ydata = x**2 + ynoise #Noisy data

    #Model
    Fofx = lambda x, a, b, c: a*x**2+b*x+c
    #Best fit parameters
    p, cov = curve_fit(Fofx, x, ydata)

    #PLOT
    fig1 = plt.figure(1)
    #Plot Data-model
    frame1=fig1.add_axes((.1,.3,.8,.6))
    #xstart, ystart, xend, yend [units are fraction of the image frame, from bottom left corner]
    frame1.plot(x,ydata,'.b') #Noisy data
    frame1.plot(x,Fofx(x,*p),'-r') #Best fit model
    frame1.set_xticklabels([]) #Remove x-tic labels for the first frame
    frame1.grid()


    #Residual plot
    difference = Fofx(x, *p) - ydata
    frame2=fig1.add_axes((.1,.1,.8,.2))        
    frame2.plot(x,difference,'or')
    frame2.grid()
    fig1.savefig('residual.eps', format='eps')


def glm_gen(beta):
    '''
    Accept/Reject glm generation
    
    P(y,x) = normal()
    while(i<n):
        
        #y_max = norm.pdf(mu,mu,sigma)
        x = np.random.uniform(-1,1)
        y_max=norm.pdf(mu,mu,sigma)
        y = np.random.uniform(0,y_max)
        yp = norm.pdf(x, mu, sigma)
        p_accept = y/y_max
        accept = np.random.rand() < p_accept    
        if(y<yp):
            i+=1
            vals.append(x)
            #print(i,x,y,y_max,p_accept)
    return vals    
    
    y(x) = beta.X + C
    '''
    x = np.random.uniform(0, 10)
    X = np.array([x, x**2, 1.])
    Xmax = np.array([10, 100, 1])
    Xmin = np.array([0, 0, 1.])
     
    mu = np.dot(X, beta[:-1])
    ymin = np.dot(Xmin, beta[:-1])
    ymax = np.dot(Xmax, beta[:-1])
    y = np.random.uniform(ymin, ymax)
    print(y, mu)
    sigma = beta[-1]
    pdf = norm.pdf(y, mu, sigma)
    pdf_max = norm.pdf(mu, mu, sigma) 
    #print(y, ymax, pdf, pdf_max)
    throw = np.random.uniform(0, pdf_max)
     
    values = np.array([y, x, x**2])
    if(throw < pdf):
        print(y)
        return values
    else:
        return None

    #xfit = np.random.rand(100, 2)
    #Xfit = np.column_stack((xfit, c))
    #beta = np.array([1, 0.1, 10])
    #efit = np.random.normal(loc=0., scale=results.x[-1], size=100)
    #y_fit = np.dot(Xfit, beta) + efit

    


def ols():
    nsample = 100
    #x = np.linspace(0, 10, 100)
    #X = np.column_stack((x, x**2))
    X = np.random.rand(100,2)
    beta = np.array([1, 0.1, 10])
    e = np.random.normal(size=nsample)
    X = sm.add_constant(X,prepend=False)
    y = np.dot(X, beta) + e
    model = sm.OLS(y, X)
    results = model.fit()
    print(results.summary())
    print(*results.params)
    
    y_fit = np.dot(X, (results.params))
    # Create a plot of our work, showing both the data and the fit.
    fig, ax = plt.subplots(2, 2)
    fig.subplots_adjust(hspace=0.3)

    
    ax[0, 0].scatter(X[:,[0]], y)
    ax[0, 0].scatter(X[:,[0]], y_fit, color='red')
    
    ax[0, 0].set_xlabel(r'$x$')
    ax[0, 0].set_ylabel(r'$f(x)$')
    
    ax[0, 1].scatter(X[:,[1]], y)
    ax[0, 1].scatter(X[:,[1]], y_fit, color='red')
    
    ax[1,0].hist(y,10,range=[min(y),max(y)])
    ax[1,0].hist(y_fit,10, range=[min(y),max(y)],color='red',lw=2)
    
    ax[0, 0].set_xlabel(r'$x$')
    ax[0, 0].set_ylabel(r'$f(x)$')
    fig.savefig('junk_ols.eps', format='eps')

def nll():
    print('Unbinned GLM NLL fit')

    x = np.linspace(0, 10, 100)
    #x = np.random.rand(100,2)
    c = np.ones(100)
    X = np.column_stack((x, x**2, c))
    
    #X = np.column_stack((x1, x2,  c))
    beta = np.array([1, 0.1, 10])
    
    e = np.random.normal(size=100)
    yObs = np.dot(X, beta) + e
    
    # Define the likelihood function where params is a list of initial parameter estimates
    def regressLL(params):
        yPred = np.dot(X, params[:-1]) 

        # Calculate the negative log-likelihood as the negative sum of the log of a normal
        # PDF where the observed values are normally distributed around the mean (yPred)
        # with a standard deviation of sd
        logLik = -np.sum(stats.norm.logpdf(yObs, loc=yPred, scale=params[-1]))
        # Tell the function to return the NLL (this is what will be minimized)
        return(logLik)

    # Make a list of initial parameter guesses (b0, b1, sd)    
    initParams = [1, 1, 1, 1]

    # Run the minimizer
    results = minimize(regressLL, initParams, method='nelder-mead')

    # Print the results. They should be really close to your actual values
    print(results.x, results.fun)
    
    # Here I would like to generate toy MC via accept/reject sampling
    y_fit = np.dot(X, results.x[:-1]) 
    
    
    y_gen = np.zeros([100,3])
    nEvts = 100
    trials = 0
    accept = 0

    while(accept < nEvts):
        gen = glm_gen(results.x)
        if(gen is not None):
            y_gen[accept] = gen
            print(y_gen[accept], gen)
            accept += 1
        trials += 1

    print(trials,accept)

    # Generate toy dataset with transformation, include the normal distribution
    # to illustrate the fit of sample error
    #xfit = np.random.rand(100, 2)
    #Xfit = np.column_stack((xfit, c))
    #beta = np.array([1, 0.1, 10])
    #efit = np.random.normal(loc=0., scale=results.x[-1], size=100)
    #y_fit = np.dot(Xfit, beta) + efit
    
    # Create a plot of our work, showing both the data and the fit.
    fig, ax = plt.subplots(2, 2)
    
    for i in range(ax.shape[0]):
        for j in range(ax.shape[1]):
            createplot(ax[i, j], X[:, [0]], yObs, X[:, [0]], y_fit)
    fig.savefig('junk_glm.eps', format='eps')   
    
    fig1,ax1 = plt.subplots(2,2)

    ax1[0,0].hist(yObs,10,range=[min(yObs),max(yObs)])
    ax1[0,0].hist(y_fit,10, range=[min(yObs),max(yObs)],color='red',lw=2)

    ax1[0,1].hist(y_gen[:,[0]],10,range=[min(y_gen[:,[0]]),max(y_gen[:,[0]])])
    ax1[1, 0].scatter(y_gen[:, [1]], y_gen[:,[0]])
    fig1.savefig('junk_normal.eps',format='eps')
    '''
    figd.subplots_adjust(hspace=0.3)
    ax[0, 0].scatter(X[:, [0]], yObs)
    ax[0, 0].scatter(X[:, [0]], y_fit, color='red')
    
    ax[0, 1].scatter(X[:, [1]], yObs)
    ax[0, 1].scatter(X[:, [1]], y_fit, color='red')

    
    ax[0, 0].set_xlabel(r'$x$')
    ax[0, 0].set_ylabel(r'$f(x)$')
    '''

    
    fig2, ax2 = plt.subplots(2, 2)
    
    for i in range(ax.shape[0]):
        for j in range(ax.shape[1]):
            createplot(ax2[i, j], X[:, [0]], yObs, y_gen[:,[1]], y_gen[:, [0]])
    fig2.savefig('junk_glm_gen.eps', format='eps')
    print('Done fit custom function Normal GLM unbinned NLL')


def main():
    logging.basicConfig(level=logging.DEBUG)
    residual()
    ols()
    nll()

if __name__ == '__main__':
    main()
