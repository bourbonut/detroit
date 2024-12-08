from collections import namedtuple
from math import pi, sin

from detroit import (  # useful classes to simplify js syntax
    Data,
    Script,
    arrange,
    d3,
    function,
    js,
    svg,
    websocket_render,  # function to render and update values
)
from detroit.ui import websocket_save

Margin = namedtuple("Margin", ("top", "right", "bottom", "left"))

istep = 4 * pi / 1000
xv = [istep * i for i in range(1000)]
yv = list(map(sin, xv))

data = Data.arrange([xv, yv])

margin = Margin(10, 30, 30, 60)
width = 660 - margin.left - margin.right
height = 420 - margin.top - margin.bottom

script = Script()

script(
    "svg",
    d3.select(script.plot_id)
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", f"translate({margin.left}, {margin.top})"),
)
x = script("x", d3.scaleLinear().domain([0, max(xv)]).range([0, width]))

script(
    svg.append("g")
    .attr("transform", f"translate(0, {height / 2})")
    .attr("class", "xaxis")
    .call(d3.axisBottom(x))
)
y = script("y", d3.scaleLinear().domain([-1, 1]).range([height, -1]).nice())

script(svg.append("g").call(d3.axisLeft(y)))

line = script(
    "line",
    svg.append("path")
    .datum(data)
    .attr("fill", "none")
    .attr("stroke", "deepskyblue")
    .attr(
        "d",
        d3.line().x(function("d").inline("x(d.x)")).y(function("d").inline("y(d.y)")),
    ),
)

update = function("data", "xmax", name="update")
update(x.domain([0, js("xmax")]).nice())
update(svg.selectAll("g.xaxis").call(d3.axisBottom(x)))
update(
    line.datum(data).attr(
        "d",
        d3.line().x(function("d").inline("x(d.x)")).y(function("d").inline("y(d.y)")),
    )
)

script(update)


def generator():
    s = 1000
    istep = 4 * pi / 1000
    xv = [istep * i for i in range(1000)]
    yv = list(map(sin, xv))
    for i in range(1000):
        xmax = istep * (s + i)
        xv.append(xmax)
        yv.append(sin(istep * (s + i)))
        yield {"values": arrange([xv, yv]), "xmax": xmax}


websocket_render(generator, script, event=update.call("values", "xmax"), init_data=data)
# websocket_save(generator, script, event=js("update(received_data.values, received_data.xmax);"), init_data=data)
