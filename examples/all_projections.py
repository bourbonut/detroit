# pytopojson has some bugged that I fixed on a fork. The author of "pytopojson"
# is busy and does not have the time to update "pytopojson" unfortunately
# You must install `pytopojson` by running this command:
# pip install git+https://github.com/bourbonut/pytopojson.git

import json
from concurrent.futures import ProcessPoolExecutor

import requests
from pytopojson.feature import Feature
from pytopojson.mesh import Mesh

import detroit as d3

WORLD_URL = "https://cdn.jsdelivr.net/npm/world-atlas@2/land-50m.json"
US_URL = "https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json"

theme = "light"
color = "white" if theme == "dark" else "black"

world = json.loads(requests.get(WORLD_URL).content)
feature = Feature()(world, world["objects"]["land"])
us = json.loads(requests.get(US_URL).content)
nation = Feature()(us, us["objects"]["nation"])

statemesh = Mesh()(
    us,
    obj=us["objects"]["states"],
    filt=lambda a, b: a != b,
)
countymesh = Mesh()(
    us,
    obj=us["objects"]["counties"],
    filt=lambda a, b: a != b and int(int(a["id"]) / 1000) == int(int(b["id"]) / 1000),
)

graticule = d3.geo_graticule_10()
outline = {"type": "Sphere"}


def cylindrical_projection(projection, width, height):
    return (
        projection.rotate([0, 0])
        .fit_extent([[1, 1], [width - 1, height - 1]], {"type": "Sphere"})
        .set_precision(0.2)
    )


def azimuthal_projection1(projection, width, height):
    return (
        projection.rotate([110, -40])
        .fit_extent([[1, 1], [width - 1, height - 1]], {"type": "Sphere"})
        .set_precision(0.2)
    )


def azimuthal_projection2(projection, width, height):
    return (
        projection.scale(width / 6)
        .translate([width / 2, height / 2])
        .set_clip_angle(74 - 1e-4)
        .set_clip_extent([[-1, -1], [width + 1, height + 1]])
        .set_precision(0.2)
    )


def azimuthal_projection3(projection, width, height):
    return (
        projection.rotate([110, -40])
        .fit_extent([[1, 1], [width - 1, height - 1]], {"type": "Sphere"})
        .set_precision(0.2)
    )


def azimuthal_projection4(projection, width, height):
    return (
        projection.scale(width / 4)
        .translate([width / 2, height / 2])
        .rotate([-27, 0])
        .set_clip_angle(135 - 1e-4)
        .set_clip_extent([[-1, -1], [width + 1, height + 1]])
        .set_precision(0.2)
    )


def conic_projection1(projection, width, height):
    return (
        projection.parallels([35, 65])
        .rotate([-20, 0])
        .scale(width * 0.55)
        .set_center([0, 52])
        .translate([width / 2, height / 2])
        .set_clip_extent([[-1, -1], [width + 1, height + 1]])
        .set_precision(0.2)
    )


def conic_projection2(projection, width, height):
    return projection.scale(1300 / 975 * width * 0.8).translate([width / 2, height / 2])


width = 688
projections = [
    (
        "equirectangular",
        d3.geo_equirectangular(),
        width / 2,
        cylindrical_projection,
        True,
    ),
    ("mercator", d3.geo_mercator(), width, cylindrical_projection, True),
    (
        "transverse_mercator",
        d3.geo_transverse_mercator(),
        width,
        cylindrical_projection,
        True,
    ),
    ("equal_earth", d3.geo_equal_earth(), width * 0.49, cylindrical_projection, True),
    (
        "natural_earth_1",
        d3.geo_natural_earth_1(),
        width * 0.5,
        cylindrical_projection,
        True,
    ),
    (
        "azimuthal_equal_area",
        d3.geo_azimuthal_equal_area(),
        400,
        azimuthal_projection1,
        True,
    ),
    (
        "azimuthal_equidistant",
        d3.geo_azimuthal_equidistant(),
        400,
        azimuthal_projection1,
        True,
    ),
    ("gnomonic", d3.geo_gnomonic(), 400, azimuthal_projection2, True),
    ("orthographic", d3.geo_orthographic(), 400, azimuthal_projection3, True),
    ("stereographic", d3.geo_stereographic(), 400, azimuthal_projection4, True),
    ("conic_conformal", d3.geo_conic_conformal(), 400, conic_projection1, True),
    ("conic_equal_area", d3.geo_conic_equal_area(), 400, conic_projection1, True),
    ("conic_equidistant", d3.geo_conic_equidistant(), 400, conic_projection1, True),
    ("albers", d3.geo_albers(), 400, conic_projection2, False),
    ("albers_usa", d3.geo_albers_usa(), 400, conic_projection2, False),
]


def generate_world(name, projection, height, transform):
    projection = transform(projection, width, height)
    path = d3.geo_path(projection)

    svg = (
        d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", f"0 0 {width} {height}")
    )
    (
        svg.append("path")
        .attr("name", "graticule")
        .attr("d", path(graticule))
        .attr("stroke", color)
        .attr("stroke-opacity", 0.2)
        .attr("fill", "none")
    )
    (
        svg.append("path")
        .attr("name", "feature")
        .attr("d", path(feature))
        .attr("fill", color)
    )
    (
        svg.append("path")
        .attr("name", "outline")
        .attr("d", path(outline))
        .attr("stroke", color)
        .attr("fill", "none")
    )

    with open(f"{theme}-projection-{name}.svg", "w") as file:
        file.write(str(svg))


def generate_us(name, projection, height, transform):
    projection = transform(projection, width, height)
    path = d3.geo_path(projection)

    svg = (
        d3.create("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("viewBox", f"0 0 {width} {height}")
    )
    (
        svg.append("path")
        .attr("name", "nation")
        .attr("d", path(nation))
        .attr("stroke", color)
        .attr("fill", "none")
    )
    (
        svg.append("path")
        .attr("name", "statemesh")
        .attr("d", path(statemesh))
        .attr("fill", "none")
        .attr("stroke", color)
        .attr("stroke-width", 0.5)
    )
    (
        svg.append("path")
        .attr("name", "countymesh")
        .attr("d", path(countymesh))
        .attr("stroke", color)
        .attr("stroke-width", 0.5)
        .attr("stroke-opacity", 0.5)
        .attr("fill", "none")
    )

    with open(f"{theme}-projection-{name}.svg", "w") as file:
        file.write(str(svg))


def generate_svg(name, projection, height, transform, is_world):
    if is_world:
        generate_world(name, projection, height, transform)
    else:
        generate_us(name, projection, height, transform)


with ProcessPoolExecutor() as pool:
    for _ in pool.map(generate_svg, *zip(*projections)):
        pass
