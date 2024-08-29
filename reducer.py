#!/usr/bin/env python3
try:
    from prime_checker import generate, check
except ModuleNotFoundError:
    from .prime_checker import generate, check
from functools import cache
from math import gcd
@cache
def old_reduce(a: int, b: int) -> tuple[int, int]:
    if b == 0:
        raise ValueError("Cannot reduce a rational with a value of NaN.")
    elif a == 0:
        return (0, 1)
    else:
        for prime in generate():
            if b == 1:
                return (int(a), 1)
            elif a == 1:
                return (1, int(b))
            elif a == b:
                return (1, 1)
            elif check(a) and check(b):
                return (int(a), int(b))
            elif (check(a) and b % a != 0) or (check(b) and a % b != 0):
                return (int(a), int(b))
            elif prime > min(a, b):
                return (int(a), int(b))
            while True:
                if (a % prime) + (b % prime) == 0:
                    a /= prime
                    b /= prime
                else:
                    break
@cache
def reduce(a: int,b: int) -> tuple[int, int]:
    rval = gcd(a,b)
    return (a//rval,b//rval)