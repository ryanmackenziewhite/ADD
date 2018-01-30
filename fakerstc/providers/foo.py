#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 Ryan Mackenzie White <ryan.white4@canada.ca>
#
# Distributed under terms of the  license.

"""

"""
import unittest

from faker import Faker
from faker.providers import BaseProvider


class FooProvider(BaseProvider):
    def foo(self):
        return self.generator.random.randint(0, 100)


class TestCase(unittest.TestCase):
    def test(self):
        fake = Faker()

        provider = FooProvider(fake)
        fake.add_provider(provider)
        print(fake.foo())


if __name__ == '__main__':
    unittest.main()
