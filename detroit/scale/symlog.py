import math
from typing import TypeVar, overload

from ..types import Number, T
from .continuous import Transformer, copy
from .init import init_range
from .linear import LinearBase

TScaleSymlog = TypeVar("Itself", bound="ScaleSymlog")


def sign(x):
    return -1 if x < 0 else 1


def transform_symlog(c):
    return lambda x: sign(x) * math.log1p(abs(x / c))


def transform_symexp(c):
    return lambda x: sign(x) * math.expm1(abs(x)) * c


class ScaleSymlog(Transformer[float], LinearBase):
    """
    A bi-symmetric log transformation for wide-range data by Webber for
    details. Unlike a log scale, a symlog scale domain can include zero.

    Parameters
    ----------
    c : Number
        Symlog constant value
    """

    def __init__(self, c: Number = 1):
        self._c = c
        super().__init__(transform_symlog(self._c), transform_symexp(self._c))

    def set_constant(self, c: Number) -> TScaleSymlog:
        """
        Sets the symlog constant to the specified number and returns this scale.

        Parameters
        ----------
        c : Number
            Constant value

        Returns
        -------
        ScaleSymlog
            Itself
        """
        self._c = float(c)
        self._transform = transform_symlog(self._c)
        self._untransform = transform_symexp(self._c)
        self._rescale()
        return self

    def get_constant(self):
        return self._c

    def copy(self):
        return copy(self, ScaleSymlog()).set_constant(self.get_constant())


@overload
def scale_symlog() -> ScaleSymlog: ...


@overload
def scale_symlog(range_vals: list[T]) -> ScaleSymlog: ...


@overload
def scale_symlog(domain: list[Number], range_vals: list[T]) -> ScaleSymlog: ...


def scale_symlog(*args):
    """
    Builds a new continuous scale with the specified domain and
    range, the constant 1, the default interpolator and clamping
    disabled.

    Parameters
    ----------
    domain : list[Number]
        Array of numbers
    range_vals : list[Number]
        Array of values

    Returns
    -------
    ScaleSymlog
        Scale object

    Examples
    --------

    >>> scale = d3.scale_symlog([0, 100], [0, 960])
    >>> scale = scale.set_constant(2)
    >>> steps = 10
    >>> scale(0)
    0.0
    >>> scale(0.5)
    54.48303899306232
    >>> for x in range(steps + 1):
    ...     x = 2 * x / steps
    ...     x = 10 ** x
    ...     print(x, scale(x))
    ...
    ...
    1.0 98.9989231832065
    1.5848931924611136 142.48806851481947
    2.51188643150958 198.64193111140278
    3.9810717055349722 267.46722288814453
    6.309573444801933 347.7495648320975
    10.0 437.47847720986016
    15.848931924611133 534.4195868305859
    25.118864315095795 636.548856160817
    39.810717055349734 742.2519630838442
    63.09573444801933 850.343754278314
    """
    scale = ScaleSymlog()
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)
