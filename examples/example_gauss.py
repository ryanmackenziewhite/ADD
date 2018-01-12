# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import logging
from faker import Faker
import pandas as pd
import numpy as np

'''
Visualization
'''

import matplotlib.pyplot as plt
import seaborn as sns
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
'''
Minuit and models in python
something close to RooFit in python
https://probfit.readthedocs.io/en/latest/
fails to install properly
'''
#from iminuit import Minuit
#from probfit import UnbinnedLH, gaussian


import time
import random

'''
MCMC
'''
import pymc3 as pm


log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())

'''
Example code based on a normal distribution
Explore ways to define a function and plot
Generate data based on a pdf
Fit data using least squares, nll, scikit, etc...
Fit data using MCMC rather than NLL/least squares
Combine MC generation from pdf with faker
'''

class PseudoGenerator(object):
    '''
    Synthetic data generator wrapper class
    Default generator is faker
    Requires a schema to be defined
    Schema properties will be mapped to 
    Faker methods, e.g. "name":fake.name()
    Generates a row of data based on the schema
    '''
    def __init__(self, schema):
        self.fake = Faker()
        self.schema = schema
        self.row = []
    def generate(self):
        '''
        generate a row of fake data

        '''
def gaussian(data,mu,sigma):
    '''
    Define Gaussian normal distribution
    for examples on fitting and MC
    '''
    if(sigma <= 0.):
        return 999.
    g = 1/(sigma * np.sqrt(2*np.pi)) * np.exp(- (data - mu)**2/(2*sigma**2) )
    return g



def sample(mu,sigma,n):
    '''
    Requires the probility distribution function
    i.e. P(x_i)=f(x_i)/integral(f(x))
    such that integral(f(x)) = 1
    the pdf for normal distribution is
    g = 1/(sigma * np.sqrt(2*np.pi)) * np.exp(- (data - mu)**2/(2*sigma**2) )
    
    To use accept/reject, need to have
    
    random < P(x_i)/P(x)_max
    
    brain freeze --- simple accept/reject is fubar
    
    draw x' from xmin to xmax
    draw y' from 0 to pdf(xmax)
    if y' < pdf(x')
    accept x'
    what gives below?
    '''
    i=0
    vals=[]
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

def plot_sample():
    '''
    Demonstrate accept/reject method with Gaussian
    '''
    print('Test Plot a Gaussian distribution')
    mu, sigma = 0.,0.1
    s = sample(mu,sigma,1000)
    print(abs(mu - np.mean(s)) < 0.01)
    print(abs(sigma - np.std(s, ddof=1)) < 0.01)
    
    count, bins, ignored = plt.hist(s, 30, normed=True)
    #plt.plot(bins, gaussian(bins,mu,sigma), linewidth=2, color='r')
    print('Done: plot_sample')
    
    
def plot_gauss():
    '''
    Use numpy to sample from norm
    '''
    print('Test Plot a Gaussian distribution')
    mu, sigma = 0.,0.1
    s = np.random.normal(mu,sigma,1000)
    print(abs(mu - np.mean(s)) < 0.01)
    print(abs(sigma - np.std(s, ddof=1)) < 0.01)
    
    count, bins, ignored = plt.hist(s, 30, normed=True)
    plt.plot(bins, gaussian(bins,mu,sigma), linewidth=2, color='r')
    print('Done: plot_gauss')
    
def fit_gauss():
    '''
    Example fit methods
    '''
    print('Fit a Gaussian with scipy fit using leastsq of histogram')
    mu, sigma= 0., 0.1
    s = np.random.normal(mu, sigma, 1000)
    mean,std=norm.fit(s)
    count, bins, ignored = plt.hist(s, 30, normed=True)
    xmin, xmax = plt.xlim()
    x = np.linspace(xmin, xmax, 100)
    y = norm.pdf(x, mean, std)
    plt.plot(x, y)
    plt.show()  
    print('Done: fit_gauss')
    
