#!/usr/bin/env python3

"""
Math calculator
"""

from math import factorial

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