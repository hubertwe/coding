#!/usr/bin/python

def extendedGCD(a, n):
    if a == 0:
        return n, 0, 1
    else:
        gcd, x, y = extendedGCD(n % a, a)
        return gcd, y - (n // a) * x, x

def multiplicativeInverse(a, n):
    gcd, x, _ = extendedGCD(a, n)
    if gcd == 1:
        return x % n
    else:
        raise ArithmeticError('GCD for ' + str(a) + ' and ' + str(n) + ' is not equal 1')

def euler(n):
    amount = 0
    relativePrimes = list()
    factors = list()
    for k in range(2, n):
        gcd, _, _ = extendedGCD(k, n)
        if gcd == 1:
            relativePrimes.append(k)
            amount += 1
        if gcd == k:
            factors.append(k)
    return amount + 1, relativePrimes, factors

def generators(n):
    amount, _, _ = euler(n)
    _, relativePrimes, factors = euler(amount)
    generator = 0
    for k in range(2, n):
        isGenerator = True
        for factor in factors:
            if (k ** factor) % n == 1:
                isGenerator = False
                break
        if isGenerator:
            generator = k
            break
    return [generator] + [(generator ** prime) % n for prime in relativePrimes]


if __name__ == '__main__':
    print multiplicativeInverse(3, 6)
    #print generators(11)
    #print euler(3 ** 4 - 1)