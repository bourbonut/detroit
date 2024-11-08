import math

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
    return lambda d: float(scale(d))

def center(scale, offset):
    offset = max(0, scale.bandwidth() - offset * 2) / 2
    if scale.round():
        offset = round(offset)
    return lambda d: float(scale(d)) + offset

def entering(context):
    return not hasattr(context, '__axis')

class Axis:

    def __init__(self, orient, scale):
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
        self._x = 'x' if orient in [LEFT, RIGHT] else 'y'
        self._transform = translate_x if orient in [TOP, BOTTOM] else translate_y

    def axis(self, context):
        if self._tick_values is not None:
            values = self._tick_values
        elif hasattr(self._scale, 'ticks'):
            values = self._scale.ticks(*self._tick_arguments) 
        else:
            values = self.scale.domain()

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

        if hasattr(self._scale, 'bandwidth'):
            position = center(self._scale.copy(), self._offset)
        else:
            position = number(self._scale.copy(), self._offset)
        
        selection = context.selection() if hasattr(context, 'selection') else context
        path = selection.select_all(".domain").data([None])
        tick = selection.select_all(".tick").data(values, self._scale).order()
        tick_exit = tick.exit()
        tick_enter = tick.enter().append("g").attr("class", "tick")
        line = tick.select("line")
        text = tick.select("text")

        path = path.merge(
            path.enter().insert("path", ".tick")
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
                      .attr("dy", "0em" if self._orient == TOP else "0.71em" if self._orient == BOTTOM else "0.32em")
        )

        if context != selection:
            path = path.transition(context)
            tick = tick.transition(context)
            line = line.transition(context)
            text = text.transition(context)

            def transform(d):
                d = position(d)
                if d is not None and math.isfinite(d):
                    return self._transform(position(d) + self._offset)

            tick_exit = (
                tick_exit.transition(context)
                         .attr("opacity", EPSILON)
                         .attr("transform", transform)
            )

            def transform(d): # TODO
                return None

            tick_enter.attr("opacity", EPSILON).attr("transform", transform)

        tick_exit.remove()

        if self._tick_size_outer:
            path.attr("d", f"M{(self._k * self._tick_size_outer)},{range0}H{self._offset}V{range1}H{(self._k * self._tick_size_outer)}")
        else:
            path.attr("d", f"M{self._offset},{range0}V{range1}")

        def transform(d):
            return self._transform(self._position(d) + self._offset)

        tick.attr("opacity", 1).attr("transform", transform)

        line.attr(f"{self._x}2", self._k * self._tick_size_inner)

        text.attr(self._x, self._k * spacing).text(format_func)

        (
            selection.filter(entering(context))
                .attr("fill", "none")
                .attr("font-size", 10)
                .attr("font-family", "sans-serif")
                .attr("text-anchor", "start" if self._orient == RIGHT else "end" if self._orient == LEFT else "middle")
        )

def axis_top(scale):
    return Axis(TOP, scale)

def axis_right(scale):
    return Axis(RIGHT, scale)

def axis_bottom(scale):
    return Axis(BOTTOM, scale)

def axis_left(scale):
    return Axis(LEFT, scale)
