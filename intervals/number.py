"""
--------------------------
Created Tue Feb 08 2022
github.com/marcodeangelis
MIT License
--------------------------
"""
from __future__ import annotations
from typing import (Sequence, Sized, Iterable, Optional, Any, Tuple, Union)
# Sequence: # Must have __len__() and __getitem__(). Ex.: Tuple, List, Range
# Sized: # It suffices to have len() 
# Iterable: # Must have __iter__() and __next__(). Ex.: Dict, Set, Tuple, List, numpy.array
# from intervals.methods import (lo,hi,width,rad,mag,straddlezero,isinterval)

import numpy
from numpy import (ndarray,asarray,stack,transpose,ascontiguousarray)
# float32=numpy.float32

from intervals.arithmetic import (multiply,divide)

MACHINE_EPS = 7./3 - 4./3 - 1

NUMERIC_TYPES =     {'int','float','complex',                   # Python numbers     
                    'int8','int16','int32','int64','intp',      # Numpy integers
                    'uint8','uint16','uint32','uint64','uintp', # Numpy unsigned integers
                    'float16','float32','float64','float_',     # Numpy floats and doubles
                    'complex64','complex128','complex_'}        # Numpy complex floats and doubles

# INTEGERS =          {'int','int8','int16','int32','int64','intp','uint8','uint16','uint32','uint64','uintp'}
# FLOATS =            {'float','float16','float32','float64','float_'}


def show(x: Interval) -> str:
    if len(x)==0: return f'[{x.lo()},{x.hi()}]' 
    elif len(x.shape)==1: return '\n'.join([f'[{xi.lo()},{xi.hi()}]' for xi in x]) # vector of intervals
    elif len(x.shape)==2: 
        n,d = x.shape
        return '\n'.join([' '.join([f'{xi.val()}' for xi in x[i,:]]) for i in range(n)]) # matrix of intervals
    else: return f'{x.val()}'

