from .linear import linearish
from .continuous import copy, transformer
from .init import init_range

def transform_symlog(c):
    return lambda x: math.sign(x) * math.log1p(abs(x / c))

def transform_symexp(c):
    return lambda x: math.sign(x) * math.expm1(abs(x)) * c

def symlogish(transform):
    c = 1
    scale = transform(transform_symlog(c), transform_symexp(c))

    def constant_func(_=None):
        nonlocal c
        if _ is not None:
            transform(transform_symlog(c := float(_)), transform_symexp(c))
            return scale
        return c

    scale.constant = constant_func
    return linearish(scale)


def symlog():
    scale = symlogish(transformer())
    scale.copy = lambda: copy(scale, symlog()).constant(scale.constant())
    return init_range(scale)


# -----

