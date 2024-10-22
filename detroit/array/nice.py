from .ticks import tick_increment
import math

def nice(start, stop, count):
    prestep = None
    while True:
        step = tick_increment(start, stop, count)
        if step == prestep or step == 0 or not math.isfinite(step):
            return [start, stop]
        elif step > 0:
            start = math.floor(start / step) * step
            stop = math.ceil(stop / step) * step
        elif step < 0:
            start = math.ceil(start * step) / step
            stop = math.floor(stop * step) / step
        prestep = step

