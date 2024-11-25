# src/threshold.py
from bisect import bisect
from init import init_range


def threshold():
    domain = [0.5]
    range_vals = [0, 1]
    unknown = None
    n = 1

    def scale(x):
        return (
            range_vals[bisect(domain, x, 0, n)] if x is not None and x <= x else unknown
        )

    def domain_func(_=None):
        nonlocal domain, n
        if _ is not None:
            domain = list(_)
            n = min(len(domain), len(range_vals) - 1)
            return scale
        return domain.copy()

    def range_func(_=None):
        nonlocal range_vals, n
        if _ is not None:
            range_vals = list(_)
            n = min(len(domain), len(range_vals) - 1)
            return scale
        return range_vals.copy()

    def invert_extent(y):
        i = range_vals.index(y)
        return [domain[i - 1], domain[i]]

    def unknown_func(_=None):
        nonlocal unknown
        if _ is not None:
            unknown = _
            return scale
        return unknown

    def copy():
        return threshold().domain(domain).range(range_vals).unknown(unknown)

    scale.domain = domain_func
    scale.range = range_func
    scale.invert_extent = invert_extent
    scale.unknown = unknown_func
    scale.copy = copy

    return init_range(scale)


# -----


# src/colors.py
def colors(s):
    return ["#" + s[i : i + 6] for i in range(0, len(s), 6)]


# -----


# src/band.py
from bisect import bisect
from init import init_range
from ordinal import ordinal
from d3_array import range as sequence


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
        return (
            band()
            .domain(domain())
            .range([r0, r1])
            .round(round)
            .padding_inner(padding_inner)
            .padding_outer(padding_outer)
            .align(align)
        )

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


# src/init.py
def init_range(domain=None, range_vals=None):
    if domain is None and range_vals is None:
        pass
    elif domain is None:
        return range_func(domain)
    else:
        return range_func(range_vals).domain(domain)


def init_interpolator(domain=None, interpolator=None):
    if domain is None and interpolator is None:
        pass
    elif domain is not None:
        if callable(domain):
            this.interpolator(domain)
        else:
            this.range(domain)
    else:
        this.domain(domain)
        if callable(interpolator):
            this.interpolator(interpolator)
        else:
            this.range(interpolator)
    return this


# -----


# src/log.py
from d3_array import ticks
from d3_format import format, format_specifier
from nice import nice
from continuous import copy, transformer
from init import init_range
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
    elif base == 10 and hasattr(math, "log10"):
        return math.log10
    elif base == 2 and hasattr(math, "log2"):
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
            if (
                not (base % 1)
                and (specifier := format_specifier(specifier)).precision is None
            ):
                specifier.trim = True
            specifier = format(specifier)
        if count == float("inf"):
            return specifier
        k = max(1, base * count / len(scale.ticks()))
        return (
            lambda d: (
                specifier(d)
                if (i := d / pows(round(logs(d)))) * base < base - 0.5
                else ""
            )
            if i <= k
            else ""
        )

    def nice_func():
        return domain(
            nice(
                domain(),
                {
                    "floor": lambda x: pows(math.floor(logs(x))),
                    "ceil": lambda x: pows(math.ceil(logs(x))),
                },
            )
        )

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


# src/sequential.py
from d3_interpolate import interpolate, interpolate_round
from continuous import identity
from init import init_interpolator
from linear import linearish
from log import loggish
from symlog import symlogish
from pow import powish


