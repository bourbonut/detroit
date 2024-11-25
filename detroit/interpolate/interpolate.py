# src/hue.py
from .color import hue


def hue_interpolator(a, b):
    i = hue(float(a), float(b))

    def interpolate(t):
        x = i(t)
        return x - 360 * math.floor(x / 360)

    return interpolate


# src/rgb.py
from d3_color import rgb as colorRgb

from .basis import basis
from .basisClosed import basisClosed
from .color import gamma, nogamma


def rgbGamma(y):
    color = gamma(y)

    def rgb(start, end):
        start = colorRgb(start)
        end = colorRgb(end)
        r = color(start.r, end.r)
        g = color(start.g, end.g)
        b = color(start.b, end.b)
        opacity = nogamma(start.opacity, end.opacity)

        def interpolate(t):
            start.r = r(t)
            start.g = g(t)
            start.b = b(t)
            start.opacity = opacity(t)
            return str(start)

        return interpolate

    rgb.gamma = rgbGamma
    return rgb


rgb = rgbGamma(1)


def rgbSpline(spline):
    def interpolate(colors):
        n = len(colors)
        r = [0] * n
        g = [0] * n
        b = [0] * n

        for i, color in enumerate(colors):
            color = colorRgb(color)
            r[i] = color.r or 0
            g[i] = color.g or 0
            b[i] = color.b or 0

        r_spline = spline(r)
        g_spline = spline(g)
        b_spline = spline(b)

        color = colorRgb()
        color.opacity = 1

        def interpolate(t):
            color.r = r_spline(t)
            color.g = g_spline(t)
            color.b = b_spline(t)
            return str(color)

        return interpolate

    return interpolate


rgbBasis = rgbSpline(basis)
rgbBasisClosed = rgbSpline(basisClosed)

# src/object.py
from .value import value


def object_interpolator(a, b):
    i = {}
    c = {}

    if a is None or not isinstance(a, dict):
        a = {}
    if b is None or not isinstance(b, dict):
        b = {}

    for k in b:
        if k in a:
            i[k] = value(a[k], b[k])
        else:
            c[k] = b[k]

    def interpolate(t):
        for k in i:
            c[k] = i[k](t)
        return c

    return interpolate


# src/numberArray.py
import numpy as np


def numberArray(a, b):
    if b is None:
        b = []
    n = min(len(b), len(a)) if a else 0
    c = b.copy()

    def interpolate(t):
        for i in range(n):
            c[i] = a[i] * (1 - t) + b[i] * t
        return c

    return interpolate


def isNumberArray(x):
    return isinstance(x, (np.ndarray, list)) and all(
        isinstance(i, (int, float)) for i in x
    )


# src/hcl.py
from d3_color import hcl as colorHcl

from .color import color, hue


def hcl(hue_func):
    def interpolator(start, end):
        start = colorHcl(start)
        end = colorHcl(end)
        h = hue_func(start.h, end.h)
        c = color(start.c, end.c)
        l = color(start.l, end.l)
        opacity = color(start.opacity, end.opacity)

        def interpolate(t):
            start.h = h(t)
            start.c = c(t)
            start.l = l(t)
            start.opacity = opacity(t)
            return str(start)

        return interpolate

    return interpolator


hcl_default = hcl(hue)
hclLong = hcl(color)


# src/number.py
def number(a, b):
    a, b = float(a), float(b)
    return lambda t: a * (1 - t) + b * t


# src/cubehelix.py
from d3_color import cubehelix as colorCubehelix

from .color import color, hue


def cubehelix(hue_func):
    def cubehelixGamma(y):
        y = float(y)

        def interpolator(start, end):
            start = colorCubehelix(start)
            end = colorCubehelix(end)
            h = hue_func(start.h, end.h)
            s = color(start.s, end.s)
            l = color(start.l, end.l)
            opacity = color(start.opacity, end.opacity)

            def interpolate(t):
                start.h = h(t)
                start.s = s(t)
                start.l = l(t**y)
                start.opacity = opacity(t)
                return str(start)

            return interpolate

        interpolator.gamma = cubehelixGamma
        return interpolator

    return cubehelixGamma(1)


cubehelix_default = cubehelix(hue)
cubehelixLong = cubehelix(color)

