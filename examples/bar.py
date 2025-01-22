# Source : https://observablehq.com/@d3/bar-chart/2
from collections import namedtuple
import polars as pl
import detroit as d3

URL = "https://static.observableusercontent.com/files/09f63bb9ff086fef80717e2ea8c974f918a996d2bfa3d8773d3ae12753942c002d0dfab833d7bee1e0c9cd358cd3578c1cd0f9435595e76901508adc3964bbdc?response-content-disposition=attachment%3Bfilename*%3DUTF-8%27%27alphabet.csv"
Margin = namedtuple("Margin", ["top", "right", "bottom", "left"])

alphabet = pl.read_csv(URL).sort(by="frequency", descending=True)

width = 928
height = 500
margin = Margin(30, 0, 30, 40)

# Declare the x (horizontal position) scale.
# descending frequency
x = (
    d3.scale_band()
    .set_domain(alphabet["letter"].unique(maintain_order=True))
    .set_range([margin.left, width - margin.right])
    .set_padding(0.1)
)

# Declare the y (vertical position) scale.
y = (
    d3.scale_linear()
    .set_domain([0, alphabet["frequency"].max()])
    .set_range([height - margin.bottom, margin.top])
)

# Create the SVG container.
svg = (
    d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", f"0 0 {width} {height}")
    .attr("style", "max-width: 100%; height: auto;")
)

# Add a rect for each bar.
(
    svg.append("g")
    .select_all()
    .data(alphabet.iter_rows())
    .join("rect")
    .attr("x", lambda d: x(d[0]))
    .attr("y", lambda d: y(d[1]))
    .attr("height", lambda d: y(0) - y(d[1]))
    .attr("width", x.bandwidth)
    .attr("fill", "steelblue")
)

# Add the x-axis and label.
svg.append("g").attr("transform", f"translate(0, {height - margin.bottom})").call(
    d3.axis_bottom(x).set_tick_size_outer(0)
)

# Add the y-axis and label, and remove the domain line.
(
    svg.append("g")
    .attr("transform", f"translate({margin.left}, 0)")
    .call(d3.axis_left(y).set_tick_format(lambda y: str(int(y * 100))))
    .call(lambda g: g.select(".domain").remove())
    .call(
        lambda g: g.append("text")
        .attr("x", -margin.left)
        .attr("y", 10)
        .attr("fill", "currentColor")
        .attr("text-anchor", "start")
        .text("↑ Frequency (%)")
    )
)

# For white axis and text
# svg.select_all("path.domain").attr("stroke", "white")
# svg.select_all("g.tick").select_all("line").attr("stroke", "white")
# svg.select_all("g.tick").select_all("text").attr("fill", "white").attr("stroke", "none")
# svg.select_all("text").attr("fill", "white").attr("stroke", "none")

with open("bar.svg", "w") as file:
    file.write(str(svg))