def transformer():
    x0 = 0
    x1 = 1
    t0 = None
    t1 = None
    k10 = None
    transform = None
    interpolator = identity
    clamp = False
    unknown = None

    def scale(x):
        return (
            unknown
            if x is None or (isinstance(x, float) and math.isnan(x))
            else interpolator(
                k10 == 0
                and 0.5
                or (x := (transform(x) - t0) * k10, clamp and max(0, min(1, x)) or x)
            )
        )

    def domain_func(_=None):
        nonlocal x0, x1, t0, t1, k10
        if _ is not None:
            x0, x1 = map(float, _)
            t0 = transform(x0)
            t1 = transform(x1)
            k10 = t0 == t1 and 0 or 1 / (t1 - t0)
            return scale
        return [x0, x1]

    def clamp_func(_=None):
        nonlocal clamp
        if _ is not None:
            clamp = bool(_)
            return scale
        return clamp

    def interpolator_func(_=None):
        nonlocal interpolator
        if _ is not None:
            interpolator = _
            return scale
        return interpolator

    def range(interpolate):
        return (
            lambda _: (r0, r1)
            if _ is None
            else (
                r0 := float(_[0]),
                r1 := float(_[1]),
                interpolator := interpolate(r0, r1),
                scale,
            )
        )

    scale.range = range(interpolate)
    scale.range_round = range(interpolate_round)

    def unknown_func(_=None):
        nonlocal unknown
        if _ is not None:
            unknown = _
            return scale
        return unknown

    return lambda t: (
        transform := t,
        t0 := t(x0),
        t1 := t(x1),
        k10 := t0 == t1 and 0 or 1 / (t1 - t0),
        scale,
    )


def copy(source, target):
    return (
        target.domain(source.domain())
        .interpolator(source.interpolator())
        .clamp(source.clamp())
        .unknown(source.unknown())
    )


def sequential():
    scale = linearish(transformer()(identity))
    scale.copy = lambda: copy(scale, sequential())
    return init_interpolator(scale)


def sequential_log():
    scale = loggish(transformer()).domain([1, 10])
    scale.copy = lambda: copy(scale, sequential_log()).base(scale.base())
    return init_interpolator(scale)


def sequential_symlog():
    scale = symlogish(transformer())
    scale.copy = lambda: copy(scale, sequential_symlog()).constant(scale.constant())
    return init_interpolator(scale)


def sequential_pow():
    scale = powish(transformer())
    scale.copy = lambda: copy(scale, sequential_pow()).exponent(scale.exponent())
    return init_interpolator(scale)


def sequential_sqrt():
    return sequential_pow().exponent(0.5)


# -----


# src/number.py
def number(x):
    return float(x)


# -----


# src/ordinal.py
from d3_array import InternMap
from init import init_range

implicit = object()


def ordinal():
    index = InternMap()
    domain = []
    range_vals = []
    unknown = implicit

    def scale(d):
        i = index.get(d)
        if i is None:
            if unknown != implicit:
                return unknown
            index.set(d, i := len(domain))
            domain.append(d)
        return range_vals[i % len(range_vals)]

    def domain_func(_=None):
        if _ is None:
            return domain.copy()
        domain.clear()
        index.clear()
        for value in _:
            if index.has(value):
                continue
            index.set(value, len(domain))
            domain.append(value)
        return scale

    def range_func(_=None):
        if _ is not None:
            range_vals[:] = list(_)
            return scale
        return range_vals.copy()

    def unknown_func(_=None):
        nonlocal unknown
        if _ is not None:
            unknown = _
            return scale
        return unknown

    def copy():
        return ordinal().domain(domain).range(range_vals).unknown(unknown)

    scale.domain = domain_func
    scale.range = range_func
    scale.unknown = unknown_func
    scale.copy = copy

    init_range(scale)

    return scale


# -----


# src/continuous.py
from bisect import bisect
from d3_interpolate import (
    interpolate as interpolate_value,
    interpolate_number,
    interpolate_round,
)
from constant import constant
from number import number

unit = [0, 1]


def identity(x):
    return x


def normalize(a, b):
    return (
        (b := (b - (a := float(a))))
        and (lambda x: (x - a) / b)
        or constant(float("nan") if math.isnan(b) else 0.5)
    )


def clamper(a, b):
    if a > b:
        a, b = b, a
    return lambda x: max(a, min(b, x))


def bimap(domain, range_vals, interpolate):
    d0, d1 = domain[0], domain[1]
    r0, r1 = range_vals[0], range_vals[1]
    if d1 < d0:
        d0 = normalize(d1, d0)
        r0 = interpolate(r1, r0)
    else:
        d0 = normalize(d0, d1)
        r0 = interpolate(r0, r1)
    return lambda x: r0(d0(x))


