#!/usr/bin/env python3

from math import inf
from itertools import zip_longest
from .fraction import Fraction


__all__ = (
    "Polynomial",
)


seaborn = None
np = None
plt = None


FORBIDDEN = (
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "⁰", "¹", "²", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹",
    "+", "-", " "
)

UPPERSCRIPT_MAP = {
    "0": "⁰",
    "1": "¹",
    "2": "²",
    "3": "³",
    "4": "⁴",
    "5": "⁵",
    "6": "⁶",
    "7": "⁷",
    "8": "⁸",
    "9": "⁹"
}


def verify_variable(variable, /):
    """Raises exception if variable is not valid."""
    if not isinstance(variable, str):
        raise TypeError("variable must be a string.") from None
    if not variable:
        raise ValueError("variable cannot be empty.") from None
    for char in variable:
        if char in FORBIDDEN:
            raise ValueError("variable cannot contain characters: {}.".format(str(FORBIDDEN))) from None


def to_upper_script(string, /):
    """Returns a string of numbers with uppercase characters."""
    return "".join(UPPERSCRIPT_MAP.get(char, char) for char in string)


class Polynomial:
    """Represents a polynomial of any given degree."""

    __slots__ = ("coefs",)

    def __init__(self, *coefs):
        if not coefs:
            self.coefs = (0,)
            return
        if len(coefs) > 1 and not coefs[0]:
            raise ValueError("highest coefficient cannot be null.") from None
        self.coefs = coefs

    @property
    def degree(self):
        """Returns the degree of the polynomial."""
        return len(self.coefs)-1 if self.coefs[0] else -inf

    @property
    def y_intercept(self):
        """Returns the y-intercept of the polynomial."""
        return self.coefs[-1]

    @property
    def is_null(self):
        """Returns `True` if polynomial is null (with degree -∞)."""
        return not self.coefs[0]

    @property
    def is_constant(self):
        """Returns `True` if polynomial is constant."""
        return len(self.coefs) == 1

    def to_dict(self, *, include_zeros=False):
        """Converts the polynomial to a dictionary with exponents as keys and coefficients as values.

        If `include_zeros` is set to `True`, null coefficients are included in the dictionary."""
        if self.is_null:
            return {0: 0}
        if include_zeros:
            return {key: value for key, value in zip(range(len(self.coefs)), reversed(self.coefs))}
        return {key: value for key, value in zip(range(len(self.coefs)), reversed(self.coefs)) if value}

    def get_coefficient(self, exponent, /):
        """Returns the coefficient of the `exponent` exponent."""
        if not isinstance(exponent, int):
            raise TypeError("exponent must be an integer.") from None
        if exponent < 0:
            raise ValueError("exponent must be positive.") from None
        try:
            return self.to_dict(include_zeros=True)[exponent]
        except KeyError:
            raise ValueError("exponent given is higher than the polynomial degree.") from None

    def get_exponents(self, coefficient, /):
        """Returns a tuple of all the exponents with the `coefficient` coefficient."""
        return tuple(exp for exp, coef in enumerate(reversed(self.coefs)) if coef==coefficient)

    def __call__(self, x):
        return sum(coef*(x**(len(self.coefs)-index-1)) for index, coef in enumerate(self.coefs))

    def __bool__(self):
        return not self.is_null

    def __pos__(self):
        return self.clone()

    def __neg__(self):
        return self.__mul__(-1)

    def expr(self, variable="x", /):
        """String representation of the polynomial."""
        verify_variable(variable)
        if self.is_null:
            return "0"

        _len = len(self.coefs)
        string = ""
        for index, coef in enumerate(self.coefs):
            if not coef:
                continue
            cal = (_len-index-1)
            if coef < 0:
                string += (" - " if string else "-")+("" if (coef==-1 and cal) else coef.__abs__().__str__())
            else:
                string += (" + " if string else "")+("" if (coef == 1 and cal) else coef.__str__())
            if not cal:
                continue
            string += (variable if cal == 1 else variable+to_upper_script(cal.__str__()))
        return string

    def __str__(self):
        return self.expr()

    def __repr__(self):
        return self.expr()

    def __eq__(self, other):
        if self.is_constant:
            if isinstance(other, Polynomial):
                if other.is_constant:
                    return self.coefs == other.coefs
                return False
            return self.coefs[0] == other
        if isinstance(other, Polynomial):
            return self.coefs == other.coefs
        return False

    @classmethod
    def null(cls):
        """Represents a null polynomial of degree -∞."""
        return cls(0)

    @classmethod
    def from_monomial(cls, degree, coefficient=0):
        """Declares a polynomial from a single monomial."""
        if not isinstance(degree, int):
            raise TypeError("degree must be an int.") from None
        if degree < 0:
            raise ValueError("degree must be positive.") from None
        if not coefficient:
            raise ValueError("coefficient cannot be null.") from None
        return cls(*[coefficient if i == degree else 0 for i in range(degree, -1, -1)])

    @classmethod
    def from_dict(cls, dictionary, /):
        """Creates a polynomial from a given dictionary, where every key is an exponent and every value the corresponding coefficient."""
        if not isinstance(dictionary, dict):
            raise TypeError("input must be a dictionary.") from None
        if not dictionary:
            raise ValueError("dictionary cannot be empty.") from None
        keys = dictionary.keys()
        for key in keys:
            if not isinstance(key, int):
                raise TypeError("all keys must be integers.") from None
            if key < 0:
                raise ValueError("all keys must be positive.") from None
        return cls(*[dictionary[exp] if (exp in keys) else 0 for exp in range(max(keys), -1, -1)])

    @staticmethod
    def enable_graphics():
        """Imports `seaborn`, `numpy` and `matplotlib` modules for plotting."""
        global seaborn, np, plt
        if np is None:
            import numpy as np
        if plt is None:
            from matplotlib import pyplot as plt
        if seaborn is None:
            import seaborn
            seaborn.set(style="ticks")

    def derivative(self):
        """Returns the derivative of the polynomial."""
        length = len(self.coefs)-1
        return Polynomial(*[(length-i)*self.coefs[i] for i in range(length)])

    def integral(self, *, constant=0):
        """Returns the definite integral of the polynomial with a given constant term."""
        length = len(self.coefs)
        p = [0]*length + [constant]
        for i in range(length):
            f = Fraction(self.coefs[i], length-i)
            if f.is_int(): p[i] = int(f)
            else: p[i] = f
        return Polynomial(*p)

    def plotting(self, start, stop, /, **options):
        """
        Returns a plotting of the function from `start` to `stop`. The options are:

        `points` (`int`): the number of points to compute (default is 50)\n
        `style` (`str`): the style of the plotting (default is "-")\n
        `width` (`int`): the linewidth (default is 2)\n
        `equal_axis` (`bool`): if the axis should have the same graduation (default is False)\n
        `legend` (`bool`): if the legend (polynomial function) should be shown (default is True)\n
        `grid` (`bool`): if grid should be visible (default is True)\n
        `title` (`str`): graph title that should be displayed (default is None)\n
        `windowtitle` (`str`): window title that should be displayed (default is "Graph")\n
        `xlabel` (`str`): x-axis label (default is None)\n
        `ylabel` (`str`): y-axis label (default is None)\n
        `xmin` (`int`/`float`): minimum x value to be displayed (default is auto)\n
        `xmax` (`int`/`float`): maximum x value to be displayed (default is auto)\n
        `ymin` (`int`/`float`): minimum y value to be displayed (default is auto)\n
        `ymax` (`int`/`float`): maximum y value to be displayed (default is auto)\n
        `add_seaborn` (`bool`): whether to add seaborn module to format axis (default is True)


        Use the `savefig()` method to save this as a file. Example:
        ```python
        >>> f = Polynomial(1, -1, -1)
        >>> plt = f.plotting(-1, 2)
        >>> plt.savefig("image.png") # As an image
        >>> plt.savefig("image.pdf") # As a PDF
        ```
        For faster performance, consider calling `Polynomial.enable_graphics()` when importing this module.
        """
        self.enable_graphics()
        points = options.get("points", 50)
        xlabel = options.get("xlabel")
        ylabel = options.get("ylabel")
        title = options.get("title")
        if start == stop:
            raise ValueError("`start` and `stop` must be different numbers.") from None
        if points < 2:
            raise ValueError("there must be at least two points.") from None

        x = np.linspace(start=start, stop=stop, num=points)
        y = tuple(map(self.__call__, x))

        fig, pol = plt.subplots()
        fig.canvas.set_window_title(options.get("windowtitle", "Graph"))

        if options.get("legend", True):
            plt.plot(x, y, options.get("style", "-"), label=self.__str__(), linewidth=options.get("width", 2))
            plt.legend()
        else:
            plt.plot(x, y, options.get("style", "-"), linewidth=options.get("width", 2))

        if xlabel:
            plt.xlabel(xlabel)
        if ylabel:
            plt.ylabel(ylabel)
        if title:
            plt.title(title)
        if options.get("equal_axis"):
            plt.axis("equal")

        left, right = plt.xlim()
        xmin = options.get("xmin", left)
        xmax = options.get("xmax", right)
        plt.xlim(xmin, xmax)

        bottom, top = plt.ylim()
        ymin = options.get("ymin", bottom)
        ymax = options.get("ymax", top)
        plt.ylim(ymin, ymax)

        if options.get("grid", True):
            plt.grid(True, which="both")
        if options.get("add_seaborn", True):
            seaborn.despine(ax=pol, offset=0)

        return plt

    def plot(self, start, stop, /, **options):
        """
        Plots the function from `start` to `stop`. This function prints the plotting but does not return anything.

        For faster performance, consider calling `Polynomial.enable_graphics()` when importing this module.
        """
        plot = self.plotting(start, stop, **options)
        plot.show()

    def __add__(self, other):
        if isinstance(other, Polynomial):
            new = [i[0]+i[1] for i in zip_longest(reversed(self.coefs), reversed(other.coefs), fillvalue=0)]
            new.reverse()
            for index, value in enumerate(new):
                if value:
                    break
            newcoefs = new[index:]
            return Polynomial(*newcoefs)
        newcoefs = list(self.coefs)
        newcoefs[-1] += other
        return Polynomial(*newcoefs)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self.__add__(other.__mul__(-1))

    def __rsub__(self, other):
        return self.__mul__(-1).__add__(other)

    def __mul__(self, other):
        if isinstance(other, Polynomial):
            if self.is_null or other.is_null:
                return Polynomial.null()
            coefficients = [0]*(1+self.degree+other.degree)
            for index1, value1 in enumerate(self.coefs):
                for index2, value2 in enumerate(other.coefs):
                    coefficients[index1+index2] += value1*value2
            return Polynomial(*coefficients)
        if not other:
            return Polynomial.null()
        return Polynomial(*[i*other for i in self.coefs])

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, other):
        if not isinstance(other, int):
            raise TypeError("power must be an integer.") from None
        if other < 0:
            raise ValueError("power must be positive.") from None
        if not other:
            return Polynomial(1)
        power = self
        for _ in range(other-1):
            power *= self
        return power

    def clone(self):
        """Creates a new polynomial instance with the same coefficients."""
        return Polynomial(*self.coefs)
