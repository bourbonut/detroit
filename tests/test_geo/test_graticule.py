import detroit as d3


def test_graticule_1():
    g = d3.geo_graticule()
    assert g.get_precision() == 2.5
    g.set_precision(999)
    assert g.get_precision() == 999


def test_graticule_2():
    g = d3.geo_graticule().set_extent([[-90, -45], [90, 45]])
    assert g.get_extent_minor() == [[-90, -45], [90, 45]]
    assert g.get_extent_major() == [[-90, -45], [90, 45]]

    g_reversed = d3.geo_graticule().set_extent([[90, 45], [-90, -45]])
    assert g_reversed.get_extent_minor() == [[-90, -45], [90, 45]]
    assert g_reversed.get_extent_major() == [[-90, -45], [90, 45]]


def test_graticule_3():
    g = d3.geo_graticule().set_extent_minor([[-90, -45], [90, 45]])
    assert g.get_extent() == [[-90, -45], [90, 45]]


def test_graticule_4():
    e = d3.geo_graticule().get_extent_major()
    assert e[0][0] == -180
    assert e[1][0] == +180


def test_graticule_5():
    e = d3.geo_graticule().get_extent_major()
    assert e[0][1] == -90 + 1e-6
    assert e[1][1] == +90 - 1e-6


def test_graticule_6():
    g = d3.geo_graticule().set_extent_major([[-90, -45], [+90, +45]])
    e = g.get_extent_major()
    assert e[0][0] == -90
    assert e[0][1] == -45
    assert e[1][0] == +90
    assert e[1][1] == +45


def test_graticule_7():
    e = d3.geo_graticule().get_extent_minor()
    assert e[0][0] == -180
    assert e[1][0] == +180


def test_graticule_8():
    e = d3.geo_graticule().get_extent_minor()
    assert e[0][1] == -80 - 1e-6
    assert e[1][1] == +80 + 1e-6


def test_graticule_9():
    g = d3.geo_graticule().set_extent_minor([[-90, -45], [+90, +45]])
    e = g.get_extent_minor()
    assert e[0][0] == -90
    assert e[0][1] == -45
    assert e[1][0] == +90
    assert e[1][1] == +45


def test_graticule_10():
    g = d3.geo_graticule().set_step([22.5, 22.5])
    assert g.get_step_minor() == [22.5, 22.5]
    assert g.get_step_major() == [22.5, 22.5]


def test_graticule_11():
    g = d3.geo_graticule().set_step_minor([22.5, 22.5])
    assert g.get_step() == [22.5, 22.5]


def test_graticule_12():
    assert d3.geo_graticule().get_step_minor() == [10, 10]


def test_graticule_13():
    g = d3.geo_graticule().set_step_minor([45, 11.25])
    s = g.get_step_minor()
    assert s[0] == 45
    assert s[1] == 11.25


def test_graticule_14():
    assert d3.geo_graticule().get_step_major() == [90, 360]


def test_graticule_15():
    g = d3.geo_graticule().set_step_major([45, 11.25])
    s = g.get_step_major()
    assert s[0] == 45
    assert s[1] == 11.25


def test_graticule_16():
    lines = d3.geo_graticule().lines()
    lines = sorted(
        filter(
            lambda line: line["coordinates"][0][0] == line["coordinates"][1][0],
            lines,
        ),
        key=lambda line: line["coordinates"][0][0],
    )
    assert lines[0]["coordinates"][0][0] == -180
    assert lines[len(lines) - 1]["coordinates"][0][0] == +170


def test_graticule_17():
    lines = d3.geo_graticule().lines()
    lines = sorted(
        filter(
            lambda line: line["coordinates"][0][1] == line["coordinates"][1][1],
            lines,
        ),
        key=lambda line: line["coordinates"][0][1],
    )
    assert lines[0]["coordinates"][0][1] == -80
    assert lines[len(lines) - 1]["coordinates"][0][1] == +80


