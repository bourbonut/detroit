from __future__ import annotations

from collections.abc import Callable
from inspect import signature
from typing import Literal, Type

from ..scale.continuous import Transformer
from ..scale.diverging import Diverging
from ..scale.sequential import Sequential
from ..selection.selection import Selection

TOP = 1
RIGHT = 2
BOTTOM = 3
LEFT = 4
EPSILON = 1e-6


def translate_x(x):
    return f"translate({x}, 0)"


def translate_y(y):
    return f"translate(0, {y})"


def number(scale):
    def f(d):
        return float(scale(d))

    return f


def center(scale, offset):
    offset = max(0, scale.bandwidth - offset * 2) / 2
    if scale.round:
        offset = round(offset)
    return lambda d: float(scale(d)) + offset


# def entering(context):
#     return not hasattr(context, "__axis")


class Axis:
    """
    Builds a new oriented axis generator for the given scale,
    with empty tick arguments, a tick size of 6 and padding of 3.

    Parameters
    ----------
    orient : Literal[1, 2, 3, 4]
        Orientation
    scale : Type[Transformer | Sequential | Diverging]
        Scaler
    """

    def __init__(
        self,
        orient: Literal[1, 2, 3, 4],
        scale: Type[Transformer | Sequential | Diverging],
    ):
        self._scale = scale
        self._orient = orient
        self._tick_arguments = []
        self._tick_values = None
        self._tick_format = None
        self._tick_size_inner = 6
        self._tick_size_outer = 6
        self._tick_padding = 3
        self._offset = 0.5
        self._k = -1 if orient in [TOP, LEFT] else 1
        self._x = "x" if orient in [LEFT, RIGHT] else "y"
        self._transform = translate_x if orient in [TOP, BOTTOM] else translate_y

    def __call__(self, context: Selection):
        """
        Render the axis to the given context, which may be either a selection
        of SVG containers (either SVG or G elements) or a corresponding transition.

        Parameters
        ----------
        context : Selection
            Context

        Examples
        --------

        >>> svg.append("g")
        ...     .attr("transform", f"translate(0, {height - margin.bottom})")
        ...     .call(d3.axis_bottom(x))

        Notes
        -----
        Transitions are not yet implemented
        """
        if self._tick_values is not None:
            values = self._tick_values
        elif hasattr(self._scale, "ticks"):
            nargs = len(signature(self._scale.ticks).parameters)
            args = self._tick_arguments[:nargs]
            values = self._scale.ticks(*args)
        else:
            values = self._scale.domain

        if self._tick_format is not None:
            format_func = self._tick_format
        elif hasattr(self._scale, "tick_format"):
            nargs = len(signature(self._scale.tick_format).parameters)
            args = self._tick_arguments[:nargs]
            format_func = self._scale.tick_format(*args)
        else:

            def format_func(d):
                return d

        spacing = max(self._tick_size_inner, 0) + self._tick_padding
        range_values = self._scale.range
        range0 = float(range_values[0]) + self._offset
        range1 = float(range_values[-1]) + self._offset

        if hasattr(self._scale, "bandwidth"):
            position = center(self._scale.copy(), self._offset)
        else:
            position = number(self._scale.copy())

        selection = context.selection() if hasattr(context, "selection") else context
        path = selection.select_all(".domain").data([None])
        tick = selection.select_all(".tick").data(values, self._scale).order()
        tick_exit = tick.exit()
        tick_enter = tick.enter().append("g").attr("class", "tick")
        line = tick.select("line")
        text = tick.select("text")

        path = path.merge(
            path.enter()
            .insert("path", ".tick")
            .attr("class", "domain")
            .attr("stroke", "currentColor")
        )

        tick = tick.merge(tick_enter)

        line = line.merge(
            tick_enter.append("line")
            .attr("stroke", "currentColor")
            .attr(f"{self._x}2", self._k * self._tick_size_inner)
        )

        text = text.merge(
            tick_enter.append("text")
            .attr("fill", "currentColor")
            .attr(self._x, self._k * spacing)
            .attr(
                "dy",
                "0em"
                if self._orient == TOP
                else "0.71em"
                if self._orient == BOTTOM
                else "0.32em",
            )
        )

        # TODO : transition implementation
        # if context != selection:
        #     path = path.transition(context)
        #     tick = tick.transition(context)
        #     line = line.transition(context)
        #     text = text.transition(context)
        #
        #     def transform(d):
        #         d = position(d)
        #         if d is not None and math.isfinite(d):
        #             return self._transform(position(d) + self._offset)
        #
        #     tick_exit = (
        #         tick_exit.transition(context)
        #                  .attr("opacity", EPSILON)
        #                  .attr("transform", transform)
        #     )
        #
        #     def transform(d): # TODO
        #         return None
        #
        #     tick_enter.attr("opacity", EPSILON).attr("transform", transform)

        tick_exit.remove()

        if self._orient == LEFT or self._orient == RIGHT:
            if self._tick_size_outer:
                path.attr(
                    "d",
                    f"M{self._k * self._tick_size_outer},{range0}H{self._offset}V{range1}H{self._k * self._tick_size_outer}",
                )
            else:
                path.attr("d", f"M{self._offset},{range0}V{range1}")
        else:
            if self._tick_size_outer:
                path.attr(
                    "d",
                    f"M{range0},{self._k * self._tick_size_outer}V{self._offset}H{range1}V{self._k * self._tick_size_outer}",
                )
            else:
                path.attr("d", f"M{range0},{self._offset}H{range1}")

        def transform(d, *args):
            return self._transform(position(d) + self._offset)

        tick.attr("opacity", 1).attr("transform", transform)

        line.attr(f"{self._x}2", self._k * self._tick_size_inner)

        text.attr(self._x, self._k * spacing).text(format_func)

        (
            selection.attr("fill", "none")  # .filter(entering(context))
            .attr("font-size", 10)
            .attr("font-family", "sans-serif")
            .attr(
                "text-anchor",
                "start"
                if self._orient == RIGHT
                else "end"
                if self._orient == LEFT
                else "middle",
            )
        )

    def set_scale(self, scale: Type[Transformer | Sequential | Diverging]) -> Axis:
        """
        Sets scale value

        Parameters
        ----------
        scale : Type[Transformer | Sequential | Diverging]
            New scale

        Returns
        -------
        Axis
            Itself

        Examples
        --------

        >>> x_axis = d3.axis_bottom().scale(x)
        """
        self._scale = scale
        return self

    @property
    def scale(self) -> Type[Transformer | Sequential | Diverging]:
        return self._scale

    def set_ticks(self, *ticks: int | str | Callable) -> Axis:
        """
        Tick values will be passed to :code:`scale.ticks` and
        :code:`scale.tick_format` when :code:`Axis.__call__` is called

        Parameters
        ----------
        *ticks : int | str | Callable
            It depends on :code:`scale` type. Most of the time, it is the
            *count* for the number of ticks and optional format specifier

        Returns
        -------
        Axis
            Itself

        Examples
        --------

        To generate twenty ticks with SI-prefix formatting on a linear scale :

        >>> axis.set_ticks(20, "s")

        To generate ticks every fifteen minutes with a time scale :

        >>> axis.set_ticks(d3.time_minute.every(15))

        Note the similarities with :code:`set_tick_arguments` :

        >>> axis.set_ticks(10) # same as axis.set_tick_arguments([10])
        """
        self._tick_arguments = list(ticks)
        return self

    def set_tick_arguments(self, tick_arguments: list[int | str | Callable]) -> Axis:
        """
        Tick arguments will be passed to :code:`scale.ticks` and
        :code:`scale.tick_format` when :code:`Axis.__call__` is called

        Parameters
        ----------
        tick_arguments : list[int | str | Callable]
            It depends on :code:`scale` type. Most of the time, it is the
            *count* for the number of ticks and optional format specifier

        Returns
        -------
            Itself

        Examples
        --------

        To generate twenty ticks with SI-prefix formatting on a linear scale :

        >>> axis.set_tick_arguments([20, "s"])

        To generate ticks every fifteen minutes with a time scale :

        >>> axis.set_tick_arguments([d3.time_minute.every(15)])
        """
        self._tick_arguments = list(tick_arguments)
        return self

    @property
    def tick_arguments(self) -> list[int | str | Callable]:
        return self._tick_arguments.copy()

    def set_tick_values(self, tick_values: list[int | float]) -> Axis:
        """
        Ticks values are used for ticks rather than the scale’s
        automatic tick generator.

        Parameters
        ----------
        tick_values : list[int | float]
            Tick values

        Returns
        -------
        Axis
            Itself

        Examples
        --------

        >>> axis = d3.axis_bottom(x).set_tick_values([1, 2, 3, 5, 8, 13, 21])
        """
        self._tick_values = tick_values
        return self

    @property
    def tick_values(self) -> list[int | float]:
        return self._tick_values

    def set_tick_format(self, tick_format: Callable) -> Axis:
        """
        Sets the tick format function and returns the axis.

        Parameters
        ----------
        tick_format : Callable
            Tick formatter

        Returns
        -------
        Axis
            Itself

        Examples
        --------

        For example, to display integers with comma-grouping for thousands :

        >>> axis.set_tick_format(d3.format(",.0f"))
        """
        self._tick_format = tick_format
        return self

    @property
    def tick_format(self) -> Callable:
        return self._tick_format

    def set_tick_size(self, tick_size: int) -> Axis:
        """
        Sets the inner and outer tick size to the specified
        value and returns the axis.

        Parameters
        ----------
        tick_size : int
            Tick size

        Returns
        -------
        Axis
            Itself

        Examples
        --------

        >>> d3.axis_bottom().set_tick_size(0)
        """
        self._tick_size_inner = self._tick_size_outer = tick_size
        return self

    def set_tick_size_inner(self, tick_size_inner: int) -> Axis:
        """
        Sets the inner tick size to the specified value and
        returns the axis.

        Parameters
        ----------
        tick_size_inner : int
            Inner tick size

        Returns
        -------
        Axis
            Itself

        Examples
        --------

        >>> d3.axis_bottom().set_tick_size_inner(0)
        """
        self._tick_size_inner = tick_size_inner
        return self

    @property
    def tick_size_inner(self) -> int:
        return self._tick_size_inner

    def set_tick_size_outer(self, tick_size_outer: int) -> Axis:
        """
        Sets the outer tick size to the specified value and
        returns the axis.

        Parameters
        ----------
        tick_size_outer : int
            Outer tick size

        Returns
        -------
        Axis
            Itself

        Examples
        --------

        >>> d3.axis_bottom().set_tick_size_outer(0)
        """
        self._tick_size_outer = tick_size_outer
        return self

    @property
    def tick_size_outer(self) -> Axis:
        return self._tick_size_outer

    def set_tick_padding(self, tick_padding: int) -> Axis:
        """
        Sets the padding to the specified value in pixels.

        Parameters
        ----------
        tick_padding : int
            Tick padding in pixels

        Returns
        -------
        Axis
            Itself

        Examples
        --------

        >>> d3.axis_bottom().set_tick_padding(0)
        """
        self._tick_padding = tick_padding
        return self

    @property
    def tick_padding(self) -> Axis:
        return self._tick_padding

    def set_offset(self, offset: int | float) -> Axis:
        """
        Sets the pixel offset to the specified value in pixels.

        Parameters
        ----------
        offset : int | float
            Pixel offset

        Returns
        -------
        Axis
            Itself

        Examples
        --------

        >>> d3.axis_bottom().set_offset(0)
        """
        self._offset = offset
        return self

    @property
    def offset(self) -> int | float:
        return self._offset


