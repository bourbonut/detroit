#   / \     This example is not working currently
#  / O \    There are some missing features which would be added in future
# /_____\

from dataclasses import make_dataclass, field, replace
import detroit as d3
import polars as pl
from operator import attrgetter
from collections import namedtuple
from itertools import starmap

URL = "https://static.observableusercontent.com/files/30316fb45e0a9f6658d43ea6d1def6cb18e0508b9e8b150cb07e55923bace4a91c4fbcbef26c3875ffea810f2334847bd3a2b757181bde9619fec76fd763c8bf?response-content-disposition=attachment%3Bfilename*%3DUTF-8%27%27archigos.csv"
Margin = namedtuple("Margin", ["top", "right", "bottom", "left", "lane_gutter"])

archigos = (
    pl.read_csv(URL)
    .filter(pl.col("countryname") == "United States of America")
    .rename({"": "id"})
    .select(
        pl.all().exclude("startdate", "enddate"),
        pl.col("startdate").str.to_datetime("%Y-%m-%d"),
        pl.col("enddate").str.to_datetime("%Y-%m-%d"),
    )
)

Row = make_dataclass(
    "Row",
    archigos.columns
    + [
        ("row_no", int, field(default=0)),
        ("lane", str, field(default="")),
        ("lane_no", int, field(default=0)),
    ],
)

data = list(starmap(Row, archigos.iter_rows()))

show_lane_labels = "right"

width = 600
height = 500
margin = Margin(30, 20, 30, 20, 120)

reference_lines = []
fixed_row_height = False
x_domain = None
x_padding = 5
round_radius = 4


def color(d):
    return d


def title(d):
    return f"{d.countryname} - {d.leader} - {d3.time_format('%Y')(d.startdate)} to {d3.time_format('%Y')(d.enddate)}"


def assign_rows(data, monotonic=False):
    # Algorithm used to assign bars to lanes.
    slots = []

    def find_slot(slots, bar_start, bar_end):
        # Add some padding to bars to leave space between them
        # Do comparisons in pixel space for cleaner padding.
        bar_start_px = round(d3.scale_time()(bar_start))
        bar_end_padded_px = round(d3.scale_time()(bar_end) + x_padding)

        for i in range(len(slots)):
            if (slots[i][1] <= bar_start_px) and not monotonic:
                slots[i][1] = bar_end_padded_px
                return slots[i][0]

        # Otherwise add a new slot and return that.
        slots.append([len(slots), bar_end_padded_px])
        return len(slots) - 1

    def update(row):
        row.row_no = find_slot(slots, row.startdate, row.enddate)
        return row

    return list(map(update, sorted(data, key=lambda item: item.startdate)))


def assign_lanes(data, monotonic=False):
    # Assign rows, but grouped by some keys so that bars are arranged in groups belonging to the same lane.
    groups = {}
    for row in data:
        group_data = groups.setdefault(row.countryname, [])
        group_data.append(row)

    new_data = []
    row_count = 0
    for i, lane_name in enumerate(groups):
        group_data = groups[lane_name]
        # For each group assign rows
        group_data = assign_rows(group_data, monotonic)
        for d in group_data:
            # Offset future rows by the maximum row number from this gorup.
            row = replace(row, lane=lane_name, lane_no=i, row_no=row_count + d.row_no)
            new_data.append(row)

        row_count += max(map(lambda d: d.row_no, group_data)) + 1

    return new_data


svg = (
    d3.create("svg").attr("class", "gantt").attr("width", width).attr("height", height)
)

axis_group = (
    svg.append("g")
    .attr("class", "gantt_group-axis")
    .attr("transform", f"translate(0, {margin.top})")
)
bars_group = svg.append("g").attr("class", "gantt_group-bars")
lanes_group = svg.append("g").attr("class", "gantt__group-lanes")
reference_lines_group = svg.append("g").attr("class", "gantt_group-reference-lines")

