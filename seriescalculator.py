#!/usr/bin/env python3

"""
Math calculator
"""

from math import factorial
from functools import cache

def sin(x: int | float, terms: int = 20):
    alternate = 1
    output = 0
    for i in range(terms):
        n = 2 * i + 1
        output += alternate * (pow(x, n, mod=None) / factorial(n))
        alternate = -alternate
    return output

def sqrt(x: int | float, terms: int = 20, guess: int | float = 1):
    output = guess
    for _ in range(terms):
        output = (output + (x / output)) / 2
    return output

def pi(terms: int = 20, *, floatingpointclass: type = float):
    """
    terms: # of terms to compute
    floatingpointclass: Class of the floating point computation.
    Use a class with more precision to get a more precise answer.
    Must support floatingpointclass(0), __iadd__, and __mul__.
    """
    @cache
    def _dfactorial(n: int):
        if n == 0 or n == 1:
            return 1
        return n * _dfactorial(n - 2)
    cursum = floatingpointclass(0)
    for i in range(terms):
        cursum += _dfactorial(2*i)/_dfactorial(2*i+1)*(1/2)**i
    return cursum * 2