def test_graticule_18():
    lines = d3.geo_graticule().lines()
    lines = filter(
        lambda line: line["coordinates"][0][0] == line["coordinates"][1][0],
        lines,
    )
    lines = filter(
        lambda line: abs(line["coordinates"][0][0] % 90) > 1e-6,
        lines,
    )
    for line in lines:
        assert d3.extent(line["coordinates"], lambda p: p[1]) == [
            -80 - 1e-6,
            +80 + 1e-6,
        ]


def test_graticule_19():
    lines = d3.geo_graticule().lines()
    lines = filter(
        lambda line: line["coordinates"][0][0] == line["coordinates"][1][0],
        lines,
    )
    lines = filter(
        lambda line: abs(line["coordinates"][0][0] % 90) < 1e-6,
        lines,
    )
    for line in lines:
        assert d3.extent(line["coordinates"], lambda p: p[1]) == [
            -90 + 1e-6,
            +90 - 1e-6,
        ]


def test_graticule_20():
    lines = d3.geo_graticule().lines()
    lines = filter(
        lambda line: line["coordinates"][0][1] == line["coordinates"][1][1],
        lines,
    )
    for line in lines:
        assert d3.extent(line["coordinates"], lambda p: p[0]) == [-180, +180]


def test_graticule_21():
    assert (
        d3.geo_graticule()
        .set_extent([[-90, -45], [90, 45]])
        .set_step([45, 45])
        .set_precision(3)
        .lines()
    ) == [
        {"type": "LineString", "coordinates": [[-90, -45], [-90, 45]]},
        {"type": "LineString", "coordinates": [[-45, -45], [-45, 45]]},
        {"type": "LineString", "coordinates": [[0, -45], [0, 45]]},
        {"type": "LineString", "coordinates": [[45, -45], [45, 45]]},
        {
            "type": "LineString",
            "coordinates": [
                [-90, -45],
                [-87, -45],
                [-84, -45],
                [-81, -45],
                [-78, -45],
                [-75, -45],
                [-72, -45],
                [-69, -45],
                [-66, -45],
                [-63, -45],
                [-60, -45],
                [-57, -45],
                [-54, -45],
                [-51, -45],
                [-48, -45],
                [-45, -45],
                [-42, -45],
                [-39, -45],
                [-36, -45],
                [-33, -45],
                [-30, -45],
                [-27, -45],
                [-24, -45],
                [-21, -45],
                [-18, -45],
                [-15, -45],
                [-12, -45],
                [-9, -45],
                [-6, -45],
                [-3, -45],
                [0, -45],
                [3, -45],
                [6, -45],
                [9, -45],
                [12, -45],
                [15, -45],
                [18, -45],
                [21, -45],
                [24, -45],
                [27, -45],
                [30, -45],
                [33, -45],
                [36, -45],
                [39, -45],
                [42, -45],
                [45, -45],
                [48, -45],
                [51, -45],
                [54, -45],
                [57, -45],
                [60, -45],
                [63, -45],
                [66, -45],
                [69, -45],
                [72, -45],
                [75, -45],
                [78, -45],
                [81, -45],
                [84, -45],
                [87, -45],
                [90, -45],
            ],
        },
        {
            "type": "LineString",
            "coordinates": [
                [-90, 0],
                [-87, 0],
                [-84, 0],
                [-81, 0],
                [-78, 0],
                [-75, 0],
                [-72, 0],
                [-69, 0],
                [-66, 0],
                [-63, 0],
                [-60, 0],
                [-57, 0],
                [-54, 0],
                [-51, 0],
                [-48, 0],
                [-45, 0],
                [-42, 0],
                [-39, 0],
                [-36, 0],
                [-33, 0],
                [-30, 0],
                [-27, 0],
                [-24, 0],
                [-21, 0],
                [-18, 0],
                [-15, 0],
                [-12, 0],
                [-9, 0],
                [-6, 0],
                [-3, 0],
                [0, 0],
                [3, 0],
                [6, 0],
                [9, 0],
                [12, 0],
                [15, 0],
                [18, 0],
                [21, 0],
                [24, 0],
                [27, 0],
                [30, 0],
                [33, 0],
                [36, 0],
                [39, 0],
                [42, 0],
                [45, 0],
                [48, 0],
                [51, 0],
                [54, 0],
                [57, 0],
                [60, 0],
                [63, 0],
                [66, 0],
                [69, 0],
                [72, 0],
                [75, 0],
                [78, 0],
                [81, 0],
                [84, 0],
                [87, 0],
                [90, 0],
            ],
        },
    ]


