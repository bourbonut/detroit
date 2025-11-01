from __future__ import annotations

from collections.abc import Callable
from typing import Literal

from ..array import argpass
from ..selection.selection import Selection
from ..types import ContinuousScaler, SequentialScaler

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
    offset = max(0, scale.get_bandwidth() - offset * 2) / 2
    if scale.get_round():
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
    scale : ContinuousScaler | SequentialScaler
        Scaler
    """

    def __init__(
        self,
        orient: Literal[1, 2, 3, 4],
        scale: ContinuousScaler | SequentialScaler,
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

        >>> import detroit as d3
        >>> svg = d3.create("svg")
        >>> svg.call(d3.axis_bottom(d3.scale_linear()))
        Selection(
            groups=[[svg]],
            parents=[svg],
        )
        >>> print(svg.to_string())
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" font-size="10" font-family="sans-serif" text-anchor="middle">
          <path class="domain" stroke="currentColor" d="M0.5,6V0.5H1.5V6"/>
          <g class="tick" opacity="1" transform="translate(0.5, 0)">
            <line stroke="currentColor" y2="6"/>
            <text fill="currentColor" y="9" dy="0.71em">0.0</text>
          </g>
          <g class="tick" opacity="1" transform="translate(0.6, 0)">
            <line stroke="currentColor" y2="6"/>
            <text fill="currentColor" y="9" dy="0.71em">0.1</text>
          </g>
          <g class="tick" opacity="1" transform="translate(0.7, 0)">
            <line stroke="currentColor" y2="6"/>
            <text fill="currentColor" y="9" dy="0.71em">0.2</text>
          </g>
          <g class="tick" opacity="1" transform="translate(0.8, 0)">
            <line stroke="currentColor" y2="6"/>
            <text fill="currentColor" y="9" dy="0.71em">0.3</text>
          </g>
          <g class="tick" opacity="1" transform="translate(0.9, 0)">
            <line stroke="currentColor" y2="6"/>
            <text fill="currentColor" y="9" dy="0.71em">0.4</text>
          </g>
          <g class="tick" opacity="1" transform="translate(1.0, 0)">
            <line stroke="currentColor" y2="6"/>
            <text fill="currentColor" y="9" dy="0.71em">0.5</text>
          </g>
          <g class="tick" opacity="1" transform="translate(1.1, 0)">
            <line stroke="currentColor" y2="6"/>
            <text fill="currentColor" y="9" dy="0.71em">0.6</text>
          </g>
          <g class="tick" opacity="1" transform="translate(1.2, 0)">
            <line stroke="currentColor" y2="6"/>
            <text fill="currentColor" y="9" dy="0.71em">0.7</text>
          </g>
          <g class="tick" opacity="1" transform="translate(1.3, 0)">
            <line stroke="currentColor" y2="6"/>
            <text fill="currentColor" y="9" dy="0.71em">0.8</text>
          </g>
          <g class="tick" opacity="1" transform="translate(1.4, 0)">
            <line stroke="currentColor" y2="6"/>
            <text fill="currentColor" y="9" dy="0.71em">0.9</text>
          </g>
          <g class="tick" opacity="1" transform="translate(1.5, 0)">
            <line stroke="currentColor" y2="6"/>
            <text fill="currentColor" y="9" dy="0.71em">1.0</text>
          </g>
        </svg>

        Notes
        -----

        Transitions are not yet implemented
        """
        if self._tick_values is not None:
            values = self._tick_values
        elif hasattr(self._scale, "ticks"):
            values = argpass(self._scale.ticks)(*self._tick_arguments)
        else:
            values = self._scale.get_domain()

        if self._tick_format is not None:
            format_func = self._tick_format
        elif hasattr(self._scale, "tick_format"):
            format_func = argpass(self._scale.tick_format)(*self._tick_arguments)
        else:

            def format_func(d):
                return d

        spacing = max(self._tick_size_inner, 0) + self._tick_padding
        range_values = self._scale.get_range()
        range0 = float(range_values[0]) + self._offset
        range1 = float(range_values[-1]) + self._offset

        if hasattr(self._scale, "get_bandwidth"):
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

    def set_scale(self, scale: ContinuousScaler | SequentialScaler) -> Axis:
        """
        Sets scale value

        Parameters
        ----------
        scale : ContinuousScaler | SequentialScaler
            New scale

        Returns
        -------
        Axis
            Itself

        Examples
        --------

        >>> scale = d3.scale_band()
        >>> x = d3.axis_bottom(d3.scale_linear())
        >>> print(x)
        Axis[BOTTOM](
            scale=ScaleLinear(domain=[0, 1], range=[0, 1]),
            tick_arguments=[],
            tick_values=None,
            tick_size_inner=6,
            tick_size_outer=6,
            tick_padding=3,
            offset=0.5,
        )
        >>> x.set_scale(scale)
        <Axis[BOTTOM] at 0x7fb4e098e9b0>
        >>> print(x)
        Axis[BOTTOM](
            scale=ScaleBand(domain=[], range=[0, 1], padding_inner=0, padding_outer=0),
            tick_arguments=[],
            tick_values=None,
            tick_size_inner=6,
            tick_size_outer=6,
            tick_padding=3,
            offset=0.5,
        )
        """
        self._scale = scale
        return self

    def set_ticks(self, *ticks: int | str) -> Axis:
        """
        Tick values will be passed to :code:`scale.ticks` and
        :code:`scale.tick_format` when :code:`Axis.__call__` is called

        Parameters
        ----------
        *ticks : int | str
            It depends on :code:`scale` type. Most of the time, it is the
            *count* for the number of ticks and optional format specifier

        Returns
        -------
        Axis
            Itself

        Examples
        --------

        To generate three ticks with percentage formatting on a linear scale :

        >>> width = 810
        >>> height = 30
        >>> margin = 15
        >>> svg = (
        ...     d3.create("svg")
        ...     .attr("width", width)
        ...     .attr("height", height)
        ...     .attr("viewBox", f"0 0 {width} {height}")
        ... )
        >>> axis = d3.axis_bottom(d3.scale_linear().set_range([0, width - 2 * margin]))
        >>> svg.append("g").attr("transform", f"translate({margin}, {margin * 0.5})").call(
        ...     axis.set_ticks(3, "%")
        ... )
        Selection(
            groups=[[g]],
            parents=[svg],
        )

        **Result**

        .. image:: ../figures/light_axis_ticks_1.svg
           :align: center
           :class: only-light

        .. image:: ../figures/dark_axis_ticks_1.svg
           :align: center
           :class: only-dark

        ------------

        To generate ticks every fifteen minutes with a time scale :

        >>> from datetime import datetime
        >>> width = 810
        >>> height = 30
        >>> margin = 15
        >>> svg = (
        ...     d3.create("svg")
        ...     .attr("width", width)
        ...     .attr("height", height)
        ...     .attr("viewBox", f"0 0 {width} {height}")
        ... )
        >>> scale = d3.scale_time(
        ...     [datetime(2000, 1, 1, 12, 0), datetime(2000, 1, 1, 13, 0)], [0, 1]
        ... )
        >>> axis = d3.axis_bottom(scale.set_range([0, width - 2 * margin]))
        >>> svg.append("g").attr("transform", f"translate({margin}, {margin * 0.5})").call(
        ...     axis.set_ticks(d3.time_minute.every(15))
        ... )
        Selection(
            groups=[[g]],
            parents=[svg],
        )

        **Result**

        .. image:: ../figures/light_axis_ticks_2.svg
           :align: center
           :class: only-light

        .. image:: ../figures/dark_axis_ticks_2.svg
           :align: center
           :class: only-dark

        ------------

        Note the similarities with :code:`set_tick_arguments`:

        >>> axis.set_ticks(10) # same as axis.set_tick_arguments([10])
        """
        self._tick_arguments = list(ticks)
        return self

    def set_tick_arguments(self, tick_arguments: list[int | str]) -> Axis:
        """
        Tick arguments will be passed to :code:`scale.ticks` and
        :code:`scale.tick_format` when :code:`Axis.__call__` is called

        Parameters
        ----------
        tick_arguments : list[int | str]
            It depends on :code:`scale` type. Most of the time, it is the
            *count* for the number of ticks and optional format specifier

        Returns
        -------
            Itself

        Examples
        --------

        To generate three ticks with percentage formatting on a linear scale :

        >>> # same as axis.set_ticks(3, "%")
        >>> axis.set_tick_arguments([3, "%"])

        To generate ticks every fifteen minutes with a time scale :

        >>> # same as axis.set_ticks(d3.time_minute.every(15))
        >>> axis.set_tick_arguments([d3.time_minute.every(15)])

        Notes
        -----

        Check :code:`Axis.set_ticks` for more details in examples
        """
        self._tick_arguments = list(tick_arguments)
        return self

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

        >>> width = 810
        >>> height = 30
        >>> margin = 15
        >>> svg = (
        ...     d3.create("svg")
        ...     .attr("width", width)
        ...     .attr("height", height)
        ...     .attr("viewBox", f"0 0 {width} {height}")
        ... )
        >>> axis = d3.axis_bottom(
        ...     d3.scale_linear().set_domain([0, 360]).set_range([0, width - 2 * margin])
        ... )
        >>> (
        ...     svg.append("g")
        ...     .attr("transform", f"translate({margin}, {margin * 0.5})")
        ...     .call(axis.set_tick_values([0, 120, 240, 360]))
        ... )
        Selection(
            groups=[[g]],
            parents=[svg],
        )

        **Result**

        .. image:: ../figures/light_axis_angle.svg
           :align: center
           :class: only-light

        .. image:: ../figures/dark_axis_angle.svg
           :align: center
           :class: only-dark
        """
        self._tick_values = tick_values
        return self

    def set_tick_format(self, tick_format: Callable[[int | float], str]) -> Axis:
        """
        Sets the tick format function and returns the axis.

        Parameters
        ----------
        tick_format : Callable[[int | float], str]
            Tick formatter

        Returns
        -------
        Axis
            Itself

        Examples
        --------

        For example, to display integers as decimal notation rounded to
        significant digits:

        >>> width = 810
        >>> height = 30
        >>> margin = 15
        >>> svg = (
        ...     d3.create("svg")
        ...     .attr("width", width)
        ...     .attr("height", height)
        ...     .attr("viewBox", f"0 0 {width} {height}")
        ... )
        >>> axis = d3.axis_bottom(
        ...     d3.scale_linear().set_domain([0, 10_000]).set_range([0, width - 2 * margin])
        ... )
        >>> (
        ...     svg.append("g")
        ...     .attr("transform", f"translate({margin}, {margin * 0.5})")
        ...     .call(axis.set_tick_format(d3.format("~s")))
        ... )
        Selection(
            groups=[[g]],
            parents=[svg],
        )

        **Result**

        .. image:: ../figures/light_axis_format.svg
           :align: center
           :class: only-light

        .. image:: ../figures/dark_axis_format.svg
           :align: center
           :class: only-dark
        """
        self._tick_format = tick_format
        return self

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

        >>> width = 810
        >>> height = 30
        >>> margin = 15
        >>> svg = (
        ...     d3.create("svg")
        ...     .attr("width", width)
        ...     .attr("height", height)
        ...     .attr("viewBox", f"0 0 {width} {height}")
        ... )
        >>> axis = d3.axis_bottom(d3.scale_linear().set_range([0, width - 2 * margin]))
        >>> (
        ...     svg.append("g")
        ...     .attr("transform", f"translate({margin}, {margin * 0.5})")
        ...     .call(axis.set_tick_size(12))
        ... )
        Selection(
            groups=[[g]],
            parents=[svg],
        )

        **Result**

        .. image:: ../figures/light_axis_tick_size.svg
           :align: center
           :class: only-light

        .. image:: ../figures/dark_axis_tick_size.svg
           :align: center
           :class: only-dark
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

        >>> width = 810
        >>> height = 30
        >>> margin = 15
        >>> svg = (
        ...     d3.create("svg")
        ...     .attr("width", width)
        ...     .attr("height", height)
        ...     .attr("viewBox", f"0 0 {width} {height}")
        ... )
        >>> axis = d3.axis_bottom(d3.scale_linear().set_range([0, width - 2 * margin]))
        >>> (
        ...     svg.append("g")
        ...     .attr("transform", f"translate({margin}, {margin * 0.5})")
        ...     .call(axis.set_tick_size_inner(0))
        ... )
        Selection(
            groups=[[g]],
            parents=[svg],
        )

        **Result**

        .. image:: ../figures/light_axis_tick_size_inner.svg
           :align: center
           :class: only-light

        .. image:: ../figures/dark_axis_tick_size_inner.svg
           :align: center
           :class: only-dark

        Notes
        -----

        Inner ticks are all ticks with an associated value.
        """
        self._tick_size_inner = tick_size_inner
        return self

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

        >>> width = 810
        >>> height = 30
        >>> margin = 15
        >>> svg = (
        ...     d3.create("svg")
        ...     .attr("width", width)
        ...     .attr("height", height)
        ...     .attr("viewBox", f"0 0 {width} {height}")
        ... )
        >>> axis = d3.axis_bottom(d3.scale_linear().set_range([0, width - 2 * margin]))
        >>> (
        ...     svg.append("g")
        ...     .attr("transform", f"translate({margin}, {margin * 0.5})")
        ...     .call(axis.set_tick_size_outer(12))
        ... )
        Selection(
            groups=[[g]],
            parents=[svg],
        )

        **Result**

        .. image:: ../figures/light_axis_tick_size_outer.svg
           :align: center
           :class: only-light

        .. image:: ../figures/dark_axis_tick_size_outer.svg
           :align: center
           :class: only-dark

        Notes
        -----

        Outer ticks are only ticks on extremities of the axis.
        """
        self._tick_size_outer = tick_size_outer
        return self

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

        >>> width = 810
        >>> height = 30
        >>> margin = 15
        >>> svg = (
        ...     d3.create("svg")
        ...     .attr("width", width)
        ...     .attr("height", height)
        ...     .attr("viewBox", f"0 0 {width} {height}")
        ... )
        >>> axis = d3.axis_bottom(d3.scale_linear().set_range([0, width - 2 * margin]))
        >>> (
        ...     svg.append("g")
        ...     .attr("transform", f"translate({margin}, {margin * 0.5})")
        ...     .call(axis.set_tick_padding(8))
        ... )
        Selection(
            groups=[[g]],
            parents=[svg],
        )

        **Result**

        .. image:: ../figures/light_axis_tick_padding.svg
           :align: center
           :class: only-light

        .. image:: ../figures/dark_axis_tick_padding.svg
           :align: center
           :class: only-dark

        Notes
        -----

        The value :code:`y` is computing as :code:`max(self._tick_size_inner,
        0) + self._tick_padding`.
        """
        self._tick_padding = tick_padding
        return self

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

        >>> width = 810
        >>> height = 30
        >>> margin = 15
        >>> svg = (
        ...     d3.create("svg")
        ...     .attr("width", width)
        ...     .attr("height", height)
        ...     .attr("viewBox", f"0 0 {width} {height}")
        ... )
        >>> axis = d3.axis_bottom(d3.scale_linear().set_range([0, width - 2 * margin]))
        >>> (
        ...     svg.append("g")
        ...     .attr("transform", f"translate({margin}, {margin * 0.5})")
        ...     .call(axis.set_offset(8))
        ... )
        Selection(
            groups=[[g]],
            parents=[svg],
        )

        **Result**

        .. image:: ../figures/light_axis_offset.svg
           :align: center
           :class: only-light

        .. image:: ../figures/dark_axis_offset.svg
           :align: center
           :class: only-dark
        """
        self._offset = offset
        return self

    def get_scale(self) -> ContinuousScaler | SequentialScaler:
        return self._scale

    def get_tick_arguments(self) -> list[int | str]:
        return self._tick_arguments.copy()

    def get_tick_values(self) -> list[int | float]:
        return self._tick_values

    def get_tick_format(self) -> Callable[[int | float], str]:
        return self._tick_format

    def get_tick_size_inner(self) -> float:
        return self._tick_size_inner

    def get_tick_size_outer(self) -> float:
        return self._tick_size_outer

    def get_tick_padding(self) -> float:
        return self._tick_padding

    def get_offset(self) -> float:
        return self._offset

    def __str__(self) -> str:
        orients = ["TOP", "RIGHT", "BOTTOM", "LEFT"]
        name = f"Axis[{orients[self._orient - 1]}]"
        scale = str(self.get_scale()).split("\n")
        scale = "\n    ".join(scale)
        attrbs = [
            "tick_arguments",
            "tick_values",
            "tick_size_inner",
            "tick_size_outer",
            "tick_padding",
            "offset",
        ]
        attrbs = (f"{a}={getattr(self, f'get_{a}')()}," for a in attrbs)
        attrbs = "\n    ".join(attrbs)
        return f"{name}(\n    scale={scale},\n    {attrbs}\n)"

    def __repr__(self) -> str:
        orients = ["TOP", "RIGHT", "BOTTOM", "LEFT"]
        name = f"Axis[{orients[self._orient - 1]}]"
        addr = id(self)
        return f"<{name} at {hex(addr)}>"


def axis_top(scale: ContinuousScaler | SequentialScaler) -> Axis:
    """
    Builds a new top-oriented axis generator for the given scale,
    with empty tick arguments, a tick size of 6 and padding of 3.
    In this orientation, ticks are drawn above the horizontal domain path.

    Parameters
    ----------
    scale : ContinuousScaler | SequentialScaler
        Scaler

    Returns
    -------
    Axis
        Axis
    """
    return Axis(TOP, scale)


def axis_right(scale: ContinuousScaler | SequentialScaler) -> Axis:
    """
    Builds a new right-oriented axis generator for the given scale,
    with empty tick arguments, a tick size of 6 and padding of 3.
    In this orientation, ticks are drawn above the vertical domain path.

    Parameters
    ----------
    scale : ContinuousScaler | SequentialScaler
        Scaler

    Returns
    -------
    Axis
        Axis
    """
    return Axis(RIGHT, scale)


def axis_bottom(scale: ContinuousScaler | SequentialScaler) -> Axis:
    """
    Builds a new bottom-oriented axis generator for the given scale,
    with empty tick arguments, a tick size of 6 and padding of 3.
    In this orientation, ticks are drawn above the horizontal domain path.

    Parameters
    ----------
    scale : ContinuousScaler | SequentialScaler
        Scaler

    Returns
    -------
    Axis
        Axis
    """
    return Axis(BOTTOM, scale)


def axis_left(scale: ContinuousScaler | SequentialScaler) -> Axis:
    """
    Builds a new left-oriented axis generator for the given scale,
    with empty tick arguments, a tick size of 6 and padding of 3.
    In this orientation, ticks are drawn above the vertical domain path.

    Parameters
    ----------
    scale : ContinuousScaler | SequentialScaler
        Scaler

    Returns
    -------
    Axis
        Axis
    """
    return Axis(LEFT, scale)
