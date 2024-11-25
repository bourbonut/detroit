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

    def set_domain(self, domain):
        super().set_domain(domain)
        return self.rescale()

    @property
    def domain(self):
        return self._domain.copy()

    def set_range(self, range_vals):
        self._r0, self._r1 = map(float, range_vals)
        return self.rescale()

    @property
    def range(self):
        return [self._r0, self._r1]

    def set_range_round(self, range_vals):
        self._r0, self._r1 = map(float, range_vals)
        self._round = True
        return self.rescale()

    @property
    def bandwidth(self):
        return self._bandwidth

    @property
    def step(self):
        return self._step

    def set_round(self, round_val):
        self._round = bool(round_val)
        return self.rescale()

    @property
    def round(self):
        return self._round

    def set_padding(self, padding):
        self._padding_outer = float(padding)
        self._padding_inner = min(1, self._padding_outer)
        return self.rescale()

    @property
    def padding(self):
        return self._padding_inner

    def set_padding_inner(self, padding_inner):
        self._padding_inner = min(1, float(padding_inner))
        return self.rescale()

    def set_padding_outer(self, padding_outer):
        self._padding_outer = float(padding_outer)
        return self.rescale()

    @property
    def padding_inner(self):
        return self._padding_inner

    @property
    def padding_outer(self):
        return self._padding_outer

    def set_align(self, align):
        self._align = max(0, min(1, float(align)))
        return self.rescale()

    @property
    def align(self):
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


def scale_point():
    return ScaleBand().set_padding_inner(1)
