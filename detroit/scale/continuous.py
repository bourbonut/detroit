from __future__ import annotations

import math
from bisect import bisect
from collections.abc import Callable
from datetime import datetime
from typing import Any, Generic, TypeVar

from ..interpolate import (
    interpolate as interpolate_value,
)
from ..interpolate import (
    interpolate_number,
    interpolate_round,
)
from .constant import constant
from .number import number

T = TypeVar("T")


def identity(x):
    return x


def normalize(a, b):
    if isinstance(a, datetime):
        a = a.timestamp()
    elif isinstance(a, str):
        a = float(a)
    if isinstance(b, datetime):
        b = b.timestamp()
    elif isinstance(b, str):
        b = float(b)
    b = b - a
    if not math.isnan(b) and b:

        def f(x):
            if isinstance(x, datetime):
                x = x.timestamp()
            elif isinstance(x, str):
                x = float(x)
            return (x - a) / b

        return f
    else:
        return constant(math.nan if math.isnan(b) else 0.5)


def clamper(a, b):
    a = a.timestamp() if isinstance(a, datetime) else a
    b = b.timestamp() if isinstance(b, datetime) else b
    if a > b:
        a, b = b, a

    def f(x):
        x = x.timestamp() if isinstance(x, datetime) else x
        return max(a, min(b, x))

    return f


class BiMap:
    def __init__(self, domain, range_vals, interpolate):
        d0, d1 = domain[0], domain[1]
        r0, r1 = range_vals[0], range_vals[1]
        if d1 < d0:
            self.d0 = normalize(d1, d0)
            self.r0 = interpolate(r1, r0)
        else:
            self.d0 = normalize(d0, d1)
            self.r0 = interpolate(r0, r1)

    def __call__(self, x):
        return self.r0(self.d0(x))


class PolyMap:
    def __init__(self, domain, range_vals, interpolate):
        self.domain = domain
        self.j = j = min(len(self.domain), len(range_vals)) - 1
        self.d = [None] * j
        self.r = [None] * j

        if self.domain[j] < self.domain[0]:
            self.domain = self.domain[::-1]
            range_vals = range_vals[::-1]

        for i in range(j):
            self.d[i] = normalize(self.domain[i], self.domain[i + 1])
            self.r[i] = interpolate(range_vals[i], range_vals[i + 1])

    def __call__(self, x):
        i = bisect(self.domain, x, 1, self.j) - 1
        return self.r[i](self.d[i](x))


def copy(source, target):
    return (
        target.set_domain(source.domain)
        .set_range(source.range)
        .set_interpolate(source.interpolate)
        .set_clamp(source.clamp)
        .set_unknown(source.unknown)
    )


class Transformer(Generic[T]):
    """
    Continous transformation

    Parameters
    ----------
    t : Callable[[int | float], T]
        Transform function
    u : Callable[[T], int | float]
        Untransform function
    """

    def __init__(
        self,
        t: Callable[[int | float], T] = identity,
        u: Callable[[T], int | float] = identity,
    ):
        self.transform = t
        self.untransform = u
        self._domain = [0, 1]
        self._range = [0, 1]
        self._clamp = identity
        self._interpolate = interpolate_value
        self._unknown = None
        self.input = None
        self.output = None
        self.rescale()

    def rescale(self):
        n = min(len(self._domain), len(self._range))
        if self._clamp != identity:
            self._clamp = clamper(self._domain[0], self._domain[n - 1])
        self.piecewise = PolyMap if n > 2 else BiMap
        self.output = self.input = None
        return self

    def __call__(self, x: int | float) -> T:
        """
        Given a value from the domain, returns the corresponding value from the range.

        Parameters
        ----------
        x : int | float
            Input value

        Returns
        -------
        T
            Corresponding value from the range
        """
        if x is None or (isinstance(x, float) and math.isnan(x)):
            return self._unknown
        else:
            if not self.output:
                domain = [
                    x.timestamp() if isinstance(x, datetime) else x
                    for x in self._domain
                ]
                domain = [self.transform(x) for x in domain]
                self.output = self.piecewise(domain, self._range, self._interpolate)
            return self.output(self.transform(self._clamp(x)))

    def invert(self, y: T) -> int | float:
        """
        Given a value from the range, returns the corresponding value
        from the domain. Inversion is useful for interaction, say to
        determine the data value corresponding to the position of the mouse.

        Parameters
        ----------
        y : T
            Input value

        Returns
        -------
        int | float
            Corresponding value from the domain
        """
        if not self.input:
            domain = [
                x.timestamp() if isinstance(x, datetime) else x for x in self._domain
            ]
            domain = [self.transform(x) for x in domain]
            self.input = self.piecewise(self._range, domain, interpolate_number)
        return self._clamp(self.untransform(self.input(y)))

    def set_domain(self, domain: list[int | float]) -> Transformer:
        """
        Sets the scale's domain to the specified array of numbers

        Parameters
        ----------
        domain : list[int | float]
            Domain

        Returns
        -------
        Transformer
            Itself
        """
        self._domain = list(map(number, domain))
        return self.rescale()

    @property
    def domain(self) -> list[int | float]:
        return self._domain.copy()

    def set_range(self, range_vals: list[T]) -> Transformer:
        """
        Sets the scale's range to the specified array of values

        Parameters
        ----------
        range_vals : list[T]
            Range values

        Returns
        -------
        Transformer
            Itself
        """
        self._range = list(range_vals)
        return self.rescale()

    @property
    def range(self) -> list[T]:
        return self._range.copy()

    def set_range_round(self, range_vals: list[T]) -> Transformer:
        """
        Sets the scale's range to the specified array of values
        and sets scale's interpolator to :code:`interpolate_round`.

        Parameters
        ----------
        range_vals : list[T]
            Range values

        Returns
        -------
        Transformer
            Itself
        """
        self._range = list(map(float, range_vals))
        self._interpolate = interpolate_round
        return self.rescale()

    def set_clamp(self, clamp: bool) -> Transformer:
        """
        Enables or disables clamping accordingly

        Parameters
        ----------
        clamp : bool
            Clamp value

        Returns
        -------
        Transformer
            Itself
        """
        self._clamp = True if clamp else identity
        return self.rescale()

    @property
    def clamp(self) -> bool:
        return self._clamp != identity

    def set_interpolate(self, interpolate: Callable[[T, T], T]) -> Transformer:
        """
        Sets the scale's range interpolator factory.

        Parameters
        ----------
        interpolate : Callable[[T, T], T]
            Interpolate function

        Returns
        -------
        Transformer
            Itself
        """
        self._interpolate = interpolate
        return self.rescale()

    @property
    def interpolate(self) -> Callable[[T, T], T]:
        return self._interpolate

    def set_unknown(self, unknown: Any) -> Transformer:
        """
        Sets the output value of the scale for undefined
        or NaN input values.

        Parameters
        ----------
        unknown : Any
            Unknown value

        Returns
        -------
        Transformer
            Itself
        """
        self._unknown = unknown
        return self.rescale()

    @property
    def unknown(self) -> Any:
        return self._unknown
