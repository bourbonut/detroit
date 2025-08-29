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