def fit_custom():
    '''
    Use scipy for arbitrary function fit
    Example found here:
    https://github.com/Ffisegydd/python-examples/blob/master/examples/scipy/fitting%20a%20gaussian%20with%20scipy%20curve_fit.py
    '''
    print('Fit Gaussian using curve_fit for arbitrary functions')
    def gauss(x,*p):
        a, b, c, d = p
        y = a*np.exp(-np.power((x - b), 2.)/(2. * c**2.)) + d
        return y
    # Start parameters
    p_initial = [1.0, 0.0, 0.1, 0.0]
    # Initial perturned paramters for dataset
    p_perturbed = [i + 0.5*(random.random()*2 - 1.) for i in p_initial]
    # Create random distribution for input data, including random errors
    x = np.linspace(-1, 1, 1000)
    y = np.array([gauss(i, *p_perturbed) + 0.1*(random.random()*2. - 1.) for i in x])
    e = np.array([random.random()*0.1 for _ in y])
    
    # Use curve fit for gaussian fit
    # Starting with initial unperturbed values
    popt, pcov = optimization.curve_fit(gauss, x, y, p0=p_initial, sigma=e)
    
    # Generate y-data based on the fit.
    # Here I would like to generate toy MC via accept/reject sampling
    y_fit = gauss(x, *popt)
    
    # Create a plot of our work, showing both the data and the fit.
    fig, ax = plt.subplots()
    ax.errorbar(x,y,e)
    ax.plot(x, y_fit, color = 'red')
    
    ax.set_xlabel(r'$x$')
    ax.set_ylabel(r'$f(x)$')
    ax.set_title('Using scipy.curve_fit to fit a normal distribution.')
    plt.show()
    print('Done: fit custom function Gaussian')
    
        
'''
NLL fit
https://stackoverflow.com/questions/7718034/maximum-likelihood-estimate-pseudocode
'''
def nll():
    print('Unbinned NLL fit of Gaussian')
    def gauss(x,*p):
        a, b, c, d = p
        y = a*np.exp(-np.power((x - b), 2.)/(2. * c**2.)) + d
        return y
    
    # Start parameters
    p_initial = [1.0, 0.0, 0.1, 0.0]
    # Initial perturned paramters for dataset
    p_perturbed = [i + 0.5*(random.random()*2 - 1.) for i in p_initial]
    # Create random distribution for input data, including random errors
    x = np.linspace(-1, 1, 1000)
    yObs = np.array([gauss(i, *p_perturbed) + 0.1*(random.random()*2. - 1.) for i in x])
    e = np.array([random.random()*0.1 for _ in yObs])
    
    # Set up your x values
    #x = np.linspace(0, 100, num=100)

    # Set up your observed y values with a known slope (2.4), intercept (5), and sd (4)
    #yObs = 5 + 2.4*x + np.random.normal(0, 4, 100)

    # Define the likelihood function where params is a list of initial parameter estimates
    def regressLL(params):
        # Resave the initial parameter guesses
        #b0 = params[0]
        #b1 = params[1]
        #sd = params[2]

        # Calculate the predicted values from the initial parameter guesses
        #yPred = b0 + b1*x
        yPred = np.log(gauss(x,*params))

        # Calculate the negative log-likelihood as the negative sum of the log of a normal
        # PDF where the observed values are normally distributed around the mean (yPred)
        # with a standard deviation of sd
        #logLik = -np.sum( stats.norm.logpdf(yObs, loc=yPred, scale=sd) )
        logLik = -np.sum( stats.norm.logpdf(yObs, loc=yPred) )
        #logLik = -np.sum(yPred)

        # Tell the function to return the NLL (this is what will be minimized)
        return(logLik)

    # Make a list of initial parameter guesses (b0, b1, sd)    
    #initParams = [1, 1, 1]
    initParams = p_perturbed

    # Run the minimizer
    results = minimize(regressLL, initParams, method='nelder-mead')

    # Print the results. They should be really close to your actual values
    print(results.x)
    
    # Here I would like to generate toy MC via accept/reject sampling
    y_fit = gauss(x, *results.x)
    
    # Create a plot of our work, showing both the data and the fit.
    fig, ax = plt.subplots()
    ax.plot(x,yObs)
    ax.plot(x, y_fit, color = 'red')
    
    #ax.set_xlabel(r'$x$')
    #ax.set_ylabel(r'$f(x)$')
    print('Done fit custom function Gaussian unbinned NLL')
    

