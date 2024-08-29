#!/usr/bin/env python3

"""
Multi-Precision Math Library/Module

Details:
MPMath.sign:
-  0: Zero
-  1: Positive
- -1: Negative
"""

from __future__ import annotations
from typing import Literal

try:
    from . import String
except ImportError:
    import String

defaultpallete = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

class MPMath:
    def __init__(self, number: int | float | MPMath, base: int = 10, strpallete: str | None = defaultpallete):
        numtype = type(number)
        if numtype is MPMath:
            self.number = number.number
            self.exponent = number.exponent
            self.base = number.base
            self.sign = number.sign
            self.pallete = number.pallete if strpallete is None else strpallete
            return
        self.base = base
        self.pallete = strpallete
        if numtype is int:
            if number == 0:
                self.number = []
                self.exponent = 0
                self.sign = 0
                self.base = base
                return
            self.number = list(String.separate(abs(number), base))
            self.exponent = len(self.number) - 1
            while self.number[-1] == 0:
                self.number = self.number[:-1]
            self.sign = 2 * (int(number > 0) - .5)
        elif numtype is float:
            exponent = 0
            while int(number) != number:
                exponent -= 1
                number *= base
            self.number = list(String.separate(int(number), base))
            while number >= base:
                number /= base
                exponent += 1
            self.exponent = exponent
            self.sign = int(number > 0)
        else:
            raise TypeError(f"Invalid type: {numtype}")
    def withsign(self, sign: Literal[-1, 0, 1] = 1) -> MPMath:
        copy = MPMath(self)
        copy.sign = sign
        return copy
    @property
    def posisign(self):
        return self.withsign(1)
    @property
    def negasign(self):
        return self.withsign(-1)
    @staticmethod
    def create(numlist: list[int], exponent: int, base: int, sign: int, pallete: str = defaultpallete) -> MPMath:
        mathobj = object.__new__(MPMath)
        mathobj.number = numlist
        mathobj.exponent = exponent
        mathobj.base = base
        mathobj.pallete = pallete
        mathobj.sign = sign
        return mathobj
    def _opajust(self: MPMath, other: MPMath):
        mynum = [0] + self.number
        othernum = [0] + other.number
        mylennum = self.exponent - len(mynum) + 1
        otherlennum = other.exponent - len(othernum) + 1
        if mylennum > otherlennum:
            ext = mylennum - otherlennum
            mynum.extend([0 for _ in range(ext)])
        else:
            ext = otherlennum - mylennum
            othernum.extend([0 for _ in range(ext)])
        if len(mynum) > len(othernum):
            othernum = [0 for _ in range(len(mynum) - len(othernum))] + othernum
        else:
            mynum = [0 for _ in range(len(othernum) - len(mynum))] + mynum
        return mynum, othernum, ext
    def __gt__(self, other: MPMath | int | float):
        if type(other) is not MPMath:
            return self + MPMath(other, self.base)
        if other.base != self.base:
            raise ValueError("Different bases")
        if self.sign < other.sign:
            return False
        if self.sign > other.sign:
            return True
        if self.exponent > other.exponent:
            return True
        elif other.exponent > self.exponent:
            return False
        mynum, othernum, _ = self._opajust(other)
        for mydigit, otherdigit in zip(mynum, othernum, strict=True):
            if mydigit > otherdigit:
                return True
            if otherdigit > mydigit:
                return False
        return False
    def _lt__(self, other: MPMath | int | float):
        if type(other) is not MPMath:
            return self + MPMath(other, self.base)
        if other.base != self.base:
            raise ValueError("Different bases")
        if self.sign > other.sign:
            return False
        if self.sign < other.sign:
            return True
        if self.exponent > other.exponent:
            return True
        elif other.exponent > self.exponent:
            return False
        mynum, othernum, _ = self._opajust(other)
        for mydigit, otherdigit in zip(mynum, othernum, strict=True):
            if mydigit < otherdigit:
                return True
            if otherdigit < mydigit:
                return False
        return False
    def reduce(self):
        i = 0
        while self.number[i] == 0:
            i += 1
        self.number = self.number[i:]
    def __eq__(self, other: MPMath | int | float):
        if type(other) is not MPMath:
            return self + MPMath(other, self.base)
        if self.sign == other.sign:
            if self.sign == 0:
                return True
        else:
            return False
        if other.base != self.base:
            raise ValueError("Different bases")
        if self.exponent != other.exponent:
            return False
        self.reduce()
        other.reduce()
        if self.number != other.number:
            return False
        return True
    def __le__(self, other: MPMath | int | float):
        return self < other or self == other
    def __ge__(self, other: MPMath | int | float):
        return self > other or self == other
    def __add__(self, other: MPMath | int | float) -> MPMath:
        if type(other) is not MPMath:
            return self + MPMath(other, self.base)
        if other.base != self.base:
            raise ValueError("Different bases")
        if other.sign == 0:
            return self
        elif other.sign == -1:
            if self.sign == 1:
                return self.posisign - other.posisign
            return -(self.posisign + other.posisign)
        elif self.sign == -1:
            return other.posisign - self.posisign
        mynum, othernum, _ = MPMath._opajust(self, other)
        newnum = []
        carry = 0
        for nA, nB in zip(mynum[::-1], othernum[::-1], strict=True):
            num = nA + nB + carry
            carry, nextnum = divmod(num, self.base)
            newnum.append(nextnum)
        newnum = newnum[::-1]
        newexp = self.exponent
        newexp += len(newnum) - len(mynum)
        if newnum[0] == 0:
            newnum = newnum[1:]
        while newnum[-1] == 0:
            newexp += 1
            newnum = newnum[:-1]
        return MPMath.create(newnum, newexp, self.base, 1)
    def __neg__(self):
        return self.withsign(-self.sign)
    def __sub__(self, other: MPMath | int | float) -> MPMath:
        if type(other) is not MPMath:
            return self - MPMath(other, self.base)
        if other.base != self.base:
            raise ValueError("Different bases")
        if other.sign == 0:
            return self
        if other.sign == -1:
            if self.sign == 1:
                return self.posisign + other.posisign
            return other.posisign - self.posisign
        if self.sign == -1:
            return -(self.posisign + other.posisign)
        if self.sign == 0:
            return other.withsign(-other.sign)
        if other > self:
            return -(other.posisign - self.posisign)
        mynum, othernum, _ = MPMath._opajust(self, other)
        newnum = []
        carry = 0
        for nA, nB in zip(mynum[::-1], othernum[::-1], strict=True):
            num = nA - nB + carry
            carry, nextnum = divmod(num, self.base)
            newnum.append(nextnum)

        newnum = newnum[::-1]
        newexp = self.exponent
        while newnum[-1] == 0:
            newexp += 1
            newnum = newnum[:-1]
        newexp += len(newnum) - len(mynum) + 1
        return MPMath.create(newnum, newexp, self.base, 1)
    def __str__(self):
        self.reduce()
        output = ""
        if self.sign == -1:
            output += "-"
        for digit in self.number:
            output += self.pallete[digit]
        output += "0" * (self.exponent - len(self.number) + 1)
        output = output[:self.exponent+1]+'.'+output[self.exponent+1:]
        return output
    def __repr__(self):
        return str(self)
MPMath(50) - 1