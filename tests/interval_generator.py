import numpy

from intervals.number import Interval

LEFT_BOUND = -1_000
RIGHT_BOUND= 1_000

def pick_endpoints_at_random_uniform(n:int=2, left_bound:float=None, right_bound:float=None, kind:type=float, shape:tuple=None): # when N=2 generates two intervals
    if left_bound is None: left_bound=LEFT_BOUND
    if right_bound is None: right_bound=RIGHT_BOUND
    if shape is None:
        if n==1:
            if kind == float: improper = left_bound + numpy.random.rand(2,) * (right_bound-left_bound)
            elif kind == int: improper = numpy.random.randint(left_bound,high=right_bound,size=(2,))
            else: return NotImplemented
            return improper[0], improper[1]
        else:
            if kind == float: improper = left_bound + numpy.random.rand(n,2) * (right_bound-left_bound)
            elif kind == int: improper = numpy.random.randint(left_bound,high=right_bound,size=(n,2))
            else: return NotImplemented
            improper_lo, improper_hi = improper[:,0], improper[:,1]
    else:
        if kind == float: 
            improper_lo = left_bound + numpy.random.rand(*shape) * (right_bound-left_bound)
            improper_hi = left_bound + numpy.random.rand(*shape) * (right_bound-left_bound)
        elif kind == int: 
            improper_lo = numpy.random.randint(left_bound,high=right_bound,size=shape)
            improper_hi = numpy.random.randint(left_bound,high=right_bound,size=shape)
        else: return NotImplemented 
    swap = improper_lo >= improper_hi
    proper_lo, proper_hi = improper_lo.copy(), improper_hi.copy()
    if numpy.sum(swap)>0: proper_lo[swap],proper_hi[swap]=proper_hi[swap],proper_lo[swap]
    return (proper_lo, proper_hi)

