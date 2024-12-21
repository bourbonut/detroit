import detroit as d3

width = 810
height = 40
rect_width = 2

schemes = [
    ("rainbow", d3.interpolate_rainbow),
    ("sinebow", d3.interpolate_sinebow),
    ("brbg", d3.interpolate_brbg),
    ("prgn", d3.interpolate_prgn),
    ("piyg", d3.interpolate_piyg),
    ("puor", d3.interpolate_puor),
    ("rdbu", d3.interpolate_rdbu),
    ("rdgy", d3.interpolate_rdgy),
    ("rdylbu", d3.interpolate_rdylbu),
    ("rdylgn", d3.interpolate_rdylgn),
    ("spectral", d3.interpolate_spectral),
    ("blues", d3.interpolate_blues),
    ("greens", d3.interpolate_greens),
    ("greys", d3.interpolate_greys),
    ("oranges", d3.interpolate_oranges),
    ("purples", d3.interpolate_purples),
    ("reds", d3.interpolate_reds),
    ("turbo", d3.interpolate_turbo),
    ("viridis", d3.interpolate_viridis),
    ("inferno", d3.interpolate_inferno),
    ("magma", d3.interpolate_magma),
    ("plasma", d3.interpolate_plasma),
    ("cividis", d3.interpolate_cividis),
    ("warm", d3.interpolate_warm),
    ("cool", d3.interpolate_cool),
    ("cubehelix_default", d3.interpolate_cubehelix_default),
    ("bugn", d3.interpolate_bugn),
    ("bupu", d3.interpolate_bupu),
    ("gnbu", d3.interpolate_gnbu),
    ("orrd", d3.interpolate_orrd),
    ("pubugn", d3.interpolate_pubugn),
    ("pubu", d3.interpolate_pubu),
    ("purd", d3.interpolate_purd),
    ("rdpu", d3.interpolate_rdpu),
    ("ylgnbu", d3.interpolate_ylgnbu),
    ("ylgn", d3.interpolate_ylgn),
    ("ylorbr", d3.interpolate_ylorbr),
    ("ylorrd", d3.interpolate_ylorrd),
]

for name, scheme in schemes:
    color = d3.scale_sequential([0, width], scheme)

    svg = (
        d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", f"0 0 {width} {height}")
    )

    (
        svg.select_all("rect")
        .data(list(range(0, width, rect_width)))
        .join("rect")
        .attr("x", lambda d: d)
        .attr("y", 0)
        .attr("width", rect_width + 1)
        .attr("height", height)
        .attr("fill", color)
    )

    with open(f"scheme_{name}.svg", "w") as file:
        file.write(str(svg))
