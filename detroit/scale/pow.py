import math
from collections.abc import Callable
from typing import TypeVar, overload

from ..types import Number
from .continuous import Transformer, copy, identity
from .init import init_range
from .linear import LinearBase

TScalePow = TypeVar("Itself", bound="ScalePow")


def transform_pow(exponent: Number) -> Callable[[float], float]:
    return lambda x: (-math.pow(-x, exponent) if x < 0 else math.pow(x, exponent))


def transform_sqrt(x: float) -> float:
    return -math.sqrt(-x) if x < 0 else math.sqrt(x)


def transform_square(x: float) -> float:
    return -x * x if x < 0 else x * x


class ScalePow(Transformer[float], LinearBase):
    """
    Power ("pow") scales are similar to linear scales, except an exponential
    transform is applied to the input domain value before the output range
    value is computed.
    Each range value y can be expressed as a function of the domain value x:
    :math:`y = m \\cdot x^k + b`, where :math:`k` is the exponent value.
    Power scales also support negative domain values, in which case the
    input value and the resulting output value are multiplied by -1.

    Parameters
    ----------
    t : Callable[[float], float]
        Transform function
    u : Callable[[float], float]
        Untransform function
    exponent : float | int
        Exponent
    """

    def __init__(
        self,
        t: Callable[[float], float] = identity,
        u: Callable[[float], float] = identity,
        exponent: float | int = 1,
    ):
        super().__init__(t, u)
        self._exponent = exponent

    def _pow_rescale(self):
        if self._exponent == 1:
            self._transform = identity
            self._untransform = identity
            self._rescale()
            return self
        elif self._exponent == 0.5:
            self._transform = transform_sqrt
            self._untransform = transform_square
            self._rescale()
            return self
        else:
            self._transform = transform_pow(self._exponent)
            self._untransform = transform_pow(1 / self._exponent)
            self._rescale()
            return self

    def set_exponent(self, exponent: Number) -> TScalePow:
        """
        Sets the current exponent to the given numeric value.

        Parameters
        ----------
        exponent : Number
            exponent

        Returns
        -------
        ScalePow
            Itself
        """
        self._exponent = float(exponent)
        return self._pow_rescale()

    def get_exponent(self) -> Number:
        return self._exponent

    def copy(self):
        return copy(self, ScalePow()).set_exponent(self.get_exponent())


@overload
def scale_pow() -> ScalePow: ...


@overload
def scale_pow(range_vals: list[float]) -> ScalePow: ...


@overload
def scale_pow(domain: list[Number], range_vals: list[float]) -> ScalePow: ...


def scale_pow(*args) -> ScalePow:
    """
    Constructs a new pow scale with the specified domain and
    range, the exponent 1, the default interpolator and
    clamping disabled.

    Parameters
    ----------
    domain : list[Number]
        Array of numbers
    range_vals : list[float]
        Array of values

    Returns
    -------
    ScalePow
        Scale object

    Examples
    --------
    >>> scale = d3.scale_pow([0, 10], [0, 960])
    >>> steps = 10
    >>> for x in range(steps + 1):
    ...     print(x, scale(x))
    ...
    ...
    0 0.0
    1 96.0
    2 192.0
    3 288.0
    4 384.0
    5 480.0
    6 576.0
    7 672.0
    8 768.0
    9 864.0
    10 960.0

    With :code:`exponent = 2`:

    >>> scale = scale.set_exponent(2)
    >>> for x in range(steps + 1):
    ...     print(x, scale(x))
    ...
    ...
    0 0.0
    1 9.6
    2 38.4
    3 86.39999999999999
    4 153.6
    5 240.0
    6 345.59999999999997
    7 470.4
    8 614.4
    9 777.6
    10 960.0
    """
    scale = ScalePow()
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)


@overload
def scale_sqrt() -> ScalePow: ...


@overload
def scale_sqrt(range_vals: list[float]) -> ScalePow: ...


@overload
def scale_sqrt(domain: list[Number], range_vals: list[float]) -> ScalePow: ...


def scale_sqrt(*args) -> ScalePow:
    """
    Constructs a new pow scale with the specified domain and range,
    the exponent 0.5, the default interpolator and clamping disabled.

    Parameters
    ----------
    domain : list[Number]
        Array of numbers
    range_vals : list[float]
        Array of values

    Returns
    -------
    ScalePow
        Scale object

    Examples
    --------
    >>> scale = d3.scale_sqrt([0, 10], [0, 960])
    >>> steps = 10
    >>> for x in range(steps + 1):
    ...     print(x, scale(x))
    ...
    ...
    0 0.0
    1 303.5786553761644
    2 429.3250516799596
    3 525.8136552049594
    4 607.1573107523288
    5 678.8225099390855
    6 743.612802471824
    7 803.1936254727125
    8 858.6501033599192
    9 910.7359661284933
    10 960.0
    """
    scale = ScalePow().set_exponent(0.5)
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)