def axis_top(scale: Type[Transformer | Sequential | Diverging]) -> Axis:
    """
    Builds a new top-oriented axis generator for the given scale,
    with empty tick arguments, a tick size of 6 and padding of 3.
    In this orientation, ticks are drawn above the horizontal domain path.

    Parameters
    ----------
    scale : Type[Transformer | Sequential | Diverging]
        Scaler

    Returns
    -------
    Axis
        Axis
    """
    return Axis(TOP, scale)


def axis_right(scale: Type[Transformer | Sequential | Diverging]) -> Axis:
    """
    Builds a new right-oriented axis generator for the given scale,
    with empty tick arguments, a tick size of 6 and padding of 3.
    In this orientation, ticks are drawn above the vertical domain path.

    Parameters
    ----------
    scale : Type[Transformer | Sequential | Diverging]
        Scaler

    Returns
    -------
    Axis
        Axis
    """
    return Axis(RIGHT, scale)


def axis_bottom(scale: Type[Transformer | Sequential | Diverging]) -> Axis:
    """
    Builds a new bottom-oriented axis generator for the given scale,
    with empty tick arguments, a tick size of 6 and padding of 3.
    In this orientation, ticks are drawn above the horizontal domain path.

    Parameters
    ----------
    scale : Type[Transformer | Sequential | Diverging]
        Scaler

    Returns
    -------
    Axis
        Axis
    """
    return Axis(BOTTOM, scale)


def axis_left(scale: Type[Transformer | Sequential | Diverging]) -> Axis:
    """
    Builds a new left-oriented axis generator for the given scale,
    with empty tick arguments, a tick size of 6 and padding of 3.
    In this orientation, ticks are drawn above the vertical domain path.

    Parameters
    ----------
    scale : Type[Transformer | Sequential | Diverging]
        Scaler

    Returns
    -------
    Axis
        Axis
    """
    return Axis(LEFT, scale)
