from detroit import Script, d3, svg, Data, js, render, save
import json

# https://observablehq.com/@d3/volcano-contours/2
values = json.load(open("volcano.json", "r"))
data = Data(values)

n = values["width"]
m = values["height"]
width = 928
height = round(m / n * width)


def make_contours(script, interpolation):
    path = script("path", d3.geoPath().projection(d3.geoIdentity().scale(width / n)))
    contours = script("contours", d3.contours().size([n, m]))

    color = script(
        "color", d3.scaleSequential(interpolation).domain(d3.extent(data.values)).nice()
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
    return script


interpolations = {
    "Turbo color scheme": d3.interpolateTurbo,
    "Warm color scheme": d3.interpolateWarm,
    "Plasma color scheme": d3.interpolatePlasma,
    "Inferno color scheme": d3.interpolateInferno,
}

length = len(interpolations)
scripts = {
    title: make_contours(script, interpolation)
    for (title, interpolation), script in zip(
        interpolations.items(), Script.multiple(length)
    )
}
# or without title
# scripts = [
#  make_contours(script, interpolation)
#  for script, interpolation in zip(interpolation.values(), Script.multiple(n))
# ]
# render(values, scripts, grid=2) # grid = number of columns
save(values, scripts, "multiple-volcano.png", grid=2)
