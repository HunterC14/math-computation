#!/usr/bin/env python3

"""
Approximator

Approximates floating point numbers as fractions.
"""

def _find_mediant(downbound: tuple[int, int], upbound: tuple[int, int]) -> tuple[int, int]:
    mediant = (downbound[0] + upbound[0], downbound[1] + upbound[1])
    return mediant

def _bet0_1approx(num: float, times: int = 20) -> tuple[int, int]:
    downbound = (0, 1)
    upbound = (1, 1)
    for _ in range(times):
        mediant = _find_mediant(downbound, upbound)
        fmed = mediant[0] / mediant[1]
        if fmed > num:
            upbound = mediant
        elif fmed < num:
            downbound = mediant
        else:
            return mediant
    mediant = _find_mediant(downbound, upbound)
    return mediant

def approximate(num: float, times: int = 20) -> tuple[int, int]:
    fpart = num % 1
    intpart = num - fpart
    fpart_approx = _bet0_1approx(fpart, times)
    denominator = fpart_approx[1]
    numerator = int(intpart * denominator + fpart_approx[0])
    return (numerator, denominator)