#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ryan Mackenzie White <ryan.white4@canada.ca>
#
# Distributed under terms of the  license.

"""
Command Line Interface
Taking example from faker
"""
import sys
import os
import argparse

from synthesizer import Synthesizer
from writer import Writer


class Command(object):

    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])

    def execute(self):

        parser = argparse.ArgumentParser(prog=self.prog_name)

        parser.add_argument('-o', dest='outfile', 
                            action='store',
                            required=True,
                            help='base dataset name')
        
        parser.add_argument('-m', '--model',
                            dest='model',
                            action='store',
                            required=True,
                            help='model to generate')

        parser.add_argument('-n', '--nevents',
                            dest='nevents',
                            type=int,
                            required=True,
                            help="Total number of events to generate")

        parser.add_argument('-s', '--seed',
                            dest='seed',
                            action='store',
                            help='set seed')

        arguments = parser.parse_args(self.argv[1:])
        
        s = Synthesizer('examples', arguments.model, 'en_CA')
        writer = Writer(arguments.outfile, s, arguments.nevents)
        writer.write()


def execute_from_command_line(argv=None):
    command = Command(argv)
    command.execute()

