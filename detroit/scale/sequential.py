from __future__ import annotations

import math
from collections.abc import Callable
from datetime import datetime
from typing import Any, Generic, TypeVar, overload

from ..interpolate import interpolate, interpolate_round
from ..types import Number, T
from .continuous import identity
from .init import init_interpolator
from .linear import LinearBase
from .log import LogBase, logp, powp, reflect, transform_log, transform_logn
from .pow import transform_pow, transform_sqrt
from .symlog import transform_symlog

TSequential = TypeVar("Itself", bound="Sequential")
TSequentialPow = TypeVar("Itself", bound="SequentialPow")
TSequentialLog = TypeVar("Itself", bound="SequentialLog")
TSequentialSymlog = TypeVar("Itself", bound="SequentialSymlog")


class Sequential(Generic[T]):
    """
    Sequential transformation

    Parameters
    ----------
    t : Callable[[Number], T]
        Transform function
    """

    def __init__(self, t: Callable[[Number], T]):
        self._x0 = 0
        self._x1 = 1
        self._transform = t
        self._t0 = t(self._x0)
        self._t1 = t(self._x1)
        self._k10 = 0 if self._t0 == self._t1 else 1 / (self._t1 - self._t0)
        self._interpolator = identity
        self._clamp = False
        self._unknown = None

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
        if x is None or (isinstance(x, float) and math.isnan(x)):
            return self._unknown
        if self._k10 == 0:
            x = 0.5
        else:
            x = (self._transform(x) - self._t0) * self._k10
            if self._clamp:
                x = max(0, min(1, x))
        return self._interpolator(x)

    def set_domain(self, domain: list[Number]) -> TSequential:
        """
        Sets the scale's domain to the specified array of numbers

        Parameters
        ----------
        domain : list[Number]
            Domain

        Returns
        -------
        Sequential
            Itself
        """
        self._x0, self._x1 = map(float, list(domain)[:2])
        self._t0 = self._transform(self._x0)
        self._t1 = self._transform(self._x1)
        self._k10 = 0 if self._t0 == self._t1 else 1 / (self._t1 - self._t0)
        return self

    def get_domain(self) -> list[Number]:
        return [self._x0, self._x1]

    def set_clamp(self, clamp: bool) -> TSequential:
        """
        Enables or disables clamping accordingly.

        Parameters
        ----------
        clamp : bool
            Clamp value

        Returns
        -------
        Sequential
            Itself
        """
        self._clamp = bool(clamp)
        return self

    def get_clamp(self) -> bool:
        return self._clamp

    def set_interpolator(self, interpolator: Callable[[float], float]) -> TSequential:
        """
        Sets the scale’s interpolator to the specified function.

        Parameters
        ----------
        interpolator: Callable[[float], float]
            Interpolator function

        Returns
        -------
        Sequential
            Itself
        """
        self._interpolator = interpolator
        return self

    def get_interpolator(self) -> Callable[[float], float]:
        return self._interpolator

    def set_range(self, range_vals: list[T]) -> TSequential:
        """
        The given two-element array is converted
        to an interpolator function using interpolate

        Parameters
        ----------
        range_vals : list[T]
            Two values

        Returns
        -------
        Sequential
            Itself
        """
        self._r0, self._r1 = list(range_vals)[:2]
        self._interpolator = interpolate(self._r0, self._r1)
        return self

    def get_range(self) -> list[T]:
        return [self._interpolator(0), self._interpolator(1)]

    def set_range_round(self, range_vals: list[T]) -> TSequential:
        """
        Sets the scale's range to the specified array of values
        and sets scale's interpolator to :code:`interpolate_round`.

        Parameters
        ----------
        range_vals : list[T]
            Range values

        Returns
        -------
        Sequential
            Itself
        """
        self._r0, self._r1 = range_vals
        self._interpolator = interpolate_round(self._r0, self._r1)
        return self

    def get_range_round(self) -> list[T]:
        return [self._interpolator(0), self._interpolator(1)]

    def set_unknown(self, unknown: Any) -> TSequential:
        """
        Sets the output value of the scale for undefined
        or NaN input values.

        Parameters
        ----------
        unknown : Any
            Unknown value

        Returns
        -------
        Sequential
            Itself
        """
        self._unknown = unknown
        return self

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


