import json

from detroit import (  # useful classes to simplify js syntax
    Data,
    Script,
    d3,
    js,
    render,  # render the script in your browser
    save,
    svg,
)

# https://observablehq.com/@d3/volcano-contours/2
values = json.load(open("volcano.json", "r"))
data = Data(values)

script = Script()  # All `script(...)` will be stored in this class

n = values["width"]  # or data.width.data
m = values["height"]
width = 928
height = round(m / n * width)

path = script("path", d3.geoPath().projection(d3.geoIdentity().scale(width / n)))
contours = script("contours", d3.contours().size([n, m]))

color = script(
    "color",
    d3.scaleSequential(d3.interpolateTurbo).domain(d3.extent(data.values)).nice(),
)

script(
    "svg",
    d3.select(script.plot_id)
    .append("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [0, 0, width, height])
    .attr("style", "max-width: 100%; height: auto;"),
)

script(
    svg.append("g")
    .attr("stroke", "black")
    .selectAll()
    .data(js("color.ticks(20)"))
    .join("path")
    .attr("d", js("d => path(contours.contour(data.values, d))"))
    .attr("fill", color)
)

# render(values, script) # then open `localhost:5000` in your browser
save(values, script, "volcano.svg")