x = d3.scale_time().set_range(
    [
        margin.left + (margin.lane_gutter if show_lane_labels == "left" else 0),
        width
        - margin.right
        - (margin.lane_gutter if show_lane_labels == "right" else 0),
    ]
)
y = d3.scale_band().set_padding(0.2).set_round(True)


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


def update_bars(new_data, height=height, duration=0):
    # Persist data|
    data = new_data
    # Create x scales using our raw data. Since we need a scale to map it with assignLanes
    start = attrgetter("startdate")
    end = attrgetter("enddate")
    x_domain_data = [
        min(list(map(start, data)) + list(map(start, reference_lines))),
        max(list(map(end, data)) + list(map(end, reference_lines))),
    ]
    # Update the x domain
    x.set_domain(x_domain or x_domain_data).nice()

    # Map our _data to swim lanes
    data = assign_lanes(data)
    n_rows = max(map(lambda d: d.row_no + 1, data))
    # Calculate the height of our chart if not specified exactly.
    if fixed_row_height:
        height = (height * n_rows) + margin.top + margin.bottom
        svg.attr("height", height)
    else:
        height = (height - margin.top - margin.bottom) / n_rows

    # Update the yDomain
    y_domain = sorted(set(map(lambda d: d.row_no, data)))
    y.set_domain(y_domain).set_range([margin.top, height - margin.bottom])

    def bar_length(d, i, shrink=0.0):
        return max(round(x(d.enddate) - x(d.startdate) - shrink), 0)

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
            .attr("height", y.bandwidth)
            .attr("rx", round_radius)
            .attr("fill", color)
            .attr("stroke", "white")
            .attr("stroke-width", 1)
            # .transition()
            # .duration(duration)
            .attr("width", lambda d: bar_length(d, 0))
        )

        g.append("title").text(title)
        # Add a clipping path for text
        # slugify = lambda text: str(text).lower().split([^a-z0-9]).filter(d => d).join('-')
        (
            g.append("clipPath")
            # .attr('id', lambda d, i: f"barclip-{slugify(d.obsid)}")
            .append("rect")
            .attr("width", lambda d, i: bar_length(d, i, 4))
            .attr("height", y.bandwidth)
            .attr("rx", round_radius)
        )
        (
            g.append("text")
            .attr("x", max(round_radius * 0.75, 5))
            .attr("y", y.bandwidth / 2)
            .attr("dominant-baseline", "middle")
            .attr("font-size", min([y.bandwidth * 0.6, 16]))
            .attr("fill", "white")
            # .attr('visibility', lambda d: 'visible' if barLength(d) >= label_min_width else 'hidden') # Hide labels on short bars
            # .attr('clip-path', lambda d, i: f"url(#barclip-{slugify(d.obsid)}")
            .text(lambda d: d.leader)
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
            .attr("height", y.bandwidth)
        )
        update.select("title").text(title)
        (
            update.select("clipPath")
            .select("rect")
            # .transition()
            # .duration(duration)
            .attr("width", lambda d, i: bar_length(d, i, 4))
            .attr("height", y.bandwidth)
        )
        (
            update.select("text")
            .attr("y", y.bandwidth / 2)
            .attr("font-size", min([y.bandwidth * 0.6, 16]))
            # .attr('visibility', lambda d: 'visible' if barLength(d) >= label_min_width else 'hidden') # Hide labels on short bars
            .text(lambda d: d.leader)
        )
        return update

    def exit_func(exit):
        exit.remove()

    # Update bars
    bars_group.select_all("g").data(data, lambda d, i: i).join(
        enter_func, update_func, exit_func
    )

    # Draw axis
    (
        axis_group.call(d3.axis_top(x))
        # .transition()
        # .duration(duration)
    )

    # IndexError: list index out of range
    # update_reference_lines(reference_lines)


update_bars(data)

with open("gantt.svg", "w") as file:
    file.write(str(svg))
