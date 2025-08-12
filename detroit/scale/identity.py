import math
from typing import Any, Generic, TypeVar

from ..types import T
from .linear import LinearBase

TIdentity = TypeVar("Itself", bound="Identity")


class Identity(LinearBase, Generic[T]):
    """
    Build a new identity scale with the specified range (and by extension, domain).
    """

    def __init__(self, domain=None):
        self._domain = list(domain) if domain is not None else [0, 1]
        self._unknown = None

    def __call__(self, x: T) -> T:
        """
        Returns same value if valid type

        Parameters
        ----------
        x : T
            Input value

        Returns
        -------
        T
            Input value if valid type
        """
        unvalid_type = x is None or (isinstance(x, float) and math.isnan(x))
        return self._unknown if unvalid_type else x

    def invert(self, x: T) -> T:
        """
        Returns same value if valid type

        Parameters
        ----------
        x : T
            Input value

        Returns
        -------
        T
            Input value if valid type
        """
        return self(x)

    def set_domain(self, domain: list[T]) -> TIdentity:
        """
        Sets the scale’s domain

        Parameters
        ----------
        domain : list[T]
            Domain

        Returns
        -------
        Identity
            Itself
        """
        self._domain = list(domain)
        return self

    def get_domain(self):
        return self._domain

    def set_range(self, range_vals: list[T]) -> TIdentity:
        """
        Sets the scale’s range

        Parameters
        ----------
        range_vals : list[T]
            Range values

        Returns
        -------
        Identity
            Itself
        """
        return self.set_domain(range_vals)

    def get_range(self):
        return self._domain

    def set_unknown(self, unknown: Any) -> TIdentity:
        """
        Sets the output value of the scale for undefined
        or NaN input values.

        Parameters
        ----------
        unknown : Any
            Unknown value

        Returns
        -------
        Identity
            Itself
        """
        self._unknown = unknown
        return self

    def get_unknown(self):
        return self._unknown

    def copy(self):
        return Identity(self._domain).set_unknown(self._unknown)

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


def scale_identity(values: list[T] | None = None) -> Identity[T]:
    """
    Build a new identity scale with the specified range
    (and by extension, domain).

    Parameters
    ----------
    values : list[T] | None
        Values to set

    Returns
    -------
    Identity
        Scale object

    Examples
    --------

    >>> scale = d3.scale_identity()
    >>> scale(3)
    3
    >>> scale("a")
    'a'
    """
    return Identity(domain=values)
