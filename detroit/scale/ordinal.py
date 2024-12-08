from __future__ import annotations

from typing import Any, TypeVar, overload

from .init import init_range

U = TypeVar("U")
V = TypeVar("V")


class ScaleOrdinal:
    """
    Unlike continuous scales, ordinal scales have a discrete domain and range.
    For example, an ordinal scale might map a set of named categories to a set
    of colors, or determine the horizontal positions of columns in a column chart.
    """

    def __init__(self):
        self._index = {}
        self._domain = []
        self._range_vals = []
        self._unknown = None

    def __call__(self, d: U) -> V:
        """
        Given a value from the domain, returns the corresponding value from the range.

        Parameters
        ----------
        x : U
            Input value

        Returns
        -------
        V
            Corresponding value from the range
        """
        i = self._index.get(d)
        if i is None:
            if self._unknown is not None:
                return self._unknown
            self._domain.append(d)
            i = len(self._domain) - 1
            self._index[d] = i
        length = len(self._range_vals)
        if not length:
            return None
        index = i % length
        if index >= length or index < 0:
            return None
        return self._range_vals[index]

    def set_domain(self, domain: list[U]) -> ScaleOrdinal:
        """
        Sets the scale’s domain to the specified array of values

        Parameters
        ----------
        domain : list[U]
            Domain

        Returns
        -------
        ScaleOrdinal
            Itself
        """
        self._domain.clear()
        self._index.clear()
        for value in domain:
            if value in self._index:
                continue
            self._domain.append(value)
            self._index[value] = len(self._domain) - 1
        return self

    @property
    def domain(self) -> list[U]:
        return self._domain.copy()

    def set_range(self, range_vals: list[V]) -> ScaleOrdinal:
        """
        Sets the scale’s range to the specified array of values

        Parameters
        ----------
        range_vals : list[V]
            Range values

        Returns
        -------
        ScaleOrdinal
            Itself
        """
        self._range_vals = list(range_vals)
        return self

    @property
    def range(self) -> list[V]:
        return self._range_vals.copy()

    def set_unknown(self, unknown: Any) -> ScaleOrdinal:
        """
        Sets the output value of the scale for undefined
        or NaN input values.

        Parameters
        ----------
        unknown : Any
            Unknown value

        Returns
        -------
        ScaleOrdinal
            Itself
        """
        self._unknown = unknown
        return self

    @property
    def unknown(self) -> Any:
        return self._unknown

    def copy(self):
        return (
            ScaleOrdinal()
            .set_domain(self.domain)
            .set_range(self.range)
            .set_unknown(self.unknown)
        )


@overload
def scale_ordinal() -> ScaleOrdinal: ...


@overload
def scale_ordinal(range_vals: list[V]) -> ScaleOrdinal: ...


@overload
def scale_ordinal(domain: list[U], range_vals: list[V]) -> ScaleOrdinal: ...


def scale_ordinal(*args):
    """
    Build a new ordinal scale with the specified domain and range

    Parameters
    ----------
    domain : list[U]
        Array of values
    range_vals : list[V]
        Array of values

    Returns
    -------
    ScaleOrdinal
        Scale object

    Examples
    --------

    >>> d3.scale_ordinal(["a", "b", "c"], ["red", "green", "blue"])
    """
    scale = ScaleOrdinal()
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)
