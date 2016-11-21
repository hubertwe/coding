#!/usr/bin/python

from Helpers import multiplicativeInverse

def modulo(polynomial, order):
    result = [value % order for value in polynomial]
    while result and result[-1] == 0:
        result.pop()
    return result

def add(p1, p2):
    if len(p1) > len(p2):
        result = list(p1)
        toAdd  = p2
    else:
        result = list(p2)
        toAdd = p1
    for i in xrange(len(toAdd)):
        result[i] += toAdd[i]
    return result

def sub(p1, p2):
    result = list(p1)
    toSub = p2
    lenDifference = len(result) - len(toSub)
    if lenDifference < 0:
        result += [0] * abs(lenDifference)
    for i in xrange(len(toSub)):
        result[i] -= toSub[i]
    return result

def mul(p1, p2):
    result = [0] * (len(p1) + len(p2) - 1)
    for i in xrange(len(p2)):
        for j in xrange(len(p1)):
            result[i+j] += p2[i] * p1[j]
    return result

def mulx(polynomial, x):
    return [value * x for value in polynomial]

def pow(polynomial, power):
    result = list(polynomial)
    if power == 0:
        return [1]
    for i in xrange(power - 1):
        result = mul(result, polynomial)
    return result

def normalize(polynomial, order):
    inverse = multiplicativeInverse(polynomial[-1], order)
    return modulo(mulx(polynomial, inverse), order)

def div(p1, p2, order):
    result = [0] * (len(p1) - len(p2) + 1)
    inverse = multiplicativeInverse(p2[-1], order)
    divisor = modulo(mulx(p2, inverse), order)
    dividend = modulo(mulx(p1, inverse), order)
    i = len(result) - 1
    while i >= 0:
        result[i] = dividend[-1] / divisor[-1]
        toSub = mul(result[:i+1], divisor)
        previousLen = len(dividend)
        dividend = modulo(sub(dividend, toSub), order)
        currentLen = len(dividend)
        i -= (previousLen - currentLen)
    return result, dividend


def value(polynomial, x):
    result = 0
    power = 0
    for parameter in polynomial:
        result += parameter * (x ** power)
        power += 1
    return result

def isPrimitive(polynomial, order):
    sequence = list()
    newPolynomial = normalize(polynomial, order)
    size = order ** (len(newPolynomial) - 1) - 1  # p^m -1
    rule = polynomial[0:-1]
    sequence += rule

    # generate sequence
    for i in xrange(len(rule) - 1, 2 * size):  # generate full sequence
        newValue = 0
        for j, value in enumerate(reversed(rule)):
            newValue += sequence[i - j] * value
        sequence.append(newValue % order)

    # check for period length
    periodLength = 1
    for x in range(len(rule), len(sequence) / 2 + 1):
        if sequence[0:x] == sequence[x:2 * x]:
            periodLength = x
            break
    return bool(periodLength == size)


class Polynomial:

    def __init__(self, polynomial, order):
        self.polynomial = modulo(polynomial, order)
        self.order = order
        self.degree = len(self.polynomial) - 1

    @classmethod
    def fromVector(cls, vector, order):
        return cls(vector, order)

    @classmethod
    def fromString(cls, string, order):
        result = [int(value) for value in reversed(string.split(' '))]
        return cls(result, order)

    def value(self, x):
        return value(self.polynomial, x)

    def isPrimitive(self):
        return isPrimitive(self.polynomial, self.order)

    def __eq__(self, other):
        return self.order == other.order and self.polynomial == other.polynomial

    def __ne__(self, other):
        return self.order != other.order or self.polynomial != other.polynomial

    def __repr__(self):
        return 'polly(' + ' '.join([str(value) for value in reversed(self.polynomial)]) + ')'

    def __str__(self):
        return ' '.join([str(value) for value in reversed(self.polynomial)])

    def __add__(self, other):
        if not self.order == other.order:
            raise TypeError('Cannot add Polynomials from Fields with different order!')
        result = add(self.polynomial, other.polynomial)
        return Polynomial(result, self.order)

    def __iadd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if not self.order == other.order:
            raise TypeError('Cannot subtract Polynomials from Fields with different order!')
        result = sub(self.polynomial, other.polynomial)
        return Polynomial(result, self.order)

    def __mul__(self, other):
        if isinstance(other, Polynomial):
            if not self.order == other.order:
                raise TypeError('Cannot multiply Polynomials from Fields with different order!')
            result = mul(self.polynomial, other.polynomial)
        else:
            result = mulx(self.polynomial, other)
        return Polynomial(result, self.order)

    def __imul__(self, other):
        return self.__mul__(other)

    def __mod__(self, other):
        if isinstance(other, Polynomial):
            if not self.order == other.order:
                raise TypeError('Cannot divide Polynomials from Fields with different order!')
            result, reminder = div(self.polynomial, other.polynomial, self.order)
            return Polynomial(reminder, self.order)
        else:
            return Polynomial(modulo(self.polynomial, other), self.order)

    def __imod__(self, other):
        return self.__mod__(other)

    def __pow__(self, power):
        return Polynomial(pow(self.polynomial, power), self.order)

    def __ipow__(self, power):
        return self.__pow__(power)

    def __div__(self, other):
        if not self.order == other.order:
            raise TypeError('Cannot divide Polynomials from Fields with different order!')
        result, reminder = div(self.polynomial, other.polynomial, self.order)
        return Polynomial(result, self.order), Polynomial(reminder, self.order)


if __name__ == '__main__':
    polynomial1 = Polynomial.fromString('5 3 0 0 1', 7)
    print 'polynomial1: ' + str(polynomial1)
    polynomial2 = Polynomial.fromString('3 2 1', 7)
    print normalize(polynomial2.polynomial, 7)
    print 'polynomial2: ' + str(polynomial2)
    print str(polynomial1) + ' + ' + str(polynomial2) + ' = ' + str(polynomial1 + polynomial2)
    print str(polynomial1) + ' - ' + str(polynomial2) + ' = ' + str(polynomial1 - polynomial2)
    print str(polynomial2) + ' - ' + str(polynomial1) + ' = ' + str(polynomial2 - polynomial1)
    print str(polynomial1) + ' * ' + str(polynomial2) + ' = ' + str(polynomial1 * polynomial2)
    print str(polynomial2) + ' * ' + str(3) + ' = ' + str(polynomial2 * 3)
    result, reminder = polynomial1 / polynomial2
    print str(polynomial1) + ' / ' + str(polynomial2) + ' = ' + str(result) + ' + ' + str(reminder)
    print str(polynomial2) + ' ^ ' + str(2) + ' = ' + str(polynomial2 ** 2)