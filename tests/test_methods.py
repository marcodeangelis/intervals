'''
Tests the constructor and the the arithmetic.
'''
import unittest

import logging
import sys

import numpy
from numpy import ndarray

from intervals.number import Interval as I
from intervals.methods import (intervalise,lo,hi,contain,almost_contain)
from intervals.random import uniform_endpoints

from intervals.methods import (abs,sqrt,exp,sin,cos)

PI = numpy.pi
numpy_sin = numpy.sin
numpy_exp = numpy.exp
numpy_linspace = numpy.linspace

X_LO_TRIG = [-2*PI, -3/2*PI, -PI, -PI/2, 0, PI/2, PI, 3/2*PI, 2*PI]
X_HI_TRIG = [ -3/2*PI, -PI, -PI/2, 0, PI/2, PI, 3/2*PI, 2*PI, 5/2*PI]

def zeroit(x, epsilon=1e-5):
    x = numpy.asarray(x, dtype=float)
    z = abs(x)<epsilon
    x[z] = 0.0
    return x

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
    def test_exp_1(self): 
        x = numpy.random.rand()
        y = exp(x)
        y_numpy = numpy_exp(x)
        self.assertEqual(y,y_numpy)
    def test_exp_2(self): 
        x = uniform_endpoints(n=1,left_bound=0,right_bound=9)
        y = exp(x)
        y_lo = numpy_exp(x.lo)
        y_hi = numpy_exp(x.hi)
        self.assertEqual(y.lo,y_lo)
        self.assertEqual(y.hi,y_hi)
    def test_log(self): pass

class TestTrig(unittest.TestCase):
    def test_sin_1(self): 
        xx = I(lo=X_LO_TRIG, hi=X_HI_TRIG)
        yy = intervalise([sin(xi) for xi in xx]) 
        x_ = numpy_linspace(min(X_LO_TRIG),max(X_HI_TRIG),num=10)
        y_ = numpy_sin(x_)
        for xxi,yyi in zip(xx,yy):  
            x_in_xx_i = contain(xxi,x_)
            y_in_yy_i = y_[x_in_xx_i]
            self.assertEqual(all(almost_contain(yyi,y_in_yy_i, tol=1e-9)),True)
    def test_sinvec_1(self): 
        xx = I(lo=X_LO_TRIG, hi=X_HI_TRIG)
        yy = sin(xx) # invokes vector sin
        x_ = numpy_linspace(min(X_LO_TRIG),max(X_HI_TRIG),num=10)
        y_ = zeroit(numpy_sin(x_))
        for xxi,yyi in zip(xx,yy):  
            x_in_xx_i = contain(xxi,x_)
            y_in_yy_i = y_[x_in_xx_i]
            self.assertEqual(all(almost_contain(yyi,y_in_yy_i, tol=1e-9)),True)
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