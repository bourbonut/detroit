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
