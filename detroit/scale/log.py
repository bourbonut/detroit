from ..array import ticks
from ..format import format, format_specifier
from .nice import nice
from .continuous import copy, transformer
from .init import init_range
import math

def transform_log(x):
    return math.log(x)

def transform_exp(x):
    return math.exp(x)

def transform_logn(x):
    return -math.log(-x)

def transform_expn(x):
    return -math.exp(-x)

def pow10(x):
    return float("1e" + str(x)) if math.isfinite(x) else 0 if x < 0 else x

def powp(base):
    if base == 10:
        return pow10
    elif base == math.e:
        return math.exp
    else:
        return lambda x: math.pow(base, x)

def logp(base):
    if base == math.e:
        return math.log
    elif base == 10 and hasattr(math, 'log10'):
        return math.log10
    elif base == 2 and hasattr(math, 'log2'):
        return math.log2
    else:
        base = math.log(base)
        return lambda x: math.log(x) / base

def reflect(f):
    return lambda x, k: -f(-x, k)

def loggish(transform):
    scale = transform(transform_log, transform_exp)
    domain = scale.domain
    base = 10
    logs = None
    pows = None

    def rescale():
        nonlocal logs, pows
        logs = logp(base)
        pows = powp(base)
        if domain()[0] < 0:
            logs = reflect(logs)
            pows = reflect(pows)
            transform(transform_logn, transform_expn)
        else:
            transform(transform_log, transform_exp)
        return scale

    def base_func(_=None):
        nonlocal base
        if _ is not None:
            base = float(_)
            return rescale()
        return base

    def domain_func(_=None):
        if _ is not None:
            domain(_)
            return rescale()
        return domain()

    def ticks_func(count):
        d = domain()
        u = d[0]
        v = d[-1]
        r = v < u

        if r:
            u, v = v, u

        i = logs(u)
        j = logs(v)
        k = None
        t = None
        n = count if count is not None else 10
        z = []

        if not (base % 1) and j - i < n:
            i = math.floor(i)
            j = math.ceil(j)
            if u > 0:
                for i in range(i, j + 1):
                    for k in range(1, base):
                        t = k / pows(-i) if i < 0 else k * pows(i)
                        if t < u:
                            continue
                        if t > v:
                            break
                        z.append(t)
            else:
                for i in range(i, j + 1):
                    for k in range(base - 1, 0, -1):
                        t = k / pows(-i) if i > 0 else k * pows(i)
                        if t < u:
                            continue
                        if t > v:
                            break
                        z.append(t)
            if len(z) * 2 < n:
                z = ticks(u, v, n)
        else:
            z = ticks(i, j, min(j - i, n)).map(pows)
        return z[::-1] if r else z

    def tick_format(count=None, specifier=None):
        if count is None:
            count = 10
        if specifier is None:
            specifier = "s" if base == 10 else ","
        if not callable(specifier):
            if not (base % 1) and (specifier := format_specifier(specifier)).precision is None:
                specifier.trim = True
            specifier = format(specifier)
        if count == float('inf'):
            return specifier
        k = max(1, base * count / len(scale.ticks()))
        return lambda d: (specifier(d) if (i := d / pows(round(logs(d)))) * base < base - 0.5 else "") if i <= k else ""

    def nice_func():
        return domain(nice(domain(), {
            'floor': lambda x: pows(math.floor(logs(x))),
            'ceil': lambda x: pows(math.ceil(logs(x)))
        }))

    scale.base = base_func
    scale.domain = domain_func
    scale.ticks = ticks_func
    scale.tick_format = tick_format
    scale.nice = nice_func

    return scale


def log():
    scale = loggish(transformer()).domain([1, 10])
    scale.copy = lambda: copy(scale, log()).base(scale.base())
    init_range(scale)
    return scale


# -----