# src/piecewise.py
from .value import value as default_value


def piecewise(interpolate, values=None):
    if values is None:
        values = interpolate
        interpolate = default_value

    i = 0
    n = len(values) - 1
    v = values[0]
    I = [interpolate(v, values[i + 1]) for i in range(n)]

    def interpolator(t):
        i = max(0, min(n - 1, int(t * n)))
        return I[i](t * n - i)

    return interpolator


# src/round.py
def round_interpolator(a, b):
    a, b = float(a), float(b)
    return lambda t: round(a * (1 - t) + b * t)


# src/value.py
from d3_color import color

from .array import genericArray
from .constant import constant
from .date import date
from .number import number
from .numberArray import isNumberArray, numberArray
from .object import object_interpolator
from .rgb import rgb
from .string import string


def value(a, b):
    if b is None or isinstance(b, bool):
        return constant(b)
    if isinstance(b, (int, float)):
        return number
    if isinstance(b, str):
        c = color(b)
        return rgb if c else string
    if isinstance(b, color):
        return rgb
    if isinstance(b, datetime.date):
        return date
    if isNumberArray(b):
        return numberArray
    if isinstance(b, (list, tuple)):
        return genericArray
    if not hasattr(b, "valueOf") and not hasattr(b, "__str__") or math.isnan(b):
        return object_interpolator
    return number


# src/hsl.py
from d3_color import hsl as colorHsl

from .color import color, hue


def hsl(hue_func):
    def interpolator(start, end):
        start = colorHsl(start)
        end = colorHsl(end)
        h = hue_func(start.h, end.h)
        s = color(start.s, end.s)
        l = color(start.l, end.l)
        opacity = color(start.opacity, end.opacity)

        def interpolate(t):
            start.h = h(t)
            start.s = s(t)
            start.l = l(t)
            start.opacity = opacity(t)
            return str(start)

        return interpolate

    return interpolator


hsl_default = hsl(hue)
hslLong = hsl(color)


# src/discrete.py
def discrete(range_):
    n = len(range_)
    return lambda t: range_[max(0, min(n - 1, int(t * n)))]


# src/string.py
import re

from .number import number

reA = re.compile(r"[-+]?(?:\d+\.?\d*|\.?\d+)(?:[eE][-+]?\d+)?")
reB = re.compile(reA.pattern)


def zero(b):
    return lambda: b


def one(b):
    return lambda t: str(b(t))


def string(a, b):
    a, b = str(a), str(b)

    bi = 0
    s = []
    q = []

    for am in reA.finditer(a):
        bm = reB.search(b, bi)
        if bm:
            if bm.start() > bi:
                s.append(b[bi : bm.start()])

            if am.group() == bm.group():
                s.append(bm.group())
            else:
                s.append(None)
                q.append(
                    {"i": len(s) - 1, "x": number(float(am.group()), float(bm.group()))}
                )

            bi = bm.end()

    if bi < len(b):
        s.append(b[bi:])

    if len(s) < 2:
        return one(q[0]["x"]) if q else zero(b)

    def interpolator(t):
        for o in q:
            s[o["i"]] = str(o["x"](t))
        return "".join(s)

    return interpolator


# src/constant.py
def constant(x):
    return lambda: x


# src/array.py
from .numberArray import isNumberArray, numberArray
from .value import value


def array(a, b):
    return numberArray(a, b) if isNumberArray(b) else genericArray(a, b)


def genericArray(a, b):
    nb = len(b) if b else 0
    na = min(nb, len(a)) if a else 0
    x = [value(a[i], b[i]) for i in range(na)]
    c = list(b)

    def interpolate(t):
        for i in range(na):
            c[i] = x[i](t)
        return c

    return interpolate


# src/basisClosed.py
from .basis import basis


def basisClosed(values):
    n = len(values)

    def interpolate(t):
        i = int((t % 1) * n)
        v0 = values[(i + n - 1) % n]
        v1 = values[i % n]
        v2 = values[(i + 1) % n]
        v3 = values[(i + 2) % n]
        return basis((t - i / n) * n, v0, v1, v2, v3)

    return interpolate


# src/zoom.py
import math

epsilon2 = 1e-12


def cosh(x):
    return (math.exp(x) + 1 / math.exp(x)) / 2