def polymap(domain, range_vals, interpolate):
    j = min(len(domain), len(range_vals)) - 1
    d = [None] * j
    r = [None] * j

    if domain[j] < domain[0]:
        domain = domain[::-1]
        range_vals = range_vals[::-1]

    for i in range(j):
        d[i] = normalize(domain[i], domain[i + 1])
        r[i] = interpolate(range_vals[i], range_vals[i + 1])

    return lambda x: r[bisect(domain, x, 1, j) - 1](d[bisect(domain, x, 1, j) - 1](x))


def copy(source, target):
    return (
        target.domain(source.domain())
        .range(source.range())
        .interpolate(source.interpolate())
        .clamp(source.clamp())
        .unknown(source.unknown())
    )


def transformer():
    domain = unit
    range_vals = unit
    interpolate = interpolate_value
    transform = None
    untransform = None
    unknown = None
    clamp = identity
    piecewise = None
    output = None
    input = None

    def rescale():
        n = min(len(domain), len(range_vals))
        if clamp != identity:
            clamp = clamper(domain[0], domain[n - 1])
        piecewise = n > 2 and polymap or bimap
        output = input = None
        return scale

    def scale(x):
        return (
            unknown
            if x is None or (isinstance(x, float) and math.isnan(x))
            else (
                output
                or (
                    output := piecewise(
                        list(map(transform, domain)), range_vals, interpolate
                    )
                )
            )(transform(clamp(x)))
        )

    def invert(y):
        return clamp(
            untransform(
                (
                    input
                    or (
                        input := piecewise(
                            range_vals, list(map(transform, domain)), interpolate_number
                        )
                    )
                )(y)
            )
        )

    def domain_func(_=None):
        if _ is not None:
            domain[:] = list(map(float, _))
            return rescale()
        return domain.copy()

    def range_func(_=None):
        if _ is not None:
            range_vals[:] = list(map(float, _))
            return rescale()
        return range_vals.copy()

    def range_round_func(_=None):
        range_vals[:] = list(map(float, _))
        interpolate = interpolate_round
        return rescale()

    def clamp_func(_=None):
        nonlocal clamp
        if _ is not None:
            clamp = _ and True or identity
            return rescale()
        return clamp != identity

    def interpolate_func(_=None):
        nonlocal interpolate
        if _ is not None:
            interpolate = _
            return rescale()
        return interpolate

    def unknown_func(_=None):
        nonlocal unknown
        if _ is not None:
            unknown = _
            return scale
        return unknown

    return lambda t, u: (transform := t, untransform := u, rescale())


def continuous():
    return transformer()(identity, identity)


# -----


# src/diverging.py
from d3_interpolate import interpolate, interpolate_round, piecewise
from continuous import identity
from init import init_interpolator
from linear import linearish
from log import loggish
from sequential import copy
from symlog import symlogish
from pow import powish


def transformer():
    x0 = 0
    x1 = 0.5
    x2 = 1
    s = 1
    t0 = None
    t1 = None
    t2 = None
    k10 = None
    k21 = None
    interpolator = identity
    transform = None
    clamp = False
    unknown = None

    def scale(x):
        return (
            unknown
            if (isinstance(x, float) and math.isnan(x))
            else (
                x := 0.5
                + ((x := float(transform(x))) - t1) * (s * x < s * t1 and k10 or k21),
                interpolator(clamp and max(0, min(1, x)) or x),
            )
        )

    def domain_func(_=None):
        nonlocal x0, x1, x2, t0, t1, t2, k10, k21, s
        if _ is not None:
            x0, x1, x2 = map(float, _)
            t0 = transform(x0)
            t1 = transform(x1)
            t2 = transform(x2)
            k10 = t0 == t1 and 0 or 0.5 / (t1 - t0)
            k21 = t1 == t2 and 0 or 0.5 / (t2 - t1)
            s = t1 < t0 and -1 or 1
            return scale
        return [x0, x1, x2]

    def clamp_func(_=None):
        nonlocal clamp
        if _ is not None:
            clamp = bool(_)
            return scale
        return clamp

    def interpolator_func(_=None):
        nonlocal interpolator
        if _ is not None:
            interpolator = _
            return scale
        return interpolator

    def range(interpolate):
        return (
            lambda _: (r0, r1, r2)
            if _ is None
            else (
                r0 := float(_[0]),
                r1 := float(_[1]),
                r2 := float(_[2]),
                interpolator := piecewise(interpolate, [r0, r1, r2]),
                scale,
            )
        )

    scale.range = range(interpolate)
    scale.range_round = range(interpolate_round)

    def unknown_func(_=None):
        nonlocal unknown
        if _ is not None:
            unknown = _
            return scale
        return unknown

    return lambda t: (
        transform := t,
        t0 := t(x0),
        t1 := t(x1),
        t2 := t(x2),
        k10 := t0 == t1 and 0 or 0.5 / (t1 - t0),
        k21 := t1 == t2 and 0 or 0.5 / (t2 - t1),
        s := t1 < t0 and -1 or 1,
        scale,
    )


