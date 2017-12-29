#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 Ryan Mackenzie White <ryan.white4@canada.ca>
#
# Distributed under terms of the  license.

"""
Example usage based on Kaggle Brazil retail dataset
Timing decorator added to test()
python3 example.py
To get detailed profiling
python3 -m cProfile example.py
"""

import logging

from Reader import Reader
from DataSchema import RecordLayout, RecordChecker
from DataQuality import Monitoring
from utils import timethis

log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


@timethis
def test():
    '''
    Test function
    '''
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

    reader = Reader('../data/kaggle/mock_kaggle.csv')
    checker = RecordChecker(record)
    
    # This is stupid
    # Needs to plot each variable
    # Infer the type from the schema object
    # Handle categorical data
    monitorvars = [False, True, True, True]

    monitor = Monitoring(record, monitorvars)
    print(checker.schema.description['Length'])
    print(checker.attributes)
    for idx, row in enumerate(reader.read_data()):
        if idx > 10:
            break
        if not checker.check(row):
            log.error('Cannot verify row %i', idx)
            continue
        log.debug('Confirmed row %i', idx)
        monitor.fill(row)
    monitor.distributions()
    # monitor.display_from_json()
    monitor.plot()


def main():
    logging.basicConfig(level=logging.DEBUG)
    test()


if __name__ == '__main__':
    main()
