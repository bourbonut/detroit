from .linear import linearish
from .continuous import copy, identity, transformer
from .init import init_range

def transform_pow(exponent):
    return lambda x: (-math.pow(-x, exponent) if x < 0 else math.pow(x, exponent))

def transform_sqrt(x):
    return (-math.sqrt(-x) if x < 0 else math.sqrt(x))

def transform_square(x):
    return (-x * x if x < 0 else x * x)

def powish(transform):
    scale = transform(identity, identity)
    exponent = 1

    def rescale():
        return (exponent == 1 and transform(identity, identity) or 
                exponent == 0.5 and transform(transform_sqrt, transform_square) or 
                transform(transform_pow(exponent), transform_pow(1 / exponent)))

    def exponent_func(_=None):
        nonlocal exponent
        if _ is not None:
            exponent = float(_)
            return rescale()
        return exponent

    scale.exponent = exponent_func
    return linearish(scale)


def pow():
    scale = powish(transformer())
    scale.copy = lambda: copy(scale, pow()).exponent(scale.exponent())
    init_range(scale)
    return scale


def sqrt():
    return pow().exponent(0.5)


# -----

