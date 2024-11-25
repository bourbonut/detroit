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
    offset = max(0, scale.bandwidth() - offset * 2) / 2
    if scale.round():
        offset = round(offset)
    return lambda d: float(scale(d)) + offset


def entering(context):
    return not hasattr(context, "__axis")


class Axis:
    def __init__(self, orient: int, scale):
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

    def __call__(self, context):
        """
        Render the axis to the given context, which may be either a selection
        of SVG containers (either SVG or G elements) or a corresponding transition.
        """
        if self._tick_values is not None:
            values = self._tick_values
        elif hasattr(self._scale, "ticks"):
            values = self._scale.ticks(*self._tick_arguments)
        else:
            values = self._scale.domain()

        if self._tick_format is not None:
            format_func = self._tick_format
        elif hasattr(self._scale, "tick_format"):
            format_func = self._tick_format
        else:

            def format_func(d):
                return d

        spacing = max(self._tick_size_inner, 0) + self._tick_padding
        range_values = self._scale.range()
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
                path.attr("d", f"M{self._offset},{range0}H{range1}")

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

    def scale(self, scale=None):
        if scale is not None:
            self._scale = scale
            return self
        return self._scale

    def ticks(self, ticks=None):
        if ticks is not None:
            self._tick_arguments = [ticks]
        else:
            self._tick_arguments = []
        return self

    def tick_arguments(self, tick_arguments=None):
        if tick_arguments is not None:
            self._tick_arguments = tick_arguments
            return self
        return self._tick_arguments.copy()

    def tick_values(self, tick_values=None):
        if tick_values is not None:
            self._tick_values = tick_values
            return self
        return self._tick_values

    def tick_format(self, tick_format=None):
        if tick_format is not None:
            self._tick_format = tick_format
            return self
        return self._tick_format

    def tick_size(self, tick_size=None):
        if tick_size is not None:
            self._tick_size_inner = self._tick_size_outer = tick_size
            return self
        return self._tick_size_inner

    def tick_size_inner(self, tick_size_inner=None):
        if tick_size_inner is not None:
            self._tick_size_inner = tick_size_inner
            return self
        return self._tick_size_inner

    def tick_size_outer(self, tick_size_outer=None):
        if tick_size_outer is not None:
            self._tick_size_outer = tick_size_outer
            return self
        return self._tick_size_outer

    def tick_padding(self, tick_padding=None):
        if tick_padding is not None:
            self._tick_padding = tick_padding
            return self
        return self._tick_padding

    def offset(self, offset=None):
        if offset is not None:
            self._offset = offset
            return self
        return self._offset


def axis_top(scale):
    """
    Builds a new top-oriented axis generator for the given scale,
    with empty tick arguments, a tick size of 6 and padding of 3.
    In this orientation, ticks are drawn above the horizontal domain path.
    """
    return Axis(TOP, scale)


def axis_right(scale):
    """
    Builds a new right-oriented axis generator for the given scale,
    with empty tick arguments, a tick size of 6 and padding of 3.
    In this orientation, ticks are drawn above the vertical domain path.
    """
    return Axis(RIGHT, scale)


def axis_bottom(scale):
    """
    Builds a new bottom-oriented axis generator for the given scale,
    with empty tick arguments, a tick size of 6 and padding of 3.
    In this orientation, ticks are drawn above the horizontal domain path.
    """
    return Axis(BOTTOM, scale)


def axis_left(scale):
    """
    Builds a new left-oriented axis generator for the given scale,
    with empty tick arguments, a tick size of 6 and padding of 3.
    In this orientation, ticks are drawn above the vertical domain path.
    """
    return Axis(LEFT, scale)
