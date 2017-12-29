#! /opt/local/bin python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Ryan Mackenzie White <ryan.white4@canada.ca>
#
# Distributed under terms of the  license.

"""
Record Layout Schema check for Data Quality check
User-defined meta data, or
Infer meta-data from input data
"""

import json
import logging
import numpy as np
import matplotlib.pyplot as plt
import unittest

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


class Histogram(object):

    def __init__(self, name, nbins):
        self.histogram = {'Name': name,
                          'Nbins': nbins,
                          'Min': None,
                          'Max': None,
                          'Edges': [],
                          'Content': [],
                          'Width': None}

    def fill(self, data, dtype):
        npdata = np.array(data, dtype)
        contents, edges = np.histogram(npdata, bins=self.histogram['Nbins'])
        width = edges[1:] - edges[:-1]  
        self.histogram['Contents'] = contents.tolist()
        self.histogram['Edges'] = edges.tolist()
        self.histogram['Min'] = float(npdata.min())
        self.histogram['Max'] = float(npdata.max())
        self.histogram['Width'] = width.tolist()
    
    def describe_from_persisted(self, data):
        '''
        Create json schema from persisted json 
        '''
        self.histogram = data
    
    def save_to_json(self, filename):
        with open(filename, 'w') as ofile:
            json.dump(self.histogram, ofile, indent=4)

    def display_from_json(self):
        print(json.dumps(self.histogram, indent=4))

    def parse_from_json(self, filename):
        with open(filename, 'r') as ifile:
            data = json.load(ifile)
            if data['Name'] != self.name:
                log.error('Persisted schema name does not match instance name')
            else:
                self.describe_from_persisted(data)

    def plot(self, fname=''):    
        plt.bar(self.edges[:-1], self.contents, width=self.width, label='B')
        plt.legend(loc='upper right')
        if fname:
            fname = 'test'+str(idx)+'.pdf'
            plt.savefig(fname)


class Monitoring(object):
    '''
    Store csv data columns to histograms
    '''
    def __init__(self, schema, monitoring):
        '''
        Requires the RecordLayout
        :param schema:
        '''
        self.schema = schema
        self.length = int(self.schema.description['Length'])
        self.attributes = self.schema.description['Attributes']
        self.monitoring = monitoring
        self.arrays = [[] for x in range(self.length)]
        self.histograms = {}

    def display_from_json(self):
        print(json.dumps(self.histograms, indent=4))
    
    def save_to_json(self, filename):
        with open(filename, 'w') as ofile:
            json.dump(self.histogram, ofile, indent=4)
    
    def describe_from_persisted(self, data):
        '''
        Create json schema from persisted json 
        '''
        self.histograms = data
    
    def parse_from_json(self, filename):
        with open(filename, 'r') as ifile:
            data = json.load(ifile)
            if data:
                self.describe_from_persisted(data)
            else:
                log.error('Monitoring data not loaded')
    
    def fill(self, row):
        for idx, item in enumerate(row):
            if self.monitoring[idx]: 
                self.arrays[idx].append(item)

    def distributions(self):
        for name in self.attributes:
            idx = self.attributes[name][1]
            data = self.arrays[idx]
            log.debug('Creating histogram %s for column %s', name, str(idx))
            if len(data) > 0:
                h = Histogram(name, 20)
                h.fill(data, np.float32)
                # h.display_from_json()
                self.histograms[name] = h.histogram
    
    def plot(self):
        '''
        Determine grid size for plots
        https://stackoverflow.com/questions/12319796/\
                dynamically-add-create-subplots-in-matplotlib
        '''
        Tot = self.length
        Cols = self.length // 2 

        Rows = Tot // Cols
        Rows += Tot % Cols

        Position = range(1, Tot + 1)

        fig = plt.figure()
        for idx, name in enumerate(self.histograms):
            h = self.histograms[name]
            ax = fig.add_subplot(Rows, Cols, Position[idx])
            ax.bar(h['Edges'][:-1], h['Contents'], width=h['Width'],
                   label=name)
            ax.set_xlabel(name)
            ax.set_ylabel('Counts')
        plt.subplots_adjust(wspace=0.3, hspace=0.30)    
        fig.savefig('testmon.pdf')    
     

class TestCase(unittest.TestCase):
    def test(self):
        '''
        '''


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    unittest.main()



