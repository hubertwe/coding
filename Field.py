#!/usr/bin/python

import itertools
from Polynomial import Polynomial

def irreduciblePolynomials(order, degree):
    if degree == 0:
        return list(), list()

    result = list()
    nullPolynomial = Polynomial([], order)

    lowerPolynomials, lastPolynomials = irreduciblePolynomials(order, degree - 1)  # return lower degree polynomials
    polynomials = list(itertools.product(range(order), repeat=(degree + 1)))  # create all possible polynomials
    polynomials = [Polynomial(list(polynomial), order) for polynomial in polynomials
                   if not polynomial[0] == 0 and not polynomial[-1] == 0]  # remove all with 0 and beginning and end

    for polynomial in polynomials:
        isIrreducible = True
        for lowerPolynomial in lowerPolynomials + lastPolynomials:
            if polynomial % lowerPolynomial == nullPolynomial:
                isIrreducible = False
                break
        if isIrreducible:
            result.append(polynomial)
    return lowerPolynomials + lastPolynomials, result

def primitivePolynomials(order, degree):
    lowerPolynomials, polynomials = irreduciblePolynomials(order, degree)
    return [polynomial for polynomial in polynomials if polynomial.isPrimitive()]

def generateField(generator):
    amount = generator.order ** generator.degree - 1  # p^m -1
    alphas = list()
    for i in xrange(amount):
        alphas.append(Polynomial([0] * (i) + [1], generator.order) % generator)
    return alphas

class Field:

    def __init__(self, generator):
        self.generator = generator
        print generator
        self.alphas = generateField(self.generator)

    @classmethod
    def fromGenerator(cls, generator):
        if generator in primitivePolynomials(generator.order, generator.degree):
            return cls(generator)
        else:
            raise ValueError('Generator ' + str(generator) + ' is not a valid primitive polynomial')

    @classmethod
    def fromDegree(cls, order, degree):
        primitives = primitivePolynomials(order, degree)
        return cls(primitives[0])

    def alpha(self, degree):
        return self.alphas[degree]

    def add(self, degree1, degree2):
        polynomial = (self.alphas[degree1] + self.alphas[degree2]) % self.generator
        return polynomial, self.alphas.index(polynomial)

    def mul(self, degree1, degree2):
        degree = (degree1 + degree2) % self.generator.degree
        return self.alphas[degree], degree

if __name__ == '__main__':
    field = Field.fromGenerator(Polynomial.fromString('1 0 0 1 0 1', 2))
    print field.mul(4, 3)
    print field.add(0, 1)
    print field.alphas