class Interval():
    """
    --------------------------
    Created Feb 2022
    github.com/marcodeangelis
    MIT License
    --------------------------

    Interval is the main class. 

    """
    def __repr__(self): # return
        return show(self)
    def __str__(self): # print
        return show(self)
    def __init__(self,
                 lo: Union[float,ndarray], 
                 hi: Optional[Union[float,ndarray]] = None) -> None:
        if hi is None:
            hi = lo.copy()
        self._unsized = True
        self.__lo = asarray(lo, dtype=float)
        self.__hi = asarray(hi, dtype=float) # check lo and hi have same shape
        if (len(self.__hi.shape)>0) | (len(self.__hi.shape)>0): self._unsized = False
        self.shape = self.__lo.shape
        self._scalar = (self.shape==()) | (self.shape==(1,))
    def __len__(self):
        if self.unsized(): return 0 # interval object is not sized, perhaps return an error: TypeError: len() of unsized object
        else: return self.__lo.shape[0] 
    def __iter__(self): # https://realpython.com/introduction-to-python-generators/
        lo_iter, hi_iter = numpy.nditer(self.lo()),numpy.nditer(self.hi())
        while True:
            try: yield Interval(lo=next(lo_iter),hi=next(hi_iter))
            except StopIteration: break
        pass
    def __next__(self):
        pass
    def __getitem__(self, i: Union[int, slice]): # make class indexable
        return Interval(lo=self.__lo[i],hi=self.__hi[i])
    # -------------- METHODS -------------- #
    def lo(self) -> ndarray:
        return self.__lo # return transpose(transpose(self.__val)[0]) # from shape (3,7,2) to (2,7,3) to (3,7)
    def hi(self) -> ndarray:
        return self.__hi # return transpose(transpose(self.__val)[1])
    def val(self):
        if self.unsized(): return asarray([self.__lo,self.__hi],dtype=float)
        else: return transpose(stack((self.__lo,self.__hi)))
    def unsized(self):
        if (len(self.__hi.shape)>0) | (len(self.__hi.shape)>0): return False
        else: return True
    def scalar(self):
        return (self.shape==()) | (self.shape==(1,))
    # -------------- ARITHMETIC -------------- #
    def __add__(self,other):
        otherType = other.__class__.__name__
        if (otherType == 'ndarray') | (otherType in NUMERIC_TYPES): lo, hi = self.lo() + other, self.hi() + other
        elif otherType == 'Interval': lo,hi = self.lo() + other.lo(), self.hi() + other.hi()
        else: return NotImplemented # TypeError: unsupported operand type(s) for +: 'int' and 'Interval' (for example)
        return Interval(lo,hi)
    def __radd__(self, left):
        leftType = left.__class__.__name__
        if (leftType == 'ndarray') | (leftType in NUMERIC_TYPES): return self.__add__(left)
        else: return NotImplemented # TypeError: unsupported operand type(s) for +: 'int' and 'Interval' (for example)
    def __sub__(self, other):
        otherType = other.__class__.__name__
        if (otherType == 'ndarray') | (otherType in NUMERIC_TYPES): lo,hi = self.lo() - other, self.hi() - other
        elif otherType == 'Interval': lo, hi = self.lo() - other.hi(), self.hi() - other.lo()
        else: NotImplemented
        return Interval(lo,hi)
    def __rsub__(self, left):
        leftType = left.__class__.__name__
        if (leftType == 'ndarray') | (leftType in NUMERIC_TYPES): lo, hi = left - self.hi(), left - self.lo()
        else: return NotImplemented #print("Error: not among the allowed types.")
        return Interval(lo,hi)
    def __mul__(self,other):
        otherType = other.__class__.__name__
        lo,hi = numpy.empty(self.__lo.shape),numpy.empty(self.__lo.shape)
        if otherType in NUMERIC_TYPES:
            if other >= 0: lo, hi = self.lo() * other, self.hi() * other
            else: lo, hi = self.hi() * other, self.lo() * other
        elif otherType == 'ndarray': # check self and other have same shape
            if len(other.shape)==0: self.__mul__(float(other)) # safety net for ndarrays with no shape
            other_positive = other >= 0
            other_negative = other_positive==False
            lo[other_positive]=self.lo()[other_positive] * other[other_positive]
            hi[other_positive]=self.hi()[other_positive] * other[other_positive]
            lo[other_negative]=self.hi()[other_negative] * other[other_negative]
            hi[other_negative]=self.lo()[other_negative] * other[other_negative]
        elif otherType == 'Interval':
            lo,hi = multiply(self,other,lo,hi)
        else: return NotImplemented
        return Interval(lo,hi)
    def __rmul__(self, left):
        leftType = left.__class__.__name__
        if (leftType == 'ndarray') | (leftType in NUMERIC_TYPES): return self.__mul__(left)
        else: return NotImplemented
    def __truediv__(self,other):
        otherType = other.__class__.__name__
        lo,hi = numpy.empty(self.__lo.shape),numpy.empty(self.__lo.shape)
        if otherType in NUMERIC_TYPES:
            if other == 0: raise ZeroDivisionError
            if other > 0: lo, hi = self.lo() / other, self.hi() / other
            else: lo, hi = self.hi() / other, self.lo() / other
        elif otherType == 'ndarray':
            if any(other.flatten()==0): raise ZeroDivisionError
            other_positive = other > 0
            other_negative = other_positive==False
            lo[other_positive]=self.lo()[other_positive] / other[other_positive]
            hi[other_positive]=self.hi()[other_positive] / other[other_positive]
            lo[other_negative]=self.hi()[other_negative] / other[other_negative]
            hi[other_negative]=self.lo()[other_negative] / other[other_negative]
            pass
        elif otherType == 'Interval':
            lo,hi = divide(self,other,lo,hi)
        else: NotImplemented
        return Interval(lo,hi)
    def __rtruediv__(self, left):
        leftType = left.__class__.__name__
        lo,hi = numpy.empty(self.__lo.shape),numpy.empty(self.__hi.shape)
        self_lo, self_hi = self.lo(), self.hi()
        self_straddle_zero = numpy.any((self_lo.flatten()<=0) & (self_hi.flatten()>=0))
        if self_straddle_zero: raise ZeroDivisionError
        if (leftType == 'ndarray') | (leftType in NUMERIC_TYPES): 
            if left >= 0: lo, hi = left / self_hi, left / self_lo
            else: lo, hi = left / self_lo, left / self_hi
        else: return NotImplemented
        return Interval(lo,hi)

