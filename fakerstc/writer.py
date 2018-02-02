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
import sys 


class Writer(object):

    def __init__(self, basename, synth, nevts, msize=1, csize=1000):
        '''
        '''
        self.dsetname = basename
        self.synthesizer = synth
        self.nevents = nevts
        self.maxfilesize = msize
        self.chunksize = csize
        self.__evtcntr = 0
        self.__filenum = 0
    
    @property
    def dsetname(self):
        return self.__dsetname

    @dsetname.setter
    def dsetname(self, value):
        self.__dsetname = value
    
    @property
    def synthesizer(self):
        return self.__synthesizer

    @synthesizer.setter
    def synthesizer(self, synth):
        self.__synthesizer = synth
    
    @property
    def chunksize(self):
        return self._csize

    @chunksize.setter
    def chunksize(self, value):
        self._csize = value

    @property
    def maxfilesize(self):
        return self._msize

    @maxfilesize.setter
    def maxfilesize(self, value):
        self._msize = value

    @property
    def nevents(self):
        return self.__nevts
    
    @property
    def eventcount(self):
        return self.__evtcntr

    @property
    def filecount(self):
        return self.__filenum

    @nevents.setter
    def nevents(self, value):
        self.__nevts = value
    
    def eventcounter(self):
        self.__evtcntr += 1
    
    def filecounter(self):
        self.__filenum += 1 

    def checkcount(self):
        if(self.eventcount == self.nevents):
            return True
        else:
            return False
   
    def chunk(self):
        '''
        Allow for concurrent generate during write
        '''
        for _ in range(self.chunksize):
            yield tuple(self.synthesizer.generate())
            self.eventcounter()
            if self.checkcount():
                break
    
    def formatname(self):
        return self.dsetname + '.' + format(self.filecount, '04') + '.csv'

    def write_file(self, fname):
        print('Writing file', fname)
        try:
            with open(fname, 'x') as f:
                writer = csv.writer(f)
                while (os.path.getsize(fname)//1024**2) < self.maxfilesize:
                    data = list(self.chunk())
                    writer.writerows(data)
                    if(self.checkcount()):
                        break
        except IOError as e:
            print('I/O Error({0}: {1})'.format(e.errno, e.strerror))
            return False
        except:
            print('Unexpected error:', sys.exc_info()[0])
            return False
        return True

    def write(self):
        '''
        Generate events up to nevts
        Automatically open new files
        given max file size
        write data in chunks to improve I/O
        '''

        while(self.eventcount < self.nevents):
            fname = self.formatname() 
            if not self.write_file(fname):
                print('Cannot write file')
                break
            self.filecounter()
            print('Completed file with ', self.eventcount)




                    



