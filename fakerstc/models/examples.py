#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ryan Mackenzie White <ryan.white4@canada.ca>
#
# Distributed under terms of the  license.

"""
Data model is a nested dictionary

model = {CustomProviders: 
            {Provider: Optional Pdf}
         Pdfs:
            {Pdf: Optional list of fakes used}
         MetaData:
            {fake: args}
        }
"""
from .model import Model


class SampleModelA(Model):
    def __init__(self):
        meta = {'name': None,
                'ean': 13}
        super(SampleModelA, self).__init__(meta)


class CustomModel(Model):
    def __init__(self):
        '''
        Here we can set the pdf
        pass to the provider 
        as an argument
        '''
        meta = {'name': None,
                'ean': 13,
                'foo': None}
        super(CustomModel, self).__init__(meta)

