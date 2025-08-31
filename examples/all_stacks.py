import detroit as d3
import polars as pl

URL = "https://raw.githubusercontent.com/d3/d3/refs/heads/main/docs/public/data/riaa-us-revenue.csv"

theme = "light"
line_color = "black" if theme == "light" else "white"

riaa = pl.read_csv(URL).select(
    pl.col("format"),
    pl.col("group"),
    pl.col("year").str.to_datetime("%Y-%m-%d"),
    pl.col("revenue") / 1000,
)

data = riaa.to_dicts()
keys = riaa["format"].unique().sort().to_list()
indexed_data = d3.index(data, lambda d: d["year"], lambda d: d["format"])
mapping_group = {key: list(group)[0] for key, group in d3.group(data, lambda d: d["format"], lambda d: d["group"]).items()}

width = 628
height = 200
margin_top = 20
margin_right = 20
margin_bottom = 20
margin_left = 40

def value_default(d, key, i, data):
    return data[d][key]["revenue"]

def value_diverging(d, key, i, data):
    d = data[d][key]
    revenue = d["revenue"]
    group = d["group"]
    return (-1 if group == "Disc" else 1) * revenue

def reverse_appearance(series):
    return d3.stack_order_appearance(series)[::-1]

def generate_svg(title, order, offset):
    value = value_diverging if "diverging" in title else value_default
    stack = (
        d3.stack()
        .set_order(order)
        .set_offset(offset)
        .set_keys(keys)
        .set_value(value)
    )
    series = stack(indexed_data)

    # Prepare the scales for positional and color encodings.
    x = (
        d3.scale_time()
        .set_domain(d3.extent(data, lambda d: d["year"]))
        .set_range([margin_left, width - margin_right])
    )

    y = (
        d3.scale_linear()
        .set_domain(
            [
                min(map(lambda serie: min(map(lambda d: d[0], serie)), series)),
                max(map(lambda serie: max(map(lambda d: d[1], serie)), series)),
            ]
        )
        .set_range_round([height - margin_bottom, margin_top])
    )

    color = (
        d3.scale_ordinal()
        .set_domain(riaa["group"].unique().sort().to_list())
        .set_range(d3.SCHEME_TABLEAU_10)
    )

    # Construct an area shape.
    area = (
        d3.area()
        .x(lambda d: x(d.data.timestamp()))
        .y0(lambda d: y(d[0]))
        .y1(lambda d: y(d[1]))
    )

    # Create the SVG container.
    svg = (
        d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("view_box", f"0 0 {width} {height}")
        .attr("style", "max-width:100%;height:auto;")
    )

    # Append the x axis, and remove the domain line.
    (
        svg.append("g")
        .attr("transform", f"translate(0, {height - margin_bottom})")
        .call(d3.axis_bottom(x).set_tick_size_outer(0))
        .call(lambda g: g.select(".domain").remove())
    )

    is_expand = "expand" in title

    # Add the y axis, remove the domain line, add grid lines and a label.
    (
        svg.append("g")
        .attr("transform", f"translate({margin_left},0)")
        .call(
            d3.axis_left(y).set_ticks(*((6, "%") if is_expand else (5,)))
        )
        .call(lambda g: g.select(".domain").remove())
        .call(
            lambda g: g.select_all(".tick line")
            .clone()
            .attr("x2", width - margin_left - margin_right)
            .attr("stroke-opacity", 0.2)
        )
        .call(
            lambda g: g.append("text")
            .attr("x", -margin_left)
            .attr("y", 10)
            .attr("fill", "currentColor")
            .attr("text-anchor", "start")
            .text("↑ Annual revenue (billions)")
        )
    )

    # Append a path for each series.
    (
        svg.append("g")
        .select_all()
        .data(series)
        .join("path")
        .attr("fill", lambda d: color(mapping_group[d.key]))
        .attr("d", area)
        .append("title")
        .text(lambda d: d.key)
    )

    if theme == "dark":
        svg.select_all("path.domain").attr("stroke", "white")
        svg.select_all("g.tick line").attr("stroke", "white")
        svg.select_all("g.tick text").attr("fill", "white").attr("stroke", "none")
        svg.select_all("text").attr("fill", "white").attr("stroke", "none")

    with open(f"{theme}-{title}.svg", "w") as file:
        file.write(str(svg))

options = [
    ("stack-order-appearance", d3.stack_order_appearance, d3.stack_offset_none),
    ("stack-order-ascending", d3.stack_order_ascending, d3.stack_offset_none),
    ("stack-order-descending", d3.stack_order_descending, d3.stack_offset_none),
    ("stack-order-inside-out", d3.stack_order_inside_out, d3.stack_offset_wiggle),
    ("stack-order-none", d3.stack_order_none, d3.stack_offset_none),
    ("stack-order-reverse", d3.stack_order_reverse, d3.stack_offset_none),
    ("stack-offset-expand", reverse_appearance, d3.stack_offset_expand),
    ("stack-offset-diverging", d3.stack_order_appearance, d3.stack_offset_diverging),
    ("stack-offset-none", d3.stack_order_appearance, d3.stack_offset_none),
    ("stack-offset-silhouette", d3.stack_order_appearance, d3.stack_offset_silhouette),
    ("stack-offset-wiggle", d3.stack_order_inside_out, d3.stack_offset_wiggle),
]

for title, order, offset in options:
    generate_svg(title, order=order, offset=offset)