# def multiply(s,o,l,h):
#     s_lo,s_hi,o_lo,o_hi=s.lo(),s.hi(),o.lo(),o.hi()
#     if s_lo.shape==o_lo.shape:
#         pp=(s_lo >= 0) & (o_lo >= 0) # A+ B+
#         l[pp] = s_lo[pp] * o_lo[pp]
#         h[pp] = s_hi[pp] * o_hi[pp]
#         pz=(s_lo>=0) & ((o_lo<0) & (o_hi>0)) # A+ B0
#         l[pz] = s_hi[pz] * o_lo[pz]
#         h[pz] = s_hi[pz] * o_hi[pz]
#         pn=(s_lo>=0) & (o_hi<=0) # A+ B-
#         l[pn] = s_hi[pn] * o_lo[pn]
#         h[pn] = s_lo[pn] * o_hi[pn]
#         zp=((s_lo<0) & (s_hi>0)) & (o_lo>=0) # A0 B+
#         l[zp] = s_lo[zp] * o_hi[zp]
#         h[zp] = s_hi[zp] * o_hi[zp]
#         zz=((s_lo<0) & (s_hi>0)) & ((o_lo<0) & (o_hi>0)) # A0 B0
#         l[zz]=numpy.min((s_lo[zz]*o_hi[zz], s_hi[zz]*o_lo[zz],s_lo[zz]*o_lo[zz],s_hi[zz]*o_hi[zz]),axis=0)
#         h[zz]=numpy.max((s_lo[zz]*o_lo[zz], s_hi[zz]*o_hi[zz],s_lo[zz]*o_hi[zz],s_hi[zz]*o_lo[zz]),axis=0)
#         zn=((s_lo<0) & (s_hi>0)) & (o_hi<=0)# A0 B-
#         l[zn] = s_hi[zn] * o_lo[zn]
#         h[zn] = s_lo[zn] * o_lo[zn]
#         np=(s_hi<=0) & (o_lo>=0) # A- B+
#         l[np] = s_lo[np] * o_hi[np]
#         h[np] = s_hi[np] * o_lo[np]
#         nz=(s_hi<=0) & ((o_lo<0) & (o_hi>0)) # A- B0
#         l[nz] = s_lo[nz] * o_hi[nz]
#         h[nz] = s_lo[nz] * o_lo[nz]
#         nn=(s_hi<=0) & (o_hi<=0) # A- B-
#         l[nn] = s_hi[nn] * o_hi[nn]
#         h[nn] = s_lo[nn] * o_lo[nn]
#     elif s.scalar():
#         pp=(s_lo >= 0) & (o_lo >= 0) # A+ B+
#         l[pp] = s_lo * o_lo[pp]
#         h[pp] = s_hi * o_hi[pp]
#         pz=(s_lo>=0) & ((o_lo<0) & (o_hi>0)) # A+ B0
#         l[pz] = s_hi * o_lo[pz]
#         h[pz] = s_hi * o_hi[pz]
#         pn=(s_lo>=0) & (o_hi<=0) # A+ B-
#         l[pn] = s_hi * o_lo[pn]
#         h[pn] = s_lo * o_hi[pn]
#         zp=((s_lo<0) & (s_hi>0)) & (o_lo>=0) # A0 B+
#         l[zp] = s_lo * o_hi[zp]
#         h[zp] = s_hi * o_hi[zp]
#         zz=((s_lo<0) & (s_hi>0)) & ((o_lo<0) & (o_hi>0)) # A0 B0
#         l[zz]=numpy.min((s_lo*o_hi[zz], s_hi*o_lo[zz],s_lo*o_lo[zz],s_hi*o_hi[zz]),axis=0)
#         h[zz]=numpy.max((s_lo*o_lo[zz], s_hi*o_hi[zz],s_lo*o_hi[zz],s_hi*o_lo[zz]),axis=0)
#         zn=((s_lo<0) & (s_hi>0)) & (o_hi<=0)# A0 B-
#         l[zn] = s_hi * o_lo[zn]
#         h[zn] = s_lo * o_lo[zn]
#         np=(s_hi<=0) & (o_lo>=0) # A- B+
#         l[np] = s_lo * o_hi[np]
#         h[np] = s_hi * o_lo[np]
#         nz=(s_hi<=0) & ((o_lo<0) & (o_hi>0)) # A- B0
#         l[nz] = s_lo * o_hi[nz]
#         h[nz] = s_lo * o_lo[nz]
#         nn=(s_hi<=0) & (o_hi<=0) # A- B-
#         l[nn] = s_hi * o_hi[nn]
#         h[nn] = s_lo * o_lo[nn]
#     elif o.scalar():
#         pp=(s_lo >= 0) & (o_lo >= 0) # A+ B+
#         l[pp] = s_lo[pp] * o_lo
#         h[pp] = s_hi[pp] * o_hi
#         pz=(s_lo>=0) & ((o_lo<0) & (o_hi>0)) # A+ B0
#         l[pz] = s_hi[pz] * o_lo
#         h[pz] = s_hi[pz] * o_hi
#         pn=(s_lo>=0) & (o_hi<=0) # A+ B-
#         l[pn] = s_hi[pn] * o_lo
#         h[pn] = s_lo[pn] * o_hi
#         zp=((s_lo<0) & (s_hi>0)) & (o_lo>=0) # A0 B+
#         l[zp] = s_lo[zp] * o_hi
#         h[zp] = s_hi[zp] * o_hi
#         zz=((s_lo<0) & (s_hi>0)) & ((o_lo<0) & (o_hi>0)) # A0 B0
#         l[zz]=numpy.min((s_lo[zz]*o_hi, s_hi[zz]*o_lo,s_lo[zz]*o_lo,s_hi[zz]*o_hi),axis=0)
#         h[zz]=numpy.max((s_lo[zz]*o_lo, s_hi[zz]*o_hi,s_lo[zz]*o_hi,s_hi[zz]*o_lo),axis=0)
#         zn=((s_lo<0) & (s_hi>0)) & (o_hi<=0)# A0 B-
#         l[zn] = s_hi[zn] * o_lo
#         h[zn] = s_lo[zn] * o_lo
#         np=(s_hi<=0) & (o_lo>=0) # A- B+
#         l[np] = s_lo[np] * o_hi
#         h[np] = s_hi[np] * o_lo
#         nz=(s_hi<=0) & ((o_lo<0) & (o_hi>0)) # A- B0
#         l[nz] = s_lo[nz] * o_hi
#         h[nz] = s_lo[nz] * o_lo
#         nn=(s_hi<=0) & (o_hi<=0) # A- B-
#         l[nn] = s_hi[nn] * o_hi
#         h[nn] = s_lo[nn] * o_lo
#     return l,h