def diverging():
    scale = linearish(transformer()(identity))
    scale.copy = lambda: copy(scale, diverging())
    return init_interpolator(scale)


def diverging_log():
    scale = loggish(transformer()).domain([0.1, 1, 10])
    scale.copy = lambda: copy(scale, diverging_log()).base(scale.base())
    return init_interpolator(scale)


def diverging_symlog():
    scale = symlogish(transformer())
    scale.copy = lambda: copy(scale, diverging_symlog()).constant(scale.constant())
    return init_interpolator(scale)


def diverging_pow():
    scale = powish(transformer())
    scale.copy = lambda: copy(scale, diverging_pow()).exponent(scale.exponent())
    return init_interpolator(scale)


def diverging_sqrt():
    return diverging_pow().exponent(0.5)


# -----


# src/utcTime.py
from d3_time import (
    utcYear,
    utcMonth,
    utcWeek,
    utcDay,
    utcHour,
    utcMinute,
    utcSecond,
    utcTicks,
    utcTickInterval,
)
from d3_time_format import utcFormat
from time import calendar
from init import init_range


def utc_time():
    return init_range(
        calendar(
            utcTicks,
            utcTickInterval,
            utcYear,
            utcMonth,
            utcWeek,
            utcDay,
            utcHour,
            utcMinute,
            utcSecond,
            utcFormat,
        ).domain([datetime.datetime(2000, 1, 1), datetime.datetime(2000, 1, 2)])
    )


# -----


# src/nice.py
def nice(domain, interval):
    domain = domain.copy()

    i0 = 0
    i1 = len(domain) - 1
    x0 = domain[i0]
    x1 = domain[i1]
    t = None

    if x1 < x0:
        t = i0
        i0 = i1
        i1 = t
        t = x0
        x0 = x1
        x1 = t

    domain[i0] = interval.floor(x0)
    domain[i1] = interval.ceil(x1)
    return domain


# -----


# src/pow.py
from linear import linearish
from continuous import copy, identity, transformer
from init import init_range


def transform_pow(exponent):
    return lambda x: (-math.pow(-x, exponent) if x < 0 else math.pow(x, exponent))


def transform_sqrt(x):
    return -math.sqrt(-x) if x < 0 else math.sqrt(x)


def transform_square(x):
    return -x * x if x < 0 else x * x


def powish(transform):
    scale = transform(identity, identity)
    exponent = 1

    def rescale():
        return (
            exponent == 1
            and transform(identity, identity)
            or exponent == 0.5
            and transform(transform_sqrt, transform_square)
            or transform(transform_pow(exponent), transform_pow(1 / exponent))
        )

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


# src/sequentialQuantile.py
from d3_array import ascending, bisect, quantile
from continuous import identity
from init import init_interpolator


