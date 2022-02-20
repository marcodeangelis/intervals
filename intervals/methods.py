"""
-------------------------
Created Tue Feb 08 2022
Marco De Angelis
github.com/marcodeangelis
MIT License
-------------------------

These methods are designed to behave quietly. An Interval object is expected as input. 
Nonetheless, if something else other than Interval is passed, the input is returned.

"""
from __future__ import annotations
from typing import (Sequence, Sized, Iterable, Optional, Any, Tuple, Union)

import numpy
from numpy import (ndarray,asarray,transpose)

from intervals.number import Interval


# Properties or maybe attributes of the interval class. These apply to all interval-like objects.
def lo(x: Interval) -> Union[float, ndarray]:
    """
    Return the left endpoint of an Interval object.

    If x is not of class Interval, input is returned.

    """
    if is_Interval(x): return x.lo
    return x

def hi(x: Interval) -> Union[float, ndarray]:
    """
    Return the right endpoint of an Interval object.

    If x is not of class Interval, input is returned.
    
    """
    if is_Interval(x): return x.hi
    return x

def width(x):
    """
    Return the width of an Interval object.

    If x is not of class Interval, input is returned.
    
    """
    if is_Interval(x): return hi(x)-lo(x)
    return x

def rad(x):
    """
    Return the radius of an Interval object.

    If x is not of class Interval, input is returned.
    
    """
    if is_Interval(x): return (hi(x)-lo(x))/2
    return x

def mid(x):
    """
    Return the midpoint of an Interval object.

    If x is not of class Interval, input is returned.
    
    """
    if is_Interval(x): return (hi(x)+lo(x))/2
    return x

def mig(x):
    pass
def mag(x):
    pass
def abs(x):
    pass

# Methods are actions that can be taken on intervals
def is_Interval(x:Any) -> bool:
    x_class_name = x.__class__.__name__
    return x_class_name == 'Interval'

def straddle_zero(x: Interval) -> bool:
    if x.unsized(): return (lo(x)<=0) & (hi(x)>=0)
    else: return any((lo(x).flatten()<=0) & (hi(x).flatten()>=0))


# Binary methods
# ...


# Universal parser
def intervalise(x: Any,) -> Union[Interval,Any]:
    """
    This function casts an array-like structure into an Interval structure. 
    All array-like structures will be first coerced into an ndarray of floats.
    If the coercion is unsuccessful the following error is thrown: `ValueError: setting an array element with a sequence.`

    For example this is the expected behaviour:
    (*) an ndarray of shape (4,2) will be cast as an Interval of shape (4,).

    (*) an ndarray of shape (7,3,2) will be cast as an Interval of shape (7,3).

    (*) an ndarray of shape (3,2,7) will be cast as a degenerate Interval of shape (3,2,7).

    (*) an ndarray of shape (2,3,7) will be cast as an Interval of shape (3,7).

    (*) an ndarray of shape (2,3,7,2) will be cast as an Interval of shape (2,3,7).

    If an ndarray has shape with multiple dimensions having size 2, then the last dimension is intervalised.
    So, an ndarray of shape (7,2,2) will be cast as an Interval of shape (7,2) with the last dimension intervalised. 
    When the ndarray has shape (2,2) again is the last dimension that gets intervalised.

    It returns an interval only if the input is an array-like structure, otherwise it returns the following numpy error:
    `ValueError: setting an array element with a sequence.`

    """
    x_ = asarray(x, dtype=float)
    s = x_.shape
    two=[si==2 for si in s]
    if all(two): return Interval(lo=transpose(x_)[0],hi=transpose(x_)[1])
    elif any(two):
        if two[-1]: return Interval(lo=transpose(x_)[0],hi=transpose(x_)[1])
        else: 
            if (sum(two)==1) & (two[0]): return Interval(lo=x_[0],hi=x_[1])# there is only one dimension of size 2 and is the first one
        print('Array-like structure must have last dimension (or first) of size 2, for it to be coerced to Interval.')
        return Interval(lo=x_) 
    else: return Interval(lo=x_)


def sizeit(x:Interval) -> Interval:
    '''
    Takes an unsized scalar interval and turns it in to a sized one.
    '''
    if is_Interval(x):
        if x.scalar & x.unsized:
            return Interval(lo=[x.lo], hi=[x.hi])
    return x

def unsizeit(x:Interval) -> Interval:
    '''
    Takes a sized scalar interval and turns it in to a unsized one.

    '''
    if is_Interval(x):
        if x.scalar & x.unsized==False:
            return Interval(lo=x.lo[0], hi=x.hi[0])
    return x
