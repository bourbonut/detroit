from math import pi

import pytest

import detroit as d3


@pytest.fixture
def equirectangular():
    return d3.geo_equirectangular().scale(900 / pi).set_precision(0)


def path(projection, obj):
    return d3.geo_path().set_projection(projection)(obj)


def test_string_1(equirectangular):
    path(
        equirectangular, {"type": "Point", "coordinates": [-63, 18]}
    ) == "M165,160m0,4.500000a4.500000,4.500000 0 1,1 0,-9a4.500000,4.500000 0 1,1 0,9z"


def test_string_2(equirectangular):
    d3.geo_path().set_projection(equirectangular).set_point_radius(10)(
        {"type": "Point", "coordinates": [-63, 18]}
    ) == "M165,160m0,10a10,10 0 1,1 0,-20a10,10 0 1,1 0,20z"


def test_string_3(equirectangular):
    path(
        equirectangular,
        {"type": "MultiPoint", "coordinates": [[-63, 18], [-62, 18], [-62, 17]]},
    ) == "M165,160m0,4.500000a4.500000,4.500000 0 1,1 0,-9a4.500000,4.500000 0 1,1 0,9zM170,160m0,4.500000a4.500000,4.500000 0 1,1 0,-9a4.500000,4.500000 0 1,1 0,9zM170,165m0,4.500000a4.500000,4.500000 0 1,1 0,-9a4.500000,4.500000 0 1,1 0,9z"


def test_string_4(equirectangular):
    path(
        equirectangular,
        {"type": "LineString", "coordinates": [[-63, 18], [-62, 18], [-62, 17]]},
    ) == "M165,160L170,160L170,165"


def test_string_5(equirectangular):
    path(
        equirectangular,
        {
            "type": "Polygon",
            "coordinates": [[[-63, 18], [-62, 18], [-62, 17], [-63, 18]]],
        },
    ) == "M165,160L170,160L170,165Z"


def test_string_6(equirectangular):
    path(
        equirectangular,
        {
            "type": "GeometryCollection",
            "geometries": [
                {
                    "type": "Polygon",
                    "coordinates": [[[-63, 18], [-62, 18], [-62, 17], [-63, 18]]],
                }
            ],
        },
    ) == "M165,160L170,160L170,165Z"


def test_string_7(equirectangular):
    path(
        equirectangular,
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[-63, 18], [-62, 18], [-62, 17], [-63, 18]]],
            },
        },
    ) == "M165,160L170,160L170,165Z"


def test_string_8(equirectangular):
    path(
        equirectangular,
        {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[[-63, 18], [-62, 18], [-62, 17], [-63, 18]]],
                    },
                }
            ],
        },
    ) == "M165,160L170,160L170,165Z"


def test_string_9(equirectangular):
    path = d3.geo_path().set_projection(equirectangular)
    path(
        {"type": "LineString", "coordinates": [[-63, 18], [-62, 18], [-62, 17]]}
    ) == "M165,160L170,160L170,165"
    path(
        {"type": "Point", "coordinates": [-63, 18]}
    ) == "M165,160m0,4.500000a4.500000,4.500000 0 1,1 0,-9a4.500000,4.500000 0 1,1 0,9z"
