from typing import Any, Generic, TypeVar, overload

from ..types import U, V
from .init import init_range

TScaleOrdinal = TypeVar("Itself", bound="ScaleOrdinal")


class ScaleOrdinal(Generic[U, V]):
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

    def set_domain(self, domain: list[U]) -> TScaleOrdinal:
        """
        Sets the scale’s domain to the specified array of values.

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

    def get_domain(self) -> list[U]:
        return self._domain.copy()

    def set_range(self, range_vals: list[V]) -> TScaleOrdinal:
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

    def get_range(self) -> list[V]:
        return self._range_vals.copy()

    def set_unknown(self, unknown: Any) -> TScaleOrdinal:
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

    def get_unknown(self) -> Any:
        return self._unknown

    def copy(self):
        return (
            ScaleOrdinal()
            .set_domain(self.get_domain())
            .set_range(self.get_range())
            .set_unknown(self.get_unknown())
        )

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


@overload
def scale_ordinal() -> ScaleOrdinal[U, V]: ...


@overload
def scale_ordinal(range_vals: list[V]) -> ScaleOrdinal[U, V]: ...


@overload
def scale_ordinal(domain: list[U], range_vals: list[V]) -> ScaleOrdinal[U, V]: ...


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
    ScaleOrdinal[U, V]
        Scale object

    Examples
    --------

    >>> scale = d3.scale_ordinal(["a", "b", "c"], ["red", "green", "blue"])
    >>> for c in "abcdefgh":
    ...     print(c, scale(c))
    ...
    ...
    a red
    b green
    c blue
    d red
    e green
    f blue
    g red
    h green
    """
    scale = ScaleOrdinal()
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)
