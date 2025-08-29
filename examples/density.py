# https://observablehq.com/@d3/density-contours
import detroit as d3
import polars as pl

URL = "https://static.observableusercontent.com/files/98d78d7f290f9776833e989617d49b592039ea65fee3b451764067cccd582eac122b3a07619cf223e8526910284fc105dfcb24b9af785535ee1dc6914687f9ac?response-content-disposition=attachment%3Bfilename*%3DUTF-8%27%27faithful.tsv"

faithful = pl.read_csv(URL, separator="\t").to_dicts()

width = 928
height = 600
margin_top = 20
margin_right = 30
margin_bottom = 30
margin_left = 40

# Create the horizontal and vertical scales.
x = (
    d3.scale_linear()
    .set_domain(d3.extent(faithful, lambda d: d["waiting"]))
    .nice()
    .set_range_round([margin_left, width - margin_right])
)

y = (
    d3.scale_linear()
    .set_domain(d3.extent(faithful, lambda d: d["eruptions"]))
    .nice()
    .set_range_round([height - margin_bottom, margin_top])
)

# Compute the density contours.
contours = (
    d3.contour_density()
    .x(lambda d: x(d["waiting"]))
    .y(lambda d: y(d["eruptions"]))
    .set_size([width, height])
    .set_bandwidth(30)
    .set_thresholds(30)(faithful)
)

# Create the SVG container.
svg = (
    d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("view_box", f"0 0 {width} {height}")
    .attr("style", "max-width: 100%; height: auto;")
)

# Append the axes.
(
    svg.append("g")
    .attr("transform", f"translate(0,{height - margin_bottom})")
    .call(d3.axis_bottom(x).set_tick_size_outer(0))
    .call(lambda g: g.select(".domain").remove())
    .call(
        lambda g: g.select(".tick:last-of-type text")
        .clone()
        .attr("y", -3)
        .attr("dy", "null")
        .attr("font-weight", "bold")
        .text("Idle (min.)")
    )
)

(
    svg.append("g")
    .attr("transform", f"translate({margin_left},0)")
    .call(d3.axis_left(y).set_tick_size_outer(0))
    .call(lambda g: g.select(".domain").remove())
    .call(
        lambda g: g.select(".tick:last-of-type text")
        .clone()
        .attr("x", 3)
        .attr("text-anchor", "start")
        .attr("font-weight", "bold")
        .text("Erupting (min.)")
    )
)

# Append the contours.
(
    svg.append("g")
    .attr("fill", "none")
    .attr("stroke", "steelblue")
    .attr("stroke-linejoin", "round")
    .select_all()
    .data(contours)
    .join("path")
    .attr("stroke-width", lambda d, i: 1 if i % 5 else 0.25)
    .attr("d", d3.geo_path())
)

# Append dots.
(
    svg.append("g")
    .attr("stroke", "white")
    # .attr("fill", "white") # for dark mode
    .select_all()
    .data(faithful)
    .join("circle")
    .attr("cx", lambda d: x(d["waiting"]))
    .attr("cy", lambda d: y(d["eruptions"]))
    .attr("r", 2)
)

# # For white axis and text
# svg.select_all("path.domain").attr("stroke", "white")
# svg.select_all("g.tick line").attr("stroke", "white")
# svg.select_all("g.tick text").attr("fill", "white").attr("stroke", "none")
# svg.select_all("text").attr("fill", "white").attr("stroke", "none")

with open("light-density.svg", "w") as file:
    file.write(str(svg))