'''
Sampling methods for MC
'''

def pyMCMC():
    '''
    http://twiecki.github.io/blog/2015/11/10/mcmc-sampling/
    requires theano which can only be installed 
    '''
    #    import pymc3 as pm
    print('Use pymc3 MCMC for fitting Gaussian')
    mu, sigma = 0.,0.1
    data = np.random.normal(mu,sigma,1000)
    
    with pm.Model():
        mu = pm.Normal('mu', 0, 1)
        sigma = 1.
        returns = pm.Normal('returns', mu=mu, sd=sigma, observed=data)
    
        step = pm.Metropolis()
        trace = pm.sample(3000, step)
    
    sns.distplot(trace[2000:]['mu'], label='PyMC3 sampler');
    #sns.distplot(posterior[500:], label='Hand-written sampler');
    #plt.legend();
    print('Done: pyMCMC')

from faker.providers import BaseProvider

class NormalProvider(BaseProvider):
    
    '''
    Create a provider instance which samples from a normal.
    Requires a call_back to continue sampling until accept.
    Currently Provider returns NaN, call_back not functioning
    call_back fixed, need to return self.call_back()
    '''
    
    y_max=norm.pdf(0.,0.,0.1)
    
    def faker_sampler(self):
        x = self.generator.random.uniform(-1,1)        
        y = self.generator.random.uniform(0,self.y_max)
        yp = norm.pdf(x, 0., 0.1)
        #if(y>yp):
        #    self.faker_sampler()
        #return x    
        if(y<yp):
            return x
        else:
            return None
        
    def smplnorm(self):
        #return self.faker_sampler()
        g = self.faker_sampler()
        
        if(g):
            return float("{0:.2f}".format(g))
        else:
            return self.smplnorm()
        #if(g is None):
        #    print('g is None')
        #    self.smplnorm()
        #else:
        #    print('g is accepted')
        #    return float("{0:.2f}".format(g))
            
def fakertest(n=10):   
    print('Testing Faker')
    # Uses python random module
    # https://docs.python.org/3.6/library/random.html
    fake = Faker()
    fake.add_provider(NormalProvider)
    #print(fake.smplnorm())
    #return
    schema = {'var1':[],
              'var2':[],
              'var3':[]}
    # instance of the random number generator    
    rndm = fake.random
    y_max=norm.pdf(0.,0.,0.1)
    
    def faker_sampler():
        x = rndm.uniform(-1,1)        
        y = rndm.uniform(0,y_max)
        yp = norm.pdf(x, 0., 0.1)
        if(y<yp):
            return x
        else:
            return None
    # returns object of current state
    # rndm.getstate()
    #print(fake.address())
    for _ in range(n):
       schema['var1'].append(fake.smplnorm())
       schema['var2'].append(fake.name())
       schema['var3'].append(fake.ssn()) 
    #i=0
    #while(i<n):
        #g = faker_sampler()
        #if g:
            #print(g)
            #print(fake.name())
            #print(fake.ssn())
            #g = float("{0:.2f}".format(x))
            #schema['var1'].append(g)
            #schema['var1'].append(float("{0:.2f}".format(g)))
            #schema['var1'].append(fake.smplnorm())
            #schema['var2'].append(fake.name())
            #schema['var3'].append(fake.ssn())
            #i += 1
            
    # Create the df from dictionary 
    df = pd.DataFrame(schema)
    print(df)
    plt.figure()
    df['var1'].plot.hist()
    #count, bins, ignored = plt.hist(s, 30, normed=True)    

def main():
    logging.basicConfig(level=logging.DEBUG)
    fakertest(1000)
    #plot_sample()
    #plot_gauss()
    #fit_gauss()
    #fit_custom()
    #nll()
    #pyMCMC()


if __name__ == '__main__':
    main()