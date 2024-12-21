import detroit as d3

schemes = [
    ("category_10", d3.SCHEME_CATEGORY_10),
    ("accent", d3.SCHEME_ACCENT),
    ("dark_2", d3.SCHEME_DARK_2),
    ("observable_10", d3.SCHEME_OBSERVABLE_10),
    ("paired", d3.SCHEME_PAIRED),
    ("pastel_1", d3.SCHEME_PASTEL_1),
    ("pastel_2", d3.SCHEME_PASTEL_2),
    ("set_1", d3.SCHEME_SET_1),
    ("set_2", d3.SCHEME_SET_2),
    ("set_3", d3.SCHEME_SET_3),
    ("tableau_10", d3.SCHEME_TABLEAU_10),
    ("brbg", d3.SCHEME_BRBG[-1]),
    ("prgn", d3.SCHEME_PRGN[-1]),
    ("piyg", d3.SCHEME_PIYG[-1]),
    ("puor", d3.SCHEME_PUOR[-1]),
    ("rdbu", d3.SCHEME_RDBU[-1]),
    ("rdgy", d3.SCHEME_RDGY[-1]),
    ("rdylbu", d3.SCHEME_RDYLBU[-1]),
    ("rdylgn", d3.SCHEME_RDYLGN[-1]),
    ("spectral", d3.SCHEME_SPECTRAL[-1]),
    ("blues", d3.SCHEME_BLUES[-1]),
    ("greens", d3.SCHEME_GREENS[-1]),
    ("greys", d3.SCHEME_GREYS[-1]),
    ("oranges", d3.SCHEME_ORANGES[-1]),
    ("purples", d3.SCHEME_PURPLES[-1]),
    ("reds", d3.SCHEME_REDS[-1]),
    ("bugn", d3.SCHEME_BUGN[-1]),
    ("bupu", d3.SCHEME_BUPU[-1]),
    ("gnbu", d3.SCHEME_GNBU[-1]),
    ("orrd", d3.SCHEME_ORRD[-1]),
    ("pubugn", d3.SCHEME_PUBUGN[-1]),
    ("pubu", d3.SCHEME_PUBU[-1]),
    ("purd", d3.SCHEME_PURD[-1]),
    ("rdpu", d3.SCHEME_RDPU[-1]),
    ("ylgnbu", d3.SCHEME_YLGNBU[-1]),
    ("ylgn", d3.SCHEME_YLGN[-1]),
    ("ylorbr", d3.SCHEME_YLORBR[-1]),
    ("ylorrd", d3.SCHEME_YLORRD[-1]),
]

for name, scheme in schemes:
    color = d3.scale_ordinal(scheme)

    rect_size = 40
    rect_count = len(scheme)

    width = rect_size * rect_count
    height = rect_size

    svg = (
        d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", f"0 0 {width} {height}")
    )

    (
        svg.select_all("rect")
        .data(scheme)
        .join("rect")
        .attr("x", lambda _, i: rect_size * i)
        .attr("y", 0)
        .attr("width", rect_size)
        .attr("height", rect_size)
        .attr("fill", color)
    )

    with open(f"discrete_scheme_{name}.svg", "w") as file:
        file.write(str(svg))
