#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ryan Mackenzie White <ryan.white4@canada.ca>
#
# Distributed under terms of the  license.

"""

"""
import numpy as np
from math import sqrt


def pi_gen(N):
    '''
    Calculate the value of pi from the area of circle
    Can be obtained by finding the area of a circle of 
    unit radius, i.e. sqrt(x**2 + y**2) = 1
    Throw random number in a corner of a square OABC
    N = number of trials
    H = number accepted in circle

    pi = 4H/N 
    '''
    trials = N
    accepts = 0
    
    for _ in range(N):
        x = np.random.uniform(0, 1)
        y = np.random.uniform(0, 1)

        radius = sqrt(x**2 + y**2) 

        if(radius <= 1):
            accepts += 1

    pi = (4. * accepts) / trials
    print(pi)


if __name__ == '__main__':
    pi_gen(100000)
