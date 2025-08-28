import detroit as d3

width = 688
height = 400

graticule = d3.geo_graticule_10()
outline = {"type": "Sphere"}

theme = "light"
color = "white" if theme == "dark" else "black"

projection = (
    d3.geo_orthographic().rotate([110, -40])
    .fit_extent([[1, 1], [width - 1, height - 1]], {"type": "Sphere"})
    .set_precision(0.2)
)
path = d3.geo_path(projection)

svg = (
    d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", f"0 0 {width} {height}")
)
(
    svg.append("path")
    .attr("name", "graticule")
    .attr("d", path(graticule))
    .attr("stroke", color)
    .attr("stroke-opacity", 0.2)
    .attr("fill", "none")
)

with open(f"{theme}-graticule.svg", "w") as file:
    file.write(str(svg))
