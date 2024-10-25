from bisect import bisect
from .init import init_range
from .ordinal import ordinal

def band():
    scale = ordinal().unknown(None)
    domain = scale.domain
    ordinal_range = scale.range
    r0 = 0
    r1 = 1
    step = None
    bandwidth = None
    round = False
    padding_inner = 0
    padding_outer = 0
    align = 0.5

    del scale.unknown

    def rescale():
        nonlocal step, bandwidth
        n = len(domain())
        reverse = r1 < r0
        start = r1 if reverse else r0
        stop = r0 if reverse else r1
        step = (stop - start) / max(1, n - padding_inner + padding_outer * 2)
        if round:
            step = int(step)
        start += (stop - start - step * (n - padding_inner)) * align
        bandwidth = step * (1 - padding_inner)
        if round:
            start = round(start)
            bandwidth = round(bandwidth)
        values = [start + step * i for i in range(n)]
        return ordinal_range(values[::-1] if reverse else values)

    def domain_func(_=None):
        if _ is not None:
            domain(_)
            return rescale()
        return domain()

    def range_func(_=None):
        nonlocal r0, r1
        if _ is not None:
            r0, r1 = map(float, _)
            return rescale()
        return [r0, r1]

    def range_round_func(_=None):
        nonlocal r0, r1, round
        r0, r1 = map(float, _)
        round = True
        return rescale()

    def bandwidth_func():
        return bandwidth

    def step_func():
        return step

    def round_func(_=None):
        nonlocal round
        if _ is not None:
            round = bool(_)
            return rescale()
        return round

    def padding_func(_=None):
        nonlocal padding_inner, padding_outer
        if _ is not None:
            padding_inner = min(1, padding_outer := float(_))
            return rescale()
        return padding_inner

    def padding_inner_func(_=None):
        nonlocal padding_inner
        if _ is not None:
            padding_inner = min(1, float(_))
            return rescale()
        return padding_inner

    def padding_outer_func(_=None):
        nonlocal padding_outer
        if _ is not None:
            padding_outer = float(_)
            return rescale()
        return padding_outer

    def align_func(_=None):
        nonlocal align
        if _ is not None:
            align = max(0, min(1, float(_)))
            return rescale()
        return align

    def copy():
        return band().domain(domain()).range([r0, r1]).round(round).padding_inner(padding_inner).padding_outer(padding_outer).align(align)

    scale.domain = domain_func
    scale.range = range_func
    scale.range_round = range_round_func
    scale.bandwidth = bandwidth_func
    scale.step = step_func
    scale.round = round_func
    scale.padding = padding_func
    scale.padding_inner = padding_inner_func
    scale.padding_outer = padding_outer_func
    scale.align = align_func
    scale.copy = copy

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
    return pointish(band().padding_inner(1))


# -----

