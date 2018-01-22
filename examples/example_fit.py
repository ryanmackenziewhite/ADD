# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 08:19:17 2018
Example fitting methods to a normal distribution
@author: ryanwhi
"""

import logging

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

import numpy as np

from scipy.stats import norm
import scipy.optimize as optimization
from scipy.optimize import minimize
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.base.model import GenericLikelihoodModel


import matplotlib.pyplot as plt

def leastsq_normal(*args):
    '''
    Example fit methods
    '''
    log.info('Fit a Gaussian with scipy leastsq fit')
    mu, sigma, n = args
    log.info('mu: %f, sigma: %f, n: %i ', mu, sigma, n)
    
    s = np.random.normal(mu, sigma, n)
    mean,std=norm.fit(s)
    count, bins, ignored = plt.hist(s, 30, normed=True)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    y = norm.pdf(x, mean, std)
    plt.plot(x, y)
    plt.show()  
    log.info('Done: fit_gauss')

def curvefit_normal():
    '''
    Use scipy for arbitrary function fit
    Example found here:
    https://github.com/Ffisegydd/python-examples/blob/master/examples/scipy/fitting%20a%20gaussian%20with%20scipy%20curve_fit.py
    '''
    log.info('Fit Gaussian using curve_fit for arbitrary functions')
    
    # Start parameters
    # p_initial = [1.0, 0.0, 0.1, 0.0]
    p_initial = [0,0.1]

    # Initial perturned paramters for dataset
    p_perturbed = [i + 0.5*(np.random.rand()*2 - 1.) for i in p_initial]
    # Create random distribution for input data, including random errors
    x = np.linspace(-1, 1, 1000)
    #y = np.array([normal(i, *p_perturbed) + 0.1*(np.random.rand()*2. - 1.) for i in x])
    y = np.array([norm.pdf(i, *p_perturbed) + 0.1*(np.random.rand()*2. - 1.) for i in x])
    e = np.array([np.random.rand()*0.1 for _ in y])
    
    # Use curve fit for gaussian fit
    # Starting with initial unperturbed values
    popt, pcov = optimization.curve_fit(norm.pdf, x, y, p0=p_initial, sigma=e)
    
    # Generate y-data based on the fit.
    # Here I would like to generate toy MC via accept/reject sampling
    y_fit = norm.pdf(x, *popt)
    
    # Create a plot of our work, showing both the data and the fit.
    fig, ax = plt.subplots()
    ax.errorbar(x,y,e)
    ax.plot(x, y_fit, color = 'red')
    
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$f(x)$')
    ax.set_title('Using scipy.curve_fit to fit a normal distribution.')
    plt.show()
    log.info('Done: fit custom function Gaussian')


'''
NLL fit
https://stackoverflow.com/questions/7718034/maximum-likelihood-estimate-pseudocode
'''

def nll():
    print('Unbinned NLL fit of Gaussian')
    
    # Start parameters
    p_initial = [0.0, 0.1]
    # Initial perturned paramters for dataset
    p_perturbed = [i + 0.5*(np.random.rand()*2 - 1.) for i in p_initial]
    # Create random distribution for input data, including random errors
    x = np.random.normal(p_perturbed[0], p_perturbed[1], 1000)    
    
    # Define the likelihood function where params is a list of initial parameter estimates
    def regressLL(params):
        # Calculate the predicted values from the initial parameter guesses
        logLik = -1. * np.sum(norm.logpdf(x,*params))
        # Tell the function to return the NLL (this is what will be minimized)
        return(logLik)

    # Make a list of initial parameter guesses (b0, b1, sd)    
    initParams = p_perturbed

    # Run the minimizer
    results = minimize(regressLL, initParams, method='nelder-mead')

    # Print the results. They should be really close to your actual values
    print(results.x)
    
    # Here I would like to generate toy MC via accept/reject sampling
    x2 = np.linspace(-1, 1, 1000)
    y_fit = norm.pdf(x2, *results.x)
    
    # Create a plot of our work, showing both the data and the fit.
    fig, ax = plt.subplots()
    count, bins, ignored = plt.hist(x, 30, normed=True)
    #ax.plot(x,yObs)
    ax.plot(x2, y_fit, color = 'red')
    
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$f(x)$')
    print('Done fit custom function Gaussian unbinned NLL')
    
# stats model
# ht://rlhick.people.wm.edu/posts/estimating-custom-mle.html    
def statsmd():
    '''
    '''
def main():
    logging.basicConfig(level=logging.INFO)
    leastsq_normal(0, 0.1, 1000)
    curvefit_normal()
    nll()


if __name__ == '__main__':
    main()    