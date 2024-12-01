import re

# [[fill]align][sign][symbol][0][width][,][.precision][~][type]
FORMAT_RE = re.compile(
    r"^(?:(.)?([<>=^]))?([+\-( ])?([$#])?(0)?(\d+)?(,)?(\.\d+)?(~)?([a-z%])?$", re.I
)


class FormatSpecifier:
    def __init__(self, specifier):
        self.fill = " " if specifier.get("fill") is None else str(specifier["fill"])
        self.align = ">" if specifier.get("align") is None else str(specifier["align"])
        self.sign = "-" if specifier.get("sign") is None else str(specifier["sign"])
        self.symbol = (
            "" if specifier.get("symbol") is None else str(specifier["symbol"])
        )
        self.zero = bool(specifier.get("zero"))
        self.width = None if specifier.get("width") is None else int(specifier["width"])
        self.comma = bool(specifier.get("comma"))
        self.precision = (
            None if specifier.get("precision") is None else int(specifier["precision"])
        )
        self.trim = bool(specifier.get("trim"))
        self.type = "" if specifier.get("type") is None else str(specifier["type"])

    def __str__(self):
        parts = [
            self.fill,
            self.align,
            self.sign,
            self.symbol,
            "0" if self.zero else "",
            str(self.width) if self.width is not None else "",
            "," if self.comma else "",
            f".{self.precision}" if self.precision is not None else "",
            "~" if self.trim else "",
            self.type,
        ]
        return "".join(parts)


def format_specifier(specifier: str) -> FormatSpecifier:
    match = FORMAT_RE.match(specifier)
    if not match:
        raise ValueError(f"invalid format: {specifier}")

    groups = match.groups()
    return FormatSpecifier(
        {
            "fill": groups[0],
            "align": groups[1],
            "sign": groups[2],
            "symbol": groups[3],
            "zero": groups[4],
            "width": groups[5],
            "comma": groups[6],
            "precision": groups[7][1:] if groups[7] else None,
            "trim": groups[8],
            "type": groups[9],
        }
    )