def copy(source, target):
    return (
        target.set_domain(source.get_domain())
        .set_interpolator(source.get_interpolator())
        .set_clamp(source.get_clamp())
        .set_unknown(source.get_unknown())
    )


class SequentialLinear(Sequential[float], LinearBase):
    """
    Linear sequential transformation
    """

    def __init__(self):
        Sequential.__init__(self, identity)

    def copy(self):
        return copy(self, SequentialLinear())


class SequentialLog(Sequential[float], LogBase):
    """
    Log sequential transformation
    """

    def __init__(self):
        Sequential.__init__(self, identity)
        LogBase.__init__(self)
        self._transform = transform_log
        self.set_domain([1, 10])

    def _rescale(self):
        self._logs = logp(self._base)
        self._pows = powp(self._base)
        d = self.get_domain()[0]
        if isinstance(d, datetime):
            d = d.timestamp()
        if d < 0:
            self._logs = reflect(self._logs)
            self._pows = reflect(self._pows)
            self._transform = transform_logn
        else:
            self._transform = transform_log
        return self

    def set_domain(self, domain: list[Number]) -> TSequentialLog:
        """
        Sets the scale's domain to the specified array of numbers

        Parameters
        ----------
        domain : list[Number]
            Domain

        Returns
        -------
        SequentialLog
            Itself
        """
        self._x0, self._x1 = map(float, list(domain)[:2])
        self._rescale()
        super().set_domain(domain)
        return self

    def copy(self):
        return copy(self, SequentialLog()).base(self.base)


class SequentialSymlog(Sequential[float]):
    """
    Symlog sequential transformation

    Parameters
    ----------
    c : Number
        Symlog constant value
    """

    def __init__(self, c: Number = 1):
        self._c = c
        super().__init__(transform_symlog(self._c))

    def set_constant(self, c: Number) -> TSequentialSymlog:
        """
        Sets the symlog constant to the specified number and returns this scale.

        Parameters
        ----------
        c : Number
            Constant value

        Returns
        -------
        SequentialSymlog
            Itself
        """
        self._c = float(c)
        self._transform = transform_symlog(self._c)
        return self

    def copy(self):
        return copy(self, SequentialSymlog()).set_constant(self.constant)


class SequentialPow(Sequential[float], LinearBase):
    """
    Power sequential transformation

    Parameters
    ----------
    t : Callable[[Number], T]
        Transform function
    """

    def __init__(self, t: Callable[[Number], float] = identity):
        super().__init__(t)
        self._exponent = 1

    def _rescale(self) -> TSequentialPow:
        if self._exponent == 1:
            self._transform = identity
            return self
        elif self._exponent == 0.5:
            self._transform = transform_sqrt
            return self
        else:
            self._transform = transform_pow(self._exponent)
            return self

    def set_exponent(self, exponent: Number) -> TSequentialPow:
        """
        Sets the scale's exponent value.

        Parameters
        ----------
        exponent : Number
            Exponent value

        Returns
        -------
        SequentialPow
            Itself
        """
        self._exponent = float(exponent)
        return self._rescale()

    def get_exponent(self):
        return self._exponent

    def copy(self):
        return copy(self, SequentialPow()).set_exponent(self.exponent)


@overload
def scale_sequential() -> SequentialLinear: ...


@overload
def scale_sequential(interpolator: Callable[[float], float]) -> SequentialLinear: ...


@overload
def scale_sequential(
    domain: list[Number], interpolator: Callable[[float], float]
) -> SequentialLinear: ...


