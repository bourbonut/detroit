from collections import namedtuple

import polars as pl

import detroit as d3

URL = "https://static.observableusercontent.com/files/609a91fa3908394198a9b2592b8432a798332e9a140a8d5f9c864615e3f18b2e822badadc579c06b394bb1396a20f064d72123b718354b829978b2d4782bd5c9?response-content-disposition=attachment%3Bfilename*%3DUTF-8%27%27traffic.csv"

Margin = namedtuple("Margin", ["top", "right", "bottom", "left"])

theme = "light"

traffic = (
    (
        pl.read_csv(URL)
        .select(
            pl.col("location"),
            pl.col("date")
            .str.to_datetime("%Y-%m-%dT%H:%MZ", strict=False)
            .dt.hour()
            .alias("hour"),
            pl.col("vehicles"),
        )
        .fill_null(0)
    )
    .group_by("location", "hour")
    .agg(pl.col("vehicles").median())
)

data = traffic.to_dicts()

width = 640
height = 820

margin = Margin(15, 40, 45, 120)

# Declare the x (horizontal position) scale.
x = d3.scale_band(list(map(str, range(24))), [margin.left, width - margin.right])

# Declare the y (vertical position) scale.
sorted_locations = (
    traffic.select(["location", "vehicles"])
    .sort("vehicles", descending=True)["location"]
    .unique(maintain_order=True)
    .to_list()
)
y = d3.scale_band(sorted_locations, [height - margin.bottom, margin.top])

# Color scale for cell colors
color = d3.scale_sequential([0, traffic["vehicles"].max()], d3.interpolate_turbo)

svg = (
    d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", f"0 0 {width} {height}")
)

# Add the x-axis, remove the domain line.
(
    svg.append("g")
    .attr("transform", f"translate(0, {height - margin.bottom})")
    .call(d3.axis_bottom(x))
    .call(lambda g: g.select(".domain").remove())
)

# Add the y-axis, remove the domain line.
(
    svg.append("g")
    .attr("transform", f"translate({margin.left}, 0)")
    .call(d3.axis_left(y))
    .call(lambda g: g.select(".domain").remove())
)

# Add cells.
(
    svg.append("g")
    .select_all()
    .data(data)
    .join("rect")
    .attr("x", lambda d: x(str(d["hour"])) + 0.5)
    .attr("y", lambda d: y(d["location"]) + 0.5)
    .attr("width", 19)
    .attr("height", 19)
    .attr("fill", lambda d: color(d["vehicles"]))
)

if theme == "dark":
    svg.select_all("path.domain").attr("stroke", "white")
    svg.select_all("g.tick line").attr("stroke", "white")
    svg.select_all("g.tick text").attr("fill", "white").attr("stroke", "none")
    svg.select_all("text").attr("fill", "white").attr("stroke", "none")

with open(f"{theme}-heatmap.svg", "w") as file:
    file.write(str(svg))
