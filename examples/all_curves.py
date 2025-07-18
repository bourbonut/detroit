import detroit as d3

width = 810
margin_left = 5
margin_right = 5
x_max = 40
y_max = 12
square_length = (width - margin_left - margin_right) / x_max
height = y_max * square_length
legend_height = int(square_length * 3)
legend_width = int(square_length * 15)

rect_color = "#2b2b2e"
line_color = "#202020"
font_color = curve_color = point_color = "white"
start_color = "#999999"

# Uncomment these lines for white theme
rect_color = "#d4d4d1"
line_color = "#f8f8f8"
font_color = curve_color = point_color = "black"
start_color = "#303030"

curves = [
    ("basis", d3.curve_basis),
    ("basis_closed", d3.curve_basis_closed),
    ("basis_open", d3.curve_basis_open),
    ("bump_radial", d3.curve_bump_radial),
    ("bump_x", d3.curve_bump_x),
    ("bump_y", d3.curve_bump_y),
    ("linear", d3.curve_linear),
    ("linear_closed", d3.curve_linear_closed),
    ("monotone_x", d3.curve_monotone_x),
    ("monotone_y", d3.curve_monotone_y),
    ("natural", d3.curve_natural),
    ("step", d3.curve_step),
    ("step_after", d3.curve_step_after),
    ("step_before", d3.curve_step_before),
]

parametric_curves = [
    ("bundle", d3.curve_bundle, "beta"),
    ("cardinal", d3.curve_cardinal, "tension"),
    ("cardinal_closed", d3.curve_cardinal_closed, "tension"),
    ("cardinal_open", d3.curve_cardinal_open, "tension"),
    ("catmull_rom", d3.curve_catmull_rom, "alpha"),
    ("catmull_rom_closed", d3.curve_catmull_rom_closed, "alpha"),
    ("catmull_rom_open", d3.curve_catmull_rom_open, "alpha"),
]

points = [
    [2, 2],
    [6, 8],
    [10, 10],
    [12, 10],
    [14, 4],
    [20, 4],
    [24, 8],
    [29, 6],
    [32, 4],
    [35, 5],
    [38, 2],
]

for name, curve in curves[:1]:
    svg = (
        d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", f"0 0 {width} {height}")
    )

    x = d3.scale_linear([0, x_max], [margin_left, width - margin_right])
    y = d3.scale_linear([0, y_max], [height, 0])

    (
        svg.append("rect")
        .attr("x", margin_left)
        .attr("y", 0)
        .attr("width", width - margin_right - margin_left)
        .attr("height", height)
        .attr("fill", rect_color)
    )

    (
        svg.append("g")
        .attr("class", "xlines")
        .select_all("lines")
        .data(list(range(1, x_max)))
        .join("line")
        .attr("x1", x)
        .attr("y1", y(0))
        .attr("x2", x)
        .attr("y2", y(y_max))
        .attr("stroke", line_color)
    )

    (
        svg.append("g")
        .attr("class", "ylines")
        .select_all("lines")
        .data(list(range(1, y_max)))
        .join("line")
        .attr("x1", x(0))
        .attr("y1", y)
        .attr("x2", x(x_max))
        .attr("y2", y)
        .attr("stroke", line_color)
    )

    (
        svg.append("g")
        .attr("class", "points")
        .select_all("circle")
        .data(points)
        .join("circle")
        .attr("cx", lambda d: x(d[0]))
        .attr("cy", lambda d: y(d[1]))
        .attr("r", 2)
        .attr("stroke", point_color)
        .attr("fill", "none")
    )

    line = d3.line().curve(curve).x(lambda d: x(d[0])).y(lambda d: y(d[1]))

    (
        svg.append("g")
        .attr("class", "curve")
        .append("path")
        .attr("d", line(points))
        .attr("stroke", curve_color)
        .attr("fill", "none")
    )

    with open(f"curve_{name}.svg", "w") as file:
        file.write(str(svg))

k = 4
values = [i / k for i in range(k + 1)]
rect_size = 2

for name, curve, variable_name in parametric_curves[:1]:
    svg = (
        d3.create("svg")
        .attr("width", width)
        .attr("height", legend_height + height)
        .attr("viewBox", f"0 0 {width} {legend_height + height}")
    )

    x = d3.scale_linear([0, x_max], [margin_left, width - margin_right])
    y = d3.scale_linear([0, y_max], [height, 0])

    minmax = d3.extent(values)
    color = d3.scale_linear(minmax, [start_color, "#3d94ff"])
    scaler = d3.scale_linear([0, legend_width], minmax)
    axis_scaler = d3.scale_linear(minmax, [0, legend_width])

    legend = (
        svg.append("g")
        .attr("class", "legend")
    )

    (
        legend.append("text")
        .attr("x", square_length * 0.4)
        .attr("y", 3 * square_length // 5)
        .attr("fill", font_color)
        .text(variable_name)
    )

    (
        legend.append("g")
        .attr("transform", f"translate({square_length * 0.4}, {3 * square_length // 4})")
        .select_all("rect")
        .data(list(range(0, legend_width, 2)))
        .join("rect")
        .attr("x", lambda d: d)
        .attr("y", 0)
        .attr("width", 3)
        .attr("height", square_length * 0.8)
        .attr("fill", lambda d: color(scaler(d)))
    )

    (
        legend.append("g")
        .attr("transform", f"translate({square_length * 0.4}, {3 * square_length // 4})")
        .call(
            d3.axis_bottom(axis_scaler)
            .set_ticks(k)
            .set_tick_size_outer(0)
            .set_tick_size(square_length * 0.8 * 1.2)
        )
        .call(lambda g: g.select(".domain").remove())
        .call(lambda g: g.select_all("line").attr("stroke", font_color))
        .call(lambda g: g.select_all("text").attr("fill", font_color))
    )

    main = (
        svg.append("g")
        .attr("class", "main")
        .attr("transform", f"translate(0, {legend_height})")
    )

    (
        main.append("rect")
        .attr("x", margin_left)
        .attr("y", 0)
        .attr("width", width - margin_right - margin_left)
        .attr("height", height)
        .attr("fill", rect_color)
    )

    (
        main.append("g")
        .attr("class", "xlines")
        .select_all("lines")
        .data(list(range(1, x_max)))
        .join("line")
        .attr("x1", x)
        .attr("y1", y(0))
        .attr("x2", x)
        .attr("y2", y(y_max))
        .attr("stroke", line_color)
    )

    (
        main.append("g")
        .attr("class", "ylines")
        .select_all("lines")
        .data(list(range(1, y_max)))
        .join("line")
        .attr("x1", x(0))
        .attr("y1", y)
        .attr("x2", x(x_max))
        .attr("y2", y)
        .attr("stroke", line_color)
    )

    (
        main.append("g")
        .attr("class", "points")
        .select_all("circle")
        .data(points)
        .join("circle")
        .attr("cx", lambda d: x(d[0]))
        .attr("cy", lambda d: y(d[1]))
        .attr("r", 2)
        .attr("stroke", point_color)
        .attr("fill", "none")
    )

    (
        main.append("g")
        .attr("class", "curve")
        .select_all("path")
        .data(values)
        .join("path")
        .attr("d", lambda d: d3.line().curve(curve(d)).x(lambda d: x(d[0])).y(lambda d: y(d[1]))(points))
        .attr("stroke", lambda d: color(d))
        .attr("fill", "none")
    )

    with open(f"curve_{name}.svg", "w") as file:
        file.write(str(svg))