def scale_sequential(*args):
    """
    Builds a new sequential scale with the specified
    domain and interpolator function or array.

    Parameters
    ----------
    domain : list[Number]
        Domain
    interpolator: Callable[[float], float]
        Interpolator

    Returns
    -------
    SequentialLinear
        Sequential object

    Examples
    --------

    >>> scale = d3.scale_sequential([0, 100], d3.interpolate_blues)
    >>> for x in range(11):
    ...     x = 10 * x
    ...     print(x, scale(x))
    ...
    ...
    0 rgb(247, 251, 255)
    10 rgb(227, 238, 249)
    20 rgb(207, 225, 242)
    30 rgb(181, 212, 233)
    40 rgb(147, 195, 223)
    50 rgb(109, 174, 213)
    60 rgb(75, 151, 201)
    70 rgb(47, 126, 188)
    80 rgb(24, 100, 170)
    90 rgb(10, 74, 144)
    100 rgb(8, 48, 107)
    >>> d3.interpolate_blues(0)
    'rgb(247, 251, 255)'
    >>> d3.interpolate_blues(1)
    'rgb(8, 48, 107)'
    """
    scale = SequentialLinear()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


@overload
def scale_sequential_log() -> SequentialLog: ...


@overload
def scale_sequential_log(interpolator: Callable[[float], float]) -> SequentialLog: ...


@overload
def scale_sequential_log(
    domain: list[Number], interpolator: Callable[[float], float]
) -> SequentialLog: ...


def scale_sequential_log(*args):
    """
    Builds a new sequential scale with a logarithmic
    transform, analogous to a log scale.

    Parameters
    ----------
    domain : list[Number]
        Domain
    interpolator: Callable[[float], float]
        Interpolator

    Returns
    -------
    SequentialLog
        Sequential object

    Examples
    --------

    >>> scale = d3.scale_sequential_log([1, 100], d3.interpolate_blues)
    >>> steps = 10
    >>> for x in range(steps + 1):
    ...     x = 2 * x / steps
    ...     x = 10 ** x
    ...     print(x, scale(x))
    ...
    ...
    1.0 rgb(247, 251, 255)
    1.5848931924611136 rgb(227, 238, 249)
    2.51188643150958 rgb(207, 225, 242)
    3.9810717055349722 rgb(181, 212, 233)
    6.309573444801933 rgb(147, 195, 223)
    10.0 rgb(109, 174, 213)
    15.848931924611133 rgb(75, 151, 201)
    25.118864315095795 rgb(47, 126, 188)
    39.810717055349734 rgb(24, 100, 170)
    63.09573444801933 rgb(10, 74, 144)
    100.0 rgb(8, 48, 107)
    >>> d3.interpolate_blues(0)
    'rgb(247, 251, 255)'
    >>> d3.interpolate_blues(1)
    'rgb(8, 48, 107)'
    """
    scale = SequentialLog()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


@overload
def scale_sequential_symlog() -> SequentialSymlog: ...


@overload
def scale_sequential_symlog(
    interpolator: Callable[[float], float],
) -> SequentialSymlog: ...


@overload
def scale_sequential_symlog(
    domain: list[Number], interpolator: Callable[[float], float]
) -> SequentialSymlog: ...


def scale_sequential_symlog(*args):
    """
    Builds a new sequential scale with a symmetric
    logarithmic transform, analogous to a symlog scale.

    Parameters
    ----------
    domain : list[Number]
        Domain
    interpolator: Callable[[float], float]
        Interpolator

    Returns
    -------
    SequentialSymlog
        Sequential object

    Examples
    --------

    >>> scale = d3.scale_sequential_symlog([1, 100], d3.interpolate_blues)
    >>> scale = scale.set_constant(2)
    >>> steps = 10
    >>> for x in range(steps + 1):
    ...     x = 2 * x / steps
    ...     x = 10 ** x
    ...     print(x, scale(x))
    ...
    ...
    1.0 rgb(255, 255, 255)
    1.5848931924611136 rgb(253, 255, 255)
    2.51188643150958 rgb(241, 247, 253)
    3.9810717055349722 rgb(227, 238, 248)
    6.309573444801933 rgb(210, 227, 243)
    10.0 rgb(187, 215, 235)
    15.848931924611133 rgb(154, 199, 225)
    25.118864315095795 rgb(113, 177, 214)
    39.810717055349734 rgb(75, 152, 201)
    63.09573444801933 rgb(44, 123, 186)
    100.0 rgb(19, 94, 165)
    >>> d3.interpolate_blues(0)
    'rgb(247, 251, 255)'
    >>> d3.interpolate_blues(1)
    'rgb(8, 48, 107)'
    """
    scale = SequentialSymlog()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


