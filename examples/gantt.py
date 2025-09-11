# Source : https://observablehq.com/@bensimonds/gantt-chart

import re
from collections import defaultdict, namedtuple
from dataclasses import field, make_dataclass, replace
from datetime import datetime
from functools import reduce
from itertools import accumulate, chain, starmap
from math import exp
from operator import attrgetter, iadd, ior

import polars as pl

import detroit as d3

URL = "https://static.observableusercontent.com/files/30316fb45e0a9f6658d43ea6d1def6cb18e0508b9e8b150cb07e55923bace4a91c4fbcbef26c3875ffea810f2334847bd3a2b757181bde9619fec76fd763c8bf?response-content-disposition=attachment%3Bfilename*%3DUTF-8%27%27archigos.csv"

# Selected countries to display
SELECTED_COUNTRIES = [
    "United States of America",
    "United Kingdom",
    "France",
    "Germany",
    "German Federal Republic",
    "German Democratic Republic",
    "Russia",
    "China",
    "Japan",
]

theme = "light"

# Load data with selected countries
archigos = (
    pl.read_csv(URL)
    .filter(
        reduce(
            ior,
            map(lambda country: pl.col("countryname") == country, SELECTED_COUNTRIES),
        )
    )
    .rename({"": "id"})
    .select(
        pl.all().exclude("startdate", "enddate"),
        pl.col("startdate").str.to_datetime("%Y-%m-%d"),
        pl.col("enddate").str.to_datetime("%Y-%m-%d"),
    )
)

# Prepare objects for convenient syntax
Margin = namedtuple("Margin", ["top", "right", "bottom", "left", "lane_gutter"])
Row = make_dataclass(
    "Row",
    archigos.columns
    + [
        ("row_no", int, field(default=0)),
        ("lane", str, field(default="")),
        ("lane_no", int, field(default=0)),
    ],
)
Reference = namedtuple("Reference", ["start", "label", "color"])

# Color mapping
cm = d3.scale_ordinal(d3.SCHEME_DARK_2).set_domain(
    archigos.group_by("exit")
    .len()
    .sort("len", "exit", descending=True)["exit"]
    .to_list()
)

# Gantt Parameters
width = 1152
key = lambda d: d.obsid
start = lambda d: d.startdate
end = lambda d: d.enddate
color = lambda d: cm(d.exit)
label = lambda d: d.leader
lane = lambda d: d.countryname
title = (
    lambda d: f"{d.countryname} - {d.leader} - {d3.time_format('%Y')(d.startdate)} to {d3.time_format('%Y')(d.enddate)}"
)
x_padding = 0
y_padding = 0.1
round_radius = 4
fixed_row_height = True
row_height = 25
height = 500
label_min_width = 50
show_lane_labels = "left"
show_axis = True

margin = Margin(30, 20, 30, 20, 120)
x_scale = d3.scale_time()
x_domain = None
show_lane_boundaries = True
reference_lines = [
    Reference(datetime(1989, 12, 9), "Berlin Wall Falls", "black"),
    Reference(datetime(1939, 10, 1), "WWII", "black"),
    Reference(datetime(1945, 10, 2), "", "#555"),
    Reference(datetime(1914, 8, 28), "WWI", "black"),
    Reference(datetime(1918, 12, 11), "", "#555"),
]

# Legend Parameters
rect_size = 15
legend_width = width
legend_height = rect_size * 2

# Transform data into list[Row]
data = list(starmap(Row, archigos.iter_rows()))


def assign_rows(data, monotonic=False):
    # Algorithm used to assign bars to lanes.
    slots = []

    def find_slot(slots, bar_start, bar_end):
        # Add some padding to bars to leave space between them
        # Do comparisons in pixel space for cleaner padding.
        bar_start_px = round(x_scale(bar_start))
        bar_end_padded_px = round(x_scale(bar_end) + x_padding)

        for i in range(len(slots)):
            if (slots[i][1] <= bar_start_px) and not monotonic:
                slots[i][1] = bar_end_padded_px
                return slots[i][0]

        # Otherwise add a new slot and return that.
        slots.append([len(slots), bar_end_padded_px])
        return len(slots) - 1

    return [
        replace(d, row_no=find_slot(slots, start(d), end(d)))
        for d in sorted(data, key=start)
    ]


def assign_lanes(data, monotonic=False):
    # Assign rows, but grouped by some keys so that bars are arranged in groups belonging to the same lane.
    groups = defaultdict(list)
    for d in data:
        groups[lane(d)].append(d)

    new_data = []
    row_count = 0
    for i, (lane_name, group_data) in enumerate(groups.items()):
        # For each group assign rows
        group_data = assign_rows(group_data, monotonic)
        for d in group_data:
            # Offset future rows by the maximum row number from this gorup.
            d = replace(d, lane=lane_name, lane_no=i, row_no=row_count + d.row_no)
            new_data.append(d)

        row_count += max(map(lambda d: d.row_no, group_data)) + 1

    return new_data


# Create the svg container
gantt = d3.create("svg").attr("class", "gantt").attr("width", width)
if not fixed_row_height:
    gantt.attr("height", height + legend_height)

