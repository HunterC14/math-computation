#!/usr/bin/env python3
from __future__ import annotations
try:
    import reducer
except ModuleNotFoundError:
    from . import reducer
import math
import typing

reduce = reducer.reduce
def _funcfract(function: typing.Callable[[int, int], int], a, b, c, d, run_ls=True):
    fract1_rev = _xor(_check(a),_check(b))
    fract2_rev = _xor(_check(c),_check(d))
    a = abs(a)
    b = abs(b)
    c = abs(c)
    d = abs(d)
    (a, b) = reduce(a, b)
    (c, d) = reduce(c, d)
    if fract1_rev:
        a = -a
    if fract2_rev:
        c = -c
    output = function((a*d),(b*c))
    if run_ls:
        output = reduce(output, b*d)
    return output
def _xor(bool1, bool2):
    return bool1^bool2
def _xnor(bool1, bool2):
    return bool(bool1) == bool(bool2)
def _mul(a, b, c, d):
    if _xnor(not _xor(_check(a),_check(b)),not _xor(_check(c),_check(d))):
        return reduce((a*c),(b*d))
    else:
        a = abs(a)
        b = abs(b)
        c = abs(c)
        d = abs(d)
        output = reduce((a*c),(b*d))
        output = list(output)
        output[0] = -output[0]
        output = (output[0], output[1])
        return output
def _div(a, b, c, d):
    if _xnor(not _xor(_check(a),_check(b)),not _xor(_check(c),_check(d))):
        return reduce((a*d),(b*c))
    else:
        a = abs(a)
        b = abs(b)
        c = abs(c)
        d = abs(d)
        output = reduce((a*d),(b*c))
        output = list(output)
        output[0] = -output[0]
        output = (output[0], output[1])
        return output
def _check(n):
    if n < 0:
        return True
    else:
        return False
def _eq(a, b, c, d):
    return reduce(a, b) == reduce(c, d)
def add(a, b, c, d):
    return _funcfract(lambda x, y: x+y, a, b, c, d)
def subtract(a, b, c, d):
    return _funcfract(lambda x, y: x-y, a, b, c, d)
def multiply(a, b, c, d):
    return _mul(a, b, c, d)
def divide(a, b, c, d):
    return _div(a, b, c, d)
def gt(a, b, c, d):
    return _funcfract(lambda x, y: x > y, a, b, c, d, False)
def lt(a, b, c, d):
    return _funcfract(lambda x, y: x < y, a, b, c, d, False)
def ge(a, b, c, d):
    return _funcfract(lambda x, y: x >= y, a, b, c, d, False)
def le(a, b, c, d):
    return _funcfract(lambda x, y: x <= y, a, b, c, d, False)
def eq(a, b, c, d):
    return _eq(a, b, c, d)
def rationalize(a, b):
    return a / b
def _fInteger(x):
    return Integer(int(x))
