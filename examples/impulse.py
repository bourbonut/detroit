# Step Response of a Second Order System (Control Theory)
from collections import namedtuple
from math import exp, sin, sqrt

import detroit as d3

theme = "light"

Margin = namedtuple("Margin", ("top", "right", "bottom", "left"))

# Arbitrary parameters for second order system.
K = 1
omega_0 = 2
e0 = 1


def second_order(t, zeta):
    if t <= 0:
        return 0
    if zeta > 1:
        p1 = -zeta * omega_0 + omega_0 * sqrt(zeta * zeta - 1)
        p2 = -zeta * omega_0 - omega_0 * sqrt(zeta * zeta - 1)
        return K * omega_0 / (2 * sqrt(zeta * zeta - 1)) * (exp(p1 * t) - exp(p2 * t))
    else:
        return (
            K
            * omega_0
            / sqrt(1 - zeta * zeta)
            * exp(-zeta * omega_0 * t)
            * sin(omega_0 * sqrt(1 - zeta * zeta) * t)
        )


xmax = 10
steps = 1000

xvalues = [(xmax * i / steps) for i in range(steps)]
allzeta = [2, 1.7, 1.5, 1.3, 1.1, 0.9, 0.7, 0.6, 0.4, 0.2]
data = {
    "allzeta": allzeta,
    "allvalues": [
        {"key": zeta, "values": [{"x": t, "y": second_order(t, zeta)} for t in xvalues]}
        for zeta in allzeta
    ],
}


# Specify the chart's dimensions.
margin = Margin(10, 30, 30, 60)
width = 960 - margin.left - margin.right
height = 680 - margin.top - margin.bottom

# Create the SVG container.
svg = (
    d3.create("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", f"translate({margin.left}, {margin.top})")
)

# Create the horizontal x scale.
x = (
    d3.scale_linear()
    .set_domain(d3.extent(data["allvalues"][0]["values"], lambda d: d["x"]))
    .set_range([0, width])
)


svg.append("g").attr("transform", f"translate(0, {height})").call(
    d3.axis_bottom(x).set_tick_format(d3.format(".0f"))
)

# Create the vertical y scale.
ymax = max(data["allvalues"][-1]["values"], key=lambda d: d["y"])["y"]

y = d3.scale_linear().set_domain([-ymax, ymax]).set_range([height, -1]).nice()

svg.append("g").call(d3.axis_left(y).set_tick_format(d3.format(".1f")))

# Create the color scale given zeta values.
color = (
    d3.scale_linear()
    .set_domain([max(data["allzeta"]), min(data["allzeta"])])
    .set_range(["gold", "deepskyblue"])
)

# Append the pathes for the lines.
line = d3.line().x(lambda d: x(d["x"])).y(lambda d: y(d["y"]))
(
    svg.select_all(".line")
    .data(data["allvalues"])
    .enter()
    .append("path")
    .attr("fill", "none")
    .attr("stroke", lambda d: color(d["key"]))
    .attr("d", lambda d: line(d["values"]))
)

if theme == "dark":
    svg.select_all("path.domain").attr("stroke", "white")
    svg.select_all("g.tick line").attr("stroke", "white")
    svg.select_all("g.tick text").attr("fill", "white").attr("stroke", "none")
    svg.select_all("text").attr("fill", "white").attr("stroke", "none")

with open(f"{theme}-impulse.svg", "w") as file:
    file.write(str(svg))
