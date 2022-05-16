#!/usr/bin/env python3

from math import gcd


__all__ = (
    "Fraction",
)


class Fraction:
    """Represents a given fraction with a numerator and denominator (different from zero)."""

    __slots__ = ("numerator", "denominator")

    def __init__(self, numerator, denominator):
        if not isinstance(numerator, int) or not isinstance(denominator, int):
            raise TypeError("numerator and denominator must be integers.") from None
        if not denominator:
            raise ValueError("denominator cannot be zero.") from None

        if denominator < 0:
            numerator *= -1
            denominator *= -1

        _gcd = gcd(numerator, denominator)
        self.numerator = numerator // _gcd
        self.denominator = denominator // _gcd


    @classmethod
    def from_number(cls, number, /):
        """Constructs a fraction from a number."""
        return cls(number, 1)

    @classmethod
    def inverse_from(cls, number, /):
        """Constructs the fraction representing the inverse from a number."""
        return cls(1, number)

    def eval(self):
        """Evaluates the fraction."""
        return self.numerator / self.denominator

    def is_int(self):
        """Returns `True` if fraction is an integer, `False` otherwise."""
        return self.denominator == 1

    def __str__(self):
        if self.denominator == 1:
            return f"{self.numerator:,}"
        return f"{self.numerator:,}" + "/" + f"{self.denominator:,}"

    def __repr__(self):
        return self.__str__()

    def __abs__(self):
        return Fraction(self.numerator.__abs__(), self.denominator)

    def __eq__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        elif not isinstance(other, Fraction):
            return False
        return (self.numerator * other.denominator) == (self.denominator * other.numerator)

    def __bool__(self):
        return self.numerator.__bool__()

    def __neg__(self):
        return self.__mul__(-1)

    def __pos__(self):
        return self.clone()

    def __lt__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        elif not isinstance(other, Fraction):
            raise TypeError("can only compare fractions.")
        return (self.numerator * other.denominator) < (self.denominator * other.numerator)

    def __le__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        elif not isinstance(other, Fraction):
            raise TypeError("can only compare fractions.")
        return (self.numerator * other.denominator) <= (self.denominator * other.numerator)

    def __gt__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        elif not isinstance(other, Fraction):
            raise TypeError("can only compare fractions.")
        return (self.numerator * other.denominator) > (self.denominator * other.numerator)

    def __ge__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        elif not isinstance(other, Fraction):
            raise TypeError("can only compare fractions.")
        return (self.numerator * other.denominator) >= (self.denominator * other.numerator)

    def __add__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        elif not isinstance(other, Fraction):
            raise TypeError("fractions can only add numbers or fractions.")
        return Fraction(self.numerator*other.denominator + self.denominator*other.numerator, self.denominator*other.denominator)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, int):
            other = Fraction(other, 1)
        elif not isinstance(other, Fraction):
            raise TypeError("fractions can only substract numbers or fractions.")
        return Fraction(self.numerator*other.denominator - self.denominator*other.numerator, self.denominator*other.denominator)

    def __rsub__(self, other):
        return self.__mul__(-1).__add__(other)

    def __mul__(self, other):
        if isinstance(other, int):
            return Fraction(self.numerator*other, self.denominator)
        if isinstance(other, Fraction):
            return Fraction(self.numerator*other.numerator, self.denominator*other.denominator)
        raise TypeError("fractions can only multiply number or fractions.")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, int):
            return Fraction(self.numerator, self.denominator*other)
        if isinstance(other, Fraction):
            return Fraction(self.numerator*other.denominator, self.denominator*other.numerator)
        raise TypeError("fractions can only divide number or fractions.")

    def __rtruediv__(self, other):
        return Fraction(self.denominator, self.numerator).__mul__(other)

    def __pow__(self, other):
        if not isinstance(other, int):
            raise TypeError("fractions can only be raised to a power of an integer.")
        if other >= 0:
            return Fraction(self.numerator**other, self.denominator**other)
        return Fraction(self.denominator**(other.__mul__(-1)), self.numerator**(other.__mul__(-1)))

    def __int__(self):
        return self.numerator // self.denominator

    def __float__(self):
        return self.eval()

    def clone(self):
        """Makes a copy of the fraction."""
        return Fraction(self.numerator, self.denominator)
