#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ryan Mackenzie White <ryan.white4@canada.ca>
#
# Distributed under terms of the  license.

"""

"""


class Model(object):
    '''
    Base Model class
    define properties, setters
    utilities to access the meta data
    Requires custom providers with optional pdfs

    Use nested dictionary, allows easy serialization to JSON
    '''
    def __init__(self, mdata):
        self.__meta = mdata

    @property
    def meta(self):
        return self.__meta

    @meta.setter
    def meta(self, mdata):
        self.__meta = mdata

    def provider(self, name):
        return self.meta[name]
