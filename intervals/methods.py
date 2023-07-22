"""
------------------------------
cre: Feb 2022

web: github.com/marcodeangelis
org: Univerity of Liverpool

MIT License
------------------------------

These methods are designed to behave neutrally on non-interval inputs. 
So, if a non-interval is passed rules of standard arithmetic apply.

Interval to float methods, IR -> R:

Interval to bool methods, IR -> {0,1}: 

Binary operations, IR2 -> IR
Unary operations, IR -> IR

Parser, Rn -> IRm: 
This method turns an array of compatible dimension into an interval (array).

Subintervalisation methods, IR -> IRn.

"""
from __future__ import annotations
from typing import (Sequence, Sized, Iterable, Optional, Any, Tuple, Union)

from itertools import product

import numpy
from numpy import (ndarray,asarray,transpose,vstack,linspace,zeros,argmax)

from intervals.number import (Interval, MACHINE_EPS)

numpy_min = numpy.min
numpy_max = numpy.max
numpy_sqrt= numpy.sqrt
numpy_exp = numpy.exp
numpy_sum = numpy.sum

# Properties or maybe attributes of the interval class. These apply to all interval-like objects.

# Interval to float methods, Unary.
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

def width(x: Interval) -> Union[float, ndarray]:
    """
    Return the width of an Interval object.

    If x is not of class Interval, input is returned.
    
    """
    if is_Interval(x): return hi(x)-lo(x)
    return x

def rad(x: Interval) -> Union[float, ndarray]:
    """
    Return the radius of an Interval object.

    If x is not of class Interval, input is returned.
    
    """
    if is_Interval(x): return (hi(x)-lo(x))/2
    return x

def mid(x: Interval) -> Union[float, ndarray]:
    """
    Return the midpoint of an Interval.

    If x is not of class Interval, input is returned.
    
    """
    if is_Interval(x): return (hi(x)+lo(x))/2
    return x

def mig(x):
    pass
def mag(x):
    pass

# Interval to interval methods. Unary.
def abs(x:Interval):
    """
    Return the absolute value of an Interval.

    If x is not of class Interval, absolute value is returned assuming input is numerical.

    If x is neither a number (neither Interval not numeric), numpy will throw an exception.
    
    """
    x_lo_abs =  numpy.abs(lo(x))
    if is_Interval(x):
        zero_in_x = contain(x,0)
        x_hi_abs = numpy.abs(hi(x))
        a = numpy.min((x_lo_abs, x_hi_abs),axis=0)
        if x.unsized: 
            if zero_in_x: a = 0
        else: a[zero_in_x] = 0
        b = numpy.max((x_lo_abs, x_hi_abs),axis=0)
        return Interval(a,b)
    return x_lo_abs

def sqrt(x:Interval):
    """
    Return the square root of an Interval.

    If x is not of class Interval, the square root is returned assuming input is numerical.

    If x is neither a number (neither Interval not numeric), numpy will throw an exception.
    
    """
    x_lo_sqrt =  numpy.sqrt(lo(x))
    if is_Interval(x):
        x_hi_sqrt = numpy.sqrt(hi(x))
        return Interval(x_lo_sqrt,x_hi_sqrt)
    return x_lo_sqrt

def exp(x:Interval):
    if is_not_Interval(x): return numpy.exp(x)
    return Interval(numpy_exp(lo(x)),numpy_exp(hi(x)))
    

# Binary methods between two intervals
# 2-interval to interval. Bianry.
def max(x:Interval, y:Interval):
    if all([is_not_Interval(x),is_not_Interval(y)]):
        return numpy.max((x,y), axis=0)
    a = numpy.max((lo(x),lo(y)), axis=0)
    b = numpy.max((hi(x),hi(y)), axis=0)
    return Interval(a,b)
def min(x:Interval, y:Interval): 
    if all([is_not_Interval(x),is_not_Interval(y)]):
        return numpy.min((x,y), axis=0)
    a = numpy.min((lo(x),lo(y)), axis=0)
    b = numpy.min((hi(x),hi(y)), axis=0)
    return Interval(a,b)

def set_difference(x:Interval,y:Interval):
    pass

def split_interval(x:Interval,y:float=None):
    if y is None: return Interval(lo(x),mid(x)), Interval(mid(x),hi(x))

    x1, x2 = Interval(lo(x),hi(x)), Interval(lo(x),hi(x)) # TODO: implement copy method
    y_in_x = contain(x,y)
    if x.unsized: 
        if ~y_in_x: return x1,x2
        return Interval(lo=lo(x),hi=y),  Interval(lo=y,hi=hi(x))
    else: pass
        # x1[y_in_x] = Interval(lo(x)[y_in_x],hi=y)
        # x2[y_in_x] = Interval(y,hi=hi(x)[y_in_x])
    return x1,x2

