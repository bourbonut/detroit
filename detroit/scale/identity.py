from __future__ import annotations

import math
from typing import Any, TypeVar

from .linear import LinearBase

T = TypeVar("T")


class Identity(LinearBase):
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

    def set_domain(self, domain: list[T]) -> Identity:
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

    @property
    def domain(self):
        return self._domain

    def set_range(self, range_vals: list[T]) -> Identity:
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

    @property
    def range(self):
        return self._domain

    def set_unknown(self, unknown: Any) -> Identity:
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

    @property
    def unknown(self):
        return self._unknown

    def copy(self):
        return Identity(self._domain).set_unknown(self._unknown)


def scale_identity(values: list[T] | None = None) -> Identity:
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
    """
    return Identity(domain=values)
