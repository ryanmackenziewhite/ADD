#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ryan Mackenzie White <ryan.white4@canada.ca>
#
# Distributed under terms of the  license.

"""
Record Linkage dataset generated
Based on Febrl generator

Febrl (Freely Extensible Biomedical Record Linkage) is a freely available tool that enables record linkage through a GUI.
The tool written in python which offers both a programming interface as well as GUI, supporting several record linakge
algorithms. In addition, the tool includes a data generator which generates two record data sets suitable for performing
record linkage. The data generator creates two datasets with the following random variables:
    field given a frequency table (histogram)
    date
    phone
    identification

The following probabilities are defined to modify
The second (duplicate) dataset draws randomly from first (original).
Each field defines a dictionary of probabilities:
Modify a given field
Mispell
Insert a character
Delete character
Substiture character
Swap two characters
Swap two fields
Swap words in field
Split a word
Merge words
Null field
Insert new value

Random selection for number of duplicates for each record, following distributions:
    Uniform
    Poisson
    Zipf
    
    For each duplicate apply the modifications up to:
    Maximum number of modifications for a given record -- fixed
    Maximum number of modifications for a given field -- randomly select number of modiication

Straightforward to implement.
Requires suitable dictionaries for generating proper Canadian addresses.
Requires dictionary of commonly mispelled words (with list of misspellings).
This will also serve well for the Postal data.
"""

class Modifier(object):
    '''
    Base modification class for row of data

    '''

    def __init__(self,meta=None):
        '''
        Requires frequencies for field modification
        Requires modification probabilities
        Pass tuple of lists or list
        '''

        meta = {'field1': 0.5,
                'field2': 0.5,
                }
        duplicate_dist = 'uniform'

        max_duplicates = 1.
        max_modifications_in_record = 1.

        modification = {'insert':0.00, # insert character in field
                        'delete':0.00, # delete character in field
                        'substitute':0., # substitute character in field
                        'misspell':0., # use mispelling dictionary
                        'transpose':0., # transpose adjacent characters
                        'replace':0.0, # replace with another value of same fake
                        'swap': 0.0, # swap two words/values in field
                        'split':0.00, # split a field
                        'merge':0.00, # merge a field
                        'nullify':0.0, # convert to null
                        'fill':0.0 # fill empty field with expected type
                        }
                        
                        def validate(self):
        '''
        Ensure defined metafields probabilitites sum to 1
        '''
        pass

    def modify(self, rows):
        '''
        modify given a row or tuple of rows
        '''
        pass

    def _modify(self, row):
        '''
        determine whether to modify a field in a row
        select modification
        apply modification
        '''
        pass

    def nduplicates(self):
        '''
        return maximum number of duplicates to generate
        '''

    def select_field(self, row):
        '''
        Select field for modification
        '''
        if (mod is 'replace'):
            row = select_fields()
        pass

    def select_fields(self, row):
        '''
        Select two fields to swap
        '''
        if(max_number_mod > 1):
            return self.swap_fields(self)
        else:
            return row
            
            def choice(self, row):
        '''
        Implemented in faker
        select bin given frequencies
        '''

    def select_modification(self):
        '''
        Select modifcation to apply to field
        '''
        idx = self.choice()

    def misspell(self, data):
        '''
        Dictionary of commonly misspelled words
        '''
        pass

    def swap_fields(self,):
        '''
        randomly replace values in pair of fields
        '''
        pass

    def nullify(self):
        '''
        random null value
        '''
        return None

    def swap_character(self):
        '''
        swap adjacent in field
        '''
        pass

    def substitute(self):
        '''
        substitute random character
        '''
        pass
        def insert_char(self, data):
        '''
        insert random character
        '''
        pass

    def insert_numeric(self):
        '''
        insert random numeral
        '''
        pass

    def insert(self, data):
        '''
        insert single character according to type
        '''
        if(isinstance(str,data)):
            return insert_char(data)
        else:
            return insert_numeric(data)
        pass

    def delete_char(self):
        '''
        delete random character in word
        '''
        pass

    def transpose(self):
        '''
        transpose two characters
        '''
        pass

    def split(self):
        '''
        split word
        '''
        pass

    def merge(self):
        '''
        merge one or more words
        '''
        pass
