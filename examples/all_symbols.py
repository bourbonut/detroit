import detroit as d3

width = 810
height = 40

# Fill symbols

svg = (
    d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", f"0 0 {width} {height}")
    .append("g")
    .attr("transform", f"translate(0, {int(height // 2)})")
)

names = ["circle", "cross", "diamond", "square", "star", "triangle", "wye"]
symbol_type = d3.scale_ordinal(names, d3.SYMBOLS_FILL)

axis = d3.scale_band(names, [0, width]).set_padding(1)

(
    svg.call(d3.axis_bottom(axis).set_tick_size_outer(0).set_offset(0))
    .call(lambda g: g.select(".domain").remove())
)

(
    svg.select_all("symbols")
    .data(names)
    .join("g")
    .attr("transform", lambda d: f"translate({axis(d)}, -10)")
    .append("path")
    .attr("d", lambda d: d3.symbol(symbol_type(d))())
    .attr("fill", "black")
)

with open("symbols_fill.svg", "w") as file:
    file.write(str(svg))

# Stroke symbols

svg = (
    d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", f"0 0 {width} {height}")
    .append("g")
    .attr("transform", f"translate(0, {int(height // 2)})")
)

names = ["asterisk", "circle", "diamond2", "plus", "square2", "times", "triangle2"]
symbol_type = d3.scale_ordinal(names, d3.SYMBOLS_STROKE)

axis = d3.scale_band(names, [0, width]).set_padding(1)

(
    svg.call(d3.axis_bottom(axis).set_tick_size_outer(0).set_offset(0))
    .call(lambda g: g.select(".domain").remove())
)

(
    svg.select_all("symbols")
    .data(names)
    .join("g")
    .attr("transform", lambda d: f"translate({axis(d)}, -10)")
    .append("path")
    .attr("d", lambda d: d3.symbol(symbol_type(d))())
    .attr("stroke", "black")
)

with open("symbols_stroke.svg", "w") as file:
    file.write(str(svg))
