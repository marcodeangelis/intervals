import unittest

import logging
import sys

import numpy

from intervals.number import Interval as I
from intervals.methods import (intervalise,lo,hi)
from .interval_generator import pick_endpoints_at_random_uniform

class TestIntervalArithmetic(unittest.TestCase):
    def test_addition_by_endpoints_analysis(self):
        """
        Test addition 100 times between random intervals.
        """
        # log = logging.getLogger("TestLog")
        # log.debug("testing addition hundred times between random intervals")
        x = intervalise(pick_endpoints_at_random_uniform(n=100))
        y = intervalise(pick_endpoints_at_random_uniform(n=100))
        for xi,yi in zip(x,y):
            xi_op_yi = xi+yi
            a,b = [lo(xi),hi(xi)], [lo(yi),hi(yi)] 
            c = [ai+bj for ai in a for bj in b] # endpoints analysis
            ea = [min(c), max(c)] 
            self.assertAlmostEqual(lo(xi_op_yi), ea[0], places=7)
            self.assertAlmostEqual(hi(xi_op_yi), ea[1], places=7)
    def test_subtraction_by_endpoints_analysis(self):
        """
        Test subtraction 100 times between random intervals.
        """
        x = intervalise(pick_endpoints_at_random_uniform(n=100))
        y = intervalise(pick_endpoints_at_random_uniform(n=100))
        for xi,yi in zip(x,y):
            xi_op_yi = xi-yi
            a,b = [lo(xi),hi(xi)], [lo(yi),hi(yi)] 
            c = [ai-bj for ai in a for bj in b] # endpoints analysis
            ea = [min(c), max(c)] 
            self.assertAlmostEqual(lo(xi_op_yi), ea[0], places=7)
            self.assertAlmostEqual(hi(xi_op_yi), ea[1], places=7)
    def test_multiplication_by_endpoints_analysis(self):
        """
        Test multiplication 100 times between random intervals.
        """
        x = intervalise(pick_endpoints_at_random_uniform(n=100))
        y = intervalise(pick_endpoints_at_random_uniform(n=100))
        for xi,yi in zip(x,y):
            xi_op_yi = xi*yi
            a,b = [lo(xi),hi(xi)], [lo(yi),hi(yi)] 
            c = [ai*bj for ai in a for bj in b] # endpoints analysis
            ea = [min(c), max(c)] 
            self.assertAlmostEqual(lo(xi_op_yi), ea[0], places=7)
            self.assertAlmostEqual(hi(xi_op_yi), ea[1], places=7)
    def test_division_by_endpoints_analysis(self):
        """
        Test division 100 times between random intervals.
        """
        x = intervalise(pick_endpoints_at_random_uniform(n=100))
        y = intervalise(pick_endpoints_at_random_uniform(n=100,left_bound=0.001))
        for xi,yi in zip(x,y):
            xi_plus_yi = xi/yi
            a,b = [lo(xi),hi(xi)], [lo(yi),hi(yi)] 
            c = [ai/bj for ai in a for bj in b] # endpoints analysis
            ea = [min(c), max(c)] 
            self.assertAlmostEqual(lo(xi_plus_yi), ea[0], places=7)
            self.assertAlmostEqual(hi(xi_plus_yi), ea[1], places=7)
    def test_four_operations_between_interval_2darrays(self):
        """
        Test element-wise operations between two dimensional arrays of intervals.
        """
        x = intervalise(pick_endpoints_at_random_uniform(shape=(100,4)))
        y = intervalise(pick_endpoints_at_random_uniform(shape=(100,4),left_bound=0.001))
        x_add_y = x+y
        x_sub_y = x-y
        x_mul_y = x*y
        x_div_y = x/y
        for xi,yi,z1,z2,z3,z4 in zip(x,y,x_add_y,x_sub_y,x_mul_y,x_div_y):
            xi_add_yi = xi+yi
            xi_sub_yi = xi-yi
            xi_mul_yi = xi*yi
            xi_div_yi = xi/yi
            self.assertAlmostEqual(lo(z1), lo(xi_add_yi), places=7)
            self.assertAlmostEqual(hi(z1), hi(xi_add_yi), places=7)
            self.assertAlmostEqual(lo(z2), lo(xi_sub_yi), places=7)
            self.assertAlmostEqual(hi(z2), hi(xi_sub_yi), places=7)
            self.assertAlmostEqual(lo(z3), lo(xi_mul_yi), places=7)
            self.assertAlmostEqual(hi(z3), hi(xi_mul_yi), places=7)
            self.assertAlmostEqual(lo(z4), lo(xi_div_yi), places=7)
            self.assertAlmostEqual(hi(z4), hi(xi_div_yi), places=7)
    def test_four_operations_between_interval_3darrays(self):
        """
        Test element-wise operations between three dimensional arrays of intervals.
        """
        x = intervalise(pick_endpoints_at_random_uniform(shape=(10,3,3)))
        y = intervalise(pick_endpoints_at_random_uniform(shape=(10,3,3),left_bound=0.001))
        x_add_y = x+y
        x_sub_y = x-y
        x_mul_y = x*y
        x_div_y = x/y
        for xi,yi,z1,z2,z3,z4 in zip(x,y,x_add_y,x_sub_y,x_mul_y,x_div_y):
            xi_add_yi = xi+yi
            xi_sub_yi = xi-yi
            xi_mul_yi = xi*yi
            xi_div_yi = xi/yi
            self.assertAlmostEqual(lo(z1), lo(xi_add_yi), places=7)
            self.assertAlmostEqual(hi(z1), hi(xi_add_yi), places=7)
            self.assertAlmostEqual(lo(z2), lo(xi_sub_yi), places=7)
            self.assertAlmostEqual(hi(z2), hi(xi_sub_yi), places=7)
            self.assertAlmostEqual(lo(z3), lo(xi_mul_yi), places=7)
            self.assertAlmostEqual(hi(z3), hi(xi_mul_yi), places=7)
            self.assertAlmostEqual(lo(z4), lo(xi_div_yi), places=7)
            self.assertAlmostEqual(hi(z4), hi(xi_div_yi), places=7)
    def test_four_operations_between_scalar_and_arrays(self):
        """
        Test element-wise operations between array-like and scalar intervals.
        """
        a = intervalise(pick_endpoints_at_random_uniform(n=1,left_bound=-1,right_bound=1))
        y = intervalise(pick_endpoints_at_random_uniform(shape=(10,3,3),left_bound=0.001))
        a_add_y = a+y
        a_sub_y = a-y
        a_mul_y = a*y
        a_div_y = a/y
        for yi,z1,z2,z3,z4 in zip(y,a_add_y,a_sub_y,a_mul_y,a_div_y):
            ai_add_yi = a+yi
            ai_sub_yi = a-yi
            ai_mul_yi = a*yi
            ai_div_yi = a/yi
            self.assertAlmostEqual(lo(z1), lo(ai_add_yi), places=7)
            self.assertAlmostEqual(hi(z1), hi(ai_add_yi), places=7)
            self.assertAlmostEqual(lo(z2), lo(ai_sub_yi), places=7)
            self.assertAlmostEqual(hi(z2), hi(ai_sub_yi), places=7)
            self.assertAlmostEqual(lo(z3), lo(ai_mul_yi), places=7)
            self.assertAlmostEqual(hi(z3), hi(ai_mul_yi), places=7)
            self.assertAlmostEqual(lo(z4), lo(ai_div_yi), places=7)
            self.assertAlmostEqual(hi(z4), hi(ai_div_yi), places=7)
    def test_four_operations_between_arrays_and_scalars(self):
        """
        Test element-wise operations between array-like and scalar intervals.
        """
        a = intervalise(pick_endpoints_at_random_uniform(n=1,left_bound=0.001,right_bound=1))
        y = intervalise(pick_endpoints_at_random_uniform(shape=(10,3,3),left_bound=0.001))
        y_add_a = y+a
        y_sub_a = y-a
        y_mul_a = y*a
        y_div_a = y/a
        for yi,z1,z2,z3,z4 in zip(y,y_add_a,y_sub_a,y_mul_a,y_div_a):
            yi_add_ai = yi+a
            yi_sub_ai = yi-a
            yi_mul_ai = yi*a
            yi_div_ai = yi/a
            self.assertAlmostEqual(lo(z1), lo(yi_add_ai), places=7)
            self.assertAlmostEqual(hi(z1), hi(yi_add_ai), places=7)
            self.assertAlmostEqual(lo(z2), lo(yi_sub_ai), places=7)
            self.assertAlmostEqual(hi(z2), hi(yi_sub_ai), places=7)
            self.assertAlmostEqual(lo(z3), lo(yi_mul_ai), places=7)
            self.assertAlmostEqual(hi(z3), hi(yi_mul_ai), places=7)
            self.assertAlmostEqual(lo(z4), lo(yi_div_ai), places=7)
            self.assertAlmostEqual(hi(z4), hi(yi_div_ai), places=7)
    def test_four_operations_between_interval_and_numeric(self):
        """
        Test element-wise operations between array-like and non-interval numbers.
        """
        a = -10 + numpy.random.rand() * 20 # a random number between -10 and 10
        y = intervalise(pick_endpoints_at_random_uniform(n=100,left_bound=0.001))
        for yi in y:
            yi_add_a = yi+a
            yi_sub_a = yi-a
            yi_mul_a = yi*a
            yi_div_a = yi/a
            yy = [lo(yi),hi(yi)]
            c_add = [bj+a for bj in yy] # endpoints analysis
            c_sub = [bj-a for bj in yy] # endpoints analysis
            c_mul = [bj*a for bj in yy] # endpoints analysis
            c_div = [bj/a for bj in yy] # endpoints analysis
            ea_add = [min(c_add), max(c_add)] 
            ea_sub = [min(c_sub), max(c_sub)] 
            ea_mul = [min(c_mul), max(c_mul)] 
            ea_div = [min(c_div), max(c_div)] 
            self.assertAlmostEqual(lo(yi_add_a), ea_add[0], places=7)
            self.assertAlmostEqual(hi(yi_add_a), ea_add[1], places=7)
            self.assertAlmostEqual(lo(yi_sub_a), ea_sub[0], places=7)
            self.assertAlmostEqual(hi(yi_sub_a), ea_sub[1], places=7)
            self.assertAlmostEqual(lo(yi_mul_a), ea_mul[0], places=7)
            self.assertAlmostEqual(hi(yi_mul_a), ea_mul[1], places=7)
            self.assertAlmostEqual(lo(yi_div_a), ea_div[0], places=7)
            self.assertAlmostEqual(hi(yi_div_a), ea_div[1], places=7)
    def test_four_operations_between_arrays_and_numeric(self):
        """
        Test element-wise operations between array-like and non-interval numbers.
        """
        a = -10 + numpy.random.rand() * 20
        y = intervalise(pick_endpoints_at_random_uniform(shape=(7,4,3),left_bound=0.001))
        y_add_a = y+a
        y_sub_a = y-a
        y_mul_a = y*a
        y_div_a = y/a
        for yi,z1,z2,z3,z4 in zip(y,y_add_a,y_sub_a,y_mul_a,y_div_a):
            yi_add_ai = yi+a
            yi_sub_ai = yi-a
            yi_mul_ai = yi*a
            yi_div_ai = yi/a
            self.assertAlmostEqual(lo(z1), lo(yi_add_ai), places=7)
            self.assertAlmostEqual(hi(z1), hi(yi_add_ai), places=7)
            self.assertAlmostEqual(lo(z2), lo(yi_sub_ai), places=7)
            self.assertAlmostEqual(hi(z2), hi(yi_sub_ai), places=7)
            self.assertAlmostEqual(lo(z3), lo(yi_mul_ai), places=7)
            self.assertAlmostEqual(hi(z3), hi(yi_mul_ai), places=7)
            self.assertAlmostEqual(lo(z4), lo(yi_div_ai), places=7)
            self.assertAlmostEqual(hi(z4), hi(yi_div_ai), places=7)

if __name__ == '__main__':
    # logging.basicConfig(stream=sys.stderr,level=logging.DEBUG)
    # unittest.TextTestRunner().run(TestIntervalArithmetic())
    # logging.basicConfig( stream=sys.stderr )
    # logging.getLogger( "SomeTest.testSomething" ).setLevel( logging.DEBUG )
    unittest.main()