def sinh(x):
    return (math.exp(x) - 1 / math.exp(x)) / 2


def tanh(x):
    return (math.exp(2 * x) - 1) / (math.exp(2 * x) + 1)


def zoomRho(rho, rho2, rho4):
    def zoom(p0, p1):
        ux0, uy0, w0 = p0
        ux1, uy1, w1 = p1
        dx = ux1 - ux0
        dy = uy1 - uy0
        d2 = dx * dx + dy * dy

        if d2 < epsilon2:
            S = math.log(w1 / w0) / rho

            def interpolator(t):
                return [ux0 + t * dx, uy0 + t * dy, w0 * math.exp(rho * t * S)]
        else:
            d1 = math.sqrt(d2)
            b0 = (w1 * w1 - w0 * w0 + rho4 * d2) / (2 * w0 * rho2 * d1)
            b1 = (w1 * w1 - w0 * w0 - rho4 * d2) / (2 * w1 * rho2 * d1)
            r0 = math.log(math.sqrt(b0 * b0 + 1) - b0)
            r1 = math.log(math.sqrt(b1 * b1 + 1) - b1)
            S = (r1 - r0) / rho

            def interpolator(t):
                s = t * S
                coshr0 = cosh(r0)
                u = w0 / (rho2 * d1) * (coshr0 * tanh(rho * s + r0) - sinh(r0))
                return [ux0 + u * dx, uy0 + u * dy, w0 * coshr0 / cosh(rho * s + r0)]

        interpolator.duration = S * 1000 * rho / math.sqrt(2)
        return interpolator

    def set_rho(new_rho):
        new_rho = max(1e-3, float(new_rho))
        return zoomRho(new_rho, new_rho * new_rho, new_rho**4)

    zoom.rho = set_rho
    return zoom


zoom = zoomRho(math.sqrt(2), 2, 4)


# src/basis.py
def basis(t1, v0, v1, v2, v3):
    t2 = t1 * t1
    t3 = t2 * t1
    return (
        (1 - 3 * t1 + 3 * t2 - t3) * v0
        + (4 - 6 * t2 + 3 * t3) * v1
        + (1 + 3 * t1 + 3 * t2 - 3 * t3) * v2
        + t3 * v3
    ) / 6


def basis_interpolator(values):
    n = len(values) - 1

    def interpolate(t):
        i = 0 if t <= 0 else (n - 1 if t >= 1 else int(t * n))
        v1 = values[i]
        v2 = values[i + 1]
        v0 = values[i - 1] if i > 0 else 2 * v1 - v2
        v3 = values[i + 2] if i < n - 1 else 2 * v2 - v1
        return basis((t - i / n) * n, v0, v1, v2, v3)

    return interpolate


# src/color.py
import math

from .constant import constant


def linear(a, d):
    return lambda t: a + t * d


def exponential(a, b, y):
    return lambda t: math.pow(a + t * (math.pow(b, y) - a), 1 / y)


def hue(a, b):
    d = b - a
    return (
        linear(a, d if abs(d) <= 180 else d - 360 * round(d / 360))
        if d
        else constant(math.isnan(a) and b or a)
    )


def gamma(y):
    y = float(y)
    if y == 1:
        return nogamma
    else:
        return (
            lambda a, b: exponential(a, b, y)
            if b - a
            else constant(math.isnan(a) and b or a)
        )


def nogamma(a, b):
    d = b - a
    return linear(a, d) if d else constant(math.isnan(a) and b or a)


# src/lab.py
from d3_color import lab as colorLab

from .color import color


def lab(start, end):
    start = colorLab(start)
    end = colorLab(end)
    l = color(start.l, end.l)
    a = color(start.a, end.a)
    b = color(start.b, end.b)
    opacity = color(start.opacity, end.opacity)

    def interpolate(t):
        start.l = l(t)
        start.a = a(t)
        start.b = b(t)
        start.opacity = opacity(t)
        return str(start)

    return interpolate


# src/date.py
import datetime


def date_interpolator(a, b):
    d = datetime.datetime.now()
    a, b = a.timestamp(), b.timestamp()

    def interpolate(t):
        d = datetime.datetime.fromtimestamp(a * (1 - t) + b * t)
        return d

    return interpolate


