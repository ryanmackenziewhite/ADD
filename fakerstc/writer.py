#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ryan Mackenzie White <ryan.white4@canada.ca>
#
# Distributed under terms of the  license.

"""
Writer class for Synthesizer rows to csv files
"""
import csv
import os


class Writer(object):

    def __init__(self, basename, synth, nevts):
        '''
        '''
        self.fbase = basename
        self.synth = synth
        self.chunk_size = 1000
        self.max_size = 1
        self.nevts = nevts
        self.evts = 0
    
    def write_file(self, fname):
        print('Writing file', fname)
        with open(fname, 'w') as f:
            writer = csv.writer(f)
            while (os.path.getsize(fname)//1024**2) < self.max_size:
                data = []
                for _ in range(self.chunk_size):
                    data.append(tuple(self.synth.generate()))
                    self.evts += 1
                    if(self.evts == self.nevts):
                        continue
                writer.writerows(data)
                if(self.evts == self.nevts):
                    break

    def write(self):
        '''
        Generate events up to nevts
        Automatically open new files
        given max file size
        write data in chunks to improve I/O
        '''
        ifile = 0

        while(self.evts < self.nevts):
            filenum = format(ifile, '04')
            fname = self.fbase + '.' + filenum + '.csv'
            self.write_file(fname) 
            ifile += 1
            print('Completed file with ', self.evts)




                    



