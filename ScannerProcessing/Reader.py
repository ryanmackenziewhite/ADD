#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Ryan Mackenzie White <ryan.white4@canada.ca>
#
# Distributed under terms of the  license.

"""
Simple class for file handling
Yields csv rows
"""
import csv
import logging
import unittest

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class Reader(object):
    '''
    Wrapper class for reading csv file
    '''
    def __init__(self, filename):
        self.filename = filename
        self._length = None

    def read_data(self):
        self._length = 0
        with open(self.filename, 'rU') as data:
            data.readline()
            reader = csv.reader(data)
            for row in reader:
                self._length += 1
                yield row


class TestCase(unittest.TestCase):
    def test(self):
        '''
        Write a file with x rows
        Read a file with Reader and check length
        '''


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    unittest.main()
