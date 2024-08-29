#!/usr/bin/env python3

"""
BaseLib (no pun intended)

BaseLib lets you use bases of all kinds.
Current working ones:

"""

try:
    from rationals import Fraction
except ModuleNotFoundError:
    from .rationals import Fraction

class FractBase(object):
    """
    FractBase

    If nums (digits) = [1, 2, 3, 4],
    and num (base f) = 123.4,
    then dp = 2
    the decimal point is the place AFTER the index dp.
    """
    def __init__(self, base: Fraction, nums: list[int], dp: int):
        self.baseNum = base.numerator
        self.baseDen = base.denominator
        self.nums = nums
        self.dp = dp
    def __str__(self):
        num = self.nums[:]
        num.insert(self.dp + 1, '.')
        snum = "".join([str(n) for n in num])
        return f"Base {self.baseNum}/{self.baseDen} {snum}"
    def __repr__(self):
        return str(self)
    def into_float(self):
        return fractbase_to_float(self)

def fractbase_to_float(num: FractBase) -> float:
    nums = num.nums
    dp = num.dp
    base = Fraction(num.baseNum, num.baseDen)
    out = 0
    for i, digit in enumerate(nums):
        place = dp - i
        value = digit * base ** place
        out += value
    return out

def int_to_fractbase(num: int, base: Fraction) -> FractBase:
    rnums = []
    while True:
        whole, digit = divmod(num, base.numerator)
        rnums.append(digit)
        if whole == 0:
            break
        num = whole * base.denominator
    nums = rnums[::-1]
    fb = FractBase(base, nums, len(nums) - 1)
    return fb

def test():
    x = int_to_fractbase(265, Fraction(7, 3))
    assert x.into_float() == 265

test()