# Gantt part

# SVG container (<g>...</g>) for gantt elements
svg = gantt.append("g").attr("transform", f"translate(0, {legend_height})")

# Prepare groups where separated gantt elements will be stored
axis_group = (
    svg.append("g")
    .attr("class", "gantt_group-axis")
    .attr("transform", f"translate(0, {margin.top})")
)
bars_group = svg.append("g").attr("class", "gantt_group-bars")
lanes_group = svg.append("g").attr("class", "gantt__group-lanes")
reference_lines_group = svg.append("g").attr("class", "gantt_group-reference-lines")

# Create the x and y scales
range_min = margin.left + (margin.lane_gutter if show_lane_labels == "left" else 0)
range_max = (
    width - margin.right - (margin.lane_gutter if show_lane_labels == "right" else 0)
)
x = d3.scale_time().set_range([range_min, range_max])
y = d3.scale_band().set_padding(y_padding).set_round(True)


def update_reference_lines(reference_lines):
    def enter_func(enter):
        g = enter.append("g").attr("transform", lambda d: f"translate({x(d.start)}, 0)")
        (
            g.append("path")
            .attr("d", d3.line()([[0, margin.top], [0, height - margin.bottom]]))
            .attr("stroke", lambda d: d.color or "darkgrey")
            .attr("stroke-dasharray", "10,5")
        )
        (
            g.append("text")
            .text(lambda d: d.label or "")
            .attr("x", 5)
            .attr("y", height - margin.bottom + 10)
            .attr("text-anchor", "middle")
            .attr("dominant-baseline", "bottom")
            .attr("font-size", "0.75em")
            .attr("fill", lambda d: d.color or "darkgrey")
        )
        return g

    def update_func(update):
        update.attr("transform", lambda d: f"translate({x(d.start)}, 0)")
        (
            update.select("path")
            .attr("d", d3.line()([[0, margin.top], [0, height - margin.bottom]]))
            .attr("stroke", lambda d: d.color or "darkgrey")
        )
        (
            update.select("text")
            .text(lambda d: d.label or "")
            .attr("y", height - margin.bottom + 10)
            .attr("fill", lambda d: d.color or "darkgrey")
        )
        return update

    def exit_func(exit):
        exit.remove()

    # Update reference lines
    reference_lines_group.select_all("g").data(reference_lines).join(
        enter_func, update_func, exit_func
    )