class Fraction(object):
    def __new__(cls, numerator: int, denominator: int):
        self = object.__new__(cls)
        if isinstance(numerator, int):
            pass
        else:
            raise TypeError("Numerator must be an integer.")
        if isinstance(denominator, int):
            pass
        else:
            raise TypeError("Denominator must be an intiger.")
        (self.numerator, self.denominator) = reduce(numerator, denominator)
        if self.denominator == 1:
            return Integer(self.numerator)
        return self
    def __init__(self, numerator: int, denominator: int):
        del numerator, denominator # the params were just for annotations
        self.numerator: int
        self.denominator: int
    def __add__(self, other: Integer | Fraction):
        if isinstance(other, Integer):
            return self + other.integer
        return Fraction(*add(self.numerator, self.denominator, other.numerator, other.denominator))
    def __sub__(self, other: Integer | Fraction):
        if isinstance(other, Integer):
            return self - other.integer
        return Fraction(*subtract(self.numerator, self.denominator, other.numerator, other.denominator))
    def __mul__(self, other: Integer | Fraction):
        if isinstance(other, Integer):
            return self * other.integer
        return Fraction(*multiply(self.numerator, self.denominator, other.numerator, other.denominator))
    def __truediv__(self, other: Integer | Fraction):
        if isinstance(other, Integer):
            return self / other.integer
        return Fraction(*divide(self.numerator, self.denominator, other.numerator, other.denominator))
    def __floordiv__(self, other: Integer | Fraction):
        if isinstance(other, Integer):
            return _fInteger(self.decimalize() // other.intiger)
        return _fInteger(self.decimalize() // other.decimalize())
    def __gt__(self, other: Integer | Fraction):
        if isinstance(other, Integer):
            return self.decimalize() > other.integer
        return gt(self.numerator, self.denominator, other.numerator, other.denominator)
    def __lt__(self, other: Integer | Fraction):
        if isinstance(other, Integer):
            return self.decimalize() < other.integer
        return lt(self.numerator, self.denominator, other.numerator, other.denominator)
    def __ge__(self, other: Integer | Fraction):
        if isinstance(other, Integer):
            return self.decimalize() >= other.integer
        return ge(self.numerator, self.denominator, other.numerator, other.denominator)
    def __le__(self, other: Integer | Fraction):
        if isinstance(other, Integer):
            return self.decimalize() <= other.integer
        return le(self.numerator, self.denominator, other.numerator, other.denominator)
    def __eq__(self, other: Integer | Fraction):
        if isinstance(other, Integer):
            return self.decimalize() == other.integer
        return eq(self.numerator, self.denominator, other.numerator, other.denominator)
    def __ne__(self, other: Integer | Fraction):
        return not (self == other)
    def __repr__(self):
        reduced = reduce(self.numerator,self.denominator)
        reduced_numerator = reduced[0]
        reduced_denominator = reduced[1]
        return "Fraction(%d,%d)" % (reduced_numerator,reduced_denominator)
    def __str__(self):
        return repr(self)
    def __radd__(self, other: int | float):
        return self + other
    def __rsub__(self, other: int | float):
        return -self + other
    def __rmul__(self, other: int | float):
        return self * other
    def __bool__(self):
        return self != Integer(0)
    def decimalize(self):
        return rationalize(self.numerator, self.denominator)
    def extract(self):
        return (self.numerator, self.denominator)
    def __neg__(self):
        self.numerator = -self.numerator
        return self
    def __pow__(self, other: int | Integer, mod: None = None):
        if mod is not None:
            raise NotImplementedError("mod must be None")
        if isinstance(other, int):
            pass
        elif isinstance(other, Integer):
            other = other.integer
        else:
            raise NotImplementedError(f"cannot POW with exp {type(other)}")
        if other == 0:
            return Integer(1)
        num = self.numerator ** other
        den = self.denominator ** other
        nf = Fraction(num, den)
        return nf
    @property
    def decimalized(self):
        return self.decimalize()
class Integer(object):
    def __init__(self, integer: int):
        if isinstance(integer, int):
            self.integer: int = integer
        else:
            raise TypeError(str(integer)+" is not an integer.")
    def __add__(self, other: Integer | Fraction):
        if isinstance(other, int):
            return Integer(self.integer+other)
        elif isinstance(other, Fraction):
            return other + self
        return Integer(self.integer+other.integer)
    def __sub__(self, other: Integer | Fraction):
        if isinstance(other, int):
            return Integer(self.integer-other)
        elif isinstance(other, Fraction):
            return other - self
        return Integer(self.integer-other.integer)
    def __mul__(self, other: Integer | Fraction):
        if isinstance(other, int):
            return Integer(self.integer*other)
        elif isinstance(other, Fraction):
            return other * self
        return Integer(self.integer*other.integer)
    def __truediv__(self, other: Integer | Fraction):
        if isinstance(other, int):
            return Fraction(self.integer,other)
        elif isinstance(other, Fraction):
            return other / self
        return Fraction(self.integer, other.integer)
    def __floordiv__(self, other: Integer | Fraction):
        if isinstance(other, int):
            return Integer(self.integer // other)
        elif isinstance(other, Fraction):
            return Integer(math.floor((self / other).decimalize()))
        return Integer(math.floor((self / other).decimalize()))
    def __radd__(self, other: Integer | Fraction | int):
        return self + other
    def __rsub__(self, other: Integer | Fraction | int):
        return -self + other
    def __rmul__(self, other: Integer | Fraction | int):
        return self * other
    def __gt__(self, other: Integer | Fraction | int):
        if isinstance(other, int):
            return self.integer > other
        elif isinstance(other, Fraction):
            return other <= self
        return self.integer > other.integer
    def __lt__(self, other: Integer | Fraction | int):
        if isinstance(other, int):
            return self.integer < other
        elif isinstance(other, Fraction):
            return other >= self
        return self.integer < other.integer
    def __ge__(self, other: Integer | Fraction):
        return not (self < other)
    def __le__(self, other: Integer | Fraction):
        return not (self > other)
    def __eq__(self, other: Integer | Fraction | int):
        if isinstance(other, int):
            return self.integer == other
        elif isinstance(other, Fraction):
            return other == self
        return self.integer == other.integer
    def __ne__(self, other: Integer | Fraction | int):
        return not (self == other)
    def __repr__(self):
        return "Integer(%d)" % (self.integer)
    def __str__(self):
        return repr(self)
    def __pow__(self, other: Integer | int, mod: int | None = None):
        if isinstance(other, Integer):
            exp = other.integer
        else:
            exp = other
        ni = Integer(pow(self.integer, exp, mod))
        return ni