def sequential_quantile():
    domain = []
    interpolator = identity

    def scale(x):
        return (
            interpolator((bisect(domain, x, 1) - 1) / (len(domain) - 1))
            if x is not None and not (isinstance(x, float) and math.isnan(x))
            else None
        )

    def domain_func(_=None):
        if _ is None:
            return domain.copy()
        domain.clear()
        for d in _:
            if d is not None and not (isinstance(d, float) and math.isnan(d)):
                domain.append(d)
        domain.sort(ascending)
        return scale

    def interpolator_func(_=None):
        if _ is not None:
            interpolator = _
            return scale
        return interpolator

    def range_func():
        return [interpolator(i / (len(domain) - 1)) for i in range(len(domain))]

    def quantiles_func(n):
        return [quantile(domain, i / n) for i in range(n + 1)]

    def copy():
        return sequential_quantile().domain(domain)

    scale.domain = domain_func
    scale.interpolator = interpolator_func
    scale.range = range_func
    scale.quantiles = quantiles_func
    scale.copy = copy

    return init_interpolator(scale)


# -----


# src/symlog.py
from linear import linearish
from continuous import copy, transformer
from init import init_range


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


# src/radial.py
from continuous import continuous
from init import init_range
from linear import linearish
from number import number


def square(x):
    return math.sign(x) * x * x


def unsquare(x):
    return math.sign(x) * math.sqrt(abs(x))


def radial():
    squared = continuous()
    range_vals = [0, 1]
    round = False
    unknown = None

    def scale(x):
        y = unsquare(squared(x))
        return (
            unknown
            if (isinstance(y, float) and math.isnan(y))
            else (round and round(y) or y)
        )

    def invert(y):
        return squared.invert(square(y))

    def domain_func(_=None):
        if _ is not None:
            squared.domain(_)
            return scale
        return squared.domain()

    def range_func(_=None):
        if _ is not None:
            squared.range([float(x) for x in _])
            return scale
        return range_vals.copy()

    def range_round_func(_=None):
        return scale.range(_).round(True)

    def round_func(_=None):
        nonlocal round
        if _ is not None:
            round = bool(_)
            return scale
        return round

    def clamp_func(_=None):
        if _ is not None:
            squared.clamp(_)
            return scale
        return squared.clamp()

    def unknown_func(_=None):
        nonlocal unknown
        if _ is not None:
            unknown = _
            return scale
        return unknown

    def copy():
        return (
            radial()
            .domain(squared.domain())
            .range(range_vals)
            .round(round)
            .clamp(squared.clamp())
            .unknown(unknown)
        )

    scale.domain = domain_func
    scale.range = range_func
    scale.range_round = range_round_func
    scale.round = round_func
    scale.clamp = clamp_func
    scale.unknown = unknown_func
    scale.copy = copy

    init_range(scale)

    return linearish(scale)


# -----


# src/quantile.py
from d3_array import ascending, bisect, quantileSorted as threshold
from init import init_range


def quantile():
    domain = []
    range_vals = []
    thresholds = []
    unknown = None

    def rescale():
        nonlocal thresholds
        n = max(1, len(range_vals))
        thresholds = [None] * (n - 1)
        for i in range(1, n):
            thresholds[i - 1] = threshold(domain, i / n)
        return scale

    def scale(x):
        return (
            unknown
            if x is None or (isinstance(x, float) and math.isnan(x))
            else range_vals[bisect(thresholds, x)]
        )

    def invert_extent(y):
        i = range_vals.index(y)
        return (
            [None, None]
            if i < 0
            else [
                thresholds[i - 1] if i > 0 else domain[0],
                thresholds[i] if i < len(thresholds) else domain[-1],
            ]
        )

    def domain_func(_=None):
        if _ is None:
            return domain.copy()
        domain.clear()
        for d in _:
            if d is not None and not (isinstance(d, float) and math.isnan(d)):
                domain.append(d)
        domain.sort(ascending)
        return rescale()

    def range_func(_=None):
        if _ is not None:
            range_vals[:] = list(_)
            return rescale()
        return range_vals.copy()

    def unknown_func(_=None):
        nonlocal unknown
        if _ is not None:
            unknown = _
            return scale
        return unknown

    def quantiles_func():
        return thresholds.copy()

    def copy():
        return quantile().domain(domain).range(range_vals).unknown(unknown)

    scale.invert_extent = invert_extent
    scale.domain = domain_func
    scale.range = range_func
    scale.unknown = unknown_func
    scale.quantiles = quantiles_func
    scale.copy = copy

    return init_range(scale)


