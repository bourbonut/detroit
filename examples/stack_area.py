# Source: https://observablehq.com/@d3/normalized-stacked-area-chart/2
import polars as pl

import detroit as d3

URL = "https://static.observableusercontent.com/files/76f13741128340cc88798c0a0b7fa5a2df8370f57554000774ab8ee9ae785ffa2903010cad670d4939af3e9c17e5e18e7e05ed2b38b848ac2fc1a0066aa0005f?response-content-disposition=attachment%3Bfilename*%3DUTF-8%27%27unemployment.csv"

unemployment = pl.read_csv(URL).select(
    pl.col("date").str.to_datetime("%Y-%m-%d"),
    pl.all().exclude("date"),
)
data = unemployment.to_dicts()

width = 928
height = 500
margin_top = 20
margin_right = 20
margin_bottom = 20
margin_left = 40


# Determine the series that need to be stacked.
series = (
    d3.stack()
    .set_offset(d3.stack_offset_expand)
    .set_keys(
        unemployment["industry"].unique().to_list()
    )  # distinct series keys, in input order
    .set_value(
        lambda d, key, index, data: data[d][key]["unemployed"]
    )(  # get value for each series key and stack
        d3.index(data, lambda d: d["date"], lambda d: d["industry"])
    )  # group by stack then series key
)

# Prepare the scales for positional and color encodings.
x = (
    d3.scale_time()
    .set_domain(d3.extent(data, lambda d: d["date"]))
    .set_range([margin_left, width - margin_right])
)

y = d3.scale_linear().set_range_round([height - margin_bottom, margin_top])

color = (
    d3.scale_ordinal()
    .set_domain([d.key for d in series])
    .set_range(d3.SCHEME_TABLEAU_10)
)

# Construct an area shape.
area = d3.area().x(lambda d: x(d.data.timestamp())).y0(lambda d: y(d[0])).y1(lambda d: y(d[1]))

# Create the SVG container.
svg = (
    d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("view_box", [0, 0, width, height])
    .attr("style", "max-width: 100% height: auto")
)

# Append a path for each series.
(
    svg.append("g")
    .select_all()
    .data(series)
    .join("path")
    .attr("fill", lambda d: color(d.key))
    .attr("d", area)
    .append("title")
    .text(lambda d: d.key)
)

# Append the x axis, and remove the domain line.
(
    svg.append("g")
    .attr("transform", f"translate(0, {height - margin_bottom})")
    .call(d3.axis_bottom(x).set_tick_size_outer(0))
    .call(lambda g: g.select(".domain").remove())
)

# Add the y axis, remove the domain line, add grid lines and a label.
(
    svg.append("g")
    .attr("transform", f"translate({margin_left},0)")
    .call(d3.axis_left(y).set_ticks(height / 80, "%"))
    .call(lambda g: g.select(".domain").remove())
    .call(
        lambda g: g.select_all(".tick line")
        .filter(lambda d: d == 0 or d == 1)
        .clone()
        .attr("x2", width - margin_left - margin_right)
    )
    .call(
        lambda g: g.append("text")
        .attr("x", -margin_left)
        .attr("y", 10)
        .attr("fill", "currentColor")
        .attr("text-anchor", "start")
        .text("↑ Unemployed persons")
    )
)

with open("stack_area.svg", "w") as file:
    file.write(str(svg))