# src/quantize.py
def quantize(interpolator, n):
    samples = [interpolator(i / (n - 1)) for i in range(n)]
    return samples


# src/transform/parse.py
import math

from .decompose import decompose, identity


def parseCss(value):
    try:
        from cssselect import parser

        m = parser.parse_style_attribute(value)[0]
        return decompose(m.a, m.b, m.c, m.d, m.e, m.f)
    except ImportError:
        print("cssselect library not found. Install it for CSS parsing support.")
        return identity


def parseSvg(value):
    if value is None:
        return identity
    try:
        from svg.path import parse_path

        path = parse_path(value)
        m = path.transform()
        return decompose(m.a, m.b, m.c, m.d, m.e, m.f)
    except ImportError:
        print("svg.path library not found. Install it for SVG parsing support.")
        return identity


# src/transform/decompose.py
import math

degrees = 180 / math.pi

identity = {
    "translateX": 0,
    "translateY": 0,
    "rotate": 0,
    "skewX": 0,
    "scaleX": 1,
    "scaleY": 1,
}


def decompose(a, b, c, d, e, f):
    scaleX = math.sqrt(a * a + b * b)
    scaleY = math.sqrt(c * c + d * d)

    if scaleX:
        a /= scaleX
        b /= scaleX

    skewX = a * c + b * d
    if skewX:
        c -= a * skewX
        d -= b * skewX

    if scaleY:
        c /= scaleY
        d /= scaleY
        skewX /= scaleY

    if a * d < b * c:
        a, b, c, d = -a, -b, -c, -d
        scaleX, scaleY = -scaleX, -scaleY

    return {
        "translateX": e,
        "translateY": f,
        "rotate": math.atan2(b, a) * degrees,
        "skewX": math.atan(skewX) * degrees,
        "scaleX": scaleX,
        "scaleY": scaleY,
    }


# src/transform/index.py
from ..number import number
from .parse import parseCss, parseSvg


def interpolateTransform(parse, pxComma, pxParen, degParen):
    def pop(s):
        return s.pop() + " " if s else ""

    def translate(xa, ya, xb, yb, s, q):
        if xa != xb or ya != yb:
            s.extend(["translate(", None, pxComma, None, pxParen])
            q.extend(
                [
                    {"i": len(s) - 4, "x": number(xa, xb)},
                    {"i": len(s) - 2, "x": number(ya, yb)},
                ]
            )
        elif xb or yb:
            s.append(f"translate({xb}{pxComma}{yb}{pxParen}")

    def rotate(a, b, s, q):
        if a != b:
            if a - b > 180:
                b += 360
            elif b - a > 180:
                a += 360
            q.append({"i": len(s), "x": number(a, b)})
            s.extend([pop(s) + "rotate(", None, degParen])
        elif b:
            s.append(f"{pop(s)}rotate({b}{degParen}")

    def skewX(a, b, s, q):
        if a != b:
            q.append({"i": len(s), "x": number(a, b)})
            s.extend([pop(s) + "skewX(", None, degParen])
        elif b:
            s.append(f"{pop(s)}skewX({b}{degParen}")

    def scale(xa, ya, xb, yb, s, q):
        if xa != xb or ya != yb:
            s.extend([pop(s) + "scale(", None, ",", None, ")"])
            q.extend(
                [
                    {"i": len(s) - 4, "x": number(xa, xb)},
                    {"i": len(s) - 2, "x": number(ya, yb)},
                ]
            )
        elif xb != 1 or yb != 1:
            s.append(f"{pop(s)}scale({xb},{yb})")

    def interpolator(a, b):
        s = []
        q = []
        a = parse(a)
        b = parse(b)
        translate(
            a["translateX"], a["translateY"], b["translateX"], b["translateY"], s, q
        )
        rotate(a["rotate"], b["rotate"], s, q)
        skewX(a["skewX"], b["skewX"], s, q)
        scale(a["scaleX"], a["scaleY"], b["scaleX"], b["scaleY"], s, q)

        def interpolate(t):
            for o in q:
                s[o["i"]] = o["x"](t)
            return "".join(s)

        return interpolate

    return interpolator


interpolateTransformCss = interpolateTransform(parseCss, "px, ", "px)", "deg)")
interpolateTransformSvg = interpolateTransform(parseSvg, ", ", ")", ")")
