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
