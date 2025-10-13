# Source: https://observablehq.com/@d3/icicle/2
import detroit as d3
import json
import requests
from functools import cmp_to_key

URL = "https://static.observableusercontent.com/files/cd7473c8d22df421e1d13814d93aec5294e72dd53726b0fe3f3e3cbf2cc76069f8ccd3a69f0728774c97f5e34941bc5a8f8a0cea8ed1165f7bea9ca00e54cabd?response-content-disposition=attachment%3Bfilename*%3DUTF-8%27%27flare-2.json"

data = json.loads(requests.get(URL).content)

width = 928
height = 2400
format_func = d3.format(",d")

color = d3.scale_ordinal(d3.quantize(d3.interpolate_rainbow, len(data["children"]) + 1))

partition = d3.partition().set_size([height, width]).set_padding(1)
root = partition(
    d3.hierarchy(data)
    .sum(lambda d: d.get("value"))
    .sort(cmp_to_key(lambda a, b: b.height - a.height or b.value - a.value))
)

svg = (
    d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [0, 0, width, height])
    .attr("style", "max-width: 100%; height: auto; font: 10px sans-serif;")
)

cell = (
    svg.select_all()
    .data(root.descendants())
    .join("g")
    .attr("transform", lambda d: f"translate({d.y0}, {d.x0})")
)


def title(node):
    return ".".join((d.data["name"] for d in reversed(node.ancestors())))


cell.append("title").text(title)


def fill(d):
    if not d.depth:
        return "#ccc"
    while d.depth > 1:
        d = d.parent
    return color(d.data["name"])


(
    cell.append("rect")
    .attr("width", lambda d: d.y1 - d.y0)
    .attr("height", lambda d: d.x1 - d.x0)
    .attr("fill-opacity", 0.6)
    .attr("fill", fill)
)

text = (
    cell.filter(lambda d: (d.x1 - d.x0) > 16).append("text").attr("x", 4).attr("y", 13)
)

text.append("tspan").text(lambda d: d.data["name"])
text.append("tspan").attr("fill-opacity", 0.7).text(
    lambda d: f" {format_func(d.value)}"
)

with open("partition.svg", "w") as file:
    file.write(str(svg))
