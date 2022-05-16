#!/usr/bin/env python3

__all__ = (
    "Sigma",
)


class Sigma:
    """Represents sigma notation."""

    __slots__ = ("_function", "_start", "_stop")

    def __init__(self, function: callable, /, *, start: int, stop: int):
        if not callable(function):
            raise TypeError("function must be callable.")
        if not isinstance(start, int) or not isinstance(stop, int):
            raise TypeError("start and stop must be integers.")

        self._function = function
        self._start = start
        self._stop = stop

    def compute_iteration(self, i: int = None, /) -> int:
        """Computes iteration at `i`. Defaults to the first iteration."""
        if i is None:
            i = self._start
        elif not isinstance(i, int):
            raise TypeError("i must be an integer.")
        elif i < self._start:
            raise ValueError("iteration is beyond start point.")

        if i > self._stop:
            raise ValueError("iteration is beyond stop point.")

        return self._function(i)

    def compute(self, *, until: int = None) -> int:
        """Computes iteration until some value, or stop value if not specified."""
        if until is None:
            until = self._stop
        elif not isinstance(until, int):
            raise TypeError("until must be an integer.")
        elif until > self._stop:
            raise ValueError("until value beyond stop point")

        if until < self._start:
            return 0

        curr = self._start
        val = 0

        while curr <= until:
            val += self.compute_iteration(curr)
            curr += 1

        return val

    def to_dict(self, *, addup: bool = False) -> dict:
        """Returns a dictionary with each variable value in the sum and their corresponding result.

        If `addup` is set to `True`, everything will add up as the variable gets bigger."""
        if not isinstance(addup, bool):
            raise TypeError("addup must be of type bool.")

        d = {}
        curr = self._start

        if addup:
            val = 0
            while curr <= self._stop:
                val += self.compute_iteration(curr)
                d[curr] = val
                curr += 1
            return d

        while curr <= self._stop:
            d[curr] = self.compute_iteration(curr)
            curr += 1

        return d

    @property
    def function(self):
        return self._function

    @property
    def start(self):
        return self._start

    @property
    def stop(self):
        return self._stop

    def copy(self):
        """Creates a copy of the sigma sum."""
        return Sigma(self._function, start=self._start, stop=self._stop)

    @staticmethod
    def symbol() -> str:
        """Returns sigma symbol Σ."""
        return "Σ"

    def __bool__(self):
        return self.compute() != 0

    def __str__(self):
        return "Sigma({0._function}, {0._start}, {0._stop})".format(self)

    def __repr__(self):
        return self.__str__()

    def __pos__(self):
        return self.compute()

    def __neg__(self):
        return -self.compute()

    def __abs__(self):
        return abs(self.compute())

    def __call__(self, *, until: int = None):
        return self.compute(until=until)

    def __eq__(self, other, /):
        if not isinstance(other, Sigma):
            return False
        return (self._function == other._function and self._start == other._start and self._stop == other._stop)

    def __len__(self):
        return max(0, self._stop-self._start+1)

    def __lt__(self, other, /):
        if not isinstance(other, Sigma):
            return False
        return self.compute() < other.compute()

    def __le__(self, other, /):
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other, /):
        if not isinstance(other, Sigma):
            return False
        return self.compute() > other.compute()

    def __ge__(self, other, /):
        return self.__gt__(other) or self.__eq__(other)
