'''
Tests the constructor and the the arithmetic.
'''
import unittest

import logging
import sys

import numpy
from numpy import ndarray

from intervals.number import Interval as I
from intervals.methods import (intervalise,lo,hi)

class TestMethods(unittest.TestCase):
    def test_lo(self): pass
    def test_hi(self): pass
    def test_width(self): pass
    def test_rad(self): pass
    def test_mid(self): pass
    def test_mig(self): pass
    def test_mag(self): pass

class TestUnary(unittest.TestCase):
    def test_abs(self): pass
    def test_sqrt(self): pass
    def test_exp(self): pass
    def test_log(self): pass

class TestTrig(unittest.TestCase):
    def test_sin(self): pass
    def test_sinvec(self): pass
    def test_cos(self): pass
    def test_cosvec(self): pass
    def test_tan(self): pass
    def test_tanvec(self): pass

class TestBinary(unittest.TestCase):
    def test_max(self): pass
    def test_min(self): pass

class TestSet(unittest.TestCase):
    def test_straddle(self): pass
    def test_intersect(self): pass
    def test_contain(self): pass

class TestParser(unittest.TestCase):
    def test_parser_1(self): pass
    def test_parser_2(self): pass
    def test_parser_3(self): pass
    def test_sizeit(self): pass
    def test_unsizeit(self): pass

class TestSubint(unittest.TestCase):
    def test_subintervalise_1(self): pass
    def test_bisect(self): pass
    def test_splitinterval(self): pass
    def test_reconstitute(self): pass
    def test_spaceproduct(self): pass

class TestTypes(unittest.TestCase):
    def test_isinterval(self): pass
    def test_isnotintrval(self): pass

if __name__ == '__main__':
    unittest.main()