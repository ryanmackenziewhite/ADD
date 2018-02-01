#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ryan Mackenzie White <ryan.white4@canada.ca>
#
# Distributed under terms of the  license.

"""
Reading / Writing csv files
"""
import numpy as np
import uuid
import csv
import os


def chunkwriter(outfile, outsize, chunksize):
    '''
    https://stackoverflow.com/questions/27731458/fastest-way-to-write-large-csv-with-python
    Writer multiple lines as chunks
    Up to max size of file
    outsize in MB
    chunksize is buffer bytes???
    '''
    with open(outfile, 'w') as csvfile:
        writer = csv.writer(csvfile)
        while (os.path.getsize(outfile)//1024**2) < outsize:
            data = [np.random.random(chunksize)*50,
                    np.random.random(chunksize)*50,
                    np.random.randint(1000, size=(chunksize,))]
            writer.writerows([list(row) for row in zip(*data)])

# Python Cookbook 7.12 call_backs


def sample():
    
    n = 0
    # Closure function
    
    def func():
        print('n=', n)

    # Accessor
    def get_n():
        return n

    def set_n(value):
        nonlocal n
        n = value

    func.get_n = get_n
    func.set_n = set_n
    return func


def apply_async(func, args, *, callback):
    
    result = func(*args)

    callback(result)

def print_result(result):
    print('Got:', result)

def add(x, y):
    return x + y

def count(i, n):
    
    while i < n:
        i += 1
    return i


class ResultHandler():

    def __init__(self):
        self.sequence = 0
    
    def handler(self, result):
        self.sequence += 1
        print('[{}] Got: {}'.format(self.sequence, result))


def make_handler():
    
    sequence = 0

    def handler(result):
        nonlocal sequence
        sequence += 1
        print('[{}] Got: {}'.format(sequence, result))
    return handler

if __name__ == '__main__':
    #chunkwriter('junk.csv', 10, 100)
    f = sample()
    f()
    f.set_n(10)
    f()
    f.get_n()

    r = ResultHandler()
    apply_async(add, (2, 3), callback=r.handler)
    apply_async(add, ('hello', 'world'), callback=r.handler)
    
    while(r.sequence < 5):
        apply_async(count, (0, 10), callback=r.handler)

    #handler = make_handler()

