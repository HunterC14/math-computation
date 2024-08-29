#!/usr/bin/env python3
def generate(maximum=None):
    primes = []
    tocheck = 2
    loops = 0
    while True:
        if maximum is not None:
            if loops >= maximum:
                break
        isprime = True
        limit = tocheck ** 0.5
        for prime in primes:
            if prime > limit:
                break
            if tocheck % prime == 0:
                isprime = False
                break
        if isprime:
            primes.append(tocheck)
            loops += 1
            yield tocheck
        tocheck += 1
    return None
def check(tocheck_in):
    if tocheck_in in (0,1):
        return False
    elif int(tocheck_in) != tocheck_in:
        return None
    else:
        primes = []
        tocheck = 2
        output = True
        tocheck_in_limit = tocheck_in ** 0.5
        while True:
            isprime = True
            tocheck_limit = tocheck ** 0.5
            if tocheck > tocheck_in_limit:
                break
            for prime in primes:
                if prime > tocheck_limit:
                    break
                if tocheck % prime == 0:
                    isprime = False
                    break
            if isprime:
                primes.append(tocheck)
                if tocheck_in % tocheck == 0:
                    output = False
                    break
            tocheck += 1
        return output
def sieve_gen(maximum: int) -> list:
    primechecks = [True for _ in range(maximum)]
    primechecks[0] = False
    sqrt = maximum**.5
    val = 1
    while True:
        if val > sqrt:
            break
        if primechecks[val]:
            for i, istrue in enumerate(primechecks):
                if i <= val:
                    continue
                if (i+1) % (val+1) == 0:
                    primechecks[i] = False
        val += 1
    primes = [i+1 for i, istrue in enumerate(primechecks) if istrue]
    return primes
def allprimes(list_):
    primes = list(filter(check, list_))
    return primes
if __name__ == "__main__":
    print("Choices:\n1: check a number,\n2: generate as big a prime as can find,\n3: get all the primes in a list")
    choice = input("Choice: ").strip()
    if choice == "1":
        tocheck = int(input("N to check: "))
        print(check(tocheck))
    elif choice == "2":
        try:
            [print(f"This is prime {i}, and the prime is {p}") for i, p in enumerate(generate())]
        except KeyboardInterrupt:
            print("\n\x1b[AClosing process")
    elif choice == "3":
        import json
        lst = json.loads(input("JSON: ").strip())
        if isinstance(lst, list):
            print(allprimes(lst))
        else:
            print("It must be a list.")
    else:
        print("Invalid choice")














