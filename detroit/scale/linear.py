from ..array import ticks, tick_increment
from .continuous import continuous, copy
from .init import init_range
from ..tickFormat import tick_format

def linearish(scale):
    domain = scale.domain

    def ticks_func(count=None):
        d = domain()
        return ticks(d[0], d[-1], count if count is not None else 10)

    def tick_format_func(count=None, specifier=None):
        d = domain()
        return tick_format(d[0], d[-1], count if count is not None else 10, specifier)

    def nice_func(count=None):
        if count is None:
            count = 10

        d = domain()
        i0 = 0
        i1 = len(d) - 1
        start = d[i0]
        stop = d[i1]
        prestep = None
        step = None
        max_iter = 10

        if stop < start:
            step = start
            start = stop
            stop = step
            step = i0
            i0 = i1
            i1 = step

        while max_iter > 0:
            step = tick_increment(start, stop, count)
            if step == prestep:
                d[i0] = start
                d[i1] = stop
                return domain(d)
            elif step > 0:
                start = math.floor(start / step) * step
                stop = math.ceil(stop / step) * step
            elif step < 0:
                start = math.ceil(start * step) / step
                stop = math.floor(stop * step) / step
            else:
                break
            prestep = step
            max_iter -= 1

        return scale

    scale.ticks = ticks_func
    scale.tick_format = tick_format_func
    scale.nice = nice_func

    return scale


def linear():
    scale = continuous()

    def copy_func():
        return copy(scale, linear())

    scale.copy = copy_func
    init_range(scale)

    return linearish(scale)


# -----

