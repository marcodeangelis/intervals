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

if __name__ == '__main__':
    # logging.basicConfig(stream=sys.stderr,level=logging.DEBUG)
    # unittest.TextTestRunner().run(TestIntervalArithmetic())
    # logging.basicConfig( stream=sys.stderr )
    # logging.getLogger( "SomeTest.testSomething" ).setLevel( logging.DEBUG )
    unittest.main()