# def divide(s,o,l,h):
#     s_lo,s_hi,o_lo,o_hi=s.lo(),s.hi(),o.lo(),o.hi()
#     other_straddle_zero = numpy.any((o_lo.flatten()<=0) & (o_hi.flatten()>=0))
#     if other_straddle_zero: raise ZeroDivisionError
#     if s_lo.shape==o_lo.shape:
#         pp=(s_lo >= 0) & (o_lo > 0) # A+ B+
#         l[pp] = s_lo[pp] / o_hi[pp]
#         h[pp] = s_hi[pp] / o_lo[pp]
#         zp=((s_lo<0) & (s_hi>0)) & (o_lo>0) # A0 B+
#         l[zp] = s_lo[zp] / o_lo[zp]
#         h[zp] = s_hi[zp] / o_lo[zp]
#         np=(s_hi<=0) & (o_lo>=0) # A- B+
#         l[np] = s_lo[np] / o_lo[np]
#         h[np] = s_hi[np] / o_hi[np]
#         pn=(s_lo>=0) & (o_hi<=0) # A+ B-
#         l[pn] = s_hi[pn] / o_hi[pn]
#         h[pn] = s_lo[pn] / o_lo[pn]
#         zn=((s_lo<0) & (s_hi>0)) & (o_hi<=0) # A0 B-
#         l[zn] = s_hi[zn] / o_hi[zn]
#         h[zn] = s_lo[zn] / o_hi[zn]
#         nn=(s_hi<=0) & (o_hi<=0) # A- B-
#         l[nn] = s_hi[nn] / o_lo[nn]
#         h[nn] = s_lo[nn] / o_hi[nn]
#     elif s.scalar():
#         pp=(s_lo >= 0) & (o_lo > 0) # A+ B+
#         l[pp] = s_lo / o_hi[pp]
#         h[pp] = s_hi / o_lo[pp]
#         zp=((s_lo<0) & (s_hi>0)) & (o_lo>0) # A0 B+
#         l[zp] = s_lo / o_lo[zp]
#         h[zp] = s_hi / o_lo[zp]
#         np=(s_hi<=0) & (o_lo>=0) # A- B+
#         l[np] = s_lo / o_lo[np]
#         h[np] = s_hi / o_hi[np]
#         pn=(s_lo>=0) & (o_hi<=0) # A+ B-
#         l[pn] = s_hi / o_hi[pn]
#         h[pn] = s_lo / o_lo[pn]
#         zn=((s_lo<0) & (s_hi>0)) & (o_hi<=0) # A0 B-
#         l[zn] = s_hi / o_hi[zn]
#         h[zn] = s_lo / o_hi[zn]
#         nn=(s_hi<=0) & (o_hi<=0) # A- B-
#         l[nn] = s_hi / o_lo[nn]
#         h[nn] = s_lo / o_hi[nn]
#     elif o.scalar():
#         pp=(s_lo >= 0) & (o_lo > 0) # A+ B+
#         l[pp] = s_lo[pp] / o_hi
#         h[pp] = s_hi[pp] / o_lo
#         zp=((s_lo<0) & (s_hi>0)) & (o_lo>0) # A0 B+
#         l[zp] = s_lo[zp] / o_lo
#         h[zp] = s_hi[zp] / o_lo
#         np=(s_hi<=0) & (o_lo>=0) # A- B+
#         l[np] = s_lo[np] / o_lo
#         h[np] = s_hi[np] / o_hi
#         pn=(s_lo>=0) & (o_hi<=0) # A+ B-
#         l[pn] = s_hi[pn] / o_hi
#         h[pn] = s_lo[pn] / o_lo
#         zn=((s_lo<0) & (s_hi>0)) & (o_hi<=0) # A0 B-
#         l[zn] = s_hi[zn] / o_hi
#         h[zn] = s_lo[zn] / o_hi
#         nn=(s_hi<=0) & (o_hi<=0) # A- B-
#         l[nn] = s_hi[nn] / o_lo
#         h[nn] = s_lo[nn] / o_hi
#     return l,h

# def iterator(x:Interval) -> Interval:
#     lo_iter,hi_iter = numpy.nditer(x.lo()),numpy.nditer(x.hi())
#     while True: yield Interval(lo=next(lo_iter),hi=next(hi_iter))


def is_Interval(x:Any) -> bool:
    x_class_name = x.__class__.__name__
    return x_class_name == 'Interval'