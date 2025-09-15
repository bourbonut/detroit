# Source: https://observablehq.com/@d3/chord-diagram/2
import detroit as d3
from itertools import chain
from math import pi, degrees

theme = "light"
main_color = "#000000" if theme == "light" else "#ffffff"
stroke_color = "white" if theme == "light" else "black"

# https://docs.python.org/3/library/itertools.html#itertools-recipes
def flatten(list_of_lists):
    return chain.from_iterable(list_of_lists)

# Declare data
matrix = [
    [11975, 5871, 8916, 2868],
    [1951, 10048, 2060, 6171],
    [8010, 16145, 8090, 8045],
    [1013, 990, 940, 6907],
]
names = ["black", "blond", "brown", "red"]
colors = [main_color, "#ffdd89", "#957244", "#f26223"]


def group_ticks(d, step):
    k = (d.end_angle - d.start_angle) / d.value
    return [
        {"value": value, "angle": value * k + d.start_angle}
        for value in range(0, d.value, step)
    ]


# Declare the chart dimensions.
width = 640
height = width
outer_radius = min(width, height) * 0.5 - 30
inner_radius = outer_radius - 20

sum_value = sum(flatten(matrix))
tick_step = d3.tick_step(0, sum_value, 100)
tick_step_major = d3.tick_step(0, sum_value, 20)
format_value = d3.format_prefix(",.0", tick_step)

# Create chord, arc and ribbon generators
chord = (
    d3.chord()
    .set_pad_angle(20 / inner_radius)
    .set_sort_subgroups(lambda a, b: -1 if b < a else (1 if b > a else 0))
)

arc = d3.arc().set_inner_radius(inner_radius).set_outer_radius(outer_radius)

ribbon = d3.ribbon().set_radius(inner_radius)

# Create the SVG container.
svg = (
    d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", ", ".join(map(str, (-width / 2, -height / 2, width, height))))
    .attr("style", "max-width: 100%; height: auto; font: 10px sans-serif;")
)

# Compute chord values.
chords = chord(matrix)

# Add chord groups.
group = svg.append("g").select_all().data(chords.groups).join("g")

(
    group.append("path")
    .attr("fill", lambda d: colors[d.index])
    .attr("d", arc)
    .append("title")
    .text(lambda d: f"{d.value:,} {names[d.index]}")
)

# Add group ticks.
group_tick = (
    group.append("g")
    .select_all()
    .data(lambda _, d: group_ticks(d, tick_step))
    .join("g")
    .attr(
        "transform",
        lambda d: f"rotate({degrees(d["angle"]) - 90}) translate({outer_radius},0)",
    )
)

group_tick.append("line").attr("stroke", main_color).attr("x2", 6)

(
    group_tick.filter(lambda d: d["value"] % tick_step_major == 0)
    .append("text")
    .attr("x", 8)
    .attr("dy", ".35em")
    .attr(
        "transform", lambda d: "rotate(180) translate(-16)" if d["angle"] > pi else "none"
    )
    .attr("text-anchor", lambda d: "end" if d["angle"] > pi else "none")
    .attr("fill", main_color)
    .text(lambda d: format_value(d["value"]))
)


# Add chord values in the SVG containers.
def alt(d):
    if d.source.index != d.target.index:
        value = f"\n{d.target.value:,} {names[d.target.index]} → {names[d.source.index]}"
    else:
        value = ""
    return f"{d.source.value:,} {names[d.source.index]} → {names[d.target.index]}{value}"


(
    svg.append("g")
    .attr("fill-opacity", 0.7)
    .select_all()
    .data(chords)
    .join("path")
    .attr("d", ribbon)
    .attr("fill", lambda d: colors[d.target.index])
    .attr("stroke", stroke_color)
    .append("title")
    .text(alt)
)

with open(f"{theme}-chord.svg", "w") as file:
    file.write(str(svg))
