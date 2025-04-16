import detroit as d3
from operator import itemgetter

width = 480
height = 400
margin_top = 20
margin_right = 50
margin_bottom = 10
margin_left = 120

numba = [
    (97.52, "macroscopic"),
    (93.8, "equilibrium"),
    (92.71, "streaming_step"),
    (89.62, "collision"),
    (85.13, "bounce_back"),
    (6.1, "inflow"),
    (5.98, "update_fin"),
    (5.86, "outflow"),
]
cupy = [
    (98.44, "macroscopic"),
    (92.99, "streaming_step"),
    (92.86, "equilibrium"),
    (87.6, "collision"),
    (85.1, "bounce_back"),
    (5.98, "update_fin"),
    (5.98, "inflow"),
    (5.84, "outflow"),
]

svg = (
    d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", f"0 0 {width} {height}")
    .style("max-width", "100%")
    .style("height", "auto")
)

access = itemgetter(0)
x_max = max(max(map(access, cupy)), max(map(access, numba)))
x = d3.scale_linear([0, x_max], [margin_left, width - margin_right])

domain = reversed(list(map(itemgetter(1), numba)))
y = d3.scale_band(domain, [height - margin_bottom, margin_top]).set_padding(0.7)

(
    svg.append("g")
    .select_all()
    .data(numba)
    .join("rect")
    .attr("x", x(0))
    .attr("y", lambda d: y(d[1]) + y.get_bandwidth() * 0.1)
    .attr("width", lambda d: x(d[0]) - x(0))
    .attr("height", y.get_bandwidth())
    .attr("fill", d3.hsl("blue").brighter(1.5))
    .attr("stroke", "blue")
)


(
    svg.append("g")
    .select_all()
    .data(cupy)
    .join("rect")
    .attr("x", x(0))
    .attr("y", lambda d: y(d[1]) - y.get_bandwidth() * 1.1)
    .attr("width", lambda d: x(d[0]) - x(0))
    .attr("height", y.get_bandwidth())
    .attr("fill", d3.hsl("red").brighter(1.5))
    .attr("stroke", "red")
)


(
    svg.append("g")
    .select_all()
    .data(numba)
    .join("text")
    .attr("x", lambda d: x(d[0]) + 5)
    .attr("y", lambda d: y(d[1]) + y.get_bandwidth() * 0.9)
    .attr("stroke", "none")
    .attr("fill", "blue")
    .text(lambda d: str(d[0]))
)

(
    svg.append("g")
    .select_all()
    .data(cupy)
    .join("text")
    .attr("x", lambda d: x(d[0]) + 5)
    .attr("y", lambda d: y(d[1]) - y.get_bandwidth() * 0.3)
    .attr("stroke", "none")
    .attr("fill", "red")
    .text(lambda d: str(d[0]))
)

(
    svg.append("g")
    .attr("transform", f"translate({margin_left}, 0)")
    .call(d3.axis_left(y).set_tick_size(0).set_tick_padding(8))
    .call(lambda g: g.select(".domain").remove())
    .attr("font-size", "14px")
)

g = svg.append("g").attr("transform", f"translate({width * 0.75}, 10)")

(
    g.append("rect")
    .attr("x", -5)
    .attr("y", -5)
    .attr("width", 75)
    .attr("height", 42)
    .attr("fill", "white")
    .attr("stroke", "black")
)

(
    g.append("rect")
    .attr("x", 0)
    .attr("y", 0)
    .attr("width", 10)
    .attr("height", 10)
    .attr("fill", d3.hsl("blue").brighter(1.5))
    .attr("stroke", "blue")
)

(
    g.append("rect")
    .attr("x", 0)
    .attr("y", 20)
    .attr("width", 10)
    .attr("height", 10)
    .attr("fill", d3.hsl("red").brighter(1.5))
    .attr("stroke", "red")
)

g.append("text").attr("x", 15).attr("y", 10).text("Numba")
g.append("text").attr("x", 15).attr("y", 30).text("Cupy")

with open("kernel_results.svg", "w") as file:
    file.write(str(svg))