def test_graticule_22():
    g = (
        d3.geo_graticule()
        .set_extent([[-90, -45], [90, 45]])
        .set_step([45, 45])
        .set_precision(3)
    )
    assert g() == {
        "type": "MultiLineString",
        "coordinates": list(map(lambda line: line["coordinates"], g.lines())),
    }


def test_graticule_23():
    assert (
        d3.geo_graticule()
        .set_extent_major([[-90, -45], [90, 45]])
        .set_precision(3)
        .outline()
    ) == {
        "type": "Polygon",
        "coordinates": [
            [
                [-90, -45],
                [-90, 45],
                [-87, 45],
                [-84, 45],
                [-81, 45],
                [-78, 45],
                [-75, 45],
                [-72, 45],
                [-69, 45],
                [-66, 45],
                [-63, 45],
                [-60, 45],
                [-57, 45],
                [-54, 45],
                [-51, 45],
                [-48, 45],
                [-45, 45],
                [-42, 45],
                [-39, 45],
                [-36, 45],
                [-33, 45],
                [-30, 45],
                [-27, 45],
                [-24, 45],
                [-21, 45],
                [-18, 45],
                [-15, 45],
                [-12, 45],
                [-9, 45],
                [-6, 45],
                [-3, 45],
                [0, 45],
                [3, 45],
                [6, 45],
                [9, 45],
                [12, 45],
                [15, 45],
                [18, 45],
                [21, 45],
                [24, 45],
                [27, 45],
                [30, 45],
                [33, 45],
                [36, 45],
                [39, 45],
                [42, 45],
                [45, 45],
                [48, 45],
                [51, 45],
                [54, 45],
                [57, 45],
                [60, 45],
                [63, 45],
                [66, 45],
                [69, 45],
                [72, 45],
                [75, 45],
                [78, 45],
                [81, 45],
                [84, 45],
                [87, 45],
                [90, 45],
                [90, -45],
                [87, -45],
                [84, -45],
                [81, -45],
                [78, -45],
                [75, -45],
                [72, -45],
                [69, -45],
                [66, -45],
                [63, -45],
                [60, -45],
                [57, -45],
                [54, -45],
                [51, -45],
                [48, -45],
                [45, -45],
                [42, -45],
                [39, -45],
                [36, -45],
                [33, -45],
                [30, -45],
                [27, -45],
                [24, -45],
                [21, -45],
                [18, -45],
                [15, -45],
                [12, -45],
                [9, -45],
                [6, -45],
                [3, -45],
                [0, -45],
                [-3, -45],
                [-6, -45],
                [-9, -45],
                [-12, -45],
                [-15, -45],
                [-18, -45],
                [-21, -45],
                [-24, -45],
                [-27, -45],
                [-30, -45],
                [-33, -45],
                [-36, -45],
                [-39, -45],
                [-42, -45],
                [-45, -45],
                [-48, -45],
                [-51, -45],
                [-54, -45],
                [-57, -45],
                [-60, -45],
                [-63, -45],
                [-66, -45],
                [-69, -45],
                [-72, -45],
                [-75, -45],
                [-78, -45],
                [-81, -45],
                [-84, -45],
                [-87, -45],
                [-90, -45],
            ]
        ],
    }
