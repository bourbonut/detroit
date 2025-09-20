# https://observablehq.com/@d3/mobile-patent-suits
# Note: in Python, `set` objects are unordered. Therefore, the color order
# (here green, blue, orange) and the position of nodes may vary for each
# execution. If you want to have the same result for all executions, you should
# the order of `set` objects to have the same starting data for each execution
# Try this:
# ```
# types = sorted(set(map(itemgetter("type"), suits)))
# nodes = [
#     {"id": id_}
#     for id_ in sorted(
#         reduce(ior, map(lambda link: set((link["source"], link["target"])), suits), set())
#     )
# ]
# ```

import detroit as  d3

from math import hypot
from functools import reduce
from operator import itemgetter, ior

suits = [
    {"source": "Microsoft", "target": "Amazon", "type": "licensing"},
    {"source": "Microsoft", "target": "HTC", "type": "licensing"},
    {"source": "Samsung", "target": "Apple", "type": "suit"},
    {"source": "Motorola", "target": "Apple", "type": "suit"},
    {"source": "Nokia", "target": "Apple", "type": "resolved"},
    {"source": "HTC", "target": "Apple", "type": "suit"},
    {"source": "Kodak", "target": "Apple", "type": "suit"},
    {"source": "Microsoft", "target": "Barnes & Noble", "type": "suit"},
    {"source": "Microsoft", "target": "Foxconn", "type": "suit"},
    {"source": "Oracle", "target": "Google", "type": "suit"},
    {"source": "Apple", "target": "HTC", "type": "suit"},
    {"source": "Microsoft", "target": "Inventec", "type": "suit"},
    {"source": "Samsung", "target": "Kodak", "type": "resolved"},
    {"source": "LG", "target": "Kodak", "type": "resolved"},
    {"source": "RIM", "target": "Kodak", "type": "suit"},
    {"source": "Sony", "target": "LG", "type": "suit"},
    {"source": "Kodak", "target": "LG", "type": "resolved"},
    {"source": "Apple", "target": "Nokia", "type": "resolved"},
    {"source": "Qualcomm", "target": "Nokia", "type": "resolved"},
    {"source": "Apple", "target": "Motorola", "type": "suit"},
    {"source": "Microsoft", "target": "Motorola", "type": "suit"},
    {"source": "Motorola", "target": "Microsoft", "type": "suit"},
    {"source": "Huawei", "target": "ZTE", "type": "suit"},
    {"source": "Ericsson", "target": "ZTE", "type": "suit"},
    {"source": "Kodak", "target": "Samsung", "type": "resolved"},
    {"source": "Apple", "target": "Samsung", "type": "suit"},
    {"source": "Kodak", "target": "RIM", "type": "suit"},
    {"source": "Nokia", "target": "Qualcomm", "type": "suit"},
]

width = 928
height = 600
types = list(set(map(itemgetter("type"), suits)))
nodes = [
    {"id": id_}
    for id_ in reduce(ior, map(lambda link: set((link["source"], link["target"])), suits), set())
]
links = suits

color = d3.scale_ordinal(types, d3.SCHEME_CATEGORY_10)

simulation = (
    d3.force_simulation(nodes)
    .set_force("link", d3.force_link(links).set_id(itemgetter("id")))
    .set_force("charge", d3.force_many_body().set_strength(-400))
    .set_force("x", d3.force_x())
    .set_force("y", d3.force_y())
    .set_alpha_target(0.3)
)

simulation.tick(30)

svg = (
    d3.create("svg")
    .attr("viewBox", ", ".join(map(str, [-width / 2, -height / 2, width, height])))
    .attr("width", width)
    .attr("height", height)
    .attr("style", "max-width: 100% height: auto font: 12px sans-serif")
)

# Per-type markers, as they don't inherit styles.
(
    svg.append("defs")
    .select_all("marker")
    .data(types)
    .join("marker")
    .attr("id", lambda d: f"arrow-{d}")
    .attr("viewBox", "0 -5 10 10")
    .attr("refX", 15)
    .attr("refY", -0.5)
    .attr("markerWidth", 6)
    .attr("markerHeight", 6)
    .attr("orient", "auto")
    .append("path")
    .attr("fill", color)
    .attr("d", "M0,-5L10,0L0,5")
)

link = (
    svg.append("g")
    .attr("fill", "none")
    .attr("stroke-width", 1.5)
    .select_all("path")
    .data(links)
    .join("path")
    .attr("stroke", lambda d: color(d["type"]))
    .attr("marker-end", lambda d: f"url(#arrow-{d['type']})")
)

def link_arc(d):
    r = hypot(d["target"]["x"] - d["source"]["x"], d["target"]["y"] - d["source"]["y"])
    return f"M{d['source']['x']},{d['source']['y']}A{r},{r} 0 0,1 {d['target']['x']},{d['target']['y']}"

link.attr("d", link_arc)


node = (
    svg.append("g")
    .attr("fill", "currentColor")
    .attr("stroke-linecap", "round")
    .attr("stroke-linejoin", "round")
    .select_all("g")
    .data(nodes)
    .join("g")
)

node.append("circle").attr("stroke", "white").attr("stroke-width", 1.5).attr("r", 4)

(
    node.append("text")
    .attr("x", 8)
    .attr("y", "0.31em")
    .text(itemgetter("id"))
    .attr("fill", "black")
    .attr("stroke", "none")
)

node.attr("transform", lambda d: f"translate({d['x']},{d['y']})")

with open("force-graph.svg", "w") as file:
    file.write(str(svg))
