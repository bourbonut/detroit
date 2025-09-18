import detroit as d3
from operator import methodcaller

width = 810
margin_left = 5
margin_right = 5
x_max = 40
y_max = 12
square_length = (width - margin_left - margin_right) / x_max
height = y_max * square_length
legend_height = int(square_length * 3)
legend_width = int(square_length * 15)

theme = "light"

rect_color = "#2b2b2e"
line_color = "#202020"
font_color = ease_color = point_color = "white"
start_color = "#999999"

if theme == "light":
    rect_color = "#d4d4d1"
    line_color = "#f8f8f8"
    font_color = ease_color = point_color = "black"
    start_color = "#303030"

easing_functions = [
    ("bounce_in", d3.ease_bounce_in),
    ("bounce_in_out", d3.ease_bounce_in_out),
    ("bounce_out", d3.ease_bounce_out),
    ("circle_in", d3.ease_circle_in),
    ("circle_in_out", d3.ease_circle_in_out),
    ("circle_out", d3.ease_circle_out),
    ("cubic_in", d3.ease_cubic_in),
    ("cubic_in_out", d3.ease_cubic_in_out),
    ("cubic_out", d3.ease_cubic_out),
    ("exp_in", d3.ease_exp_in),
    ("exp_in_out", d3.ease_exp_in_out),
    ("exp_out", d3.ease_exp_out),
    ("linear", d3.ease_linear),
    ("quad_in", d3.ease_quad_in),
    ("quad_in_out", d3.ease_quad_in_out),
    ("quad_out", d3.ease_quad_out),
    ("sin_in", d3.ease_sin_in),
    ("sin_in_out", d3.ease_sin_in_out),
    ("sin_out", d3.ease_sin_out),
]

parametric_easing_functions = [
    ("back_in", d3.ease_back_in, "overshoot"),
    ("back_in_out", d3.ease_back_in_out, "overshoot"),
    ("back_out", d3.ease_back_out, "overshoot"),
    ("elastic_in", d3.ease_elastic_in, "amplitude"),
    ("elastic_in_out", d3.ease_elastic_in_out, "amplitude"),
    ("elastic_out", d3.ease_elastic_out, "amplitude"),
    ("poly_in", d3.ease_poly_in, "exponent"),
    ("poly_in_out", d3.ease_poly_in_out, "exponent"),
    ("poly_out", d3.ease_poly_out, "exponent"),
]

# Easing functions
step = 250

for name, easing_function in easing_functions:
    points = [
        [i / step * x_max, easing_function(i / step) * y_max] for i in range(step + 1)
    ]
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

    line = d3.line().x(lambda d: x(d[0])).y(lambda d: y(d[1]))

    (
        svg.append("g")
        .attr("class", "ease")
        .append("path")
        .attr("d", line(points))
        .attr("stroke", ease_color)
        .attr("fill", "none")
    )

    with open(f"{theme}_ease_{name}.svg", "w") as file:
        file.write(str(svg))

# Parametric easing functions

k = 5
rect_size = 2

for name, easing_function, variable_name in parametric_easing_functions:
    match variable_name:
        case "overshoot":
            values = [(i / k) * 2.5 + 0.5 for i in range(k + 1)]
        case "amplitude":
            values = [(i / k) * 0.5 + 1.0 for i in range(k + 1)]
        case "exponent":
            values = [(i / k) * 3.6 + 0.4 for i in range(k + 1)]

    match name:
        case "elastic_in":
            offset_height = 110
        case "elastic_out" | "elastic_in_out":
            offset_height = 60
        case "back_in":
            offset_height = 70
        case "back_in_out":
            offset_height = 40
        case _:
            offset_height = 0

    legend_offset_height = 45 if name == "elastic_out" else 0
    local_legend_height = legend_height + legend_offset_height
    svg = (
        d3.create("svg")
        .attr("width", width)
        .attr("height", local_legend_height + height + offset_height)
        .attr("viewBox", f"0 0 {width} {local_legend_height + height + offset_height}")
    )

    x = d3.scale_linear([0, x_max], [margin_left, width - margin_right])
    y = d3.scale_linear([0, y_max], [height, 0])

    minmax = d3.extent(values)
    color = d3.scale_linear(minmax, [start_color, "#3d94ff"])
    scaler = d3.scale_linear([0, legend_width], minmax)
    axis_scaler = d3.scale_linear(minmax, [0, legend_width])

    legend = svg.append("g").attr("class", "legend")
    if legend_offset_height:
        legend.attr("transform", f"translate(0, {legend_offset_height})")

    (
        legend.append("text")
        .attr("x", square_length * 0.4)
        .attr("y", 3 * square_length // 5)
        .attr("fill", font_color)
        .text(variable_name)
    )

    (
        legend.append("g")
        .attr(
            "transform", f"translate({square_length * 0.4}, {3 * square_length // 4})"
        )
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
        .attr(
            "transform", f"translate({square_length * 0.4}, {3 * square_length // 4})"
        )
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
        .attr("transform", f"translate(0, {local_legend_height})")
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

    line = d3.line().x(lambda d: x(d[0])).y(lambda d: y(d[1]))

    def points(d):
        f = methodcaller(variable_name, d)(easing_function)
        return [[i / step * x_max, f(i / step) * y_max] for i in range(step + 1)]

    (
        main.append("g")
        .attr("class", "ease")
        .select_all("path")
        .data(values)
        .join("path")
        .attr("d", lambda d: line(points(d)))
        .attr("stroke", lambda d: color(d))
        .attr("fill", "none")
    )

    with open(f"{theme}_ease_{name}.svg", "w") as file:
        file.write(str(svg))
