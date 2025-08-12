from bisect import bisect
from collections.abc import Callable
from datetime import datetime
from math import isnan, nan
from typing import Any, Generic, TypeVar

from ..interpolate import (
    interpolate as interpolate_value,
)
from ..interpolate import (
    interpolate_number,
    interpolate_round,
)
from ..types import GenValue, Number, T
from .utils import as_float, constant, identity

TTransformer = TypeVar("Itself", bound="Transformer")


def normalize(a: GenValue, b: GenValue) -> Callable[[T], float]:
    """
    Makes a function which takes a generic value and returns the normalized value
    based on :code:`a` and :code:`b` values. Normalization is done by applying the
    following formula: :code:`(x - a) / (b - a)`.

    Parameters
    ----------
    a : GenValue
        Generic value
    b : GenValue
        Generic value

    Returns
    -------
    Callable[[T], float]
        Normalization function based on :code:`a` and :code:`b` values
    """
    a = as_float(a)
    b = as_float(b)
    b = b - a

    if isnan(b):
        return constant(nan)
    elif b == 0:
        return constant(0.5)

    def normalizer(x):
        x = as_float(x)
        return (x - a) / b

    return normalizer


def clamper(a: GenValue, b: GenValue) -> Callable[[GenValue], float]:
    """
    Makes a function which clamps its input value borned by :code:`a` and :code:`b`
    values.

    Parameters
    ----------
    a : GenValue
        Generic value
    b : GenValue
        Generic value

    Returns
    -------
    Callable[[GenValue], float]
        Clamp function based on :code:`a` and :code:`b` values
    """
    a = as_float(a)
    b = as_float(b)
    if a > b:
        a, b = b, a

    def clamp(x):
        x = as_float(x)
        return max(a, min(b, x))

    return clamp


class BiMap:
    def __init__(
        self,
        domain: tuple[T, T],
        range_vals: tuple[T, T],
        interpolate: Callable[[T, T], Callable[[T], float]],
    ):
        d0, d1 = domain[0], domain[1]
        r0, r1 = range_vals[0], range_vals[1]
        if d1 < d0:
            self.d0 = normalize(d1, d0)
            self.r0 = interpolate(r1, r0)
        else:
            self.d0 = normalize(d0, d1)
            self.r0 = interpolate(r0, r1)

    def __call__(self, x: T) -> float:
        return self.r0(self.d0(x))


class PolyMap:
    def __init__(
        self,
        domain: list[T],
        range_vals: list[T],
        interpolate: Callable[[T, T], Callable[[T], float]],
    ):
        self.domain = domain
        self.j = j = min(len(self.domain), len(range_vals)) - 1
        self.d = [None] * j  # TODO: use list by comprehension
        self.r = [None] * j

        if self.domain[j] < self.domain[0]:
            self.domain = self.domain[::-1]
            range_vals = range_vals[::-1]

        for i in range(j):
            self.d[i] = normalize(self.domain[i], self.domain[i + 1])
            self.r[i] = interpolate(range_vals[i], range_vals[i + 1])

    def __call__(self, x: T) -> float:
        i = bisect(self.domain, x, 1, self.j) - 1
        return self.r[i](self.d[i](x))


def copy(source, target):
    return (
        target.set_domain(source.get_domain())
        .set_range(source.get_range())
        .set_interpolate(source.get_interpolate())
        .set_clamp(source.get_clamp())
        .set_unknown(source.get_unknown())
    )


class Transformer(Generic[T]):
    """
    Continous transformation

    Parameters
    ----------
    t : Callable[[Number], T]
        Transform function
    u : Callable[[T], Number]
        Untransform function
    """

    def __init__(
        self,
        t: Callable[[Number], T] = identity,
        u: Callable[[T], Number] = identity,
    ):
        self._transform = t
        self._untransform = u
        self._domain = [0, 1]
        self._range = [0, 1]
        self._clamp = identity
        self._interpolate = interpolate_value
        self._unknown = None
        self._input = None
        self._output = None
        self._rescale()

    def _rescale(self) -> TTransformer:
        """
        Private method which updates:

        * :code:`clamp` attribute
        * :code:`piecewise` attribute
        * :code:`input` attribute
        * :code:`output` attribute
        """
        n = min(len(self._domain), len(self._range))
        if self._clamp != identity:
            self._clamp = clamper(self._domain[0], self._domain[n - 1])
        self.piecewise = PolyMap if n > 2 else BiMap
        self._output = self._input = None
        return self

    def __call__(self, x: Number) -> T:
        """
        Given a value from the domain, returns the corresponding value from the range.

        Parameters
        ----------
        x : Number
            Input value

        Returns
        -------
        T
            Corresponding value from the range
        """
        if x is None or (isinstance(x, float) and isnan(x)):
            return self._unknown
        else:
            if not self._output:
                domain = [
                    x.timestamp() if isinstance(x, datetime) else x
                    for x in self._domain
                ]
                domain = [self._transform(x) for x in domain]
                self._output = self.piecewise(domain, self._range, self._interpolate)
            return self._output(self._transform(self._clamp(x)))

    def invert(self, y: T) -> Number:
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
        Number
            Corresponding value from the domain
        """
        if not self._input:
            domain = [
                x.timestamp() if isinstance(x, datetime) else x for x in self._domain
            ]
            domain = [self._transform(x) for x in domain]
            self._input = self.piecewise(self._range, domain, interpolate_number)
        return self._clamp(self._untransform(self._input(y)))

    def set_domain(self, domain: list[Number]) -> TTransformer:
        """
        Sets the scale's domain to the specified array of numbers

        Parameters
        ----------
        domain : list[Number]
            Domain

        Returns
        -------
        Transformer
            Itself
        """
        # TODO: update lambda function to as_float function
        self._domain = list(
            map(lambda x: float(x) if isinstance(x, str) else x, domain)
        )
        return self._rescale()

    def get_domain(self) -> list[Number]:
        return self._domain.copy()

    def set_range(self, range_vals: list[T]) -> TTransformer:
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
        return self._rescale()

    def get_range(self) -> list[T]:
        return self._range.copy()

    def set_range_round(self, range_vals: list[T]) -> TTransformer:
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
        return self._rescale()

    def set_clamp(self, clamp: bool) -> TTransformer:
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
        return self._rescale()

    def get_clamp(self) -> bool:
        return self._clamp != identity

    def set_interpolate(self, interpolate: Callable[[T, T], T]) -> TTransformer:
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
        return self._rescale()

    def get_interpolate(self) -> Callable[[T, T], T]:
        return self._interpolate

    def set_unknown(self, unknown: Any) -> TTransformer:
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
        return self._rescale()

    def get_unknown(self) -> Any:
        return self._unknown

    def __str__(self) -> str:
        name = self.__class__.__name__
        attrbs = ["domain", "range"]
        attrbs = (f"{a}={getattr(self, f'get_{a}')()}" for a in attrbs)
        attrbs = ", ".join(attrbs)
        return f"{name}({attrbs})"

    def __repr__(self) -> str:
        name = self.__class__.__name__
        addr = id(self)
        return f"<{name} at {hex(addr)}>"
