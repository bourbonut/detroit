from collections import namedtuple
from functools import reduce
from operator import attrgetter, iadd

import detroit as d3

Margin = namedtuple("Margin", ["top", "right", "bottom", "left"])
Curve = namedtuple("Curve", ["values", "label", "color"])

width = 770
height = 500
margin = Margin(60, 20, 30, 40)

colors = ["royalblue", "goldenrod", "tomato"]
curves = [
    Curve(
        values=[(xi, pow(xi, i + 1)) for xi in range(0, 10)],
        label=f"$y = x^{i + 1}$" if i > 0 else "$y = x$",
        color=colors[i],
    )
    for i in range(3)
]


all_values = reduce(iadd, map(attrgetter("values"), curves), [])
x = d3.scale_linear(
    d3.extent(all_values, lambda d: d[0]), [margin.left, width - margin.right]
)
y = d3.scale_linear(
    d3.extent(all_values, lambda d: d[1]), [height - margin.bottom, margin.top]
)

line = d3.line().x(lambda d: x(d[0])).y(lambda d: y(d[1]))

svg = (
    d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", f"0, 0, {width}, {height}")
    .attr("style", "max-width: 100%; height: auto;")
)

(
    svg.append("g")
    .attr("transform", f"translate(0, {height - margin.bottom})")
    .call(d3.axis_bottom(x))
    .call(
        lambda g: g.append("text")
        .attr("x", width - margin.right)
        .attr("y", -4)
        .attr("fill", "#000")
        .attr("text-anchor", "end")
        .attr("font-weight", "bold")
        .text("x →")
    )
)

(
    svg.append("g")
    .attr("transform", f"translate({margin.left}, 0)")
    .call(d3.axis_left(y))
    .call(
        lambda g: (
            g.append("text")
            .attr("x", -margin.left // 2)
            .attr("y", margin.top - 10)
            .attr("fill", "currentColor")
            .attr("text-anchor", "start")
            .text("↑ y")
        )
    )
)

(
    svg.select_all(".line")
    .data(curves)
    .enter()
    .append("path")
    .attr("fill", "none")
    .attr("stroke", lambda d: d.color)
    .attr("stroke-width", 1.5)
    .attr("d", lambda d: line(d.values))
)

nb_columns = 3
middle = (width - 100 * nb_columns) / 2
rect_size = 20

(
    svg.select_all("legend")
    .data(curves)
    .enter()
    .append("g")
    .append("rect")
    .attr("x", lambda d, i: (i % nb_columns) * 100 + margin.left // 2)
    .attr("y", lambda d, i: 16 + 30 * (i // nb_columns))
    .attr("width", rect_size)
    .attr("height", rect_size)
    .style("fill", lambda d: d.color)
)

(
    svg.select_all("squares")
    .data(curves)
    .enter()
    .append("g")
    .append("text")
    .attr("x", lambda d, i: rect_size + 5 + (i % nb_columns) * 100 + margin.left // 2)
    .attr("y", lambda d, i: 30 * (i // nb_columns + 1))
    .text(lambda d: d.label)
    .style("fill", "black")
    .style("font-size", 15)
)

with open("figure.svg", "w") as file:
    file.write(str(svg))
