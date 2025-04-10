import detroit as d3
from datetime import datetime

width = 810
height = 30
margin = 15

svg = (
    d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", f"0 0 {width} {height}")
)
axis = d3.axis_bottom(d3.scale_linear().set_range([0, width - 2 * margin]))
x1 = svg.append("g").attr("transform", f"translate({margin}, {margin * 0.5})").call(
    axis.set_ticks(3, "%")
)

# To change color all in white
# svg.select_all(".domain").attr("stroke", "white")
# svg.select_all("g.tick").attr("fill", "none").attr("stroke", "white")
# svg.select_all("line").attr("fill", "none").attr("stroke", "white")
# svg.select_all("text").style("fill", "white").style("stroke", "none")

# with open("light_axis_ticks_1.svg", "w") as file:
    # file.write(str(svg))

svg = (
    d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", f"0 0 {width} {height}")
)
scale = d3.scale_time(
    [datetime(2000, 1, 1, 12, 0), datetime(2000, 1, 1, 13, 0)], [0, 1]
)
axis = d3.axis_bottom(scale.set_range([0, width - 2 * margin]))
x2 = svg.append("g").attr("transform", f"translate({margin}, {margin * 0.5})").call(
    axis.set_ticks(d3.time_minute.every(15))
)

# To change color all in white
# svg.select_all(".domain").attr("stroke", "white")
# svg.select_all("g.tick").attr("fill", "none").attr("stroke", "white")
# svg.select_all("line").attr("fill", "none").attr("stroke", "white")
# svg.select_all("text").style("fill", "white").style("stroke", "none")

# with open("light_axis_ticks_2.svg", "w") as file:
    # file.write(str(svg))

svg = (
    d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", f"0 0 {width} {height}")
)
axis = d3.axis_bottom(
    d3.scale_linear().set_domain([0, 360]).set_range([0, width - 2 * margin])
)
x3 = (
    svg.append("g")
    .attr("transform", f"translate({margin}, {margin * 0.5})")
    .call(axis.set_tick_values([0, 120, 240, 360]))
)

# To change color all in white
# svg.select_all(".domain").attr("stroke", "white")
# svg.select_all("g.tick").attr("fill", "none").attr("stroke", "white")
# svg.select_all("line").attr("fill", "none").attr("stroke", "white")
# svg.select_all("text").style("fill", "white").style("stroke", "none")

# with open("light_axis_angle.svg", "w") as file:
    # file.write(str(svg))

svg = (
    d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", f"0 0 {width} {height}")
)
axis = d3.axis_bottom(
    d3.scale_linear().set_domain([0, 10_000]).set_range([0, width - 2 * margin])
)
x4 = (
    svg.append("g")
    .attr("transform", f"translate({margin}, {margin * 0.5})")
    .call(axis.set_tick_format(d3.format("~s")))
)

# To change color all in white
# svg.select_all(".domain").attr("stroke", "white")
# svg.select_all("g.tick").attr("fill", "none").attr("stroke", "white")
# svg.select_all("line").attr("fill", "none").attr("stroke", "white")
# svg.select_all("text").style("fill", "white").style("stroke", "none")

# with open("light_axis_format.svg", "w") as file:
    # file.write(str(svg))

svg = (
    d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", f"0 0 {width} {height}")
)
axis = d3.axis_bottom(d3.scale_linear().set_range([0, width - 2 * margin]))
x5 = (
    svg.append("g")
    .attr("transform", f"translate({margin}, {margin * 0.5})")
    .call(axis.set_tick_size(12))
)

# To change color all in white
# svg.select_all(".domain").attr("stroke", "white")
# svg.select_all("g.tick").attr("fill", "none").attr("stroke", "white")
# svg.select_all("line").attr("fill", "none").attr("stroke", "white")
# svg.select_all("text").style("fill", "white").style("stroke", "none")

# with open("light_axis_tick_size.svg", "w") as file:
    # file.write(str(svg))

svg = (
    d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", f"0 0 {width} {height}")
)
axis = d3.axis_bottom(d3.scale_linear().set_range([0, width - 2 * margin]))
x6 = (
    svg.append("g")
    .attr("transform", f"translate({margin}, {margin * 0.5})")
    .call(axis.set_tick_size_inner(0))
)

# To change color all in white
# svg.select_all(".domain").attr("stroke", "white")
# svg.select_all("g.tick").attr("fill", "none").attr("stroke", "white")
# svg.select_all("line").attr("fill", "none").attr("stroke", "white")
# svg.select_all("text").style("fill", "white").style("stroke", "none")

# with open("light_axis_tick_size_inner.svg", "w") as file:
    # file.write(str(svg))

svg = (
    d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", f"0 0 {width} {height}")
)
axis = d3.axis_bottom(d3.scale_linear().set_range([0, width - 2 * margin]))
x7 = (
    svg.append("g")
    .attr("transform", f"translate({margin}, {margin * 0.5})")
    .call(axis.set_tick_size_outer(12))
)

# To change color all in white
# svg.select_all(".domain").attr("stroke", "white")
# svg.select_all("g.tick").attr("fill", "none").attr("stroke", "white")
# svg.select_all("line").attr("fill", "none").attr("stroke", "white")
# svg.select_all("text").style("fill", "white").style("stroke", "none")

# with open("light_axis_tick_size_outer.svg", "w") as file:
    # file.write(str(svg))

svg = (
    d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", f"0 0 {width} {height}")
)
axis = d3.axis_bottom(d3.scale_linear().set_range([0, width - 2 * margin]))
x8 = (
    svg.append("g")
    .attr("transform", f"translate({margin}, {margin * 0.5})")
    .call(axis.set_tick_padding(8))
)

# To change color all in white
# svg.select_all(".domain").attr("stroke", "white")
# svg.select_all("g.tick").attr("fill", "none").attr("stroke", "white")
# svg.select_all("line").attr("fill", "none").attr("stroke", "white")
# svg.select_all("text").style("fill", "white").style("stroke", "none")

# with open("light_axis_tick_padding.svg", "w") as file:
    # file.write(str(svg))

svg = (
    d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", f"0 0 {width} {height}")
)
axis = d3.axis_bottom(d3.scale_linear().set_range([0, width - 2 * margin]))
x9 = (
    svg.append("g")
    .attr("transform", f"translate({margin}, {margin * 0.5})")
    .call(axis.set_offset(8))
)

# To change color all in white
# svg.select_all(".domain").attr("stroke", "white")
# svg.select_all("g.tick").attr("fill", "none").attr("stroke", "white")
# svg.select_all("line").attr("fill", "none").attr("stroke", "white")
# svg.select_all("text").style("fill", "white").style("stroke", "none")

# with open("light_axis_offset.svg", "w") as file:
    # file.write(str(svg))