def update_bars(new_data, duration=0):
    global height
    global row_height
    # Persist data
    data = new_data
    # Create x scales using our raw data. Since we need a scale to map it with assign_lanes
    start = attrgetter("startdate")
    end = attrgetter("enddate")
    x_domain_data = [
        min(chain(map(start, data), map(lambda d: d.start, reference_lines))),
        max(chain(map(end, data), map(lambda d: d.start, reference_lines))),
    ]
    # Update the x domain
    x.set_domain(x_domain or x_domain_data).nice()

    # Map our _data to swim lanes
    data = assign_lanes(data)
    n_rows = max(map(lambda d: d.row_no + 1, data))
    # Calculate the height of our chart if not specified exactly.
    if fixed_row_height:
        height = (row_height * n_rows) + margin.top + margin.bottom
        # svg.attr("height", height)
    else:
        row_height = (height - margin.top - margin.bottom) / n_rows

    if fixed_row_height:
        gantt.attr("height", height + legend_height)

    # Update the y domain
    y_domain = sorted(set(map(lambda d: d.row_no, data)))
    y.set_domain(y_domain).set_range([margin.top, height - margin.bottom])

    def bar_length(d, i, shrink=0.0):
        return max(round(x(end(d)) - x(start(d)) - shrink), 0)

    def enter_func(enter):
        g = enter.append("g")
        # It looks nice if we start in the correct y position and scale out
        (
            g.attr("transform", lambda d: f"translate({width / 2}, {y(d.row_no)})")
            # .transition()
            # .ease(d3.easeExpOut)
            # .duration(duration)
            .attr("transform", lambda d: f"translate({x(start(d))}, {y(d.row_no)})")
        )
        (
            g.append("rect")
            .attr("height", y.get_bandwidth())
            .attr("rx", round_radius)
            .attr("fill", color)
            .attr("stroke", "white")
            .attr("stroke-width", 1)
            # .transition()
            # .duration(duration)
            .attr("width", lambda d: bar_length(d, 0))
        )

        if title is not None:
            g.append("title").text(title)
        if label is not None:
            # Add a clipping path for text
            slugify = lambda text: "-".join(
                filter(None, re.split(r"[^a-z0-9]", str(text).lower()))
            )
            (
                g.append("clipPath")
                .attr("id", lambda d: f"barclip-{slugify(key(d))}")
                .append("rect")
                .attr("width", lambda d, i: bar_length(d, i, 4))
                .attr("height", y.get_bandwidth())
                .attr("rx", round_radius)
            )
            (
                g.append("text")
                .attr("x", max(round_radius * 0.75, 5))
                .attr("y", y.get_bandwidth() / 2)
                .attr("dominant-baseline", "middle")
                .attr("font-size", min([y.get_bandwidth() * 0.6, 16]))
                .attr("fill", "white")
                .attr(
                    "visibility",
                    lambda d: "visible"
                    if bar_length(d, 0) >= label_min_width
                    else "hidden",
                )  # Hide labels on short bars
                .attr("clip-path", lambda d, i: f"url(#barclip-{slugify(d.obsid)}")
                .text(lambda d: label(d))
            )
        return g

    def update_func(update):
        (
            update.attr(
                "transform", lambda d: f"translate({x(d.start)}, {y(d.row_no)})"
            )
            # .transition()
            # .duration(duration)
        )
        (
            update.select("rect")
            # .transition()
            # .duration(duration)
            .attr("fill", color)
            .attr("width", lambda d: bar_length(d))
            .attr("height", y.get_bandwidth())
        )
        if title is not None:
            update.select("title").text(title)

        if label is not None:
            (
                update.select("clipPath")
                .select("rect")
                # .transition()
                # .duration(duration)
                .attr("width", lambda d, i: bar_length(d, i, 4))
                .attr("height", y.get_bandwidth())
            )
            (
                update.select("text")
                .attr("y", y.get_bandwidth() / 2)
                .attr("font-size", min([y.get_bandwidth() * 0.6, 16]))
                .attr(
                    "visibility",
                    lambda d: "visible"
                    if bar_length(d, i) >= label_min_width
                    else "hidden",
                )  # Hide labels on short bars
                .text(lambda d: label(d))
            )
        return update

    def exit_func(exit):
        exit.remove()

    # Update bars
    bars_group.select_all("g").data(data, lambda d: key(d)).join(
        enter_func, update_func, exit_func
    )

    if show_lane_boundaries:
        lanes = {}
        for d in data:
            lanes[d.countryname] = max(d.row_no, lanes.get(d.countryname, 0))
        lanes = list(lanes.items())

        def enter_func(enter):
            g = enter.append("g").attr(
                "transform",
                lambda d: f"translate(0, {y(d[1]) + y.get_step() - y.get_padding_inner() * y.get_step() * 0.5})",
            )
            (
                g.append("path")
                .attr("d", d3.line()([[margin.left, 0], [width - margin.right, 0]]))
                .attr("stroke", "grey")
            )
            if show_lane_labels:
                if show_lane_labels == "left":
                    x_value = margin.left + 5
                elif show_lane_labels == "right":
                    x_value = width - margin.right - 5
                else:
                    x_value = 0
                (
                    g.append("text")
                    .text(lambda d: d[0])
                    .attr("x", x_value)
                    .attr("y", -5)
                    .attr(
                        "text-anchor",
                        "beginning" if show_lane_labels == "left" else "end",
                    )
                    .attr("dominant-baseline", "bottom")
                    .attr("font-size", "0.75em")
                    .attr("fill", "grey")
                )
            return g

        def update_func(update):
            (
                update.attr(
                    "transform",
                    lambda d: f"translate(0, {y(d[1]) + y.get_step() - y.get_padding_inner() * y.get_step() * 0.5})",
                )
            )
            (update.select("text").text(lambda d: d[0]))
            return update

        def exit_func(exit):
            exit.remove()

        lanes_group.select_all("g").data(lanes).join(enter_func, update_func, exit_func)

    # Draw axis
    if show_axis:
        (
            axis_group.call(d3.axis_top(x))
            # .transition()
            # .duration(duration)
        )

    update_reference_lines(reference_lines)


# Generates the gantt elements
update_bars(data)

# Legend part

legend = gantt.append("g").attr(
    "transform", f"translate({rect_size / 2}, {rect_size / 2})"
)

# Labels of the legend
data = cm.get_domain()


# Function to clamp input between 0 and 1
def clamp_total(total):
    def f(x):
        return 1 - exp(-x / total)

    return f


lengths = list(map(len, data))
clamp = clamp_total(max(lengths))
weights = list(map(clamp, lengths))
w_max = max(weights)
weights = [w / w_max for w in weights]  # normalize weights

# Spaces between labels
spaces = [0] + list(
    accumulate(
        map(lambda w: w * 150 + rect_size, weights[:-1]),
        iadd,
    )
)

g = (
    legend.select_all("g")
    .data(data)
    .enter()
    .append("g")
    .attr("transform", lambda _, i: f"translate({spaces[i]}, 0)")
)
(
    g.append("rect")
    .attr("x", 0)
    .attr("y", 0)
    .attr("width", rect_size)
    .attr("height", rect_size)
    .attr("fill", lambda d: cm(d))
    .attr("stroke", "none")
)
(
    g.append("text")
    .attr("x", rect_size + 5)
    .attr("y", rect_size * 0.85)
    .attr("fill", "black")
    .attr("stroke", "none")
    .attr("font-size", "0.75em")
    .text(lambda d: d)
)

if theme == "dark":
    gantt.style("background", "black")
    svg.select_all("text").attr("fill", "white")
    svg.select_all("line").attr("stroke", "white")
    svg.select_all("path").attr("stroke", "white")
    g.select_all("text").attr("fill", "white")

with open(f"{theme}-gantt.svg", "w") as file:
    file.write(str(gantt))
