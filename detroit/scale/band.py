from .init import init_range
from .ordinal import ScaleOrdinal

class ScaleBand(ScaleOrdinal):
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
        self.rescale()

    def rescale(self):
        n = len(self._domain)
        reverse = self._r1 < self._r0
        start = self._r1 if reverse else self._r0
        stop = self._r0 if reverse else self._r1
        self._step = (stop - start) / max(1, n - self._padding_inner + self._padding_outer * 2)
        if self._round:
            self._step = int(self._step)
        start += (stop - start - self._step * (n - self._padding_inner)) * self._align
        self._bandwidth = self._step * (1 - self._padding_inner)
        if self._round:
            start = round(start)
            self._bandwidth = round(self._bandwidth)
        values = [start + self._step * i for i in range(n)]
        return super().range(values[::-1] if reverse else values)

    def domain(self, *args):
        if args:
            super().domain(*args)
            return self.rescale()
        return self._domain.copy()

    def range(self, *args):
        if args:
            self._r0, self._r1 = map(float, args[0])
            return self.rescale()
        return [self._r0, self._r1]

    def range_round(self, *args):
        self._r0, self._r1 = map(float, args[0])
        self._round = True
        return self.rescale()

    def bandwidth(self):
        return self._bandwidth

    def step(self):
        return self._step

    def round(self, *args):
        if args:
            self._round = bool(args[0])
            return self.rescale()
        return self._round

    def padding(self, *args):
        if args:
            self._padding_outer = float(args[0])
            self._padding_inner = min(1, self._padding_outer)
            return self.rescale()
        return self._padding_inner

    def padding_inner(self, *args):
        if args:
            self._padding_inner = min(1, float(args[0]))
            return self.rescale()
        return self._padding_inner

    def padding_outer(self, *args):
        if args:
            self._padding_outer = float(args[0])
            return self.rescale()
        return self._padding_outer

    def align(self, *args):
        if args:
            self._align = max(0, min(1, float(args[0])))
            return self.rescale()
        return self._align

    def copy(self):
        return ScaleBand().domain(self._domain).range([self._r0, self._r1]).round(self._round).padding_inner(self._padding_inner).padding_outer(self._padding_outer).align(self._align)


def scale_band(*args):
    scale = ScaleBand()
    if len(args) == 1:
        return init_range(scale, range_vals=args[0])
    elif len(args) == 2:
        domain, range_vals = args
        return init_range(scale, domain=domain, range_vals=range_vals)
    return init_range(scale)

def pointish(scale):
    copy = scale.copy

    scale.padding = scale.padding_outer
    del scale.padding_inner
    del scale.padding_outer

    def new_copy():
        return pointish(copy())

    scale.copy = new_copy

    return scale


def point():
    return pointish(ScaleBand().padding_inner(1))
