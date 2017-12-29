#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Ryan Mackenzie White <ryan.white4@canada.ca>
#
# Distributed under terms of the  license.

"""
Schema enforcing for data
"""
import logging
import json
from datetime import datetime
from enum import Enum
import unittest

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class DataType(Enum):
    '''
    Simple Enum class taken from DataSynthesize
    '''
    INTEGER = 'Integer'
    FLOAT = 'Float'
    STRING = 'String'
    DATETIME = 'DateTime'
    SOCIAL_SECURITY_NUMBER = 'SocialSecurityNumber'


class RecordLayout(object):
    """
    Predefined metadata class
    Instantitiate with all required properties to check
    Length of row
    Datatypes
    """
    def __init__(self, name, length=None,
                 attribute_to_datatype={}, persisted=None):
        '''
        >>> record = RecordLayout('Test', 1, {'Attr1':('String',0)})
        '''
        if name is None:
            log.error('Error, name not given')
        elif persisted:
            self.name = name
            self.persisted = persisted
            self.parse_from_json(persisted)
        else:
            self.name = name
            # Length of row
            self.length = length
            # Dictionary attribute name and type
            self.attribute_to_datatype = attribute_to_datatype
            # Nested dictionary (equivalent to JSON) recording the metadata
            self.description = {}
            # JSON schema file
            self.persisted = ''
            self.describe_from_configured()

    def describe(self):
        pass   

    def describe_from_configured(self):
        '''
        Create json schema from configured properties
        '''
        self.description['Name'] = self.name
        self.description['Length'] = self.length
        self.description['Attributes'] = self.attribute_to_datatype
        if self.length != len(self.attribute_to_datatype.items()):
            log.error('Length not equal to number of attributes')    

    def describe_from_persisted(self, data):
        '''
        Create json schema from persisted json 
        '''
        self.description = data

    def save_to_json(self, filename):
        with open(filename, 'w') as ofile:
            json.dump(self.description, ofile, indent=4)

    def display_from_json(self):
        '''
        >>> record = RecordLayout('Test', 1, {'Attr1':('String',0)})
        >>> record.display_from_json()
        '''
        print(json.dumps(self.description, indent=4))

    def parse_from_json(self, filename):
        with open(filename, 'r') as ifile:
            data = json.load(ifile)
            if data['Name'] != self.name:
                log.error('Persisted schema name does not match instance name')
            else:
                self.describe_from_persisted(data)


class RecordChecker(object):
   
    typemap = {datetime: 'DateTime',
               int: 'Integer',
               float: 'Float',
               str: 'String'}
   
    def __init__(self, schema):
        '''
        >>> rchecker = RecordChecker(RecordLayout('Test', 1, {'Attr1':('String',0)}))
        '''
        self.schema = schema
        self.length = int(self.schema.description['Length'])
        self.attributes = list(self.schema.description['Attributes'].values())
        self.row = []
        self.rowtypes = []
    
    def check(self, row):    
        if not self.check_length(row):
            return False
        if not self.check_types(row):
            return False
        self.row = row
        log.debug('Row verified')
        log.debug('Row: %s', repr(self.row))
        log.debug('Types: %s', repr(self.rowtypes))
        
        return True

    def check_length(self, row):
        if len(row) != self.length:
            log.error('Cannot verify length of row')
            return False
        else:
            return True

    def check_types(self, row):
        ischecked = True
        types = self.get_types(row)
        self.rowtypes = types
        if(len(types) != self.length):
            log.error('Expect %i, converted types %i', self.length, len(types))
            return False
        for idx, item in enumerate(types):
            if item != self.attributes[idx][0]:
                log.error('Cannot verify type %s for schema %s', 
                          repr(item), repr(self.attributes[idx][0]))
                ischecked = False
        return ischecked        
    
    def get_type(self, value):
        '''
        Determine type of value with heuristics lambda
        https://stackoverflow.com/questions/2103071/\
                determine-the-type-of-a-value-which-is-represented-as-string-in-python
        >>> rc = RecordChecker(RecordLayout('Test', 1, {'Attr1':('String',0)}))
        >>> rc.get_type('blah')
        'blah'
        >>> rc.get_type(1.2)
        1.2
        '''
        heuristics = (lambda value: datetime.strptime(value, "%Y-%m-%d"), 
                      int, float)
        
        for type in heuristics:
            try:
                return type(value)
            except ValueError:
                continue
        return value

    def get_types(self, row):
        '''
        Check types from row in csv
        >>> rc = RecordChecker(RecordLayout('Test', 1, {'Attr1':('String',0)}))
        >>> rc.get_types(['blah'])
        ['String']
        >>> rc.get_types(['blah',2.0])
        ['String','Float']
        '''
        types = []
        for idx, item in enumerate(row):
            var_type = self.typemap[type(self.get_type(item))]
            if var_type is None:
                log.error('Conversion type to DataType failed')
            else:
                types.append(var_type)
        return types 


class TestCase(unittest.TestCase):
    def test(self):
        length = 4
        attr = {'Attr1': ('DateTime', 0),
                'Attr2': ('Integer', 1),
                'Attr3': ('Integer', 2),
                'Attr4': ('Float', 3)}
        record = RecordLayout('Test', length, attr)
        record.display_from_json()
        record.save_to_json('test.json')

        record2 = RecordLayout('Test', 0, attr, 'test.json')
        record2.display_from_json()
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
    unittest.main()
