#!/usr/bin/env python3
from math import log
from typing import Generator, Any
def getdigit(val: int, digit:int, base:int=10) -> int:
    return ((val - val % (base ** digit)) // (base ** digit)) % base
def separate(val: int, base:int=10) -> Generator[int, Any, None]:
    nDigits = int(log(val, base))
    for i in range(nDigits, -1, -1):
        yield getdigit(val, i, base)
def stringify(val: int, base:int=10, palletefunc=str):
    output = ""
    for digit in separate(val, base):
        output += palletefunc(digit)
    return output
def printout(val: int, base:int=10, palletefunc=str):
    for digit in separate(val, base):
        print(palletefunc(digit),end="")
    print()
def pallete_wrapper(pallete: dict):
    def palletefunc(digit: int):
        return pallete[digit]
    return palletefunc
def pallete_enumerator(palletestr: str):
    pallete = {}
    for i, char in enumerate(palletestr):
        pallete[i] = char
    return pallete_wrapper(pallete)
def unstr(numlist: list[int], base: int):
    num = 0
    for i, numdigit in enumerate(numlist[::-1]):
        num += numdigit * base ** i
    return num
def main():
    from calculator import calculate_expression
    expression = input("Type an expression: ").strip().lower()
    printout(calculate_expression(expression))
if __name__ == "__main__":
    main()