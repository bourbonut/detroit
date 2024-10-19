import numpy as np

top = 1
right = 2
bottom = 3
left = 4
epsilon = 1e-6

def translate_x(x):
    return f"translate({x},0)"

def translate_y(y):
    return f"translate(0,{y})"

def number(scale):
    return lambda d: float(scale(d))

def center(scale, offset):
    offset = max(0, scale.bandwidth() - offset * 2) / 2
    if scale.round():
        offset = round(offset)
    return lambda d: float(scale(d)) + offset

def entering(context):
    return not hasattr(context, '__axis')

def axis(orient, scale):
    tick_arguments = []
    tick_values = None
    tick_format = None
    tick_size_inner = 6
    tick_size_outer = 6
    tick_padding = 3
    offset = 0 if np.isfinite(1 / 1) else 0.5  # Simulating devicePixelRatio > 1
    k = -1 if orient in [top, left] else 1
    x = 'x' if orient in [left, right] else 'y'
    transform = translate_x if orient in [top, bottom] else translate_y

    def axis_func(context):
        nonlocal tick_values, tick_format, tick_size_inner, tick_size_outer, tick_padding, offset

        values = (tick_values if tick_values is not None else 
                  (scale.ticks(*tick_arguments) if hasattr(scale, 'ticks') else scale.domain()))
        format_func = (tick_format if tick_format is not None else 
                       (scale.tick_format(*tick_arguments) if hasattr(scale, 'tick_format') else lambda d: d))
        spacing = max(tick_size_inner, 0) + tick_padding
        range_ = scale.range()
        range0 = float(range_[0]) + offset
        range1 = float(range_[-1]) + offset
        position = (center(scale.copy(), offset) if hasattr(scale, 'bandwidth') else number(scale.copy()))
        
        # Simulating selection and data binding (context.selection is not a direct equivalent in Python)
        selection = context.selection() if hasattr(context, 'selection') else context
        path = selection.select_all(".domain").data([None])
        tick = selection.select_all(".tick").data(values, scale).order()
        tick_exit = tick.exit()
        tick_enter = tick.enter().append("g").attr("class", "tick")
        line = tick.select("line")
        text = tick.select("text")

        path = path.merge(path.enter().insert("path", ".tick")
                          .attr("class", "domain")
                          .attr("stroke", "currentColor"))

        tick = tick.merge(tick_enter)

        line = line.merge(tick_enter.append("line")
                          .attr("stroke", "currentColor")
                          .attr(f"{x}2", k * tick_size_inner))

        text = text.merge(tick_enter.append("text")
                          .attr("fill", "currentColor")
                          .attr(x, k * spacing)
                          .attr("dy", "0em" if orient == top else "0.71em" if orient == bottom else "0.32em"))

        if context != selection:
            path = path.transition(context)
            tick = tick.transition(context)
            line = line.transition(context)
            text = text.transition(context)

            tick_exit = tick_exit.transition(context)\
                .attr("opacity", epsilon)\
                .attr("transform", lambda d: transform(position(d) + offset) if np.isfinite(d := position(d)) else None)

            tick_enter\
                .attr("opacity", epsilon)\
                .attr("transform", lambda d: transform((p := getattr(this.parentNode, '__axis', None)(d) if p else position(d)) + offset))

        tick_exit.remove()

        path.attr("d", (f"M{(k * tick_size_outer)},{range0}H{offset}V{range1}H{(k * tick_size_outer)}" if tick_size_outer else f"M{offset},{range0}V{range1}"))

        tick.attr("opacity", 1)\
            .attr("transform", lambda d: transform(position(d) + offset))

        line.attr(f"{x}2", k * tick_size_inner)

        text.attr(x, k * spacing)\
            .text(format_func)

        selection.filter(entering(context))\
            .attr("fill", "none")\
            .attr("font-size", 10)\
            .attr("font-family", "sans-serif")\
            .attr("text-anchor", "start" if orient == right else "end" if orient == left else "middle")

        for elem in selection:
            elem.__axis = position

    axis_func.scale = lambda _: (scale := _, axis_func) if _ else scale
    axis_func.ticks = lambda *args: (tick_arguments := list(args), axis_func)
    axis_func.tick_arguments = lambda _: (tick_arguments := [] if _ is None else list(_), axis_func) if _ else tick_arguments.copy()
    axis_func.tick_values = lambda _: (tick_values := None if _ is None else list(_), axis_func) if _ else (tick_values.copy() if tick_values else None)
    axis_func.tick_format = lambda _: (tick_format := _, axis_func) if _ else tick_format
    axis_func.tick_size = lambda _: (tick_size_inner := tick_size_outer := float(_), axis_func) if _ else tick_size_inner
    axis_func.tick_size_inner = lambda _: (tick_size_inner := float(_), axis_func) if _ else tick_size_inner
    axis_func.tick_size_outer = lambda _: (tick_size_outer := float(_), axis_func) if _ else tick_size_outer
    axis_func.tick_padding = lambda _: (tick_padding := float(_), axis_func) if _ else tick_padding
    axis_func.offset = lambda _: (offset := float(_), axis_func) if _ else offset

    return axis_func

def axis_top(scale):
    return axis(top, scale)

def axis_right(scale):
    return axis(right, scale)

def axis_bottom(scale):
    return axis(bottom, scale)

def axis_left(scale):
    return axis(left, scale)

