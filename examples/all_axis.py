import detroit as d3

width = 810
height = 570
margin = 30
offset = 5

svg = (
    d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", f"0 0 {width} {height}")
)

(
    svg.append("g")
    .attr("transform", f"translate({margin}, {margin - offset})")
    .call(d3.axis_top(d3.scale_linear().set_domain([0, 10]).set_range([0, width - 2 * margin - offset])))
    .append("text")
    .style("fill", "black")
    .style("font-size", 20)
    .style("text-anchor", "middle")
    .attr("x", width * 0.5 - margin - offset)
    .attr("y", margin)
    .text("axis_top")
)

(
    svg.append("g")
    .attr("transform", f"translate({margin}, {height - margin})")
    .call(d3.axis_bottom(d3.scale_linear().set_domain([0, 10]).set_range([0, width - 2 * margin - offset])))
    .append("text")
    .style("fill", "black")
    .style("font-size", 20)
    .style("text-anchor", "middle")
    .attr("x", width * 0.5 - margin - offset)
    .attr("y", -margin)
    .text("axis_bottom")
)

(
    svg.append("g")
    .attr("transform", f"translate({margin - offset}, {margin})")
    .call(d3.axis_left(d3.scale_linear().set_domain([0, 10]).set_range([0, height - 2 * margin - offset])))
    .append("text")
    .style("fill", "black")
    .style("font-size", 20)
    .style("text-anchor", "middle")
    .attr("x", margin * 2)
    .attr("y", height * 0.5 - margin + 0.5 * offset)
    .text("axis_left")
)

(
    svg.append("g")
    .attr("transform", f"translate({width - margin}, {margin})")
    .call(d3.axis_right(d3.scale_linear().set_domain([0, 10]).set_range([0, height - 2 * margin - offset])))
    .append("text")
    .style("fill", "black")
    .style("font-size", 20)
    .style("text-anchor", "middle")
    .attr("x", -margin * 2)
    .attr("y", height * 0.5 - margin + 0.5 * offset)
    .text("axis_right")
)

# To change color all in white
# svg.select_all("path.domain").attr("stroke", "white")
# svg.select_all("g.tick line").attr("stroke", "white")
# svg.select_all("g.tick text").attr("fill", "white").attr("stroke", "none")
# svg.select_all("text").attr("fill", "white").attr("stroke", "none")

with open("all_axis.svg", "w") as file:
    file.write(str(svg))