# Interval to ndarray[float]
# def linspace():pass

# Interval to float methods, Binary.
def union(): pass
def intersection(): pass
def difference(): pass


# Interval to bool methods, Unary.
def is_Interval(x:Any) -> bool: return x.__class__.__name__ == 'Interval'
def is_not_Interval(x:Any) -> bool: return x.__class__.__name__ != 'Interval'

def straddle_zero(x: Interval) -> bool:
    if x.unsized: return (lo(x)<=0) & (hi(x)>=0)
    else: return any((lo(x).flatten()<=0) & (hi(x).flatten()>=0))

# Interval to bool methods, Binary.
# ...
def intersect(x:Interval, y:Interval): return ~((x<y) | (y<x)) # commutative
def contain(x:Interval, y:Interval):  return (lo(x)<=lo(y)) & (hi(x)>=hi(y)) # x contain y

# Universal parser
def intervalise(x_: Any, index = -1) -> Union[Interval,Any]:
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

    In case of ambiguity, e.g. (2,5,2), now the first dimension can be forced to be intervalised, selecting index=0, default is -1.

    It returns an interval only if the input is an array-like structure, otherwise it returns the following numpy error:
    `ValueError: setting an array element with a sequence.`

    """
    if x_.__class__.__name__=='Interval': return x_
    x = asarray(x_, dtype=float)
    s = x.shape
    two=[si==2 for si in s]
    if all(two): return Interval(lo=transpose(x)[0],hi=transpose(x)[1])
    elif any(two):
        if two[-1]: return Interval(lo=transpose(x)[0],hi=transpose(x)[1]) # the last dimension has size 2
        elif two[0]: return Interval(lo=x[0],hi=x[1])
        elif (two[-1]) & (two[0]): # this is the ambiguous case (2,3,5,2)
            if index == 0: return Interval(lo=x[0],hi=x[1]) # first dimension gets intervalised
            elif index == -1: return Interval(lo=transpose(x)[0],hi=transpose(x)[1])
            # if (sum(two)==1) & (two[0]): return Interval(lo=x[0],hi=x[1])# there is only one dimension of size 2 and is the first one
        print('Array-like structure must have last dimension (or first) of size 2, for it to be coerced to Interval.')
        return Interval(lo=x) 
    else: return Interval(lo=x)

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

def subintervalise(x_:Interval, n:Union[int,tuple]=0):
    x = intervalise(x_)
    d = len(x.shape) # dimension of the array
    if n==0: return x
    elif n==1: return x # should return a subtiling (sized interval)
    if x.scalar:  # or x.scalar == True
        xx = linspace(x.lo,x.hi,num=n+1)
        return intervalise(vstack([xx[:-1], xx[1:]]))
    elif d==1: ## x.shape = (m,)
        m = x.shape[0] # size of 1d array
        if type(n)==int: n=m*[n] # differential split number 
        X_sub = []
        for i,xi in enumerate(x):
            xxi = subintervalise(xi,n=n[i]) # recursion
            X_sub.append(sizeit(xxi).val)
        return intervalise(asarray(list(product(*X_sub)),dtype=float))
#     elif len(x.shape)>1: pass # TODO: implement space-product subintervalization with arrays of dimension greater than 2.
    else: print('!! Subtiling not yet supported for interval arrays of dimension 2 or larger. Input will be returned.')
    return x


def reconstitute(x_:Interval):
    x = intervalise(x_)
    d = len(x.shape) # dimension of the subtiling ==1 if scalar, ==2 if 1d array
    if d==1: return Interval(lo=numpy.min(x.lo), hi=numpy.max(x.hi))
    elif d==2: return Interval(lo=numpy.min(x.lo,axis=1), hi=numpy.max(x.hi,axis=1))
    else: print('!! Subtiling not yet supported for interval arrays of dimension 2 or larger.')
    return x

def space_product(x_:Union[ndarray,Interval],y_:Union[ndarray,Interval]): return asarray(tuple(product(x_,y_)))

def bisect(x_:Interval,i:int=None):
    """
    :x_: Interval of shape (n,)

    Bisect the largest box if i is None.
    """
    x = intervalise(x_)
    if x.scalar: 
        mid_x = mid(x)
        return Interval(lo(x),mid_x), Interval(mid_x,hi(x))
    if i is not None: split_index = i
    else: 
        w = width(x)
        split_index = argmax(w)
    d=x.shape[0] 
    n=[0]*d
    n[split_index]=2 # ex: (0,0,2,0,0,0) if interval of dim 6 has third dimension bisected
    x_bisect = subintervalise(x,n=tuple(n))
    return x_bisect[0], x_bisect[1]
