# Source: https://observablehq.com/@d3/tree-component
import detroit as d3
import json
import requests
from math import inf

URL = "https://static.observableusercontent.com/files/e65374209781891f37dea1e7a6e1c5e020a3009b8aedf113b4c80942018887a1176ad4945cf14444603ff91d3da371b3b0d72419fa8d2ee0f6e815732475d5de?response-content-disposition=attachment%3Bfilename*%3DUTF-8%27%27flare-2.json"

flare = json.loads(requests.get(URL).content)


def label(d):
    return d.data["name"]


def title(node):
    return ".".join((d.data["name"] for d in reversed(node.ancestors())))


def link(node):
    p1 = "tree" if node.children else "blob"
    p2 = "/".join((d.data["name"] for d in reversed(node.ancestors())))
    p3 = "" if node.children else ".as"
    return f"https://github.com/prefuse/Flare/{p1}/master/flare/src/{p2}{p3}"


width = 1152
padding = 1

root = d3.hierarchy(flare)
descendants = root.descendants()

dx = 10
dy = width / (root.height + padding)
d3.tree().set_node_size([dx, dy])(root)

x = [inf, -inf]


def visit(d):
    if d.x > x[1]:
        x[1] = d.x
    if d.x < x[0]:
        x[0] = d.x


root.each(visit)

height = x[1] - x[0] + dx * 2
curve = d3.curve_bump_x

svg = (
    d3.create("svg")
    .attr("viewBox", [-dy * padding * 0.5, x[0] - dx, width, height])
    .attr("width", width)
    .attr("height", height)
    .attr("style", "max-width: 100%; height: auto;")
    .attr("font-family", "sans-serif")
    .attr("font-size", 10)
)

(
    svg.append("g")
    .attr("fill", "none")
    .attr("stroke", "#555")
    .attr("stroke-opacity", 0.4)
    .attr("stroke-width", 1.5)
    .select_all("path")
    .data(root.links())
    .join("path")
    .attr("d", d3.link(curve).x(lambda d: d.y).y(lambda d: d.x))
)

node = (
    svg.append("g")
    .select_all("a")
    .data(root.descendants())
    .join("a")
    .attr("xlink:href", link)
    .attr("target", "blank_")
    .attr("transform", lambda d: f"translate({d.y}, {d.x})")
)

(
    node.append("circle")
    .attr("fill", lambda d: "#555" if d.children else "#999")
    .attr("r", 3)
)
(node.append("title").text(title))

(
    node.append("text")
    .attr("dy", "0.32em")
    .attr("x", lambda d: -6 if d.children else 6)
    .attr("text-anchor", lambda d: "end" if d.children else "start")
    .attr("paint-order", "stroke")
    .attr("stroke", "#fff")
    .attr("stroke-width", 3)
    .text(label)
)

with open("tree.svg", "w") as file:
    file.write(str(svg))
