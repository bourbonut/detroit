from typing import Generic, TypeVar, overload

from ..types import Number, T
from .init import init_range
from .ordinal import ScaleOrdinal

TScaleBand = TypeVar("Itself", bound="ScaleBand")


class ScaleBand(ScaleOrdinal[T, Number], Generic[T]):
    """
    Band scales are like band scales except the output range is continuous
    and numeric. The scale divides the continuous range into uniform bands.
    Band scales are typically used for bar charts with an band or categorical
    dimension.
    """

    def __init__(self):
        super().__init__()
        self._r0 = 0
        self._r1 = 1
        self._step = None
        self._bandwidth = None
        self._round = False
        self._padding_inner = 0
        self._padding_outer = 0
        self._align = 0.5
        self._rescale()

    def _rescale(self):
        n = len(self._domain)
        reverse = self._r1 < self._r0
        start = self._r1 if reverse else self._r0
        stop = self._r0 if reverse else self._r1
        self._step = (stop - start) / max(
            1, n - self._padding_inner + self._padding_outer * 2
        )
        if self._round:
            self._step = int(self._step)
        start += (stop - start - self._step * (n - self._padding_inner)) * self._align
        self._bandwidth = self._step * (1 - self._padding_inner)
        if self._round:
            start = round(start)
            self._bandwidth = round(self._bandwidth)
        values = [start + self._step * i for i in range(n)]
        return super().set_range(values[::-1] if reverse else values)

    def set_domain(self, domain: list[T]) -> TScaleBand:
        """
        Sets the scale's domain to the specified array of values

        Parameters
        ----------
        domain : list[T]
            Domain

        Returns
        -------
        ScaleBand
            Itself
        """
        super().set_domain(domain)
        return self._rescale()

    def get_domain(self):
        return self._domain.copy()

    def set_range(self, range_vals: list[Number]) -> TScaleBand:
        """
        Sets the scale's range to the specified array of numbers

        Parameters
        ----------
        range_vals : list[Number]
            Range

        Returns
        -------
        ScaleBand
            Itself
        """
        self._r0, self._r1 = map(float, range_vals)
        return self._rescale()

    def get_range(self) -> list[Number]:
        return [self._r0, self._r1]

    def set_range_round(self, range_vals: list[int | range]) -> TScaleBand:
        """
        Sets the scale's range to the specified array of values
        and sets scale's interpolator to :code:`interpolate_round`.

        Parameters
        ----------
        range_vals : list[int | range]
            Range values

        Returns
        -------
        ScaleBand
            Itself
        """
        self._r0, self._r1 = map(float, range_vals)
        self._round = True
        return self._rescale()

    def get_bandwidth(self):
        return self._bandwidth

    def get_step(self):
        return self._step

    def set_round(self, round_val: bool) -> TScaleBand:
        """
        Enable or disable rounding accordingly

        Parameters
        ----------
        round_val : bool
            Round value

        Returns
        -------
        ScaleBand
            Itself
        """
        self._round = bool(round_val)
        return self._rescale()

    def get_round(self):
        return self._round

    def set_padding(self, padding: Number) -> TScaleBand:
        """
        A convenience method for setting the inner and outer padding
        to the same padding value.

        Parameters
        ----------
        padding : Number
            Padding value

        Returns
        -------
        ScaleBand
            Itself
        """
        self._padding_outer = float(padding)
        self._padding_inner = min(1, self._padding_outer)
        return self._rescale()

    def get_padding(self):
        return self._padding_inner

    def set_padding_inner(self, padding_inner: Number) -> TScaleBand:
        """
        Sets the inner padding to the specified number which must
        be less than or equal to 1

        Parameters
        ----------
        padding_inner : Number
            Inner padding value

        Returns
        -------
        ScaleBand
            Itself
        """
        self._padding_inner = min(1, float(padding_inner))
        return self._rescale()

    def set_padding_outer(self, padding_outer: Number) -> TScaleBand:
        """
        Sets the outer padding to the specified number
        which is typically in the range [0, 1]

        Parameters
        ----------
        padding_outer : Number
            Outer padding value

        Returns
        -------
        ScaleBand
            Itself
        """
        self._padding_outer = float(padding_outer)
        return self._rescale()

    def get_padding_inner(self):
        return self._padding_inner

    def get_padding_outer(self):
        return self._padding_outer

    def set_align(self, align: Number) -> TScaleBand:
        """
        Sets the alignment to the specified value which must
        be in the range [0, 1]

        Parameters
        ----------
        align : Number
            Alignment value

        Returns
        -------
        ScaleBand
            Itself
        """
        self._align = max(0, min(1, float(align)))
        return self._rescale()

    def get_align(self):
        return self._align

    def copy(self):
        return (
            ScaleBand()
            .set_domain(self._domain)
            .set_range([self._r0, self._r1])
            .set_round(self._round)
            .set_padding_inner(self._padding_inner)
            .set_padding_outer(self._padding_outer)
            .set_align(self._align)
        )

    def __str__(self) -> str:
        name = self.__class__.__name__
        attrbs = ["domain", "range", "padding_inner", "padding_outer"]
        attrbs = (f"{a}={getattr(self, f'get_{a}')()}" for a in attrbs)
        attrbs = ", ".join(attrbs)
        return f"{name}({attrbs})"

    def __repr__(self) -> str:
        name = self.__class__.__name__
        addr = id(self)
        return f"<{name} at {hex(addr)}>"


@overload
def scale_band() -> TScaleBand: ...


@overload
def scale_band(range_vals: list[Number]) -> TScaleBand: ...


@overload
def scale_band(domain: list[T], range_vals: list[Number]) -> TScaleBand: ...


def scale_band(*args):
    """
    Builds a new band scale with the specified domain
    and range, no padding, no rounding and center alignment

    Parameters
    ----------
    domain : list[T]
        Array of values
    range_vals : list[Number]
        Array of numbers

    Returns
    -------
    ScaleBand
        Scale object

    Examples
    --------

    >>> scale = d3.scale_band(["a", "b", "c"], [0, 960])
    >>> for c in "abcdefgh":
    ...     print(c, scale(c))
    ...
    ...
    a 0.0
    b 320.0
    c 640.0
    d 0.0
    e 320.0
    f 640.0
    g 0.0
    h 320.0
    >>> scale.get_bandwidth()
    320.0
    """
    scale = ScaleBand()
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)


@overload
def scale_point() -> ScaleBand[T]: ...


@overload
def scale_point(range_vals: list[Number]) -> ScaleBand[T]: ...


@overload
def scale_point(domain: list[T], range_vals: list[Number]) -> ScaleBand[T]: ...


def scale_point(*args):
    """
    Builds a new point scale with the specified domain and
    range, no padding, no rounding and center alignment

    Parameters
    ----------
    domain : list[T]
        Array of values
    range_vals : list[Number]
        Array of numbers

    Returns
    -------
    ScaleBand
        Scale object

    Examples
    --------

    >>> scale = d3.scale_point(["a", "b", "c"], [0, 960])
    >>> for c in "abcdefgh":
    ...     print(c, scale(c))
    ...
    ...
    a 0.0
    b 480.0
    c 960.0
    d 0.0
    e 480.0
    f 960.0
    g 0.0
    h 480.0
    >>> scale.get_bandwidth()
    0.0
    """
    scale = ScaleBand().set_padding_inner(1)
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)
