# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 11:51:20 2018

@author: ryanwhi
Take some ideas from here
https://pypkg.com/pypi/simpledist/f/simpledist/distributions.py
https://stackoverflow.com/questions/17821458/random-number-from-histogram?answertab=oldest#tab-top

From vector create histogram
Histogram compute the PDF and CDF
CDF can be used to generate sample from PDF
Produce pdf and cdf which also includes Laplace noise
"""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from scipy.interpolate import UnivariateSpline as interpolate


def run():
    data = np.random.normal(size=1000)
    hist, bins = np.histogram(data, bins=50)

    x_grid = np.linspace(min(data), max(data), 1000)
    kdepdf = kde(data, x_grid, bandwidth=0.1)
    random_from_kde = generate_rand_from_pdf(kdepdf, x_grid)

    bin_midpoints = bins[:-1] + np.diff(bins) / 2
    random_from_cdf = generate_rand_from_pdf(hist, bin_midpoints)
    random_from_spline = generate_rand_from_spline(hist,bin_midpoints,min(data),max(data))

    f, axarr = plt.subplots(2, 2)
    f.subplots_adjust(hspace=0.3)

    axarr[0,0].hist(data, 50, normed=True, alpha=0.5, label='hist')
    axarr[0,0].plot(x_grid, kdepdf, color='r', alpha=0.5, lw=3, label='kde')
    axarr[0,0].legend()
    axarr[0,1].hist(random_from_spline, 50, alpha=0.5, label='from spline')
    axarr[0,1].legend()
    axarr[1,0].hist(random_from_cdf, 50, alpha=0.5, label='from hist')
    axarr[1,0].legend()
    axarr[1,1].hist(random_from_kde, 50, alpha=0.5, label='from kde')
    axarr[1,1].legend()
    #plt.show()


def kde(x, x_grid, bandwidth=0.2, **kwargs):
    """Kernel Density Estimation with Scipy"""
    kde = gaussian_kde(x, bw_method=bandwidth / x.std(ddof=1), **kwargs)
    return kde.evaluate(x_grid)


def generate_rand_from_pdf(pdf, x_grid):
    cdf = np.cumsum(pdf)
    cdf = cdf / cdf[-1]
    #cdf_spline = interpolate(x_grid,cdf,s=0,k=1)
    values = np.random.rand(1000)
    value_bins = np.searchsorted(cdf, values)
    random_from_cdf = x_grid[value_bins]
    return random_from_cdf

def generate_rand_from_spline(pdf, x_grid, xmin, xmax):
    pdf_initial = interpolate(x_grid,pdf,s=0,k=1)
    xscan=np.linspace(xmin,xmax,1000)
    pdfstep=pdf_initial(xscan)
    ymax=max(pdfstep)
    i=0
    vals=[]
    while(i<1000):
        x = np.random.uniform(xmin,xmax)
        y = np.random.uniform(0,ymax)
        yp = pdf_initial(x)
        if(y<yp):
            i+=1
            vals.append(x)
            #print(i,x,y,y_max,p_accept)
    return vals    
    
    
     

    
if __name__ == '__main__':
    run()