# -----


# src/constant.py
def constants(x):
    return lambda: x


# -----


# src/index.py
from band import scale_band, point as scale_point
from identity import scale_identity
from linear import scale_linear
from log import scale_log
from symlog import scale_symlog
from ordinal import scale_ordinal, implicit as scale_implicit
from pow import scale_pow, sqrt as scale_sqrt
from radial import scale_radial
from quantile import scale_quantile
from quantize import scale_quantize
from threshold import scale_threshold
from time import scale_time
from utcTime import scale_utc
from sequential import (
    scale_sequential,
    scale_sequential_log,
    scale_sequential_pow,
    scale_sequential_sqrt,
    scale_sequential_symlog,
)
from sequentialQuantile import scale_sequential_quantile
from diverging import (
    scale_diverging,
    scale_diverging_log,
    scale_diverging_pow,
    scale_diverging_sqrt,
    scale_diverging_symlog,
)

__all__ = [
    "scale_band",
    "scale_point",
    "scale_identity",
    "scale_linear",
    "scale_log",
    "scale_symlog",
    "scale_ordinal",
    "scale_implicit",
    "scale_pow",
    "scale_sqrt",
    "scale_radial",
    "scale_quantile",
    "scale_quantize",
    "scale_threshold",
    "scale_time",
    "scale_utc",
    "scale_sequential",
    "scale_sequential_log",
    "scale_sequential_pow",
    "scale_sequential_sqrt",
    "scale_sequential_symlog",
    "scale_sequential_quantile",
    "scale_diverging",
    "scale_diverging_log",
    "scale_diverging_pow",
    "scale_diverging_sqrt",
    "scale_diverging_symlog",
]


# -----


# src/linear.py
from d3_array import ticks, tick_increment
from continuous import continuous, copy
from init import init_range
from tickFormat import tick_format


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


# src/time.py
from d3_time import (
    timeYear,
    timeMonth,
    timeWeek,
    timeDay,
    timeHour,
    timeMinute,
    timeSecond,
    timeTicks,
    timeTickInterval,
)
from d3_time_format import timeFormat
from continuous import copy
from init import init_range
from nice import nice


def date(t):
    return datetime.datetime.fromtimestamp(t)


def number(t):
    return (
        t
        if isinstance(t, datetime.datetime)
        else datetime.datetime.fromtimestamp(t).timestamp()
    )


def calendar(
    ticks, tick_interval, year, month, week, day, hour, minute, second, format
):
    scale = continuous()
    invert = scale.invert
    domain = scale.domain

    format_millisecond = format(".%L")
    format_second = format(":%S")
    format_minute = format("%I:%M")
    format_hour = format("%I %p")
    format_day = format("%a %d")
    format_week = format("%b %d")
    format_month = format("%B")
    format_year = format("%Y")

    def tick_format(date):
        return (
            format_millisecond
            if second(date) < date
            else format_second
            if minute(date) < date
            else format_minute
            if hour(date) < date
            else format_hour
            if day(date) < date
            else format_week
            if month(date) < date
            else format_month
            if year(date) < date
            else format_year
        )(date)

    def invert_func(y):
        return datetime.datetime.fromtimestamp(invert(y))

    def domain_func(_=None):
        return (
            domain(list(map(number, _))) if _ is not None else list(map(date, domain()))
        )

    def ticks_func(interval):
        d = domain()
        return ticks(d[0], d[-1], interval if interval is not None else 10)

    def tick_format_func(count, specifier=None):
        return specifier is None and tick_format or format(specifier)

    def nice_func(interval=None):
        d = domain()
        if not interval or not hasattr(interval, "range"):
            interval = tick_interval(
                d[0], d[-1], interval if interval is not None else 10
            )
        return interval and domain(nice(d, interval)) or scale

    def copy_func():
        return copy(
            scale,
            calendar(
                ticks,
                tick_interval,
                year,
                month,
                week,
                day,
                hour,
                minute,
                second,
                format,
            ),
        )

    scale.invert = invert_func
    scale.domain = domain_func
    scale.ticks = ticks_func
    scale.tick_format = tick_format_func
    scale.nice = nice_func
    scale.copy = copy_func

    return scale


