from ..array import ticks, tick_increment
from .continuous import copy, Transformer
from .init import init_range
# from .tick_format import tick_format
import math


class LinearBase:

    def ticks(self, count=None):
        d = self.domain()
        return ticks(d[0], d[-1], count if count is not None else 10)

    def tick_format(self, count=None, specifier=None):
        raise NotImplementedError()
        # d = self.domain()
        # return tick_format(d[0], d[-1], count if count is not None else 10, specifier)

    def nice(self, count=None):
        if count is None:
            count = 10

        d = self.domain()
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
                return self.domain(d)
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

        return self.scale

class ScaleLinear(Transformer, LinearBase):
    def copy(self):
        return copy(self, ScaleLinear())

def scale_linear(*args):
    scale = ScaleLinear()
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)
