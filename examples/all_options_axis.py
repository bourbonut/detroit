from datetime import datetime

import detroit as d3

width = 810
height = 30
margin = 15

theme = "light"

axes = [
    (
        "axis_ticks_1",
        d3.axis_bottom(d3.scale_linear().set_range([0, width - 2 * margin])).set_ticks(
            3, "%"
        ),
    ),
    (
        "axis_ticks_2",
        d3.axis_bottom(
            d3.scale_time(
                [datetime(2000, 1, 1, 12, 0), datetime(2000, 1, 1, 13, 0)], [0, 1]
            ).set_range([0, width - 2 * margin])
        ).set_ticks(d3.time_minute.every(15)),
    ),
    (
        "axis_angle",
        d3.axis_bottom(
            d3.scale_linear().set_domain([0, 360]).set_range([0, width - 2 * margin])
        ).set_tick_values([0, 120, 240, 360]),
    ),
    (
        "axis_format",
        d3.axis_bottom(
            d3.scale_linear().set_domain([0, 10_000]).set_range([0, width - 2 * margin])
        ).set_tick_format(d3.format("~s")),
    ),
    (
        "axis_ticks_size",
        d3.axis_bottom(
            d3.scale_linear().set_range([0, width - 2 * margin])
        ).set_tick_size(12),
    ),
    (
        "axis_tick_size_inner",
        d3.axis_bottom(
            d3.scale_linear().set_range([0, width - 2 * margin])
        ).set_tick_size_inner(0),
    ),
    (
        "axis_ticks_size_outer",
        d3.axis_bottom(
            d3.scale_linear().set_range([0, width - 2 * margin])
        ).set_tick_size_outer(12),
    ),
    (
        "axis_tick_padding",
        d3.axis_bottom(
            d3.scale_linear().set_range([0, width - 2 * margin])
        ).set_tick_padding(8),
    ),
    (
        "axis_offset",
        d3.axis_bottom(d3.scale_linear().set_range([0, width - 2 * margin])).set_offset(
            8
        ),
    ),
]


def generate_svg(title, axis):
    svg = (
        d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", f"0 0 {width} {height}")
    )
    (
        svg.append("g")
        .attr("transform", f"translate({margin}, {margin * 0.5})")
        .call(axis)
    )

    if theme == "dark":
        svg.select_all("path.domain").attr("stroke", "white")
        svg.select_all("g.tick line").attr("stroke", "white")
        svg.select_all("g.tick text").attr("fill", "white").attr("stroke", "none")
        svg.select_all("text").attr("fill", "white").attr("stroke", "none")

    with open(f"{theme}_{title}.svg", "w") as file:
        file.write(str(svg))


for title, axis in axes:
    generate_svg(title, axis)