def time():
    return init_range(
        calendar(
            timeTicks,
            timeTickInterval,
            timeYear,
            timeMonth,
            timeWeek,
            timeDay,
            timeHour,
            timeMinute,
            timeSecond,
            timeFormat,
        ).domain([datetime.datetime(2000, 1, 1), datetime.datetime(2000, 1, 2)])
    )


# -----


# src/identity.py
from linear import linearish
from number import number


def identity(domain=None):
    unknown = None

    def scale(x):
        return unknown if x is None or (isinstance(x, float) and math.isnan(x)) else x

    scale.invert = scale

    def domain_func(_=None):
        return domain if _ is None else (domain := list(map(float, _)), scale)

    scale.domain = scale.range = domain_func

    def unknown_func(_=None):
        nonlocal unknown
        return unknown if _ is None else (unknown := _, scale)

    scale.unknown = unknown_func

    def copy_func():
        return identity(domain).unknown(unknown)

    scale.copy = copy_func

    domain = list(map(float, domain)) if domain is not None else [0, 1]

    return linearish(scale)


# -----


# src/tickFormat.py
from d3_array import tick_step
from d3_format import (
    format,
    format_prefix,
    format_specifier,
    precision_fixed,
    precision_prefix,
    precision_round,
)


def tick_format(start, stop, count, specifier):
    step = tick_step(start, stop, count)
    precision = None
    specifier = format_specifier(specifier if specifier is not None else ",f")

    if specifier.type == "s":
        value = max(abs(start), abs(stop))
        if specifier.precision is None and not math.isnan(
            precision := precision_prefix(step, value)
        ):
            specifier.precision = precision
        return format_prefix(specifier, value)
    elif specifier.type in ("", "e", "g", "p", "r"):
        if specifier.precision is None and not math.isnan(
            precision := precision_round(step, max(abs(start), abs(stop)))
        ):
            specifier.precision = precision - (specifier.type == "e")
    elif specifier.type in ("f", "%"):
        if specifier.precision is None and not math.isnan(
            precision := precision_fixed(step)
        ):
            specifier.precision = precision - (specifier.type == "%") * 2

    return format(specifier)


# -----


# src/quantize.py
from bisect import bisect
from linear import linearish
from init import init_range


def quantize():
    x0 = 0
    x1 = 1
    n = 1
    domain = [0.5]
    range_vals = [0, 1]
    unknown = None

    def scale(x):
        return (
            range_vals[bisect(domain, x, 0, n)] if x is not None and x <= x else unknown
        )

    def rescale():
        nonlocal domain
        domain = [(i + 1) * x1 - (i - n) * x0 / (n + 1) for i in range(n)]
        return scale

    def domain_func(_=None):
        return (
            (x0, x1) if _ is None else (x0 := float(_[0]), x1 := float(_[1]), rescale())
        )

    def range_func(_=None):
        return (
            range_vals.copy()
            if _ is None
            else (n := (range_vals := list(_)).length - 1, rescale())
        )

    def invert_extent(y):
        i = range_vals.index(y)
        return (
            [None, None]
            if i < 0
            else [domain[i - 1] if i > 0 else x0, domain[i] if i < n else x1]
        )

    def unknown_func(_=None):
        nonlocal unknown
        return unknown if _ is None else (unknown := _, scale)

    def thresholds_func():
        return domain.copy()

    def copy_func():
        return quantize().domain([x0, x1]).range(range_vals).unknown(unknown)

    scale.domain = domain_func
    scale.range = range_func
    scale.invert_extent = invert_extent
    scale.unknown = unknown_func
    scale.thresholds = thresholds_func
    scale.copy = copy_func

    return init_range(linearish(scale))


# -----
