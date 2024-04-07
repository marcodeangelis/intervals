# Intervals

[![png](./logos/GitHub-Mark-32px.png)](https://github.com/marcodeangelis/intervals)[https://github.com/marcodeangelis/intervals](https://github.com/marcodeangelis/intervals)

[![codecov](https://codecov.io/gh/marcodeangelis/intervals/branch/main/graph/badge.svg?token=JM6Z8NDNUU)](https://codecov.io/gh/marcodeangelis/intervals) 
[![Build Status](https://github.com/marcodeangelis/intervals/actions/workflows/codecov.yml/badge.svg)](https://github.com/marcodeangelis/intervals/actions/workflows/codecov.yml/badge.svg)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.6205624.svg)](https://doi.org/10.5281/zenodo.6205624)

*intervals* is a library for interval computing in Python. 

The library implements Numpy vectorized interval arithmetic between array-like structures.  An `Interval` object is a wrapper of an `ndarray`. So just like an `ndarray` an `Interval` is iterable, indexable, and calculations are element-wise unless otherwise specified. Interval computing is emulated in the sense that all operations are done in floating-point arithmetic. We do not recommend  this library for rigorous computation. A proposal is currently under consideration for it to replace the floating-point apparatus with fixed-point or rational arithmetic. 

This is an __open source project__: we welcome contributions to enlarge and improve this code. If you see any error or problem, please open a new issue. If you want to join our team of developers, get in touch!

Disclaimer: Interval arithmetic is emulated in the sense that computations are *inclusive* w.r.t. the specified intervals but not *verified*. 

### Use this code
* To emulate interval arithmetic between array-like structures. 

### Do not use this code
* for __Verified computing__. If you need verified computations and outward-directed rounding you should use other software like: [IntLab](https://www.tuhh.de/ti3/rump/intlab/) or [Julia Intervals](https://juliaintervals.github.io).

### Why use this code
* It's free. 
* It's optimized for vector and matrix computations.


### Contact
`marco.de-angelis@strath.ac.uk`

## References
[1] Ramon E Moore. *Interval analysis*, volume 4. Prentice-Hall Englewood Cliffs, 1966.

[2] Arnold Neumaier. *Interval methods for systems of equations*. Number 37. Cambridge university press, 1990.

[3] Alefeld, G. and Mayer, G., 2000. *Interval analysis: theory and applications*. Journal of computational and applied mathematics, 121(1-2), pp.421-464.

[4] Jaulin, L., Kieffer, M., Didrit, O. and Walter, E., 2001. *Interval analysis*. In Applied interval analysis (pp. 11-43). Springer, London.

[5] Caprani, O., Madsen, K., & Nielsen, H. B. (2002). *Introduction to Interval Analysis*. http://www2.imm.dtu.dk/pubdb/p.php?1462

[6] Kearfott, R.B., et al. (2010). *Standardized notation in interval analysis* https://interval.louisiana.edu/preprints/Shary_n.pdf

[7] *IEEE Standard for Interval Arithmetic*, in IEEE Std 1788-2015 , vol., no., pp.1-97, 30 June 2015, doi: 10.1109/IEEESTD.2015.7140721. 

[8] *IEEE Standard for Interval Arithmetic (Simplified)*, in IEEE Std 1788.1-2017 , vol., no., pp.1-38, 31 Jan. 2018, doi: 10.1109/IEEESTD.2018.8277144. 



# Install
Upon activation of your virtual environment, return the following line in your CLI or terminal:

`pip install git+https://github.com/marcodeangelis/intervals.git`

More on [install](docs/install.md).

## Dependencies

Only Numpy is needed to use `intervals`. 

```
numpy>=1.22
```

We recommend also installing `matplotlib` for plotting.

# Use


## Imports
```python
from intervals.number import Interval as I
from intervals.methods import (lo,hi,mid,width,intervalise)
```


## Arithmetic between scalar intervals

Intervals are created using the endpoints notation. So let `x=[1,2]` and `y=[-3,-2]` be two scalar intervals,

```python
x=I(1,2)
print(x)
# [1.0,2.0]
y=I(-3,-2)
print(y)
# [-3.0,-2.0]
```

the four arithmetic operations between `x` and `y` are 

```python
print(x+y)
# [-2.0,0.0]
print(x-y)
# [3.0,5.0]
print(x*y)
# [-6.0,-2.0]
print(x/y)
# [-1.0,-0.33]
```

We can check that these operations are correct with __endpoints analysis__. For example, the addition is 

```python
xe = [lo(x),hi(x)]
ye = [lo(y),hi(y)]
xye= [xc+yc for xc in xe for yc in ye ]
print(min(xye))
# -2.0
print(max(xye))
# 0.0
```

## Properties of scalar intervals

We can also check that `x` and `y` are scalar with the property `scalar`.

```python
x.scalar
# True
```

`x` and `y` are unsized scalars, which means they cannot be iterated.

```python
print(len(x))
# 0
```
We can check if an interval is iterable with the property `unsized`.

```python
print(x.unsized)
# True
```
Unsized intervals have an empty shape just like ndarrays.

```python
x.shape
# ()
```

and have length `0`.

```python
len(x)
# 0
```

Scalar intervals can also be iterable or sized. For example, the following interval is a scalar.

```python
x_ = I([1],[2])
```
So `x_` is just like `x=[1,2]` in terms of computations, with the only difference of being sized. So the scalar interval `x_` is now 

(1) indexable, 

(2) iterable, and 

(3) sized.

```python
print(x_.scalar) # (0) scalar
# True
print(x_[0]) # (1) indexable
# [1.0,2.0]
for xi in x: # (2) iterable
    print(x)
# [1.0,2.0]
print(len(x)) # (3) sized
# 1
```

## Arithmetic between array-like intervals

Array-like intervals are intervals whose endpoints are array-like structures. We can define arrays of different shapes, for example:

(1) interval of shape (n,) __vector__, __1d array__.

(2) interval of shape (n,m) __matrix__, __2d array__.

(3) interval of shape (n,m,l) __3d, array__.

(4) interval of shape (n,m,...) __Nd, array__.

All computations between array-like intervals are elementwise, unless otherwise specified.

Two interval vectors `x` and `y` can be defined as follows.

```python
x = I(lo=[1,2,3,4],hi=[2,3,4,5])
print(x)
# [1.0,2.0]
# [2.0,3.0]
# [3.0,4.0]
# [4.0,5.0]
y = I(lo=[-1,-2,-3,-4],hi=[-1,-1,-1,-1])
print(y)
# [-1.0,-1.0]
# [-2.0,-1.0]
# [-3.0,-1.0]
# [-4.0,-1.0]
```
Arithmetic between vectors.

```python
print(x+y)
# [0.0,1.0]
# [0.0,2.0]
# [0.0,3.0]
# [0.0,4.0]
print(x-y)
# [2.0,3.0]
# [3.0,5.0]
# [4.0,7.0]
# [5.0,9.0]
print(x*y)
# [-2.0,-1.0]
# [-6.0,-2.0]
# [-12.0,-3.0]
# [-20.0,-4.0]
print(x/y)
# [-2.0,-1.0]
# [-3.0,-1.0]
# [-4.0,-1.0]
# [-5.0,-1.0]
```

We can check that the operations are done elementwise by iterating over the intervals.

```python
for xi,yi in zip(x,y): print(xi-yi)
# [2.0,3.0]
# [3.0,5.0]
# [4.0,7.0]
# [5.0,9.0]
```

Arithmetic between array-like and scalar intervals must also be available. 

Let us create a scalar interval `a`.

```python
a = I(-1,1)
```

Operations between vectors and scalars work as expected.

```python
print(a+x)
# [0.0,3.0]
# [1.0,4.0]
# [2.0,5.0]
# [3.0,6.0]
print(a-x)
# [-3.0,0.0]
# [-4.0,-1.0]
# [-5.0,-2.0]
# [-6.0,-3.0]
print(a*x)
# [-2.0,2.0]
# [-3.0,3.0]
# [-4.0,4.0]
# [-5.0,5.0]
print(a/x)
# [-1.0,1.0]
# [-0.5,0.5]
# [-0.33,0.33]
# [-0.25,0.25]
```

## Parser

Any array-like structure whose shape is `(n,m,...,2)` can be cast to an interval structure. For example, the following structure can be seen as a matrix of intervals.

```python
a = [[[1,2], [2,3], [4,5]],
      [[-1,2],[-2,1],[3,5]],
      [[0,2], [3,4], [6,8]]]
```
 The structure has shape `(3,3,2)`, thus is cast to an interval of shape `(3,3)`.

```python
x = intervalise(a)
print(x.shape)
# (3,3)
print(x)
# [1. 2.] [-1.  2.] [0. 2.]
# [2. 3.] [-2.  1.] [3. 4.]
# [4. 5.] [3. 5.] [6. 8.]
```

<!-- Any 2d-array with either first or second dimension of size two also qualifies as an interval. So the parser `intervalise` will turn them into an interval.  -->

<!-- For example, the data structure: -->

The structure `b` with shape `(4,2)`,

```python
b = [[1,2],[2,3],[4,5],[5,6]]
```

is the interval vector of shape `(4,)`

```python
x = intervalise(b)
print(x.shape)
# (4,)
print(x)
# [1.0,2.0]
# [2.0,3.0]
# [4.0,5.0]
# [5.0,6.0]
```

<!-- Another example is the following data structure: -->

Sometimes an interval is given as a concatenation of two precise structures. The array-like equivalent structure will have shape (2,m,n,...). In this case, it the use of `intervalise` is discouraged, because the last dimension may be 2. The last dimension takes priority over the first, resulting in the wrong interval structure. In this case, the constructor `Interval` should be used instead. Otherwise, `intervalise` should be used with the `index` flag set to `0`. The two behaviours are exemplified as follows.

```python
a = [[1,2,4,5],[2,3,5,6]]
```

This data structure `a = [[1,2,4,5],[2,3,5,6]]` is seen as a list of left and right endpoints.

<!-- which has shape `(2,4)`. The first dimension has size two, so it can also be parsed as an interval. `intervalise` will turn this structure in an interval vector: -->

```python
x = I(lo=a[0],hi=a[1])
print(x.shape)
# (4,)
print(x)
# [1.0,2.0]
# [2.0,3.0]
# [4.0,5.0]
# [5.0,6.0]
```
or

```python
x = intervalise(a,index=0)
print(x.shape)
# (4,)
print(x)
# [1.0,2.0]
# [2.0,3.0]
# [4.0,5.0]
# [5.0,6.0]
```

In case of ambiguity, structures of shape `(2,2)` the last dimension is prioritised over the first. 

```python
a = [[1,2],[5,6]]
```

becomes

```python
x = intervalise(a)
print(x.shape)
# (2,)
print(x)
# [1.0,2.0]
# [5.0,6.0]
```

## Efficiency

Computing with intervals should take at most four times the computational effort required for computing with floats.  However, because `Interval` is a wrapper of the `ndarray`, there is some overhead due to casting, branching (if-statements) and masking. 

A simple speed test shows that multiplying two large `Interval` matrices takes about 15 times more computing time than multiplying two large `ndarray` matrices.

```python
from intervals.random import create_two_large_interval_matrices

shape=(10_000,10_000)
x,y = create_two_large_interval_matrices(shape)
t0 = time.time()
z=x*y
t1 = time.time()
print(t1-t0)
# 6.893776178359985 s
t0 = time.time()
z_lo=x.lo*y.lo
t1 = time.time()
print(t1-t0)
# 0.4369039535522461 s
```

Graphing array size against running time reveals the performance of `Interval` against `ndarray`.

![png](docs/figures/versus_ndarray.png)

The above comparison was done between matrices of shape: `(100,100)`, `(500,500)`, `(1_000,1_000)`, `(5_000,5_000)`, `(10_000,10_000)`, and `(20_000,20_000)`.