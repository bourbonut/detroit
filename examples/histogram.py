from collections import namedtuple

import polars as pl

import detroit as d3

URL = "https://static.observableusercontent.com/files/8a6057f29caa4e010854bfc31984511e074ff9042ec2a99f30924984821414fbaeb75e59654e9303db359dfa0c1052534691dac86017c4c2f992d23b874f9b6e?response-content-disposition=attachment%3Bfilename*%3DUTF-8%27%27unemployment-x.csv"
Margin = namedtuple("Margin", ["top", "right", "bottom", "left"])

unemployment = pl.read_csv(URL)

width = 928
height = 500
margin = Margin(20, 20, 30, 40)

# Bin the data.
bins = d3.bin().thresholds(40).value(lambda d: d[3])(unemployment.iter_rows())

# Declare the x (horizontal position) scale.
x = (
    d3.scale_linear()
    .set_domain([bins[0].x0, bins[-1].x1])
    .set_range([margin.left, width - margin.right])
)

# Declare the y (vertical position) scale.
y = (
    d3.scale_linear()
    .set_domain([0, max(map(len, bins))])
    .set_range([height - margin.bottom, margin.top])
)

# Create the SVG container.
svg = (
    d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", f"0, 0, {width}, {height}")
    .attr("style", "max-width: 100%; height: auto;")
)

# Add a rect for each bin.
(
    svg.append("g")
    .attr("fill", "steelblue")
    .select_all()
    .data(bins)
    .join("rect")
    .attr("x", lambda d: x(d.x0) + 1)
    .attr("width", lambda d: x(d.x1) - x(d.x0) - 1)
    .attr("y", lambda d: y(len(d)))
    .attr("height", lambda d: y(0) - y(len(d)))
)

# Add the x-axis and label.
(
    svg.append("g")
    .attr("transform", f"translate(0, {height - margin.bottom})")
    .call(d3.axis_bottom(x).set_ticks(width / 80).set_tick_size_outer(0))
    .call(
        lambda g: g.append("text")
        .attr("x", width)
        .attr("y", margin.bottom - 4)
        .attr("fill", "currentColor")
        .attr("text-anchor", "end")
        .text("Unemployment rate (%) →")
    )
)

# Add the y-axis and label, and remove the domain line.
(
    svg.append("g")
    .attr("transform", f"translate({margin.left}, 0)")
    .call(d3.axis_left(y).set_ticks(height / 40))
    .call(lambda g: g.select(".domain").remove())
    .call(
        lambda g: (
            g.append("text")
            .attr("x", -margin.left)
            .attr("y", 10)
            .attr("fill", "currentColor")
            .attr("text-anchor", "start")
            .text("↑ Frequency (no. of counties)")
        )
    )
)

# For white axis and text
# svg.select_all("path.domain").attr("stroke", "white")
# svg.select_all("g.tick").select_all("line").attr("stroke", "white")
# svg.select_all("g.tick").select_all("text").attr("fill", "white").attr("stroke", "none")
# svg.select_all("text").attr("fill", "white").attr("stroke", "none")

with open("histogram.svg", "w") as file:
    file.write(str(svg))
