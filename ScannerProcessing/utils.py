#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Ryan Mackenzie White <ryan.white4@canada.ca>
#
# Distributed under terms of the  license.

"""
Utilities
"""

import time
from functools import wraps


def timethis(func):
    '''
    Decorator for timing methods
    Python Cookbook 14.13
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        '''
        Timing wrapper
        '''
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        print('{}.{} : {}'.format(func.__module__, func.__name__, end - start))
        return r
    return wrapper