@overload
def scale_sequential_pow() -> SequentialPow: ...


@overload
def scale_sequential_pow(interpolator: Callable[[float], float]) -> SequentialPow: ...


@overload
def scale_sequential_pow(
    domain: list[Number], interpolator: Callable[[float], float]
) -> SequentialPow: ...


def scale_sequential_pow(*args):
    """
    Builds a new sequential scale with an exponential
    transform, analogous to a power scale.


    Parameters
    ----------
    domain : list[Number]
        Domain
    interpolator: Callable[[float], float]
        Interpolator

    Returns
    -------
    SequentialPow
        Sequential object

    Examples
    --------

    >>> scale = d3.scale_sequential_pow([0, 100], d3.interpolate_blues)
    >>> scale = scale.set_exponent(2)
    >>> steps = 10
    >>> for x in range(steps + 1):
    ...     x = 10 * x / steps
    ...     print(x, scale(x))
    ...
    ...
    0.0 rgb(247, 251, 255)
    1.0 rgb(245, 250, 254)
    2.0 rgb(239, 246, 252)
    3.0 rgb(229, 239, 249)
    4.0 rgb(215, 231, 245)
    5.0 rgb(195, 219, 238)
    6.0 rgb(162, 203, 227)
    7.0 rgb(112, 176, 214)
    8.0 rgb(63, 141, 196)
    9.0 rgb(22, 98, 168)
    10.0 rgb(8, 48, 107)
    >>> d3.interpolate_blues(0)
    'rgb(247, 251, 255)'
    >>> d3.interpolate_blues(1)
    'rgb(8, 48, 107)'
    """
    scale = SequentialPow()
    if len(args) == 1:
        return init_interpolator(scale, interpolator=args[0])
    elif len(args) == 2:
        domain, interpolator = args
        return init_interpolator(scale, domain=domain, interpolator=interpolator)
    return init_interpolator(scale)


@overload
def scale_sequential_sqrt() -> SequentialPow: ...


@overload
def scale_sequential_sqrt(interpolator: Callable[[float], float]) -> SequentialPow: ...


@overload
def scale_sequential_sqrt(
    domain: list[Number], interpolator: Callable[[float], float]
) -> SequentialPow: ...


def scale_sequential_sqrt(*args):
    """
    Builds a new sequential scale with a square-root
    transform, analogous to a sqrt scale


    Parameters
    ----------
    domain : list[Number]
        Domain
    interpolator: Callable[[float], float]
        Interpolator

    Returns
    -------
    SequentialSqrt
        Sequential object

    Examples
    --------

    >>> scale = d3.scale_sequential_sqrt([0, 100], d3.interpolate_blues)
    >>> steps = 10
    >>> for x in range(steps + 1):
    ...     x = 100**2 * x / steps
    ...     print(x, scale(x))
    ...
    ...
    0.0 rgb(247, 251, 255)
    1000.0 rgb(176, 210, 232)
    2000.0 rgb(129, 186, 219)
    3000.0 rgb(92, 163, 208)
    4000.0 rgb(65, 143, 197)
    5000.0 rgb(45, 124, 186)
    6000.0 rgb(29, 107, 175)
    7000.0 rgb(17, 91, 162)
    8000.0 rgb(11, 76, 146)
    9000.0 rgb(8, 62, 127)
    10000.0 rgb(8, 48, 107)
    >>> d3.interpolate_blues(0)
    'rgb(247, 251, 255)'
    >>> d3.interpolate_blues(1)
    'rgb(8, 48, 107)'
    """
    return scale_sequential_pow(*args).set_exponent(0.5)
